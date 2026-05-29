# L0 实验：Web 日志分析

本实验对应 L0 的“Web 日志分析系统”，目标是让学员用纯 Python 标准库完成一次端到端数据处理：生成数据、解析日志、聚合统计、输出 JSON 报告。

## 学习目标

- 理解日志行的基本结构和解析方式。
- 使用 `dict`、`Counter`、文件读写完成统计任务。
- 建立“输入数据 -> 处理脚本 -> 输出报告 -> 自动测试”的最小工程闭环。

## 运行步骤

```bash
# 1. 生成确定性的样例日志
python3 generate_logs.py --rows 200 --output data/access.log

# 2. 分析日志并输出报告
python3 analyze_logs.py data/access.log --output output/report.json

# 3. 运行测试
python3 -m unittest test_analyze_logs.py
```

`data/access.log.sample` 提供了 3 行最小样例，便于先阅读日志格式。

也可以在仓库根目录执行：

```bash
make lab-l0-test
```

## 输出示例

`output/report.json` 会包含：

```json
{
  "total_requests": 200,
  "status_counts": {"200": 150, "404": 20},
  "top_ips": [["192.168.1.10", 16]],
  "top_paths": [["/index.html", 42]]
}
```
