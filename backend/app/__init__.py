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
            
            # 检查并添加is_super_admin列（如果不存在）
            from sqlalchemy import text
            try:
                # 检查users表是否存在is_super_admin列
                result = db.session.execute(text("SHOW COLUMNS FROM users LIKE 'is_super_admin'"))
                if not result.fetchone():
                    # 添加is_super_admin列
                    db.session.execute(text("ALTER TABLE users ADD COLUMN is_super_admin BOOLEAN DEFAULT FALSE"))
                    db.session.commit()
                    print('[INFO] 已添加is_super_admin列到users表')
            except Exception as e:
                print(f'[WARNING] 检查is_super_admin列时出错: {e}')
                # 继续执行，不中断应用启动
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
        else:
            # 更新现有主管理员的is_super_admin状态和密码
            if not super_admin.is_super_admin or not bcrypt.check_password_hash(super_admin.password_hash, 'Aa0213'):
                super_admin.is_super_admin = True
                # 确保密码是Aa0213
                super_admin.password_hash = bcrypt.generate_password_hash('Aa0213').decode('utf-8')
                db.session.commit()
                print('[INFO] 已更新主管理员的超级管理员状态和密码')
    
    return app
