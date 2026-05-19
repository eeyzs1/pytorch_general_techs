# L2 Kafka / Flink / ClickHouse 命令行速查卡

> **所属阶段**：L2 中级工程师 | 快速参考 | 持续更新

---

## 一、Kafka 常用命令速查

### 1.1 Topic 管理

```bash
# 创建Topic
kafka-topics.sh --bootstrap-server localhost:9092 \
  --create --topic my-topic \
  --partitions 6 --replication-factor 3 \
  --config retention.ms=604800000 \
  --config max.message.bytes=1048576 \
  --config min.insync.replicas=2

# 实例说明:
#   partitions=6: 6个分区，支持最多6个Consumer并行消费
#   replication-factor=3: 3副本，容忍2台Broker宕机
#   retention.ms=604800000: 保留7天 (7×24×3600×1000)
#   max.message.bytes=1048576: 单条消息最大1MB
#   min.insync.replicas=2: 最少2个ISR确认后才返回成功

# 查看所有Topic列表
kafka-topics.sh --bootstrap-server localhost:9092 --list

# 查看单个Topic详情
kafka-topics.sh --bootstrap-server localhost:9092 \
  --describe --topic my-topic

# 输出示例:
# Topic: my-topic  PartitionCount: 6  ReplicationFactor: 3  Configs: ...
#   Topic: my-topic  Partition: 0  Leader: 1  Replicas: 1,2,3  Isr: 1,2,3
#   Topic: my-topic  Partition: 1  Leader: 2  Replicas: 2,3,1  Isr: 2,3,1
# ...
# 解读:
#   Leader: 1  → 此分区的Leader在Broker 1上
#   Replicas: 1,2,3 → 该分区的副本分布在Broker 1,2,3
#   Isr: 1,2,3 → 所有副本保持同步（正常）
#   Isr: 1,2 → Broker 3掉线了（异常）

# 修改Topic配置（动态修改，无需重启）
kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type topics --entity-name my-topic \
  --alter --add-config retention.ms=259200000

# 增加Partition数（只能增加，不能减少！）
kafka-topics.sh --bootstrap-server localhost:9092 \
  --alter --topic my-topic --partitions 12

# 删除Topic
kafka-topics.sh --bootstrap-server localhost:9092 \
  --delete --topic my-topic

# 查看Topic消息总数（所有Partition的最新Offset之和）
kafka-run-class.sh kafka.tools.GetOffsetShell \
  --broker-list localhost:9092 --topic my-topic --time -1

# 查看Topic的最早Offset
kafka-run-class.sh kafka.tools.GetOffsetShell \
  --broker-list localhost:9092 --topic my-topic --time -2

# 导出Topic数据到文件（可用于备份/迁移）
kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic my-topic --from-beginning --timeout-ms 10000 \
  > /backup/my-topic-dump.txt

# 查看Topic的分区Leader分布均衡性
kafka-topics.sh --bootstrap-server localhost:9092 \
  --describe --topic my-topic | awk '{print $3}' | sort | uniq -c
```

### 1.2 Producer / Consumer 测试工具

```bash
# ============ Producer 性能测试 ============

# 基本压测（无限吞吐模式）
kafka-producer-perf-test.sh \
  --topic perf-test \
  --num-records 10000000 \
  --record-size 1024 \
  --throughput -1 \
  --producer-props bootstrap.servers=localhost:9092 \
    acks=1 batch.size=65536 linger.ms=5 compression.type=lz4

# 输出示例解读:
# 10000000 records sent, 320456.7 records/sec (313.2 MB/sec),
#   8.5 ms avg latency, 42.3 ms max latency,
#   5 ms 50th, 18 ms 95th, 35 ms 99th, 40 ms 99.9th.
# 解读:
#   records/sec=320456.7: Producer吞吐量 ~32万条/秒
#   MB/sec=313.2: 约313 MB/s的写入带宽
#   avg latency=8.5ms: 平均延迟8.5毫秒
#   P99=35ms: 99%的消息在35ms内确认

# 控制发送速率（每秒10万条）
kafka-producer-perf-test.sh \
  --topic perf-test \
  --num-records 5000000 \
  --record-size 512 \
  --throughput 100000 \
  --producer-props bootstrap.servers=localhost:9092 acks=1

# 同时测试多种压缩算法
for comp in none gzip snappy lz4 zstd; do
  echo "=== compression=$comp ==="
  kafka-producer-perf-test.sh \
    --topic perf-$comp \
    --num-records 2000000 \
    --record-size 1024 \
    --throughput -1 \
    --producer-props bootstrap.servers=localhost:9092 \
      compression.type=$comp acks=1 2>&1 | grep "records/sec"
done

# 测试不同消息大小的性能
for size in 100 512 1024 5120 10240; do
  echo "=== record-size=$size ==="
  kafka-producer-perf-test.sh \
    --topic perf-size \
    --num-records 2000000 \
    --record-size $size \
    --throughput -1 \
    --producer-props bootstrap.servers=localhost:9092 acks=1 \
    2>&1 | grep -E "records/sec|MB/sec"
done

# ============ Consumer 性能测试 ============

# 基本消费速度测试
kafka-consumer-perf-test.sh \
  --topic perf-test \
  --bootstrap-server localhost:9092 \
  --messages 10000000 \
  --group perf-group \
  --threads 3 \
  --hide-header

# 输出示例:
# 2024-01-15 10:00:00, 2024-01-15 10:02:00, 8192.0000,
#   68.2667, 8000000, 66666.6667, 3450, 116550, 70.3087, 68653.8461
# 解读:
#   第3列 8192.0000 = 消费数据量(MB)
#   第4列 68.2667 = MB/sec
#   第5列 8000000 = 消费消息数
#   第6列 66666.6667 = 消息/秒 (nMsg.sec)

# 不同fetch.min.bytes对比
for fb in 1 10240 102400 1048576; do
  echo "=== fetch.min.bytes=$fb ==="
  kafka-consumer-perf-test.sh \
    --topic perf-test \
    --bootstrap-server localhost:9092 \
    --messages 1000000 \
    --group "group-fb-$fb" \
    --consumer-props fetch.min.bytes=$fb \
    --hide-header 2>&1 | tail -1
done

# ============ Console操作 ============

# Console Producer（交互式发送消息）
kafka-console-producer.sh --bootstrap-server localhost:9092 \
  --topic my-topic \
  --property "parse.key=true" \
  --property "key.separator=:"

# 示例输入:
# key1:{"name":"张三","age":25}
# key2:{"name":"李四","age":30}
# (Ctrl+C 退出)

# Console Consumer（查看Topic数据）
kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic my-topic --from-beginning \
  --property print.key=true \
  --property print.value=true \
  --property print.partition=true \
  --property print.offset=true \
  --property print.timestamp=true

# 按时间戳消费（从指定时间开始）
kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic my-topic \
  --property print.timestamp=true \
  --offset $(kafka-run-class.sh kafka.tools.GetOffsetShell \
    --broker-list localhost:9092 --topic my-topic \
    --time $(date -d "2024-01-15 10:00:00" +%s)000 | head -1 | cut -d: -f3)

# 消费最新N条消息
kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic my-topic --max-messages 100
```

### 1.3 Consumer Group 管理

```bash
# 查看所有Consumer Group
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list

# 查看Group详情（含Lag）
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group --describe

# 输出示例解读:
# GROUP    TOPIC    PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG  CONSUMER-ID    HOST        CLIENT-ID
# my-group my-topic 0          1523000         1524500         1500 consumer-1-xxx /192.168.1.1 consumer-1
# my-group my-topic 1          1500100         1524500         24400 consumer-2-yyy /192.168.1.2 consumer-2
# 解读:
#   CURRENT-OFFSET: Consumer已消费到的位置
#   LOG-END-OFFSET: 分区的当前最新位置
#   LAG = LOG-END-OFFSET - CURRENT-OFFSET: 消费延迟量
#   LAG=24400 表示Consumer落后了24400条消息

# 按Lag大小排序查看（找出积压最大的分区）
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group --describe 2>/dev/null | \
  awk 'NR>1 {print $6,$0}' | sort -rn | head -10

# 重置Offset（重置到最新位置，放弃积压消息）
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group --topic my-topic \
  --reset-offsets --to-latest --execute

# 重置Offset（重置到最早位置，重新消费）
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group --topic my-topic \
  --reset-offsets --to-earliest --execute

# 重置Offset到指定时间
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group --topic my-topic \
  --reset-offsets --to-datetime 2024-01-15T10:00:00.000 --execute

# 重置Offset到指定位置（按Partition分别指定）
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group --topic my-topic:0,1,2 \
  --reset-offsets --to-offset 1000000 --execute

# 按偏移量减少重置（往前回退1000条，重新消费）
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group --topic my-topic \
  --reset-offsets --shift-by -1000 --execute

# 按偏移量增加重置（往前跳过1000条）
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group --topic my-topic \
  --reset-offsets --shift-by 1000 --execute

# 删除Consumer Group
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group --delete

# 查看Group成员信息
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group --describe --members

# 查看Group状态
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group --describe --state

# 持续监控Lag（每2秒刷新）
watch -n 2 "kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group --describe 2>/dev/null"
```

### 1.4 Offset 管理

```bash
# 获取指定时间戳对应的Offset（用于回放特定时间之后的数据）
kafka-run-class.sh kafka.tools.GetOffsetShell \
  --broker-list localhost:9092 \
  --topic my-topic \
  --time 1705300000000 \
  --offsets 1

# 输出示例:
# my-topic:0:1523000
# my-topic:1:1500100
# my-topic:2:1485000
# 解读: 时间戳1705300000000之后，各分区的第一条消息Offset

# 获取最新Offset（end offset）
kafka-run-class.sh kafka.tools.GetOffsetShell \
  --broker-list localhost:9092 --topic my-topic --time -1

# 获取最早Offset（beginning offset）
kafka-run-class.sh kafka.tools.GetOffsetShell \
  --broker-list localhost:9092 --topic my-topic --time -2

# 统计Topic总消息数（各分区end offset - beginning offset之和）
TOTAL=0
for p_offset in $(kafka-run-class.sh kafka.tools.GetOffsetShell \
    --broker-list localhost:9092 --topic my-topic --time -1 | cut -d: -f3); do
  TOTAL=$((TOTAL + p_offset))
done
echo "Topic my-topic 总消息数: $TOTAL"

# 导出Offset到文件（用于灾备恢复）
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group --describe 2>/dev/null | tail -n +2 | \
  awk '{print $2","$3","$4}' > /backup/offsets_my-group_$(date +%Y%m%d).csv

# 导入Offset（使用之前保存的Offset文件恢复）
# 先dry-run预览
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group --topic my-topic:0,1,2 \
  --reset-offsets --to-offset 1523000 --dry-run

# 再execute执行
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group --topic my-topic:0,1,2 \
  --reset-offsets --to-offset 1523000 --execute
```

### 1.5 ACL 管理（安全相关）

```bash
# 创建ACL：允许User:alice对Topic:my-topic有读写权限
kafka-acls.sh --bootstrap-server localhost:9092 \
  --add --allow-principal User:alice \
  --operation Read --operation Write \
  --topic my-topic

# 创建ACL：允许Group:analytics-group消费
kafka-acls.sh --bootstrap-server localhost:9092 \
  --add --allow-principal User:alice \
  --operation Read --group analytics-group

# 查看所有ACL
kafka-acls.sh --bootstrap-server localhost:9092 --list

# 查看特定Topic的ACL
kafka-acls.sh --bootstrap-server localhost:9092 \
  --list --topic my-topic

# 删除ACL
kafka-acls.sh --bootstrap-server localhost:9092 \
  --remove --allow-principal User:alice \
  --operation Read --topic my-topic

# 批量删除某用户的所有ACL（使用 --force 跳过确认）
kafka-acls.sh --bootstrap-server localhost:9092 \
  --remove --allow-principal User:alice --force

# 创建Producer权限（包含对TransactionId的写权限）
kafka-acls.sh --bootstrap-server localhost:9092 \
  --add --allow-principal User:producer-app \
  --producer --topic my-topic

# 创建Consumer权限
kafka-acls.sh --bootstrap-server localhost:9092 \
  --add --allow-principal User:consumer-app \
  --consumer --topic my-topic --group analytics-group
```

### 1.6 配置查看与管理

```bash
# 查看所有Broker配置（动态配置）
kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type brokers --entity-default --describe

# 查看特定Broker配置
kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type brokers --entity-name 1 --describe

# 查看Topic的动态配置
kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type topics --entity-name my-topic --describe

# 动态修改Broker配置（无需重启）
kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type brokers --entity-name 1 \
  --alter --add-config log.retention.hours=48

# 修改Topic的消息保留时间
kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type topics --entity-name my-topic \
  --alter --add-config retention.ms=86400000

# 删除Topic的某个自定义配置（恢复默认）
kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type topics --entity-name my-topic \
  --alter --delete-config retention.ms

# 查看所有用户的配额（Quota）
kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type users --describe

# 设置用户配额（限制Producer吞吐量 10MB/s）
kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type users --entity-name producer-app \
  --alter --add-config producer_byte_rate=10485760

# 设置Client ID配额
kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type clients --entity-name my-client \
  --alter --add-config consumer_byte_rate=52428800

# 删除配额
kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type users --entity-name producer-app \
  --alter --delete-config producer_byte_rate
```

### 1.7 集群管理与元数据

```bash
# 查看Broker版本
kafka-broker-api-versions.sh --bootstrap-server localhost:9092 | head -5

# 查看Controller状态
kafka-metadata-quorum.sh --bootstrap-server localhost:9092 describe --status

# 查看分区Leader分布（判断负载是否均衡）
kafka-topics.sh --bootstrap-server localhost:9092 --describe | \
  grep "Leader:" | awk '{print $3}' | sort | uniq -c | sort -rn

# 重新选举Preferred Leader（恢复Leader均衡）
kafka-leader-election.sh --bootstrap-server localhost:9092 \
  --election-type PREFERRED --topic my-topic --partition 0

# 对所有Topic的所有Partition执行Preferred Leader选举
kafka-leader-election.sh --bootstrap-server localhost:9092 \
  --election-type PREFERRED --all-topic-partitions

# 重新分配分区（数据迁移）
# 1. 生成迁移计划JSON
kafka-reassign-partitions.sh --bootstrap-server localhost:9092 \
  --topics-to-move-json-file topics-to-move.json \
  --broker-list "1,2,3,4" --generate

# 2. 执行迁移
kafka-reassign-partitions.sh --bootstrap-server localhost:9092 \
  --reassignment-json-file reassignment.json --execute

# 3. 查看迁移进度
kafka-reassign-partitions.sh --bootstrap-server localhost:9092 \
  --reassignment-json-file reassignment.json --verify

# 查看未复制的分区（潜在风险）
kafka-topics.sh --bootstrap-server localhost:9092 --describe --under-replicated-partitions

# 查看没有Leader的分区（严重故障）
kafka-topics.sh --bootstrap-server localhost:9092 --describe --unavailable-partitions

# 查看日志目录详细信息
kafka-log-dirs.sh --bootstrap-server localhost:9092 \
  --describe --broker-list 1,2,3

# 查看每个Topic的磁盘使用量
kafka-log-dirs.sh --bootstrap-server localhost:9092 \
  --describe --broker-list 1,2,3 --topic-list my-topic
```

### 1.8 日志段（Segment）管理

```bash
# 查看日志段文件（需要SSH到Broker节点）
ls -lh /var/lib/kafka/data/my-topic-0/
# 输出示例:
# 00000000000000000000.log   (日志数据文件, 1GB)
# 00000000000000000000.index (偏移索引文件, 10MB)
# 00000000000000000000.timeindex (时间戳索引文件, 12MB)
# 0000000000015230000.log   (下一个日志段)
# 0000000000015230000.index
# 0000000000015230000.timeindex
# leader-epoch-checkpoint

# 手动触发日志段滚动（闭合当前Segment，创建新Segment）
kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type topics --entity-name my-topic \
  --alter --add-config segment.bytes=104857600

# 查看Log Cleaner状态
kafka-log-dirs.sh --bootstrap-server localhost:9092 \
  --describe --broker-list 1

# Dump日志段内容（查看二进制日志内容）
kafka-run-class.sh kafka.tools.DumpLogSegments \
  --files /var/lib/kafka/data/my-topic-0/00000000000000000000.log \
  --print-data-log

# Dump索引文件内容
kafka-run-class.sh kafka.tools.DumpLogSegments \
  --files /var/lib/kafka/data/my-topic-0/00000000000000000000.index
```

---

## 二、Flink 常用命令速查

### 2.1 集群管理

```bash
# 启动Flink集群
./bin/start-cluster.sh

# 停止Flink集群
./bin/stop-cluster.sh

# 启动JobManager
./bin/jobmanager.sh start

# 启动TaskManager
./bin/taskmanager.sh start

# 查看集群状态
flink list

# 查看所有运行中的Job
flink list -r

# 查看所有已完成/失败的Job
flink list -s          # 所有已调度的Job
flink list -a          # 所有Job（运行+已完成+失败）

# 查看Job详情
flink info -c com.example.MyJob my-job.jar
# 输出: Job执行计划、并行度、State Backend等信息

# 查看集群资源配置
curl http://localhost:8081/overview
# 输出示例:
# {"taskmanagers":3,"slots-total":24,"slots-available":18,"jobs-running":2,...}
# 解读: 3个TM, 共24个Slot, 18个空闲, 2个Job在运行

# 查看各TaskManager详情
curl http://localhost:8081/taskmanagers/
```

### 2.2 任务提交与管理

```bash
# ============ 任务提交 ============

# 基本提交（前台运行，日志直接输出到终端）
flink run my-job.jar

# 后台运行（detached模式，返回JobID）
flink run -d my-job.jar

# 指定Job类名（JAR中有多个main class时）
flink run -c com.example.MyJob my-job.jar

# 指定并行度
flink run -p 8 my-job.jar

# 带参数提交（传入main方法args）
flink run my-job.jar --kafka-brokers localhost:9092 --topic input-topic

# 从Savepoint恢复
flink run -s hdfs://namenode:9000/flink/savepoints/savepoint-xxx-xxx \
  -c com.example.MyJob my-job.jar

# 从Savepoint恢复但忽略状态（-n = --allowNonRestoredState）
flink run -s hdfs://namenode:9000/flink/savepoints/savepoint-xxx-xxx \
  -n my-job.jar

# 从Checkpoint恢复
flink run -s hdfs://namenode:9000/flink/checkpoints/xxx/chk-100 \
  -c com.example.MyJob my-job.jar

# 提交Python Flink Job
flink run -py my_job.py

# Python Job带依赖
flink run -py my_job.py -pyfs dependency.zip

# ============ 任务取消 ============

# 取消Job（默认会创建Savepoint）
flink cancel <jobId>

# 取消Job并保留Savepoint
flink stop --savepointPath hdfs://namenode:9000/flink/savepoints <jobId>

# 强制取消（不创建Savepoint，不等待）
flink cancel --withSavepoint hdfs://namenode:9000/flink/savepoints <jobId>
# 如果超时未完成Savepoint，加 --force 强制取消

# ============ Savepoint/Checkpoint操作 ============

# 手动触发Savepoint
flink savepoint <jobId> hdfs://namenode:9000/flink/savepoints

# 触发Savepoint并停止Job
flink stop --savepointPath hdfs://namenode:9000/flink/savepoints <jobId>

# 放弃（删除）Savepoint
flink savepoint -d hdfs://namenode:9000/flink/savepoints/savepoint-xxx-xxx

# 列出所有Savepoint
hdfs dfs -ls hdfs://namenode:9000/flink/savepoints/

# 查看Checkpoint历史（通过REST API）
curl http://localhost:8081/jobs/<jobId>/checkpoints
```

### 2.3 日志查看

```bash
# 查看JobManager日志
tail -f /opt/flink/log/flink-*-standalonesession-*.log

# 查看TaskManager日志
tail -f /opt/flink/log/flink-*-taskexecutor-*.log

# 查看Job运行日志（Flink 1.15+ 历史日志服务）
curl http://localhost:8081/jobs/<jobId>/exceptions

# 查看特定日志级别
# 在 Flink Web UI → Job → TaskManagers → Logs 中查看

# 动态修改日志级别（无需重启，Flink 1.17+）
curl -X PUT http://localhost:8081/jobmanager/log \
  -H "Content-Type: application/json" \
  -d '{"loggerName":"org.apache.flink.runtime.checkpoint","level":"DEBUG"}'

# 搜索Checkpoint相关日志
grep -i "checkpoint" /opt/flink/log/flink-*-taskexecutor-*.log | tail -100

# 搜索反压相关日志
grep -i "backpressur" /opt/flink/log/flink-*-taskexecutor-*.log | tail -50
```

### 2.4 Flink SQL 客户端

```bash
# 启动SQL Client（嵌入式模式）
./bin/sql-client.sh

# 启动SQL Client（Gateway模式，连接远程集群）
./bin/sql-client.sh -d /opt/flink/conf/sql-client-config.yaml

# SQL Client常用命令（在SQL Client内部执行）
# 查看所有表
SHOW TABLES;

# 查看表结构
DESCRIBE my_table;
DESC my_table;

# 查看函数
SHOW FUNCTIONS;

# 查看Catalog
SHOW CATALOGS;
SHOW CURRENT CATALOG;
USE CATALOG my_catalog;

# 查看数据库
SHOW DATABASES;
SHOW CURRENT DATABASE;
USE my_database;

# 查看正在运行的Job
SHOW JOBS;

# 执行SQL文件
./bin/sql-client.sh -f my-script.sql

# 设置执行模式（流/批）
SET 'execution.runtime-mode' = 'streaming';
SET 'execution.runtime-mode' = 'batch';

# 设置Checkpoint
SET 'execution.checkpointing.interval' = '60s';
SET 'execution.checkpointing.mode' = 'EXACTLY_ONCE';
SET 'state.backend' = 'rocksdb';
SET 'state.backend.incremental' = 'true';

# 设置并行度
SET 'parallelism.default' = '8';

# 创建Kafka Source表
CREATE TABLE kafka_source (
  user_id STRING,
  event_type STRING,
  event_time TIMESTAMP(3),
  WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
) WITH (
  'connector' = 'kafka',
  'topic' = 'user-events',
  'properties.bootstrap.servers' = 'localhost:9092',
  'properties.group.id' = 'flink-sql-consumer',
  'scan.startup.mode' = 'latest-offset',
  'format' = 'json'
);

# 创建ClickHouse Sink表
CREATE TABLE ch_sink (
  window_start TIMESTAMP(3),
  window_end TIMESTAMP(3),
  event_type STRING,
  cnt BIGINT
) WITH (
  'connector' = 'clickhouse',
  'url' = 'clickhouse://localhost:8123',
  'database-name' = 'analytics',
  'table-name' = 'event_stats',
  'format' = 'json'
);

# 流式聚合（SQL Client中执行）
INSERT INTO ch_sink
SELECT
  TUMBLE_START(event_time, INTERVAL '1' MINUTE) AS window_start,
  TUMBLE_END(event_time, INTERVAL '1' MINUTE) AS window_end,
  event_type,
  COUNT(*) AS cnt
FROM kafka_source
GROUP BY
  TUMBLE(event_time, INTERVAL '1' MINUTE),
  event_type;

# 退出SQL Client
quit;
```

### 2.5 YARN模式命令

```bash
# 启动YARN Session（长会话模式）
./bin/yarn-session.sh -n 4 -jm 2048m -tm 4096m -d
# -n 4: 4个TaskManager
# -jm 2048m: JobManager内存2GB
# -tm 4096m: 每个TaskManager内存4GB
# -d: detached模式

# 提交到YARN Session
flink run -t yarn-session -Dyarn.application.id=<appId> my-job.jar

# Per-Job模式提交（每个Job独立YARN应用）
flink run -t yarn-per-job -c com.example.MyJob my-job.jar

# Application模式（推荐，Flink 1.11+）
flink run-application -t yarn-application -c com.example.MyJob my-job.jar

# 查看YARN上的Flink应用
yarn application -list

# Kill YARN上的Flink应用
yarn application -kill <appId>
```

---

## 三、Kafka JVM 调优参数速查

### 3.1 GC 配置

```bash
# ============ 推荐GC: G1GC (Kafka 2.5+) ============
# $KAFKA_HOME/bin/kafka-server-start.sh 中设置

export KAFKA_HEAP_OPTS="-Xmx6g -Xms6g \
  -XX:+UseG1GC \
  -XX:MaxGCPauseMillis=20 \
  -XX:InitiatingHeapOccupancyPercent=35 \
  -XX:+DisableExplicitGC \
  -XX:G1HeapRegionSize=16m \
  -XX:MinMetaspaceFreeRatio=50 \
  -XX:MaxMetaspaceFreeRatio=80 \
  -XX:+ParallelRefProcEnabled"

# 参数详解:
# -Xmx6g -Xms6g: 堆大小6GB（生产建议：PageCache用剩余内存）
# MaxGCPauseMillis=20: GC最大暂停目标20ms
# InitiatingHeapOccupancyPercent=35: 堆使用35%启动并发标记周期
# G1HeapRegionSize=16m: G1 Region大小16MB（堆<32GB时推荐）
# DisableExplicitGC: 禁用System.gc()调用
# ParallelRefProcEnabled: 并行处理引用对象

# ============ GC日志配置 ============
export KAFKA_GC_LOG_OPTS="-Xlog:gc*:file=/var/log/kafka/gc.log:time,tags:filecount=10,filesize=100M"

# 分析GC日志
# 统计GC频率
grep "GC(" /var/log/kafka/gc.log | wc -l
# 统计Full GC次数
grep "Full GC" /var/log/kafka/gc.log | wc -l
# 统计GC耗时
grep "GC(" /var/log/kafka/gc.log | grep -oP '\d+\.\d+ms' | \
  awk '{sum+=$1; count++} END {print "Avg:", sum/count, "ms, Total:", sum, "ms"}'
```

### 3.2 Heap 配置

```bash
# ============ 堆大小建议 ============
# 原则: Brokers的堆内存 + Page Cache < 总内存 - OS开销(1-2GB)
#
# 16GB 物理内存 → 堆: 5-6GB, Page Cache: 8-10GB
# 32GB 物理内存 → 堆: 6-8GB, Page Cache: 22-24GB
# 64GB 物理内存 → 堆: 6-8GB, Page Cache: 54-56GB
#
# Kafka不需要很大堆内存！优先留给Page Cache做磁盘缓存

# 开启JMX监控
export KAFKA_JMX_OPTS="-Dcom.sun.management.jmxremote \
  -Dcom.sun.management.jmxremote.port=9999 \
  -Dcom.sun.management.jmxremote.authenticate=false \
  -Dcom.sun.management.jmxremote.ssl=false"

# Direct Memory配置（网络缓冲区）
# 在KAFKA_OPTS中设置:
export KAFKA_OPTS="-XX:MaxDirectMemorySize=1g \
  -Djava.net.preferIPv4Stack=true"
```

### 3.3 OS 调优

```bash
# ============ 文件描述符 ============
# /etc/security/limits.conf
# kafka  soft  nofile  100000
# kafka  hard  nofile  200000
ulimit -n 100000

# ============ 虚拟内存 ============
# /etc/sysctl.conf
# vm.swappiness=1           # 尽量少使用swap（Kafka依赖PageCache）
# vm.dirty_ratio=40         # 脏页比例达到40%才强制刷盘
# vm.dirty_background_ratio=5  # 脏页比例5%时开始后台刷盘
# net.core.wmem_default=1048576  # 默认写缓冲区1MB
# net.core.rmem_default=1048576  # 默认读缓冲区1MB

# 使配置生效
sysctl -p

# ============ 磁盘调度器 ============
# SSD使用noop/deadline，HDD使用deadline
# 查看当前调度器
cat /sys/block/sda/queue/scheduler
# 设置为deadline
echo deadline > /sys/block/sda/queue/scheduler

# ============ 关闭atime（减少磁盘写操作）============
# /etc/fstab
# /dev/sda1 /var/lib/kafka ext4 defaults,noatime,nodiratime 0 0
mount -o remount,noatime,nodiratime /var/lib/kafka
```

---

## 四、Flink Checkpoint 调优参数速查

### 4.1 关键参数矩阵

```bash
# ============ Java代码配置 ============
# Checkpoint基础配置
env.enableCheckpointing(60000);                    # 间隔60秒
env.getCheckpointConfig().setCheckpointTimeout(600000);   # 超时10分钟
env.getCheckpointConfig().setMinPauseBetweenCheckpoints(30000); # 最小间隔30秒
env.getCheckpointConfig().setMaxConcurrentCheckpoints(1);     # 最多1个并发
env.getCheckpointConfig().setTolerableCheckpointFailureNumber(3); # 容忍3次失败

# 非对齐Checkpoint
env.getCheckpointConfig().enableUnalignedCheckpoints();

# 外部化Checkpoint（Job取消后保留）
env.getCheckpointConfig().setExternalizedCheckpointCleanup(
    CheckpointConfig.ExternalizedCheckpointCleanup.RETAIN_ON_CANCELLATION);

# ============ Flink SQL SET配置 ============
# 通过 SET 语句在 SQL 客户端中设置
SET 'execution.checkpointing.interval' = '60s';
SET 'execution.checkpointing.timeout' = '10min';
SET 'execution.checkpointing.min-pause' = '30s';
SET 'execution.checkpointing.max-concurrent-checkpoints' = '1';
SET 'execution.checkpointing.mode' = 'EXACTLY_ONCE';
SET 'execution.checkpointing.externalized-checkpoint-retention' = 'RETAIN_ON_CANCELLATION';
SET 'execution.checkpointing.unaligned' = 'false';    # 是否开启非对齐
SET 'execution.checkpointing.alignment-timeout' = '0s'; # 对齐超时（0=无限等待）

# ============ flink-conf.yaml 全局配置 ============
# $FLINK_HOME/conf/flink-conf.yaml
execution.checkpointing.interval: 60s
execution.checkpointing.timeout: 10min
execution.checkpointing.min-pause: 30s
execution.checkpointing.max-concurrent-checkpoints: 1
execution.checkpointing.mode: EXACTLY_ONCE
state.backend: rocksdb
state.backend.incremental: true
state.checkpoints.dir: hdfs://namenode:9000/flink/checkpoints
state.savepoints.dir: hdfs://namenode:9000/flink/savepoints
state.backend.rocksdb.checkpoint.transfer.thread.num: 4
state.backend.local-recovery: true
taskmanager.network.memory.buffer-debloat.enabled: true

# ============ RocksDB 调优（flink-conf.yaml）============
# 写入缓冲区
state.backend.rocksdb.writebuffer.size: 128mb
state.backend.rocksdb.writebuffer.count: 4
state.backend.rocksdb.writebuffer.number-to-merge: 3

# 压缩
state.backend.rocksdb.compaction.level.max-size-level-base: 256mb
state.backend.rocksdb.compaction.style: LEVEL

# Block Cache
state.backend.rocksdb.block.blocksize: 16kb
state.backend.rocksdb.block.cache-size: 256mb

# 线程配置
state.backend.rocksdb.thread.num: 4

# 增量Checkpoint
state.backend.rocksdb.predefined-options: SPINNING_DISK_OPTIMIZED_HIGH_MEM

# Local Recovery
state.backend.local-recovery: true
taskmanager.state.local.root-dirs: /tmp/flink-local-state
```

### 4.2 调优决策树

```yaml
# Checkpoint调优决策流程:
# 
# 问题: Checkpoint超时
#   ├── 状态大(>10GB)?
#   │   ├── 是 → 使用RocksDB + 增量Checkpoint
#   │   │      → 增大checkpoint.timeout到20-30分钟
#   │   │      → 降低checkpoint间隔到5-10分钟
#   │   └── 否 → 检查存储系统性能
#   │
#   ├── 反压严重?
#   │   ├── 是 → 开启非对齐Checkpoint
#   │   │      → 或者优化处理逻辑消除反压根源
#   │   └── 否 → 增大超时时间
#   │
#   └── Barrier对齐慢?
#       ├── 是(单通道延迟) → 检查是否存在数据倾斜
#       └── 是(多通道) → 开启非对齐Checkpoint

# 常用场景参数速查:
# 场景1: 轻量级流(状态<100MB, 延迟敏感)
checkpoint.interval = 1-3分钟
state.backend = hashmap
checkpoint.timeout = 5分钟

# 场景2: 中量级流(状态100MB-1GB, 生产常见)
checkpoint.interval = 3-5分钟
state.backend = rocksdb + 增量
checkpoint.timeout = 10分钟

# 场景3: 重量级流(状态>1GB, Join/Condition类应用)
checkpoint.interval = 5-10分钟
state.backend = rocksdb + 增量 + Local Recovery
checkpoint.timeout = 15-20分钟
incremental.checkpoint = true

# 场景4: 高反压(背压频繁)
unaligned.checkpoint = true
alignment.timeout = 30s  # 30秒对齐不到齐则走非对齐
```

### 4.3 Checkpoint监控命令

```bash
# 通过REST API查看Checkpoint历史
curl http://localhost:8081/jobs/<jobId>/checkpoints

# 查看Checkpoint配置
curl http://localhost:8081/jobs/<jobId>/checkpoints/config

# 查看最近一次完成的Checkpoint
curl http://localhost:8081/jobs/<jobId>/checkpoints/details/<checkpointId>

# 查看Checkpoint统计（Prometheus格式）
curl http://localhost:8081/jobs/<jobId>/metrics?get=\
  numberOfCompletedCheckpoints,\
  numberOfFailedCheckpoints,\
  lastCheckpointDuration,\
  lastCheckpointSize,\
  lastCheckpointAlignmentBuffered

# 触发Checkpoint（通过REST API）
curl -X POST http://localhost:8081/jobs/<jobId>/checkpoints
```

---

## 五、ClickHouse 常用命令速查

### 5.1 连接与基础操作

```bash
# 命令行客户端连接
clickhouse-client -h localhost --port 9000 -u default --password '' \
  --database analytics

# 执行SQL文件
clickhouse-client --query "$(cat my_query.sql)"

# 非交互式执行单条SQL
clickhouse-client --query "SELECT count() FROM analytics.events"

# 带格式输出
clickhouse-client --format PrettyCompact --query "SELECT * FROM events LIMIT 10"
clickhouse-client --format JSONEachRow --query "SELECT * FROM events LIMIT 10"
clickhouse-client --format CSVWithNames --query "SELECT * FROM events LIMIT 10"

# 导入CSV数据
clickhouse-client --query "INSERT INTO analytics.events FORMAT CSV" < data.csv

# 导出数据到CSV
clickhouse-client --query "SELECT * FROM analytics.events" \
  --format CSVWithNames > export.csv

# 查看数据库列表
clickhouse-client --query "SHOW DATABASES"

# 查看表列表
clickhouse-client --query "SHOW TABLES FROM analytics"

# 查看表结构
clickhouse-client --query "DESCRIBE TABLE analytics.events"

# 查看建表语句
clickhouse-client --query "SHOW CREATE TABLE analytics.events"
```

### 5.2 集群与副本管理

```bash
# 查看集群信息
clickhouse-client --query "SELECT * FROM system.clusters"

# 查看副本状态
clickhouse-client --query "
SELECT
  database,
  table,
  is_leader,
  total_replicas,
  active_replicas
FROM system.replicas
"

# 查看分布式表发送延迟（需要发送但未发送的数据量）
clickhouse-client --query "
SELECT
  database,
  table,
  is_readonly,
  future_parts,
  parts_to_check,
  queue_size,
  inserts_in_queue,
  merges_in_queue
FROM system.replicas
"

# 手动同步副本（副本不一致时）
clickhouse-client --query "SYSTEM SYNC REPLICA analytics.events"

# 重启副本（副本进入只读状态时）
clickhouse-client --query "SYSTEM RESTART REPLICA analytics.events"

# 查看ZooKeeper中的ClickHouse信息
clickhouse-client --query "SELECT * FROM system.zookeeper WHERE path = '/'"

# 查看特定表的ZK路径
clickhouse-client --query "
SELECT * FROM system.zookeeper
WHERE path = '/clickhouse/tables/01/analytics/events'
"
```

### 5.3 合并（Merge）管理

```bash
# 查看Merge队列
clickhouse-client --query "
SELECT
  database,
  table,
  elapsed,
  progress,
  num_parts,
  result_part_name,
  total_size_bytes_compressed,
  bytes_read_uncompressed,
  bytes_written_uncompressed,
  memory_usage,
  thread_number
FROM system.merges
ORDER BY elapsed DESC
"

# 查看Parts信息（查看数据碎片化程度）
clickhouse-client --query "
SELECT
  database,
  table,
  partition,
  name,
  active,
  rows,
  bytes_on_disk,
  modification_time
FROM system.parts
WHERE database = 'analytics' AND table = 'events'
ORDER BY modification_time DESC
"

# 手动优化表（触发Merge）
clickhouse-client --query "OPTIMIZE TABLE analytics.events FINAL"

# 手动优化指定分区
clickhouse-client --query "OPTIMIZE TABLE analytics.events PARTITION '2024-01' FINAL"

# 查看当前正在执行的操作
clickhouse-client --query "
SELECT
  query_id,
  query,
  elapsed,
  read_rows,
  memory_usage
FROM system.processes
WHERE query NOT LIKE '%system.processes%'
"

# Kill长时间运行的查询
clickhouse-client --query "KILL QUERY WHERE query_id = 'xxx-xxx-xxx'"

# Kill所有Mutation（ALTER UPDATE/DELETE操作）
clickhouse-client --query "KILL MUTATION WHERE database='analytics' AND table='events'"
```

### 5.4 性能诊断

```bash
# 查看查询日志（system.query_log）
clickhouse-client --query "
SELECT
  query_start_time,
  query_duration_ms,
  read_rows,
  read_bytes,
  memory_usage,
  query
FROM system.query_log
WHERE type = 'QueryFinish'
ORDER BY query_start_time DESC
LIMIT 10
"

# 找出最慢的查询（Top 10）
clickhouse-client --query "
SELECT
  query,
  query_duration_ms,
  read_rows,
  formatReadableSize(read_bytes) AS read_size
FROM system.query_log
WHERE type = 'QueryFinish' AND query_duration_ms > 1000
ORDER BY query_duration_ms DESC
LIMIT 10
"

# 查看表大小
clickhouse-client --query "
SELECT
  database,
  table,
  formatReadableSize(sum(bytes_on_disk)) AS size,
  sum(rows) AS rows,
  count() AS parts
FROM system.parts
WHERE active = 1
GROUP BY database, table
ORDER BY sum(bytes_on_disk) DESC
"

# 查看列压缩比
clickhouse-client --query "
SELECT
  name,
  compression_codec,
  formatReadableSize(data_compressed_bytes) AS compressed,
  formatReadableSize(data_uncompressed_bytes) AS uncompressed
FROM system.columns
WHERE database = 'analytics' AND table = 'events'
"

# 查看当前连接数
clickhouse-client --query "SELECT count() FROM system.processes"

# 查看内存使用
clickhouse-client --query "
SELECT
  metric,
  value,
  description
FROM system.metrics
WHERE metric IN ('MemoryTracking', 'MemoryResident', 'Query')
"
```

### 5.5 数据压缩与TTL

```bash
# 查看TTL策略
clickhouse-client --query "SELECT name, engine_full FROM system.tables WHERE database='analytics'"

# 强制触发TTL清理
clickhouse-client --query "ALTER TABLE analytics.events MATERIALIZE TTL"

# 修改TTL
clickhouse-client --query "
ALTER TABLE analytics.events
MODIFY TTL event_time + INTERVAL 72 HOUR
"

# 添加列级TTL
clickhouse-client --query "
ALTER TABLE analytics.events
MODIFY COLUMN raw_data String TTL event_time + INTERVAL 24 HOUR
"

# 修改压缩策略
clickhouse-client --query "
ALTER TABLE analytics.events
MODIFY COLUMN event_data String CODEC(ZSTD(3))
"
```

### 5.6 备份与恢复

```bash
# 导出整个数据库结构
clickhouse-client --query "SHOW CREATE DATABASE analytics" > schema.sql
# 导出所有表结构
clickhouse-client --query "
SELECT concat('-- Table: ', name, '\n', create_table_query, ';\n')
FROM system.tables
WHERE database = 'analytics'
FORMAT TSVRaw
" >> schema.sql

# 备份单个表（导出INSERT语句）
clickhouse-client --query "
SELECT * FROM analytics.events
FORMAT Native
" > events_backup.native

# 恢复数据（从Native格式）
clickhouse-client --query "
INSERT INTO analytics.events FORMAT Native
" < events_backup.native

# 在线备份（使用ALTER TABLE FREEZE）
# 1. 创建冻结快照（不会阻塞读写）
clickhouse-client --query "ALTER TABLE analytics.events FREEZE"
# 2. 备份冻结的文件
cp -r /var/lib/clickhouse/shadow/ /backup/clickhouse/shadow_$(date +%Y%m%d)
# 3. 清理冻结（可选）
clickhouse-client --query "ALTER TABLE analytics.events UNFREEZE"
```

---

## 六、常见问题快速排查命令集合

### 6.1 Kafka 问题排查命令集

```bash
# ============ 问题1: Producer发送失败 ============
# 症状: Producer报错或发送超时
# 排查命令:
# 1. 检查Broker是否可达
echo "test" | kafka-console-producer.sh --bootstrap-server localhost:9092 \
  --topic test-connection
# 2. 检查Topic是否存在
kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic my-topic
# 3. 检查min.insync.replicas和当前ISR数量
kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic my-topic | grep "Isr:"
# 4. 检查Broker磁盘是否满了
df -h /var/lib/kafka/data

# ============ 问题2: Consumer Lag持续增长 ============
# 症状: kafka-consumer-groups显示LAG持续增大
# 排查命令:
# 1. 确认当前Lag
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group my-group --describe
# 2. 检查Consumer是否存活
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group my-group \
  --describe --members
# 3. 检查Consumer处理延迟（查看Consumer日志中的处理耗时）
# 4. 与生产速率对比
kafka-producer-perf-test.sh --topic my-topic --num-records 1000 \
  --record-size 1024 --throughput -1 \
  --producer-props bootstrap.servers=localhost:9092 2>&1 | grep "records/sec"

# ============ 问题3: Broker宕机恢复慢 ============
# 症状: Broker重启后长时间无法追平Leader
# 排查命令:
# 1. 查看复制落后量
kafka-replica-verification.sh --broker-list localhost:9092
# 2. 查看网络吞吐
iftop -i eth0
# 3. 查看磁盘 IO
iostat -x 1 5

# ============ 问题4: ISR频繁变化 ============
# 症状: Isr Shrinks/Expands 频繁发生
# 排查命令:
# 1. 查看ISR变化历史（JMX指标IsrShrinksPerSec, IsrExpandsPerSec）
# 2. 检查Follower的fetch延迟
# 3. 检查Broker间网络延迟
ping -c 100 kafka-broker-2
# 4. 查看GC日志，确认不是GC导致停顿
grep "Full GC" /var/log/kafka/gc.log
```

### 6.2 Flink 问题排查命令集

```bash
# ============ 问题1: Checkpoint超时/失败 ============
# 症状: Flink UI显示Checkpoint FAILED或超时
# 排查命令:
# 1. 查看Checkpoint历史
curl http://localhost:8081/jobs/<jobId>/checkpoints
# 2. 查看失败原因
curl http://localhost:8081/jobs/<jobId>/checkpoints/details/<checkpointId>
# 3. 检查状态大小
curl http://localhost:8081/jobs/<jobId>/metrics?get=lastCheckpointSize
# 4. 检查存储连通性
hdfs dfs -ls hdfs://namenode:9000/flink/checkpoints/<jobId>/

# ============ 问题2: 反压(Backpressure) ============
# 症状: Flink UI显示算子为HIGH反压(红色)
# 排查命令:
# 1. 查看反压状态
curl http://localhost:8081/jobs/<jobId>/vertices/<vertexId>/backpressure
# 2. 查看算子吞吐量
curl http://localhost:8081/jobs/<jobId>/vertices/<vertexId>/metrics?get=\
  numRecordsInPerSecond,numRecordsOutPerSecond
# 3. 查看TaskManager CPU/内存
curl http://localhost:8081/taskmanagers/<tmId>/metrics?get=\
  Status.JVM.CPU.Load,Status.JVM.Memory.Heap.Used

# ============ 问题3: 作业频繁重启 ============
# 症状: Job在RESTARTING和RUNNING之间反复
# 排查命令:
# 1. 查看异常信息
curl http://localhost:8081/jobs/<jobId>/exceptions
# 2. 查看TaskManager日志
grep -i "error\|exception\|fail" /opt/flink/log/flink-*-taskexecutor-*.log | tail -50
# 3. 检查是否是OOM
grep -i "OutOfMemoryError\|oom" /opt/flink/log/*.out | tail -20

# ============ 问题4: 端到端延迟过高 ============
# 症状: Kafka生产到ClickHouse落盘延迟 > 预期
# 排查命令:
# 1. 检查Kafka端延迟(Kafka Consumer Lag)
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group flink-group --describe
# 2. 检查Flink处理延迟
curl http://localhost:8081/jobs/<jobId>/metrics?get=\
  lastCheckpointDuration,numberOfCompletedCheckpoints
# 3. 检查ClickHouse写入延迟
clickhouse-client --query "
SELECT query_duration_ms, query
FROM system.query_log WHERE type='QueryFinish' AND query LIKE '%INSERT%'
ORDER BY query_start_time DESC LIMIT 5
"
```

### 6.3 ClickHouse 问题排查命令集

```bash
# ============ 问题1: 查询变慢 ============
# 症状: 原来毫秒级查询变成秒级
# 排查命令:
# 1. 查看是否有大量Parts未合并
clickhouse-client --query "
SELECT database, table, count() AS parts
FROM system.parts WHERE active=1
GROUP BY database, table HAVING parts > 100
"
# 2. 查看Merge队列
clickhouse-client --query "SELECT * FROM system.merges"
# 3. 查看内存是否充足
clickhouse-client --query "
SELECT metric, value FROM system.metrics WHERE metric LIKE '%Memory%'
"
# 4. 分析查询计划
clickhouse-client --query "EXPLAIN SELECT ..." --format PrettyCompact

# ============ 问题2: 写入积压 ============
# 症状: Flink Sink写入ClickHouse越来越慢
# 排查命令:
# 1. 查看当前Parts数量（碎片化程度）
clickhouse-client --query "
SELECT database, table, partition, count() AS parts, sum(rows) AS rows
FROM system.parts WHERE active=1
GROUP BY database, table, partition
ORDER BY parts DESC LIMIT 20
"
# 2. 查看磁盘IO
iostat -x 1 5
# 3. 查看未合并的数据量
clickhouse-client --query "SELECT * FROM system.replication_queue" --format PrettyCompact

# ============ 问题3: 副本延迟 ============
# 症状: ReplicaDelay过大
# 排查命令:
# 1. 检查副本队列
clickhouse-client --query "SELECT * FROM system.replication_queue"
# 2. 检查网络
ping -c 10 clickhouse-node2
# 3. 查看故障副本
clickhouse-client --query "SELECT database, table, total_replicas, active_replicas
FROM system.replicas WHERE active_replicas < total_replicas"
```

### 6.4 一键诊断脚本

```bash
#!/bin/bash
# quick-diagnosis.sh - 大数据系统一键诊断

echo "=========== 1. Kafka 集群状态 ==========="
kafka-topics.sh --bootstrap-server localhost:9092 --list 2>/dev/null | wc -l
echo "Under Replicated Partitions:"
kafka-topics.sh --bootstrap-server localhost:9092 --describe --under-replicated-partitions 2>/dev/null | wc -l

echo ""
echo "=========== 2. Flink 集群状态 ==========="
curl -s http://localhost:8081/overview 2>/dev/null | python3 -m json.tool 2>/dev/null || echo "Flink不可达"

echo ""
echo "=========== 3. ClickHouse 状态 ==========="
clickhouse-client --query "SELECT metric, value FROM system.metrics WHERE metric IN ('ReadonlyReplica','Query','Merge')" 2>/dev/null

echo ""
echo "=========== 4. 磁盘使用率 ==========="
df -h /var/lib/kafka /var/lib/clickhouse /opt/flink 2>/dev/null

echo ""
echo "=========== 5. 内存使用 ==========="
free -h

echo ""
echo "=========== 6. ZooKeeper 状态 ==========="
echo stat | nc localhost 2181 2>/dev/null | head -5 || echo "ZK不可达"

echo ""
echo "=========== 诊断完成 ==========="
```

---

## 七、附录：快速参考卡片

### 7.1 Kafka 关键路径速记

```
Topic管理:    kafka-topics.sh --bootstrap-server localhost:9092 --{create|list|describe|alter|delete}
Consumer组:   kafka-consumer-groups.sh --bootstrap-server localhost:9092 --{list|describe|delete}
Producer测试:  kafka-producer-perf-test.sh --topic xxx --num-records xxx --record-size xxx
Consumer测试:  kafka-consumer-perf-test.sh --topic xxx --messages xxx --group xxx
配置管理:     kafka-configs.sh --bootstrap-server localhost:9092 --entity-type {topics|brokers|users}
ACL管理:      kafka-acls.sh --bootstrap-server localhost:9092 --{add|remove|list}
元数据:       kafka-metadata-quorum.sh --bootstrap-server localhost:9092 describe --status
```

### 7.2 Kafka 常用端口

```
9092  - Kafka Broker (PLAINTEXT)
9093  - Kafka Broker (SSL)
9094  - Kafka Broker (SASL_SSL)
9999  - JMX (默认)
2181  - ZooKeeper Client Port
2888  - ZooKeeper Peer Port
3888  - ZooKeeper Leader Election
```

### 7.3 Flink 常用端口

```
8081  - Flink Web UI (JobManager)
6123  - JobManager RPC
6124  - TaskManager RPC
6125  - TaskManager Data Port
9999  - JMX (默认)
9249  - PrometheusReporter
```

### 7.4 ClickHouse 常用端口

```
8123  - HTTP 接口
9000  - Native TCP 协议
9004  - MySQL 协议 (clickhouse-server --mysql-port)
9009  - Interserver HTTP (副本间通信)
9363  - Prometheus Metrics
```