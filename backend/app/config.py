import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    ADMIN_KEY = os.environ.get('ADMIN_KEY', '0000')
    
    # 数据库配置
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    if DATABASE_URL:
        # 处理数据库 URL 协议
        if DATABASE_URL.startswith('postgres://'):
            DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
        elif DATABASE_URL.startswith('mysql://'):
            DATABASE_URL = DATABASE_URL.replace('mysql://', 'mysql+pymysql://', 1)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # 本地开发默认配置
        SQLALCHEMY_DATABASE_URI = 'sqlite:///word_learning.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT 配置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_SAMESITE = 'Lax'
    
    # 上传配置
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
