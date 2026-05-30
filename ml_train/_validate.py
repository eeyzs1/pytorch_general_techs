import json

files = [
    '07_alignment_training/01_rlhf.ipynb',
    '11_rag/01_document_processing.ipynb',
    '12_agent/01_tool_use.ipynb',
    '09_inference_optimization/01_kv_cache.ipynb',
]

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as fh:
            data = json.load(fh)
        print(f'{f}: valid JSON, {len(data["cells"])} cells')
    except Exception as e:
        print(f'{f}: ERROR - {e}')