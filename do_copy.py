
import shutil
import os

base = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(base, "桌面版", "dist", "单词学习助手.exe")
dst_dir = os.path.join(base, "backend", "uploads", "downloads")
dst = os.path.join(dst_dir, "单词学习助手.exe")

print("Working from:", base)
print("Source:", src)
print("Source exists?", os.path.exists(src))
print("Dest dir:", dst_dir)
print("Dest dir exists?", os.path.exists(dst_dir))

if os.path.exists(src):
    print("Copying...")
    shutil.copy2(src, dst)
    print("Done!")
    print("Dest exists?", os.path.exists(dst))
else:
    print("Source not found!")
