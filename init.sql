-- 初始化数据库
CREATE DATABASE IF NOT EXISTS word_learning CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE word_learning;

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 单词书表
CREATE TABLE IF NOT EXISTS wordbooks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    pdf_filename VARCHAR(255),
    word_count INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 单词表
CREATE TABLE IF NOT EXISTS words (
    id INT AUTO_INCREMENT PRIMARY KEY,
    wordbook_id INT NOT NULL,
    word VARCHAR(100) NOT NULL,
    phonetic VARCHAR(100),
    translation TEXT NOT NULL,
    sequence INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (wordbook_id) REFERENCES wordbooks(id) ON DELETE CASCADE,
    UNIQUE KEY unique_wordbook_sequence (wordbook_id, sequence),
    INDEX idx_wordbook_sequence (wordbook_id, sequence)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 用户学习进度表
CREATE TABLE IF NOT EXISTS user_progress (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    wordbook_id INT NOT NULL,
    current_index INT DEFAULT 1,
    last_learn_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (wordbook_id) REFERENCES wordbooks(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_wordbook (user_id, wordbook_id),
    INDEX idx_user_wordbook (user_id, wordbook_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 生词本表
CREATE TABLE IF NOT EXISTS vocabulary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    word_id INT NOT NULL,
    added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (word_id) REFERENCES words(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_word (user_id, word_id),
    INDEX idx_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
