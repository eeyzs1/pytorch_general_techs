# 可运行实验室

`labs/` 用来承载可以直接运行和验证的实验资产，补齐课程文档与真实动手之间的断层。

## 当前实验

| 实验 | 对应阶段 | 目标 | 验证命令 |
|------|----------|------|----------|
| [l0-web-log-analysis](l0-web-log-analysis/README.md) | L0 | 生成 Web 访问日志并完成基础统计分析 | `make lab-l0-test` |
| [l1-sql-warehouse](l1-sql-warehouse/README.md) | L1 | 用 SQLite 跑通离线数仓指标分析闭环 | `make lab-l1-test` |
| [l2-streaming-window](l2-streaming-window/README.md) | L2 | 用 JSONL 事件流模拟实时窗口聚合 | `make lab-l2-test` |
| [l3-skew-tuning](l3-skew-tuning/README.md) | L3 | 模拟热点 Key 倾斜与加盐聚合调优 | `make lab-l3-test` |
| [l4-architecture-scorecard](l4-architecture-scorecard/README.md) | L4 | 用评分卡量化架构选型 Trade-off | `make lab-l4-test` |
| [l5-strategy-radar](l5-strategy-radar/README.md) | L5 | 根据战略因子生成技术雷达分区 | `make lab-l5-test` |

## 实验目录约定

每个实验建议包含：

```text
README.md          实验说明、学习目标、运行步骤
data/              样例数据或生成后的数据
output/            运行输出，默认不提交大文件
scripts/ 或 *.py   可执行脚本
```

新增实验后，请在本文件和根目录 `README.md` 中补充入口。
