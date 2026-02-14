
from app import create_app

app = create_app()

print("=" * 50)
print("已注册的所有路由：")
print("=" * 50)

for rule in app.url_map.iter_rules():
    print(f"{rule.methods} {rule.rule}")

print("=" * 50)
