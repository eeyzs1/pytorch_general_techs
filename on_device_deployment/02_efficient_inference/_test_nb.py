import json
import sys

with open(r'e:\AI_Generated_Projects\pytorch_general_techs\on_device_deployment\02_efficient_inference\2.1_kv_cache.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

code_cells = [c for c in nb['cells'] if c['cell_type'] == 'code']
shared_ns = {}
for i, cell in enumerate(code_cells):
    code = ''.join(cell['source'])
    print(f'--- Cell {i} ---')
    try:
        exec(compile(code, f'cell_{i}', 'exec'), shared_ns)
        print(f'Cell {i} OK')
    except Exception as e:
        print(f'Cell {i} ERROR: {e}')
        sys.exit(1)

print('\nAll cells passed!')
