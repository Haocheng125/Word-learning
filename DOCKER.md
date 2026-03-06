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
# 构建并启动所有服务（后台运行）
docker-compose up -d

# 构建并启动（显示日志）
docker-compose up

# 强制重新构建镜像
docker-compose up -d --build
```

### 3. 访问服务

- 前端页面: http://localhost
- 后端 API: http://localhost:5000
- 管理后台: http://localhost:5000/admin

### 4. 停止服务

```bash
# 停止服务（保留容器和数据）
docker-compose stop

# 停止并删除容器
docker-compose down

# 停止并删除容器和数据卷（清空数据库）
docker-compose down -v
```

## 服务说明

| 服务 | 端口 | 说明 |
|------|------|------|
| frontend | 80 | Nginx + Vue3 前端 |
| backend | 5000 | Flask 后端 API |
| db | 3306 | MySQL 数据库 |

## 常用命令

### 查看日志

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看后端日志
docker-compose logs -f backend

# 查看前端日志
docker-compose logs -f frontend

# 查看数据库日志
docker-compose logs -f db

# 查看最近100行日志
docker-compose logs --tail=100 backend
```

### 服务管理

```bash
# 重启所有服务
docker-compose restart

# 重启单个服务
docker-compose restart backend

# 重新构建并重启
docker-compose up -d --build --force-recreate

# 查看运行状态
docker-compose ps

# 查看资源使用
docker-compose top
```

### 进入容器

```bash
# 进入后端容器
docker-compose exec backend sh

# 进入前端容器
docker-compose exec frontend sh

# 进入数据库容器
docker-compose exec db mysql -uroot -p

# 进入数据库容器（bash）
docker-compose exec db bash
```

### 数据库操作

```bash
# 备份数据库
docker-compose exec db mysqldump -uroot -p word_learning > backup.sql

# 恢复数据库
docker-compose exec -T db mysql -uroot -p word_learning < backup.sql

# 查看数据库状态
docker-compose exec db mysql -uroot -p -e "SHOW DATABASES;"
```

### 清理操作

```bash
# 删除所有停止的容器
docker container prune

# 删除未使用的镜像
docker image prune

# 删除未使用的数据卷
docker volume prune

# 清理所有（容器、镜像、卷、网络）
docker system prune -a
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

## 开发模式

### 仅启动后端和数据库

```bash
# 启动后端和数据库
docker-compose up -d backend db

# 前端使用本地开发服务器
npm run dev
```

### 热重载开发

修改 `docker-compose.yml` 添加 volumes 挂载：

```yaml
backend:
  volumes:
    - ./backend:/app
    - ./uploads:/app/uploads
  environment:
    - FLASK_ENV=development
    - FLASK_DEBUG=1
```

## 故障排查

### 端口冲突

```bash
# 查看端口占用
netstat -ano | findstr :5000
netstat -ano | findstr :3306

# 停止占用端口的进程
docker-compose down
```

### 容器无法启动

```bash
# 查看容器日志
docker-compose logs backend

# 检查容器状态
docker-compose ps

# 重新构建
docker-compose up -d --build --force-recreate
```

### 数据库连接失败

```bash
# 检查数据库容器状态
docker-compose ps db

# 查看数据库日志
docker-compose logs db

# 重启数据库
docker-compose restart db
```

## 生产部署建议

1. **修改默认密码**：务必修改 `SECRET_KEY`、`JWT_SECRET_KEY` 和 `MYSQL_ROOT_PASSWORD`
2. **使用 HTTPS**：配置 SSL 证书
3. **限制端口暴露**：只暴露必要的端口
4. **定期备份**：设置数据库自动备份
5. **监控日志**：配置日志收集和分析
