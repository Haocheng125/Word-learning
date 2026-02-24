# 腾飞AI科技企业网站系统

## 项目结构

```
Web/
├── front_web/          # 前端展示网站
│   ├── index.html      # 主页面
│   ├── js/
│   │   ├── config.js   # API配置
│   │   └── api.js      # API调用封装
│   └── images/         # 图片资源
├── admin_web/          # 管理后台
│   ├── index.html      # 管理后台页面
│   ├── css/
│   │   └── admin.css   # 后台样式
│   └── js/
│       └── admin.js    # 后台逻辑
└── backend_service/    # 后端服务
    ├── pom.xml         # Maven配置
    └── src/main/
        ├── java/       # Java源码
        └── resources/  # 配置文件
```

## 功能说明

### 1. 前端展示网站 (front_web)
- 展示企业信息、产品服务、成功案例
- 用户咨询表单提交
- 响应式设计，支持移动端

### 2. 管理后台 (admin_web)
- 登录系统（用户名：admin，密码：admin123）
- 管理关于我们、联系我们信息
- 管理产品与服务列表
- 管理成功案例列表
- 查看和管理用户咨询记录

### 3. 后端服务 (backend_service)
- Spring Boot框架
- MySQL数据库（localhost:3306/comdb）
- RESTful API接口
- 数据库自动建表

## 使用步骤

### 1. 准备MySQL数据库

确保MySQL服务运行在 localhost:3306，并创建数据库：

```sql
CREATE DATABASE comdb DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. 启动后端服务

进入backend_service目录，使用Maven启动：

```bash
cd backend_service
mvn spring-boot:run
```

或者使用IDE（如IntelliJ IDEA）打开项目并运行 `EnterpriseApplication.java`

后端服务将在 http://localhost:8080 启动

### 3. 访问前端网站

使用浏览器打开：
- 前端展示: `front_web/index.html`
- 管理后台: `admin_web/index.html`

建议使用Live Server或HTTP服务器运行前端页面。

## API接口说明

### 关于我们
- GET `/api/about` - 获取关于我们信息
- POST `/api/about` - 保存/更新关于我们信息

### 联系我们
- GET `/api/contact` - 获取联系信息
- POST `/api/contact` - 保存/更新联系信息

### 产品与服务
- GET `/api/products` - 获取产品列表
- GET `/api/products/{id}` - 获取产品详情
- POST `/api/products` - 添加产品
- PUT `/api/products/{id}` - 更新产品
- DELETE `/api/products/{id}` - 删除产品

### 成功案例
- GET `/api/cases` - 获取案例列表
- GET `/api/cases/{id}` - 获取案例详情
- POST `/api/cases` - 添加案例
- PUT `/api/cases/{id}` - 更新案例
- DELETE `/api/cases/{id}` - 删除案例

### 用户咨询
- GET `/api/consultations` - 获取咨询列表
- POST `/api/consultations` - 提交咨询
- DELETE `/api/consultations/{id}` - 删除咨询

### 管理员登录
- POST `/api/admin/login` - 管理员登录

## 数据库表结构

系统会自动创建以下数据表：
- `about_us` - 关于我们信息
- `contact_info` - 联系我们信息
- `product_service` - 产品与服务
- `success_case` - 成功案例
- `consultation` - 用户咨询
- `admin_user` - 管理员用户（默认用户：admin/admin123）

## 技术栈

- 前端：HTML5, CSS3, JavaScript (原生)
- 后端：Spring Boot 2.7.14, JPA, MySQL
- 数据库：MySQL 8.0

## 注意事项

1. 确保MySQL服务正常运行
2. 确保数据库连接信息正确（用户名：root，密码：123456）
3. 首次启动会自动创建表结构和默认管理员账号
4. 修改管理后台内容后，前端网站会实时显示更新
5. 建议使用Chrome或Firefox浏览器访问
