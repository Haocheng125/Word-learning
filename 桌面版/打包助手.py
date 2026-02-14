import os
import sys
import subprocess
import shutil

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_python():
    print_header("检查 Python 环境")
    print(f"Python 版本: {sys.version}")
    return True

def install_package(package):
    try:
        subprocess.check_call(['py', "-m", "pip", "install", package])
        return True
    except:
        return False

def check_and_install_dependencies():
    print_header("检查依赖")
    
    required_packages = ['PyInstaller', 'pdfplumber']
    
    for package in required_packages:
        try:
            __import__(package.lower().replace('-', ''))
            print(f"✓ {package} 已安装")
        except ImportError:
            print(f"✗ {package} 未安装，正在安装...")
            if install_package(package):
                print(f"✓ {package} 安装成功")
            else:
                print(f"✗ {package} 安装失败")
                return False
    
    return True

def build_exe():
    print_header("开始打包")
    
    if not os.path.exists('main.py'):
        print("错误: 找不到 main.py 文件")
        return False
    
    cmd = [
        'py', '-m', 'PyInstaller',
        '--onefile',
        '--windowed',
        '--name', '单词学习助手',
        'main.py'
    ]
    
    print("执行打包命令...")
    print(f"命令: {' '.join(cmd)}")
    print("\n这可能需要几分钟时间，请耐心等待...\n")
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n✓ 打包完成！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ 打包失败: {e}")
        return False

def check_output():
    print_header("检查输出文件")
    
    exe_path = os.path.join('dist', '单词学习助手.exe')
    
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"✓ 找到可执行文件: {exe_path}")
        print(f"  文件大小: {size_mb:.2f} MB")
        return exe_path
    else:
        print("✗ 未找到可执行文件")
        return None

def copy_to_backend(exe_path):
    print_header("复制到后端")
    
    target_dir = os.path.join('..', 'backend', 'uploads', 'downloads')
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
        print(f"创建目录: {target_dir}")
    
    target_path = os.path.join(target_dir, '单词学习助手.exe')
    
    try:
        shutil.copy2(exe_path, target_path)
        print(f"✓ 已复制到: {target_path}")
        return True
    except Exception as e:
        print(f"✗ 复制失败: {e}")
        return False

def main():
    print("\n" + "╔" + "═"*58 + "╗")
    print("║" + " "*10 + "单词学习助手 - 打包工具" + " "*24 + "║")
    print("╚" + "═"*58 + "╝")
    
    if not check_python():
        input("\n按回车键退出...")
        return
    
    if not check_and_install_dependencies():
        input("\n按回车键退出...")
        return
    
    if not build_exe():
        input("\n按回车键退出...")
        return
    
    exe_path = check_output()
    if not exe_path:
        input("\n按回车键退出...")
        return
    
    print("\n" + "="*60)
    print("  打包完成！")
    print("="*60)
    
    choice = input("\n是否将 exe 复制到后端 downloads 文件夹？(y/n): ").strip().lower()
    if choice == 'y':
        copy_to_backend(exe_path)
    
    print("\n" + "="*60)
    print("  完成！")
    print(f"  可执行文件位置: {exe_path}")
    print("="*60)
    
    input("\n按回车键退出...")

if __name__ == '__main__':
    main()
