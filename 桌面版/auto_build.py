import os
import sys
import subprocess
import shutil

def run_cmd(cmd):
    print(f"执行: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"错误: {e}")
        print(e.stdout)
        print(e.stderr)
        return False

def main():
    print("=" * 60)
    print("自动打包桌面版应用")
    print("=" * 60)
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 1. 打包
    print("\n1. 开始打包...")
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--windowed',
        '--name', '单词学习助手',
        'main.py'
    ]
    
    if not run_cmd(cmd):
        print("打包失败！")
        return
    
    # 2. 检查输出
    exe_path = os.path.join('dist', '单词学习助手.exe')
    if not os.path.exists(exe_path):
        print(f"未找到文件: {exe_path}")
        return
    
    size_mb = os.path.getsize(exe_path) / (1024 * 1024)
    print(f"\n2. 打包成功！")
    print(f"   文件: {exe_path}")
    print(f"   大小: {size_mb:.2f} MB")
    
    # 3. 复制到后端
    target_dir = os.path.join('..', 'backend', 'uploads', 'downloads')
    target_path = os.path.join(target_dir, '单词学习助手.exe')
    
    print(f"\n3. 复制到后端...")
    print(f"   目标: {target_path}")
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
    
    try:
        shutil.copy2(exe_path, target_path)
        print("   复制成功！")
    except Exception as e:
        print(f"   复制失败: {e}")
        return
    
    print("\n" + "=" * 60)
    print("完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()
