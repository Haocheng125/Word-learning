-- ============================================
-- 腾飞AI科技企业网站数据库初始化脚本
-- 数据库名称: comdb
-- 字符集: utf8mb4
-- 创建日期: 2026-01-16
-- ============================================

-- 1. 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS comdb 
DEFAULT CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 2. 使用数据库
USE comdb;

-- ============================================
-- 删除已存在的表（如果需要重新初始化）
-- ============================================
DROP TABLE IF EXISTS consultation;
DROP TABLE IF EXISTS success_case;
DROP TABLE IF EXISTS product_service;
DROP TABLE IF EXISTS contact_info;
DROP TABLE IF EXISTS about_us;
DROP TABLE IF EXISTS admin_user;

-- ============================================
-- 3. 创建管理员用户表
-- ============================================
CREATE TABLE admin_user (
    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    password VARCHAR(100) NOT NULL COMMENT '密码（需加密）',
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='管理员用户表';

-- ============================================
-- 4. 创建关于我们表
-- ============================================
CREATE TABLE about_us (
    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    title VARCHAR(200) COMMENT '标题',
    content TEXT COMMENT '内容描述',
    stat1_label VARCHAR(100) COMMENT '统计1标签',
    stat1_value VARCHAR(50) COMMENT '统计1数值',
    stat2_label VARCHAR(100) COMMENT '统计2标签',
    stat2_value VARCHAR(50) COMMENT '统计2数值',
    stat3_label VARCHAR(100) COMMENT '统计3标签',
    stat3_value VARCHAR(50) COMMENT '统计3数值',
    image_url VARCHAR(500) COMMENT '图片URL',
    updated_at DATETIME COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='关于我们表';

-- ============================================
-- 5. 创建联系信息表
-- ============================================
CREATE TABLE contact_info (
    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    address VARCHAR(200) COMMENT '地址',
    phone VARCHAR(50) COMMENT '电话',
    email VARCHAR(100) COMMENT '邮箱',
    working_hours VARCHAR(100) COMMENT '工作时间',
    updated_at DATETIME COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='联系信息表';

-- ============================================
-- 6. 创建产品服务表
-- ============================================
CREATE TABLE product_service (
    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    title VARCHAR(200) NOT NULL COMMENT '标题',
    icon VARCHAR(50) COMMENT '图标',
    description TEXT COMMENT '描述',
    image_url VARCHAR(500) COMMENT '图片URL',
    features TEXT COMMENT '特性列表（JSON格式）',
    display_order INT COMMENT '显示顺序',
    created_at DATETIME COMMENT '创建时间',
    updated_at DATETIME COMMENT '更新时间',
    INDEX idx_display_order (display_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='产品服务表';

-- ============================================
-- 7. 创建成功案例表
-- ============================================
CREATE TABLE success_case (
    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    title VARCHAR(200) NOT NULL COMMENT '标题',
    category VARCHAR(50) COMMENT '类别',
    description TEXT COMMENT '描述',
    image_url VARCHAR(500) COMMENT '图片URL',
    result1_label VARCHAR(100) COMMENT '成果1标签',
    result1_value VARCHAR(50) COMMENT '成果1数值',
    result2_label VARCHAR(100) COMMENT '成果2标签',
    result2_value VARCHAR(50) COMMENT '成果2数值',
    display_order INT COMMENT '显示顺序',
    created_at DATETIME COMMENT '创建时间',
    updated_at DATETIME COMMENT '更新时间',
    INDEX idx_category (category),
    INDEX idx_display_order (display_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='成功案例表';

-- ============================================
-- 8. 创建咨询表
-- ============================================
CREATE TABLE consultation (
    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    name VARCHAR(100) NOT NULL COMMENT '姓名',
    phone VARCHAR(50) COMMENT '电话',
    email VARCHAR(100) COMMENT '邮箱',
    company VARCHAR(200) COMMENT '公司',
    content TEXT COMMENT '咨询内容',
    created_at DATETIME COMMENT '创建时间',
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='咨询表';

-- ============================================
-- 初始化数据
-- ============================================

-- 插入默认管理员账号（用户名: admin, 密码: admin123）
-- 注意：这是明文密码，生产环境需要加密
INSERT INTO admin_user (username, password) VALUES 
('admin', 'admin123');

-- 插入关于我们示例数据
INSERT INTO about_us (title, content, stat1_label, stat1_value, stat2_label, stat2_value, stat3_label, stat3_value, updated_at) VALUES 
('关于腾飞AI科技', 
'腾飞AI科技是一家专注于人工智能技术研发与应用的创新型企业。我们致力于为企业提供智能化解决方案，帮助客户实现数字化转型。',
'服务客户', '500+',
'成功案例', '200+',
'团队成员', '100+',
NOW());

-- 插入联系信息示例数据
INSERT INTO contact_info (address, phone, email, working_hours, updated_at) VALUES 
('北京市海淀区中关村科技园', '010-12345678', 'contact@tengfei-ai.com', '周一至周五 9:00-18:00', NOW());

-- 插入产品服务示例数据
INSERT INTO product_service (title, icon, description, features, display_order, created_at, updated_at) VALUES 
('智能客服系统', 'chat', '基于自然语言处理技术的智能客服解决方案，7x24小时在线服务', 
'["多轮对话理解","情感识别","知识库管理","多渠道接入"]', 1, NOW(), NOW()),

('数据分析平台', 'chart', '企业级大数据分析平台，助力数据驱动决策', 
'["实时数据处理","可视化报表","预测分析","自定义看板"]', 2, NOW(), NOW()),

('AI视觉识别', 'eye', '计算机视觉解决方案，支持图像识别、物体检测等功能', 
'["人脸识别","物体检测","OCR文字识别","质量检测"]', 3, NOW(), NOW());

-- 插入成功案例示例数据
INSERT INTO success_case (title, category, description, result1_label, result1_value, result2_label, result2_value, display_order, created_at, updated_at) VALUES 
('某电商平台智能客服系统', '电商', '为大型电商平台打造智能客服系统，显著提升用户满意度', 
'响应速度提升', '300%', '客服成本降低', '60%', 1, NOW(), NOW()),

('制造业质量检测系统', '制造业', '基于AI视觉技术的产品质量检测系统，提高生产效率', 
'检测准确率', '99.5%', '人力成本节省', '70%', 2, NOW(), NOW()),

('金融风控大数据平台', '金融', '为金融机构提供智能风控解决方案，有效降低风险', 
'风险识别率', '95%', '审核效率提升', '400%', 3, NOW(), NOW());

-- 插入咨询示例数据（可选）
INSERT INTO consultation (name, phone, email, company, content, created_at) VALUES 
('张三', '13800138000', 'zhangsan@example.com', '示例科技公司', '希望了解智能客服系统的详细方案', NOW());

-- ============================================
-- 查询验证
-- ============================================
SELECT '数据库初始化完成！' AS message;
SELECT '管理员账号' AS info, username, password FROM admin_user;
SELECT '数据表统计' AS info, 
    (SELECT COUNT(*) FROM admin_user) AS admin_users,
    (SELECT COUNT(*) FROM about_us) AS about_us,
    (SELECT COUNT(*) FROM contact_info) AS contact_info,
    (SELECT COUNT(*) FROM product_service) AS products,
    (SELECT COUNT(*) FROM success_case) AS cases,
    (SELECT COUNT(*) FROM consultation) AS consultations;
