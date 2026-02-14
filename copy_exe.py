import shutil
import os
import sys

src = os.path.join(os.path.dirname(__file__), "桌面版", "dist", "单词学习助手.exe")
dst_dir = os.path.join(os.path.dirname(__file__), "backend", "uploads", "downloads")
dst = os.path.join(dst_dir, "单词学习助手.exe")

print("源文件:", src)
print("目标:", dst)
print("源文件存在:", os.path.exists(src))
print("目标目录存在:", os.path.exists(dst_dir))

if os.path.exists(src):
    print("开始复制...")
    try:
        shutil.copy2(src, dst)
        print("复制成功！")
        print("目标文件存在:", os.path.exists(dst))
    except Exception as e:
        print("错误:", e)
        import traceback
        traceback.print_exc()
else:
    print("源文件不存在！")
    print("桌面版 dist 目录内容:", os.listdir(os.path.join(os.path.dirname(__file__), "桌面版", "dist")))
