# 评估与题库

`assessments/` 存放结构化题库、考试配置和评分 rubrics，用于逐步替代“题目和答案混在 Markdown 正文里”的维护方式。

## 目录

- `questions/`：结构化题目，适合抽题和生成测验。
- `exams/`：考试/项目验收配置。
- `rubrics/`：评分标准。

## 校验

```bash
python3 scripts/validate_assessments.py
```
