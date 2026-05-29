# 大数据技术全栈课程

本项目是一套从编程基础到 CTO 视野的大数据课程资料库，覆盖 Python/SQL、Hadoop/Spark、Kafka/Flink、数据湖仓、MLOps、云原生、架构设计与技术管理。

> 维护约定：课程元信息以 `curriculum.yaml` 为准。历史文档中的周次、课时、项目编号如果与 `curriculum.yaml` 冲突，后续应向 `curriculum.yaml` 收敛。

## 快速入口

| 阶段 | 定位 | 主入口 | 关键交付物 |
|------|------|--------|------------|
| L0 | 编程基本功 | [L0_预备阶段/README.md](L0_预备阶段/README.md) | Web 日志分析、电商 SQL、命令行运维 |
| L1 | 大数据入门 | [L1_初级工程师/README.md](L1_初级工程师/README.md) | 离线数仓、用户画像、Airflow 编排 |
| L2 | 工程深化 | [L2_中级工程师/README.md](L2_中级工程师/README.md) | 实时监控大屏、Kafka 调优、故障排查 SOP |
| L3 | 技术深度 | [L3_高级工程师/README.md](L3_高级工程师/README.md) | 源码分析、论文精读、调优攻坚、MLOps |
| L4 | 架构设计 | [L4_架构师/README.md](L4_架构师/README.md) | 系统设计、企业架构方案、FinOps、dbt CI/CD |
| L5 | CTO 视野 | [L5_CTO视野/README.md](L5_CTO视野/README.md) | 技术战略、组织建设、商业翻译、年度述职 |

## 配套资料

- [项目编号目录](project_catalog.json)：统一维护主线项目和补充项目的编号、阶段和路径。
- [学员入口](learner/README.md)：学习路径、实验入口和交付物模板。
- [讲师入口](instructor/README.md)：答案、评分 rubrics 和课堂运营建议。
- [内部维护入口](internal/README.md)：内容治理、发布检查和迁移规则。
- [结构化评估](assessments/README.md)：题库、考试配置和评分标准。
- [技术全景图](big_data_technology_overview.md)：大数据产业级技术分类和组件地图。
- [课程总课件](big_data_courseware.md)：课程主干内容和阶段说明。
- [贯穿项目](贯穿项目_电商数据平台演进/电商数据平台全周期演进指南.md)：电商数据平台从脚本到云原生平台的递进式演进。
- [动手实验室](交互式学习_动手实验室指南.md)：跨阶段实验指南。
- [可运行实验室](labs/README.md)：真实脚本、样例数据和自动测试。
- [编程挑战集](交互式学习_编程挑战集.md)：项目化练习和参考实现。
- [学习进度追踪](学习进度追踪体系.md)：技能树、周/月复盘和里程碑检查表。

## 仓库规范

建议按以下分层逐步整理内容：

```text
learner/       学员材料：题目、实验步骤、交付要求
instructor/    讲师材料：答案、评分细则、讲师提示
data/          样例数据和数据生成脚本
labs/          可运行实验环境：Docker Compose、脚本、验证命令
scripts/       仓库质量检查和文档工具
```

当前资料仍以历史目录为主，新增内容优先遵循上述结构。

## 本地质量检查

```bash
make check
make lab-test
```

等价于：

```bash
python3 scripts/check_links.py
python3 scripts/check_placeholders.py
python3 scripts/check_curriculum_refs.py
python3 scripts/check_project_catalog.py
```

## 文档站预览

如果本机安装了 MkDocs，可以预览文档站：

```bash
mkdocs serve
```

配置文件为 `mkdocs.yml`。
