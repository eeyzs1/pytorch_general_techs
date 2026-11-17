# L3 实验：CDC 重放与删除一致性

用 Python 标准库与 SQLite 实现一个可恢复的最新状态表，观察重复输入、业务版本迟到、删除后旧状态复活及提交中断。配套阅读：[2026-11 湖仓与流处理工程更新](../../2026-11_湖仓与流处理工程更新.md)。

## 输入约定

每行 JSON 包含 `partition`、`offset`、`key`、`revision`、`op`、`value`。只处理一个流；`(partition, offset)` 是传输身份，`revision` 是同一业务主键可比较的版本。

- 每个分区的新 offset 递增，允许空洞；已接收的 offset 可以重放。
- 业务 revision 可以随到达顺序变小；同一 key / revision 的业务内容必须一致。
- `upsert` 的 value 为对象，`delete` 的 value 为 null。
- 删除保留 revision 墓碑，直到有更高版本明确重建。
- 不同时处理多个 topic / 源数据库；扩展时需把源命名空间纳入身份与 checkpoint。

这里的“乱序”指业务版本迟到。源传输位置无序且尚未接收时会报错，防止进度越过未处理的消息。消费者需要按其源协议建立分区内顺序。

## 运行与重放

在本实验目录中运行，Python 3.10+，无第三方依赖：

```bash
python replay_cdc.py data/events.jsonl.sample
python replay_cdc.py data/events.jsonl.sample
python -m unittest test_replay_cdc.py
```

第一次处理 10 条输入，其中 2 条重复、2 条业务旧版本；保留 A 的已支付状态、C 的已发货状态和 B 的删除墓碑。第二次处理同一文件，10 条都识别为重复，数据库状态保持一致。输出为 `output/cdc.db` 和 `output/report.json`。

从 `big_data` 目录运行时显式指定输出路径：

```bash
python labs/l3-cdc-replay/replay_cdc.py labs/l3-cdc-replay/data/events.jsonl.sample --database labs/l3-cdc-replay/output/cdc.db --output labs/l3-cdc-replay/output/report.json
python -m unittest discover -s labs/l3-cdc-replay -p "test_*.py"
```

## 验证与恢复边界

业务状态、接收记录和分区进度在一个 SQLite 事务里提交；任何输入、版本冲突或读取错误都会回滚整个批次。测试覆盖完整重放、删除后的迟到写入、独立分区位置、内容冲突、批次回滚和关闭 / 重开数据库。

接收记录在本实验中不清理，输入通过迭代器逐条读取，整个批次仍是一个事务。大规模生产系统需设定批次边界、去重记录保留期、schema 演进及并发写入策略。发邮件等外部副作用不属于这个 SQLite 事务；这个实验也未实现 Kafka / Flink / Iceberg 的集群事务协议。
