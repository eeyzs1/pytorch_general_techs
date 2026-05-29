# 内部维护入口

这里放课程维护规则、发布流程和内容治理说明，不直接面向学员。

## 内容治理规则

- `curriculum.yaml` 是阶段元信息唯一来源。
- `project_catalog.json` 是项目编号唯一来源。
- 新增课程页必须能从 README、MkDocs nav 或阶段 README 被发现。
- 新增实验必须提供 README、运行命令和测试命令。
- 新增答案必须放入 `instructor/` 或 `assessments/`，不要放入学员入口。

## 发布前检查

```bash
make check
make lab-test
```

## 后续迁移任务

- 将历史题库拆分为学员题目和讲师答案。
- 将 Docker Compose / K8s / dbt 等重型实验沉淀到 `labs/`。
- 用脚本从 `curriculum.yaml` 和 `project_catalog.json` 生成文档索引，减少手工重复维护。
