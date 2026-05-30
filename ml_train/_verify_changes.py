import json, os, re

base = r'e:\AI_Generated_Projects\pytorch_general_techs\ml_train'
files = [
    '02_learning_paradigms/01_supervised_learning.ipynb',
    '03_architecture_design/01_overall_architecture.ipynb',
    '03_architecture_design/02_attention_mechanism.ipynb',
    '06_fine_tuning/02_peft.ipynb',
]

for f in files:
    path = os.path.join(base, f)
    with open(path, 'r', encoding='utf-8') as fh:
        data = json.load(fh)
    cells = data['cells']

    first_src = ''.join(cells[0]['source'])
    has_time = '预估学习时间' in first_src

    # Extract time estimate
    match = re.search(r'(\d+)分钟', first_src)
    time_val = match.group(1) if match else 'N/A'

    last_src = ''.join(cells[-1]['source'])
    has_exercises = '课后思考题' in last_src

    print(f'[{f}]')
    print(f'  cells: {len(cells)} | time: {time_val}min ({("OK" if has_time else "MISSING")}) | exercises: {("OK" if has_exercises else "MISSING")} | JSON: VALID')