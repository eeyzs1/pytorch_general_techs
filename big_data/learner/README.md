# 学员学习入口

这里是面向学员的入口层，只放学习路径、实验步骤、交付要求和自检表。标准答案、评分细则和讲师提示不应放在本目录。

## 学习顺序

1. 阅读根目录 [README](../README.md) 和 [课程元信息](../curriculum.yaml)。
2. 按 L0-L5 阶段进入对应 README。
3. 每完成一个阶段，提交阶段项目、实验报告和复盘记录。
4. 通过 `labs/` 中的可运行实验建立最小工程闭环。

## 当前推荐实验

| 阶段 | 实验 | 命令 |
|------|------|------|
| L0 | [Web 日志分析](../labs/l0-web-log-analysis/README.md) | `make lab-l0-test` |
| L1 | [SQL 离线数仓](../labs/l1-sql-warehouse/README.md) | `make lab-l1-test` |
| L2 | [实时窗口聚合](../labs/l2-streaming-window/README.md) | `make lab-l2-test` |
| L3 | [数据倾斜调优](../labs/l3-skew-tuning/README.md) | `make lab-l3-test` |
| L4 | [架构选型评分卡](../labs/l4-architecture-scorecard/README.md) | `make lab-l4-test` |
| L5 | [技术战略雷达](../labs/l5-strategy-radar/README.md) | `make lab-l5-test` |

## 学员版题库

- [随堂测验题库（学员版）](随堂测验题库_学员版.md)：由脚本生成，不包含正确答案和解析。

## 学员交付物模板

每个项目建议提交：

```text
project-report.md     需求理解、方案设计、运行截图、指标结果、复盘
src/ 或 scripts/      可运行代码
README.md             环境准备、启动命令、验证命令
output/               小型结果样例或截图，不提交大文件
```

## 自检标准

- 是否能从空目录重新运行并得到相同结果？
- 是否有明确输入、处理逻辑、输出和验证方式？
- 是否解释了关键技术选择，而不只是贴代码？
- 是否记录了遇到的问题、定位过程和改进方案？
