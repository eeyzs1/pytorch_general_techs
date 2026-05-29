# L5 实验：技术战略雷达

本实验把 CTO 视野里的技术雷达做成可运行脚本：根据影响、信心、成本、风险计算 Adopt / Trial / Assess / Hold 分区。

## 运行

```bash
python3 build_radar.py data/technologies.csv --output output/radar.json
python3 -m unittest test_strategy_radar.py
```

仓库根目录快捷命令：

```bash
make lab-l5-test
```
