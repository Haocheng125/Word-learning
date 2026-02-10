FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 复制 backend 目录下的依赖文件
COPY backend/requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制整个 backend 目录
COPY backend/ .

# 创建上传目录
RUN mkdir -p uploads

# 暴露端口（Zeabur 会自动使用 PORT 环境变量）
EXPOSE 8080

# 创建启动脚本
RUN echo '#!/bin/sh' > /start.sh && \
    echo 'echo "Starting application on port $PORT..."' >> /start.sh && \
    echo 'python -c "from app import create_app; from app.extensions import db; app = create_app(); app.app_context().push(); db.create_all(); print(\"Database initialized!\")" || echo "DB init skipped"' >> /start.sh && \
    echo 'exec gunicorn -w 4 -b 0.0.0.0:$PORT wsgi:app' >> /start.sh && \
    chmod +x /start.sh

# 启动命令
CMD ["/start.sh"]
