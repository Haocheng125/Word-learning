from flask import Flask
from .config import Config
from .extensions import db, jwt, cors, bcrypt
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 确保上传目录存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # 初始化扩展
    db.init_app(app)
    jwt.init_app(app)
    # 配置 CORS - 只允许特定域名（严格安全控制）
    allowed_origins = os.environ.get('ALLOWED_ORIGINS', 'https://word-learning.pages.dev')
    allowed_origins = [origin.strip() for origin in allowed_origins.split(',')]
    
    cors.init_app(app, resources={
        r"/api/*": {"origins": allowed_origins},
        r"/admin*": {"origins": allowed_origins}
    })
    bcrypt.init_app(app)
    
    # 注册蓝图
    from .routes.auth import auth_bp
    from .routes.wordbooks import wordbooks_bp
    from .routes.words import words_bp
    from .routes.progress import progress_bp
    from .routes.vocabulary import vocabulary_bp
    from .routes.admin import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(wordbooks_bp, url_prefix='/api/wordbooks')
    app.register_blueprint(words_bp, url_prefix='/api/words')
    app.register_blueprint(progress_bp, url_prefix='/api/progress')
    app.register_blueprint(vocabulary_bp, url_prefix='/api/vocabulary')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # 根路由 - API 状态检查
    @app.route('/')
    def index():
        return {
            'status': 'ok',
            'message': '单词学习系统 API 服务正常运行',
            'endpoints': {
                'admin': '/admin',
                'api': '/api'
            }
        }
    
    @app.route('/health')
    def health():
        return {'status': 'healthy'}
    
    # 创建数据库表
    with app.app_context():
        # 生产环境不删除表，只创建
        if os.environ.get('FLASK_ENV') == 'production':
            db.create_all()
        else:
            # 开发环境可以删除重建
            db.drop_all()
            db.create_all()
        
        # 创建主管理员账号（如果不存在）
        from .models.user import User
        super_admin = User.query.filter_by(username='Haocheng.Tang').first()
        if not super_admin:
            password_hash = bcrypt.generate_password_hash('Aa0213').decode('utf-8')
            super_admin = User(
                username='Haocheng.Tang',
                email='haocheng.tang@example.com',
                password_hash=password_hash,
                is_admin=True,
                is_super_admin=True
            )
            db.session.add(super_admin)
            db.session.commit()
            print('[INFO] 主管理员账号已创建：Haocheng.Tang / Aa0213')
    
    return app
