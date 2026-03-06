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
    
    # 配置 CORS
    allowed_origins = os.environ.get('ALLOWED_ORIGINS', '*')
    if allowed_origins != '*':
        allowed_origins = [origin.strip() for origin in allowed_origins.split(',')]
    
    cors.init_app(app, resources={
        r"/api/*": {"origins": allowed_origins, "supports_credentials": True},
        r"/admin*": {"origins": allowed_origins, "supports_credentials": True}
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
    
    # 根路由
    @app.route('/')
    def index():
        return {
            'status': 'ok',
            'message': '单词学习系统 API',
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
        try:
            db.create_all()
            
            # 创建主管理员账号
            from .models.user import User
            super_admin = User.query.filter_by(username='Haocheng.Tang').first()
            if not super_admin:
                password_hash = bcrypt.generate_password_hash('Aa050213').decode('utf-8')
                super_admin = User(
                    username='Haocheng.Tang',
                    email='haocheng.tang@example.com',
                    password_hash=password_hash,
                    is_admin=True,
                    is_super_admin=True
                )
                db.session.add(super_admin)
                db.session.commit()
        except Exception as e:
            print(f'数据库初始化失败: {str(e)}')
            print('应用将继续运行，但数据库功能可能不可用')
    
    return app
