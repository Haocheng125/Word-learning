# 单词学习系统

基于 Flask + Vue3 的单词学习网站。

## 项目结构

```
单词网站/
├── backend/          # 后端（Flask）
│   ├── app/
│   │   ├── models/   # 数据模型
│   │   ├── routes/   # 路由
│   │   └── services/ # 业务逻辑
│   └── requirements.txt
├── frontend/         # 前端（Vue3 + Vite）
│   └── src/
└── 桌面版/           # 桌面版应用
```

## 本地运行

### 后端

```bash
cd backend
pip install -r requirements.txt
python wsgi.py
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

## 管理员账号

- 用户名：Haocheng.Tang
- 密码：Aa050213

## 功能

- 用户注册/登录
- 单词书浏览
- 在线学习
- 生词本管理
- 管理员后台
