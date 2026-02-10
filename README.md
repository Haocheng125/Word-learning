# 单词学习系统

一个基于 Flask + Vue3 的单词学习网站，支持 Excel 词库导入、在线学习和生词本管理。

> 🌐 **在线访问**
> - 前端（用户端）: https://incomparable-llama-827043.netlify.app/
> - 后端（管理端）: https://lain05.zeabur.app/admin

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
- ✅ 词库上架/下架管理
- ✅ 词库删除和下载
- ✅ 系统统计数据

## 🔧 技术栈

- **前端**: Vue 3 + Vite + Vue Router + Pinia
- **后端**: Flask + SQLAlchemy + Flask-JWT-Extended
- **数据库**: MySQL 8.0
- **容器**: Docker + Docker Compose
- **Excel 解析**: openpyxl

## 📝 词库格式

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

## 🛠️ 开发维护

### 本地开发命令

```bash
# 后端开发
cd backend
python wsgi.py  # 启动服务 (端口 5000)

# 前端开发
cd frontend
npm run dev     # 启动服务 (端口 4000)
npm run build   # 构建生产版本
```

### Docker 管理

```bash
# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f backend
docker-compose logs -f frontend

# 重启服务
docker-compose restart

# 重新构建
docker-compose up -d --build

# 停止服务
docker-compose down
```

### 生产部署

**前端**：使用 Netlify Drop 部署 `frontend/dist` 目录

**后端**：部署到 Zeabur 平台

## 📄 许可证

MIT License
