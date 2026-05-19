# 课时31：Spark与Flink on K8s

> **所属阶段**：L3 高级工程师 | **模块**：补充模块_云原生大数据 | **课时**：3h | **难度**：★★★★★

---

## 一、教学目标

1. 掌握Spark on K8s的两种提交模式（cluster/client），理解Driver/Executor Pod生命周期
2. 能够使用Spark Operator管理Spark作业，编写SparkApplication CRD
3. 掌握Flink on K8s的Application/Session模式，使用Flink Operator部署流处理任务
4. 能够使用Strimzi Operator部署和管理Kafka集群
5. 理解K8s存储与网络在大数据场景下的最佳实践
6. 掌握生产级监控、日志和弹性伸缩方案

---

## 二、Spark on Kubernetes

### 2.1 提交模式

```
Spark on K8s两种提交模式:

  模式1: Cluster模式（推荐）
  ┌──────────────────────────────────────────────────────────────┐
  │                                                              │
  │  用户机器                                                    │
  │  ┌──────────────┐                                           │
  │  │ spark-submit │ ──提交请求──→ K8s API Server              │
  │  └──────────────┘                                           │
  │                                                              │
  │  K8s集群                                                     │
  │  ┌──────────────────────────────────────────────────────┐   │
  │  │  Driver Pod                                           │   │
  │  │  ┌──────────────────────────────────────────────┐    │   │
  │  │  │  SparkContext                                │    │   │
  │  │  │  ├── 请求Executor资源                        │    │   │
  │  │  │  ├── 任务调度与分发                          │    │   │
  │  │  │  └── 结果收集与写回                          │    │   │
  │  │  └──────────────────────────────────────────────┘    │   │
  │  │         │                                              │   │
  │  │         │ 创建                                         │   │
  │  │         ▼                                              │   │
  │  │  Executor Pod-1    Executor Pod-2    Executor Pod-3   │   │
  │  │  ┌──────────┐    ┌──────────┐    ┌──────────┐       │   │
  │  │  │ TaskSet  │    │ TaskSet  │    │ TaskSet  │       │   │
  │  │  │ Shuffle  │    │ Shuffle  │    │ Shuffle  │       │   │
  │  │  └──────────┘    └──────────┘    └──────────┘       │   │
  │  └──────────────────────────────────────────────────────┘   │
  │                                                              │
  │  特点: Driver在K8s内运行，用户提交后可断开                    │
  └──────────────────────────────────────────────────────────────┘

  模式2: Client模式
  ┌──────────────────────────────────────────────────────────────┐
  │                                                              │
  │  用户机器                                                    │
  │  ┌──────────────────────────────────────────────┐           │
  │  │  Driver (本地JVM进程)                         │           │
  │  │  SparkContext                                │           │
  │  │  └── 请求Executor资源 ──→ K8s API Server     │           │
  │  └──────────────────────────────────────────────┘           │
  │                        │                                     │
  │  K8s集群               │ 创建                               │
  │  ┌─────────────────────▼──────────────────────────────┐    │
  │  │  Executor Pod-1    Executor Pod-2    Executor Pod-3│    │
  │  └────────────────────────────────────────────────────┘    │
  │                                                              │
  │  特点: Driver在用户机器运行，需保持网络连接                    │
  │  适合: 交互式调试、Jupyter Notebook                          │
  └──────────────────────────────────────────────────────────────┘
```

### 2.2 spark-submit提交作业

```bash
spark-submit \
  --master k8s://https://$(kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}') \
  --deploy-mode cluster \
  --name spark-etl-orders \
  --class com.bigdata.etl.OrderETLJob \
  --conf spark.kubernetes.container.image=your-registry/spark:3.5.0 \
  --conf spark.kubernetes.container.image.pullPolicy=Always \
  --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
  --conf spark.kubernetes.namespace=bigdata \
  --conf spark.driver.cores=2 \
  --conf spark.driver.memory=4g \
  --conf spark.driver.memoryOverhead=1g \
  --conf spark.executor.cores=2 \
  --conf spark.executor.memory=4g \
  --conf spark.executor.memoryOverhead=1g \
  --conf spark.executor.instances=4 \
  --conf spark.dynamicAllocation.enabled=true \
  --conf spark.dynamicAllocation.minExecutors=2 \
  --conf spark.dynamicAllocation.maxExecutors=10 \
  --conf spark.dynamicAllocation.shuffleTracking.enabled=true \
  --conf spark.kubernetes.executor.deleteOnTermination=true \
  --conf spark.kubernetes.driver.pod.name=spark-etl-orders-driver \
  --conf spark.kubernetes.driver.label.app=spark-etl \
  --conf spark.kubernetes.driver.label.env=production \
  --conf spark.kubernetes.executor.label.app=spark-etl \
  --conf spark.kubernetes.executor.label.env=production \
  --conf spark.hadoop.fs.s3a.endpoint=http://minio.bigdata.svc:9000 \
  --conf spark.hadoop.fs.s3a.access.key=admin \
  --conf spark.hadoop.fs.s3a.secret.key=admin123456 \
  --conf spark.hadoop.fs.s3a.path.style.access=true \
  --conf spark.sql.catalog.iceberg=org.apache.iceberg.spark.SparkCatalog \
  --conf spark.sql.catalog.iceberg.type=hive \
  --conf spark.sql.catalog.iceberg.uri=thrift://hive-metastore.bigdata.svc:9083 \
  --conf spark.sql.catalog.iceberg.warehouse=s3a://warehouse/iceberg \
  --conf spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions \
  https://your-registry/spark-jobs/etl-job-1.0.0.jar
```

#### 自定义Spark镜像

```dockerfile
FROM spark:3.5.0

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir \
    pyspark==3.5.0 \
    iceberg-py==0.7.0

ADD https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.5_2.12/1.5.0/iceberg-spark-runtime-3.5_2.12-1.5.0.jar /opt/spark/jars/
ADD https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar /opt/spark/jars/
ADD https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar /opt/spark/jars/
ADD https://repo1.maven.org/maven2/org/apache/hive/hive-metastore-client-standalone/3.1.3/hive-metastore-client-standalone-3.1.3.jar /opt/spark/jars/

WORKDIR /opt/spark
```

### 2.3 Spark Operator

#### 安装Spark Operator

```bash
helm repo add spark-operator https://kubeflow.github.io/spark-operator
helm repo update

helm install spark-operator spark-operator/spark-operator \
  --namespace spark-operator \
  --create-namespace \
  --set image.repository=kubeflow/spark-operator \
  --set image.tag=v1beta2-1.6.2-3.5.0 \
  --set serviceAccounts.spark.create=true \
  --set serviceAccounts.spark.name=spark \
  --set webhook.enable=true
```

#### SparkApplication CRD

```yaml
apiVersion: sparkoperator.k8s.io/v1beta2
kind: SparkApplication
metadata:
  name: spark-etl-orders
  namespace: bigdata
spec:
  type: Scala
  mode: cluster
  image: "your-registry/spark:3.5.0-iceberg"
  imagePullPolicy: Always
  mainClass: com.bigdata.etl.OrderETLJob
  mainApplicationFile: "s3a://spark-jars/etl-job-1.0.0.jar"
  sparkVersion: "3.5.0"
  restartPolicy:
    type: OnFailure
    onFailureRetries: 3
    onFailureRetryInterval: 30
    onSubmissionFailureRetries: 2
    onSubmissionFailureRetryInterval: 60
  driver:
    cores: 2
    memory: "4g"
    memoryOverhead: "1g"
    serviceAccount: spark
    labels:
      app: spark-etl
      env: production
    env:
    - name: S3_ENDPOINT
      value: "http://minio.bigdata.svc:9000"
    envFrom:
    - secretRef:
        name: minio-secret
    volumeMounts:
    - name: spark-events
      mountPath: /tmp/spark-events
  executor:
    cores: 2
    memory: "4g"
    memoryOverhead: "1g"
    instances: 4
    labels:
      app: spark-etl
      env: production
    env:
    - name: S3_ENDPOINT
      value: "http://minio.bigdata.svc:9000"
    envFrom:
    - secretRef:
        name: minio-secret
  dynamicAllocation:
    enabled: true
    minExecutors: 2
    maxExecutors: 10
    shuffleTrackingTimeout: 300000
  deps:
    packages:
    - org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.0
    - org.apache.hadoop:hadoop-aws:3.3.4
  hadoopConf:
    fs.s3a.endpoint: "http://minio.bigdata.svc:9000"
    fs.s3a.access.key: "admin"
    fs.s3a.secret.key: "admin123456"
    fs.s3a.path.style.access: "true"
  sparkConf:
    spark.sql.catalog.iceberg: "org.apache.iceberg.spark.SparkCatalog"
    spark.sql.catalog.iceberg.type: "hive"
    spark.sql.catalog.iceberg.uri: "thrift://hive-metastore.bigdata.svc:9083"
    spark.sql.catalog.iceberg.warehouse: "s3a://warehouse/iceberg"
    spark.sql.extensions: "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions"
    spark.eventLog.enabled: "true"
    spark.eventLog.dir: "s3a://spark-events"
  volumes:
  - name: spark-events
    persistentVolumeClaim:
      claimName: spark-events-pvc
```

#### SparkApplication Python版

```yaml
apiVersion: sparkoperator.k8s.io/v1beta2
kind: SparkApplication
metadata:
  name: spark-py-wordcount
  namespace: bigdata
spec:
  type: Python
  mode: cluster
  image: "your-registry/spark-py:3.5.0"
  imagePullPolicy: Always
  mainApplicationFile: "s3a://spark-jobs/wordcount.py"
  sparkVersion: "3.5.0"
  restartPolicy:
    type: OnFailure
    onFailureRetries: 3
  driver:
    cores: 1
    memory: "1g"
    serviceAccount: spark
    labels:
      app: spark-wordcount
  executor:
    cores: 1
    memory: "2g"
    instances: 2
    labels:
      app: spark-wordcount
  hadoopConf:
    fs.s3a.endpoint: "http://minio.bigdata.svc:9000"
    fs.s3a.access.key: "admin"
    fs.s3a.secret.key: "admin123456"
    fs.s3a.path.style.access: "true"
```

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("WordCount") \
    .getOrCreate()

data = ["hello spark", "hello kubernetes", "hello big data", "spark on k8s"]

df = spark.createDataFrame([(s,) for s in data], ["text"])

from pyspark.sql.functions import explode, split, lower, col

words = df.select(explode(split(lower(col("text")), " ")).alias("word"))
counts = words.groupBy("word").count().orderBy(col("count").desc())
counts.show()

spark.stop()
```

#### SparkApplication管理命令

```bash
kubectl apply -f spark-etl-orders.yaml

kubectl get sparkapplications -n bigdata

kubectl describe sparkapplication spark-etl-orders -n bigdata

kubectl get pods -n bigdata -l sparkapp=spark-etl-orders

kubectl logs -n bigdata spark-etl-orders-driver --tail=50

kubectl delete sparkapplication spark-etl-orders -n bigdata

kubectl patch sparkapplication spark-etl-orders -n bigdata --type merge -p '{"spec":{"executor":{"instances":6}}}'
```

---

## 三、Flink on Kubernetes

### 3.1 部署模式

```
Flink on K8s两种部署模式:

  模式1: Application模式（推荐生产使用）
  ┌──────────────────────────────────────────────────────────┐
  │  一个Flink Application = 一个K8s Deployment               │
  │                                                          │
  │  ┌──────────────────────────────────────────────────┐   │
  │  │  Flink Cluster (专属于一个Job)                     │   │
  │  │                                                    │   │
  │  │  ┌──────────┐   ┌──────────┐   ┌──────────┐    │   │
  │  │  │JobManager│   │TaskManager│   │TaskManager│    │   │
  │  │  │  Pod     │   │  Pod-1   │   │  Pod-2   │    │   │
  │  │  └──────────┘   └──────────┘   └──────────┘    │   │
  │  └──────────────────────────────────────────────────┘   │
  │                                                          │
  │  优点: 资源隔离、独立配置、Job失败不影响其他Job           │
  │  缺点: 每个Job一套集群，资源开销大                       │
  └──────────────────────────────────────────────────────────┘

  模式2: Session模式
  ┌──────────────────────────────────────────────────────────┐
  │  多个Flink Job共享一个Flink Cluster                       │
  │                                                          │
  │  ┌──────────────────────────────────────────────────┐   │
  │  │  Flink Session Cluster (共享)                      │   │
  │  │                                                    │   │
  │  │  ┌──────────┐   ┌──────────┐   ┌──────────┐    │   │
  │  │  │JobManager│   │TaskManager│   │TaskManager│    │   │
  │  │  │  Pod     │   │  Pod-1   │   │  Pod-2   │    │   │
  │  │  └──────────┘   └──────────┘   └──────────┘    │   │
  │  │       ▲                                           │   │
  │  │       │ 提交                                      │   │
  │  │  ┌────┴────┐  ┌─────────┐  ┌─────────┐         │   │
  │  │  │ Job A   │  │ Job B   │  │ Job C   │         │   │
  │  │  └─────────┘  └─────────┘  └─────────┘         │   │
  │  └──────────────────────────────────────────────────┘   │
  │                                                          │
  │  优点: 资源共享、启动快、适合短作业                      │
  │  缺点: Job间资源竞争、一个Job崩溃可能影响其他Job          │
  └──────────────────────────────────────────────────────────┘
```

### 3.2 Flink Operator

#### 安装Flink Operator

```bash
helm repo add flink-operator-repo https://downloads.apache.org/flink/flink-kubernetes-operator-1.7.0/
helm repo update

kubectl create namespace flink-operator

helm install flink-kubernetes-operator flink-operator-repo/flink-kubernetes-operator \
  --namespace flink-operator
```

#### FlinkDeployment CRD（Application模式）

```yaml
apiVersion: flink.apache.org/v1beta1
kind: FlinkDeployment
metadata:
  name: order-stats-job
  namespace: bigdata
spec:
  image: flink:1.18.0-java17
  flinkVersion: v1_18
  serviceAccount: flink
  mode: native
  ingress:
    template: "flink-job/{{namespace}}/{{name}}(/|$)(.*)"
    className: "nginx"
    annotations:
      nginx.ingress.kubernetes.io/rewrite-target: "/$2"
  flinkConfiguration:
    taskmanager.numberOfTaskSlots: "2"
    state.backend: rocksdb
    state.backend.rocksdb.localdir: /data/rocksdb
    state.checkpoints.dir: s3://flink-checkpoints/order-stats
    state.savepoints.dir: s3://flink-savepoints/order-stats
    execution.checkpointing.interval: 60000
    execution.checkpointing.mode: EXACTLY_ONCE
    execution.checkpointing.timeout: 600000
    restart-strategy: fixed-delay
    restart-strategy.fixed-delay.attempts: 3
    restart-strategy.fixed-delay.delay: 30s
    s3.endpoint: http://minio.bigdata.svc:9000
    s3.path.style.access: "true"
    s3.access.key: admin
    s3.secret.key: admin123456
  podTemplate:
    apiVersion: v1
    kind: Pod
    spec:
      containers:
      - name: flink-main-container
        volumeMounts:
        - name: flink-data
          mountPath: /data
      volumes:
      - name: flink-data
        persistentVolumeClaim:
          claimName: flink-data-pvc
  job:
    jarURI: s3://flink-jobs/order-stats-job.jar
    parallelism: 4
    upgradeMode: savepoint
    state: running
    args: ["--bootstrap.servers", "kafka-cluster.bigdata.svc:9092",
           "--topic", "orders",
           "--s3.endpoint", "http://minio.bigdata.svc:9000",
           "--iceberg.warehouse", "s3a://warehouse/iceberg"]
  jobManager:
    resource:
      memory: "2048m"
      cpu: 1
  taskManager:
    resource:
      memory: "4096m"
      cpu: 2
```

#### FlinkDeployment CRD（Session模式）

```yaml
apiVersion: flink.apache.org/v1beta1
kind: FlinkDeployment
metadata:
  name: flink-session-cluster
  namespace: bigdata
spec:
  image: flink:1.18.0-java17
  flinkVersion: v1_18
  serviceAccount: flink
  mode: native
  flinkConfiguration:
    taskmanager.numberOfTaskSlots: "4"
    state.backend: rocksdb
    state.checkpoints.dir: s3://flink-checkpoints/session
    state.savepoints.dir: s3://flink-savepoints/session
    s3.endpoint: http://minio.bigdata.svc:9000
    s3.path.style.access: "true"
    s3.access.key: admin
    s3.secret.key: admin123456
  jobManager:
    resource:
      memory: "4096m"
      cpu: 2
  taskManager:
    resource:
      memory: "8192m"
      cpu: 4
  podTemplate:
    apiVersion: v1
    kind: Pod
    spec:
      containers:
      - name: flink-main-container
        volumeMounts:
        - name: flink-data
          mountPath: /data
      volumes:
      - name: flink-data
        persistentVolumeClaim:
          claimName: flink-data-pvc
```

#### FlinkSessionJob CRD

```yaml
apiVersion: flink.apache.org/v1beta1
kind: FlinkSessionJob
metadata:
  name: realtime-aggregation
  namespace: bigdata
spec:
  deploymentName: flink-session-cluster
  job:
    jarURI: s3://flink-jobs/realtime-aggregation.jar
    parallelism: 4
    upgradeMode: savepoint
    state: running
    args: ["--bootstrap.servers", "kafka-cluster.bigdata.svc:9092",
           "--input-topic", "user-events",
           "--output-topic", "aggregated-stats"]
```

#### FlinkDeployment管理命令

```bash
kubectl apply -f flink-deployment-order-stats.yaml

kubectl get flinkdeployment -n bigdata

kubectl describe flinkdeployment order-stats-job -n bigdata

kubectl get pods -n bigdata -l app=order-stats-job

kubectl logs -n bigdata -l app=order-stats-job,component=jobmanager --tail=50

kubectl get flinksessionjob -n bigdata

kubectl patch flinkdeployment order-stats-job -n bigdata --type merge -p \
  '{"spec":{"job":{"state":"suspended"}}}'

kubectl patch flinkdeployment order-stats-job -n bigdata --type merge -p \
  '{"spec":{"job":{"state":"running"}}}'

kubectl delete flinkdeployment order-stats-job -n bigdata
```

---

## 四、Kafka on Kubernetes（Strimzi Operator）

### 4.1 Strimzi Operator架构

```
Strimzi Operator架构:

  ┌──────────────────────────────────────────────────────────────┐
  │                    Strimzi Operator                           │
  │                                                              │
  │  ┌──────────────────────────────────────────────────────┐   │
  │  │  Cluster Operator                                     │   │
  │  │  - 监听Kafka/KafkaConnect CRD变更                     │   │
  │  │  - 创建/更新StatefulSet/Service/ConfigMap             │   │
  │  │  - 管理滚动升级                                       │   │
  │  └──────────────────────────────────────────────────────┘   │
  │                                                              │
  │  ┌──────────────────────────────────────────────────────┐   │
  │  │  Topic Operator                                       │   │
  │  │  - 监听KafkaTopic CRD变更                             │   │
  │  │  - 同步K8s Topic资源与Kafka Broker                    │   │
  │  └──────────────────────────────────────────────────────┘   │
  │                                                              │
  │  ┌──────────────────────────────────────────────────────┐   │
  │  │  User Operator                                        │   │
  │  │  - 监听KafkaUser CRD变更                              │   │
  │  │  - 管理Kafka用户认证和授权                            │   │
  │  └──────────────────────────────────────────────────────┘   │
  └──────────────────────────────────────────────────────────────┘
```

### 4.2 安装Strimzi Operator

```bash
helm repo add strimzi https://strimzi.io/charts/
helm repo update

helm install strimzi-kafka strimzi/strimzi-kafka-operator \
  --namespace kafka \
  --create-namespace \
  --set watchAnyNamespace=true
```

### 4.3 Kafka集群部署

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: kafka-cluster
  namespace: bigdata
spec:
  kafka:
    version: 3.6.0
    replicas: 3
    listeners:
    - name: plain
      port: 9092
      type: internal
      tls: false
    - name: tls
      port: 9093
      type: internal
      tls: true
      authentication:
        type: tls
    - name: external
      port: 9094
      type: nodeport
      tls: false
    config:
      offsets.topic.replication.factor: 3
      transaction.state.log.replication.factor: 3
      transaction.state.log.min.isr: 2
      default.replication.factor: 3
      min.insync.replicas: 2
      log.retention.hours: 168
      log.segment.bytes: 1073741824
      num.network.threads: 8
      num.io.threads: 8
      socket.send.buffer.bytes: 102400
      socket.receive.buffer.bytes: 102400
      socket.request.max.bytes: 104857600
      auto.create.topics.enable: "false"
    resources:
      requests:
        cpu: "1"
        memory: 2Gi
      limits:
        cpu: "2"
        memory: 4Gi
    storage:
      type: persistent-claim
      size: 100Gi
      storageClassName: local-storage
      deleteClaim: false
    livenessProbe:
      initialDelaySeconds: 60
      timeoutSeconds: 10
    readinessProbe:
      initialDelaySeconds: 30
      timeoutSeconds: 10
    template:
      pod:
        affinity:
          podAntiAffinity:
            requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchExpressions:
                - key: strimzi.io/name
                  operator: In
                  values:
                  - kafka-cluster-kafka
              topologyKey: kubernetes.io/hostname
  zookeeper:
    replicas: 3
    resources:
      requests:
        cpu: "500m"
        memory: 1Gi
      limits:
        cpu: "1"
        memory: 2Gi
    storage:
      type: persistent-claim
      size: 20Gi
      storageClassName: local-storage
      deleteClaim: false
  entityOperator:
    topicOperator:
      resources:
        requests:
          cpu: "200m"
          memory: 256Mi
        limits:
          cpu: "500m"
          memory: 512Mi
    userOperator:
      resources:
        requests:
          cpu: "200m"
          memory: 256Mi
        limits:
          cpu: "500m"
          memory: 512Mi
```

### 4.4 KafkaTopic CRD

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: orders
  namespace: bigdata
  labels:
    strimzi.io/cluster: kafka-cluster
spec:
  partitions: 6
  replicas: 3
  config:
    retention.ms: 604800000
    retention.bytes: 1073741824
    segment.bytes: 268435456
    min.insync.replicas: 2
    cleanup.policy: delete
---
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: user-events
  namespace: bigdata
  labels:
    strimzi.io/cluster: kafka-cluster
spec:
  partitions: 12
  replicas: 3
  config:
    retention.ms: 259200000
    retention.bytes: 5368709120
    segment.bytes: 536870912
    min.insync.replicas: 2
    cleanup.policy: delete
---
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: aggregated-stats
  namespace: bigdata
  labels:
    strimzi.io/cluster: kafka-cluster
spec:
  partitions: 3
  replicas: 3
  config:
    retention.ms: 86400000
    cleanup.policy: compact,delete
```

### 4.5 Kafka滚动升级

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: kafka-cluster
  namespace: bigdata
spec:
  kafka:
    version: 3.7.0
    replicas: 3
    listeners:
    - name: plain
      port: 9092
      type: internal
      tls: false
    config:
      offsets.topic.replication.factor: 3
      transaction.state.log.replication.factor: 3
      transaction.state.log.min.isr: 2
      default.replication.factor: 3
      min.insync.replicas: 2
    storage:
      type: persistent-claim
      size: 100Gi
      storageClassName: local-storage
      deleteClaim: false
    template:
      pod:
        affinity:
          podAntiAffinity:
            requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchExpressions:
                - key: strimzi.io/name
                  operator: In
                  values:
                  - kafka-cluster-kafka
              topologyKey: kubernetes.io/hostname
  zookeeper:
    replicas: 3
    storage:
      type: persistent-claim
      size: 20Gi
      storageClassName: local-storage
      deleteClaim: false
```

```bash
kubectl apply -f kafka-cluster-upgrade.yaml

kubectl get kafka kafka-cluster -n bigdata -o yaml | grep -A5 "conditions"

kubectl rollout status statefulset/kafka-cluster-kafka -n bigdata

kubectl get pods -n bigdata -l strimzi.io/name=kafka-cluster-kafka -w
```

---

## 五、存储与网络

### 5.1 PV/PVC/StorageClass

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-storage
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
reclaimPolicy: Retain
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: local-pv-minio
spec:
  capacity:
    storage: 50Gi
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: local-storage
  local:
    path: /mnt/data/minio
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - worker-node-1
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: minio-data-pvc
  namespace: bigdata
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: local-storage
  resources:
    requests:
      storage: 50Gi
```

### 5.2 对象存储与Iceberg集成

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: iceberg-catalog-config
  namespace: bigdata
data:
  catalog.properties: |
    catalog-impl=org.apache.iceberg.hive.HiveCatalog
    uri=thrift://hive-metastore.bigdata.svc:9083
    warehouse=s3a://warehouse/iceberg
    s3.endpoint=http://minio.bigdata.svc:9000
    s3.path-style-access=true
    s3.access-key-id=admin
    s3.secret-access-key=admin123456
    io-impl=org.apache.iceberg.aws.s3.S3FileIO
```

```sql
SELECT * FROM iceberg_db.orders
WHERE create_time >= TIMESTAMP '2024-01-01'
ORDER BY total_amount DESC
LIMIT 100;
```

### 5.3 NetworkPolicy

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-bigdata-internal
  namespace: bigdata
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: bigdata
  - from:
    - namespaceSelector:
        matchLabels:
          name: monitoring
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: bigdata
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: UDP
      port: 53
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: kafka-allow-clients
  namespace: bigdata
spec:
  podSelector:
    matchLabels:
      strimzi.io/name: kafka-cluster-kafka
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: bigdata
    ports:
    - protocol: TCP
      port: 9092
```

---

## 六、生产实践

### 6.1 监控：Prometheus + Grafana

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: monitoring
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
      evaluation_interval: 15s
    scrape_configs:
    - job_name: 'kubernetes-pods'
      kubernetes_sd_configs:
      - role: pod
      relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        target_label: __address__
        regex: (.+)
        replacement: ${1}
    - job_name: 'spark-metrics'
      static_configs:
      - targets: ['spark-metrics.bigdata.svc:7777']
    - job_name: 'flink-metrics'
      static_configs:
      - targets: ['flink-session-cluster.bigdata.svc:9249']
    - job_name: 'kafka-metrics'
      static_configs:
      - targets:
        - 'kafka-cluster-kafka-0.kafka-cluster-kafka-brokers.bigdata.svc:9404'
        - 'kafka-cluster-kafka-1.kafka-cluster-kafka-brokers.bigdata.svc:9404'
        - 'kafka-cluster-kafka-2.kafka-cluster-kafka-brokers.bigdata.svc:9404'
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus
  namespace: monitoring
spec:
  replicas: 1
  selector:
    matchLabels:
      app: prometheus
  template:
    metadata:
      labels:
        app: prometheus
    spec:
      serviceAccountName: prometheus
      containers:
      - name: prometheus
        image: prom/prometheus:v2.48.0
        args:
        - --config.file=/etc/prometheus/prometheus.yml
        - --storage.tsdb.path=/prometheus
        - --storage.tsdb.retention.time=30d
        ports:
        - containerPort: 9090
        volumeMounts:
        - name: config
          mountPath: /etc/prometheus
        - name: data
          mountPath: /prometheus
        resources:
          requests:
            cpu: "500m"
            memory: "1Gi"
          limits:
            cpu: "1"
            memory: "2Gi"
      volumes:
      - name: config
        configMap:
          name: prometheus-config
      - name: data
        persistentVolumeClaim:
          claimName: prometheus-data-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: prometheus
  namespace: monitoring
spec:
  type: ClusterIP
  selector:
    app: prometheus
  ports:
  - port: 9090
    targetPort: 9090
```

#### 关键监控指标

```
大数据组件关键监控指标:

  Spark:
  - spark_executor_active_tasks
  - spark_executor_memory_used_bytes
  - spark_job_duration_seconds
  - spark_stage_failed_tasks
  - spark_driver_BlockManager_disk_diskSpaceUsed

  Flink:
  - flink_jobmanager_job_numRestarts
  - flink_taskmanager_job_task_backPressuredTimeMsPerSecond
  - flink_taskmanager_Status_JVM_Memory_Heap_Used
  - flink_jobmanager_job_lastCheckpointDuration
  - flink_taskmanager_job_task_numRecordsInPerSecond

  Kafka:
  - kafka_server_BrokerTopicMetrics_MessagesInPerSec
  - kafka_server_BrokerTopicMetrics_BytesInPerSec
  - kafka_controller_KafkaController_ActiveControllerCount
  - kafka_server_ReplicaManager_UnderReplicatedPartitions
  - kafka_server_ReplicaManager_LeaderCount

  MinIO:
  - minio_s3_requests_total
  - minio_s3_errors_total
  - minio_disk_storage_used_bytes
  - minio_disk_storage_available_bytes
  - minio_node_network_rx_bytes
```

### 6.2 日志：Loki + Promtail

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: loki
  namespace: monitoring
spec:
  replicas: 1
  selector:
    matchLabels:
      app: loki
  template:
    metadata:
      labels:
        app: loki
    spec:
      containers:
      - name: loki
        image: grafana/loki:2.9.0
        args:
        - -config.file=/etc/loki/local-config.yaml
        - -config.expand-env=true
        ports:
        - containerPort: 3100
        volumeMounts:
        - name: config
          mountPath: /etc/loki
        - name: data
          mountPath: /loki
        resources:
          requests:
            cpu: "200m"
            memory: "512Mi"
          limits:
            cpu: "1"
            memory: "1Gi"
      volumes:
      - name: config
        configMap:
          name: loki-config
      - name: data
        persistentVolumeClaim:
          claimName: loki-data-pvc
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: loki-config
  namespace: monitoring
data:
  local-config.yaml: |
    auth_enabled: false
    server:
      http_listen_port: 3100
    common:
      path_prefix: /loki
      storage:
        filesystem:
          chunks_directory: /loki/chunks
          rules_directory: /loki/rules
      replication_factor: 1
      ring:
        kvstore:
          store: inmemory
    schema_config:
      configs:
      - from: 2020-10-24
        store: boltdb-shipper
        object_store: filesystem
        schema: v11
        index:
          prefix: index_
          period: 24h
    limits_config:
      retention_period: 744h
      max_query_length: 721h
```

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: promtail
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: promtail
  template:
    metadata:
      labels:
        app: promtail
    spec:
      containers:
      - name: promtail
        image: grafana/promtail:2.9.0
        args:
        - -config.file=/etc/promtail/config.yml
        volumeMounts:
        - name: config
          mountPath: /etc/promtail
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
      volumes:
      - name: config
        configMap:
          name: promtail-config
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
```

### 6.3 弹性伸缩

#### HPA（水平Pod自动伸缩）

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: trino-worker-hpa
  namespace: bigdata
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: trino-worker
  minReplicas: 2
  maxReplicas: 8
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 25
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
      - type: Pods
        value: 2
        periodSeconds: 60
      selectPolicy: Max
```

#### Flink弹性伸缩

```yaml
apiVersion: flink.apache.org/v1beta1
kind: FlinkDeployment
metadata:
  name: flink-session-cluster
  namespace: bigdata
spec:
  image: flink:1.18.0-java17
  flinkVersion: v1_18
  serviceAccount: flink
  mode: native
  flinkConfiguration:
    taskmanager.numberOfTaskSlots: "4"
    state.backend: rocksdb
    state.checkpoints.dir: s3://flink-checkpoints/session
    s3.endpoint: http://minio.bigdata.svc:9000
    s3.path.style.access: "true"
    s3.access.key: admin
    s3.secret.key: admin123456
    scheduler-mode: reactive
    execution.checkpointing.interval: 60000
  jobManager:
    resource:
      memory: "4096m"
      cpu: 2
  taskManager:
    resource:
      memory: "8192m"
      cpu: 4
```

---

## 七、课堂练习（45min）

### 练习1：用Spark on K8s运行WordCount（15min）

```bash
kubectl create serviceaccount spark -n bigdata 2>/dev/null || true
kubectl create clusterrolebinding spark-role --clusterrole=edit --serviceaccount=bigdata:spark 2>/dev/null || true

cat <<'PYEOF' > wordcount.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, lower, col

spark = SparkSession.builder.appName("WordCount").getOrCreate()

data = ["hello spark on kubernetes",
        "big data processing with spark",
        "spark flink kafka trino",
        "kubernetes container orchestration",
        "cloud native big data platform"]

df = spark.createDataFrame([(s,) for s in data], ["text"])
words = df.select(explode(split(lower(col("text")), " ")).alias("word"))
counts = words.groupBy("word").count().orderBy(col("count").desc())
counts.show(20)
spark.stop()
PYEOF

kubectl create configmap wordcount-script --from-file=wordcount.py -n bigdata

spark-submit \
  --master k8s://https://$(kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}') \
  --deploy-mode cluster \
  --name spark-wordcount \
  --conf spark.kubernetes.container.image=spark:3.5.0 \
  --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
  --conf spark.kubernetes.namespace=bigdata \
  --conf spark.driver.cores=1 \
  --conf spark.driver.memory=1g \
  --conf spark.executor.cores=1 \
  --conf spark.executor.memory=1g \
  --conf spark.executor.instances=2 \
  --conf spark.kubernetes.file.upload.path=s3a://spark-jobs \
  local:///opt/spark/examples/jars/spark-examples_2.12-3.5.0.jar 100

kubectl get pods -n bigdata -l spark-app-name=spark-wordcount
```

### 练习2：用Flink Operator部署流处理任务（15min）

```bash
kubectl create serviceaccount flink -n bigdata 2>/dev/null || true
kubectl create clusterrolebinding flink-role --clusterrole=edit --serviceaccount=bigdata:flink 2>/dev/null || true

cat <<EOF > flink-session.yaml
apiVersion: flink.apache.org/v1beta1
kind: FlinkDeployment
metadata:
  name: flink-session
  namespace: bigdata
spec:
  image: flink:1.18.0-java17
  flinkVersion: v1_18
  serviceAccount: flink
  mode: native
  flinkConfiguration:
    taskmanager.numberOfTaskSlots: "2"
    state.backend: rocksdb
    state.checkpoints.dir: file:///tmp/flink-checkpoints
    execution.checkpointing.interval: 30000
  jobManager:
    resource:
      memory: "2048m"
      cpu: 1
  taskManager:
    resource:
      memory: "4096m"
      cpu: 2
EOF

kubectl apply -f flink-session.yaml

kubectl get flinkdeployment -n bigdata
kubectl get pods -n bigdata -l app=flink-session

kubectl port-forward svc/flink-session-rest 8081:8081 -n bigdata &

curl -s http://localhost:8081/overview
```

### 练习3：用Strimzi部署Kafka集群（15min）

```bash
cat <<EOF > kafka-single.yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: kafka-cluster
  namespace: bigdata
spec:
  kafka:
    version: 3.6.0
    replicas: 1
    listeners:
    - name: plain
      port: 9092
      type: internal
      tls: false
    config:
      offsets.topic.replication.factor: 1
      transaction.state.log.replication.factor: 1
      transaction.state.log.min.isr: 1
      default.replication.factor: 1
    storage:
      type: persistent-claim
      size: 10Gi
      deleteClaim: false
    resources:
      requests:
        cpu: "500m"
        memory: 1Gi
      limits:
        cpu: "1"
        memory: 2Gi
  zookeeper:
    replicas: 1
    storage:
      type: persistent-claim
      size: 5Gi
      deleteClaim: false
    resources:
      requests:
        cpu: "200m"
        memory: 512Mi
      limits:
        cpu: "500m"
        memory: 1Gi
EOF

kubectl apply -f kafka-single.yaml

kubectl get kafka kafka-cluster -n bigdata -o wide
kubectl get pods -n bigdata -l strimzi.io/cluster=kafka-cluster -w

cat <<EOF > kafka-topic.yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: test-topic
  namespace: bigdata
  labels:
    strimzi.io/cluster: kafka-cluster
spec:
  partitions: 3
  replicas: 1
  config:
    retention.ms: 604800000
EOF

kubectl apply -f kafka-topic.yaml

kubectl get kafkatopic -n bigdata
```

---

## 八、课后作业

### 必做

1. **Spark ETL迁移到K8s**：将L1项目4的Spark ETL任务迁移到K8s运行，要求：
   - 编写SparkApplication CRD YAML
   - 使用MinIO作为数据存储（替代HDFS）
   - 配置Iceberg Catalog连接Hive Metastore
   - 验证ETL任务在K8s上运行成功并产出数据

2. **Flink实时管道迁移到K8s**：用Flink Operator部署L2项目7的实时管道，要求：
   - 编写FlinkDeployment CRD YAML（Application模式）
   - 使用Strimzi部署Kafka集群作为数据源
   - 配置Checkpoint到MinIO
   - 验证流处理任务正常运行

3. **部署文档与运维手册**：编写K8s部署文档和运维手册，包含：
   - 环境搭建步骤（Kind集群 + 所有组件）
   - 各组件Helm Values配置说明
   - 日常运维操作（扩缩容、滚动升级、故障排查）
   - 监控告警配置（关键指标 + 阈值）

### 选做

1. 配置Spark on K8s的动态资源分配，验证Executor自动伸缩
2. 部署Prometheus + Grafana + Loki完整可观测性栈
3. 编写Airflow DAG，编排Spark ETL + Flink实时管道的端到端数据流

---

## 九、参考资料

- [Spark on Kubernetes官方文档](https://spark.apache.org/docs/latest/running-on-kubernetes.html)
- [Spark Operator GitHub](https://github.com/kubeflow/spark-operator)
- [Flink Kubernetes Operator官方文档](https://nightlies.apache.org/flink/flink-kubernetes-operator-docs-stable/)
- [Strimzi Kafka Operator官方文档](https://strimzi.io/docs/latest/)
- [K8s存储最佳实践](https://kubernetes.io/docs/concepts/storage/)
- [K8s NetworkPolicy](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
- [Prometheus Flink Exporter](https://flink.apache.org/docs/latest/deployment/metric_reporters/#prometheus)
- [Strimzi Kafka监控](https://strimzi.io/docs/latest/#proc-monitoring-str)
