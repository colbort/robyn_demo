import os

# 动态加载 models 目录下的所有模块
modules = [
    f.split(".")[0]
    for f in os.listdir(os.path.dirname(__file__))  # 遍历当前目录
    if f.endswith(".py") and f != "__init__.py"  # 筛选 Python 文件，排除 __init__.py
]

models = []

for module in modules:
    models.append(f"models.{module}")  # 动态导入每个模型模块
