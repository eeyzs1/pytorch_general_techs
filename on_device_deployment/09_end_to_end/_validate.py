import json
import os

# 使用相对路径，自动定位到本脚本所在目录下的 notebook
script_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(script_dir, "9.2_troubleshooting_debug.ipynb")
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

print("Valid JSON!")
print(f"  Cell count: {len(data['cells'])}")
print(f"  nbformat: {data['nbformat']}")
print(f"  nbformat_minor: {data['nbformat_minor']}")
md = sum(1 for c in data["cells"] if c["cell_type"] == "markdown")
code = sum(1 for c in data["cells"] if c["cell_type"] == "code")
print(f"  Markdown cells: {md}")
print(f"  Code cells: {code}")
