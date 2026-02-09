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
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
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
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    return app
