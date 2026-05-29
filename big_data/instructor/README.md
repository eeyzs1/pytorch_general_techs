# 讲师与教练入口

这里用于维护讲师版材料：答案、评分 rubrics、教学节奏、常见误区和课堂引导问题。学员可见材料应放在 `learner/` 或原阶段目录中。

## 使用原则

- 答案和评分标准不要混入学员练习页。
- 每个项目至少有一个 rubric，明确功能、工程化、解释能力和复盘质量。
- 课堂讲解应围绕“为什么这么设计”和“如何验证”，而不是只演示命令。

## 当前材料

- [评分 Rubrics 总览](rubrics/README.md)
- [答案材料索引](answers/README.md)
- [结构化题库](../assessments/questions/l0_sample.json)
- [L0 项目评分表](../assessments/rubrics/l0-project-rubric.md)

## 课堂运营建议

1. 开课前用 `make check` 验证文档链接和项目引用。
2. 实验课前用 `make lab-test` 验证本机脚本可运行。
3. 考核时从 `assessments/` 抽题，不直接使用含答案的历史题库。
4. 每阶段结束后补充 3 类案例：高分样例、常见错误、边界问题。
