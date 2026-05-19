# 课时33：数据测试与CI/CD

> **所属阶段**：L4 架构师 | **模块**：补充模块_dbt与现代数据栈 | **课时**：3h | **难度**：★★★★★

---

## 一、教学目标

1. 理解数据测试金字塔，掌握从单元测试到端到端测试的分层策略
2. 掌握pytest + PySpark测试Spark ETL逻辑的方法
3. 掌握dbt test集成到CI流水线的方法
4. 掌握Great Expectations Checkpoint作为CI门禁的实现
5. 了解数据版本控制：DVC数据版本管理与LakeFS Git-like数据分支
6. 掌握GitHub Actions构建数据管道CI/CD流水线
7. 理解数据质量门禁机制，实现质量检查不通过阻止下游发布
8. 了解生产实践：蓝绿部署数据管道、Canary发布新模型

---

## 二、数据测试金字塔

### 2.1 测试金字塔模型

```
数据测试金字塔（从底到顶，数量递减，成本递增）:

                    ┌─────────────┐
                    │  端到端测试  │  ← 少量，验证完整数据流
                    │  E2E Test   │     数据源→ETL→数仓→BI
                    └──────┬──────┘
                           │
                ┌──────────┴──────────┐
                │    集成测试          │  ← 中等数量，验证模块间交互
                │  Integration Test   │     模型间引用、上下游一致性
                └──────────┬──────────┘
                           │
            ┌──────────────┴──────────────┐
            │       单元测试               │  ← 大量，验证单个逻辑
            │     Unit Test               │     单个SQL、单个UDF、单个转换
            └──────────────┬──────────────┘
                           │
        ┌──────────────────┴──────────────────┐
        │         数据质量门禁                  │  ← 贯穿所有层
        │    Data Quality Gate                 │     不通过则阻止发布
        └──────────────────────────────────────┘

各层测试对比:
  ┌────────────┬──────────────────────┬──────────────┬──────────────┐
  │  测试层级  │  验证内容             │  运行速度    │  维护成本    │
  ├────────────┼──────────────────────┼──────────────┼──────────────┤
  │  单元测试  │  单个转换逻辑         │  毫秒~秒     │  低          │
  │  集成测试  │  模型间数据一致性     │  秒~分钟     │  中          │
  │  端到端测试│  完整管道输出正确性   │  分钟~小时   │  高          │
  │  质量门禁  │  关键指标阈值检查     │  秒~分钟     │  中          │
  └────────────┴──────────────────────┴──────────────┴──────────────┘
```

### 2.2 数据测试与软件测试的区别

```
数据测试 vs 软件测试:

  ┌──────────────────────────────────────────────────────────────────┐
  │  软件测试                        数据测试                        │
  │  ─────────                       ─────────                      │
  │  输入确定，输出确定              输入不确定，输出有概率性         │
  │  测试代码逻辑                    测试数据特征                    │
  │  Pass/Fail二值                   Pass/Warn/Fail三值             │
  │  测试环境与生产隔离              测试数据就是生产数据的一部分     │
  │  回归测试覆盖已知Bug             数据漂移随时可能发生            │
  │  Mock外部依赖                    需要真实数据样本                │
  │                                                                  │
  │  数据测试的独特挑战:                                             │
  │  1. 数据量巨大，全量测试不现实                                   │
  │  2. 数据持续变化，昨天的测试今天可能失败                         │
  │  3. 业务规则隐含在数据中，难以显式表达                           │
  │  4. 上游数据变更可能影响下游，需要端到端验证                     │
  └──────────────────────────────────────────────────────────────────┘
```

---

## 三、pytest + PySpark：测试Spark ETL逻辑

### 3.1 测试环境搭建

```bash
pip install pytest pyspark pytest-spark chispa
```

### 3.2 conftest.py：Spark Session Fixture

```python
import pytest
from pyspark.sql import SparkSession

@pytest.fixture(scope="session")
def spark():
    spark = SparkSession.builder \
        .master("local[*]") \
        .appName("pytest-spark") \
        .config("spark.sql.shuffle.partitions", "4") \
        .config("spark.default.parallelism", "4") \
        .config("spark.ui.enabled", "false") \
        .config("spark.sql.warehouse.dir", "/tmp/spark-warehouse-test") \
        .getOrCreate()
    yield spark
    spark.stop()
```

### 3.3 单元测试：测试单个转换函数

```python
from pyspark.sql import Row
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType
import pytest

def transform_order_status(df):
    return df.withColumn(
        "order_status_cn",
        when(col("order_status") == "CREATED", "待支付")
        .when(col("order_status") == "PAID", "已支付")
        .when(col("order_status") == "COMPLETED", "已完成")
        .when(col("order_status") == "CANCELLED", "已取消")
        .when(col("order_status") == "REFUNDED", "已退款")
        .otherwise("未知")
    )

def test_transform_order_status_known_values(spark):
    input_data = [
        Row(order_id=1, order_status="CREATED"),
        Row(order_id=2, order_status="PAID"),
        Row(order_id=3, order_status="COMPLETED"),
        Row(order_id=4, order_status="CANCELLED"),
        Row(order_id=5, order_status="REFUNDED"),
    ]
    schema = StructType([
        StructField("order_id", LongType(), False),
        StructField("order_status", StringType(), False),
    ])
    df = spark.createDataFrame(input_data, schema)
    result = transform_order_status(df)
    rows = result.select("order_status", "order_status_cn").collect()
    mapping = {row["order_status"]: row["order_status_cn"] for row in rows}
    assert mapping["CREATED"] == "待支付"
    assert mapping["PAID"] == "已支付"
    assert mapping["COMPLETED"] == "已完成"
    assert mapping["CANCELLED"] == "已取消"
    assert mapping["REFUNDED"] == "已退款"

def test_transform_order_status_unknown_value(spark):
    input_data = [Row(order_id=1, order_status="UNKNOWN")]
    schema = StructType([
        StructField("order_id", LongType(), False),
        StructField("order_status", StringType(), False),
    ])
    df = spark.createDataFrame(input_data, schema)
    result = transform_order_status(df)
    row = result.select("order_status_cn").first()
    assert row["order_status_cn"] == "未知"
```

### 3.4 单元测试：测试金额计算逻辑

```python
from pyspark.sql import Row
from pyspark.sql.types import StructType, StructField, DoubleType, LongType
from pyspark.sql.functions import col

def calculate_order_metrics(df):
    return df.withColumn(
        "actual_payment",
        when(col("payment_amount").isNotNull(), col("payment_amount")).otherwise(0)
    ).withColumn(
        "payment_ratio",
        when(col("total_amount") > 0, col("actual_payment") / col("total_amount")).otherwise(0)
    )

def test_calculate_order_metrics_with_payment(spark):
    input_data = [
        Row(order_id=1, total_amount=100.0, payment_amount=100.0),
        Row(order_id=2, total_amount=200.0, payment_amount=150.0),
    ]
    schema = StructType([
        StructField("order_id", LongType(), False),
        StructField("total_amount", DoubleType(), False),
        StructField("payment_amount", DoubleType(), True),
    ])
    df = spark.createDataFrame(input_data, schema)
    result = calculate_order_metrics(df)
    rows = {row["order_id"]: row for row in result.collect()}
    assert rows[1]["actual_payment"] == 100.0
    assert abs(rows[1]["payment_ratio"] - 1.0) < 0.001
    assert rows[2]["actual_payment"] == 150.0
    assert abs(rows[2]["payment_ratio"] - 0.75) < 0.001

def test_calculate_order_metrics_without_payment(spark):
    input_data = [
        Row(order_id=1, total_amount=100.0, payment_amount=None),
    ]
    schema = StructType([
        StructField("order_id", LongType(), False),
        StructField("total_amount", DoubleType(), False),
        StructField("payment_amount", DoubleType(), True),
    ])
    df = spark.createDataFrame(input_data, schema)
    result = calculate_order_metrics(df)
    row = result.first()
    assert row["actual_payment"] == 0.0
    assert row["payment_ratio"] == 0.0
```

### 3.5 集成测试：测试ETL管道

```python
from pyspark.sql import Row
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType, IntegerType
from pyspark.sql.functions import col, sum as spark_sum, count as spark_count

def run_order_etl(spark, orders_df, details_df, users_df):
    orders_clean = orders_df.filter(
        col("order_id").isNotNull() & col("user_id").isNotNull() & (col("total_amount") >= 0)
    )
    details_agg = details_df.groupBy("order_id").agg(
        spark_count("*").alias("item_count"),
        spark_sum("subtotal").alias("calculated_total")
    )
    result = orders_clean.join(details_agg, "order_id", "left").join(users_df, "user_id", "left")
    return result

def test_order_etl_integration(spark):
    orders_data = [
        Row(order_id=1, user_id=101, total_amount=300.0, order_status="PAID"),
        Row(order_id=2, user_id=102, total_amount=500.0, order_status="CREATED"),
        Row(order_id=3, user_id=None, total_amount=100.0, order_status="PAID"),
    ]
    orders_schema = StructType([
        StructField("order_id", LongType(), False),
        StructField("user_id", LongType(), True),
        StructField("total_amount", DoubleType(), False),
        StructField("order_status", StringType(), False),
    ])
    orders_df = spark.createDataFrame(orders_data, orders_schema)

    details_data = [
        Row(order_id=1, product_id=1, subtotal=200.0),
        Row(order_id=1, product_id=2, subtotal=100.0),
        Row(order_id=2, product_id=3, subtotal=500.0),
    ]
    details_schema = StructType([
        StructField("order_id", LongType(), False),
        StructField("product_id", LongType(), False),
        StructField("subtotal", DoubleType(), False),
    ])
    details_df = spark.createDataFrame(details_data, details_schema)

    users_data = [
        Row(user_id=101, user_name="张三"),
        Row(user_id=102, user_name="李四"),
    ]
    users_schema = StructType([
        StructField("user_id", LongType(), False),
        StructField("user_name", StringType(), False),
    ])
    users_df = spark.createDataFrame(users_data, users_schema)

    result = run_order_etl(spark, orders_df, details_df, users_df)
    assert result.count() == 2
    order_ids = [row["order_id"] for row in result.collect()]
    assert 1 in order_ids
    assert 2 in order_ids
    assert 3 not in order_ids

    order1 = result.filter(col("order_id") == 1).first()
    assert order1["item_count"] == 2
    assert abs(order1["calculated_total"] - 300.0) < 0.01
    assert order1["user_name"] == "张三"
```

### 3.6 使用chispa进行DataFrame比较

```python
from chispa.dataframe_comparer import assert_df_equality

def test_transform_output_matches_expected(spark):
    input_data = [
        (1, "CREATED", 100.0),
        (2, "PAID", 200.0),
    ]
    input_df = spark.createDataFrame(input_data, ["order_id", "order_status", "total_amount"])

    expected_data = [
        (1, "CREATED", 100.0, "待支付"),
        (2, "PAID", 200.0, "已支付"),
    ]
    expected_df = spark.createDataFrame(expected_data, ["order_id", "order_status", "total_amount", "order_status_cn"])

    result_df = transform_order_status(input_df)
    assert_df_equality(result_df, expected_df, ignore_nullable=True)
```

### 3.7 pytest配置

```ini
pytest.ini:

[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
markers =
    unit: 单元测试
    integration: 集成测试
    e2e: 端到端测试
    slow: 慢速测试
```

---

## 四、dbt test集成到CI

### 4.1 dbt CI脚本

```bash
scripts/ci_dbt_test.sh:

#!/bin/bash
set -e

echo "=== dbt CI Pipeline ==="

echo "--- Step 1: dbt deps ---"
dbt deps --profiles-dir profiles

echo "--- Step 2: dbt parse ---"
dbt parse --profiles-dir profiles

echo "--- Step 3: dbt compile ---"
dbt compile --profiles-dir profiles

echo "--- Step 4: dbt test (staging) ---"
dbt test --select staging --profiles-dir profiles

echo "--- Step 5: dbt test (intermediate) ---"
dbt test --select intermediate --profiles-dir profiles

echo "--- Step 6: dbt test (marts) ---"
dbt test --select marts --profiles-dir profiles

echo "--- Step 7: dbt test (custom) ---"
dbt test --select test_type:singular --profiles-dir profiles

echo "=== All dbt tests passed ==="
```

### 4.2 dbt CI环境配置

```yaml
profiles/ci/profiles.yml:

ecommerce_warehouse:
  target: ci
  outputs:
    ci:
      type: duckdb
      path: "./ci_data/ci.duckdb"
      threads: 2
```

### 4.3 dbt PR检查脚本

```bash
scripts/dbt_pr_check.sh:

#!/bin/bash
set -e

CHANGED_MODELS=$(git diff --name-only origin/main...HEAD | \
    grep "models/" | \
    sed 's/models\///g' | \
    sed 's/\.sql$//g' | \
    tr '/' '.')

if [ -z "$CHANGED_MODELS" ]; then
    echo "No model changes detected, skipping dbt tests"
    exit 0
fi

echo "Changed models: $CHANGED_MODELS"

echo "--- Running dbt compile ---"
dbt compile --profiles-dir profiles

for model in $CHANGED_MODELS; do
    echo "--- Testing model: $model ---"
    dbt test --select "$model" --profiles-dir profiles
done

echo "--- Running upstream/downstream tests ---"
dbt test --select "staging.*+1_tag:ci" --profiles-dir profiles

echo "=== PR check passed ==="
```

---

## 五、Great Expectations Checkpoint作为CI门禁

### 5.1 GE Checkpoint配置

```yaml
great_expectations/checkpoints/ods_quality_gate.yml:

name: ods_quality_gate
config_version: 1.0
template_name:
module_name: great_expectations.checkpoint
class_name: Checkpoint
run_name_template: "%Y%m%d-%H%M%S-ods-quality-gate"
expectation_suite_name: ods_order_info_suite
batch_request:
    datasource_name: spark_datasource
    data_connector_name: default_runtime_data_connector_name
    data_asset_name: ods_order_info
action_list:
    - name: store_validation_result
      action:
        class_name: StoreValidationResultAction
    - name: store_evaluation_params
      action:
        class_name: StoreEvaluationParametersAction
    - name: update_data_docs
      action:
        class_name: UpdateDataDocsAction
    - name: send_slack_notification
      action:
        class_name: SlackNotificationAction
        slack_webhook: ${SLACK_WEBHOOK}
        notify_on: failure
        notify_with: all
evaluation_parameters: {}
runtime_configuration: {}
```

### 5.2 GE门禁脚本

```python
scripts/ge_quality_gate.py:

import great_expectations as gx
import sys

def run_quality_gate(suite_name, table_name, min_pass_rate=0.95):
    context = gx.get_context()
    checkpoint = context.get_checkpoint(f"{suite_name}_quality_gate")
    result = checkpoint.run()
    success = result.get("success", False)
    run_results = result.get("run_results", {})

    total_expectations = 0
    passed_expectations = 0

    for run_result in run_results.values():
        validation_result = run_result.get("validation_result", {})
        stats = validation_result.get("statistics", {})
        total_expectations += stats.get("evaluated_expectations", 0)
        passed_expectations += stats.get("successful_expectations", 0)

    if total_expectations > 0:
        pass_rate = passed_expectations / total_expectations
    else:
        pass_rate = 0

    print(f"质量门禁结果: {table_name}")
    print(f"  总规则数: {total_expectations}")
    print(f"  通过规则数: {passed_expectations}")
    print(f"  通过率: {pass_rate:.2%}")
    print(f"  门禁阈值: {min_pass_rate:.2%}")
    print(f"  最终结果: {'PASS' if success and pass_rate >= min_pass_rate else 'FAIL'}")

    if not success or pass_rate < min_pass_rate:
        sys.exit(1)

if __name__ == "__main__":
    suite_name = sys.argv[1]
    table_name = sys.argv[2]
    min_pass_rate = float(sys.argv[3]) if len(sys.argv) > 3 else 0.95
    run_quality_gate(suite_name, table_name, min_pass_rate)
```

### 5.3 多层级质量门禁

```python
scripts/multi_layer_quality_gate.py:

import great_expectations as gx
import sys

QUALITY_GATE_CONFIG = {
    "staging": {
        "suites": ["ods_order_info_suite", "ods_order_detail_suite", "ods_users_suite"],
        "min_pass_rate": 0.90,
        "severity": "warn",
    },
    "intermediate": {
        "suites": ["dwd_order_detail_suite"],
        "min_pass_rate": 0.95,
        "severity": "error",
    },
    "marts": {
        "suites": ["dws_trade_user_order_day_suite", "fct_orders_suite"],
        "min_pass_rate": 0.99,
        "severity": "block",
    },
}

def run_multi_layer_gate(layer=None):
    context = gx.get_context()
    all_passed = True

    for layer_name, config in QUALITY_GATE_CONFIG.items():
        if layer and layer_name != layer:
            continue

        print(f"\n{'='*60}")
        print(f"质量门禁: {layer_name}层")
        print(f"{'='*60}")

        layer_passed = True
        for suite_name in config["suites"]:
            try:
                checkpoint = context.get_checkpoint(f"{suite_name}_quality_gate")
                result = checkpoint.run()
                success = result.get("success", False)
                status = "PASS" if success else "FAIL"
                print(f"  {suite_name}: {status}")
                if not success:
                    layer_passed = False
            except Exception as e:
                print(f"  {suite_name}: ERROR - {e}")
                layer_passed = False

        if not layer_passed:
            severity = config["severity"]
            if severity == "block":
                print(f"  → {layer_name}层质量门禁未通过，阻止发布！")
                all_passed = False
            elif severity == "error":
                print(f"  → {layer_name}层质量门禁未通过，标记为错误！")
                all_passed = False
            elif severity == "warn":
                print(f"  → {layer_name}层质量门禁未通过，发出警告")
        else:
            print(f"  → {layer_name}层质量门禁通过 ✓")

    if not all_passed:
        sys.exit(1)

if __name__ == "__main__":
    layer = sys.argv[1] if len(sys.argv) > 1 else None
    run_multi_layer_gate(layer)
```

---

## 六、数据版本控制

### 6.1 DVC数据版本管理

```
DVC工作流:

  ┌──────────────────────────────────────────────────────────────────┐
  │  Git (代码版本)              DVC (数据版本)                      │
  │                                                                  │
  │  git add model.sql            dvc add data/raw_orders.parquet   │
  │  git commit -m "update"       → 生成 data/raw_orders.parquet.dvc│
  │  git push                       记录文件的MD5哈希和远程路径      │
  │                                                                  │
  │                                dvc push                          │
  │                                  → 上传数据到远程存储             │
  │                                    (S3/GCS/Azure/本地)           │
  │                                                                  │
  │  git checkout v1.0            dvc checkout                       │
  │                                → 自动下载对应版本的数据           │
  └──────────────────────────────────────────────────────────────────┘
```

#### DVC初始化与配置

```bash
pip install dvc dvc-s3

cd ecommerce_warehouse

git init
dvc init

dvc remote add -d myremote s3://ecommerce-dvc-store
dvc remote modify myremote endpointurl http://minio:9000
dvc remote modify myremote access_key_id admin
dvc remote modify myremote secret_access_key admin123456
```

#### DVC数据版本追踪

```bash
dvc add data/raw_orders.parquet

git add data/raw_orders.parquet.dvc data/.gitignore
git commit -m "track raw_orders v1"

dvc push

dvc run -n stage_stg_orders \
    -d data/raw_orders.parquet \
    -o data/stg_orders.parquet \
    "dbt run --select stg_orders"

dvc run -n stage_fct_orders \
    -d data/stg_orders.parquet \
    -o data/fct_orders.parquet \
    "dbt run --select fct_orders"

dvc dag
```

#### DVC实验管理

```bash
dvc exp run -n experiment_v2

dvc exp show

dvc exp apply experiment_v2

dvc exp push myremote experiment_v2
```

### 6.2 LakeFS：Git-like数据分支

```
LakeFS核心概念:

  ┌──────────────────────────────────────────────────────────────────┐
  │  LakeFS = 数据湖上的Git                                         │
  │                                                                  │
  │  Git概念          LakeFS对应                                     │
  │  ────────         ────────────                                   │
  │  Repository       Repository (S3 Bucket / GCS Bucket)           │
  │  Branch           Branch (数据分支，隔离写入)                    │
  │  Commit           Commit (数据快照，不可变)                      │
  │  Merge            Merge (合并数据分支)                           │
  │  Revert           Revert (回滚数据到之前快照)                    │
  │  Diff             Diff (比较两个分支的数据差异)                  │
  │                                                                  │
  │  典型工作流:                                                     │
  │                                                                  │
  │  main分支 (生产)                                                 │
  │    │                                                             │
  │    ├── lakectl branch create etl-v2                              │
  │    │       │                                                     │
  │    │       ├── 写入新数据到etl-v2分支                            │
  │    │       ├── 运行dbt test验证                                  │
  │    │       ├── lakectl diff main etl-v2  (查看差异)              │
  │    │       ├── lakectl merge etl-v2 main  (验证通过后合并)       │
  │    │       └── lakectl branch delete etl-v2                      │
  │    │                                                             │
  │    └── 如果验证失败，直接删除分支，生产数据不受影响               │
  └──────────────────────────────────────────────────────────────────┘
```

#### LakeFS部署

```yaml
docker-compose-lakefs.yml:

version: '3.8'

services:
  lakefs-db:
    image: postgres:14
    environment:
      POSTGRES_DB: lakefs
      POSTGRES_USER: lakefs
      POSTGRES_PASSWORD: lakefs
    volumes:
      - lakefs_db_data:/var/lib/postgresql/data

  lakefs:
    image: treeverse/lakefs:1.8
    ports:
      - "8000:8000"
    depends_on:
      - lakefs-db
    environment:
      LAKEFS_DATABASE_TYPE: postgres
      LAKEFS_DATABASE_POSTGRES_CONNECTION_STRING: postgres://lakefs:lakefs@lakefs-db:5432/lakefs?sslmode=disable
      LAKEFS_AUTH_ENCRYPT_SECRET_KEY: "some-secret-key-min-32-chars!!"
      LAKEFS_BLOCKSTORE_TYPE: local
      LAKEFS_BLOCKSTORE_LOCAL_PATH: /home/lakefs
      LAKEFS_LOGGING_LEVEL: INFO
    volumes:
      - lakefs_data:/home/lakefs

volumes:
  lakefs_db_data:
  lakefs_data:
```

```bash
docker-compose -f docker-compose-lakefs.yml up -d

lakectl config --host http://localhost:8000
lakectl repo create lakefs://ecommerce-warehouse s3://ecommerce-warehouse
```

#### LakeFS数据分支操作

```bash
lakectl branch list lakefs://ecommerce-warehouse

lakectl branch create lakefs://ecommerce-warehouse/etl-v2 --source lakefs://ecommerce-warehouse/main

lakectl fs upload lakefs://ecommerce-warehouse/etl-v2/data/orders.parquet --source ./data/orders.parquet

lakectl diff lakefs://ecommerce-warehouse/main lakefs://ecommerce-warehouse/etl-v2

lakectl commit lakefs://ecommerce-warehouse/etl-v2 -m "Add new orders data"

lakectl merge lakefs://ecommerce-warehouse/etl-v2 lakefs://ecommerce-warehouse/main -m "Merge ETL v2"

lakectl branch delete lakefs://ecommerce-warehouse/etl-v2

lakectl log lakefs://ecommerce-warehouse/main

lakectl branch revert lakefs://ecommerce-warehouse/main --commit_ref <commit_id>
```

---

## 七、CI/CD流水线

### 7.1 GitHub Actions + dbt test + Great Expectations

```yaml
.github/workflows/data_pipeline_ci.yml:

name: Data Pipeline CI

on:
  pull_request:
    branches: [main]
    paths:
      - 'models/**'
      - 'macros/**'
      - 'tests/**'
      - 'snapshots/**'
      - 'seeds/**'
      - 'dbt_project.yml'
      - 'packages.yml'

env:
  DBT_PROFILES_DIR: ./profiles

jobs:
  dbt-compile:
    name: dbt编译检查
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install dbt-core dbt-duckdb dbt-postgres
          dbt deps

      - name: dbt compile
        run: dbt compile

  dbt-test:
    name: dbt数据测试
    runs-on: ubuntu-latest
    needs: dbt-compile
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install dbt-core dbt-duckdb
          dbt deps

      - name: dbt seed
        run: dbt seed

      - name: dbt run (staging)
        run: dbt run --select staging.*

      - name: dbt run (intermediate)
        run: dbt run --select intermediate.*

      - name: dbt run (marts)
        run: dbt run --select marts.*

      - name: dbt test
        run: dbt test

      - name: dbt test (singular/custom)
        run: dbt test --select test_type:singular

  quality-gate:
    name: 数据质量门禁
    runs-on: ubuntu-latest
    needs: dbt-test
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install great-expectations pandas

      - name: Run quality gate
        run: |
          python scripts/ge_quality_gate.py ods_order_info ods.ods_order_info 0.95
          python scripts/ge_quality_gate.py dwd_order_detail dwd.dwd_order_detail 0.95
          python scripts/ge_quality_gate.py dws_trade_user_order_day dws.dws_trade_user_order_day 0.99

  spark-unit-test:
    name: Spark ETL单元测试
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install pyspark pytest chispa
          pip install -r requirements.txt

      - name: Run unit tests
        run: pytest tests/unit -v --tb=short

      - name: Run integration tests
        run: pytest tests/integration -v --tb=short
```

### 7.2 完整的CD流水线

```yaml
.github/workflows/data_pipeline_cd.yml:

name: Data Pipeline CD

on:
  push:
    branches: [main]
    paths:
      - 'models/**'
      - 'macros/**'
      - 'tests/**'
      - 'dbt_project.yml'

env:
  DBT_PROFILES_DIR: ./profiles

jobs:
  deploy-staging:
    name: 部署到Staging环境
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install dbt-core dbt-postgres
          dbt deps

      - name: dbt seed
        run: dbt seed --target staging

      - name: dbt run
        run: dbt run --target staging

      - name: dbt test
        run: dbt test --target staging

      - name: Run quality gate
        run: python scripts/multi_layer_quality_gate.py

      - name: Generate docs
        run: dbt docs generate --target staging

      - name: Upload docs artifact
        uses: actions/upload-artifact@v4
        with:
          name: dbt-docs
          path: target/

  deploy-production:
    name: 部署到Production环境
    runs-on: ubuntu-latest
    needs: deploy-staging
    environment: production
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install dbt-core dbt-postgres
          dbt deps

      - name: dbt run (production)
        run: dbt run --target prod

      - name: dbt test (production)
        run: dbt test --target prod

      - name: Run production quality gate
        run: python scripts/multi_layer_quality_gate.py marts

      - name: dbt snapshot
        run: dbt snapshot --target prod

      - name: Generate production docs
        run: dbt docs generate --target prod

      - name: Deploy docs to S3
        run: aws s3 sync target/ s3://dbt-docs-bucket/ --delete
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

      - name: Notify deployment
        if: always()
        run: |
          curl -X POST "${{ secrets.SLACK_WEBHOOK }}" \
            -H "Content-Type: application/json" \
            -d '{"text":"数据管道部署 ${{ job.status }}: ${{ github.event.head_commit.message }}"}'
```

---

## 八、数据质量门禁

### 8.1 门禁机制设计

```
数据质量门禁架构:

  ┌──────────────────────────────────────────────────────────────────┐
  │                     CI/CD Pipeline                                │
  │                                                                  │
  │  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   │
  │  │  代码提交 │──→│  编译检查 │──→│  单元测试 │──→│  集成测试 │   │
  │  └──────────┘   └──────────┘   └──────────┘   └──────┬───┘   │
  │                                                       │         │
  │                              ┌─────────────────────────┘        │
  │                              ▼                                  │
  │                    ┌──────────────────┐                         │
  │                    │  数据质量门禁     │                         │
  │                    │  ┌────────────┐  │                         │
  │                    │  │ dbt test   │  │                         │
  │                    │  │ GE check   │  │                         │
  │                    │  │ 行数波动   │  │                         │
  │                    │  │ 指标异常   │  │                         │
  │                    │  └─────┬──────┘  │                         │
  │                    │        │         │                         │
  │                    │   PASS ↓ FAIL    │                         │
  │                    └───┬────────┬─────┘                         │
  │                        │        │                                │
  │                   ┌────▼──┐ ┌───▼────┐                         │
  │                   │ 继续部署│ │ 阻止发布│                         │
  │                   └───────┘ └────────┘                         │
  └──────────────────────────────────────────────────────────────────┘
```

### 8.2 门禁规则配置

```yaml
quality_gates/config.yml:

gates:
  - name: staging_gate
    description: "Staging层质量门禁"
    rules:
      - type: dbt_test
        select: "staging.*"
        min_pass_rate: 0.90
        action: warn
      - type: row_count_check
        table: staging.stg_orders
        min_rows: 100
        max_change_rate: 0.5
        action: warn
      - type: freshness_check
        table: source.raw_ecommerce.orders
        max_delay_hours: 12
        action: error

  - name: marts_gate
    description: "Marts层质量门禁"
    rules:
      - type: dbt_test
        select: "marts.*"
        min_pass_rate: 0.99
        action: block
      - type: metric_anomaly
        table: marts.finance.fct_orders
        metric: sum(total_amount)
        compare_to: yesterday
        max_change_rate: 0.3
        action: block
      - type: cross_check
        source_table: marts.finance.fct_orders
        source_metric: sum(total_amount)
        target_table: marts.finance.fct_payments
        target_metric: sum(payment_amount)
        tolerance: 0.01
        action: block
```

### 8.3 门禁执行脚本

```python
scripts/quality_gate_runner.py:

import yaml
import subprocess
import sys

def load_gate_config(config_path="quality_gates/config.yml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def run_dbt_test(select, min_pass_rate):
    result = subprocess.run(
        ["dbt", "test", "--select", select, "--output", "json", "--output-path", "target/test-results"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return False, 0.0
    pass_rate = 1.0
    return pass_rate >= min_pass_rate, pass_rate

def check_row_count(table, min_rows, max_change_rate):
    result = subprocess.run(
        ["dbt", "run-operation", "check_row_count", "--args", f"'{{table: {table}, min_rows: {min_rows}}}'"],
        capture_output=True, text=True
    )
    return result.returncode == 0

def run_quality_gate(gate_name):
    config = load_gate_config()
    gate = None
    for g in config["gates"]:
        if g["name"] == gate_name:
            gate = g
            break

    if not gate:
        print(f"Gate {gate_name} not found")
        sys.exit(1)

    print(f"Running quality gate: {gate_name}")
    print(f"Description: {gate['description']}")

    all_passed = True
    for rule in gate["rules"]:
        print(f"\n  Rule: {rule['type']} - {rule.get('description', '')}")

        if rule["type"] == "dbt_test":
            passed, rate = run_dbt_test(rule["select"], rule["min_pass_rate"])
            status = "PASS" if passed else "FAIL"
            print(f"    Result: {status} (pass_rate={rate:.2%}, threshold={rule['min_pass_rate']:.2%})")

        elif rule["type"] == "row_count_check":
            passed = check_row_count(rule["table"], rule["min_rows"], rule["max_change_rate"])
            status = "PASS" if passed else "FAIL"
            print(f"    Result: {status}")

        else:
            print(f"    Unknown rule type: {rule['type']}")
            continue

        if not passed:
            action = rule.get("action", "warn")
            if action == "block":
                print(f"    → BLOCKED: 质量门禁阻止发布！")
                all_passed = False
            elif action == "error":
                print(f"    → ERROR: 质量检查失败！")
                all_passed = False
            elif action == "warn":
                print(f"    → WARN: 质量检查未通过，发出警告")

    if not all_passed:
        sys.exit(1)

if __name__ == "__main__":
    gate_name = sys.argv[1]
    run_quality_gate(gate_name)
```

---

## 九、生产实践

### 9.1 蓝绿部署数据管道

```
蓝绿部署数据管道:

  ┌──────────────────────────────────────────────────────────────────┐
  │  蓝环境（当前生产）                                              │
  │                                                                  │
  │  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   │
  │  │ stg_v1   │──→│ int_v1   │──→│ fct_v1   │──→│ BI报表   │   │
  │  └──────────┘   └──────────┘   └──────────┘   └──────────┘   │
  │                                                                  │
  │  绿环境（新版本验证）                                            │
  │                                                                  │
  │  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   │
  │  │ stg_v2   │──→│ int_v2   │──→│ fct_v2   │──→│ 验证对比  │   │
  │  └──────────┘   └──────────┘   └──────────┘   └──────────┘   │
  │                                                                  │
  │  切换流程:                                                       │
  │  1. 部署绿环境，运行dbt run到_v2 Schema                        │
  │  2. 运行dbt test验证绿环境数据质量                              │
  │  3. 对比蓝绿环境关键指标                                        │
  │  4. 验证通过 → 切换BI查询到绿环境                               │
  │  5. 验证失败 → 删除绿环境，蓝环境不受影响                       │
  └──────────────────────────────────────────────────────────────────┘
```

```sql
macros/blue_green_deploy.sql:

{% macro blue_green_deploy(model_name, version) %}
    {% set target_schema = api.Relation.create(
        schema=model_name ~ '_v' ~ version
    ) %}
    {{ config(schema=target_schema) }}
{% endmacro %}
```

### 9.2 Canary发布新模型

```
Canary发布流程:

  ┌──────────────────────────────────────────────────────────────────┐
  │  Step 1: 新模型写入独立Schema                                    │
  │                                                                  │
  │  marts.finance.fct_orders        ← 当前生产（100%流量）          │
  │  marts.finance_canary.fct_orders ← 新模型（0%流量）              │
  │                                                                  │
  │  Step 2: 对比验证                                                │
  │                                                                  │
  │  SELECT                                                         │
  │      'production' AS env,                                       │
  │      COUNT(*) AS row_count,                                     │
  │      SUM(total_amount) AS total                                 │
  │  FROM marts.finance.fct_orders                                  │
  │  UNION ALL                                                      │
  │  SELECT                                                         │
  │      'canary' AS env,                                           │
  │      COUNT(*) AS row_count,                                     │
  │      SUM(total_amount) AS total                                 │
  │  FROM marts.finance_canary.fct_orders                           │
  │                                                                  │
  │  Step 3: 逐步切流                                                │
  │                                                                  │
  │  10%流量 → canary → 验证1小时 → 30% → 验证4小时 → 100%        │
  │                                                                  │
  │  Step 4: 全量切换或回滚                                          │
  │                                                                  │
  │  验证通过: RENAME fct_orders TO fct_orders_old                  │
  │           RENAME fct_orders_canary TO fct_orders                │
  │  验证失败: DROP fct_orders_canary                               │
  └──────────────────────────────────────────────────────────────────┘
```

### 9.3 Canary对比脚本

```python
scripts/canary_compare.py:

import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, sum as spark_sum, abs as spark_abs

def compare_tables(spark, prod_table, canary_table, key_column, metric_columns):
    prod_df = spark.table(prod_table)
    canary_df = spark.table(canary_table)

    prod_count = prod_df.count()
    canary_count = canary_df.count()
    count_diff_pct = abs(prod_count - canary_count) / max(prod_count, 1) * 100

    print(f"行数对比: 生产={prod_count}, Canary={canary_count}, 差异={count_diff_pct:.2f}%")

    if count_diff_pct > 5:
        print("行数差异超过5%，Canary验证失败！")
        return False

    for metric_col in metric_columns:
        prod_metric = prod_df.agg(spark_sum(col(metric_col)).alias("total")).first()["total"] or 0
        canary_metric = canary_df.agg(spark_sum(col(metric_col)).alias("total")).first()["total"] or 0
        metric_diff_pct = abs(prod_metric - canary_metric) / max(abs(prod_metric), 1) * 100

        print(f"指标对比 [{metric_col}]: 生产={prod_metric:.2f}, Canary={canary_metric:.2f}, 差异={metric_diff_pct:.2f}%")

        if metric_diff_pct > 1:
            print(f"  → {metric_col} 差异超过1%，需要人工审查")

    return True

if __name__ == "__main__":
    spark = SparkSession.builder.appName("canary-compare").getOrCreate()
    prod_table = sys.argv[1]
    canary_table = sys.argv[2]
    key_column = sys.argv[3]
    metric_columns = sys.argv[4].split(",")
    result = compare_tables(spark, prod_table, canary_table, key_column, metric_columns)
    spark.stop()
    sys.exit(0 if result else 1)
```

---

## 十、课堂练习（45min）

### 练习1：为ETL编写pytest测试（15min）

```python
tests/unit/test_transform.py:

import pytest
from pyspark.sql import Row, SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType
from pyspark.sql.functions import col, when

def classify_user_tier(df):
    return df.withColumn(
        "user_tier",
        when(col("order_count") >= 20, "VIP客户")
        .when(col("order_count") >= 6, "活跃客户")
        .when(col("order_count") >= 2, "普通客户")
        .when(col("order_count") == 1, "新客")
        .otherwise("无订单")
    )

def test_classify_user_tier(spark):
    data = [
        Row(user_id=1, order_count=0),
        Row(user_id=2, order_count=1),
        Row(user_id=3, order_count=3),
        Row(user_id=4, order_count=10),
        Row(user_id=5, order_count=25),
    ]
    schema = StructType([
        StructField("user_id", LongType(), False),
        StructField("order_count", LongType(), False),
    ])
    df = spark.createDataFrame(data, schema)
    result = classify_user_tier(df)
    rows = {row["user_id"]: row["user_tier"] for row in result.collect()}
    assert rows[1] == "无订单"
    assert rows[2] == "新客"
    assert rows[3] == "普通客户"
    assert rows[4] == "活跃客户"
    assert rows[5] == "VIP客户"

def test_classify_user_tier_null_order_count(spark):
    data = [Row(user_id=1, order_count=None)]
    schema = StructType([
        StructField("user_id", LongType(), False),
        StructField("order_count", LongType(), True),
    ])
    df = spark.createDataFrame(data, schema)
    result = classify_user_tier(df)
    row = result.first()
    assert row["user_tier"] == "无订单"
```

```bash
pytest tests/unit/test_transform.py -v
```

### 练习2：配置GitHub Actions运行dbt test（15min）

创建 `.github/workflows/dbt_ci.yml`:

```yaml
name: dbt CI

on:
  pull_request:
    branches: [main]
    paths:
      - 'models/**'
      - 'tests/**'
      - 'dbt_project.yml'

jobs:
  dbt-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dbt
        run: pip install dbt-core dbt-duckdb

      - name: dbt deps
        run: dbt deps

      - name: dbt seed
        run: dbt seed

      - name: dbt run
        run: dbt run

      - name: dbt test
        run: dbt test
```

### 练习3：实现数据质量门禁（15min）

```python
scripts/simple_quality_gate.py:

import subprocess
import sys

def run_dbt_test(select=None):
    cmd = ["dbt", "test"]
    if select:
        cmd.extend(["--select", select])
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def quality_gate():
    print("=== 数据质量门禁 ===")

    print("\n[1/3] Staging层测试...")
    staging_pass = run_dbt_test("staging.*")
    print(f"  结果: {'PASS' if staging_pass else 'FAIL'}")

    print("\n[2/3] Marts层测试...")
    marts_pass = run_dbt_test("marts.*")
    print(f"  结果: {'PASS' if marts_pass else 'FAIL'}")

    print("\n[3/3] 自定义测试...")
    custom_pass = run_dbt_test("test_type:singular")
    print(f"  结果: {'PASS' if custom_pass else 'FAIL'}")

    all_pass = staging_pass and marts_pass and custom_pass
    print(f"\n=== 门禁结果: {'PASS - 允许发布' if all_pass else 'FAIL - 阻止发布'} ===")
    sys.exit(0 if all_pass else 1)

if __name__ == "__main__":
    quality_gate()
```

```bash
python scripts/simple_quality_gate.py
```

---

## 十一、课后作业

### 必做

1. **为L2项目7的实时管道编写测试套件**：包含:
   - 3个PySpark单元测试（测试Flink SQL转换逻辑的PySpark等价实现）
   - 2个集成测试（测试Kafka→Flink→ClickHouse的数据一致性）
   - 1个端到端测试（验证实时大屏数据与离线数仓数据一致）
   - 所有测试通过CI运行

2. **配置完整的CI/CD流水线**：使用GitHub Actions，包含:
   - PR阶段：dbt compile + dbt test + pytest单元测试
   - 合并到main：dbt run + dbt test + 质量门禁 + dbt docs generate
   - 部署到生产：dbt run --target prod + dbt test --target prod + 通知

3. **实现数据质量门禁阻止低质量数据发布**：包含:
   - 至少3层门禁规则（staging/intermediate/marts）
   - 不同层级不同阈值和动作（warn/error/block）
   - 门禁失败时发送告警通知
   - 验证：故意引入数据问题，确认门禁能正确阻止发布

4. **写一篇"数据工程CI/CD最佳实践"技术Blog**（1500字以上），包含:
   - 数据测试金字塔的实践经验
   - CI/CD流水线设计思路
   - 质量门禁的阈值设定策略
   - 蓝绿部署和Canary发布的适用场景
   - 常见踩坑和解决方案

### 选做

1. 搭建LakeFS环境，实践数据分支和合并操作
2. 使用DVC管理训练数据和模型版本
3. 实现Canary发布流程，包含自动对比和自动回滚

---

## 十二、参考资料

- [dbt测试文档](https://docs.getdbt.com/docs/build/data-tests)
- [Great Expectations官方文档](https://docs.greatexpectations.io/docs/)
- [DVC官方文档](https://dvc.org/doc)
- [LakeFS官方文档](https://docs.lakefs.io/)
- [GitHub Actions文档](https://docs.github.com/en/actions)
- [PySpark测试最佳实践](https://spark.apache.org/docs/latest/api/python/getting_started/testing_pyspark.html)
- [chispa: PySpark测试辅助库](https://github.com/MrPowers/chispa)
- [Astronomer Cosmos: Airflow编排dbt](https://astronomer.github.io/astronomer-cosmos/)
- [数据工程CI/CD模式](https://docs.getdbt.com/docs/deploy/ci-jobs)
- [蓝绿部署数据管道](https://docs.getdbt.com/best-practices/blue-green-deployments)
