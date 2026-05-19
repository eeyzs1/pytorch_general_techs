# 项目8：Kafka深度调优

> **所属阶段**：L2 中级工程师 | **预计时长**：20h | **难度**：★★★☆☆
>
> **核心目标**：对Kafka集群进行系统性性能调优和故障演练

---

## 一、项目描述

对Kafka集群从Partition、Producer、Consumer三个维度进行系统化的性能基准测试和调优，同时进行4个核心故障场景的演练，输出可指导生产环境的配置建议。

---

## 二、Partition级别调优

### 2.1 实验设计

```yaml
实验目标: 找出给定硬件配置下的最优Partition数

硬件环境:
  Broker: 3节点, 4核CPU, 16GB内存, SSD磁盘
  网络: 1Gbps

测试方法:
  - 创建不同Partition数的Topic
  - 每个Topic运行相同的压测（1000万条，512字节/条）
  - 记录吞吐量和P99延迟
```

### 2.2 实验脚本

```bash
#!/bin/bash
# partition-benchmark.sh
# Partition数对吞吐量的影响测试

TOPIC_PREFIX="partition-test"
PARTITIONS=(1 3 6 10 15 20 30)
RECORDS=5000000
RECORD_SIZE=512

echo "=== Kafka Partition数据对比实验 ==="
echo "记录数: ${RECORDS}万, 记录大小: ${RECORD_SIZE}字节"
echo ""

for p in "${PARTITIONS[@]}"; do
    TOPIC="${TOPIC_PREFIX}-p${p}"
    
    # 1. 创建Topic
    kafka-topics.sh --create \
      --topic $TOPIC \
      --partitions $p \
      --replication-factor 3 \
      --bootstrap-server localhost:9092 \
      --if-not-exists
    
    # 2. 压测
    echo "=== 测试 Partition数=$p ==="
    RESULT=$(kafka-producer-perf-test.sh \
      --topic $TOPIC \
      --num-records $RECORDS \
      --record-size $RECORD_SIZE \
      --throughput -1 \
      --producer-props \
        bootstrap.servers=localhost:9092 \
        acks=1 \
        batch.size=65536 \
        linger.ms=5 \
        compression.type=lz4 \
      --print-metrics 2>&1)
    
    # 3. 提取关键指标
    THROUGHPUT=$(echo "$RESULT" | grep "records/sec" | awk '{print $1}' | sed 's/\..*//')
    MB_SEC=$(echo "$RESULT" | grep "MB/sec" | awk '{print $3}')
    AVG_LATENCY=$(echo "$RESULT" | grep "avg latency" | awk '{print $3}')
    MAX_LATENCY=$(echo "$RESULT" | grep "max latency" | awk '{print $3}')
    
    echo "Partitions=$p | Throughput: ${THROUGHPUT} rec/s | MB/s: ${MB_SEC} | AvgLatency: ${AVG_LATENCY}ms | MaxLatency: ${MAX_LATENCY}ms"
    echo ""
    
    # 4. 清理Topic
    kafka-topics.sh --delete --topic $TOPIC --bootstrap-server localhost:9092
    sleep 5
done

echo "=== 实验完成 ==="
```

### 2.3 预期结果分析

```
Partition数 vs 吞吐量（典型结果）:

Partitions    Throughput(rec/s)   P99 Latency(ms)   CPU使用率
    1             80,000              120             15%
    3            200,000               85             35%
    6            320,000               65             55%
   10            380,000               55             72%
   15            360,000               70             88%
   20            300,000              110             95%
   30            220,000              180             98%

结论:
  - Partition数 ≈ CPU核数 时吞吐最佳（本次实验：6-10）
  - Partition过多 → CPU上下文切换频繁，吞吐下降
  - Partition过少 → CPU利用不充分，吞吐受限
  
生产建议:
  - Partition数 = max(期望吞吐/单分区吞吐, 下游Consumer数)
  - 单分区吞吐约 30-50MB/s（SSD环境）
  - 预留20%余量应对峰值
```

---

## 三、Producer参数调优矩阵

### 3.1 实验设计

```yaml
参数矩阵:
  acks: [0, 1, all]
  batch.size: [16KB, 64KB, 256KB, 1MB]
  linger.ms: [0, 5, 20, 100]
  compression.type: [none, gzip, snappy, lz4, zstd]

总计: 3 × 4 × 4 × 5 = 240个组合

优化策略: 采用正交实验法，减少至20个关键组合
核心思想: 每次只改变一个变量，其他保持基线值
```

### 3.2 完整实验脚本

```python
"""
kafka_producer_benchmark.py
Kafka Producer参数矩阵实验
"""
import subprocess
import json
import time
import csv
from itertools import product
from datetime import datetime

BASELINE_CONFIG = {
    'bootstrap.servers': 'localhost:9092',
    'acks': '1',
    'batch.size': 65536,        # 64KB
    'linger.ms': 5,
    'compression.type': 'lz4',
    'buffer.memory': 33554432,  # 32MB
    'retries': 0,
}

TOPIC = 'perf-test-producer'
NUM_RECORDS = 5000000
RECORD_SIZE = 1024


def run_benchmark(topic, num_records, record_size, props):
    """运行一次Producer压测"""
    props_str = ' '.join([f'{k}={v}' for k, v in props.items()])
    
    cmd = [
        'kafka-producer-perf-test.sh',
        '--topic', topic,
        '--num-records', str(num_records),
        '--record-size', str(record_size),
        '--throughput', '-1',
        '--producer-props', props_str,
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    return result.stdout + result.stderr


def parse_result(output):
    """解析压测输出"""
    metrics = {}
    for line in output.split('\n'):
        if 'records sent' in line:
            parts = line.split()
            metrics['records_per_sec'] = float(parts[0].replace(',', ''))
            metrics['mb_per_sec'] = float(parts[2].replace('(', '').replace(',', ''))
        elif 'avg latency' in line:
            parts = line.split()
            metrics['avg_latency_ms'] = float(parts[3])
            metrics['max_latency_ms'] = float(parts[6])
        elif '50th' in line:
            parts = line.split()
            metrics['p50_latency_ms'] = float(parts[2])
            metrics['p95_latency_ms'] = float(parts[5])
            metrics['p99_latency_ms'] = float(parts[8])
    return metrics


def main():
    results = []
    
    # ====== 实验组1: acks 对比 ======
    print("=" * 60)
    print("实验组1: acks 对比 (acks=0/1/all)")
    
    for acks in [0, 1, 'all']:
        config = dict(BASELINE_CONFIG)
        config['acks'] = acks
        
        print(f"  测试 acks={acks}...")
        output = run_benchmark(TOPIC, NUM_RECORDS, RECORD_SIZE, config)
        metrics = parse_result(output)
        metrics['experiment'] = 'acks'
        metrics['value'] = str(acks)
        metrics.update(config)
        results.append(metrics)
        
        print(f"    吞吐: {metrics.get('records_per_sec', 'N/A')} rec/s, "
              f"平均延迟: {metrics.get('avg_latency_ms', 'N/A')}ms")
    
    # ====== 实验组2: batch.size 对比 ======
    print("=" * 60)
    print("实验组2: batch.size 对比")
    
    for batch_size in [16384, 32768, 65536, 131072, 262144, 524288, 1048576]:
        config = dict(BASELINE_CONFIG)
        config['batch.size'] = batch_size
        
        print(f"  测试 batch.size={batch_size} ({batch_size/1024:.0f}KB)...")
        output = run_benchmark(TOPIC, NUM_RECORDS, RECORD_SIZE, config)
        metrics = parse_result(output)
        metrics['experiment'] = 'batch.size'
        metrics['value'] = str(batch_size)
        metrics.update(config)
        results.append(metrics)
        
        print(f"    吞吐: {metrics.get('records_per_sec', 'N/A')} rec/s, "
              f"P99: {metrics.get('p99_latency_ms', 'N/A')}ms")
    
    # ====== 实验组3: linger.ms 对比 ======
    print("=" * 60)
    print("实验组3: linger.ms 对比")
    
    for linger in [0, 2, 5, 10, 20, 50, 100, 200]:
        config = dict(BASELINE_CONFIG)
        config['linger.ms'] = linger
        
        print(f"  测试 linger.ms={linger}...")
        output = run_benchmark(TOPIC, NUM_RECORDS, RECORD_SIZE, config)
        metrics = parse_result(output)
        metrics['experiment'] = 'linger.ms'
        metrics['value'] = str(linger)
        metrics.update(config)
        results.append(metrics)
        
        print(f"    吞吐: {metrics.get('records_per_sec', 'N/A')} rec/s, "
              f"平均延迟: {metrics.get('avg_latency_ms', 'N/A')}ms")
    
    # ====== 实验组4: compression.type 对比 ======
    print("=" * 60)
    print("实验组4: compression.type 对比")
    
    for comp in ['none', 'gzip', 'snappy', 'lz4', 'zstd']:
        config = dict(BASELINE_CONFIG)
        config['compression.type'] = comp
        
        print(f"  测试 compression={comp}...")
        output = run_benchmark(TOPIC, NUM_RECORDS, RECORD_SIZE, config)
        metrics = parse_result(output)
        metrics['experiment'] = 'compression.type'
        metrics['value'] = comp
        metrics.update(config)
        results.append(metrics)
        
        print(f"    吞吐: {metrics.get('records_per_sec', 'N/A')} rec/s, "
              f"MB/s: {metrics.get('mb_per_sec', 'N/A')}")
    
    # ====== 保存结果 ======
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'kafka_producer_benchmark_{timestamp}.csv'
    
    fieldnames = ['experiment', 'value', 'records_per_sec', 'mb_per_sec',
                  'avg_latency_ms', 'max_latency_ms', 'p50_latency_ms',
                  'p95_latency_ms', 'p99_latency_ms', 'acks', 'batch.size',
                  'linger.ms', 'compression.type']
    
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(results)
    
    print(f"结果已保存到: {filename}")
    
    # ====== 汇总报告 ======
    print("\n" + "=" * 60)
    print("汇总报告")
    print("=" * 60)
    
    for exp_type in ['acks', 'batch.size', 'linger.ms', 'compression.type']:
        exp_results = [r for r in results if r['experiment'] == exp_type]
        best = max(exp_results, key=lambda x: x.get('records_per_sec', 0))
        print(f"\n{exp_type} 最优配置:")
        print(f"  值: {best['value']}")
        print(f"  吞吐: {best.get('records_per_sec', 'N/A')} rec/s")
        print(f"  平均延迟: {best.get('avg_latency_ms', 'N/A')}ms")


if __name__ == '__main__':
    main()
```

### 3.3 生产推荐配置

```yaml
# 高吞吐配置（适合日志收集、埋点数据）
high-throughput:
  acks: 1
  batch.size: 262144          # 256KB
  linger.ms: 10
  compression.type: lz4
  buffer.memory: 67108864     # 64MB
  max.in.flight.requests.per.connection: 5

# 低延迟配置（适合交易数据、实时告警）
low-latency:
  acks: 1
  batch.size: 16384           # 16KB
  linger.ms: 2
  compression.type: snappy
  buffer.memory: 33554432     # 32MB
  max.in.flight.requests.per.connection: 5

# 高可靠配置（适合金融、订单数据）
high-reliability:
  acks: all
  batch.size: 65536           # 64KB
  linger.ms: 5
  compression.type: lz4
  buffer.memory: 67108864     # 64MB
  enable.idempotence: true
  max.in.flight.requests.per.connection: 5
  retries: 2147483647         # Integer.MAX_VALUE

# 折中最优配置（推荐大多数场景使用）
balanced:
  acks: 1
  batch.size: 131072          # 128KB
  linger.ms: 5
  compression.type: lz4
  buffer.memory: 67108864     # 64MB
  retries: 3
  max.in.flight.requests.per.connection: 5
```

---

## 四、Consumer调优

### 4.1 关键参数实验

```bash
#!/bin/bash
# consumer-benchmark.sh

TOPIC="perf-test-consumer"
GROUP="perf-consumer-group"

# 实验1: max.poll.records 对比
echo "=== max.poll.records 对比 ==="
for pr in 50 100 500 1000 5000; do
    echo "max.poll.records=$pr:"
    kafka-consumer-perf-test.sh \
      --topic $TOPIC \
      --bootstrap-server localhost:9092 \
      --messages 1000000 \
      --group "${GROUP}-${pr}" \
      --consumer-props max.poll.records=$pr \
      --hide-header 2>&1 | grep -v "^$"
done

# 实验2: fetch.min.bytes 对比
echo "=== fetch.min.bytes 对比 ==="
for fb in 1 1024 10240 102400 1048576; do
    echo "fetch.min.bytes=$fb:"
    kafka-consumer-perf-test.sh \
      --topic $TOPIC \
      --bootstrap-server localhost:9092 \
      --messages 1000000 \
      --group "${GROUP}-fb-${fb}" \
      --consumer-props fetch.min.bytes=$fb \
      --hide-header 2>&1 | grep -v "^$"
done
```

### 4.2 Rebalance策略对比

```java
// CooperativeStickyAssignor vs RangeAssignor

// 推荐配置（Kafka 2.4+）
props.put("partition.assignment.strategy",
    "org.apache.kafka.clients.consumer.CooperativeStickyAssignor");

// 效果对比：
// RangeAssignor (老): Rebalance → 全部停止 → 重新分配 → 全部恢复
// CooperativeSticky: Rebalance → 只迁移最少的分区 → 其他分区继续消费
```

---

## 五、故障演练

### 场景1：Broker宕机

```bash
#!/bin/bash
# failover-drill-1-broker-down.sh

echo "=== 场景1: Broker宕机演练 ==="

# 1. 记录初始状态
echo "[初始状态]"
kafka-topics.sh --describe --topic drill-topic --bootstrap-server localhost:9092

# 2. 启动持续压测（后台）
echo "[启动压测]"
kafka-producer-perf-test.sh \
  --topic drill-topic \
  --num-records 10000000 \
  --record-size 1024 \
  --throughput 50000 \
  --producer-props bootstrap.servers=localhost:9092 acks=all \
  > /tmp/perf.log 2>&1 &
PERF_PID=$!

# 3. 等待5秒稳定
sleep 5

# 4. Kill Broker 1
BROKER1=$(docker ps --filter "name=kafka-broker-1" -q)
echo "[故障注入] Kill Broker 1 (container=$BROKER1)"
KILL_TIME=$(date +%s)
docker kill $BROKER1

# 5. 每2秒观察ISR变化
for i in {1..30}; do
    echo "T+${i}秒:"
    kafka-topics.sh --describe --topic drill-topic --bootstrap-server localhost:9092 2>/dev/null | grep "Isr:"
    # 检查Leader是否切换
    NEW_LEADER=$(kafka-topics.sh --describe --topic drill-topic --bootstrap-server localhost:9092 2>/dev/null | grep "Leader: 2\|Leader: 3")
    if [ -n "$NEW_LEADER" ]; then
        SWITCH_TIME=$(date +%s)
        echo "  ✓ Leader切换成功！切换耗时: $((SWITCH_TIME - KILL_TIME))秒"
        break
    fi
    sleep 2
done

# 6. 检查Producer是否受影响
echo "[Producer状态]"
tail -5 /tmp/perf.log

# 7. 恢复Broker 1
echo "[恢复] 启动Broker 1..."
docker start $BROKER1
sleep 15
echo "[恢复后状态]"
kafka-topics.sh --describe --topic drill-topic --bootstrap-server localhost:9092

# 清理
kill $PERF_PID 2>/dev/null
```

### 场景2：磁盘满模拟

```bash
#!/bin/bash
# failover-drill-2-disk-full.sh

echo "=== 场景2: 磁盘满演练 ==="

# 1. 查看Broker 1的磁盘使用率
echo "[初始] 磁盘使用率:"
docker exec kafka-broker-1 df -h /var/lib/kafka/data

# 2. 模拟磁盘满（创建大文件填充磁盘）
echo "[故障注入] 填充磁盘..."
docker exec kafka-broker-1 dd if=/dev/zero of=/var/lib/kafka/data/fill_disk bs=1M count=9000 2>/dev/null

# 3. 观察Kafka行为
echo "[观察] Broker日志:"
docker logs kafka-broker-1 --tail 20 2>&1 | grep -i "disk\|error\|exception"

# 4. 尝试写入
echo "[测试写入]"
kafka-console-producer.sh \
  --topic test-disk-full \
  --bootstrap-server localhost:9092 <<< "test message" 2>&1

# 5. 查看ISR变化
kafka-topics.sh --describe --topic drill-topic --bootstrap-server localhost:9092

# 6. 清理
echo "[恢复] 清理填充文件..."
docker exec kafka-broker-1 rm -f /var/lib/kafka/data/fill_disk

sleep 10
echo "[恢复后] ISR状态:"
kafka-topics.sh --describe --topic drill-topic --bootstrap-server localhost:9092
```

### 场景3：网络分区

```bash
#!/bin/bash
# failover-drill-3-network-partition.sh

echo "=== 场景3: 网络分区演练 ==="

# 1. 当前ISR状态
echo "[初始]"
kafka-topics.sh --describe --topic drill-topic --bootstrap-server localhost:9092

# 2. 模拟Broker 2与其他Broker网络延迟
echo "[故障注入] 给Broker 2添加500ms网络延迟..."
docker exec kafka-broker-2 tc qdisc add dev eth0 root netem delay 500ms

# 3. 观察30秒
for i in {1..15}; do
    sleep 2
    echo "T+$((i*2))秒:"
    kafka-topics.sh --describe --topic drill-topic --bootstrap-server localhost:9092 2>/dev/null | grep "Isr:"
done

# 4. 检查Consumer Lag
echo "[Consumer Lag]"
kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --group drill-group \
  --describe 2>/dev/null

# 5. 恢复网络
echo "[恢复] 移除网络延迟..."
docker exec kafka-broker-2 tc qdisc del dev eth0 root

sleep 10
echo "[恢复后]"
kafka-topics.sh --describe --topic drill-topic --bootstrap-server localhost:9092
```

### 场景4：Consumer Lag雪崩

```bash
#!/bin/bash
# failover-drill-4-consumer-lag.sh

echo "=== 场景4: Consumer Lag雪崩演练 ==="

TOPIC="lag-drill-topic"
GROUP="lag-drill-group"

# 1. 启动Producer持续写入
echo "[1] 启动Producer (10000条/秒)..."
kafka-producer-perf-test.sh \
  --topic $TOPIC \
  --num-records 1000000 \
  --record-size 1024 \
  --throughput 10000 \
  --producer-props bootstrap.servers=localhost:9092 \
  > /dev/null 2>&1 &
PROD_PID=$!

sleep 5

# 2. 启动Consumer并立即停止
echo "[2] 启动Consumer..."
kafka-console-consumer.sh \
  --topic $TOPIC \
  --bootstrap-server localhost:9092 \
  --group $GROUP \
  --timeout-ms 3000 \
  > /dev/null 2>&1 &

sleep 1
# Consumer已经因为timeout退出了

# 3. 观察Lag积累
echo "[3] 观察Lag..."
for i in {1..30}; do
    sleep 2
    LAG=$(kafka-consumer-groups.sh \
      --bootstrap-server localhost:9092 \
      --group $GROUP \
      --describe 2>/dev/null | tail -1 | awk '{print $6}')
    echo "  T+$((i*2))秒 | Lag: ${LAG:-0}"
done

# 4. 增加Consumer配置提高追赶速度
echo "[4] 以高消费速率重新启动Consumer..."
kafka-consumer-perf-test.sh \
  --topic $TOPIC \
  --bootstrap-server localhost:9092 \
  --messages 1000000 \
  --group "${GROUP}-fast" \
  --consumer-props \
    fetch.max.bytes=104857600 \
    max.partition.fetch.bytes=10485760 \
    max.poll.records=5000 \
    enable.auto.commit=false \
  --hide-header 2>&1

echo "[5] 最终Lag:"
kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --group $GROUP \
  --describe 2>/dev/null

kill $PROD_PID 2>/dev/null
```

---

## 六、产出报告模板

```markdown
# Kafka深度调优报告

## 1. 测试环境
- Kafka版本: 3.5.0
- Broker配置: 3节点, 4核16GB, SSD×500GB
- 网络: 1Gbps
- 测试数据: 1000万条 × 1KB, Topic 6分区 3副本

## 2. Partition实验

| Partitions | Throughput(rec/s) | P99 Latency(ms) | CPU% | 结论 |
|------------|-------------------|-----------------|------|------|
| 1 | 80,000 | 120 | 15% | 吞吐不足 |
| 3 | 200,000 | 85 | 35% | 仍有上升空间 |
| 6 | 320,000 | 65 | 55% | **最优** |
| 10 | 380,000 | 55 | 72% | 吞吐最高但CPU偏高 |
| 20 | 300,000 | 110 | 95% | CPU瓶颈 |
| 30 | 220,000 | 180 | 98% | 过度分区 |

**结论**: 当前硬件最优Partition数 = 6-10

## 3. Producer参数实验

### acks 对比
| acks | Throughput | Avg Latency | 可靠性 |
|------|------------|-------------|--------|
| 0 | 420,000 | 5ms | 可能丢数据 |
| 1 | 320,000 | 8ms | 基本可靠 |
| all | 250,000 | 15ms | 最可靠 |

### compression 对比
| 算法 | Throughput | 压缩比 | CPU使用 |
|------|------------|--------|---------|
| none | 280,000 | 1.0x | 15% |
| gzip | 120,000 | 0.3x | 45% |
| snappy | 300,000 | 0.6x | 22% |
| lz4 | 350,000 | 0.55x | 20% |
| zstd | 220,000 | 0.35x | 35% |

**推荐**: lz4 (最佳性价比)

## 4. 故障演练结果

| 场景 | 影响范围 | 恢复时间 | Producer影响 | Consumer影响 |
|------|----------|----------|-------------|-------------|
| Broker宕机 | 该Broker的Leader分区 | 3-5秒 | 短暂重试后恢复 | 可能触发Rebalance |
| 磁盘满 | 该Broker全部不可用 | 手动清理后恢复 | 写入失败 | 分区不可用 |
| 网络分区 | ISR收缩 | 网络恢复后自动恢复 | 延迟增加 | Lag上升 |
| Consumer Lag | Lag持续增长 | 取决于追赶速度 | 无影响 | 延迟处理 |

## 5. 生产推荐配置

[见3.3节的生产推荐配置]

## 6. 监控指标建议

以下指标必须监控:
- UnderReplicatedPartitions > 0 → 告警
- ActiveControllerCount != 1 → 告警
- OfflinePartitionsCount > 0 → 告警
- ConsumerGroup Lag > 10000 → 告警
- DiskUsage > 85% → 告警
```

---

## 七、交付物清单

1. **Kafka调优基准测试报告**：至少20个实验组合的结果数据和图表
2. **生产环境推荐配置**：高吞吐/低延迟/高可靠/折中 四套配置
3. **故障演练SOP**：4个场景的标准操作手册（含预期现象和恢复步骤）
4. **Kafka监控Dashboard配置**：Prometheus + Grafana JSON

---

## 八、评分标准

| 评分项 | 权重 | 优秀标准 |
|--------|------|----------|
| 实验完整性 | 30% | 完成全部4组实验，数据真实有效 |
| 结论质量 | 25% | 每个实验都能给出有数据支撑的结论 |
| 故障演练 | 25% | 完成全部4个场景，有完整的演练报告 |
| 监控搭建 | 10% | 搭建了可用的Kafka监控Dashboard |
| 报告质量 | 10% | 格式规范，图表清晰，结论实用 |

---

## 九、完整240参数组合Python实验脚本（正交实验法）

### 9.1 全因子实验设计

```
实验参数空间:
  acks:             [0, 1, all]
  batch.size:       [16384, 32768, 65536, 131072, 262144, 524288, 1048576]
  linger.ms:        [0, 2, 5, 10, 20, 50, 100, 200]
  compression.type: [none, gzip, snappy, lz4, zstd]
  buffer.memory:    [16777216, 33554432, 67108864, 134217728]

全组合: 3 × 7 × 8 × 5 × 4 = 3360 个组合

关键参数组合: 根据前期经验，筛选为 acks×batch×linger×compression = 840组合
运行时间预估: 每组合约30秒, 840组合 ÷ 2并发 ≈ 3.5小时
```

### 9.2 完整Python自动化实验脚本

```python
#!/usr/bin/env python3
"""
kafka_full_benchmark.py
Kafka Producer 240+参数组合正交实验 — 完整自动化脚本

功能:
  1. 全因子正交实验 (840个有效组合)
  2. 自动创建/清理Topic
  3. 并发执行 (可配置并发度)
  4. CSV输出 + JSON汇总报告
  5. 自动生成图表 (需要matplotlib)

用法: python kafka_full_benchmark.py --concurrency 2
"""

import subprocess
import json
import time
import csv
import os
import sys
import argparse
import threading
import queue
from itertools import product
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    HAS_PLT = True
except ImportError:
    HAS_PLT = False

# ======================== 配置 ========================

@dataclass
class BenchmarkConfig:
    """基准测试全局配置"""
    bootstrap_servers: str = "localhost:9092"
    topic_prefix: str = "perf-full-bench"
    num_records: int = 2000000
    record_size: int = 512
    replication_factor: int = 3
    partition_count: int = 12
    concurrency: int = 1
    warmup_records: int = 50000
    output_dir: str = "./benchmark_results"
    cleanup_topics: bool = True
    timeout_seconds: int = 600

# ======================== 参数空间定义 ========================

PARAM_SPACE = {
    'acks': ['0', '1', 'all'],
    'batch.size': [16384, 32768, 65536, 131072, 262144, 524288, 1048576],
    'linger.ms': [0, 2, 5, 10, 20, 50, 100, 200],
    'compression.type': ['none', 'gzip', 'snappy', 'lz4', 'zstd'],
}

PARAM_DEFAULT = {
    'acks': '1',
    'batch.size': 65536,
    'linger.ms': 5,
    'compression.type': 'lz4',
    'buffer.memory': 67108864,
    'max.in.flight.requests.per.connection': 5,
    'retries': 0,
}

# ======================== 结果数据结构 ========================

@dataclass
class BenchmarkResult:
    """单次实验结果"""
    experiment_id: int = 0
    timestamp: str = ""
    
    # 参数
    acks: str = ""
    batch_size: int = 0
    linger_ms: int = 0
    compression_type: str = ""
    
    # 吞吐指标
    records_per_sec: float = 0.0
    mb_per_sec: float = 0.0
    
    # 延迟指标 (ms)
    avg_latency_ms: float = 0.0
    max_latency_ms: float = 0.0
    p50_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0
    p999_latency_ms: float = 0.0
    
    # 系统指标
    cpu_percent: float = 0.0
    duration_seconds: float = 0.0
    
    # 性价比指标
    throughput_per_cpu: float = 0.0
    
    success: bool = True
    error_msg: str = ""


class KafkaBenchmarkRunner:
    """Kafka压测执行器"""
    
    def __init__(self, config: BenchmarkConfig):
        self.config = config
        self.results: List[BenchmarkResult] = []
        self.result_queue = queue.Queue()
        self.lock = threading.Lock()
        self.start_time = None
        
    def create_topic(self, topic_name: str) -> bool:
        """创建测试Topic"""
        try:
            subprocess.run([
                'kafka-topics.sh', '--create',
                '--topic', topic_name,
                '--partitions', str(self.config.partition_count),
                '--replication-factor', str(self.config.replication_factor),
                '--bootstrap-server', self.config.bootstrap_servers,
                '--if-not-exists',
            ], capture_output=True, timeout=30, check=False)
            return True
        except Exception as e:
            print(f"  创建Topic失败: {e}")
            return False
    
    def delete_topic(self, topic_name: str):
        """删除测试Topic"""
        try:
            subprocess.run([
                'kafka-topics.sh', '--delete',
                '--topic', topic_name,
                '--bootstrap-server', self.config.bootstrap_servers,
            ], capture_output=True, timeout=30, check=False)
        except Exception:
            pass
    
    def run_single_benchmark(self, topic_name: str, props: Dict) -> Tuple[str, str]:
        """执行单次Producer压测, 返回(stdout, stderr)"""
        props_str = ' '.join([f'{k}={v}' for k, v in props.items()])
        
        cmd = [
            'kafka-producer-perf-test.sh',
            '--topic', topic_name,
            '--num-records', str(self.config.num_records),
            '--record-size', str(self.config.record_size),
            '--throughput', '-1',
            '--producer-props', props_str,
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.config.timeout_seconds
            )
            return result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return "", "TIMEOUT"
        except Exception as e:
            return "", str(e)
    
    def parse_output(self, stdout: str, stderr: str) -> Optional[Dict]:
        """解析 kafka-producer-perf-test.sh 输出"""
        full_output = stdout + '\n' + stderr
        
        if "TIMEOUT" in stderr or "ERROR" in stderr.upper():
            return None
        
        metrics = {}
        for line in full_output.split('\n'):
            line = line.strip()
            
            if 'records sent' in line:
                parts = line.replace('(', '').replace(')', '').split()
                try:
                    metrics['records_per_sec'] = float(parts[0].replace(',', ''))
                    metrics['mb_per_sec'] = float(parts[2].replace(',', ''))
                except (ValueError, IndexError):
                    pass
            
            elif 'avg latency' in line:
                parts = line.split()
                try:
                    metrics['avg_latency_ms'] = float(parts[3])
                    metrics['max_latency_ms'] = float(parts[6])
                except (ValueError, IndexError):
                    pass
            
            elif 'percentile' in line.lower() or '50th' in line:
                parts = line.split()
                try:
                    p50_idx = next(i for i, p in enumerate(parts) if '50th' in p or '50' == p)
                    p95_idx = next(i for i, p in enumerate(parts) if '95th' in p or '95' == p)
                    p99_idx = next(i for i, p in enumerate(parts) if '99th' in p or '99' == p)
                    metrics['p50_latency_ms'] = float(parts[p50_idx + 1])
                    metrics['p95_latency_ms'] = float(parts[p95_idx + 1])
                    metrics['p99_latency_ms'] = float(parts[p99_idx + 1])
                    if any('99.9' in p for p in parts):
                        p999_idx = next(i for i, p in enumerate(parts) if '99.9' in p)
                        metrics['p999_latency_ms'] = float(parts[p999_idx + 1])
                except (ValueError, IndexError, StopIteration):
                    pass
        
        return metrics if metrics else None
    
    def warmup(self, topic_name: str, props: Dict):
        """预热Producer连接"""
        warmup_props = dict(props)
        warmup_props['batch.size'] = 16384
        
        subprocess.run([
            'kafka-producer-perf-test.sh',
            '--topic', topic_name,
            '--num-records', str(self.config.warmup_records),
            '--record-size', '100',
            '--throughput', '-1',
            '--producer-props',
            ' '.join([f'{k}={v}' for k, v in warmup_props.items()]),
        ], capture_output=True, timeout=30)
    
    def experiment_worker(self, worker_id: int, combinations: List[Tuple], 
                          topic_name: str):
        """工作线程: 执行一组参数组合"""
        for idx, combo in enumerate(combinations):
            acks, batch_size, linger, compression = combo
            
            # 构建Producer配置
            props = dict(PARAM_DEFAULT)
            props['acks'] = str(acks)
            props['batch.size'] = batch_size
            props['linger.ms'] = linger
            props['compression.type'] = compression
            
            result = BenchmarkResult(
                experiment_id=idx + worker_id * 1000,
                timestamp=datetime.now().isoformat(),
                acks=str(acks),
                batch_size=batch_size,
                linger_ms=linger,
                compression_type=compression,
            )
            
            try:
                stdout, stderr = self.run_single_benchmark(topic_name, props)
                metrics = self.parse_output(stdout, stderr)
                
                if metrics:
                    result.records_per_sec = metrics.get('records_per_sec', 0)
                    result.mb_per_sec = metrics.get('mb_per_sec', 0)
                    result.avg_latency_ms = metrics.get('avg_latency_ms', 0)
                    result.max_latency_ms = metrics.get('max_latency_ms', 0)
                    result.p50_latency_ms = metrics.get('p50_latency_ms', 0)
                    result.p95_latency_ms = metrics.get('p95_latency_ms', 0)
                    result.p99_latency_ms = metrics.get('p99_latency_ms', 0)
                    result.p999_latency_ms = metrics.get('p999_latency_ms', 0)
                    result.throughput_per_cpu = (
                        result.records_per_sec / max(result.cpu_percent, 1) * 100
                    )
                    result.success = True
                else:
                    result.success = False
                    result.error_msg = "Failed to parse output"
                    
            except Exception as e:
                result.success = False
                result.error_msg = str(e)
            
            self.result_queue.put(result)
            
            # 进度显示
            completed = self.result_queue.qsize()
            total = len(combinations)
            if completed % 10 == 0 or completed == total:
                print(f"  [Worker {worker_id}] 进度: {completed}/{total} "
                      f"({completed/total*100:.1f}%)")
    
    def run_full_benchmark(self):
        """执行完整的全因子实验"""
        self.start_time = time.time()
        
        # 生成所有参数组合
        all_combos = list(product(
            PARAM_SPACE['acks'],
            PARAM_SPACE['batch.size'],
            PARAM_SPACE['linger.ms'],
            PARAM_SPACE['compression.type'],
        ))
        
        total_combos = len(all_combos)
        print(f"\n{'='*60}")
        print(f"Kafka Full Benchmark - 全因子实验")
        print(f"{'='*60}")
        print(f"参数组合总数: {total_combos}")
        print(f"并发Worker数: {self.config.concurrency}")
        print(f"预计耗时: ~{total_combos * 35 / self.config.concurrency / 60:.0f} 分钟")
        print(f"输出目录: {self.config.output_dir}")
        print(f"{'='*60}\n")
        
        # 创建输出目录
        os.makedirs(self.config.output_dir, exist_ok=True)
        
        # 为每个Worker创建独立Topic
        topics = []
        for w in range(self.config.concurrency):
            topic = f"{self.config.topic_prefix}-w{w}"
            self.create_topic(topic)
            topics.append(topic)
        
        # 均匀分配参数组合给Worker
        chunk_size = (total_combos + self.config.concurrency - 1) // self.config.concurrency
        chunks = [all_combos[i:i+chunk_size] for i in range(0, total_combos, chunk_size)]
        
        # 启动工作线程
        threads = []
        for w in range(self.config.concurrency):
            t = threading.Thread(
                target=self.experiment_worker,
                args=(w, chunks[w], topics[w])
            )
            t.start()
            threads.append(t)
        
        # 等待所有线程完成
        for t in threads:
            t.join()
        
        # 收集结果
        while not self.result_queue.empty():
            self.results.append(self.result_queue.get())
        
        elapsed = time.time() - self.start_time
        print(f"\n实验完成! 总耗时: {elapsed/60:.1f} 分钟")
        print(f"成功: {sum(1 for r in self.results if r.success)} / {len(self.results)}")
        
        # 清理Topic
        if self.config.cleanup_topics:
            for topic in topics:
                self.delete_topic(topic)
        
        return self.results
    
    def save_results(self):
        """保存实验结果到CSV和JSON"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # CSV输出
        csv_path = os.path.join(self.config.output_dir, 
                                f'kafka_full_benchmark_{timestamp}.csv')
        fieldnames = [
            'experiment_id', 'timestamp', 'acks', 'batch_size', 'linger_ms',
            'compression_type', 'records_per_sec', 'mb_per_sec',
            'avg_latency_ms', 'max_latency_ms', 'p50_latency_ms',
            'p95_latency_ms', 'p99_latency_ms', 'p999_latency_ms',
            'cpu_percent', 'duration_seconds', 'throughput_per_cpu',
            'success', 'error_msg'
        ]
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            for r in self.results:
                writer.writerow(asdict(r))
        print(f"CSV结果: {csv_path}")
        
        # JSON汇总
        successful = [r for r in self.results if r.success]
        
        summary = {
            'metadata': {
                'total_experiments': len(self.results),
                'successful': len(successful),
                'failed': len(self.results) - len(successful),
                'timestamp': timestamp,
                'duration_seconds': time.time() - self.start_time,
            },
            'top_by_throughput': sorted(
                successful, key=lambda r: r.records_per_sec, reverse=True
            )[:10],
            'top_by_latency': sorted(
                successful, key=lambda r: r.p99_latency_ms
            )[:10],
            'top_by_efficiency': sorted(
                successful, key=lambda r: r.throughput_per_cpu, reverse=True
            )[:10],
        }
        
        json_path = os.path.join(self.config.output_dir,
                                 f'kafka_full_benchmark_{timestamp}_summary.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, default=str, ensure_ascii=False)
        print(f"JSON汇总: {json_path}")
    
    def generate_reports(self):
        """生成分析报告"""
        successful = [r for r in self.results if r.success]
        if not successful:
            print("无成功结果，跳过报告生成")
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # ===== 分析1: acks影响 =====
        print("\n" + "="*60)
        print("分析1: acks参数对吞吐/延迟的影响")
        print("="*60)
        for acks_val in PARAM_SPACE['acks']:
            group = [r for r in successful if r.acks == str(acks_val)]
            if group:
                avg_tp = sum(r.records_per_sec for r in group) / len(group)
                avg_p99 = sum(r.p99_latency_ms for r in group) / len(group)
                print(f"  acks={acks_val:>3}: 平均吞吐={avg_tp:>10,.0f} rec/s, "
                      f"平均P99延迟={avg_p99:>6.1f}ms")
        
        # ===== 分析2: batch.size最佳值 =====
        print("\n" + "="*60)
        print("分析2: batch.size vs 吞吐量")
        print("="*60)
        batch_perf = {}
        for r in successful:
            bs = r.batch_size
            if bs not in batch_perf:
                batch_perf[bs] = []
            batch_perf[bs].append(r.records_per_sec)
        
        for bs in sorted(batch_perf.keys()):
            avg = sum(batch_perf[bs]) / len(batch_perf[bs])
            max_val = max(batch_perf[bs])
            print(f"  batch.size={bs:>7} ({bs/1024:>5.0f}KB): "
                  f"平均吞吐={avg:>10,.0f} rec/s, 最大={max_val:>10,.0f}")
        
        # ===== 分析3: linger.ms最佳值 =====
        print("\n" + "="*60)
        print("分析3: linger.ms vs P99延迟")
        print("="*60)
        linger_perf = {}
        for r in successful:
            lm = r.linger_ms
            if lm not in linger_perf:
                linger_perf[lm] = []
            linger_perf[lm].append((r.records_per_sec, r.p99_latency_ms))
        
        for lm in sorted(linger_perf.keys()):
            avg_tp = sum(x[0] for x in linger_perf[lm]) / len(linger_perf[lm])
            avg_p99 = sum(x[1] for x in linger_perf[lm]) / len(linger_perf[lm])
            print(f"  linger.ms={lm:>3}: 平均吞吐={avg_tp:>10,.0f} rec/s, "
                  f"平均P99={avg_p99:>6.1f}ms")
        
        # ===== 分析4: compression对比 =====
        print("\n" + "="*60)
        print("分析4: compression.type 综合对比")
        print("="*60)
        print(f"  {'算法':<8} {'吞吐(rec/s)':<15} {'MB/s':<10} {'P99(ms)':<10} "
              f"{'CPU效率':<10}")
        print(f"  {'-'*8} {'-'*15} {'-'*10} {'-'*10} {'-'*10}")
        
        for comp in PARAM_SPACE['compression.type']:
            group = [r for r in successful if r.compression_type == comp]
            if group:
                avg_tp = sum(r.records_per_sec for r in group) / len(group)
                avg_mb = sum(r.mb_per_sec for r in group) / len(group)
                avg_p99 = sum(r.p99_latency_ms for r in group) / len(group)
                avg_eff = sum(r.throughput_per_cpu for r in group) / len(group)
                print(f"  {comp:<8} {avg_tp:>14,.0f} {avg_mb:>9.1f} "
                      f"{avg_p99:>9.1f} {avg_eff:>9.1f}")
        
        # ===== 分析5: 最优配置组合 =====
        print("\n" + "="*60)
        print("分析5: Top-10 综合最优配置")
        print("="*60)
        
        for r in successful:
            r_norm_tp = (r.records_per_sec - min(r2.records_per_sec for r2 in successful)) / \
                        (max(r2.records_per_sec for r2 in successful) - min(r2.records_per_sec for r2 in successful) + 1)
            r_norm_lat = 1 - (r.p99_latency_ms - min(r2.p99_latency_ms for r2 in successful)) / \
                         (max(r2.p99_latency_ms for r2 in successful) - min(r2.p99_latency_ms for r2 in successful) + 1)
            r._score = 0.6 * r_norm_tp + 0.4 * r_norm_lat
        
        top10 = sorted(successful, key=lambda r: r._score, reverse=True)[:10]
        for i, r in enumerate(top10):
            print(f"  #{i+1}: acks={r.acks}, batch={r.batch_size//1024}KB, "
                  f"linger={r.linger_ms}ms, comp={r.compression_type}")
            print(f"       吞吐={r.records_per_sec:,.0f} rec/s, "
                  f"P99={r.p99_latency_ms:.1f}ms, 评分={r._score:.3f}")
        
        # ===== 图表生成 (需要matplotlib) =====
        if HAS_PLT:
            self._generate_charts(successful, timestamp)
    
    def _generate_charts(self, results, timestamp):
        """生成可视化图表"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))
        
        # Chart 1: acks vs Throughput
        ax = axes[0, 0]
        acks_data = {}
        for r in results:
            acks_data.setdefault(r.acks, []).append(r.records_per_sec)
        ax.boxplot([acks_data.get(k, []) for k in ['0', '1', 'all']], 
                    labels=['acks=0', 'acks=1', 'acks=all'])
        ax.set_title('acks vs Throughput')
        ax.set_ylabel('records/sec')
        ax.grid(True, alpha=0.3)
        
        # Chart 2: batch.size vs Throughput
        ax = axes[0, 1]
        batch_data = {}
        for r in results:
            batch_data.setdefault(r.batch_size, []).append(r.records_per_sec)
        sorted_bs = sorted(batch_data.keys())
        avgs = [sum(batch_data[bs])/len(batch_data[bs]) for bs in sorted_bs]
        ax.plot([bs/1024 for bs in sorted_bs], avgs, 'o-', linewidth=2)
        ax.set_title('batch.size vs Throughput')
        ax.set_xlabel('batch.size (KB)')
        ax.set_ylabel('records/sec')
        ax.grid(True, alpha=0.3)
        
        # Chart 3: compression.type comparison
        ax = axes[1, 0]
        comps = list(PARAM_SPACE['compression.type'])
        tp_data = []
        p99_data = []
        for comp in comps:
            group = [r for r in results if r.compression_type == comp]
            tp_data.append(sum(r.records_per_sec for r in group) / len(group) if group else 0)
            p99_data.append(sum(r.p99_latency_ms for r in group) / len(group) if group else 0)
        
        x = range(len(comps))
        width = 0.35
        ax.bar([i - width/2 for i in x], tp_data, width, label='Throughput', alpha=0.8)
        ax_twin = ax.twinx()
        ax_twin.bar([i + width/2 for i in x], p99_data, width, label='P99 Latency', 
                     alpha=0.8, color='orange')
        ax.set_xticks(x)
        ax.set_xticklabels(comps)
        ax.set_title('compression.type Comparison')
        ax.set_ylabel('records/sec')
        ax_twin.set_ylabel('P99 Latency (ms)')
        ax.legend(loc='upper left')
        ax_twin.legend(loc='upper right')
        
        # Chart 4: Pareto Front (Throughput vs P99)
        ax = axes[1, 1]
        tps = [r.records_per_sec for r in results]
        p99s = [r.p99_latency_ms for r in results]
        ax.scatter(tps, p99s, alpha=0.3, s=5)
        ax.set_title('Pareto: Throughput vs P99 Latency')
        ax.set_xlabel('Throughput (rec/s)')
        ax.set_ylabel('P99 Latency (ms)')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        chart_path = os.path.join(self.config.output_dir,
                                  f'kafka_benchmark_charts_{timestamp}.png')
        plt.savefig(chart_path, dpi=150)
        plt.close()
        print(f"图表: {chart_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Kafka Producer 全因子基准测试'
    )
    parser.add_argument('--concurrency', type=int, default=1,
                        help='并发Worker数 (default: 1)')
    parser.add_argument('--num-records', type=int, default=2000000,
                        help='每次测试的记录数 (default: 2000000)')
    parser.add_argument('--record-size', type=int, default=512,
                        help='每条记录大小(字节) (default: 512)')
    parser.add_argument('--bootstrap-servers', type=str, 
                        default='localhost:9092',
                        help='Kafka Bootstrap Servers')
    parser.add_argument('--output-dir', type=str, 
                        default='./benchmark_results',
                        help='结果输出目录')
    parser.add_argument('--skip-charts', action='store_true',
                        help='跳过图表生成')
    parser.add_argument('--quick', action='store_true',
                        help='快速模式: 只测试部分组合(20个)')
    
    args = parser.parse_args()
    
    config = BenchmarkConfig(
        bootstrap_servers=args.bootstrap_servers,
        num_records=args.num_records,
        record_size=args.record_size,
        concurrency=args.concurrency,
        output_dir=args.output_dir,
    )
    
    runner = KafkaBenchmarkRunner(config)
    
    if args.quick:
        global PARAM_SPACE
        PARAM_SPACE = {
            'acks': ['0', '1', 'all'],
            'batch.size': [16384, 65536, 262144],
            'linger.ms': [0, 5, 50],
            'compression.type': ['none', 'lz4', 'zstd'],
        }
        print("快速模式: 参数空间缩减为 3×3×3×3 = 81 组合")
    
    runner.run_full_benchmark()
    runner.save_results()
    runner.generate_reports()
    
    print(f"\n所有结果已保存到: {config.output_dir}")


if __name__ == '__main__':
    main()
```

### 9.3 快速模式运行

```bash
# 快速验证模式 (81个组合, ~40分钟)
python kafka_full_benchmark.py --quick --concurrency 2

# 完整模式 (840个组合, ~3.5小时, 建议 overnight)
python kafka_full_benchmark.py --concurrency 4 --num-records 5000000

# 仅测试指定Bootstrap Server
python kafka_full_benchmark.py \
  --bootstrap-servers "kafka-prod-1:9092,kafka-prod-2:9092" \
  --concurrency 2 \
  --output-dir "./prod_benchmark_results"
```

---

## 十、每种故障演练的详细Bash脚本（含注入命令和恢复命令）

### 10.1 场景1：Broker宕机 — 完整版

```bash
#!/bin/bash
###########################################################################
# kafka-dr-scenario1-broker-crash.sh
# 场景: Broker宕机完整演练
# 覆盖: 单Broker宕机、Leader切换、ISR收缩与恢复、Producer/Consumer影响
###########################################################################

set -euo pipefail

BOOTSTRAP="localhost:9092"
TOPIC="dr-broker-crash"
GROUP="dr-broker-crash-consumer"
BROKER_TO_KILL="kafka-broker-2"
LOG_DIR="/tmp/kafka-dr-scenario1"
RESULTS="${LOG_DIR}/results-$(date +%Y%m%d_%H%M%S).log"

mkdir -p "$LOG_DIR"

log() { echo "[$(date '+%H:%M:%S')] $1" | tee -a "$RESULTS"; }
section() { log ""; log "========== $1 =========="; }

# ==================== 阶段0: 准备 ====================
section "阶段0: 环境准备"

log "创建测试Topic (3分区, 3副本)..."
kafka-topics.sh --create \
    --topic "$TOPIC" \
    --partitions 3 \
    --replication-factor 3 \
    --bootstrap-server "$BOOTSTRAP" \
    --if-not-exists 2>/dev/null || true

log "初始Topic状态:"
kafka-topics.sh --describe --topic "$TOPIC" --bootstrap-server "$BOOTSTRAP" | tee -a "$RESULTS"

# 启动Producer持续发送
log "启动持续Producer (1000条/秒)..."
kafka-producer-perf-test.sh \
    --topic "$TOPIC" \
    --num-records 10000000 \
    --record-size 1024 \
    --throughput 1000 \
    --producer-props \
        bootstrap.servers="$BOOTSTRAP" \
        acks=all \
        retries=3 \
        max.in.flight.requests.per.connection=1 \
    > "${LOG_DIR}/producer.log" 2>&1 &
PRODUCER_PID=$!
log "Producer PID: $PRODUCER_PID"

# 启动Consumer
log "启动Consumer..."
kafka-consumer-perf-test.sh \
    --topic "$TOPIC" \
    --bootstrap-server "$BOOTSTRAP" \
    --messages 10000000 \
    --group "$GROUP" \
    --consumer-props enable.auto.commit=false \
    > "${LOG_DIR}/consumer.log" 2>&1 &
CONSUMER_PID=$!
log "Consumer PID: $CONSUMER_PID"

sleep 10
log "初始状态已稳定"

# ==================== 阶段1: 故障注入前快照 ====================
section "阶段1: 故障前状态快照"

log "=== ISR状态 ==="
kafka-topics.sh --describe --topic "$TOPIC" --bootstrap-server "$BOOTSTRAP" | tee -a "$RESULTS"

log "=== Consumer Lag ==="
kafka-consumer-groups.sh \
    --bootstrap-server "$BOOTSTRAP" \
    --group "$GROUP" \
    --describe 2>/dev/null | tee -a "$RESULTS"

log "=== Producer最新输出 ==="
tail -3 "${LOG_DIR}/producer.log" | tee -a "$RESULTS"

log "=== 目标Broker上作为Leader的分区 ==="
kafka-topics.sh --describe --topic "$TOPIC" --bootstrap-server "$BOOTSTRAP" \
    | grep "Leader: 2" | tee -a "$RESULTS"

# ==================== 阶段2: 故障注入 ====================
section "阶段2: 故障注入 — Kill Broker"

FAIL_TIME=$(date +%s)
log "故障注入时间: $(date -d @$FAIL_TIME '+%H:%M:%S')"

# 方式1: Docker环境
if command -v docker &>/dev/null && docker ps --filter "name=$BROKER_TO_KILL" -q 2>/dev/null | grep -q .; then
    BROKER_CID=$(docker ps --filter "name=$BROKER_TO_KILL" -q)
    log "[Docker] 停止容器 $BROKER_TO_KILL (ID=$BROKER_CID)"
    docker kill "$BROKER_CID"
# 方式2: 直接kill进程
elif pgrep -f "kafka.*broker.*2" &>/dev/null; then
    BROKER_PID=$(pgrep -f "kafka.*broker.*2" | head -1)
    log "[进程] kill -9 Broker PID=$BROKER_PID"
    kill -9 "$BROKER_PID"
else
    log "[模拟] 没有找到Broker 2, 模拟观察..."
fi

# ==================== 阶段3: 观察故障反应 ====================
section "阶段3: 实时观察"

# T+0: 立即观察
sleep 1
log "T+1s: Producer状态"
tail -2 "${LOG_DIR}/producer.log" | tee -a "$RESULTS"

# T+1-30: 观察ISR变化和Leader选举
for t in $(seq 2 2 30); do
    sleep 2
    log "T+${t}s:"
    kafka-topics.sh --describe --topic "$TOPIC" --bootstrap-server "$BOOTSTRAP" 2>/dev/null \
        | grep -E "Topic:|Partition:" | tee -a "$RESULTS"
    
    # 检查Leader切换是否完成
    NO_BROKER2_LEADER=$(kafka-topics.sh --describe --topic "$TOPIC" \
        --bootstrap-server "$BOOTSTRAP" 2>/dev/null \
        | grep "Leader: 2" | wc -l)
    if [ "$NO_BROKER2_LEADER" -eq 0 ]; then
        SWITCH_TIME=$(( $(date +%s) - FAIL_TIME ))
        log "  ✓ Leader切换完成! 耗时: ${SWITCH_TIME}s"
        break
    fi
done

log ""
log "T+30s: Consumer Lag"
kafka-consumer-groups.sh \
    --bootstrap-server "$BOOTSTRAP" \
    --group "$GROUP" \
    --describe 2>/dev/null | tee -a "$RESULTS"

# ==================== 阶段4: 恢复 ====================
section "阶段4: 恢复Broker"

RECOVER_TIME=$(date +%s)
log "恢复时间: $(date -d @$RECOVER_TIME '+%H:%M:%S')"

if command -v docker &>/dev/null; then
    BROKER_CID=$(docker ps -a --filter "name=$BROKER_TO_KILL" -q 2>/dev/null)
    if [ -n "$BROKER_CID" ]; then
        docker start "$BROKER_CID"
        log "Broker容器已启动"
    fi
fi

# 等待Broker完全恢复
for t in $(seq 5 5 60); do
    sleep 5
    log "T+${t}s (恢复后):"
    kafka-topics.sh --describe --topic "$TOPIC" --bootstrap-server "$BOOTSTRAP" 2>/dev/null \
        | grep -E "Isr:" | tee -a "$RESULTS"
    
    # 检查所有ISR是否恢复 (3副本)
    ALL_ISR_OK=$(kafka-topics.sh --describe --topic "$TOPIC" \
        --bootstrap-server "$BOOTSTRAP" 2>/dev/null \
        | grep "Isr:" | grep -v "Isr: 1,3" | grep -v "Isr: 3,1" | wc -l)
    if [ "$ALL_ISR_OK" -eq 0 ]; then
        FULL_RECOVER_TIME=$(( $(date +%s) - RECOVER_TIME ))
        log "  ✓ ISR全部恢复! 恢复耗时: ${FULL_RECOVER_TIME}s"
        break
    fi
done

# ==================== 阶段5: 验证 ====================
section "阶段5: 最终验证"

log "=== 最终Topic状态 ==="
kafka-topics.sh --describe --topic "$TOPIC" --bootstrap-server "$BOOTSTRAP" | tee -a "$RESULTS"

log "=== 最终Consumer Lag ==="
kafka-consumer-groups.sh \
    --bootstrap-server "$BOOTSTRAP" \
    --group "$GROUP" \
    --describe 2>/dev/null | tee -a "$RESULTS"

log "=== Producer最终状态 ==="
tail -5 "${LOG_DIR}/producer.log" | tee -a "$RESULTS"

TOTAL_TIME=$(( $(date +%s) - FAIL_TIME ))
log ""
log "╔═══════════════════════════════════════╗"
log "║  场景1: Broker宕机 — 演练完成          ║"
log "╠═══════════════════════════════════════╣"
log "║  Leader切换耗时: ${SWITCH_TIME:-N/A}s                    ║"
log "║  ISR完全恢复: ${FULL_RECOVER_TIME:-N/A}s                    ║"
log "║  总演练时间: ${TOTAL_TIME}s                        ║"
log "╚═══════════════════════════════════════╝"

# 清理
kill $PRODUCER_PID $CONSUMER_PID 2>/dev/null || true
log "完整日志: $RESULTS"
```

### 10.2 场景2：磁盘满 — 完整版

```bash
#!/bin/bash
###########################################################################
# kafka-dr-scenario2-disk-full.sh
# 场景: Broker磁盘满完整演练
# 覆盖: 磁盘接近满→写入失败→ISR踢出→清理恢复→ISR重新加入
###########################################################################

set -euo pipefail

BOOTSTRAP="localhost:9092"
TOPIC="dr-disk-full"
BROKER_TARGET="kafka-broker-1"
DATA_DIR="/var/lib/kafka/data"
LOG_DIR="/tmp/kafka-dr-scenario2"
RESULTS="${LOG_DIR}/results-$(date +%Y%m%d_%H%M%S).log"

mkdir -p "$LOG_DIR"
log() { echo "[$(date '+%H:%M:%S')] $1" | tee -a "$RESULTS"; }

# ==================== 阶段0: 准备 ====================
log "========== 场景2: Broker磁盘满演练 =========="

kafka-topics.sh --create \
    --topic "$TOPIC" \
    --partitions 3 \
    --replication-factor 3 \
    --bootstrap-server "$BOOTSTRAP" \
    --if-not-exists 2>/dev/null || true

log "初始Topic状态:"
kafka-topics.sh --describe --topic "$TOPIC" --bootstrap-server "$BOOTSTRAP"

log "Broker 1 磁盘使用情况:"
docker exec "$BROKER_TARGET" df -h "$DATA_DIR" 2>/dev/null || df -h

# ==================== 阶段1: 渐进式磁盘填充 ====================
log ""
log "========== 阶段1: 渐进式磁盘填充 =========="

# 获取当前磁盘使用率和可用空间
get_disk_usage() {
    docker exec "$BROKER_TARGET" df "$DATA_DIR" 2>/dev/null \
        | tail -1 | awk '{print $5}' | sed 's/%//'
}

get_avail_mb() {
    docker exec "$BROKER_TARGET" df -m "$DATA_DIR" 2>/dev/null \
        | tail -1 | awk '{print $4}'
}

INITIAL_USAGE=$(get_disk_usage)
INITIAL_AVAIL=$(get_avail_mb)
log "初始使用率: ${INITIAL_USAGE}%, 可用空间: ${INITIAL_AVAIL}MB"

# 计算需要填充的容量 (填充到95%)
TARGET_FILL_MB=$(( INITIAL_AVAIL - 500 ))  # 留500MB
log "计划填充: ${TARGET_FILL_MB}MB (目标使用率 ~95%)"

# 分步填充
CURRENT_FILL=0
STEP=200  # 每次填充200MB
STEP_COUNT=0

while [ "$CURRENT_FILL" -lt "$TARGET_FILL_MB" ]; do
    FILL_NOW=$STEP
    if [ $((CURRENT_FILL + STEP)) -gt "$TARGET_FILL_MB" ]; then
        FILL_NOW=$((TARGET_FILL_MB - CURRENT_FILL))
    fi
    
    STEP_COUNT=$((STEP_COUNT + 1))
    
    log "  步骤${STEP_COUNT}: 填充 ${FILL_NOW}MB..."
    docker exec "$BROKER_TARGET" \
        dd if=/dev/zero of="${DATA_DIR}/fill_${STEP_COUNT}.dat" \
        bs=1M count="$FILL_NOW" 2>/dev/null
    
    CURRENT_FILL=$((CURRENT_FILL + FILL_NOW))
    CURRENT_USAGE=$(get_disk_usage)
    log "  当前使用率: ${CURRENT_USAGE}%"
    
    if [ "$CURRENT_USAGE" -ge 85 ]; then
        log "  ⚠ 使用率已超过85%，观察Kafka行为..."
        docker logs "$BROKER_TARGET" --tail 5 2>&1 | grep -i "disk\|log.dir" || true
    fi
done

FINAL_USAGE=$(get_disk_usage)
log "最终磁盘使用率: ${FINAL_USAGE}%"

# ==================== 阶段2: 观察Kafka对磁盘满的反应 ====================
log ""
log "========== 阶段2: 观察Kafka反应 =========="

log "Broker 1 日志 (最后20行):"
docker logs "$BROKER_TARGET" --tail 20 2>&1 | tee -a "$RESULTS"

log ""
log "尝试写入数据 (预期部分失败):"

# 尝试写入5条消息，观察哪些成功
for i in $(seq 1 5); do
    if echo "test-message-$i-$(date +%s)" | kafka-console-producer.sh \
        --topic "$TOPIC" \
        --bootstrap-server "$BOOTSTRAP" \
        --timeout 3000 2>/dev/null; then
        log "  消息 $i: ✓ 写入成功"
    else
        log "  消息 $i: ✗ 写入失败"
    fi
done

log ""
log "ISR变化 (Broker 1可能被踢出ISR):"
kafka-topics.sh --describe --topic "$TOPIC" --bootstrap-server "$BOOTSTRAP"

log ""
log "查看UnderReplicatedPartitions指标:"
# 通过JMX或kafka-run-class获取
kafka-run-class.sh kafka.tools.JmxTool \
    --object-name kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions \
    --jmx-url service:jmx:rmi:///jndi/rmi://localhost:9999/jmxrmi \
    --one-time true 2>/dev/null || log "  (JMX不可用, 跳过)"

# ==================== 阶段3: 恢复 ====================
log ""
log "========== 阶段3: 恢复 — 清理填充文件 =========="

log "清理填充文件..."
docker exec "$BROKER_TARGET" sh -c "rm -f ${DATA_DIR}/fill_*.dat"

sleep 5

RECOVERY_USAGE=$(get_disk_usage)
log "恢复后磁盘使用率: ${RECOVERY_USAGE}%"

log "等待Broker 1重新加入ISR..."
for t in $(seq 5 5 120); do
    sleep 5
    IN_ISR=$(kafka-topics.sh --describe --topic "$TOPIC" \
        --bootstrap-server "$BOOTSTRAP" 2>/dev/null \
        | grep "Isr:" | grep -c "Isr:.*,1,\|Isr:.*1," || true)
    
    TOTAL_PARTITIONS=$(kafka-topics.sh --describe --topic "$TOPIC" \
        --bootstrap-server "$BOOTSTRAP" 2>/dev/null \
        | grep "Leader:" | wc -l)
    
    log "  T+${t}s: $IN_ISR/$TOTAL_PARTITIONS 分区已恢复Broker 1"
    
    if [ "$IN_ISR" -ge "$TOTAL_PARTITIONS" ]; then
        log "  ✓ 全部ISR已恢复!"
        break
    fi
done

# ==================== 阶段4: 验证 ====================
log ""
log "========== 阶段4: 最终验证 =========="
log "最终Topic状态:"
kafka-topics.sh --describe --topic "$TOPIC" --bootstrap-server "$BOOTSTRAP"

log "验证写入恢复:"
if echo "recovery-test-$(date +%s)" | kafka-console-producer.sh \
    --topic "$TOPIC" \
    --bootstrap-server "$BOOTSTRAP" \
    --timeout 3000 2>/dev/null; then
    log "✓ 写入已恢复正常!"
else
    log "✗ 写入仍然失败，需要进一步排查"
fi

log ""
log "╔═══════════════════════════════════════╗"
log "║  场景2: 磁盘满 — 演练完成              ║"
log "╠═══════════════════════════════════════╣"
log "║  磁盘使用率: ${INITIAL_USAGE}% → ${FINAL_USAGE}% → ${RECOVERY_USAGE}%       ║"
log "║  完整日志: $RESULTS                      ║"
log "╚═══════════════════════════════════════╝"
```

### 10.3 场景3：网络分区 — 完整版

```bash
#!/bin/bash
###########################################################################
# kafka-dr-scenario3-network-partition.sh
# 场景: 网络分区完整演练
# 覆盖: 延迟注入→ISR收缩→Producer超时→网络恢复→ISR重建
###########################################################################

set -euo pipefail

BOOTSTRAP="localhost:9092"
TOPIC="dr-network-partition"
BROKER_TARGET="kafka-broker-2"
LOG_DIR="/tmp/kafka-dr-scenario3"
RESULTS="${LOG_DIR}/results-$(date +%Y%m%d_%H%M%S).log"

mkdir -p "$LOG_DIR"
log() { echo "[$(date '+%H:%M:%S')] $1" | tee -a "$RESULTS"; }

# ==================== 准备 ====================
log "========== 场景3: 网络分区演练 =========="

kafka-topics.sh --create \
    --topic "$TOPIC" \
    --partitions 6 \
    --replication-factor 3 \
    --bootstrap-server "$BOOTSTRAP" \
    --if-not-exists 2>/dev/null || true

log "初始状态:"
kafka-topics.sh --describe --topic "$TOPIC" --bootstrap-server "$BOOTSTRAP"

# 启动Producer (acks=all, 对网络敏感)
kafka-producer-perf-test.sh \
    --topic "$TOPIC" \
    --num-records 5000000 \
    --record-size 1024 \
    --throughput 5000 \
    --producer-props \
        bootstrap.servers="$BOOTSTRAP" \
        acks=all \
        retries=3 \
        request.timeout.ms=5000 \
    > "${LOG_DIR}/producer.log" 2>&1 &
PRODUCER_PID=$!

sleep 5

# ==================== 故障注入: 网络延迟 ====================
log ""
log "========== 故障注入: 网络延迟 =========="

check_network() {
    docker exec "$BROKER_TARGET" ping -c 1 -W 1 kafka-broker-1 2>/dev/null \
        | grep "time=" | grep -oP 'time=\K[0-9.]+' || echo "N/A"
}

RTT_BEFORE=$(check_network)
log "Broker 2 → Broker 1 RTT (故障前): ${RTT_BEFORE}ms"

FAIL_TIME=$(date +%s)

# 注入级别1: 轻微延迟 (100ms)
log "【级别1】注入100ms网络延迟..."
docker exec "$BROKER_TARGET" tc qdisc add dev eth0 root netem delay 100ms 10ms 25% 2>/dev/null || {
    log "  无法使用tc, 使用iptables模拟..."
    docker exec "$BROKER_TARGET" iptables -A INPUT -p tcp --dport 9092 -j DROP 2>/dev/null || true
    docker exec "$BROKER_TARGET" iptables -A OUTPUT -p tcp --dport 9092 -j DROP 2>/dev/null || true
}

sleep 5
RTT_AFTER=$(check_network)
log "Broker 2 → Broker 1 RTT (注入后): ${RTT_AFTER}ms"

# 观察ISR变化
for t in $(seq 5 5 30); do
    sleep 5
    log "T+${t}s ISR状态:"
    kafka-topics.sh --describe --topic "$TOPIC" --bootstrap-server "$BOOTSTRAP" 2>/dev/null \
        | grep "Isr:" | tee -a "$RESULTS"
done

log "Producer状态:"
tail -3 "${LOG_DIR}/producer.log" | tee -a "$RESULTS"

# 注入级别2: 严重延迟 (500ms)
log ""
log "【级别2】升级到500ms网络延迟..."
docker exec "$BROKER_TARGET" tc qdisc change dev eth0 root netem delay 500ms 50ms 25% 2>/dev/null || true

for t in $(seq 5 5 30); do
    sleep 5
    log "T+${t}s ISR状态:"
    kafka-topics.sh --describe --topic "$TOPIC" --bootstrap-server "$BOOTSTRAP" 2>/dev/null \
        | grep "Isr:" | tee -a "$RESULTS"
    
    # 检查Broker 2是否被完全踢出ISR
    ISR_WITH_BROKER2=$(kafka-topics.sh --describe --topic "$TOPIC" \
        --bootstrap-server "$BOOTSTRAP" 2>/dev/null \
        | grep "Isr:" | grep -c "Isr:.*,2,\|Isr:.*,2$" || true)
    log "  Broker 2 仍在ISR中的分区数: $ISR_WITH_BROKER2"
done

# 注入级别3: 完全分区 (丢包100%)
log ""
log "【级别3】完全网络分区..."
docker exec "$BROKER_TARGET" tc qdisc change dev eth0 root netem loss 100% 2>/dev/null || true

sleep 10
log "网络完全分区后的ISR:"
kafka-topics.sh --describe --topic "$TOPIC" --bootstrap-server "$BOOTSTRAP" 2>/dev/null \
    | grep "Isr:" | tee -a "$RESULTS"

# ==================== 恢复 ====================
log ""
log "========== 恢复: 清除网络故障 =========="

RECOVER_TIME=$(date +%s)

# 清除所有tc规则
docker exec "$BROKER_TARGET" tc qdisc del dev eth0 root 2>/dev/null || true
# 清除iptables规则
docker exec "$BROKER_TARGET" iptables -F 2>/dev/null || true

log "网络规则已清除"

RTT_RECOVERED=$(check_network)
log "恢复后RTT: ${RTT_RECOVERED}ms"

# 等待ISR重建
log "等待ISR重建..."
for t in $(seq 5 5 120); do
    sleep 5
    TOTAL=$(kafka-topics.sh --describe --topic "$TOPIC" \
        --bootstrap-server "$BOOTSTRAP" 2>/dev/null | grep "Leader:" | wc -l)
    FULL_ISR=$(kafka-topics.sh --describe --topic "$TOPIC" \
        --bootstrap-server "$BOOTSTRAP" 2>/dev/null \
        | grep "Isr:" | grep -c "Isr:.*,.*,.*," || true)
    
    log "  T+${t}s: ISR完整分区=$FULL_ISR/$TOTAL"
    
    if [ "$FULL_ISR" -ge "$TOTAL" ]; then
        FULL_RECOVER_TIME=$(( $(date +%s) - RECOVER_TIME ))
        log "  ✓ 全部ISR已恢复! 耗时: ${FULL_RECOVER_TIME}s"
        break
    fi
done

# ==================== 验证 ====================
log ""
log "========== 最终验证 =========="
log "最终Topic状态:"
kafka-topics.sh --describe --topic "$TOPIC" --bootstrap-server "$BOOTSTRAP" | tee -a "$RESULTS"

log "Producer最终状态:"
tail -5 "${LOG_DIR}/producer.log" | tee -a "$RESULTS"

TOTAL_TIME=$(( $(date +%s) - FAIL_TIME ))
log ""
log "╔═══════════════════════════════════════╗"
log "║  场景3: 网络分区 — 演练完成            ║"
log "╠═══════════════════════════════════════╣"
log "║  故障持续时间: ${TOTAL_TIME}s                      ║"
log "║  ISR恢复耗时: ${FULL_RECOVER_TIME:-N/A}s                      ║"
log "╚═══════════════════════════════════════╝"

kill $PRODUCER_PID 2>/dev/null || true
```

### 10.4 场景4：Consumer Lag雪崩 — 完整版

```bash
#!/bin/bash
###########################################################################
# kafka-dr-scenario4-consumer-lag-avalanche.sh
# 场景: Consumer Lag雪崩完整演练
# 覆盖: Lag累积→消费者恢复→追赶策略→不同参数组合对比
###########################################################################

set -euo pipefail

BOOTSTRAP="localhost:9092"
TOPIC="dr-lag-avalanche"
GROUP="dr-lag-group"
LOG_DIR="/tmp/kafka-dr-scenario4"
RESULTS="${LOG_DIR}/results-$(date +%Y%m%d_%H%M%S).log"

mkdir -p "$LOG_DIR"
log() { echo "[$(date '+%H:%M:%S')] $1" | tee -a "$RESULTS"; }

# ==================== 准备 ====================
log "========== 场景4: Consumer Lag雪崩演练 =========="

# 创建高吞吐Topic (12分区)
kafka-topics.sh --create \
    --topic "$TOPIC" \
    --partitions 12 \
    --replication-factor 1 \
    --bootstrap-server "$BOOTSTRAP" \
    --if-not-exists 2>/dev/null || true

log "Topic创建完成: 12分区"

# 获取当前每个分区的起始offset
log "记录初始Offset..."
declare -A INITIAL_OFFSETS
while IFS=: read -r topic partition offset; do
    INITIAL_OFFSETS[$partition]=$offset
done < <(kafka-run-class.sh kafka.tools.GetOffsetShell \
    --broker-list "$BOOTSTRAP" \
    --topic "$TOPIC" \
    --time -2 2>/dev/null)

# ==================== 阶段1: 快速写入数据积累Lag ====================
log ""
log "========== 阶段1: 快速写入 — 积累Lag =========="

log "启动Producer (50000条/秒, 共500万条)..."
kafka-producer-perf-test.sh \
    --topic "$TOPIC" \
    --num-records 5000000 \
    --record-size 512 \
    --throughput 50000 \
    --producer-props \
        bootstrap.servers="$BOOTSTRAP" \
        acks=1 \
        compression.type=lz4 \
        linger.ms=5 \
    > "${LOG_DIR}/producer-fast.log" 2>&1 &
PRODUCER_PID=$!

# 同时启动一个慢速Consumer (只能消费1000条/秒)
log "启动慢速Consumer (故意制造Lag)..."
kafka-consumer-perf-test.sh \
    --topic "$TOPIC" \
    --bootstrap-server "$BOOTSTRAP" \
    --messages 100000 \
    --group "$GROUP" \
    --consumer-props \
        max.poll.records=10 \
        fetch.max.wait.ms=100 \
        enable.auto.commit=false \
    > "${LOG_DIR}/consumer-slow.log" 2>&1 &
SLOW_CONSUMER_PID=$!

wait $SLOW_CONSUMER_PID 2>/dev/null || true

# 等待Producer完成
wait $PRODUCER_PID 2>/dev/null || true

# ==================== 阶段2: 测量Lag ====================
log ""
log "========== 阶段2: 测量积累的Lag =========="

log "Consumer Group状态:"
kafka-consumer-groups.sh \
    --bootstrap-server "$BOOTSTRAP" \
    --group "$GROUP" \
    --describe 2>/dev/null | tee -a "$RESULTS"

TOTAL_LAG=0
while IFS= read -r line; do
    LAG=$(echo "$line" | awk '{print $6}')
    if [[ "$LAG" =~ ^[0-9]+$ ]]; then
        TOTAL_LAG=$((TOTAL_LAG + LAG))
    fi
done < <(kafka-consumer-groups.sh \
    --bootstrap-server "$BOOTSTRAP" \
    --group "$GROUP" \
    --describe 2>/dev/null | tail -n +3)

log "总Lag: ${TOTAL_LAG} 条"

# ==================== 阶段3: 对比不同追赶策略 ====================
log ""
log "========== 阶段3: 追赶策略对比 =========="

declare -A STRATEGIES
STRATEGIES=(
    ["strategy1_default"]="max.poll.records=500 fetch.min.bytes=1"
    ["strategy2_large_fetch"]="max.poll.records=5000 fetch.min.bytes=1048576 fetch.max.bytes=104857600"
    ["strategy3_max_parallel"]="max.poll.records=10000 fetch.min.bytes=10485760 max.partition.fetch.bytes=10485760"
)

for strategy_name in "${!STRATEGIES[@]}"; do
    strategy_props="${STRATEGIES[$strategy_name]}"
    
    log ""
    log "--- 测试策略: $strategy_name ---"
    log "参数: $strategy_props"
    
    # 创建独立Consumer Group
    test_group="${GROUP}-${strategy_name}"
    
    START=$(date +%s%3N)
    
    kafka-consumer-perf-test.sh \
        --topic "$TOPIC" \
        --bootstrap-server "$BOOTSTRAP" \
        --messages 500000 \
        --group "$test_group" \
        --consumer-props $strategy_props enable.auto.commit=false \
        --hide-header 2>&1 | tee "${LOG_DIR}/consumer-${strategy_name}.log"
    
    END=$(date +%s%3N)
    DURATION=$((END - START))
    
    # 解析吞吐
    THROUGHPUT=$(grep -oP '(\d+\.\d+) MB/sec' "${LOG_DIR}/consumer-${strategy_name}.log" \
        | head -1 | awk '{print $1}' || echo "N/A")
    
    log "  耗时: ${DURATION}ms, 吞吐: ${THROUGHPUT} MB/s"
    
    # 记录结果供汇总
    echo "$strategy_name|$DURATION|$THROUGHPUT|$strategy_props" >> "${LOG_DIR}/strategy_comparison.txt"
done

# ==================== 阶段4: 结果汇总 ====================
log ""
log "========== 阶段4: 策略对比结果 =========="
log ""
printf "%-25s %-12s %-12s %s\n" "策略" "耗时(ms)" "吞吐(MB/s)" "参数"
printf "%-25s %-12s %-12s %s\n" "----" "--------" "----------" "----"

if [ -f "${LOG_DIR}/strategy_comparison.txt" ]; then
    while IFS='|' read -r name duration throughput props; do
        printf "%-25s %-12s %-12s %s\n" "$name" "$duration" "$throughput" "$props"
    done < "${LOG_DIR}/strategy_comparison.txt"
fi

# 最终Lag
log ""
log "最终Lag状态:"
for g in "${!STRATEGIES[@]}"; do
    test_group="${GROUP}-${g}"
    log "Group: $test_group"
    kafka-consumer-groups.sh \
        --bootstrap-server "$BOOTSTRAP" \
        --group "$test_group" \
        --describe 2>/dev/null | tail -n +3 | tee -a "$RESULTS"
done

log ""
log "╔═══════════════════════════════════════╗"
log "║  场景4: Consumer Lag — 演练完成        ║"
log "╠═══════════════════════════════════════╣"
log "║  积累Lag: ${TOTAL_LAG} 条                      ║"
log "║  完整日志: $RESULTS                      ║"
log "╚═══════════════════════════════════════╝"
```

---

## 十一、调优基准测试报告的完整表格模板

```markdown
# Kafka深度调优基准测试报告

> **测试日期**: YYYY-MM-DD  
> **测试人员**: [姓名]  
> **Kafka版本**: X.X.X  
> **报告版本**: v1.0  

---

## 1. 测试环境

### 1.1 硬件配置

| 组件 | 配置 |
|------|------|
| Broker节点数 | 3 |
| CPU | Intel Xeon E5-2680 v4 @ 2.40GHz, 8核 |
| 内存 | 32GB DDR4 ECC |
| 系统盘 | SSD 480GB (SATA) |
| 数据盘 | NVMe SSD 1TB × 2 (RAID 0) |
| 网络 | 10Gbps Ethernet |
| OS | CentOS 7.9 / Ubuntu 20.04 LTS |
| 文件系统 | XFS (挂载选项: noatime,nodiratime) |

### 1.2 软件配置

| 组件 | 版本/配置 |
|------|----------|
| Kafka | 3.5.0 |
| Java | OpenJDK 11.0.20 (G1GC) |
| Zookeeper | 3.8.1 (KRaft模式可选) |
| 压测工具 | kafka-producer-perf-test.sh (自带) |
| 监控 | JMX + Prometheus 2.45 + Grafana 10.0 |

### 1.3 Broker JVM配置

```
KAFKA_HEAP_OPTS="-Xms8G -Xmx8G"
KAFKA_JVM_PERFORMANCE_OPTS="
  -XX:+UseG1GC
  -XX:MaxGCPauseMillis=20
  -XX:InitiatingHeapOccupancyPercent=35
  -XX:G1HeapRegionSize=16M
  -XX:MinMetaspaceFreeRatio=50
  -XX:MaxMetaspaceFreeRatio=80
"
```

### 1.4 OS调优

| 参数 | 值 | 说明 |
|------|-----|------|
| vm.swappiness | 1 | 减少内存交换 |
| net.core.rmem_max | 134217728 | 最大接收缓冲 |
| net.core.wmem_max | 134217728 | 最大发送缓冲 |
| net.ipv4.tcp_rmem | 4096 87380 134217728 | TCP接收缓冲 |
| net.ipv4.tcp_wmem | 4096 65536 134217728 | TCP发送缓冲 |
| vm.dirty_background_ratio | 5 | 后台刷脏页阈值 |
| vm.dirty_ratio | 60 | 强制刷脏页阈值 |

---

## 2. Partition级别调优实验

### 2.1 实验设计

| 参数 | 值 |
|------|-----|
| 测试数据量 | 1000万条/次 |
| 记录大小 | 512字节 |
| 副本数 | 3 |
| Producer acks | 1 |
| Producer压缩 | lz4 |
| 测试Partition数 | 1, 3, 6, 8, 10, 12, 15, 20, 30, 50 |

### 2.2 实验结果

| Partitions | Throughput (rec/s) | MB/s | Avg Latency (ms) | P50 (ms) | P95 (ms) | P99 (ms) | P999 (ms) | CPU% | Disk IO (MB/s) |
|------------|-------------------|------|------------------|----------|----------|----------|-----------|------|---------------|
| 1 | 85,000 | 43.5 | 18 | 15 | 35 | 120 | 250 | 12 | 45 |
| 3 | 235,000 | 120.1 | 14 | 11 | 28 | 85 | 180 | 32 | 125 |
| 6 | 420,000 | 214.8 | 12 | 9 | 22 | 65 | 140 | 55 | 220 |
| 8 | 510,000 | 260.7 | 14 | 11 | 25 | 70 | 155 | 68 | 270 |
| 10 | 575,000 | 294.0 | 16 | 13 | 30 | 80 | 170 | 78 | 305 |
| 12 | 540,000 | 276.1 | 19 | 15 | 38 | 95 | 200 | 82 | 290 |
| 15 | 480,000 | 245.4 | 24 | 19 | 50 | 120 | 260 | 88 | 260 |
| 20 | 395,000 | 201.9 | 32 | 25 | 70 | 180 | 380 | 93 | 210 |
| 30 | 280,000 | 143.1 | 48 | 38 | 110 | 260 | 520 | 97 | 155 |
| 50 | 190,000 | 97.1 | 72 | 55 | 180 | 420 | 850 | 98 | 105 |

### 2.3 结论与建议

| 指标 | 最优值 | 分析 |
|------|--------|------|
| 最高吞吐 | 10 partitions (575,000 rec/s) | 此时CPU使用率78%，仍有余量 |
| 最优性价比 | 8-10 partitions | 吞吐接近峰值，CPU使用率合理 |
| 推荐配置 | 10 partitions | 兼顾吞吐和延迟 |

---

## 3. Producer参数调优实验

### 3.1 acks对比

| acks | Throughput (rec/s) | Avg Latency (ms) | P99 (ms) | 可靠性 | 适用场景 |
|------|-------------------|------------------|----------|--------|----------|
| 0 | 680,000 | 3 | 15 | 可能丢数据 | 日志收集（可容忍少量丢失） |
| 1 | 575,000 | 8 | 45 | Leader确认 | 推荐（平衡） |
| all | 420,000 | 18 | 95 | 最高可靠 | 金融/订单（零丢失要求） |

### 3.2 batch.size对比

| batch.size | KB | Throughput (rec/s) | P99 (ms) | 内存占用(MB) | 分析 |
|------------|-----|-------------------|----------|-------------|------|
| 16384 | 16 | 380,000 | 35 | 12 | 吞吐不足 |
| 32768 | 32 | 480,000 | 38 | 18 | |
| 65536 | 64 | 540,000 | 42 | 28 | 推荐中等场景 |
| 131072 | 128 | 575,000 | 48 | 45 | **最优平衡** |
| 262144 | 256 | 590,000 | 58 | 68 | 高吞吐首选 |
| 524288 | 512 | 595,000 | 78 | 98 | 吞吐增益递减 |
| 1048576 | 1024 | 598,000 | 110 | 160 | 延迟显著恶化 |

### 3.3 linger.ms对比

| linger.ms | Throughput (rec/s) | P50 (ms) | P99 (ms) | 分析 |
|-----------|-------------------|----------|----------|------|
| 0 | 430,000 | 8 | 38 | 低延迟但吞吐低 |
| 2 | 520,000 | 10 | 42 | |
| 5 | 570,000 | 12 | 48 | **推荐** |
| 10 | 585,000 | 15 | 55 | 吞吐接近顶峰 |
| 20 | 590,000 | 22 | 70 | |
| 50 | 595,000 | 48 | 120 | 延迟显著增加 |
| 100 | 598,000 | 95 | 220 | 不推荐 |
| 200 | 600,000 | 185 | 380 | 延迟不可接受 |

### 3.4 compression.type对比

| 算法 | Throughput (rec/s) | 压缩比 | P99 (ms) | CPU% | 网络流量(MB/s) | 综合评价 |
|------|-------------------|--------|----------|------|---------------|----------|
| none | 480,000 | 1.00x | 40 | 18 | 245 | CPU最省但网络流量大 |
| gzip | 210,000 | 0.32x | 185 | 68 | 78 | 压缩最好但最慢 |
| snappy | 530,000 | 0.62x | 48 | 28 | 152 | 综合均衡 |
| lz4 | 585,000 | 0.55x | 45 | 25 | 135 | **推荐（最佳性价比）** |
| zstd | 380,000 | 0.35x | 72 | 45 | 86 | 压缩好但吞吐中等 |

### 3.5 Producer综合最优配置

| 场景 | acks | batch.size | linger.ms | compression | buffer.memory | max.in.flight |
|------|------|-----------|-----------|-------------|---------------|---------------|
| 🚀 极限吞吐 | 1 | 524288 (512KB) | 20 | lz4 | 134217728 | 5 |
| ⚡ 低延迟 | 1 | 32768 (32KB) | 2 | snappy | 67108864 | 5 |
| 🛡 高可靠 | all | 131072 (128KB) | 5 | lz4 | 67108864 | 1 |
| ⚖ 均衡 | 1 | 131072 (128KB) | 5 | lz4 | 67108864 | 5 |

---

## 4. Consumer调优实验

### 4.1 max.poll.records对比

| max.poll.records | Throughput (MB/s) | Poll间隔(ms) | 分析 |
|------------------|-------------------|-------------|------|
| 50 | 35 | 120 | 频繁Poll，效率低 |
| 100 | 58 | 180 | |
| 500 | 120 | 350 | **推荐** |
| 1000 | 155 | 520 | 高吞吐但poll间隔大 |
| 5000 | 165 | 1100 | 可能导致session超时 |

### 4.2 fetch参数优化

| 参数组合 | Throughput (MB/s) | 单次Fetch大小(MB) | 分析 |
|----------|-------------------|-------------------|------|
| 默认 (fetch.min=1, max=50MB) | 95 | 0.5-5 | 基线 |
| min=1MB, max=100MB | 140 | 2-15 | 有效提升 |
| min=10MB, max=200MB | 168 | 10-30 | **最优** |
| min=50MB, max=500MB | 172 | 20-40 | 增益递减 |

---

## 5. 故障演练结果

### 5.1 演练汇总

| 场景 | 故障类型 | 注入方式 | 检测时间 | 恢复时间 | 数据影响 | 评分 |
|------|---------|---------|---------|---------|---------|------|
| 1 | Broker宕机 | kill -9 / docker kill | 3s | 5s (Leader切换) + 45s (ISR恢复) | 无丢数据，延迟抖动3s | ✅ |
| 2 | 磁盘满 | dd填充磁盘 | 即时 | 手动清理后30s | 受影响分区写入失败 | ⚠️ |
| 3 | 网络分区(100ms) | tc netem | 15s | ISR保持正常 | 延迟增加但未丢数据 | ✅ |
| 3 | 网络分区(500ms) | tc netem | 10s | 恢复后60s重建ISR | ISR收缩到2副本 | ⚠️ |
| 3 | 完全网络分区 | tc netem loss 100% | 5s | 恢复后90s重建ISR | 目标Broker被踢出ISR | ⚠️ |
| 4 | Consumer Lag | 慢Consumer | 持续 | 调整参数后2分钟追上 | 处理延迟 | ✅ |

### 5.2 关键发现

1. **Leader切换时间**: 3-5秒（由 `unclean.leader.election.enable=false` 和 `controlled.shutdown` 控制）
2. **ISR恢复时间**: 45-90秒（取决于分区数量和副本同步速度）
3. **Producer重试行为**: acks=all时自动重试，对业务无感知（需配合 `enable.idempotence=true`）
4. **Consumer影响**: Rebalance耗时与分区数和Consumer数量成正比

---

## 6. 生产推荐配置

### 6.1 四套配置对比

| 维度 | 高吞吐 | 低延迟 | 均衡 | 低成本 |
|------|--------|--------|------|--------|
| acks | 1 | 1 | 1 | 0 |
| batch.size | 512KB | 32KB | 128KB | 256KB |
| linger.ms | 20 | 2 | 5 | 10 |
| compression | lz4 | snappy | lz4 | lz4 |
| buffer.memory | 256MB | 64MB | 128MB | 64MB |
| partitions | 15 | 6 | 10 | 8 |
| replication | 2 | 3 | 3 | 2 |
| min.insync.replicas | 1 | 2 | 2 | 1 |

---

## 7. 改进建议

1. **[高优先级]** 启用KRaft模式替代ZooKeeper（Kafka 3.5+已稳定）
2. **[中优先级]** 数据盘升级为NVMe SSD，预期吞吐提升30-50%
3. **[中优先级]** 网络升级到25Gbps，满足高吞吐场景
4. **[低优先级]** 开启Tiered Storage，降低长期存储成本

---

## 附录A: 原始实验数据

[附所有原始CSV数据链接或路径]

## 附录B: 监控面板JSON

[附Grafana Dashboard JSON导出]
```

---

## 十二、生产环境4套推荐配置（含OS和JVM调优）

### 12.1 配置总览

```
四套配置定位:

┌──────────────────────────────────────────────────────────────┐
│                        生产配置矩阵                           │
├──────────┬──────────┬──────────┬──────────┬─────────────────┤
│          │ 高吞吐    │ 低延迟    │ 均衡      │ 低成本           │
├──────────┼──────────┼──────────┼──────────┼─────────────────┤
│ 典型场景  │ 日志采集   │ 交易处理   │ 通用业务   │ 开发/测试/归档    │
│ 吞吐目标  │ >500MB/s  │ >100MB/s  │ >300MB/s  │ >200MB/s         │
│ P99延迟   │ <100ms    │ <10ms     │ <50ms     │ <200ms           │
│ 数据可靠性 │ At-Least  │ Exactly   │ At-Least  │ Best-Effort      │
│ 硬件要求   │ 高配       │ 高配       │ 中配       │ 低配              │
│ 成本等级   │ $$$$      │ $$$$      │ $$$       │ $                 │
└──────────┴──────────┴──────────┴──────────┴─────────────────┘
```

### 12.2 配置A：高吞吐配置

```properties
# ============================================================
# 高吞吐配置：适用于日志收集、埋点数据、IoT数据等
# 设计目标: 最大化吞吐量，接受一定延迟和少量数据丢失
# ============================================================

# ========== Broker配置 ==========
# 基础配置
broker.id=0
listeners=PLAINTEXT://0.0.0.0:9092
advertised.listeners=PLAINTEXT://kafka-broker-0:9092
num.network.threads=16
num.io.threads=16

# Socket配置
socket.send.buffer.bytes=2097152
socket.receive.buffer.bytes=2097152
socket.request.max.bytes=209715200

# 日志存储
log.dirs=/data/kafka-logs
num.partitions=15
default.replication.factor=2
log.segment.bytes=1073741824
log.retention.hours=72
log.retention.bytes=-1
log.cleanup.policy=delete
log.flush.interval.messages=100000
log.flush.interval.ms=5000

# 副本管理
num.replica.fetchers=8
replica.fetch.max.bytes=10485760
replica.fetch.wait.max.ms=500
replica.high.watermark.checkpoint.interval.ms=5000
replica.lag.time.max.ms=30000

# ZooKeeper
zookeeper.connect=zk-1:2181,zk-2:2181,zk-3:2181
zookeeper.connection.timeout.ms=18000
zookeeper.session.timeout.ms=18000

# ========== Producer配置 ==========
acks=1
batch.size=524288
linger.ms=20
compression.type=lz4
buffer.memory=268435456
max.request.size=10485760
retries=3
retry.backoff.ms=300
max.in.flight.requests.per.connection=5
request.timeout.ms=60000
delivery.timeout.ms=120000
enable.idempotence=false

# ========== Consumer配置 ==========
fetch.min.bytes=1048576
fetch.max.bytes=104857600
max.partition.fetch.bytes=10485760
max.poll.records=5000
fetch.max.wait.ms=500
heartbeat.interval.ms=3000
session.timeout.ms=45000
max.poll.interval.ms=600000
partition.assignment.strategy=\
  org.apache.kafka.clients.consumer.CooperativeStickyAssignor

# ========== Topic配置 ==========
min.insync.replicas=1
unclean.leader.election.enable=true
segment.bytes=1073741824
compression.type=producer

# ========== JVM配置 (G1GC) ==========
# KAFKA_HEAP_OPTS="-Xms16G -Xmx16G"
# KAFKA_JVM_PERFORMANCE_OPTS="
#   -server
#   -XX:+UseG1GC
#   -XX:MaxGCPauseMillis=50
#   -XX:InitiatingHeapOccupancyPercent=40
#   -XX:G1ReservePercent=15
#   -XX:ParallelGCThreads=16
#   -XX:ConcGCThreads=4
#   -XX:G1HeapRegionSize=32M
#   -XX:+DisableExplicitGC
#   -XX:+AlwaysPreTouch
# "

# ========== OS调优 ==========
# /etc/sysctl.conf:
# vm.swappiness=1
# vm.dirty_background_ratio=5
# vm.dirty_ratio=60
# vm.dirty_expire_centisecs=3000
# net.core.rmem_max=134217728
# net.core.wmem_max=134217728
# net.ipv4.tcp_rmem=4096 87380 134217728
# net.ipv4.tcp_wmem=4096 65536 134217728
# net.ipv4.tcp_max_syn_backlog=8192
# net.core.somaxconn=32768
# net.core.netdev_max_backlog=16384
# net.ipv4.tcp_tw_reuse=1
# net.ipv4.tcp_fin_timeout=15
# net.nodelay=1
# fs.file-max=655360
```

### 12.3 配置B：低延迟配置

```properties
# ============================================================
# 低延迟配置：适用于实时交易、欺诈检测、在线推荐等
# 设计目标: P99延迟<10ms，宁可牺牲吞吐
# ============================================================

# ========== Broker配置 ==========
broker.id=0
listeners=PLAINTEXT://0.0.0.0:9092
num.network.threads=8
num.io.threads=16

# Socket配置 — 小缓冲降低延迟
socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
socket.request.max.bytes=104857600

# 日志存储 — 快速刷新
log.dirs=/data/kafka-logs
num.partitions=6
default.replication.factor=3
log.segment.bytes=268435456
log.retention.hours=24
log.flush.interval.messages=1000
log.flush.interval.ms=100
log.cleaner.threads=2

# 副本管理
num.replica.fetchers=4
replica.fetch.max.bytes=2097152
replica.fetch.wait.max.ms=300
replica.lag.time.max.ms=10000
min.insync.replicas=2

# ========== Producer配置 ==========
acks=1
batch.size=32768
linger.ms=2
compression.type=snappy
buffer.memory=67108864
max.request.size=1048576
retries=1
retry.backoff.ms=50
max.in.flight.requests.per.connection=5
request.timeout.ms=10000
delivery.timeout.ms=30000
enable.idempotence=false

# ========== Consumer配置 ==========
fetch.min.bytes=1
fetch.max.bytes=52428800
max.partition.fetch.bytes=1048576
max.poll.records=100
fetch.max.wait.ms=100
heartbeat.interval.ms=1000
session.timeout.ms=10000
max.poll.interval.ms=300000
partition.assignment.strategy=\
  org.apache.kafka.clients.consumer.CooperativeStickyAssignor

# ========== Topic配置 ==========
min.insync.replicas=2
unclean.leader.election.enable=false
segment.bytes=268435456
compression.type=snappy

# ========== JVM配置 (低延迟GC) ==========
# KAFKA_HEAP_OPTS="-Xms8G -Xmx8G"
# KAFKA_JVM_PERFORMANCE_OPTS="
#   -server
#   -XX:+UseG1GC
#   -XX:MaxGCPauseMillis=10
#   -XX:InitiatingHeapOccupancyPercent=30
#   -XX:G1ReservePercent=20
#   -XX:ParallelGCThreads=8
#   -XX:ConcGCThreads=2
#   -XX:G1HeapRegionSize=8M
#   -XX:+DisableExplicitGC
#   -XX:+AlwaysPreTouch
#   -XX:+UseNUMA
#   -XX:+UseTransparentHugePages
# "

# ========== OS调优 ==========
# /etc/sysctl.conf:
# vm.swappiness=1
# vm.dirty_background_ratio=3
# vm.dirty_ratio=20
# vm.dirty_expire_centisecs=500
# net.core.rmem_default=262144
# net.core.wmem_default=262144
# net.core.rmem_max=16777216
# net.core.wmem_max=16777216
# net.ipv4.tcp_rmem=4096 87380 16777216
# net.ipv4.tcp_wmem=4096 65536 16777216
# net.ipv4.tcp_low_latency=1
# net.core.busy_read=50
# net.core.busy_poll=50
# fs.file-max=655360
```

### 12.4 配置C：均衡配置（推荐大多数场景）

```properties
# ============================================================
# 均衡配置：适用于通用ETL、实时数仓同步、数据管道等
# 设计目标: 吞吐和延迟的帕累托最优平衡点
# ============================================================

# ========== Broker配置 ==========
broker.id=0
listeners=PLAINTEXT://0.0.0.0:9092
num.network.threads=12
num.io.threads=12

# Socket配置
socket.send.buffer.bytes=1048576
socket.receive.buffer.bytes=1048576
socket.request.max.bytes=104857600

# 日志存储
log.dirs=/data/kafka-logs
num.partitions=10
default.replication.factor=3
log.segment.bytes=536870912
log.retention.hours=168
log.retention.bytes=-1
log.cleanup.policy=delete
log.retention.check.interval.ms=300000
log.flush.interval.messages=10000
log.flush.interval.ms=1000

# 副本管理
num.replica.fetchers=6
replica.fetch.max.bytes=5242880
replica.fetch.wait.max.ms=500
replica.lag.time.max.ms=30000
min.insync.replicas=2

# ZooKeeper
zookeeper.connect=zk-1:2181,zk-2:2181,zk-3:2181
zookeeper.connection.timeout.ms=18000

# ========== Producer配置 ==========
acks=1
batch.size=131072
linger.ms=5
compression.type=lz4
buffer.memory=67108864
max.request.size=5242880
retries=3
retry.backoff.ms=100
max.in.flight.requests.per.connection=5
request.timeout.ms=30000
delivery.timeout.ms=120000
enable.idempotence=false

# ========== Consumer配置 ==========
fetch.min.bytes=10240
fetch.max.bytes=52428800
max.partition.fetch.bytes=5242880
max.poll.records=500
fetch.max.wait.ms=500
heartbeat.interval.ms=3000
session.timeout.ms=45000
max.poll.interval.ms=300000
enable.auto.commit=false
auto.offset.reset=earliest
partition.assignment.strategy=\
  org.apache.kafka.clients.consumer.CooperativeStickyAssignor

# ========== Topic配置 ==========
min.insync.replicas=2
unclean.leader.election.enable=false
segment.bytes=536870912
compression.type=producer
retention.ms=604800000

# ========== JVM配置 (均衡GC) ==========
# KAFKA_HEAP_OPTS="-Xms10G -Xmx10G"
# KAFKA_JVM_PERFORMANCE_OPTS="
#   -server
#   -XX:+UseG1GC
#   -XX:MaxGCPauseMillis=20
#   -XX:InitiatingHeapOccupancyPercent=35
#   -XX:G1ReservePercent=15
#   -XX:ParallelGCThreads=12
#   -XX:ConcGCThreads=3
#   -XX:G1HeapRegionSize=16M
#   -XX:+DisableExplicitGC
#   -XX:+AlwaysPreTouch
#   -XX:G1MixedGCLiveThresholdPercent=85
#   -XX:+ParallelRefProcEnabled
# "

# ========== OS调优 ==========
# /etc/sysctl.conf:
# vm.swappiness=1
# vm.dirty_background_ratio=5
# vm.dirty_ratio=60
# vm.dirty_expire_centisecs=3000
# net.core.rmem_max=67108864
# net.core.wmem_max=67108864
# net.ipv4.tcp_rmem=4096 87380 67108864
# net.ipv4.tcp_wmem=4096 65536 67108864
# net.ipv4.tcp_max_syn_backlog=4096
# net.core.somaxconn=16384
# net.core.netdev_max_backlog=8192
# net.ipv4.tcp_tw_reuse=1
# fs.file-max=655360
# fs.aio-max-nr=1048576
```

### 12.5 配置D：低成本配置

```properties
# ============================================================
# 低成本配置：适用于开发/测试环境、归档数据存储等
# 设计目标: 资源使用最小化，接受较低的性能和可靠性
# ============================================================

# ========== Broker配置 ==========
broker.id=0
listeners=PLAINTEXT://0.0.0.0:9092
num.network.threads=4
num.io.threads=4

# Socket配置
socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
socket.request.max.bytes=104857600

# 日志存储
log.dirs=/data/kafka-logs
num.partitions=8
default.replication.factor=2
log.segment.bytes=536870912
log.retention.hours=48
log.cleanup.policy=delete
log.flush.interval.messages=9223372036854775807
log.flush.interval.ms=9223372036854775807

# 副本管理 (最小化)
num.replica.fetchers=2
replica.fetch.max.bytes=2097152
replica.fetch.wait.max.ms=500
replica.lag.time.max.ms=30000
min.insync.replicas=1

# ========== Producer配置 ==========
acks=0
batch.size=262144
linger.ms=10
compression.type=lz4
buffer.memory=33554432
retries=0
max.in.flight.requests.per.connection=5
request.timeout.ms=30000
delivery.timeout.ms=60000
enable.idempotence=false

# ========== Consumer配置 ==========
fetch.min.bytes=1
fetch.max.bytes=52428800
max.partition.fetch.bytes=5242880
max.poll.records=500
fetch.max.wait.ms=500
heartbeat.interval.ms=3000
session.timeout.ms=30000
enable.auto.commit=true
auto.commit.interval.ms=5000

# ========== Topic配置 ==========
min.insync.replicas=1
unclean.leader.election.enable=true
segment.bytes=536870912

# ========== JVM配置 (最小内存) ==========
# KAFKA_HEAP_OPTS="-Xms2G -Xmx2G"
# KAFKA_JVM_PERFORMANCE_OPTS="
#   -server
#   -XX:+UseG1GC
#   -XX:MaxGCPauseMillis=200
#   -XX:InitiatingHeapOccupancyPercent=45
#   -XX:G1HeapRegionSize=4M
#   -XX:+DisableExplicitGC
# "

# ========== OS调优 ==========
# /etc/sysctl.conf:
# vm.swappiness=10
# fs.file-max=131072
# net.core.rmem_max=16777216
# net.core.wmem_max=16777216
```

### 12.6 配置选择决策树

```
开始选择配置
│
├─ 数据是否绝对不能丢失？
│   ├─ 是 → 使用"高可靠"变体 (基于均衡配置，修改 acks=all, min.insync.replicas=3)
│   └─ 否 → 继续
│
├─ P99延迟要求 < 10ms？
│   ├─ 是 → 配置B: 低延迟
│   └─ 否 → 继续
│
├─ 吞吐量要求 > 500MB/s？
│   ├─ 是 → 配置A: 高吞吐
│   └─ 否 → 继续
│
├─ 预算是首要考虑？
│   ├─ 是 → 配置D: 低成本
│   └─ 否 → 配置C: 均衡
│
└─ 生产环境 90% 场景 → 配置C: 均衡
   特殊场景再由A/B/D微调
```

### 12.7 配置变更Checklist

```markdown
# Kafka配置变更Checklist

## 变更前
- [ ] 在测试环境验证新配置
- [ ] 记录当前所有配置 (备份 server.properties)
- [ ] 确认变更窗口 (建议低峰期)
- [ ] 通知下游消费者团队
- [ ] 准备回滚方案 (备份配置文件)

## 变更中
- [ ] 逐台Broker滚动重启 (非同时重启)
- [ ] 每台Broker重启后等待ISR恢复正常再下一台
- [ ] 观察关键指标:
  - UnderReplicatedPartitions = 0
  - ActiveControllerCount = 1
  - OfflinePartitionsCount = 0
- [ ] 监控Producer/Consumer错误率

## 变更后
- [ ] 运行压测验证性能变化 (对比变更前后)
- [ ] 检查Consumer Lag是否正常
- [ ] 观察至少30分钟确保稳定
- [ ] 更新运维文档
- [ ] 通知相关团队变更完成
```