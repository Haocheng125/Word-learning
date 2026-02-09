# 前端 Dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# 定义构建参数
ARG VITE_API_BASE_URL=https://lain05.zeabur.app/api
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

# 复制前端代码
COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build

# 使用 nginx 提供静态文件
FROM nginx:alpine

# 安装 envsubst 用于替换环境变量
RUN apk add --no-cache gettext

# 复制构建产物
COPY --from=builder /app/dist /usr/share/nginx/html

# 创建 nginx 配置模板
RUN echo 'server { \n\
    listen ${PORT}; \n\
    location / { \n\
        root /usr/share/nginx/html; \n\
        index index.html; \n\
        try_files $uri $uri/ /index.html; \n\
    } \n\
}' > /etc/nginx/conf.d/default.conf.template

# 创建启动脚本
RUN echo '#!/bin/sh' > /docker-entrypoint.sh && \
    echo 'export PORT=${PORT:-80}' >> /docker-entrypoint.sh && \
    echo 'envsubst '\''$PORT'\'' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf' >> /docker-entrypoint.sh && \
    echo 'nginx -g "daemon off;"' >> /docker-entrypoint.sh && \
    chmod +x /docker-entrypoint.sh

EXPOSE 80

CMD ["/docker-entrypoint.sh"]
