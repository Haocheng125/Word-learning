import sys
import os

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 将 backend 目录添加到 Python 路径
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# 导入应用
from app import create_app

# 创建应用实例
app = create_app()

# 这是 Vercel 需要的应用实例
application = app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
