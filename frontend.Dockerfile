# 前端 Dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# 构建参数
ARG VITE_API_BASE_URL=https://lain05.zeabur.app/api
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

# 安装依赖并构建
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# 使用 nginx
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html

# 简单的 nginx 配置
RUN echo 'server { listen \${PORT:-80}; location / { root /usr/share/nginx/html; index index.html; try_files \$uri \$uri/ /index.html; } }' > /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
