
import os

print("=" * 50)
print("测试下载路径：")
print("=" * 50)

current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"当前文件所在目录: {current_dir}")

downloads_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads', 'downloads')
print(f"计算的 downloads_dir: {downloads_dir}")

filename = '单词学习助手.exe'
file_path = os.path.join(downloads_dir, filename)

print(f"文件完整路径: {file_path}")
print(f"downloads_dir 存在吗? {os.path.exists(downloads_dir)}")
print(f"文件存在吗? {os.path.exists(file_path)}")

if os.path.exists(downloads_dir):
    print(f"\ndownloads_dir 里面的内容:")
    files = os.listdir(downloads_dir)
    for f in files:
        fpath = os.path.join(downloads_dir, f)
        size = os.path.getsize(fpath)
        print(f"  - {f} ({size} 字节)")
