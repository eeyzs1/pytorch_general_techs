# 项目B：IoT设备监控与预测性维护

> **所属阶段**：L2 中级工程师 | **模块**：补充模块_跨行业实战 | **预计时长**：25h | **难度**：★★★★☆
>
> **技术栈**：MQTT(EMQX) → Kafka → Flink → TDengine + Redis → XGBoost → Grafana
>
> **前置要求**：完成L2课时17-18（Kafka深入）+ 课时19-21（Flink流处理）

---

## 一、项目描述

构建IoT场景的设备实时监控和预测性维护系统。项目覆盖设备数据模拟、时序数据管道、预测性维护模型、监控告警全流程，让学员掌握工业物联网大数据的核心应用模式。

### 业务价值

```
IoT预测性维护系统解决的问题：

  问题1: "设备故障如何提前预警？"
    → 以前: 故障后维修，产线停机损失巨大
    → 现在: 预测性维护，提前24小时预警

  问题2: "如何实时监控1000台设备？"
    → 以前: 人工巡检，效率低覆盖面窄
    → 现在: 实时监控大屏，异常秒级发现

  问题3: "传感器数据如何高效存储和查询？"
    → 以前: 关系型数据库，写入慢查询慢
    → 现在: TDengine时序数据库，千万级吞吐

  问题4: "如何从传感器数据中提取故障特征？"
    → 以前: 阈值告警，误报多漏报多
    → 现在: ML模型预测，精确率>85%
```

---

## 二、整体架构

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                      IoT设备监控与预测性维护系统                                │
│                                                                              │
│  ┌──────────┐   ┌──────────┐   ┌───────────┐   ┌────────────────────────┐  │
│  │ IoT设备  │──→│  EMQX    │──→│   Kafka   │──→│       Flink           │  │
│  │(传感器)  │   │(MQTT网关)│   │ (消息队列) │   │ (实时处理+特征计算)   │  │
│  └──────────┘   └──────────┘   └───────────┘   └──────────┬─────────────┘  │
│                                                          │                  │
│                              ┌───────────────────────────┼──────────┐       │
│                              │                           │          │       │
│                       ┌──────▼──────┐           ┌───────▼───┐ ┌───▼─────┐ │
│                       │  TDengine   │           │   Redis   │ │ XGBoost │ │
│                       │ (时序存储)  │           │ (实时缓存)│ │(预测模型)│ │
│                       └──────┬──────┘           └───────┬───┘ └───┬─────┘ │
│                              │                          │         │        │
│                       ┌──────▼──────────────────────────▼─────────▼─────┐ │
│                       │                  Grafana                        │ │
│                       │            (监控大屏+告警)                      │ │
│                       └────────────────────────────────────────────────┘ │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 三、阶段1 - IoT数据模拟（4h）

### 3.1 设备数据模型

```sql
-- ============================================
-- IoT设备管理数据模型（MySQL）
-- ============================================

CREATE DATABASE IF NOT EXISTS iot_monitor;

CREATE TABLE iot_monitor.devices (
    device_id VARCHAR(32) PRIMARY KEY,
    device_type VARCHAR(20) NOT NULL COMMENT '电机/泵/压缩机/风机/传送带',
    factory VARCHAR(50) NOT NULL,
    production_line VARCHAR(50) NOT NULL,
    install_date DATE NOT NULL,
    status TINYINT DEFAULT 1 COMMENT '0-停机 1-运行 2-维修 3-报废',
    last_maintenance_date DATE,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_device_type (device_type),
    INDEX idx_factory (factory),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE iot_monitor.fault_records (
    fault_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    device_id VARCHAR(32) NOT NULL,
    fault_type VARCHAR(30) NOT NULL COMMENT '过热/振动异常/压力异常/电流异常/轴承磨损',
    fault_time DATETIME NOT NULL,
    fault_severity TINYINT COMMENT '1-轻微 2-中等 3-严重',
    repair_duration_hours DECIMAL(6, 2),
    repair_cost DECIMAL(10, 2),
    INDEX idx_device_id (device_id),
    INDEX idx_fault_time (fault_time),
    INDEX idx_fault_type (fault_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 3.2 TDengine时序表设计

```sql
-- ============================================
-- TDengine 时序数据表设计
-- ============================================

CREATE STABLE iot_monitor.sensor_data (
    ts TIMESTAMP,
    value DOUBLE
) TAGS (
    device_id BINARY(32),
    sensor_type BINARY(20),
    factory BINARY(50),
    production_line BINARY(50)
);

CREATE STABLE iot_monitor.sensor_stats_minute (
    ts TIMESTAMP,
    avg_value DOUBLE,
    max_value DOUBLE,
    min_value DOUBLE,
    std_value DOUBLE,
    count_value BIGINT
) TAGS (
    device_id BINARY(32),
    sensor_type BINARY(20)
);

CREATE STABLE iot_monitor.anomaly_events (
    ts TIMESTAMP,
    anomaly_type BINARY(30),
    anomaly_value DOUBLE,
    threshold DOUBLE,
    severity BINARY(10)
) TAGS (
    device_id BINARY(32),
    sensor_type BINARY(20)
);

CREATE STABLE iot_monitor.prediction_results (
    ts TIMESTAMP,
    fault_probability DOUBLE,
    predicted_fault_type BINARY(30),
    confidence DOUBLE
) TAGS (
    device_id BINARY(32)
);
```

### 3.3 IoT数据模拟器

```python
"""
iot_data_simulator.py

IoT设备数据模拟器
1000台设备、10种传感器、每秒10000条数据点
模拟正常模式 + 异常模式 + 故障模式
"""
import json
import time
import random
import math
import hashlib
import paho.mqtt.client as mqtt
from datetime import datetime, timedelta
from threading import Thread, Event

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/sensor/data"

DEVICE_TYPES = ['电机', '泵', '压缩机', '风机', '传送带']
FACTORIES = ['北京工厂', '上海工厂', '广州工厂', '深圳工厂']
PRODUCTION_LINES = ['A线', 'B线', 'C线', 'D线', 'E线']

SENSOR_CONFIGS = {
    '电机': [
        {'name': 'temperature', 'unit': '°C', 'normal_range': (40, 80), 'anomaly_shift': 30},
        {'name': 'vibration', 'unit': 'mm/s', 'normal_range': (0.5, 4.0), 'anomaly_shift': 5.0},
        {'name': 'current', 'unit': 'A', 'normal_range': (10, 50), 'anomaly_shift': 20},
        {'name': 'rpm', 'unit': 'rpm', 'normal_range': (1400, 1600), 'anomaly_shift': 200},
        {'name': 'power', 'unit': 'kW', 'normal_range': (5, 25), 'anomaly_shift': 10},
    ],
    '泵': [
        {'name': 'temperature', 'unit': '°C', 'normal_range': (30, 70), 'anomaly_shift': 25},
        {'name': 'vibration', 'unit': 'mm/s', 'normal_range': (1.0, 6.0), 'anomaly_shift': 8.0},
        {'name': 'pressure_in', 'unit': 'MPa', 'normal_range': (0.2, 0.8), 'anomaly_shift': 0.3},
        {'name': 'pressure_out', 'unit': 'MPa', 'normal_range': (1.0, 3.0), 'anomaly_shift': 1.0},
        {'name': 'flow_rate', 'unit': 'm³/h', 'normal_range': (10, 50), 'anomaly_shift': 15},
    ],
    '压缩机': [
        {'name': 'temperature', 'unit': '°C', 'normal_range': (50, 100), 'anomaly_shift': 35},
        {'name': 'vibration', 'unit': 'mm/s', 'normal_range': (0.5, 3.0), 'anomaly_shift': 4.0},
        {'name': 'pressure', 'unit': 'MPa', 'normal_range': (0.6, 1.2), 'anomaly_shift': 0.4},
        {'name': 'current', 'unit': 'A', 'normal_range': (20, 80), 'anomaly_shift': 30},
        {'name': 'oil_level', 'unit': '%', 'normal_range': (60, 100), 'anomaly_shift': -30},
    ],
    '风机': [
        {'name': 'temperature', 'unit': '°C', 'normal_range': (30, 60), 'anomaly_shift': 20},
        {'name': 'vibration', 'unit': 'mm/s', 'normal_range': (0.3, 2.5), 'anomaly_shift': 3.0},
        {'name': 'wind_speed', 'unit': 'm/s', 'normal_range': (5, 15), 'anomaly_shift': 5},
        {'name': 'current', 'unit': 'A', 'normal_range': (5, 30), 'anomaly_shift': 15},
        {'name': 'bearing_temp', 'unit': '°C', 'normal_range': (40, 80), 'anomaly_shift': 30},
    ],
    '传送带': [
        {'name': 'temperature', 'unit': '°C', 'normal_range': (25, 50), 'anomaly_shift': 20},
        {'name': 'vibration', 'unit': 'mm/s', 'normal_range': (0.2, 1.5), 'anomaly_shift': 2.0},
        {'name': 'speed', 'unit': 'm/s', 'normal_range': (0.5, 2.0), 'anomaly_shift': 0.5},
        {'name': 'tension', 'unit': 'N', 'normal_range': (500, 2000), 'anomaly_shift': 500},
        {'name': 'current', 'unit': 'A', 'normal_range': (3, 15), 'anomaly_shift': 8},
    ],
}


class DeviceSimulator:

    def __init__(self, device_id, device_type, factory, production_line):
        self.device_id = device_id
        self.device_type = device_type
        self.factory = factory
        self.production_line = production_line
        self.sensors = SENSOR_CONFIGS[device_type]
        self.sensor_states = {}
        self.anomaly_start_time = None
        self.anomaly_sensors = []
        self.fault_time = None
        self.is_faulty = False

        for sensor in self.sensors:
            mid = (sensor['normal_range'][0] + sensor['normal_range'][1]) / 2
            self.sensor_states[sensor['name']] = {
                'current_value': mid,
                'trend': 0,
                'noise_level': (sensor['normal_range'][1] - sensor['normal_range'][0]) * 0.05
            }

    def _generate_normal_value(self, sensor_name):
        state = self.sensor_states[sensor_name]
        config = next(s for s in self.sensors if s['name'] == sensor_name)

        state['current_value'] += random.gauss(0, state['noise_level'])
        state['current_value'] += state['trend'] * 0.01

        low, high = config['normal_range']
        mid = (low + high) / 2
        state['current_value'] = mid + (state['current_value'] - mid) * 0.99

        state['current_value'] = max(low * 0.8, min(high * 1.2, state['current_value']))

        return round(state['current_value'], 3)

    def _generate_anomaly_value(self, sensor_name):
        state = self.sensor_states[sensor_name]
        config = next(s for s in self.sensors if s['name'] == sensor_name)

        if sensor_name in self.anomaly_sensors:
            state['trend'] += config['anomaly_shift'] * 0.005
            state['current_value'] += state['trend'] * 0.02
            state['current_value'] += random.gauss(0, state['noise_level'] * 3)

            low, high = config['normal_range']
            state['current_value'] = max(low * 0.5, min(high * 2.0, state['current_value']))
        else:
            return self._generate_normal_value(sensor_name)

        return round(state['current_value'], 3)

    def trigger_anomaly(self, current_time):
        if self.anomaly_start_time is None and random.random() < 0.0001:
            self.anomaly_start_time = current_time
            num_anomaly_sensors = random.randint(1, 3)
            self.anomaly_sensors = [s['name'] for s in random.sample(self.sensors, num_anomaly_sensors)]

            fault_delay = random.randint(3600, 86400)
            self.fault_time = self.anomaly_start_time + fault_delay

    def generate_reading(self, current_time):
        self.trigger_anomaly(current_time)

        readings = []
        for sensor in self.sensors:
            if self.anomaly_start_time is not None and current_time >= self.anomaly_start_time:
                value = self._generate_anomaly_value(sensor['name'])
            else:
                value = self._generate_normal_value(sensor['name'])

            readings.append({
                'device_id': self.device_id,
                'device_type': self.device_type,
                'factory': self.factory,
                'production_line': self.production_line,
                'sensor_type': sensor['name'],
                'unit': sensor['unit'],
                'value': value,
                'timestamp': int(current_time * 1000),
                'is_anomaly': 1 if (self.anomaly_start_time and
                                    current_time >= self.anomaly_start_time and
                                    sensor['name'] in self.anomaly_sensors) else 0,
                'fault_label': 1 if (self.fault_time and current_time >= self.fault_time) else 0
            })

        if self.fault_time and current_time >= self.fault_time + 3600:
            self.anomaly_start_time = None
            self.anomaly_sensors = []
            self.fault_time = None
            for sensor_name in self.sensor_states:
                mid = (next(s['normal_range'][0] + s['normal_range'][1] for s in self.sensors if s['name'] == sensor_name)) / 2
                self.sensor_states[sensor_name]['current_value'] = mid
                self.sensor_states[sensor_name]['trend'] = 0

        return readings


class IoTSimulator:

    def __init__(self, num_devices=1000, rate_per_second=10000):
        self.num_devices = num_devices
        self.rate = rate_per_second
        self.devices = []
        self.client = mqtt.Client(client_id="iot_simulator")
        self.stop_event = Event()

        for i in range(num_devices):
            device_id = f"DEV_{i+1:06d}"
            device_type = random.choice(DEVICE_TYPES)
            factory = random.choice(FACTORIES)
            production_line = random.choice(PRODUCTION_LINES)
            self.devices.append(
                DeviceSimulator(device_id, device_type, factory, production_line)
            )

    def connect(self):
        self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
        self.client.loop_start()
        print(f"已连接MQTT Broker: {MQTT_BROKER}:{MQTT_PORT}")

    def run(self, duration_seconds=3600):
        self.connect()
        print(f"开始模拟: {self.num_devices}台设备, {self.rate}条/秒, 持续{duration_seconds}秒")

        start_time = time.time()
        current_sim_time = start_time
        total_sent = 0
        interval = 1.0 / (self.rate / self.num_devices)

        batch = []
        batch_size = 500

        while not self.stop_event.is_set() and (time.time() - start_time) < duration_seconds:
            for device in self.devices:
                readings = device.generate_reading(current_sim_time)
                for reading in readings:
                    batch.append(json.dumps(reading))

                    if len(batch) >= batch_size:
                        payload = "\n".join(batch)
                        self.client.publish(MQTT_TOPIC, payload, qos=0)
                        total_sent += len(batch)
                        batch = []

                if total_sent % 100000 < self.num_devices * 10:
                    elapsed = time.time() - start_time
                    actual_rate = total_sent / elapsed if elapsed > 0 else 0
                    print(f"  已发送 {total_sent} 条, 实际速率 {actual_rate:.0f}/s")

            current_sim_time += 1

            if total_sent % 1000000 == 0 and total_sent > 0:
                print(f"  里程碑: {total_sent} 条数据已发送")

        if batch:
            payload = "\n".join(batch)
            self.client.publish(MQTT_TOPIC, payload, qos=0)
            total_sent += len(batch)

        self.client.loop_stop()
        self.client.disconnect()
        print(f"模拟完成: 共发送 {total_sent} 条数据")

    def stop(self):
        self.stop_event.set()


if __name__ == '__main__':
    sim = IoTSimulator(num_devices=1000, rate_per_second=10000)
    try:
        sim.run(duration_seconds=3600)
    except KeyboardInterrupt:
        sim.stop()
        print("模拟器已停止")
```

---

## 四、阶段2 - 时序数据管道（8h）

### 4.1 EMQX + Kafka Connect配置

```properties
# emqx.conf 核心配置
listeners.tcp.default {
  bind = "0.0.0.0:1883"
  max_connections = 102400
}

# Kafka Bridge配置（EMQX企业版或使用Kafka Connect MQTT Source）
# Kafka Connect MQTT Source Connector配置
name=mqtt-source-iot
connector.class=com.datamountaineer.streamreactor.connect.mqtt.source.MqttSourceConnector
tasks.max=4
connect.mqtt.hosts=tcp://emqx:1883
connect.mqtt.topics=iot/sensor/#
connect.kafka.topic=iot.sensor.raw
connect.converter.key.converter=org.apache.kafka.connect.storage.StringConverter
connect.converter.value.converter=org.apache.kafka.connect.storage.StringConverter
```

### 4.2 Kafka Topic设计

| Topic名称 | 数据内容 | 分区数 | 副本数 | Retention |
|-----------|----------|--------|--------|-----------|
| iot.sensor.raw | 原始传感器数据 | 12 | 3 | 24h |
| iot.sensor.clean | 清洗后数据 | 12 | 3 | 24h |
| iot.sensor.stats | 聚合统计 | 6 | 3 | 168h |
| iot.anomaly.events | 异常事件 | 6 | 3 | 720h |
| iot.prediction.results | 预测结果 | 6 | 3 | 720h |

### 4.3 Flink实时处理作业

```java
package com.example.iot.monitor;

import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.functions.AggregateFunction;
import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.common.functions.FilterFunction;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.datastream.SingleOutputStreamOperator;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaProducer;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.util.OutputTag;
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

public class IoTPipeline {

    private static final OutputTag<String> ANOMALY_TAG = new OutputTag<String>("anomalies") {};

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();

        env.enableCheckpointing(30000);

        Properties kafkaProps = new Properties();
        kafkaProps.setProperty("bootstrap.servers", "localhost:9092");
        kafkaProps.setProperty("group.id", "iot-pipeline-group");
        kafkaProps.setProperty("auto.offset.reset", "latest");

        FlinkKafkaConsumer<String> source = new FlinkKafkaConsumer<>(
            "iot.sensor.raw",
            new SimpleStringSchema(),
            kafkaProps
        );

        DataStream<SensorReading> rawStream = env.addSource(source)
            .map(line -> JSON.parseObject(line, SensorReading.class))
            .assignTimestampsAndWatermarks(
                WatermarkStrategy
                    .<SensorReading>forBoundedOutOfOrderness(Duration.ofSeconds(3))
                    .withTimestampAssigner((event, ts) -> event.timestamp)
            );

        DataStream<SensorReading> cleanedStream = rawStream
            .filter(new OutlierFilterFunction())
            .map(new MissingValueFillFunction());

        DataStream<SensorStats> statsStream = cleanedStream
            .keyBy(r -> r.deviceId + "_" + r.sensorType)
            .window(TumblingEventTimeWindows.of(Time.minutes(1)))
            .aggregate(new SensorStatsAggregator());

        SingleOutputStreamOperator<SensorReading> mainStream = cleanedStream
            .process(new AnomalyDetectProcessFunction(ANOMALY_TAG));

        DataStream<String> anomalyStream = mainStream.getSideOutput(ANOMALY_TAG);

        FlinkKafkaProducer<String> statsSink = new FlinkKafkaProducer<>(
            "iot.sensor.stats",
            new SimpleStringSchema(),
            kafkaProps
        );

        FlinkKafkaProducer<String> anomalySink = new FlinkKafkaProducer<>(
            "iot.anomaly.events",
            new SimpleStringSchema(),
            kafkaProps
        );

        statsStream.map(s -> JSON.toJSONString(s)).addSink(statsSink);
        anomalyStream.addSink(anomalySink);

        env.execute("IoT Real-Time Pipeline");
    }

    static class OutlierFilterFunction implements FilterFunction<SensorReading> {
        @Override
        public boolean filter(SensorReading reading) throws Exception {
            if (reading.value == null || Double.isNaN(reading.value) || Double.isInfinite(reading.value)) {
                return false;
            }
            if ("temperature".equals(reading.sensorType)) {
                return reading.value > -50 && reading.value < 300;
            }
            if ("vibration".equals(reading.sensorType)) {
                return reading.value >= 0 && reading.value < 100;
            }
            if ("current".equals(reading.sensorType)) {
                return reading.value >= 0 && reading.value < 500;
            }
            if ("pressure".equals(reading.sensorType) || "pressure_in".equals(reading.sensorType)
                || "pressure_out".equals(reading.sensorType)) {
                return reading.value >= 0 && reading.value < 50;
            }
            return true;
        }
    }

    static class MissingValueFillFunction implements MapFunction<SensorReading, SensorReading> {
        @Override
        public SensorReading map(SensorReading reading) throws Exception {
            if (reading.value == null) {
                reading.value = 0.0;
                reading.filled = true;
            }
            return reading;
        }
    }

    static class SensorStatsAggregator implements AggregateFunction<
            SensorReading, StatsAccumulator, SensorStats> {

        @Override
        public StatsAccumulator createAccumulator() {
            return new StatsAccumulator();
        }

        @Override
        public StatsAccumulator add(SensorReading reading, StatsAccumulator acc) {
            acc.count++;
            acc.sum += reading.value;
            acc.sumSq += reading.value * reading.value;
            acc.min = Math.min(acc.min, reading.value);
            acc.max = Math.max(acc.max, reading.value);
            acc.deviceId = reading.deviceId;
            acc.sensorType = reading.sensorType;
            return acc;
        }

        @Override
        public SensorStats getResult(StatsAccumulator acc) {
            SensorStats stats = new SensorStats();
            stats.deviceId = acc.deviceId;
            stats.sensorType = acc.sensorType;
            stats.avgValue = acc.count > 0 ? acc.sum / acc.count : 0;
            stats.minValue = acc.min;
            stats.maxValue = acc.max;
            stats.stdValue = acc.count > 1
                ? Math.sqrt((acc.sumSq - acc.sum * acc.sum / acc.count) / (acc.count - 1))
                : 0;
            stats.count = acc.count;
            return stats;
        }

        @Override
        public StatsAccumulator merge(StatsAccumulator a, StatsAccumulator b) {
            a.count += b.count;
            a.sum += b.sum;
            a.sumSq += b.sumSq;
            a.min = Math.min(a.min, b.min);
            a.max = Math.max(a.max, b.max);
            return a;
        }
    }

    static class StatsAccumulator {
        String deviceId;
        String sensorType;
        long count = 0;
        double sum = 0;
        double sumSq = 0;
        double min = Double.MAX_VALUE;
        double max = Double.MIN_VALUE;
    }

    static class SensorReading {
        public String deviceId;
        public String deviceType;
        public String factory;
        public String productionLine;
        public String sensorType;
        public String unit;
        public Double value;
        public Long timestamp;
        public Integer isAnomaly;
        public Integer faultLabel;
        public Boolean filled;
    }

    static class SensorStats {
        public String deviceId;
        public String sensorType;
        public Double avgValue;
        public Double minValue;
        public Double maxValue;
        public Double stdValue;
        public Long count;
    }
}
```

### 4.4 Flink SQL实时处理

```sql
-- Flink SQL: IoT实时数据处理

CREATE TABLE iot_sensor_raw (
    device_id STRING,
    device_type STRING,
    factory STRING,
    production_line STRING,
    sensor_type STRING,
    unit STRING,
    value DOUBLE,
    `timestamp` BIGINT,
    is_anomaly INT,
    fault_label INT,
    event_time AS TO_TIMESTAMP(FROM_UNIXTIME(`timestamp` / 1000)),
    WATERMARK FOR event_time AS event_time - INTERVAL '3' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'iot.sensor.raw',
    'properties.bootstrap.servers' = 'localhost:9092',
    'properties.group.id' = 'iot-sql-group',
    'format' = 'json',
    'scan.startup.mode' = 'latest-offset'
);

CREATE TABLE iot_sensor_stats (
    device_id STRING,
    sensor_type STRING,
    window_start TIMESTAMP(3),
    window_end TIMESTAMP(3),
    avg_value DOUBLE,
    max_value DOUBLE,
    min_value DOUBLE,
    std_value DOUBLE,
    count_value BIGINT,
    PRIMARY KEY (device_id, sensor_type, window_start) NOT ENFORCED
) WITH (
    'connector' = 'upsert-kafka',
    'topic' = 'iot.sensor.stats',
    'properties.bootstrap.servers' = 'localhost:9092',
    'key.format' = 'json',
    'value.format' = 'json'
);

INSERT INTO iot_sensor_stats
SELECT
    device_id,
    sensor_type,
    TUMBLE_START(event_time, INTERVAL '1' MINUTE) AS window_start,
    TUMBLE_END(event_time, INTERVAL '1' MINUTE) AS window_end,
    AVG(value) AS avg_value,
    MAX(value) AS max_value,
    MIN(value) AS min_value,
    STDDEV_POP(value) AS std_value,
    COUNT(*) AS count_value
FROM iot_sensor_raw
WHERE value IS NOT NULL AND NOT IS_NAN(value)
GROUP BY
    device_id,
    sensor_type,
    TUMBLE(event_time, INTERVAL '1' MINUTE);

CREATE TABLE iot_anomaly_events (
    device_id STRING,
    sensor_type STRING,
    anomaly_type STRING,
    anomaly_value DOUBLE,
    threshold DOUBLE,
    severity STRING,
    event_time TIMESTAMP(3),
    PRIMARY KEY (device_id, sensor_type, event_time) NOT ENFORCED
) WITH (
    'connector' = 'upsert-kafka',
    'topic' = 'iot.anomaly.events',
    'properties.bootstrap.servers' = 'localhost:9092',
    'key.format' = 'json',
    'value.format' = 'json'
);

INSERT INTO iot_anomaly_events
SELECT
    device_id,
    sensor_type,
    '3SIGMA' AS anomaly_type,
    value AS anomaly_value,
    avg_val + 3 * std_val AS threshold,
    CASE
        WHEN value > avg_val + 4 * std_val THEN 'CRITICAL'
        WHEN value > avg_val + 3 * std_val THEN 'WARNING'
        ELSE 'INFO'
    END AS severity,
    event_time
FROM (
    SELECT
        r.device_id,
        r.sensor_type,
        r.value,
        r.event_time,
        s.avg_value AS avg_val,
        s.std_value AS std_val
    FROM iot_sensor_raw r
    JOIN iot_sensor_stats s
    ON r.device_id = s.device_id AND r.sensor_type = s.sensor_type
    WHERE r.value > s.avg_value + 3 * s.std_value
      OR r.value < s.avg_value - 3 * s.std_value
);
```

### 4.5 TDengine写入Sink

```python
"""
tdengine_sink.py

Flink Sink: 写入TDengine时序数据库
支持原始数据写入和聚合数据写入
"""
import requests
import json
from datetime import datetime

TDENGINE_HOST = "localhost"
TDENGINE_PORT = 6041
TDENGINE_USER = "root"
TDENGINE_PASSWORD = "taosdata"
TDENGINE_DB = "iot_monitor"


class TDengineWriter:

    def __init__(self):
        self.base_url = f"http://{TDENGINE_HOST}:{TDENGINE_PORT}/rest/sql"
        self.auth = (TDENGINE_USER, TDENGINE_PASSWORD)
        self._init_database()

    def _init_database(self):
        self._execute(f"CREATE DATABASE IF NOT EXISTS {TDENGINE_DB}")
        self._execute(f"USE {TDENGINE_DB}")

    def _execute(self, sql):
        try:
            resp = requests.post(
                self.base_url,
                data=sql.encode('utf-8'),
                auth=self.auth
            )
            return resp.json()
        except Exception as e:
            print(f"TDengine执行失败: {sql}, 错误: {e}")
            return None

    def write_sensor_data(self, readings):
        if not readings:
            return

        sqls = []
        for r in readings:
            ts = r.get('timestamp', 0)
            device_id = r.get('device_id', '')
            sensor_type = r.get('sensor_type', '')
            value = r.get('value', 0)
            factory = r.get('factory', '')
            production_line = r.get('production_line', '')

            table_name = f"s_{device_id}_{sensor_type}".replace('-', '_')
            sql = (
                f"INSERT INTO {table_name} USING {TDENGINE_DB}.sensor_data "
                f"TAGS ('{device_id}', '{sensor_type}', '{factory}', '{production_line}') "
                f"VALUES ({ts}, {value})"
            )
            sqls.append(sql)

        batch_sql = " ".join(sqls)
        self._execute(batch_sql)

    def write_stats_data(self, stats_list):
        if not stats_list:
            return

        sqls = []
        for s in stats_list:
            ts = s.get('window_end', 0)
            device_id = s.get('device_id', '')
            sensor_type = s.get('sensor_type', '')
            avg_val = s.get('avg_value', 0)
            max_val = s.get('max_value', 0)
            min_val = s.get('min_value', 0)
            std_val = s.get('std_value', 0)
            count_val = s.get('count_value', 0)

            table_name = f"st_{device_id}_{sensor_type}".replace('-', '_')
            sql = (
                f"INSERT INTO {table_name} USING {TDENGINE_DB}.sensor_stats_minute "
                f"TAGS ('{device_id}', '{sensor_type}') "
                f"VALUES ({ts}, {avg_val}, {max_val}, {min_val}, {std_val}, {count_val})"
            )
            sqls.append(sql)

        batch_sql = " ".join(sqls)
        self._execute(batch_sql)

    def write_anomaly_event(self, event):
        ts = event.get('event_time', 0)
        device_id = event.get('device_id', '')
        sensor_type = event.get('sensor_type', '')
        anomaly_type = event.get('anomaly_type', '3SIGMA')
        anomaly_value = event.get('anomaly_value', 0)
        threshold = event.get('threshold', 0)
        severity = event.get('severity', 'WARNING')

        table_name = f"a_{device_id}_{sensor_type}".replace('-', '_')
        sql = (
            f"INSERT INTO {table_name} USING {TDengineWriter}.anomaly_events "
            f"TAGS ('{device_id}', '{sensor_type}') "
            f"VALUES ({ts}, '{anomaly_type}', {anomaly_value}, {threshold}, '{severity}')"
        )
        self._execute(sql)

    def query_latest_stats(self, device_id, sensor_type, minutes=60):
        sql = (
            f"SELECT ts, avg_value, max_value, min_value, std_value "
            f"FROM {TDENGINE_DB}.sensor_stats_minute "
            f"WHERE device_id = '{device_id}' AND sensor_type = '{sensor_type}' "
            f"AND ts > NOW - {minutes}m "
            f"ORDER BY ts DESC LIMIT 60"
        )
        result = self._execute(sql)
        if result and result.get('status') == 'succ':
            return result.get('data', [])
        return []

    def query_device_health(self, device_id):
        sql = (
            f"SELECT sensor_type, last(*) as last_value, last_row(ts) as last_ts "
            f"FROM {TDENGINE_DB}.sensor_data "
            f"WHERE device_id = '{device_id}' "
            f"GROUP BY sensor_type"
        )
        result = self._execute(sql)
        if result and result.get('status') == 'succ':
            return result.get('data', [])
        return []
```

---

## 五、阶段3 - 预测性维护（8h）

### 5.1 特征工程

```python
"""
feature_engineering.py

IoT预测性维护 - 特征工程
统计特征 + 频域特征 + 趋势特征
"""
import numpy as np
import pandas as pd
from scipy import signal
from scipy.fft import fft
from datetime import datetime, timedelta


def compute_statistical_features(df, window_size=60):
    features = df.groupby('device_id').rolling(window=window_size, on='timestamp')

    result = df.groupby('device_id').apply(
        lambda g: compute_window_features(g, window_size)
    ).reset_index(drop=True)

    return result


def compute_window_features(group, window_size):
    results = []
    sensor_types = group['sensor_type'].unique()

    for sensor_type in sensor_types:
        sensor_data = group[group['sensor_type'] == sensor_type].sort_values('timestamp')
        values = sensor_data['value'].values

        if len(values) < window_size:
            continue

        for i in range(window_size, len(values) + 1):
            window = values[i - window_size:i]

            feat = {
                'device_id': group['device_id'].iloc[0],
                'sensor_type': sensor_type,
                'timestamp': sensor_data['timestamp'].iloc[i - 1],
                'fault_label': sensor_data['fault_label'].iloc[i - 1],
            }

            feat.update(compute_stat_features(window))
            feat.update(compute_frequency_features(window))
            feat.update(compute_trend_features(window))

            results.append(feat)

    return pd.DataFrame(results) if results else pd.DataFrame()


def compute_stat_features(window):
    return {
        'mean': np.mean(window),
        'std': np.std(window),
        'min': np.min(window),
        'max': np.max(window),
        'range': np.max(window) - np.min(window),
        'median': np.median(window),
        'skewness': float(pd.Series(window).skew()),
        'kurtosis': float(pd.Series(window).kurtosis()),
        'rms': np.sqrt(np.mean(window ** 2)),
        'crest_factor': np.max(np.abs(window)) / np.sqrt(np.mean(window ** 2)) if np.mean(window ** 2) > 0 else 0,
        'zero_crossing_rate': np.sum(np.diff(np.sign(window)) != 0) / len(window),
    }


def compute_frequency_features(window):
    n = len(window)
    yf = fft(window)
    power = np.abs(yf[:n // 2]) ** 2
    freqs = np.fft.fftfreq(n, d=1.0)[:n // 2]

    total_power = np.sum(power)
    if total_power == 0:
        return {
            'dominant_freq': 0,
            'spectral_centroid': 0,
            'spectral_bandwidth': 0,
            'total_power': 0,
            'freq_band_0_5': 0,
            'freq_band_5_15': 0,
            'freq_band_15_plus': 0,
        }

    dominant_idx = np.argmax(power[1:]) + 1
    dominant_freq = abs(freqs[dominant_idx])

    spectral_centroid = np.sum(freqs * power) / total_power
    spectral_bandwidth = np.sqrt(np.sum(((freqs - spectral_centroid) ** 2) * power) / total_power)

    band_0_5 = np.sum(power[(freqs >= 0) & (freqs < 0.05)])
    band_5_15 = np.sum(power[(freqs >= 0.05) & (freqs < 0.15)])
    band_15_plus = np.sum(power[freqs >= 0.15])

    return {
        'dominant_freq': dominant_freq,
        'spectral_centroid': spectral_centroid,
        'spectral_bandwidth': spectral_bandwidth,
        'total_power': total_power,
        'freq_band_0_5': band_0_5,
        'freq_band_5_15': band_5_15,
        'freq_band_15_plus': band_15_plus,
    }


def compute_trend_features(window):
    x = np.arange(len(window))
    y = window

    slope, intercept = np.polyfit(x, y, 1)

    ma_5 = np.mean(window[-5:]) if len(window) >= 5 else np.mean(window)
    ma_10 = np.mean(window[-10:]) if len(window) >= 10 else np.mean(window)
    ma_20 = np.mean(window[-20:]) if len(window) >= 20 else np.mean(window)

    alpha = 0.3
    ema = window[0]
    for val in window[1:]:
        ema = alpha * val + (1 - alpha) * ema

    return {
        'trend_slope': slope,
        'ma_5': ma_5,
        'ma_10': ma_10,
        'ma_20': ma_20,
        'ema': ema,
        'ma_5_ma_20_diff': ma_5 - ma_20,
        'current_vs_ma5': window[-1] - ma_5,
    }


def build_feature_matrix(df):
    all_features = []
    device_ids = df['device_id'].unique()

    for device_id in device_ids:
        device_data = df[df['device_id'] == device_id].sort_values('timestamp')
        device_features = compute_window_features(device_data, window_size=60)

        if not device_features.empty:
            pivot_features = device_features.pivot_table(
                index=['device_id', 'timestamp', 'fault_label'],
                columns='sensor_type',
                aggfunc='first'
            )
            pivot_features.columns = [
                f"{col[1]}_{col[0]}" for col in pivot_features.columns
            ]
            pivot_features = pivot_features.reset_index()
            all_features.append(pivot_features)

    if all_features:
        return pd.concat(all_features, ignore_index=True)
    return pd.DataFrame()
```

### 5.2 XGBoost模型训练

```python
"""
predictive_maintenance_model.py

XGBoost预测性维护模型
预测设备是否会在24小时内故障
"""
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.preprocessing import LabelEncoder
import mlflow
import mlflow.xgboost
import json


def prepare_training_data(feature_df):
    feature_df = feature_df.sort_values('timestamp')
    feature_df['fault_in_24h'] = 0

    device_ids = feature_df['device_id'].unique()
    for device_id in device_ids:
        mask = feature_df['device_id'] == device_id
        device_data = feature_df[mask].copy()
        fault_indices = device_data[device_data['fault_label'] == 1].index

        for fault_idx in fault_indices:
            fault_time = device_data.loc[fault_idx, 'timestamp']
            window_start = fault_time - 24 * 3600 * 1000
            window_mask = (device_data['timestamp'] >= window_start) & (device_data['timestamp'] < fault_time)
            feature_df.loc[device_data[window_mask].index, 'fault_in_24h'] = 1

    drop_cols = ['device_id', 'timestamp', 'fault_label']
    feature_cols = [c for c in feature_df.columns if c not in drop_cols + ['fault_in_24h']]

    X = feature_df[feature_cols].fillna(0).replace([np.inf, -np.inf], 0)
    y = feature_df['fault_in_24h']

    return X, y, feature_cols


def train_xgboost_model(X, y, feature_cols):
    mlflow.set_experiment("iot_predictive_maintenance")

    with mlflow.start_run(run_name="xgboost_fault_prediction"):
        tscv = TimeSeriesSplit(n_splits=5)

        split_idx = int(len(X) * 0.8)
        X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

        scale_pos_weight = (y_train == 0).sum() / max((y_train == 1).sum(), 1)

        params = {
            'objective': 'binary:logistic',
            'eval_metric': ['auc', 'logloss'],
            'max_depth': 6,
            'learning_rate': 0.1,
            'n_estimators': 200,
            'scale_pos_weight': scale_pos_weight,
            'min_child_weight': 5,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'reg_alpha': 0.1,
            'reg_lambda': 1.0,
            'random_state': 42,
        }

        mlflow.log_params(params)

        model = xgb.XGBClassifier(**params)
        model.fit(
            X_train, y_train,
            eval_set=[(X_train, y_train), (X_test, y_test)],
            verbose=50
        )

        y_pred_proba = model.predict_proba(X_test)[:, 1]
        y_pred = (y_pred_proba > 0.5).astype(int)

        auc = roc_auc_score(y_test, y_pred_proba)
        report = classification_report(y_test, y_pred, output_dict=True)

        mlflow.log_metric("auc", auc)
        mlflow.log_metric("precision_1", report['1']['precision'])
        mlflow.log_metric("recall_1", report['1']['recall'])
        mlflow.log_metric("f1_1", report['1']['f1-score'])

        print(f"AUC: {auc:.4f}")
        print(f"\n分类报告:")
        print(classification_report(y_test, y_pred))

        cm = confusion_matrix(y_test, y_pred)
        print(f"混淆矩阵:\n{cm}")

        importance = model.feature_importances_
        feat_importance = sorted(zip(feature_cols, importance), key=lambda x: x[1], reverse=True)
        print(f"\n特征重要性TOP20:")
        for feat, imp in feat_importance[:20]:
            print(f"  {feat}: {imp:.4f}")

        importance_dict = {feat: float(imp) for feat, imp in feat_importance}
        mlflow.log_dict(importance_dict, "feature_importance.json")

        mlflow.xgboost.log_model(model, "xgboost_model")

        model.save_model("iot_fault_model.json")
        print("模型已保存: iot_fault_model.json")

        return model, feature_cols, auc


def optimize_threshold(model, X_test, y_test):
    from sklearn.metrics import precision_recall_curve, f1_score

    y_pred_proba = model.predict_proba(X_test)[:, 1]

    precisions, recalls, thresholds = precision_recall_curve(y_test, y_pred_proba)

    f1_scores = 2 * precisions * recalls / (precisions + recalls + 1e-8)
    best_idx = np.argmax(f1_scores)
    best_threshold = thresholds[best_idx]

    print(f"最优阈值: {best_threshold:.4f}")
    print(f"对应F1: {f1_scores[best_idx]:.4f}")
    print(f"对应精确率: {precisions[best_idx]:.4f}")
    print(f"对应召回率: {recalls[best_idx]:.4f}")

    return best_threshold


if __name__ == '__main__':
    feature_df = pd.read_csv("iot_features.csv")
    X, y, feature_cols = prepare_training_data(feature_df)
    model, feature_cols, auc = train_xgboost_model(X, y, feature_cols)

    split_idx = int(len(X) * 0.8)
    X_test = X.iloc[split_idx:]
    y_test = y.iloc[split_idx:]
    best_threshold = optimize_threshold(model, X_test, y_test)

    with open("model_config.json", "w") as f:
        json.dump({
            "model_path": "iot_fault_model.json",
            "feature_cols": feature_cols,
            "threshold": best_threshold,
            "auc": auc
        }, f, indent=2)
```

### 5.3 实时预测服务

```python
"""
realtime_prediction_service.py

实时预测服务
Flink计算实时特征 → 调用模型API → 预测故障概率
"""
import json
import numpy as np
import xgboost as xgb
from flask import Flask, request, jsonify
import redis

app = Flask(__name__)

model = xgb.XGBClassifier()
model.load_model("iot_fault_model.json")

with open("model_config.json", "r") as f:
    config = json.load(f)

FEATURE_COLS = config['feature_cols']
THRESHOLD = config['threshold']

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
DEVICE_FEATURE_PREFIX = "iot:features:"
DEVICE_PREDICTION_PREFIX = "iot:prediction:"


@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    device_id = data.get('device_id')
    features = data.get('features', {})

    feature_vector = []
    missing_features = []
    for col in FEATURE_COLS:
        if col in features:
            val = features[col]
            if val is None or (isinstance(val, float) and (np.isnan(val) or np.isinf(val))):
                feature_vector.append(0.0)
            else:
                feature_vector.append(float(val))
        else:
            feature_vector.append(0.0)
            missing_features.append(col)

    X = np.array([feature_vector])
    fault_probability = float(model.predict_proba(X)[0][1])
    predicted_fault = 1 if fault_probability > THRESHOLD else 0

    result = {
        'device_id': device_id,
        'fault_probability': round(fault_probability, 4),
        'predicted_fault': predicted_fault,
        'threshold': THRESHOLD,
        'confidence': round(max(fault_probability, 1 - fault_probability), 4),
        'missing_features': missing_features[:5]
    }

    key = f"{DEVICE_PREDICTION_PREFIX}{device_id}"
    r.hset(key, mapping={
        'fault_probability': str(result['fault_probability']),
        'predicted_fault': str(result['predicted_fault']),
        'confidence': str(result['confidence']),
    })
    r.expire(key, 3600)

    if fault_probability > 0.7:
        result['alert'] = 'HIGH_RISK'
    elif fault_probability > 0.5:
        result['alert'] = 'MEDIUM_RISK'
    else:
        result['alert'] = 'LOW_RISK'

    return jsonify(result)


@app.route('/batch_predict', methods=['POST'])
def batch_predict():
    data_list = request.json
    results = []

    feature_matrix = []
    device_ids = []

    for data in data_list:
        device_id = data.get('device_id')
        features = data.get('features', {})
        device_ids.append(device_id)

        feature_vector = []
        for col in FEATURE_COLS:
            val = features.get(col, 0.0)
            if val is None or (isinstance(val, float) and (np.isnan(val) or np.isinf(val))):
                feature_vector.append(0.0)
            else:
                feature_vector.append(float(val))
        feature_matrix.append(feature_vector)

    X = np.array(feature_matrix)
    probabilities = model.predict_proba(X)[:, 1]

    for i, device_id in enumerate(device_ids):
        prob = float(probabilities[i])
        results.append({
            'device_id': device_id,
            'fault_probability': round(prob, 4),
            'predicted_fault': 1 if prob > THRESHOLD else 0,
            'alert': 'HIGH_RISK' if prob > 0.7 else ('MEDIUM_RISK' if prob > 0.5 else 'LOW_RISK')
        })

    return jsonify(results)


@app.route('/device_status/<device_id>', methods=['GET'])
def device_status(device_id):
    pred_key = f"{DEVICE_PREDICTION_PREFIX}{device_id}"
    pred_data = r.hgetall(pred_key)

    feat_key = f"{DEVICE_FEATURE_PREFIX}{device_id}"
    feat_data = r.hgetall(feat_key)

    return jsonify({
        'device_id': device_id,
        'prediction': pred_data,
        'latest_features': feat_data
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
```

---

## 六、阶段4 - 监控与告警（5h）

### 6.1 Grafana设备监控大屏

```json
{
  "dashboard": {
    "title": "IoT设备监控与预测性维护",
    "refresh": "5s",
    "panels": [
      {
        "title": "设备状态总览",
        "type": "piechart",
        "targets": [{
          "rawSql": "SELECT status, count() AS cnt FROM devices GROUP BY status",
          "format": "table"
        }]
      },
      {
        "title": "异常设备数",
        "type": "stat",
        "targets": [{
          "rawSql": "SELECT count(DISTINCT device_id) AS anomaly_count FROM anomaly_events WHERE ts > NOW - 1h",
          "format": "table"
        }],
        "fieldConfig": {
          "defaults": {
            "color": {"mode": "thresholds"},
            "thresholds": {
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 5},
                {"color": "red", "value": 20}
              ]
            }
          }
        }
      },
      {
        "title": "实时传感器曲线（温度）",
        "type": "timeseries",
        "targets": [{
          "rawSql": "SELECT ts, avg_value, max_value, min_value FROM sensor_stats_minute WHERE sensor_type = 'temperature' AND device_id = 'DEV_000001' AND ts > NOW - 1h ORDER BY ts",
          "format": "time_series"
        }]
      },
      {
        "title": "振动频谱",
        "type": "timeseries",
        "targets": [{
          "rawSql": "SELECT ts, avg_value, max_value FROM sensor_stats_minute WHERE sensor_type = 'vibration' AND ts > NOW - 1h ORDER BY ts",
          "format": "time_series"
        }]
      },
      {
        "title": "故障预测概率趋势",
        "type": "gauge",
        "targets": [{
          "rawSql": "SELECT avg(fault_probability) AS avg_prob FROM prediction_results WHERE ts > NOW - 5m",
          "format": "table"
        }],
        "fieldConfig": {
          "defaults": {
            "unit": "percentunit",
            "min": 0,
            "max": 1,
            "thresholds": {
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 0.5},
                {"color": "red", "value": 0.7}
              ]
            }
          }
        }
      },
      {
        "title": "设备健康度排名",
        "type": "bargauge",
        "targets": [{
          "rawSql": "SELECT device_id, 1 - avg(fault_probability) AS health_score FROM prediction_results WHERE ts > NOW - 1h GROUP BY device_id ORDER BY health_score ASC LIMIT 20",
          "format": "table"
        }],
        "fieldConfig": {
          "defaults": {
            "min": 0,
            "max": 1,
            "thresholds": {
              "steps": [
                {"color": "red", "value": null},
                {"color": "yellow", "value": 0.5},
                {"color": "green", "value": 0.8}
              ]
            }
          }
        }
      },
      {
        "title": "异常事件列表",
        "type": "table",
        "targets": [{
          "rawSql": "SELECT ts, device_id, sensor_type, anomaly_type, anomaly_value, threshold, severity FROM anomaly_events WHERE ts > NOW - 1h ORDER BY ts DESC LIMIT 50",
          "format": "table"
        }]
      },
      {
        "title": "各工厂异常分布",
        "type": "barchart",
        "targets": [{
          "rawSql": "SELECT d.factory, count() AS anomaly_count FROM anomaly_events a JOIN devices d ON a.device_id = d.device_id WHERE a.ts > NOW - 1h GROUP BY d.factory ORDER BY anomaly_count DESC",
          "format": "table"
        }]
      }
    ]
  }
}
```

### 6.2 告警服务

```python
"""
alert_service.py

IoT告警服务
传感器超阈值 → 实时告警
故障预测概率>0.7 → 预警通知
设备离线 → 紧急告警
"""
import json
import time
import redis
import requests
from datetime import datetime
from threading import Thread

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

ALERT_PREFIX = "iot:alert:"
DEVICE_ONLINE_PREFIX = "iot:online:"
PREDICTION_PREFIX = "iot:prediction:"

ALERT_LEVELS = {
    'INFO': 0,
    'WARNING': 1,
    'CRITICAL': 2,
    'EMERGENCY': 3
}

THRESHOLD_CONFIG = {
    'temperature': {'warning': 90, 'critical': 110},
    'vibration': {'warning': 8.0, 'critical': 12.0},
    'current': {'warning': 80, 'critical': 100},
    'pressure': {'warning': 2.5, 'critical': 3.5},
    'pressure_in': {'warning': 0.9, 'critical': 1.2},
    'pressure_out': {'warning': 3.5, 'critical': 4.5},
}


def check_sensor_threshold(device_id, sensor_type, value):
    if sensor_type not in THRESHOLD_CONFIG:
        return None

    thresholds = THRESHOLD_CONFIG[sensor_type]

    if value >= thresholds['critical']:
        return create_alert(
            device_id=device_id,
            alert_type='SENSOR_CRITICAL',
            level='CRITICAL',
            message=f"设备{device_id}的{sensor_type}值{value}超过严重阈值{thresholds['critical']}",
            value=value,
            threshold=thresholds['critical']
        )
    elif value >= thresholds['warning']:
        return create_alert(
            device_id=device_id,
            alert_type='SENSOR_WARNING',
            level='WARNING',
            message=f"设备{device_id}的{sensor_type}值{value}超过警告阈值{thresholds['warning']}",
            value=value,
            threshold=thresholds['warning']
        )
    return None


def check_prediction_alert(device_id):
    key = f"{PREDICTION_PREFIX}{device_id}"
    data = r.hgetall(key)
    if not data:
        return None

    fault_prob = float(data.get('fault_probability', 0))

    if fault_prob > 0.7:
        return create_alert(
            device_id=device_id,
            alert_type='PREDICTION_HIGH_RISK',
            level='CRITICAL',
            message=f"设备{device_id}预测故障概率{fault_prob:.1%}，超过0.7阈值",
            value=fault_prob,
            threshold=0.7
        )
    elif fault_prob > 0.5:
        return create_alert(
            device_id=device_id,
            alert_type='PREDICTION_MEDIUM_RISK',
            level='WARNING',
            message=f"设备{device_id}预测故障概率{fault_prob:.1%}，超过0.5阈值",
            value=fault_prob,
            threshold=0.5
        )
    return None


def check_device_online(device_id, timeout_seconds=300):
    key = f"{DEVICE_ONLINE_PREFIX}{device_id}"
    last_heartbeat = r.get(key)

    if last_heartbeat is None:
        return create_alert(
            device_id=device_id,
            alert_type='DEVICE_OFFLINE',
            level='EMERGENCY',
            message=f"设备{device_id}离线，无心跳数据",
            value=0,
            threshold=timeout_seconds
        )

    elapsed = time.time() - float(last_heartbeat)
    if elapsed > timeout_seconds:
        return create_alert(
            device_id=device_id,
            alert_type='DEVICE_TIMEOUT',
            level='EMERGENCY',
            message=f"设备{device_id}超时{elapsed:.0f}秒未上报数据",
            value=elapsed,
            threshold=timeout_seconds
        )
    return None


def create_alert(device_id, alert_type, level, message, value, threshold):
    alert = {
        'device_id': device_id,
        'alert_type': alert_type,
        'level': level,
        'message': message,
        'value': value,
        'threshold': threshold,
        'timestamp': datetime.now().isoformat(),
        'acknowledged': False
    }

    alert_key = f"{ALERT_PREFIX}{device_id}:{alert_type}"
    r.setex(alert_key, 3600, json.dumps(alert, ensure_ascii=False))

    r.publish(f"iot:alerts:{level.lower()}", json.dumps(alert, ensure_ascii=False))

    print(f"[{level}] {message}")
    return alert


def update_device_heartbeat(device_id):
    key = f"{DEVICE_ONLINE_PREFIX}{device_id}"
    r.setex(key, 600, str(time.time()))


def alert_monitor_loop():
    pubsub = r.pubsub()
    pubsub.subscribe('iot:alerts:emergency', 'iot:alerts:critical')

    print("告警监控已启动...")
    for message in pubsub.listen():
        if message['type'] == 'message':
            alert = json.loads(message['data'])
            handle_emergency_alert(alert)


def handle_emergency_alert(alert):
    print(f"紧急告警处理: {alert['message']}")
    print(f"  设备: {alert['device_id']}")
    print(f"  类型: {alert['alert_type']}")
    print(f"  值: {alert['value']}, 阈值: {alert['threshold']}")


if __name__ == '__main__':
    monitor_thread = Thread(target=alert_monitor_loop, daemon=True)
    monitor_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("告警服务已停止")
```

### 6.3 Docker Compose部署

```yaml
# docker-compose-iot-monitor.yml
version: '3.8'

services:
  emqx:
    image: emqx/emqx:5.4
    ports:
      - "1883:1883"
      - "8083:8083"
      - "18083:18083"
    environment:
      EMQX_LOADED_PLUGINS: "emqx_management"
    volumes:
      - emqx_data:/opt/emqx/data

  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1

  mysql:
    image: mysql:8.0
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: root123
      MYSQL_DATABASE: iot_monitor
    volumes:
      - ./sql:/docker-entrypoint-initdb.d

  redis:
    image: redis:7.2
    ports:
      - "6379:6379"
    command: redis-server --maxmemory 2gb --maxmemory-policy allkeys-lru

  tdengine:
    image: tdengine/tdengine:3.2
    ports:
      - "6030:6030"
      - "6041:6041"
    environment:
      TAOS_FQDN: "tdengine"
    volumes:
      - tdengine_data:/var/lib/taos

  flink-jobmanager:
    image: flink:1.17.1-scala_2.12
    ports:
      - "8081:8081"
    command: jobmanager
    environment:
      - JOB_MANAGER_RPC_ADDRESS=flink-jobmanager

  flink-taskmanager:
    image: flink:1.17.1-scala_2.12
    depends_on:
      - flink-jobmanager
    command: taskmanager
    environment:
      - JOB_MANAGER_RPC_ADDRESS=flink-jobmanager
    deploy:
      replicas: 3

  mlflow:
    image: ghcr.io/mlflow/mlflow:v2.9.2
    ports:
      - "5001:5000"
    environment:
      MLFLOW_BACKEND_STORE_URI: sqlite:///mlflow.db
      MLFLOW_DEFAULT_ARTIFACT_ROOT: /mlflow/artifacts
    volumes:
      - mlflow_data:/mlflow

  prediction-service:
    build:
      context: ./prediction_service
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    depends_on:
      - redis
      - mlflow

  grafana:
    image: grafana/grafana:10.1
    ports:
      - "3000:3000"
    environment:
      GF_INSTALL_PLUGINS: volkovlabs-tdengine-datasource
    volumes:
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./grafana/datasources:/etc/grafana/provisioning/datasources

volumes:
  emqx_data:
  tdengine_data:
  mlflow_data:
```

---

## 七、验收标准

| 验收项 | 标准 | 验证方法 |
|--------|------|----------|
| 数据模拟 | 1000台设备每秒10000条数据 | MQTT客户端订阅验证 |
| MQTT→Kafka | 数据转发延迟 < 1秒 | Kafka Consumer时间戳对比 |
| Flink处理 | 清洗+聚合+异常检测延迟 < 3秒 | Flink UI Metrics |
| TDengine | 写入吞吐 > 10000条/秒 | taosBenchmark |
| 预测模型 | AUC > 0.85, F1 > 0.80 | MLflow实验记录 |
| 实时预测 | 预测API响应 < 100ms | 压测工具 |
| 告警 | 阈值告警+预测告警+离线告警 | 手动触发验证 |
| Grafana | 8个面板实时刷新 | 目视检查 |

---

## 八、交付物清单

| 序号 | 交付物 | 文件 | 要求 |
|------|--------|------|------|
| 1 | IoT数据模拟器 | `iot_data_simulator.py` | 1000设备+10传感器+异常模式 |
| 2 | MQTT+Kafka+Flink管道 | `IoTPipeline.java` | 清洗+聚合+异常检测 |
| 3 | Flink SQL处理 | `iot_pipeline_sql.sql` | 窗口聚合+3-Sigma检测 |
| 4 | TDengine建表 | `tdengine_ddl.sql` | 超级表+子表设计 |
| 5 | TDengine写入Sink | `tdengine_sink.py` | 批量写入+查询接口 |
| 6 | 特征工程 | `feature_engineering.py` | 统计+频域+趋势特征 |
| 7 | 预测模型 | `predictive_maintenance_model.py` | XGBoost+MLflow+阈值优化 |
| 8 | 实时预测服务 | `realtime_prediction_service.py` | Flask API+Redis缓存 |
| 9 | 告警服务 | `alert_service.py` | 三级告警+Redis Pub/Sub |
| 10 | Grafana Dashboard | `iot_monitor_dashboard.json` | 8面板监控大屏 |
| 11 | Docker Compose | `docker-compose-iot-monitor.yml` | 一键启动全栈环境 |

---

## 九、评分标准

| 评分项 | 权重 | 要求 |
|--------|------|------|
| 数据模拟 | 10% | 模拟器可运行，正常+异常+故障模式完整 |
| 时序管道 | 25% | MQTT→Kafka→Flink→TDengine全链路通畅 |
| 特征工程 | 15% | 统计+频域+趋势三类特征完整实现 |
| 预测模型 | 20% | XGBoost AUC>0.85，MLflow追踪完整 |
| 监控告警 | 20% | Grafana大屏+三级告警全部实现 |
| 代码质量 | 10% | 代码规范，异常处理完善，可复现 |
