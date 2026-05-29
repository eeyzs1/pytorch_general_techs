# L4 实验：架构选型评分卡

本实验把 L4 架构设计中的 Trade-off 显性化：用统一维度给候选方案打分，输出推荐方案和风险说明。

## 运行

```bash
python3 score_architecture.py data/options.json --output output/decision.json
python3 -m unittest test_score_architecture.py
```

仓库根目录快捷命令：

```bash
make lab-l4-test
```
