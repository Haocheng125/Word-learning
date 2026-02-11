@echo off
chcp 65001 >nul
echo ========================================
echo 单词学习助手
echo ========================================
echo.
echo 正在启动...
echo.

python main.py

if errorlevel 1 (
    echo.
    echo 启动失败！请确保已安装 Python 和依赖包。
    echo.
    echo 安装依赖命令：
    echo   pip install PyPDF2 pdfplumber
    echo.
    pause
)
