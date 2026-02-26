import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    ADMIN_KEY = os.environ.get('ADMIN_KEY', '0000')
    
    # 数据库配置 - 优先使用环境变量
    DATABASE_URL = (
        os.environ.get('DATABASE_URL') or 
        os.environ.get('MYSQL_URL') or 
        os.environ.get('MYSQLDATABASE_URL') or
        os.environ.get('POSTGRES_URL') or
        os.environ.get('POSTGRESQL_URL')
    )
    
    # 打印调试信息（生产环境可删除）
    print(f"[DEBUG] DATABASE_URL from env: {DATABASE_URL}")
    print(f"[DEBUG] All env vars: {dict(os.environ)}")
    
    if DATABASE_URL:
        # 处理 Railway/Render 提供的数据库 URL
        if DATABASE_URL.startswith('postgres://'):
            DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
        elif DATABASE_URL.startswith('mysql://'):
            DATABASE_URL = DATABASE_URL.replace('mysql://', 'mysql+pymysql://', 1)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
        print(f"[DEBUG] Using DATABASE_URL: {SQLALCHEMY_DATABASE_URI}")
    else:
        # 本地开发默认配置
        MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
        MYSQL_PORT = os.environ.get('MYSQL_PORT', '3306')
        MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
        MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'password')
        MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'word_learning')
        
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@"
            f"{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"
        )
        print(f"[DEBUG] Using local MySQL: {SQLALCHEMY_DATABASE_URI}")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT 配置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # 文件上传配置
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
