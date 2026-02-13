# Railway 部署指南

本指南将帮助你将单词学习系统的后端部署到 Railway 平台（无需银行卡）。

## 📋 前置条件

1. 一个 Railway 账号（https://railway.app）
2. 代码已推送到 Gitee/GitHub 仓库

## 🚀 部署步骤

### 1. 注册并登录 Railway

1. 访问 https://railway.app
2. 点击 "Login"
3. 使用 GitHub/GitLab 账号登录（**不需要银行卡！**）

### 2. 新建项目

1. 登录后，点击 "New Project"
2. 选择 "Deploy from GitHub repo"
3. 连接你的 GitHub/GitLab 账号
4. 选择你的仓库（word-learning）
5. 选择分支：`main`

### 3. 添加数据库

1. 在项目页面，点击 "New" → "Database"
2. 选择 "MySQL"
3. 点击 "Add MySQL"
4. 等待数据库创建完成

### 4. 配置环境变量

1. 在项目页面，点击你的 Web 服务
2. 点击 "Variables" 标签
3. 添加以下环境变量：

| 变量名 | 值 |
|--------|-----|
| `FLASK_ENV` | `production` |
| `DATABASE_URL` | （从 MySQL 服务复制 `DATABASE_URL`） |
| `SECRET_KEY` | （点击 "Generate" 自动生成） |
| `JWT_SECRET_KEY` | （点击 "Generate" 自动生成） |

**如何获取 DATABASE_URL：**
- 点击 MySQL 服务
- 在 "Variables" 中找到 `DATABASE_URL`
- 复制它的值

### 5. 配置构建和启动命令

1. 在 Web 服务页面，点击 "Settings"
2. 找到 "Build & Deploy" 部分
3. 设置：
   - **Build Command**: 留空（Railway 会自动检测）
   - **Start Command**: `gunicorn --chdir backend wsgi:app`
4. 点击 "Save"

### 6. 部署

1. 配置完成后，Railway 会自动开始部署
2. 等待部署完成（通常需要 2-5 分钟）
3. 部署成功后，你会看到一个绿色的 "Live" 状态

### 7. 访问你的应用

部署成功后，点击 Web 服务右上角的域名，你会获得类似这样的地址：
- 后端: `https://word-learning-backend.up.railway.app`
- 管理后台: `https://word-learning-backend.up.railway.app/admin`

## ⚙️ 可选：使用 railway.json 配置

如果你想使用 `railway.json` 配置文件：

1. 确保 `railway.json` 在仓库根目录
2. 推送代码到 GitHub
3. Railway 会自动读取配置

## 📝 更新前端配置

将前端的 API 地址更新为你的 Railway 后端地址。

## ⚠️ 注意事项

### 免费计划限制

1. **运行时间**：
   - 每月 500 小时（约 20 天）
   - 超过后服务会暂停，下月重置

2. **数据库**：
   - 1 GB 存储
   - 足够小项目使用

3. **文件上传**：
   - Railway 的文件系统是临时的
   - 上传的文件在重新部署后会丢失
   - 如需持久化存储，建议使用云存储服务

### 唤醒服务

如果服务休眠了，访问一次网址就会自动唤醒（可能需要 30-60 秒）。

## 🔧 故障排查

### 部署失败
- 检查 `requirements.txt` 中的依赖
- 查看 Railway 的日志（Deployments 标签页）

### 数据库连接失败
- 确认 `DATABASE_URL` 环境变量已正确设置
- 检查数据库是否已就绪

### 服务无法访问
- 确认服务状态为 "Live"
- 检查环境变量配置
- 查看服务日志

### 端口问题
- Railway 会自动分配端口，使用 `$PORT` 环境变量
- 不需要在代码中硬编码端口 5000

## 📚 更多资源

- Railway 官方文档: https://docs.railway.app
- Railway Python 部署: https://docs.railway.app/guides/python
