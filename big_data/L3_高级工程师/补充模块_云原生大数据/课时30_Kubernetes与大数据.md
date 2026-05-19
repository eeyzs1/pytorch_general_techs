# 课时30：Kubernetes与大数据

> **所属阶段**：L3 高级工程师 | **模块**：补充模块_云原生大数据 | **课时**：4h | **难度**：★★★★★

---

## 一、教学目标

1. 理解Kubernetes核心架构，掌握Pod/Service/Deployment/StatefulSet等核心资源对象
2. 能够搭建本地K8s开发集群（Kind/Minikube）
3. 掌握大数据组件在K8s上的部署方法：MinIO、Hive Metastore、Trino、Airflow
4. 理解Helm包管理工具，能编写Values文件自定义配置
5. 掌握K8s资源管理机制：ResourceQuota/LimitRange/PriorityClass/GPU调度

---

## 二、Kubernetes核心概念

### 2.1 K8s是什么

```
Kubernetes = 容器编排平台

  ┌───────────────────────────────────────────────────────────────┐
  │                     Kubernetes 解决什么问题                     │
  │                                                               │
  │  Docker Compose:  单机编排，一台机器上的多容器管理              │
  │  Kubernetes:      集群编排，成百上千台机器上的容器管理          │
  │                                                               │
  │  核心能力:                                                     │
  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐    │
  │  │  服务发现  │ │  弹性伸缩  │ │  滚动更新  │ │  自愈(故障恢复)│    │
  │  └──────────┘ └──────────┘ └──────────┘ └──────────────┘    │
  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐    │
  │  │  配置管理  │ │  存储编排  │ │  负载均衡  │ │  密钥管理     │    │
  │  └──────────┘ └──────────┘ └──────────┘ └──────────────┘    │
  └───────────────────────────────────────────────────────────────┘
```

### 2.2 核心资源对象

```
K8s核心资源对象一览:

  ┌─────────────────────────────────────────────────────────────┐
  │  工作负载:                                                   │
  │    Pod          → 最小调度单元，一个或多个容器的集合            │
  │    Deployment   → 无状态应用，管理Pod副本集                    │
  │    StatefulSet  → 有状态应用，稳定网络标识+持久存储            │
  │    DaemonSet    → 每个节点运行一个Pod（日志/监控Agent）        │
  │    Job/CronJob  → 一次性/定时任务                             │
  │                                                              │
  │  服务发现:                                                   │
  │    Service      → 为Pod提供稳定访问入口（ClusterIP/NodePort/  │
  │                   LoadBalancer）                              │
  │    Ingress      → HTTP层路由，域名+路径转发                    │
  │                                                              │
  │  配置与存储:                                                 │
  │    ConfigMap    → 非敏感配置（环境变量、配置文件）              │
  │    Secret       → 敏感配置（密码、证书、Token）                │
  │    PV/PVC       → 持久化存储（PersistentVolume / Claim）      │
  │    StorageClass → 动态存储供给                                │
  │                                                              │
  │  组织与安全:                                                 │
  │    Namespace    → 资源隔离（多租户/多环境）                    │
  │    RBAC         → 基于角色的访问控制                          │
  │    NetworkPolicy→ 网络隔离策略                                │
  └─────────────────────────────────────────────────────────────┘
```

#### Pod详解

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: spark-driver
  namespace: bigdata
  labels:
    app: spark
    role: driver
spec:
  containers:
  - name: spark-driver
    image: spark:3.5.0
    command: ["/opt/spark/bin/spark-submit"]
    args:
    - "--class"
    - "org.apache.spark.examples.SparkPi"
    - "--master"
    - "k8s://https://kubernetes.default.svc"
    - "--deploy-mode"
    - "cluster"
    - "local:///opt/spark/examples/jars/spark-examples.jar"
    - "100"
    resources:
      requests:
        cpu: "1"
        memory: "2Gi"
      limits:
        cpu: "2"
        memory: "4Gi"
    env:
    - name: SPARK_HOME
      value: "/opt/spark"
    volumeMounts:
    - name: data
      mountPath: /data
  volumes:
  - name: data
    persistentVolumeClaim:
      claimName: spark-data-pvc
  restartPolicy: Never
```

#### Service详解

```yaml
apiVersion: v1
kind: Service
metadata:
  name: minio
  namespace: bigdata
spec:
  type: ClusterIP
  selector:
    app: minio
  ports:
  - name: api
    port: 9000
    targetPort: 9000
  - name: console
    port: 9001
    targetPort: 9001
---
apiVersion: v1
kind: Service
metadata:
  name: minio-external
  namespace: bigdata
spec:
  type: NodePort
  selector:
    app: minio
  ports:
  - name: api
    port: 9000
    targetPort: 9000
    nodePort: 30900
```

#### StatefulSet详解

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: hive-metastore-db
  namespace: bigdata
spec:
  serviceName: hive-metastore-db
  replicas: 1
  selector:
    matchLabels:
      app: hive-metastore-db
  template:
    metadata:
      labels:
        app: hive-metastore-db
    spec:
      containers:
      - name: postgres
        image: postgres:15
        env:
        - name: POSTGRES_DB
          value: metastore
        - name: POSTGRES_USER
          value: hive
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: hive-metastore-secret
              key: postgres-password
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: metastore-data
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            cpu: "500m"
            memory: "1Gi"
          limits:
            cpu: "1"
            memory: "2Gi"
  volumeClaimTemplates:
  - metadata:
      name: metastore-data
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: local-storage
      resources:
        requests:
          storage: 20Gi
```

#### ConfigMap与Secret

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: trino-config
  namespace: bigdata
data:
  trino-config.properties: |
    coordinator=true
    node-scheduler.include-coordinator=false
    http-server.http.port=8080
    query.max-memory=4GB
    query.max-memory-per-node=1GB
    discovery.uri=http://trino-coordinator:8080
  trino-iceberg.properties: |
    connector.name=iceberg
    iceberg.catalog.type=hive_metastore
    hive.metastore.uri=thrift://hive-metastore:9083
    iceberg.file-io-impl=org.apache.iceberg.aws.s3.S3FileIO
    s3.endpoint=http://minio:9000
    s3.path-style-access=true
---
apiVersion: v1
kind: Secret
metadata:
  name: minio-secret
  namespace: bigdata
type: Opaque
stringData:
  root-user: admin
  root-password: admin123456
  accesskey: minioadmin
  secretkey: minioadmin123
```

#### Namespace

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: bigdata
  labels:
    name: bigdata
    environment: production
---
apiVersion: v1
kind: Namespace
metadata:
  name: bigdata-dev
  labels:
    name: bigdata-dev
    environment: development
```

### 2.3 K8s架构

```
Kubernetes集群架构:

  ┌──────────────────────────────────────────────────────────────────────┐
  │                        Control Plane (控制面)                         │
  │                                                                      │
  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
  │  │  API Server   │  │    etcd       │  │  Scheduler   │              │
  │  │              │  │              │  │              │              │
  │  │ 集群入口     │  │ 状态存储     │  │ Pod调度      │              │
  │  │ REST API     │  │ KV数据库     │  │ 节点选择     │              │
  │  │ 认证授权     │  │ Watch机制    │  │ 亲和/反亲和  │              │
  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
  │         │                  │                  │                      │
  │  ┌──────┴──────────────────┴──────────────────┴───────┐            │
  │  │              Controller Manager                     │            │
  │  │  Deployment Controller / ReplicaSet Controller     │            │
  │  │  StatefulSet Controller / Job Controller           │            │
  │  │  Node Controller / Service Account Controller      │            │
  │  └────────────────────────────────────────────────────┘            │
  └──────────────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────────────────┐
  │                     Worker Node (工作节点)                            │
  │                                                                      │
  │  ┌──────────────────────────┐  ┌──────────────────────────┐        │
  │  │        kubelet            │  │      kube-proxy          │        │
  │  │                          │  │                          │        │
  │  │  Pod生命周期管理          │  │  Service网络代理          │        │
  │  │  容器健康检查            │  │  iptables/ipvs规则        │        │
  │  │  资源上报                │  │  负载均衡                 │        │
  │  │  Volume挂载              │  │  网络策略执行             │        │
  │  └──────────────────────────┘  └──────────────────────────┘        │
  │                                                                      │
  │  ┌──────────────────────────────────────────────────────────┐      │
  │  │               Container Runtime (containerd/CRI-O)        │      │
  │  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐        │      │
  │  │  │ Pod A  │  │ Pod B  │  │ Pod C  │  │ Pod D  │        │      │
  │  │  └────────┘  └────────┘  └────────┘  └────────┘        │      │
  │  └──────────────────────────────────────────────────────────┘      │
  └──────────────────────────────────────────────────────────────────────┘
```

---

## 三、大数据on K8s的挑战

### 3.1 四大核心挑战

```
大数据组件上K8s的挑战:

  挑战1: 有状态服务
  ┌──────────────────────────────────────────────────────────┐
  │  大数据组件多数有状态:                                     │
  │  - Kafka: 分区Leader选举、副本同步                        │
  │  - Hive Metastore: 数据库状态                             │
  │  - HDFS: NameNode/DataNode状态                           │
  │  - ZooKeeper: 集群协调状态                                │
  │                                                          │
  │  K8s原生适合无状态服务(Deployment)                         │
  │  有状态服务需要StatefulSet + PVC + Headless Service       │
  └──────────────────────────────────────────────────────────┘

  挑战2: 存储挂载
  ┌──────────────────────────────────────────────────────────┐
  │  大数据需要大量持久化存储:                                 │
  │  - 本地存储性能好但Pod迁移后丢失                           │
  │  - 网络存储(Ceph/NFS)性能有损耗                           │
  │  - 对象存储(S3/MinIO)不支持追加写                         │
  │  - 存储类选择影响性能和成本                                │
  └──────────────────────────────────────────────────────────┘

  挑战3: 网络性能
  ┌──────────────────────────────────────────────────────────┐
  │  大数据Shuffle产生大量网络IO:                              │
  │  - K8s网络 overlay 有性能损耗(约10-20%)                   │
  │  - Spark Shuffle可能占满网络带宽                          │
  │  - 需要考虑HostNetwork/CNI选择                            │
  │  - 网络策略可能影响组件间通信                              │
  └──────────────────────────────────────────────────────────┘

  挑战4: 资源隔离
  ┌──────────────────────────────────────────────────────────┐
  │  多租户共享集群:                                          │
  │  - 不同团队/项目资源争抢                                   │
  │  - 大作业可能占满集群资源                                  │
  │  - 需要ResourceQuota限制命名空间资源                      │
  │  - 需要LimitRange约束Pod资源                              │
  │  - 需要PriorityClass实现优先级抢占                        │
  └──────────────────────────────────────────────────────────┘
```

### 3.2 大数据组件K8s部署策略对比

```
部署策略选择:

  ┌──────────────────────────────────────────────────────────────┐
  │  组件类型        部署方式          存储方案       网络方案     │
  │  ────────────────────────────────────────────────────────── │
  │  计算引擎        Deployment/Job    临时存储       普通CNI     │
  │  (Spark/Flink)                                                │
  │                                                               │
  │  查询引擎      StatefulSet       PVC            普通CNI     │
  │  (Trino/Presto)                                               │
  │                                                               │
  │  消息队列        StatefulSet       本地PV         HostNetwork │
  │  (Kafka)        + Headless Svc                                │
  │                                                               │
  │  对象存储       StatefulSet       本地PV         HostNetwork │
  │  (MinIO)                                                      │
  │                                                               │
  │  元数据服务      Deployment        PVC            普通CNI     │
  │  (Hive Metastore)                                             │
  │                                                               │
  │  调度器          Deployment        PVC            普通CNI     │
  │  (Airflow)                                                    │
  └──────────────────────────────────────────────────────────────┘
```

---

## 四、本地K8s集群搭建

### 4.1 Kind集群搭建

```yaml
apiVersion: kind.x-k8s.io/v1alpha4
kind: Cluster
name: bigdata-cluster
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 30900
    hostPort: 9000
  - containerPort: 30901
    hostPort: 9001
  - containerPort: 30080
    hostPort: 8080
  - containerPort: 30053
    hostPort: 8053
  extraMounts:
  - hostPath: ./data
    containerPath: /data
- role: worker
  extraMounts:
  - hostPath: ./data
    containerPath: /data
- role: worker
  extraMounts:
  - hostPath: ./data
    containerPath: /data
```

```bash
kind create cluster --config kind-cluster.yaml --image kindest/node:v1.28.0

kubectl cluster-info --context kind-bigdata-cluster

kubectl get nodes

kubectl create namespace bigdata

kubectl config set-context --current --namespace=bigdata
```

### 4.2 Minikube集群搭建（备选）

```bash
minikube start --cpus=4 --memory=8192 --disk-size=50g --driver=docker --kubernetes-version=v1.28.0

minikube addons enable metrics-server
minikube addons enable dashboard
minikube addons enable ingress
minikube addons enable storage-provisioner

kubectl get nodes

minikube dashboard
```

---

## 五、Helm Charts

### 5.1 Helm核心概念

```
Helm = K8s的包管理器（类似apt/yum/brew）

  ┌──────────────────────────────────────────────────────────┐
  │  Chart     → 应用包（一组K8s YAML模板 + 默认配置）        │
  │  Values    → 配置值（覆盖Chart默认配置）                  │
  │  Release   → Chart的一次安装实例                          │
  │  Repository→ Chart仓库（存放和分发Chart）                 │
  │                                                          │
  │  工作流程:                                                │
  │  helm repo add → helm search → helm install → helm upgrade│
  │                                                          │
  │  Chart目录结构:                                           │
  │  mychart/                                                │
  │  ├── Chart.yaml          ← Chart元信息                   │
  │  ├── values.yaml         ← 默认配置值                    │
  │  ├── templates/          ← K8s资源模板                   │
  │  │   ├── deployment.yaml                                │
  │  │   ├── service.yaml                                   │
  │  │   ├── configmap.yaml                                 │
  │  │   ├── _helpers.tpl    ← 模板辅助函数                 │
  │  │   └── NOTES.txt       ← 安装后提示                   │
  │  ├── charts/             ← 依赖的子Chart                │
  │  └── .helmignore                                        │
  └──────────────────────────────────────────────────────────┘
```

### 5.2 Helm常用命令

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add minio https://charts.min.io/
helm repo add apache-airflow https://airflow.apache.org
helm repo update

helm search repo minio
helm search repo trino

helm install my-minio minio/minio --namespace bigdata
helm list -n bigdata
helm status my-minio -n bigdata
helm upgrade my-minio minio/minio --namespace bigdata -f values-minio.yaml
helm rollback my-minio 1 -n bigdata
helm uninstall my-minio -n bigdata

helm get values my-minio -n bigdata
helm template my-minio minio/minio -f values-minio.yaml > rendered.yaml
```

---

## 六、大数据组件K8s部署

### 6.1 MinIO部署（S3兼容对象存储）

#### Helm方式部署

```yaml
values-minio.yaml:

mode: distributed
replicas: 4
image:
  repository: minio/minio
  tag: RELEASE.2024-01-16T16-07-38Z
  pullPolicy: IfNotPresent

rootUser: admin
rootPassword: admin123456

persistence:
  enabled: true
  storageClassName: local-storage
  accessMode: ReadWriteOnce
  size: 50Gi

resources:
  requests:
    cpu: "500m"
    memory: "1Gi"
  limits:
    cpu: "2"
    memory: "4Gi"

service:
  type: ClusterIP
  port: 9000
  consolePort: 9001

ingress:
  enabled: true
  ingressClassName: nginx
  host: minio.bigdata.local
  consoleHost: minio-console.bigdata.local

buckets:
  - name: warehouse
    policy: none
    purge: false
  - name: iceberg-data
    policy: none
    purge: false
  - name: spark-events
    policy: none
    purge: false

environment:
  MINIO_BROWSER_REDIRECT_URL: http://minio-console.bigdata.local
  MINIO_SERVER_URL: http://minio.bigdata.local

tolerations: []
nodeSelector: {}
affinity: {}
```

```bash
helm install minio minio/minio \
  --namespace bigdata \
  -f values-minio.yaml \
  --timeout 5m

kubectl get pods -n bigdata -l app=minio
kubectl get svc -n bigdata -l app=minio

kubectl port-forward svc/minio 9000:9000 -n bigdata &
kubectl port-forward svc/minio-console 9001:9001 -n bigdata &
```

#### 原生YAML方式部署

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: minio
  namespace: bigdata
spec:
  serviceName: minio-headless
  replicas: 1
  selector:
    matchLabels:
      app: minio
  template:
    metadata:
      labels:
        app: minio
    spec:
      containers:
      - name: minio
        image: minio/minio:RELEASE.2024-01-16T16-07-38Z
        args:
        - server
        - /data
        - --console-address
        - ":9001"
        env:
        - name: MINIO_ROOT_USER
          valueFrom:
            secretKeyRef:
              name: minio-secret
              key: root-user
        - name: MINIO_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: minio-secret
              key: root-password
        ports:
        - containerPort: 9000
          name: api
        - containerPort: 9001
          name: console
        volumeMounts:
        - name: data
          mountPath: /data
        resources:
          requests:
            cpu: "500m"
            memory: "1Gi"
          limits:
            cpu: "2"
            memory: "4Gi"
        livenessProbe:
          httpGet:
            path: /minio/health/live
            port: 9000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /minio/health/ready
            port: 9000
          initialDelaySeconds: 10
          periodSeconds: 5
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: local-storage
      resources:
        requests:
          storage: 50Gi
---
apiVersion: v1
kind: Service
metadata:
  name: minio
  namespace: bigdata
spec:
  type: ClusterIP
  selector:
    app: minio
  ports:
  - name: api
    port: 9000
    targetPort: 9000
  - name: console
    port: 9001
    targetPort: 9001
---
apiVersion: v1
kind: Service
metadata:
  name: minio-headless
  namespace: bigdata
spec:
  type: ClusterIP
  clusterIP: None
  selector:
    app: minio
  ports:
  - name: api
    port: 9000
    targetPort: 9000
```

### 6.2 Hive Metastore部署

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hive-metastore
  namespace: bigdata
spec:
  replicas: 1
  selector:
    matchLabels:
      app: hive-metastore
  template:
    metadata:
      labels:
        app: hive-metastore
    spec:
      initContainers:
      - name: wait-for-db
        image: busybox:1.36
        command:
        - sh
        - -c
        - |
          until nc -z hive-metastore-db 5432; do
            echo "Waiting for PostgreSQL..."
            sleep 2
          done
      - name: schema-init
        image: apache/hive:3.1.3
        command:
        - /opt/hive/bin/schematool
        - -dbType
        - postgres
        - -initSchema
        env:
        - name: SERVICE_NAME
          value: metastore
        - name: IS_RESUME
          value: "true"
        - name: HIVE_METASTORE_URIS
          value: thrift://hive-metastore:9083
        - name: METASTORE_DB_HOSTNAME
          value: hive-metastore-db
        - name: METASTORE_DB_PORT
          value: "5432"
        - name: METASTORE_DB_NAME
          value: metastore
        - name: METASTORE_DB_USER
          value: hive
        - name: METASTORE_DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: hive-metastore-secret
              key: postgres-password
      containers:
      - name: metastore
        image: apache/hive:3.1.3
        env:
        - name: SERVICE_NAME
          value: metastore
        - name: IS_RESUME
          value: "true"
        - name: HIVE_METASTORE_URIS
          value: thrift://hive-metastore:9083
        - name: METASTORE_DB_HOSTNAME
          value: hive-metastore-db
        - name: METASTORE_DB_PORT
          value: "5432"
        - name: METASTORE_DB_NAME
          value: metastore
        - name: METASTORE_DB_USER
          value: hive
        - name: METASTORE_DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: hive-metastore-secret
              key: postgres-password
        - name: S3_ENDPOINT
          value: http://minio:9000
        - name: S3_ACCESS_KEY
          valueFrom:
            secretKeyRef:
              name: minio-secret
              key: root-user
        - name: S3_SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: minio-secret
              key: root-password
        ports:
        - containerPort: 9083
        resources:
          requests:
            cpu: "500m"
            memory: "1Gi"
          limits:
            cpu: "1"
            memory: "2Gi"
---
apiVersion: v1
kind: Service
metadata:
  name: hive-metastore
  namespace: bigdata
spec:
  type: ClusterIP
  selector:
    app: hive-metastore
  ports:
  - port: 9083
    targetPort: 9083
```

### 6.3 Trino on K8s部署

#### Coordinator

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: trino-coordinator
  namespace: bigdata
spec:
  replicas: 1
  selector:
    matchLabels:
      app: trino
      role: coordinator
  template:
    metadata:
      labels:
        app: trino
        role: coordinator
    spec:
      containers:
      - name: trino
        image: trinodb/trino:435
        ports:
        - containerPort: 8080
        volumeMounts:
        - name: trino-config
          mountPath: /etc/trino/config.properties
          subPath: config.properties
        - name: trino-config
          mountPath: /etc/trino/node.properties
          subPath: node.properties
        - name: trino-catalog-iceberg
          mountPath: /etc/trino/catalog/iceberg.properties
          subPath: iceberg.properties
        resources:
          requests:
            cpu: "1"
            memory: "4Gi"
          limits:
            cpu: "2"
            memory: "8Gi"
      volumes:
      - name: trino-config
        configMap:
          name: trino-coordinator-config
      - name: trino-catalog-iceberg
        configMap:
          name: trino-catalog-config
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: trino-coordinator-config
  namespace: bigdata
data:
  config.properties: |
    coordinator=true
    node-scheduler.include-coordinator=false
    http-server.http.port=8080
    query.max-memory=8GB
    query.max-memory-per-node=2GB
    query.max-total-memory-per-node=3GB
    discovery.uri=http://trino-coordinator:8080
  node.properties: |
    node.environment=production
    node.data-dir=/data/trino
    plugin.dir=/usr/lib/trino/plugin
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: trino-catalog-config
  namespace: bigdata
data:
  iceberg.properties: |
    connector.name=iceberg
    iceberg.catalog.type=hive_metastore
    hive.metastore.uri=thrift://hive-metastore:9083
    iceberg.file-io-impl=org.apache.iceberg.aws.s3.S3FileIO
    s3.endpoint=http://minio:9000
    s3.path-style-access=true
    s3.access-key-id=admin
    s3.secret-access-key=admin123456
```

#### Worker

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: trino-worker
  namespace: bigdata
spec:
  replicas: 2
  selector:
    matchLabels:
      app: trino
      role: worker
  template:
    metadata:
      labels:
        app: trino
        role: worker
    spec:
      containers:
      - name: trino
        image: trinodb/trino:435
        volumeMounts:
        - name: trino-config
          mountPath: /etc/trino/config.properties
          subPath: config.properties
        - name: trino-config
          mountPath: /etc/trino/node.properties
          subPath: node.properties
        - name: trino-catalog-iceberg
          mountPath: /etc/trino/catalog/iceberg.properties
          subPath: iceberg.properties
        resources:
          requests:
            cpu: "2"
            memory: "8Gi"
          limits:
            cpu: "4"
            memory: "16Gi"
      volumes:
      - name: trino-config
        configMap:
          name: trino-worker-config
      - name: trino-catalog-iceberg
        configMap:
          name: trino-catalog-config
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: trino-worker-config
  namespace: bigdata
data:
  config.properties: |
    coordinator=false
    http-server.http.port=8080
    query.max-memory=8GB
    query.max-memory-per-node=4GB
    query.max-total-memory-per-node=5GB
    discovery.uri=http://trino-coordinator:8080
  node.properties: |
    node.environment=production
    node.data-dir=/data/trino
    plugin.dir=/usr/lib/trino/plugin
```

#### Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: trino-coordinator
  namespace: bigdata
spec:
  type: ClusterIP
  selector:
    app: trino
    role: coordinator
  ports:
  - port: 8080
    targetPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: trino-worker
  namespace: bigdata
spec:
  type: ClusterIP
  clusterIP: None
  selector:
    app: trino
    role: worker
  ports:
  - port: 8080
    targetPort: 8080
```

### 6.4 Airflow on K8s部署

```yaml
values-airflow.yaml:

airflowVersion: "2.8.0"
defaultAirflowRepository: apache/airflow
defaultAirflowTag: "2.8.0"

executor: KubernetesExecutor

database:
  type: postgres
  postgres:
    enabled: true
    user: airflow
    password: airflow123
    db: airflow

redis:
  enabled: false

webserver:
  replicas: 1
  resources:
    requests:
      cpu: "500m"
      memory: "1Gi"
    limits:
      cpu: "1"
      memory: "2Gi"
  service:
    type: ClusterIP
    ports:
      - name: airflow-ui
        port: 8080

scheduler:
  replicas: 1
  resources:
    requests:
      cpu: "1"
      memory: "2Gi"
    limits:
      cpu: "2"
      memory: "4Gi"

workers:
  replicas: 1
  resources:
    requests:
      cpu: "1"
      memory: "2Gi"
    limits:
      cpu: "2"
      memory: "4Gi"

triggerer:
  replicas: 1
  resources:
    requests:
      cpu: "500m"
      memory: "1Gi"
    limits:
      cpu: "1"
      memory: "2Gi"

logs:
  persistence:
    enabled: true
    storageClassName: local-storage
    accessMode: ReadWriteOnce
    size: 10Gi

dags:
  gitSync:
    enabled: true
    repo: "https://github.com/your-org/airflow-dags.git"
    branch: main
    subPath: "dags"
    syncWait: 60
    depth: 1

config:
  core:
    dags_folder: /opt/airflow/dags
    load_examples: False
  kubernetes:
    namespace: bigdata
    worker_container_repository: apache/airflow
    worker_container_tag: "2.8.0"
    delete_worker_pods: True
    delete_worker_pods_on_failure: True

extraEnv:
  - name: AIRFLOW_VAR_S3_ENDPOINT
    value: "http://minio:9000"
  - name: AIRFLOW_VAR_S3_ACCESS_KEY
    valueFrom:
      secretKeyRef:
        name: minio-secret
        key: root-user
  - name: AIRFLOW_VAR_S3_SECRET_KEY
    valueFrom:
      secretKeyRef:
        name: minio-secret
        key: root-password

ingress:
  web:
    enabled: true
    ingressClassName: nginx
    host: airflow.bigdata.local
```

```bash
helm repo add apache-airflow https://airflow.apache.org
helm repo update

helm install airflow apache-airflow/airflow \
  --namespace bigdata \
  -f values-airflow.yaml \
  --timeout 10m

kubectl get pods -n bigdata -l app.kubernetes.io/name=airflow

kubectl port-forward svc/airflow-webserver 8053:8080 -n bigdata &

kubectl exec -it -n bigdata airflow-webserver-xxx -- airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \
  --password admin123
```

---

## 七、资源管理

### 7.1 ResourceQuota（命名空间级资源配额）

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: bigdata-quota
  namespace: bigdata
spec:
  hard:
    requests.cpu: "20"
    requests.memory: 40Gi
    limits.cpu: "40"
    limits.memory: 80Gi
    persistentvolumeclaims: "20"
    requests.storage: 200Gi
    pods: "50"
    services: "20"
    configmaps: "30"
    secrets: "30"
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: bigdata-dev-quota
  namespace: bigdata-dev
spec:
  hard:
    requests.cpu: "8"
    requests.memory: 16Gi
    limits.cpu: "16"
    limits.memory: 32Gi
    persistentvolumeclaims: "10"
    requests.storage: 50Gi
    pods: "20"
    services: "10"
```

### 7.2 LimitRange（Pod级资源约束）

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: bigdata-limits
  namespace: bigdata
spec:
  limits:
  - type: Pod
    max:
      cpu: "8"
      memory: 32Gi
    min:
      cpu: "100m"
      memory: 128Mi
  - type: Container
    max:
      cpu: "8"
      memory: 32Gi
    min:
      cpu: "100m"
      memory: 128Mi
    default:
      cpu: "500m"
      memory: 1Gi
    defaultRequest:
      cpu: "100m"
      memory: 256Mi
    maxLimitRequestRatio:
      cpu: "4"
      memory: "4"
  - type: PersistentVolumeClaim
    max:
      storage: 100Gi
    min:
      storage: 1Gi
```

### 7.3 PriorityClass（优先级与抢占）

```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
description: "高优先级: 生产任务"
value: 1000000
globalDefault: false
preemptionPolicy: PreemptLowerPriority
---
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: medium-priority
description: "中优先级: 开发测试"
value: 500000
globalDefault: false
preemptionPolicy: PreemptLowerPriority
---
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: low-priority
description: "低优先级: 批处理/训练任务"
value: 100000
globalDefault: true
preemptionPolicy: PreemptLowerPriority
```

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: spark-etl-job
  namespace: bigdata
spec:
  template:
    spec:
      priorityClassName: high-priority
      containers:
      - name: spark
        image: spark:3.5.0
        resources:
          requests:
            cpu: "4"
            memory: "8Gi"
          limits:
            cpu: "4"
            memory: "8Gi"
      restartPolicy: Never
  backoffLimit: 3
```

### 7.4 GPU调度

```yaml
apiVersion: resource.k8s.io/v1beta1
kind: DeviceClass
metadata:
  name: gpu-nvidia
spec:
  nodeSelector:
    accelerator: nvidia-tesla-v100
---
apiVersion: v1
kind: Pod
metadata:
  name: spark-gpu-job
  namespace: bigdata
spec:
  priorityClassName: high-priority
  containers:
  - name: spark-executor
    image: spark:3.5.0-gpu
    resources:
      requests:
        cpu: "4"
        memory: "16Gi"
        nvidia.com/gpu: "1"
      limits:
        cpu: "4"
        memory: "16Gi"
        nvidia.com/gpu: "1"
    volumeMounts:
    - name: nvidia
      mountPath: /usr/local/nvidia
  volumes:
  - name: nvidia
    hostPath:
      path: /usr/local/nvidia
  nodeSelector:
    accelerator: nvidia-tesla-v100
  tolerations:
  - key: nvidia.com/gpu
    operator: Exists
    effect: NoSchedule
```

### 7.5 多租户隔离方案

```
多租户隔离架构:

  ┌──────────────────────────────────────────────────────────────┐
  │                    Kubernetes Cluster                         │
  │                                                              │
  │  ┌────────────────────────────────────────────────────────┐ │
  │  │  Namespace: team-alpha                                  │ │
  │  │  ResourceQuota: CPU=10, Mem=20Gi, Pods=30              │ │
  │  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────────┐             │ │
  │  │  │Spark │ │Trino │ │Airflow│ │MinIO     │             │ │
  │  │  │ETL   │ │Query │ │DAG   │ │Data      │             │ │
  │  │  └──────┘ └──────┘ └──────┘ └──────────┘             │ │
  │  └────────────────────────────────────────────────────────┘ │
  │                                                              │
  │  ┌────────────────────────────────────────────────────────┐ │
  │  │  Namespace: team-beta                                   │ │
  │  │  ResourceQuota: CPU=8, Mem=16Gi, Pods=20              │ │
  │  │  ┌──────┐ ┌──────┐ ┌──────────┐                       │ │
  │  │  │Flink │ │Kafka │ │Airflow   │                       │ │
  │  │  │RT    │ │Stream│ │DAG       │                       │ │
  │  │  └──────┘ └──────┘ └──────────┘                       │ │
  │  └────────────────────────────────────────────────────────┘ │
  │                                                              │
  │  ┌────────────────────────────────────────────────────────┐ │
  │  │  Namespace: shared-infra                                │ │
  │  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐  │ │
  │  │  │Hive Metastore│ │MinIO(共享)   │ │Monitoring    │  │ │
  │  │  └──────────────┘ └──────────────┘ └──────────────┘  │ │
  │  └────────────────────────────────────────────────────────┘ │
  └──────────────────────────────────────────────────────────────┘
```

---

## 八、课堂练习（60min）

### 练习1：用Kind创建本地K8s集群（10min）

```bash
cat <<EOF > kind-bigdata.yaml
apiVersion: kind.x-k8s.io/v1alpha4
kind: Cluster
name: bigdata-lab
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 30900
    hostPort: 9000
  - containerPort: 30080
    hostPort: 8080
  - containerPort: 30053
    hostPort: 8053
- role: worker
EOF

kind create cluster --config kind-bigdata.yaml --image kindest/node:v1.28.0

kubectl get nodes

kubectl create namespace bigdata

kubectl config set-context --current --namespace=bigdata
```

### 练习2：部署MinIO + Trino + Airflow（30min）

```bash
helm repo add minio https://charts.min.io/
helm repo add apache-airflow https://airflow.apache.org
helm repo update

cat <<EOF > values-minio-lab.yaml
mode: standalone
rootUser: admin
rootPassword: admin123456
persistence:
  enabled: true
  size: 10Gi
resources:
  requests:
    cpu: 200m
    memory: 512Mi
  limits:
    cpu: "1"
    memory: 1Gi
buckets:
  - name: warehouse
  - name: iceberg-data
  - name: spark-events
EOF

helm install minio minio/minio -n bigdata -f values-minio-lab.yaml --timeout 5m

kubectl get pods -n bigdata -l app=minio
kubectl get svc -n bigdata -l app=minio

kubectl apply -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: minio-secret
  namespace: bigdata
type: Opaque
stringData:
  root-user: admin
  root-password: admin123456
EOF

kubectl apply -f hive-metastore-db.yaml
kubectl apply -f hive-metastore.yaml

kubectl wait --for=condition=ready pod -l app=hive-metastore -n bigdata --timeout=120s

kubectl apply -f trino-coordinator.yaml
kubectl apply -f trino-worker.yaml
kubectl apply -f trino-service.yaml

kubectl wait --for=condition=ready pod -l app=trino -n bigdata --timeout=120s

kubectl port-forward svc/trino-coordinator 8080:8080 -n bigdata &

curl -s http://localhost:8080/v1/info
```

```bash
cat <<EOF > values-airflow-lab.yaml
airflowVersion: "2.8.0"
executor: KubernetesExecutor
database:
  type: postgres
  postgres:
    enabled: true
redis:
  enabled: false
webserver:
  replicas: 1
  resources:
    requests:
      cpu: 200m
      memory: 512Mi
scheduler:
  replicas: 1
  resources:
    requests:
      cpu: 200m
      memory: 512Mi
workers:
  replicas: 0
dags:
  gitSync:
    enabled: false
config:
  core:
    load_examples: False
EOF

helm install airflow apache-airflow/airflow -n bigdata -f values-airflow-lab.yaml --timeout 10m

kubectl get pods -n bigdata -l app.kubernetes.io/name=airflow

kubectl port-forward svc/airflow-webserver 8053:8080 -n bigdata &
```

### 练习3：提交Spark作业到K8s（20min）

```bash
kubectl create serviceaccount spark -n bigdata
kubectl create clusterrolebinding spark-role --clusterrole=edit --serviceaccount=bigdata:spark

kubectl apply -f - <<EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: spark-config
  namespace: bigdata
data:
  spark-defaults.conf: |
    spark.kubernetes.container.image=spark:3.5.0
    spark.kubernetes.authenticate.driver.serviceAccountName=spark
    spark.kubernetes.namespace=bigdata
EOF

/spark/bin/spark-submit \
  --master k8s://https://$(kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}') \
  --deploy-mode cluster \
  --name spark-pi \
  --class org.apache.spark.examples.SparkPi \
  --conf spark.kubernetes.container.image=spark:3.5.0 \
  --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
  --conf spark.kubernetes.namespace=bigdata \
  --conf spark.driver.cores=1 \
  --conf spark.driver.memory=1g \
  --conf spark.executor.cores=1 \
  --conf spark.executor.memory=1g \
  --conf spark.executor.instances=2 \
  local:///opt/spark/examples/jars/spark-examples_2.12-3.5.0.jar \
  100

kubectl get pods -n bigdata -l spark-app-name=spark-pi

kubectl logs -n bigdata -l spark-app-name=spark-pi --tail=20
```

---

## 九、课后作业

### 必做

1. **湖仓环境部署**：在K8s上部署完整的湖仓环境（MinIO + Iceberg + Trino），要求：
   - MinIO作为S3兼容存储，创建warehouse和iceberg-data两个Bucket
   - Hive Metastore作为Iceberg Catalog
   - Trino Coordinator + 2个Worker，能查询Iceberg表
   - 验证：通过Trino创建Iceberg表并写入查询数据

2. **Helm Values自定义**：编写Helm Values文件，自定义以下配置：
   - MinIO: 修改默认密码、配置4副本分布式模式、设置资源限制
   - Trino: 调整query.max-memory、增加Iceberg Catalog配置、配置S3端点
   - Airflow: 配置KubernetesExecutor、设置GitSync、配置环境变量

3. **多租户隔离**：配置资源配额实现多租户隔离，要求：
   - 创建team-alpha和team-beta两个Namespace
   - 每个Namespace配置ResourceQuota和LimitRange
   - 配置PriorityClass，生产任务优先级高于开发任务
   - 验证：当资源不足时，低优先级任务被抢占

### 选做

1. 搭建Prometheus + Grafana监控K8s上的大数据组件
2. 配置Ingress实现外部访问MinIO/Trino/Airflow
3. 编写Airflow DAG，在K8s上提交Spark作业查询Iceberg数据

---

## 十、参考资料

- [Kubernetes官方文档](https://kubernetes.io/docs/home/)
- [Kind官方文档](https://kind.sigs.k8s.io/)
- [Minikube官方文档](https://minikube.sigs.k8s.io/docs/)
- [Helm官方文档](https://helm.sh/docs/)
- [MinIO Helm Chart](https://github.com/minio/charts)
- [Apache Airflow Helm Chart](https://airflow.apache.org/docs/helm-chart/stable/)
- [Trino on Kubernetes](https://trino.io/docs/current/installation/kubernetes.html)
- [Spark on Kubernetes](https://spark.apache.org/docs/latest/running-on-kubernetes.html)
- [K8s Resource Quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/)
