# 单词学习助手 - 桌面应用

一个基于 Python Tkinter 的桌面背单词软件，支持从 PDF 文件导入单词。

## 功能特性

- 📄 从 PDF 文件导入单词列表
- 📁 批量导入整个文件夹的 PDF 文件
- 📖 卡片式学习界面
- ✅ 学习进度追踪
- 🗂️ 单词队列管理
- 💾 本地数据库存储

## 快速开始

### 方式一：直接运行 Python 脚本

1. 确保已安装 Python 3.7+
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 运行应用：
   ```bash
   python main.py
   ```

### 方式二：打包成可执行文件

1. 运行打包脚本：
   ```bash
   build.bat
   ```
2. 打包完成后，可执行文件位于 `dist\单词学习助手.exe`

## 使用说明

### 导入单词

1. 点击"加载PDF文件"选择一个或多个 PDF 文件
2. 或点击"加载PDF文件夹"导入整个文件夹
3. 程序会自动解析 PDF 中的单词表格

### 学习单词

1. 在单词列表中点击"开始学习"
2. 点击单词卡片查看中文释义
3. 使用"上一个"和"下一个"按钮切换单词
4. 点击"加入队列"将当前单词添加到复习队列

## 技术栈

- **GUI 框架**: Tkinter
- **PDF 解析**: PyPDF2, pdfplumber
- **数据库**: SQLite
- **打包工具**: PyInstaller

## 文件说明

- `main.py` - 主程序入口和 GUI 界面
- `database.py` - 数据库管理
- `pdf_reader.py` - PDF 文件解析
- `requirements.txt` - Python 依赖包
- `build.spec` - PyInstaller 配置文件
- `build.bat` - Windows 打包脚本

## 系统要求

- Windows 7/10/11
- Python 3.7+ (仅开发者需要)
