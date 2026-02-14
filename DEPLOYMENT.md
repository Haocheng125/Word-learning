# 部署指南

## 📋 完整部署方案

### 后端部署到 Railway

#### 1. Railway 部署步骤

1. **登录 Railway**：访问 https://railway.app/
2. **创建新项目**：
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 选择你的仓库（word-learning）
3. **添加数据库**：
   - 在项目中点击 "Add Service" → "Database" → "PostgreSQL"
4. **配置环境变量**：
   - 在后端服务中设置以下环境变量：
     - `DATABASE_URL`：Railway 会自动提供（无需手动设置）
     - `SECRET_KEY`：设置一个强密钥
     - `FLASK_ENV`：`production`
     - `ALLOWED_ORIGINS`：你的 Cloudflare Pages 域名（例如 `https://your-app.pages.dev`）
5. **部署**：
   - 点击 "Deploy" 开始部署

---

### 前端部署到 Cloudflare Pages

#### 2. Cloudflare Pages 部署步骤

1. **登录 Cloudflare**：访问 https://dash.cloudflare.com/
2. **进入 Pages**：
   - 点击 "Workers & Pages"
   - 点击 "Create application"
   - 选择 "Pages" 标签
3. **连接 Git 仓库**：
   - 点击 "Connect to Git"
   - 选择你的 GitHub/Gitee 仓库
4. **配置构建设置**：
   - **Project name**: word-learning（或你喜欢的名字）
   - **Production branch**: `main`
   - **Framework preset**: `Vite`
   - **Build command**: `npm run build`
   - **Build output directory**: `dist`
   - **Root directory**: `frontend`
5. **环境变量**：
   - 在项目设置中添加环境变量：
     - `VITE_API_BASE_URL`: 你的 Railway 后端地址（例如 `https://your-railway-app.up.railway.app/api`）
6. **部署**：
   - 点击 "Save and Deploy"

---

## 🎯 域名配置

### Cloudflare Pages 域名
Cloudflare Pages 会自动提供一个免费的域名：`https://your-project-name.pages.dev`

你也可以绑定你自己的域名。

---

## 📝 本地开发 vs 生产环境

| 环境 | 前端地址 | 后端地址 |
|------|-----------|-----------|
| 本地开发 | http://localhost:4000 | http://localhost:5000 |
| 生产环境 | https://your-app.pages.dev | https://your-railway-app.up.railway.app |

---

## ⚙️ 环境变量说明

### 后端环境变量（Railway）
- `DATABASE_URL`：数据库连接字符串（自动设置）
- `SECRET_KEY`：JWT 密钥
- `FLASK_ENV`：`production` 或 `development`
- `ALLOWED_ORIGINS`：允许的前端域名

### 前端环境变量（Cloudflare Pages）
- `VITE_API_BASE_URL`：后端 API 地址

---

## 🔄 更新部署

### 更新后端
1. 推送代码到 GitHub/Gitee
2. Railway 会自动重新部署

### 更新前端
1. 推送代码到 GitHub/Gitee
2. Cloudflare Pages 会自动重新部署
