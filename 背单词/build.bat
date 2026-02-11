@echo off
echo ========================================
echo 单词学习助手 - 打包脚本
echo ========================================
echo.

echo [1/4] 检查 Python 环境...
python --version
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python
    pause
    exit /b 1
)
echo.

echo [2/4] 安装依赖包...
pip install -r requirements.txt
pip install pyinstaller
echo.

echo [3/4] 使用 PyInstaller 打包...
pyinstaller --clean build.spec
echo.

echo [4/4] 打包完成！
echo.
echo 可执行文件位置: dist\单词学习助手.exe
echo.
echo ========================================
pause
