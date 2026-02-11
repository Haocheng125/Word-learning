# 单词学习系统

一个基于 Flask + Vue3 的单词学习网站，支持 Excel 词库导入、在线学习和生词本管理。

> 🌐 **在线访问**
> - 前端（用户端）: https://incomparable-llama-827043.netlify.app/
> - 后端（管理端）: https://lain05.zeabur.app/admin
>
> 🖥️ **本地运行地址**
> - 前端（用户端）: http://localhost:4000
> - 后端（管理端）: http://localhost:5000/admin

## 📁 项目结构

```
单词网站/
├── backend/                 # 后端（Flask）
│   ├── app/
│   │   ├── models/         # 数据模型
│   │   ├── routes/         # 路由
│   │   ├── services/       # 业务逻辑（Excel解析器）
│   │   └── templates/      # Jinja2 模板（管理后台）
│   ├── requirements.txt    # Python 依赖
│   └── wsgi.py            # 应用入口
├── frontend/               # 前端（Vue3 + Vite）
│   ├── src/
│   │   ├── api/           # API 接口
│   │   ├── components/    # 组件
│   │   ├── router/        # 路由
│   │   ├── stores/        # 状态管理
│   │   └── views/         # 页面
│   └── package.json
├── docker/                # Docker 配置
│   ├── backend.Dockerfile
│   ├── frontend.Dockerfile
│   └── nginx.conf
├── docker-compose.yml     # 容器编排
└── init.sql              # 数据库初始化
```

## 🚀 快速开始

### 本地开发

1. **安装依赖**
```bash
# 后端
cd backend
pip install -r requirements.txt

# 前端
cd ../frontend
npm install
```

2. **启动服务**
```bash
# 后端 (端口 5000)
cd backend
python wsgi.py

# 前端 (端口 4000)
cd frontend
npm run dev
```

3. **访问应用**
- 前端（用户端）: http://localhost:4000
- 后端（管理端）: http://localhost:5000/admin

### Docker 部署

```bash
docker-compose up -d
```

访问地址：
- 前端: http://localhost:80
- 后端: http://localhost:5000/admin

## ✨ 主要功能

### 用户端
- ✅ 用户注册/登录
- ✅ 选择词库开始学习
- ✅ 单词卡片翻转显示释义
- ✅ 学习进度保存
- ✅ 生词本管理

### 管理端
- ✅ Excel 词库上传（自动解析 Word 和 Meaning 列）
- ✅ PDF 词库上传（自动转换为 Excel 并导入）
- ✅ 词库上架/下架管理
- ✅ 词库删除和下载
- ✅ 词库单词列表查看和导出
- ✅ 系统统计数据

## 🔧 技术栈

- **前端**: Vue 3 + Vite + Vue Router + Pinia
- **后端**: Flask + SQLAlchemy + Flask-JWT-Extended
- **数据库**: MySQL 8.0
- **容器**: Docker + Docker Compose
- **Excel 解析**: openpyxl
- **PDF 解析**: pdfplumber + pandas

## 📝 词库格式

### Excel 格式
支持的 Excel 格式：
- 第一行可包含表头（Word, Meaning）
- Word 列：英文单词（支持换行符分隔的音标）
- Meaning 列：中文释义
- 支持多列格式（自动识别所有 Word 和 Meaning 列）

示例：
```
| Word                      | Meaning          |
|---------------------------|------------------|
| atmosphere\n[ˈætməsfɪə]   | n. 大气；气氛    |
| hydrosphere               | n. 水圈          |
```

### PDF 格式
支持的 PDF 格式：
- 包含表格结构的 PDF 文件
- 表格应包含英文单词、音标、中文释义等列
- 支持跨行合并的复杂表格结构
- 自动识别并提取表格数据转换为词库

## 🔐 环境变量

复制 `.env.example` 到 `.env` 并修改：

```env
MYSQL_ROOT_PASSWORD=your_password
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
```

## 📦 数据持久化

数据存储在 Docker volumes 中：
- `mysql_data`: 数据库数据
- `uploads_data`: 上传的 Excel 文件

## 🛠️ 本地运行指南

### 环境准备

1. **安装 Python 3.8+**
2. **安装 Node.js 16+**
3. **安装 MySQL 8.0**（或使用 Docker）

### 本地开发启动

```bash
# 1. 克隆项目
git clone <repository-url>
cd 单词网站

# 2. 后端环境搭建
cd backend
pip install -r requirements.txt

# 3. 前端环境搭建
cd ../frontend
npm install

# 4. 配置环境变量
cp ../.env.example .env
# 编辑 .env 文件，设置数据库密码等

# 5. 启动后端服务 (端口 5000)
cd ../backend
python wsgi.py

# 6. 启动前端服务 (端口 4000，新终端)
cd frontend
npm run dev
```

### 访问地址

- **前端（用户端）**: http://localhost:4000
- **后端（管理端）**: http://localhost:5000/admin
- **API 接口**: http://localhost:5000/api

### 管理后台功能

访问 http://localhost:5000/admin 后可以：

1. **上传词库**
   - Excel 上传：直接上传 Excel 文件
   - PDF 上传：上传 PDF 文件，系统自动转换为词库

2. **管理词库**
   - 查看所有词库列表
   - 上架/下架词库
   - 查看词库详细单词列表
   - 导出词库为 Excel
   - 删除词库

3. **系统监控**
   - 查看用户统计
   - 查看词库统计
   - 查看单词总数

### 数据库初始化

```sql
-- 创建数据库
CREATE DATABASE word_learning CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 运行 init.sql 初始化表结构
mysql -u root -p word_learning < init.sql
```

### Docker 本地部署

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看运行状态
docker-compose ps

# 查看日志
docker-compose logs -f backend
docker-compose logs -f frontend

# 重启服务
docker-compose restart

# 重新构建
docker-compose up -d --build

# 停止服务
docker-compose down

# 停止并删除数据卷
docker-compose down -v
```

访问地址：
- 前端: http://localhost:80
- 后端: http://localhost:5000/admin

### 生产部署

**前端部署**：
```bash
cd frontend
npm run build
# 将 dist 目录部署到 Netlify/Vercel/Cloudflare Pages 等平台
```

**后端部署**：
- 部署到 Zeabur 平台
- 需要配置环境变量：数据库连接、密钥等
- 确保上传文件夹权限设置正确

### 常见问题

1. **PDF 转换失败**
   - 确保 PDF 包含表格结构
   - 检查 PDF 是否为扫描版（需要 OCR）
   - 查看后端日志获取详细错误信息

2. **数据库连接失败**
   - 检查 MySQL 服务是否启动
   - 验证数据库连接参数
   - 确认数据库用户权限

3. **文件上传失败**
   - 检查 uploads 文件夹权限
   - 确认文件大小限制设置
   - 验证文件格式是否支持

## 📄 许可证

MIT License
