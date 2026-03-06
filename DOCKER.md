# Docker 本地部署指南

## 快速开始

### 1. 安装 Docker

确保已安装 Docker 和 Docker Compose：
```bash
docker --version
docker-compose --version
```

### 2. 启动所有服务

```bash
docker-compose up -d
```

### 3. 访问服务

- 前端页面: http://localhost
- 后端 API: http://localhost:5000
- 管理后台: http://localhost:5000/admin

### 4. 停止服务

```bash
docker-compose down
```

## 服务说明

| 服务 | 端口 | 说明 |
|------|------|------|
| frontend | 80 | Nginx + Vue3 前端 |
| backend | 5000 | Flask 后端 API |
| db | 3306 | MySQL 数据库 |

## 常用命令

```bash
# 查看所有日志
docker-compose logs -f

# 查看后端日志
docker-compose logs -f backend

# 查看前端日志
docker-compose logs -f frontend

# 重启服务
docker-compose restart

# 重建镜像
docker-compose up -d --build

# 进入后端容器
docker-compose exec backend sh

# 进入数据库容器
docker-compose exec db mysql -uroot -p
```

## 配置说明

### 环境变量

在 `docker-compose.yml` 中修改以下配置：

- `SECRET_KEY`: 应用密钥（建议修改）
- `JWT_SECRET_KEY`: JWT 密钥（建议修改）
- `MYSQL_ROOT_PASSWORD`: 数据库 root 密码（建议修改）

### 数据持久化

- 数据库数据: Docker Volume `mysql_data`
- 上传文件: 映射到 `./uploads` 目录

## 仅启动后端（开发模式）

如果只需要后端服务：

```bash
docker-compose up -d backend db
```

然后前端使用 `npm run dev` 本地开发。
