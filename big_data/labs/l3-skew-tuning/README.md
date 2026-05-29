# L3 实验：数据倾斜调优最小闭环

本实验用 Python 标准库模拟 Spark/Flink 调优攻坚里的一个核心问题：热点 Key 导致聚合倾斜。实验包含数据生成、基线聚合、加盐聚合、结果一致性校验和简单性能指标输出。

## 学习目标

- 识别热点 Key 和倾斜比例。
- 理解“加盐拆分热点 Key -> 二次聚合”的基本思路。
- 用可重复脚本验证优化前后结果一致。

## 运行

```bash
python3 generate_skewed_events.py --rows 5000 --output data/events.csv
python3 compare_strategies.py data/events.csv --output output/report.json
python3 -m unittest test_skew_tuning.py
```

仓库根目录快捷命令：

```bash
make lab-l3-test
```
