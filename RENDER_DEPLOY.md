# Render 部署指南

本指南将帮助你将单词学习系统的后端部署到 Render 平台。

## 📋 前置条件

1. 一个 Render 账号（https://render.com）
2. 代码已推送到 Gitee/GitHub 仓库

## 🚀 部署步骤

### 方法一：使用 render.yaml 自动部署（推荐）

1. **登录 Render**
   - 访问 https://render.com
   - 使用 GitHub/GitLab 账号登录

2. **新建 Blueprint**
   - 点击右上角的 "New +"
   - 选择 "Blueprint"
   - 连接你的 Gitee/GitHub 仓库
   - 选择包含 `render.yaml` 的分支
   - 点击 "Apply"

3. **等待部署**
   - Render 会自动：
     - 创建 PostgreSQL 数据库
     - 构建并部署后端服务
     - 配置环境变量
   - 部署完成后，你会获得一个类似 `https://word-learning-backend.onrender.com` 的地址

### 方法二：手动部署

#### 1. 创建数据库

1. 登录 Render
2. 点击 "New +" → "PostgreSQL"
3. 填写信息：
   - Name: `word-learning-db`
   - Database: `word_learning`
   - User: `word_learning`
   - Plan: Free
4. 点击 "Create Database"
5. 等待数据库创建完成，复制 `Internal Connection String`

#### 2. 创建 Web 服务

1. 点击 "New +" → "Web Service"
2. 连接你的 Gitee/GitHub 仓库
3. 配置服务：
   - Name: `word-learning-backend`
   - Region: 选择离你最近的
   - Branch: `main`
   - Root Directory: 留空（或填 `backend`）
   - Runtime: Python 3
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `gunicorn --chdir backend wsgi:app`
   - Plan: Free
4. 点击 "Create Web Service"

#### 3. 配置环境变量

在 Web 服务页面，点击 "Environment" → "Add Environment Variable"，添加：

| 变量名 | 值 |
|--------|-----|
| `FLASK_ENV` | `production` |
| `DATABASE_URL` | 从 PostgreSQL 页面复制的 `Internal Connection String` |
| `SECRET_KEY` | （点击 "Generate" 自动生成） |
| `JWT_SECRET_KEY` | （点击 "Generate" 自动生成） |

点击 "Save Changes"，服务会自动重新部署。

## 🌐 访问你的应用

部署成功后，你会看到类似这样的地址：
- 后端: `https://word-learning-backend.onrender.com`
- 管理后台: `https://word-learning-backend.onrender.com/admin`

## 📝 更新前端配置

将前端的 API 地址更新为你的 Render 后端地址。

## ⚠️ 注意事项

1. **免费计划限制**：
   - Web 服务在 15 分钟无活动后会休眠
   - 首次访问可能需要 30-60 秒唤醒
   - 数据库有存储限制

2. **数据库初始化**：
   - 首次部署后，需要运行数据库初始化
   - 可以通过管理后台上传词库来测试

3. **文件上传**：
   - Render 的免费计划不提供持久化文件存储
   - 上传的文件在服务重启后会丢失
   - 如需持久化存储，建议使用云存储服务（如 AWS S3、阿里云 OSS）

## 🔧 故障排查

### 部署失败
- 检查 `requirements.txt` 中的依赖是否正确
- 查看 Render 的日志（Logs 标签页）

### 数据库连接失败
- 确认 `DATABASE_URL` 环境变量已正确设置
- 检查数据库是否已就绪

### 服务无法访问
- 确认服务状态为 "Live"
- 检查环境变量配置
- 查看服务日志

## 📚 更多资源

- Render 官方文档: https://render.com/docs
- Flask 部署指南: https://render.com/docs/deploy-flask
