# L2 实验：实时窗口聚合最小闭环

本实验用 JSONL 事件流模拟 Kafka + Flink 的核心思想：事件时间、乱序、窗口聚合和告警输出。它不依赖外部服务，适合作为进入真实 Kafka/Flink 环境前的可运行预备实验。

## 学习目标

- 理解事件流和批量文件的区别。
- 按事件时间做 1 分钟窗口聚合。
- 识别高风险交易并输出窗口级指标。
- 为后续 Kafka/Flink 版本保留相同输入输出契约。

## 运行步骤

```bash
python3 generate_events.py --rows 240 --output data/events.jsonl
python3 window_aggregate.py data/events.jsonl --output output/window_report.json
python3 -m unittest test_streaming_window.py
```

仓库根目录快捷命令：

```bash
make lab-l2-test
```

## 输入事件格式

```json
{"event_id":"evt-000001","event_time":"2026-05-29T09:00:00+08:00","user_id":"u001","amount":99.0,"risk_score":0.12}
```
