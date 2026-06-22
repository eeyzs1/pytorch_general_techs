# 评估与题库

`assessments/` 存放结构化题库、考试配置和评分 rubrics，用于逐步替代"题目和答案混在 Markdown 正文里"的维护方式。

## 目录结构

```
assessments/
├── questions/          # 结构化题目（JSON）
│   ├── l0_sample.json  # L0：Python/SQL/Linux/Git
│   ├── l1_sample.json  # L1：HDFS/MapReduce/Hive/Spark
│   ├── l2_sample.json  # L2：Kafka/Flink/DDIA/数据湖仓
│   ├── l3_sample.json  # L3：源码/论文/调优
│   ├── l4_sample.json  # L4：系统设计/架构/FinOps
│   └── l5_sample.json  # L5：技术战略/组织建设/商业翻译
├── exams/              # 考试/项目验收配置（JSON）
│   ├── l0_project_exam.json
│   ├── l1_project_exam.json
│   ├── l2_project_exam.json
│   ├── l3_project_exam.json
│   ├── l4_project_exam.json
│   └── l5_project_exam.json
└── rubrics/            # 评分标准（Markdown）
    ├── l0-project-rubric.md
    ├── l1-project-rubric.md
    ├── l2-project-rubric.md
    ├── l3-project-rubric.md
    ├── l4-project-rubric.md
    └── l5-project-rubric.md
```

## 与 curriculum.yaml 的关联

每个阶段的 `assessment` 字段引用了对应的 questions/exam/rubric 文件，详见 [curriculum.yaml](../curriculum.yaml)。

## 校验

```bash
python3 scripts/validate_assessments.py
```
