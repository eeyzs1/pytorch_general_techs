# 讲师与教练入口

这里用于维护讲师版材料：答案、评分 rubrics、教学节奏、常见误区和课堂引导问题。学员可见材料应放在 `learner/` 或原阶段目录中。

## 使用原则

- 答案和评分标准不要混入学员练习页。
- 每个项目至少有一个 rubric，明确功能、工程化、解释能力和复盘质量。
- 课堂讲解应围绕“为什么这么设计”和“如何验证”，而不是只演示命令。

## 当前材料

- [评分 Rubrics 总览](rubrics/README.md)
- [答案材料索引](answers/README.md)

### 结构化题库（按阶段）

- [L0 题库](../assessments/questions/l0_sample.json)（Python/SQL/Linux/Git）
- [L1 题库](../assessments/questions/l1_sample.json)（HDFS/MapReduce/Hive/Spark）
- [L2 题库](../assessments/questions/l2_sample.json)（Kafka/Flink/DDIA/数据湖仓）
- [L3 题库](../assessments/questions/l3_sample.json)（源码/论文/调优）
- [L4 题库](../assessments/questions/l4_sample.json)（系统设计/架构/FinOps）
- [L5 题库](../assessments/questions/l5_sample.json)（技术战略/组织建设/商业翻译）

### 项目评分表（按阶段）

- [L0 项目评分表](../assessments/rubrics/l0-project-rubric.md)
- [L1 项目评分表](../assessments/rubrics/l1-project-rubric.md)
- [L2 项目评分表](../assessments/rubrics/l2-project-rubric.md)
- [L3 项目评分表](../assessments/rubrics/l3-project-rubric.md)
- [L4 项目评分表](../assessments/rubrics/l4-project-rubric.md)
- [L5 项目评分表](../assessments/rubrics/l5-project-rubric.md)

### 考试/项目验收配置

- [L0 项目考试](../assessments/exams/l0_project_exam.json)
- [L1 项目考试](../assessments/exams/l1_project_exam.json)
- [L2 项目考试](../assessments/exams/l2_project_exam.json)
- [L3 项目考试](../assessments/exams/l3_project_exam.json)
- [L4 项目考试](../assessments/exams/l4_project_exam.json)
- [L5 项目考试](../assessments/exams/l5_project_exam.json)

## 课堂运营建议

1. 开课前用 `make check` 验证文档链接和项目引用。
2. 实验课前用 `make lab-test` 验证本机脚本可运行。
3. 考核时从 `assessments/` 抽题，不直接使用含答案的历史题库。
4. 每阶段结束后补充 3 类案例：高分样例、常见错误、边界问题。
