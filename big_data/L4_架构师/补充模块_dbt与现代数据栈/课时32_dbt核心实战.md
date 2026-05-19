# 课时32：dbt核心实战

> **所属阶段**：L4 架构师 | **模块**：补充模块_dbt与现代数据栈 | **课时**：3h | **难度**：★★★★☆

---

## 一、教学目标

1. 理解现代数据栈架构，掌握ELT与ETL的本质区别以及dbt在数据栈中的定位
2. 掌握dbt核心概念：Model、Source、Ref、Macro、Test、Documentation、Snapshot
3. 掌握dbt项目分层架构：Staging → Intermediate → Marts，理解每层的职责边界
4. 掌握增量模型策略：merge、insert_overwrite、delete+insert，能根据场景选型
5. 掌握dbt测试体系：Schema Test与Custom Test，实现数据质量门禁
6. 掌握dbt文档自动生成，理解数据字典与血缘图的价值
7. 了解dbt与Airflow集成方案：dbt Cloud与Airflow dbt operator

---

## 二、现代数据栈架构

### 2.1 ELT vs ETL

```
传统ETL架构:

  ┌──────────┐     ┌──────────────────────┐     ┌──────────┐
  │  数据源   │────→│  ETL引擎(Informatica │────→│  数据仓库 │
  │  MySQL    │     │  /DataStage/Kettle)  │     │  Oracle  │
  │  日志文件  │     │  Extract → Transform │     │  Teradata│
  │  API      │     │  → Load              │     │          │
  └──────────┘     └──────────────────────┘     └──────────┘

  特点: 先转换再加载，转换逻辑在ETL引擎中执行
  问题: 转换逻辑与调度耦合、难以版本控制、难以测试


现代ELT架构:

  ┌──────────┐     ┌──────────────────────┐     ┌──────────────────────┐
  │  数据源   │────→│  Extract+Load        │────→│  Transform(dbt)      │
  │  MySQL    │     │  (Fivetran/Airbyte   │     │  SQL-first           │
  │  日志文件  │     │   /Kafka CDC)        │     │  版本控制 + 测试      │
  │  API      │     │  原样加载到数据仓库    │     │  文档 + 血缘          │
  └──────────┘     └──────────────────────┘     └──────────────────────┘
         │                                              │
         │              ┌──────────────────────┐        │
         └──────────────→  云数据仓库            ←──────┘
                        │  Snowflake/BigQuery  │
                        │  Redshift/DuckDB     │
                        │  PostgreSQL          │
                        └──────────────────────┘

  特点: 先加载再转换，转换逻辑由dbt在数据仓库内执行
  优势: 利用数仓算力、SQL-first易上手、Git版本控制、可测试可文档
```

### 2.2 dbt在现代数据栈中的定位

```
现代数据栈全景:

  ┌─────────────────────────────────────────────────────────────────────┐
  │                        数据消费层                                    │
  │   BI工具(Looker/Metabase)  分析笔记本  数据应用  ML特征存储          │
  └────────────────────────────────┬────────────────────────────────────┘
                                   │ 查询Marts层模型
  ┌────────────────────────────────▼────────────────────────────────────┐
  │                     dbt转换层（核心）                                 │
  │                                                                     │
  │   ┌──────────┐   ┌──────────────┐   ┌──────────┐                  │
  │   │ Staging  │──→│ Intermediate │──→│  Marts   │                  │
  │   │ 清洗标准化│   │  业务逻辑转换 │   │ 主题域建模│                  │
  │   └──────────┘   └──────────────┘   └──────────┘                  │
  │        ↑                                     │                     │
  │   Source定义                             Test/Docs                 │
  │   血缘起点                              质量保障+文档              │
  └────────────────────────────────┬────────────────────────────────────┘
                                   │
  ┌────────────────────────────────▼────────────────────────────────────┐
  │                       数据存储层                                     │
  │   Snowflake / BigQuery / Redshift / DuckDB / PostgreSQL            │
  └────────────────────────────────┬────────────────────────────────────┘
                                   │
  ┌────────────────────────────────▼────────────────────────────────────┐
  │                       数据摄入层                                     │
  │   Fivetran / Airbyte / Kafka CDC / Debezium / dlt                  │
  └─────────────────────────────────────────────────────────────────────┘
```

---

## 三、dbt核心概念

### 3.1 七大核心概念

```
dbt七大核心概念:

  ┌──────────────────────────────────────────────────────────────────┐
  │                                                                  │
  │  1. Source  → 原始数据源定义，标记血缘起点                        │
  │     sources:                                                     │
  │       - name: raw_ecommerce                                     │
  │         tables:                                                  │
  │           - name: orders                                        │
  │           - name: users                                         │
  │                                                                  │
  │  2. Model   → 一个SELECT语句 = 一个表/视图，dbt的核心单元         │
  │     models/staging/stg_orders.sql                                │
  │     → 编译后: CREATE OR REPLACE VIEW stg_orders AS SELECT ...    │
  │                                                                  │
  │  3. Ref     → 模型间引用，替代硬编码表名，自动解析依赖            │
  │     SELECT * FROM {{ ref('stg_orders') }}                       │
  │     → 编译后: SELECT * FROM "analytics"."staging"."stg_orders"  │
  │                                                                  │
  │  4. Macro   → 可复用的SQL片段（类似函数），支持参数和条件逻辑     │
  │     {{ get_payment_status('order_status') }}                    │
  │                                                                  │
  │  5. Test    → 数据质量断言，Schema Test + Custom Test             │
  │     unique / not_null / accepted_values / relationships          │
  │                                                                  │
  │  6. Docs    → 自动生成数据字典和血缘DAG图                         │
  │     dbt docs generate → dbt docs serve                          │
  │                                                                  │
  │  7. Snapshot → 捕获维度表的历史变化，实现SCD Type 2               │
  │     记录维度属性何时变更，保留完整历史                             │
  │                                                                  │
  └──────────────────────────────────────────────────────────────────┘
```

### 3.2 dbt项目结构

```
dbt项目目录结构:

  ecommerce_warehouse/
  ├── dbt_project.yml          ← 项目级配置（数据库名/Schema前缀/全局变量）
  ├── profiles.yml             ← 连接配置（不在Git中，~/.dbt/profiles.yml）
  ├── packages.yml             ← dbt包依赖
  ├── models/
  │   ├── staging/             ← Staging层：清洗原始数据
  │   │   ├── _staging__models.yml    ← Staging层Schema+Test定义
  │   │   ├── _sources.yml           ← Source定义
  │   │   ├── stg_orders.sql
  │   │   ├── stg_order_details.sql
  │   │   ├── stg_users.sql
  │   │   └── stg_products.sql
  │   ├── intermediate/        ← Intermediate层：业务逻辑转换
  │   │   ├── _intermediate__models.yml
  │   │   ├── int_orders_enriched.sql
  │   │   ├── int_user_order_summary.sql
  │   │   └── int_product_metrics.sql
  │   └── marts/               ← Marts层：面向业务的主题域
  │       ├── _marts__models.yml
  │       ├── finance/
  │       │   ├── _finance__models.yml
  │       │   ├── fct_orders.sql
  │       │   └── fct_payments.sql
  │       ├── marketing/
  │       │   ├── _marketing__models.yml
  │       │   ├── dim_users.sql
  │       │   └── mart_user_retention.sql
  │       └── product/
  │           ├── _product__models.yml
  │           ├── dim_products.sql
  │           └── mart_product_sales.sql
  ├── macros/
  │   ├── get_payment_status.sql
  │   ├── generate_surrogate_key.sql
  │   └── date_spine.sql
  ├── tests/
  │   ├── assert_order_amount_positive.sql
  │   └── assert_user_retention_range.sql
  ├── snapshots/
  │   └── snap_users.sql
  ├── seeds/
  │   ├── csv/
  │   │   ├── country_codes.csv
  │   │   └── payment_methods.csv
  │   └── _seeds__schema.yml
  └── analyses/
      └── adhoc_analysis.sql
```

---

## 四、dbt项目初始化与配置

### 4.1 安装与初始化

```bash
pip install dbt-core dbt-duckdb

dbt init ecommerce_warehouse

cd ecommerce_warehouse
```

### 4.2 profiles.yml连接配置

```yaml
ecommerce_warehouse:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: "./data/ecommerce.duckdb"
      threads: 4
    prod:
      type: postgres
      host: "{{ env_var('DBT_POSTGRES_HOST') }}"
      port: 5432
      user: "{{ env_var('DBT_POSTGRES_USER') }}"
      password: "{{ env_var('DBT_POSTGRES_PASSWORD') }}"
      dbname: analytics
      schema: public
      threads: 8
```

### 4.3 dbt_project.yml项目配置

```yaml
name: ecommerce_warehouse
version: '1.0.0'
config-version: 2

profile: ecommerce_warehouse

model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

target-path: "target"
clean-targets:
  - "target"
  - "dbt_packages"

models:
  ecommerce_warehouse:
    staging:
      +materialized: view
      +schema: staging
    intermediate:
      +materialized: view
      +schema: intermediate
    marts:
      +materialized: table
      +schema: marts
      finance:
        +materialized: table
      marketing:
        +materialized: table
      product:
        +materialized: table

vars:
  start_date: '2024-01-01'
  max_date: '2024-12-31'
```

### 4.4 packages.yml依赖管理

```yaml
packages:
  - package: dbt-labs/dbt_utils
    version: "1.1.1"
  - package: calogica/dbt_expectations
    version: "0.10.1"
  - package: dbt-labs/codegen
    version: "0.12.1"
```

```bash
dbt deps
```

---

## 五、Staging层模型：清洗原始数据

### 5.1 Source定义

```yaml
models:
  staging:
    +materialized: view
```

```yaml
models/staging/_sources.yml:

version: 2

sources:
  - name: raw_ecommerce
    description: "电商原始数据，由Airbyte从MySQL同步"
    schema: raw
    tables:
      - name: orders
        description: "订单主表"
        columns:
          - name: order_id
            description: "订单ID"
            tests:
              - unique
              - not_null
          - name: user_id
            description: "用户ID"
            tests:
              - not_null
          - name: status
            description: "订单状态"
          - name: total_amount
            description: "订单总金额"
          - name: created_at
            description: "创建时间"
        loaded_at_field: created_at
        freshness:
          warn_after: {count: 12, period: hour}
          error_after: {count: 24, period: hour}

      - name: order_details
        description: "订单明细表"
        columns:
          - name: detail_id
            tests:
              - unique
              - not_null
          - name: order_id
          - name: product_id
          - name: quantity
          - name: unit_price

      - name: users
        description: "用户表"
        columns:
          - name: user_id
            tests:
              - unique
              - not_null
          - name: username
          - name: email
          - name: gender
          - name: province
          - name: city

      - name: products
        description: "商品表"
        columns:
          - name: product_id
            tests:
              - unique
              - not_null
          - name: product_name
          - name: category
          - name: brand
          - name: price
```

### 5.2 Staging层模型

```sql
models/staging/stg_orders.sql:

WITH source AS (
    SELECT * FROM {{ source('raw_ecommerce', 'orders') }}
),

renamed AS (
    SELECT
        order_id,
        user_id,
        UPPER(TRIM(status)) AS order_status,
        total_amount,
        payment_amount,
        shipping_province,
        shipping_city,
        created_at,
        pay_time,
        finish_time,
        DATE(created_at) AS order_date
    FROM source
    WHERE order_id IS NOT NULL
      AND user_id IS NOT NULL
      AND total_amount >= 0
),

categorized AS (
    SELECT
        *,
        CASE
            WHEN order_status = 'CREATED' THEN '待支付'
            WHEN order_status = 'PAID' THEN '已支付'
            WHEN order_status = 'COMPLETED' THEN '已完成'
            WHEN order_status = 'CANCELLED' THEN '已取消'
            WHEN order_status = 'REFUNDED' THEN '已退款'
            ELSE '未知'
        END AS order_status_cn,
        CASE
            WHEN total_amount >= 5000 THEN '大额订单'
            WHEN total_amount >= 1000 THEN '中额订单'
            ELSE '小额订单'
        END AS order_amount_tier
    FROM renamed
)

SELECT * FROM categorized
```

```sql
models/staging/stg_order_details.sql:

WITH source AS (
    SELECT * FROM {{ source('raw_ecommerce', 'order_details') }}
),

renamed AS (
    SELECT
        detail_id,
        order_id,
        product_id,
        quantity AS sku_num,
        unit_price AS order_price,
        quantity * unit_price AS subtotal,
        created_at
    FROM source
    WHERE detail_id IS NOT NULL
      AND order_id IS NOT NULL
      AND quantity > 0
      AND unit_price >= 0
)

SELECT * FROM renamed
```

```sql
models/staging/stg_users.sql:

WITH source AS (
    SELECT * FROM {{ source('raw_ecommerce', 'users') }}
),

renamed AS (
    SELECT
        user_id,
        TRIM(username) AS user_name,
        LOWER(TRIM(email)) AS email,
        CASE
            WHEN gender IN ('M', '男') THEN '男'
            WHEN gender IN ('F', '女') THEN '女'
            ELSE '未知'
        END AS user_gender,
        TRIM(province) AS user_province,
        TRIM(city) AS user_city,
        created_at AS register_time,
        DATE(created_at) AS register_date
    FROM source
    WHERE user_id IS NOT NULL
)

SELECT * FROM renamed
```

```sql
models/staging/stg_products.sql:

WITH source AS (
    SELECT * FROM {{ source('raw_ecommerce', 'products') }}
),

renamed AS (
    SELECT
        product_id,
        TRIM(product_name) AS product_name,
        TRIM(category) AS category_name,
        TRIM(brand) AS brand,
        price,
        stock,
        CASE
            WHEN stock = 0 THEN '缺货'
            WHEN stock < 10 THEN '低库存'
            ELSE '正常'
        END AS stock_status
    FROM source
    WHERE product_id IS NOT NULL
      AND price >= 0
)

SELECT * FROM renamed
```

### 5.3 Staging层Schema与Test定义

```yaml
models/staging/_staging__models.yml:

version: 2

models:
  - name: stg_orders
    description: "订单主表清洗后模型，标准化状态值和金额"
    columns:
      - name: order_id
        description: "订单ID，主键"
        tests:
          - unique
          - not_null
      - name: user_id
        description: "用户ID"
        tests:
          - not_null
      - name: order_status
        description: "订单状态（英文原文）"
        tests:
          - accepted_values:
              values: ['CREATED', 'PAID', 'COMPLETED', 'CANCELLED', 'REFUNDED']
      - name: order_status_cn
        description: "订单状态（中文）"
        tests:
          - accepted_values:
              values: ['待支付', '已支付', '已完成', '已取消', '已退款', '未知']
      - name: total_amount
        description: "订单总金额"
        tests:
          - not_null
          - dbt_expectations.expect_column_values_to_be_between:
              min_value: 0
              max_value: 1000000
      - name: order_date
        description: "下单日期"
        tests:
          - not_null

  - name: stg_order_details
    description: "订单明细清洗后模型"
    columns:
      - name: detail_id
        description: "明细ID，主键"
        tests:
          - unique
          - not_null
      - name: order_id
        description: "订单ID"
        tests:
          - not_null
          - relationships:
              to: ref('stg_orders')
              field: order_id
      - name: product_id
        description: "商品ID"
        tests:
          - not_null
          - relationships:
              to: ref('stg_products')
              field: product_id
      - name: sku_num
        description: "购买数量"
        tests:
          - not_null
          - dbt_expectations.expect_column_values_to_be_between:
              min_value: 1
              max_value: 999
      - name: order_price
        description: "单价"
        tests:
          - not_null
          - dbt_expectations.expect_column_values_to_be_between:
              min_value: 0
              max_value: 100000

  - name: stg_users
    description: "用户清洗后模型，标准化性别值"
    columns:
      - name: user_id
        description: "用户ID，主键"
        tests:
          - unique
          - not_null
      - name: user_gender
        description: "性别"
        tests:
          - accepted_values:
              values: ['男', '女', '未知']
      - name: email
        description: "邮箱"
        tests:
          - not_null:
              config:
                severity: warn

  - name: stg_products
    description: "商品清洗后模型"
    columns:
      - name: product_id
        description: "商品ID，主键"
        tests:
          - unique
          - not_null
      - name: price
        description: "价格"
        tests:
          - not_null
          - dbt_expectations.expect_column_values_to_be_between:
              min_value: 0
              max_value: 100000
      - name: stock_status
        description: "库存状态"
        tests:
          - accepted_values:
              values: ['缺货', '低库存', '正常']
```

---

## 六、Intermediate层模型：业务逻辑转换

### 6.1 订单宽表

```sql
models/intermediate/int_orders_enriched.sql:

WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

details AS (
    SELECT * FROM {{ ref('stg_order_details') }}
),

users AS (
    SELECT * FROM {{ ref('stg_users') }}
),

products AS (
    SELECT * FROM {{ ref('stg_products') }}
),

order_detail_agg AS (
    SELECT
        order_id,
        COUNT(DISTINCT product_id) AS product_count,
        SUM(sku_num) AS total_sku_num,
        SUM(subtotal) AS calculated_total
    FROM details
    GROUP BY order_id
),

enriched AS (
    SELECT
        o.order_id,
        o.user_id,
        u.user_name,
        u.user_gender,
        u.user_province,
        u.user_city,
        o.order_status,
        o.order_status_cn,
        o.total_amount,
        o.payment_amount,
        o.shipping_province,
        o.shipping_city,
        o.order_date,
        o.order_amount_tier,
        COALESCE(od.product_count, 0) AS product_count,
        COALESCE(od.total_sku_num, 0) AS total_sku_num,
        COALESCE(od.calculated_total, 0) AS calculated_total,
        CASE
            WHEN o.payment_amount IS NOT NULL THEN o.payment_amount
            ELSE 0
        END AS actual_payment,
        CASE
            WHEN o.payment_amount IS NOT NULL
                AND ABS(o.total_amount - COALESCE(od.calculated_total, o.total_amount)) > 0.01
            THEN True
            ELSE False
        END AS amount_mismatch_flag
    FROM orders o
    LEFT JOIN order_detail_agg od ON o.order_id = od.order_id
    LEFT JOIN users u ON o.user_id = u.user_id
)

SELECT * FROM enriched
```

### 6.2 用户订单汇总

```sql
models/intermediate/int_user_order_summary.sql:

WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

user_summary AS (
    SELECT
        user_id,
        COUNT(*) AS total_order_count,
        COUNT(CASE WHEN order_status = 'COMPLETED' THEN 1 END) AS completed_order_count,
        COUNT(CASE WHEN order_status = 'CANCELLED' THEN 1 END) AS cancelled_order_count,
        SUM(total_amount) AS total_order_amount,
        SUM(CASE WHEN payment_amount IS NOT NULL THEN payment_amount ELSE 0 END) AS total_payment_amount,
        MIN(order_date) AS first_order_date,
        MAX(order_date) AS last_order_date,
        DATE_DIFF(MAX(order_date), MIN(order_date), DAY) AS order_day_span,
        COUNT(DISTINCT order_date) AS active_days,
        CASE
            WHEN COUNT(*) = 0 THEN '无订单'
            WHEN COUNT(*) = 1 THEN '新客'
            WHEN COUNT(*) BETWEEN 2 AND 5 THEN '普通客户'
            WHEN COUNT(*) BETWEEN 6 AND 20 THEN '活跃客户'
            ELSE 'VIP客户'
        END AS user_tier,
        CASE
            WHEN SUM(CASE WHEN payment_amount IS NOT NULL THEN payment_amount ELSE 0 END) >= 10000 THEN '高价值'
            WHEN SUM(CASE WHEN payment_amount IS NOT NULL THEN payment_amount ELSE 0 END) >= 3000 THEN '中价值'
            ELSE '低价值'
        END AS value_tier
    FROM orders
    GROUP BY user_id
)

SELECT * FROM user_summary
```

### 6.3 商品指标

```sql
models/intermediate/int_product_metrics.sql:

WITH details AS (
    SELECT * FROM {{ ref('stg_order_details') }}
),

orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

product_metrics AS (
    SELECT
        d.product_id,
        COUNT(DISTINCT d.order_id) AS order_count,
        SUM(d.sku_num) AS total_sold,
        SUM(d.subtotal) AS total_revenue,
        AVG(d.order_price) AS avg_selling_price,
        COUNT(DISTINCT o.user_id) AS buyer_count
    FROM details d
    INNER JOIN orders o ON d.order_id = o.order_id
    WHERE o.order_status IN ('PAID', 'COMPLETED')
    GROUP BY d.product_id
)

SELECT * FROM product_metrics
```

---

## 七、Marts层模型：面向业务的主题域

### 7.1 事实表：订单事实

```sql
models/marts/finance/fct_orders.sql:

{{ config(
    materialized='table',
    partition_by={'field': 'order_date', 'data_type': 'date'},
    cluster_by=['user_id', 'order_status']
) }}

WITH enriched AS (
    SELECT * FROM {{ ref('int_orders_enriched') }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['order_id']) }} AS order_key,
    order_id,
    user_id,
    user_name,
    user_gender,
    user_province,
    user_city,
    order_status,
    order_status_cn,
    total_amount,
    payment_amount,
    actual_payment,
    shipping_province,
    shipping_city,
    product_count,
    total_sku_num,
    calculated_total,
    amount_mismatch_flag,
    order_date,
    order_amount_tier
FROM enriched
WHERE order_id IS NOT NULL
```

### 7.2 维度表：用户维度

```sql
models/marts/marketing/dim_users.sql:

{{ config(
    materialized='table',
    cluster_by=['user_tier', 'value_tier']
) }}

WITH users AS (
    SELECT * FROM {{ ref('stg_users') }}
),

order_summary AS (
    SELECT * FROM {{ ref('int_user_order_summary') }}
),

dim AS (
    SELECT
        {{ dbt_utils.generate_surrogate_key(['u.user_id']) }} AS user_key,
        u.user_id,
        u.user_name,
        u.email,
        u.user_gender,
        u.user_province,
        u.user_city,
        u.register_date,
        COALESCE(os.total_order_count, 0) AS total_order_count,
        COALESCE(os.completed_order_count, 0) AS completed_order_count,
        COALESCE(os.cancelled_order_count, 0) AS cancelled_order_count,
        COALESCE(os.total_order_amount, 0) AS total_order_amount,
        COALESCE(os.total_payment_amount, 0) AS total_payment_amount,
        os.first_order_date,
        os.last_order_date,
        os.order_day_span,
        os.active_days,
        COALESCE(os.user_tier, '无订单') AS user_tier,
        COALESCE(os.value_tier, '低价值') AS value_tier
    FROM users u
    LEFT JOIN order_summary os ON u.user_id = os.user_id
)

SELECT * FROM dim
```

### 7.3 维度表：商品维度

```sql
models/marts/product/dim_products.sql:

{{ config(
    materialized='table',
    cluster_by=['category_name']
) }}

WITH products AS (
    SELECT * FROM {{ ref('stg_products') }}
),

metrics AS (
    SELECT * FROM {{ ref('int_product_metrics') }}
),

dim AS (
    SELECT
        {{ dbt_utils.generate_surrogate_key(['p.product_id']) }} AS product_key,
        p.product_id,
        p.product_name,
        p.category_name,
        p.brand,
        p.price,
        p.stock,
        p.stock_status,
        COALESCE(m.order_count, 0) AS order_count,
        COALESCE(m.total_sold, 0) AS total_sold,
        COALESCE(m.total_revenue, 0) AS total_revenue,
        COALESCE(m.avg_selling_price, p.price) AS avg_selling_price,
        COALESCE(m.buyer_count, 0) AS buyer_count,
        CASE
            WHEN COALESCE(m.total_revenue, 0) >= 100000 THEN '头部商品'
            WHEN COALESCE(m.total_revenue, 0) >= 10000 THEN '腰部商品'
            ELSE '尾部商品'
        END AS revenue_tier
    FROM products p
    LEFT JOIN metrics m ON p.product_id = m.product_id
)

SELECT * FROM dim
```

### 7.4 业务主题域：用户留存

```sql
models/marts/marketing/mart_user_retention.sql:

{{ config(
    materialized='table',
    partition_by={'field': 'cohort_date', 'data_type': 'date'}
) }}

WITH user_first_order AS (
    SELECT
        user_id,
        MIN(order_date) AS cohort_date
    FROM {{ ref('stg_orders') }}
    WHERE order_status IN ('PAID', 'COMPLETED')
    GROUP BY user_id
),

user_activity AS (
    SELECT DISTINCT
        user_id,
        order_date
    FROM {{ ref('stg_orders') }}
    WHERE order_status IN ('PAID', 'COMPLETED')
),

retention AS (
    SELECT
        fo.user_id,
        fo.cohort_date,
        ua.order_date,
        DATE_DIFF(ua.order_date, fo.cohort_date, DAY) AS day_diff
    FROM user_first_order fo
    INNER JOIN user_activity ua ON fo.user_id = ua.user_id
),

cohort_agg AS (
    SELECT
        cohort_date,
        COUNT(DISTINCT user_id) AS cohort_size,
        COUNT(DISTINCT CASE WHEN day_diff = 0 THEN user_id END) AS d0,
        COUNT(DISTINCT CASE WHEN day_diff = 1 THEN user_id END) AS d1,
        COUNT(DISTINCT CASE WHEN day_diff = 3 THEN user_id END) AS d3,
        COUNT(DISTINCT CASE WHEN day_diff = 7 THEN user_id END) AS d7,
        COUNT(DISTINCT CASE WHEN day_diff = 14 THEN user_id END) AS d14,
        COUNT(DISTINCT CASE WHEN day_diff = 30 THEN user_id END) AS d30
    FROM retention
    GROUP BY cohort_date
)

SELECT
    cohort_date,
    cohort_size,
    d0,
    d1,
    d3,
    d7,
    d14,
    d30,
    ROUND(d1 * 100.0 / NULLIF(d0, 0), 2) AS d1_rate,
    ROUND(d7 * 100.0 / NULLIF(d0, 0), 2) AS d7_rate,
    ROUND(d30 * 100.0 / NULLIF(d0, 0), 2) AS d30_rate
FROM cohort_agg
ORDER BY cohort_date
```

### 7.5 业务主题域：商品销售

```sql
models/marts/product/mart_product_sales.sql:

{{ config(
    materialized='table',
    partition_by={'field': 'order_date', 'data_type': 'date'}
) }}

WITH details AS (
    SELECT * FROM {{ ref('stg_order_details') }}
),

orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

products AS (
    SELECT * FROM {{ ref('stg_products') }}
),

sales AS (
    SELECT
        d.product_id,
        p.product_name,
        p.category_name,
        p.brand,
        o.order_date,
        COUNT(DISTINCT d.order_id) AS daily_order_count,
        SUM(d.sku_num) AS daily_sold,
        SUM(d.subtotal) AS daily_revenue,
        AVG(d.order_price) AS daily_avg_price
    FROM details d
    INNER JOIN orders o ON d.order_id = o.order_id
    INNER JOIN products p ON d.product_id = p.product_id
    WHERE o.order_status IN ('PAID', 'COMPLETED')
    GROUP BY d.product_id, p.product_name, p.category_name, p.brand, o.order_date
)

SELECT * FROM sales
```

---

## 八、增量模型

### 8.1 增量模型策略对比

```
增量模型三种策略:

  ┌──────────────────────────────────────────────────────────────────────┐
  │  1. merge (默认策略)                                                  │
  │     原理: MERGE INTO target USING source ON key                      │
  │           MATCHED → UPDATE, NOT MATCHED → INSERT                    │
  │     适合: 维度表更新、订单状态变更                                     │
  │     优点: 精确更新，不重复                                            │
  │     缺点: MERGE语句较重，大数据量时性能一般                           │
  │                                                                      │
  │  2. insert_overwrite                                                  │
  │     原理: INSERT OVERWRITE 分区                                       │
  │           先删除匹配分区，再插入新数据                                 │
  │     适合: 按分区全量刷新（如每日分区汇总）                             │
  │     优点: 简单高效，适合分区表                                        │
  │     缺点: 必须有分区字段，会覆盖整个分区                              │
  │                                                                      │
  │  3. delete+insert                                                     │
  │     原理: 先DELETE匹配的行，再INSERT新数据                            │
  │     适合: 不支持MERGE的数据库（如旧版MySQL）                          │
  │     优点: 兼容性好                                                    │
  │     缺点: 非原子操作，中间状态可能不一致                              │
  └──────────────────────────────────────────────────────────────────────┘
```

### 8.2 增量模型实战：merge策略

```sql
models/marts/finance/fct_orders_incremental.sql:

{{ config(
    materialized='incremental',
    unique_key='order_id',
    incremental_strategy='merge',
    partition_by={'field': 'order_date', 'data_type': 'date'}
) }}

WITH source AS (
    SELECT * FROM {{ ref('int_orders_enriched') }}
),

filtered AS (
    SELECT * FROM source
    {% if is_incremental() %}
    WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 3 DAY)
    {% endif %}
)

SELECT
    order_id,
    user_id,
    user_name,
    user_gender,
    user_province,
    user_city,
    order_status,
    order_status_cn,
    total_amount,
    payment_amount,
    actual_payment,
    shipping_province,
    shipping_city,
    product_count,
    total_sku_num,
    calculated_total,
    amount_mismatch_flag,
    order_date,
    order_amount_tier
FROM filtered
```

### 8.3 增量模型实战：insert_overwrite策略

```sql
models/marts/product/mart_product_sales_incremental.sql:

{{ config(
    materialized='incremental',
    incremental_strategy='insert_overwrite',
    partition_by={'field': 'order_date', 'data_type': 'date'},
    partitions=var('lookback_partitions', [1])
) }}

WITH details AS (
    SELECT * FROM {{ ref('stg_order_details') }}
),

orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

products AS (
    SELECT * FROM {{ ref('stg_products') }}
),

filtered_orders AS (
    SELECT * FROM orders
    {% if is_incremental() %}
    WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
    {% endif %}
),

sales AS (
    SELECT
        d.product_id,
        p.product_name,
        p.category_name,
        p.brand,
        o.order_date,
        COUNT(DISTINCT d.order_id) AS daily_order_count,
        SUM(d.sku_num) AS daily_sold,
        SUM(d.subtotal) AS daily_revenue,
        AVG(d.order_price) AS daily_avg_price
    FROM details d
    INNER JOIN filtered_orders o ON d.order_id = o.order_id
    INNER JOIN products p ON d.product_id = p.product_id
    WHERE o.order_status IN ('PAID', 'COMPLETED')
    GROUP BY d.product_id, p.product_name, p.category_name, p.brand, o.order_date
)

SELECT * FROM sales
```

### 8.4 增量模型实战：delete+insert策略

```sql
models/marts/finance/fct_payments_incremental.sql:

{{ config(
    materialized='incremental',
    unique_key='payment_id',
    incremental_strategy='delete+insert',
    partition_by={'field': 'payment_date', 'data_type': 'date'}
) }}

WITH payments AS (
    SELECT
        order_id AS payment_id,
        user_id,
        payment_amount,
        order_status,
        order_date AS payment_date
    FROM {{ ref('stg_orders') }}
    WHERE payment_amount IS NOT NULL
      AND payment_amount > 0
    {% if is_incremental() %}
      AND order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
    {% endif %}
)

SELECT * FROM payments
```

---

## 九、dbt测试

### 9.1 Schema Test

```yaml
models/marts/finance/_finance__models.yml:

version: 2

models:
  - name: fct_orders
    description: "订单事实表，包含订单全量信息"
    tests:
      - dbt_utils.expression_is_true:
          expression: "total_amount >= 0"
          name: total_amount_non_negative
      - dbt_utils.expression_is_true:
          expression: "payment_amount <= total_amount"
          name: payment_not_exceed_total
    columns:
      - name: order_key
        description: "订单代理键"
        tests:
          - unique
          - not_null
      - name: order_id
        description: "订单业务ID"
        tests:
          - unique
          - not_null
      - name: user_id
        description: "用户ID"
        tests:
          - not_null
      - name: order_status_cn
        description: "订单状态中文"
        tests:
          - not_null
          - accepted_values:
              values: ['待支付', '已支付', '已完成', '已取消', '已退款', '未知']
      - name: total_amount
        description: "订单总金额"
        tests:
          - not_null
          - dbt_expectations.expect_column_values_to_be_between:
              min_value: 0
              max_value: 1000000
      - name: order_date
        description: "下单日期"
        tests:
          - not_null

  - name: fct_orders_incremental
    description: "订单事实表（增量模型）"
    tests:
      - dbt_utils.expression_is_true:
          expression: "total_amount >= 0"
    columns:
      - name: order_id
        tests:
          - unique
          - not_null

  - name: fct_payments_incremental
    description: "支付事实表（增量模型）"
    columns:
      - name: payment_id
        tests:
          - unique
          - not_null
      - name: payment_amount
        tests:
          - not_null
          - dbt_expectations.expect_column_values_to_be_between:
              min_value: 0.01
              max_value: 1000000
```

### 9.2 自定义测试：业务规则验证

```sql
tests/assert_order_amount_positive.sql:

SELECT
    order_id,
    total_amount,
    calculated_total,
    ABS(total_amount - calculated_total) AS diff
FROM {{ ref('fct_orders') }}
WHERE total_amount < 0
   OR (calculated_total > 0 AND ABS(total_amount - calculated_total) > 1.0)
```

```sql
tests/assert_user_retention_range.sql:

SELECT
    cohort_date,
    d1_rate,
    d7_rate,
    d30_rate
FROM {{ ref('mart_user_retention') }}
WHERE d1_rate > 100
   OR d7_rate > 100
   OR d30_rate > 100
   OR d1_rate < 0
   OR d7_rate < 0
   OR d30_rate < 0
```

```sql
tests/assert_no_orphan_order_details.sql:

SELECT
    d.detail_id,
    d.order_id
FROM {{ ref('stg_order_details') }} d
LEFT JOIN {{ ref('stg_orders') }} o ON d.order_id = o.order_id
WHERE o.order_id IS NULL
```

```sql
tests/assert_payment_consistency.sql:

SELECT
    order_id,
    total_amount,
    payment_amount
FROM {{ ref('fct_orders') }}
WHERE order_status_cn = '已支付'
  AND payment_amount IS NULL
```

---

## 十、Macro：可复用的SQL片段

### 10.1 通用Macro

```sql
macros/generate_surrogate_key.sql:

{% macro generate_surrogate_key(field_list) %}
    {{ return(dbt_utils.generate_surrogate_key(field_list)) }}
{% endmacro %}
```

```sql
macros/get_payment_status.sql:

{% macro get_payment_status(status_column) %}
    CASE
        WHEN {{ status_column }} = 'CREATED' THEN '待支付'
        WHEN {{ status_column }} = 'PAID' THEN '已支付'
        WHEN {{ status_column }} = 'COMPLETED' THEN '已完成'
        WHEN {{ status_column }} = 'CANCELLED' THEN '已取消'
        WHEN {{ status_column }} = 'REFUNDED' THEN '已退款'
        ELSE '未知'
    END
{% endmacro %}
```

```sql
macros/date_spine.sql:

{% macro date_spine(start_date, end_date, datepart='day') %}
    WITH RECURSIVE dates AS (
        SELECT {{ start_date }} AS date_value
        UNION ALL
        SELECT DATE_ADD(date_value, INTERVAL 1 {{ datepart }})
        FROM dates
        WHERE date_value < {{ end_date }}
    )
    SELECT date_value FROM dates
{% endmacro %}
```

### 10.2 增量过滤Macro

```sql
macros/incremental_filter.sql:

{% macro incremental_filter(date_column, lookback_days=3) %}
    {% if is_incremental() %}
    WHERE {{ date_column }} >= DATE_SUB(CURRENT_DATE(), INTERVAL {{ lookback_days }} DAY)
    {% endif %}
{% endmacro %}
```

### 10.3 使用Macro的模型

```sql
models/marts/marketing/mart_user_retention_macro.sql:

{{ config(
    materialized='table',
    partition_by={'field': 'cohort_date', 'data_type': 'date'}
) }}

WITH user_first_order AS (
    SELECT
        user_id,
        MIN(order_date) AS cohort_date
    FROM {{ ref('stg_orders') }}
    WHERE order_status IN ('PAID', 'COMPLETED')
    GROUP BY user_id
),

date_spine AS (
    {{ date_spine("'2024-01-01'", "CURRENT_DATE()") }}
),

user_activity AS (
    SELECT DISTINCT
        user_id,
        order_date
    FROM {{ ref('stg_orders') }}
    WHERE order_status IN ('PAID', 'COMPLETED')
),

retention AS (
    SELECT
        fo.user_id,
        fo.cohort_date,
        ua.order_date,
        DATE_DIFF(ua.order_date, fo.cohort_date, DAY) AS day_diff
    FROM user_first_order fo
    INNER JOIN user_activity ua ON fo.user_id = ua.user_id
),

cohort_agg AS (
    SELECT
        cohort_date,
        COUNT(DISTINCT user_id) AS cohort_size,
        COUNT(DISTINCT CASE WHEN day_diff = 0 THEN user_id END) AS d0,
        COUNT(DISTINCT CASE WHEN day_diff = 1 THEN user_id END) AS d1,
        COUNT(DISTINCT CASE WHEN day_diff = 7 THEN user_id END) AS d7,
        COUNT(DISTINCT CASE WHEN day_diff = 30 THEN user_id END) AS d30
    FROM retention
    GROUP BY cohort_date
)

SELECT
    cohort_date,
    cohort_size,
    d0,
    d1,
    d7,
    d30,
    ROUND(d1 * 100.0 / NULLIF(d0, 0), 2) AS d1_rate,
    ROUND(d7 * 100.0 / NULLIF(d0, 0), 2) AS d7_rate,
    ROUND(d30 * 100.0 / NULLIF(d0, 0), 2) AS d30_rate
FROM cohort_agg
ORDER BY cohort_date
```

---

## 十一、dbt文档

### 11.1 自动生成数据字典和血缘图

```bash
dbt docs generate

dbt docs serve --port 8080
```

### 11.2 文档增强：模型级描述

```yaml
models/marts/marketing/_marketing__models.yml:

version: 2

models:
  - name: dim_users
    description: >
      用户维度表，整合用户基础信息和订单汇总指标。
      每行代表一个用户，包含用户属性和RFM分层。
      数据更新频率: 每日T+1
      数据负责人: 数据平台-张三
    columns:
      - name: user_key
        description: "用户代理键，由user_id生成的SHA256哈希值"
      - name: user_id
        description: "用户业务ID，来源于raw_ecommerce.users表"
      - name: user_tier
        description: >
          用户分层，基于订单数量:
          - 无订单: 0笔
          - 新客: 1笔
          - 普通客户: 2-5笔
          - 活跃客户: 6-20笔
          - VIP客户: 20笔以上
      - name: value_tier
        description: >
          价值分层，基于累计支付金额:
          - 高价值: >=10000元
          - 中价值: 3000-10000元
          - 低价值: <3000元

  - name: mart_user_retention
    description: >
      用户留存分析表，按首次下单日期（cohort）分组，
      计算D1/D7/D30留存率和留存人数。
      用于评估用户粘性和获客质量。
```

### 11.3 文档增强：列级描述和示例

```yaml
models/marts/finance/_finance__models.yml:

version: 2

models:
  - name: fct_orders
    description: "订单事实表"
    columns:
      - name: order_key
        description: "订单代理键"
        meta:
          pii: false
          masking_required: false
      - name: order_id
        description: "订单业务ID"
        meta:
          pii: false
          business_key: true
      - name: total_amount
        description: "订单总金额，单位：元"
        meta:
          metric: true
          unit: "元"
          range: "[0, 1000000]"
      - name: amount_mismatch_flag
        description: "金额不一致标记，当total_amount与calculated_total差异超过0.01时为True"
        meta:
          quality_check: true
          alert_on_true: true
```

---

## 十二、Snapshot：维度历史追踪

### 12.1 Snapshot配置

```sql
snapshots/snap_users.sql:

{% snapshot snap_users %}

{{
    config(
        target_schema='snapshots',
        strategy='timestamp',
        updated_at='updated_at',
        check_cols=['user_name', 'email', 'user_gender', 'user_province', 'user_city'],
        unique_key='user_id',
        invalidate_hard_deletes=True
    )
}}

SELECT * FROM {{ ref('stg_users') }}

{% endsnapshot %}
```

### 12.2 Snapshot查询

```sql
SELECT
    user_id,
    user_name,
    user_gender,
    user_province,
    dbt_valid_from,
    dbt_valid_to,
    CASE
        WHEN dbt_valid_to IS NULL THEN '当前有效'
        ELSE '已失效'
    END AS record_status
FROM snapshots.snap_users
WHERE user_id = 1001
ORDER BY dbt_valid_from
```

---

## 十三、dbt与Airflow集成

### 13.1 dbt Cloud方式

```
dbt Cloud + Airflow集成:

  ┌──────────────────────────────────────────────────────────────────┐
  │  dbt Cloud                                                       │
  │                                                                  │
  │  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   │
  │  │  代码仓库 │   │  CI/CD   │   │  调度运行 │   │  文档站点 │   │
  │  │  GitHub  │──→│  PR检查  │──→│  定时执行 │──→│  自动发布 │   │
  │  └──────────┘   └──────────┘   └──────────┘   └──────────┘   │
  │                                      ↑                          │
  │                                      │ dbt Cloud API            │
  │  ┌──────────────────────────────────┘                          │
  │  │  Airflow                                                      │
  │  │  DbtCloudRunJobOperator → 触发dbt Cloud Job                  │
  │  │  DbtCloudGetJobRunStatusOperator → 轮询运行状态              │
  └──────────────────────────────────────────────────────────────────┘
```

### 13.2 Airflow dbt operator方式

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.amazon.aws.operators.s3 import S3CreateBucketOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'dbt_warehouse_pipeline',
    default_args=default_args,
    schedule_interval='0 6 * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_runs=1,
) as dag:

    dbt_run_staging = BashOperator(
        task_id='dbt_run_staging',
        bash_command='cd /opt/airflow/dags/ecommerce_warehouse && dbt run --select staging.*',
    )

    dbt_run_intermediate = BashOperator(
        task_id='dbt_run_intermediate',
        bash_command='cd /opt/airflow/dags/ecommerce_warehouse && dbt run --select intermediate.*',
    )

    dbt_run_marts = BashOperator(
        task_id='dbt_run_marts',
        bash_command='cd /opt/airflow/dags/ecommerce_warehouse && dbt run --select marts.*',
    )

    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='cd /opt/airflow/dags/ecommerce_warehouse && dbt test',
    )

    dbt_snapshot = BashOperator(
        task_id='dbt_snapshot',
        bash_command='cd /opt/airflow/dags/ecommerce_warehouse && dbt snapshot',
    )

    dbt_docs = BashOperator(
        task_id='dbt_docs_generate',
        bash_command='cd /opt/airflow/dags/ecommerce_warehouse && dbt docs generate',
    )

    dbt_run_staging >> dbt_run_intermediate >> dbt_run_marts >> dbt_test >> dbt_snapshot >> dbt_docs
```

### 13.3 使用cosmos运营商（推荐）

```python
from airflow import DAG
from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.constants import ExecutionMode
from datetime import datetime

profile_config = ProfileConfig(
    profile_name='ecommerce_warehouse',
    target_name='dev',
    profiles_yml_filepath='/opt/airflow/dags/profiles.yml',
)

dbt_warehouse_dag = DbtDag(
    dag_id='dbt_warehouse_cosmos',
    project_config=ProjectConfig(
        dbt_project_path='/opt/airflow/dags/ecommerce_warehouse',
    ),
    profile_config=profile_config,
    execution_config=ExecutionConfig(
        execution_mode=ExecutionMode.LOCAL,
    ),
    schedule_interval='0 6 * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args={'retries': 2},
    tags=['dbt', 'warehouse'],
)
```

---

## 十四、课堂练习（45min）

### 练习1：初始化dbt项目连接到DuckDB（10min）

```bash
pip install dbt-duckdb

mkdir -p ~/dbt_lab && cd ~/dbt_lab

dbt init ecommerce_lab --adapter duckdb

cd ecommerce_lab
```

编辑 `~/.dbt/profiles.yml`:

```yaml
ecommerce_lab:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: "./ecommerce_lab.duckdb"
      threads: 4
```

```bash
dbt debug

dbt run --select staging.*
```

### 练习2：创建3层模型（20min）

```bash
mkdir -p models/staging models/intermediate models/marts/finance models/marts/marketing models/marts/product
```

创建Source定义 `models/staging/_sources.yml`（参考第五节内容）。

创建Staging层模型:
- `models/staging/stg_orders.sql`
- `models/staging/stg_users.sql`
- `models/staging/stg_products.sql`

创建Intermediate层模型:
- `models/intermediate/int_orders_enriched.sql`
- `models/intermediate/int_user_order_summary.sql`

创建Marts层模型:
- `models/marts/finance/fct_orders.sql`
- `models/marts/marketing/dim_users.sql`

```bash
dbt run

dbt run --select staging.*

dbt run --select intermediate.*

dbt run --select marts.*
```

### 练习3：运行dbt test验证数据质量（10min）

创建Schema Test定义（参考第九节内容）。

创建自定义测试:
- `tests/assert_order_amount_positive.sql`
- `tests/assert_no_orphan_order_details.sql`

```bash
dbt test

dbt test --select staging

dbt test --select marts

dbt test --select assert_order_amount_positive
```

### 练习4：生成dbt docs查看文档和血缘（5min）

```bash
dbt docs generate

dbt docs serve --port 8080
```

打开浏览器访问 `http://localhost:8080`，查看:
1. 左侧模型列表，点击查看每个模型的详情
2. 右上角DAG图标，查看模型依赖关系图（血缘图）
3. 点击具体列查看列级描述和测试

---

## 十五、课后作业

### 必做

1. **用dbt重构L1项目4的Hive SQL ETL逻辑**：将L1项目4（离线数仓构建）中的ODS→DWD→DWS→ADS全部SQL用dbt Model重写，要求:
   - 定义Source对应原始Hive表
   - Staging层对应ODS层清洗
   - Intermediate层对应DWD层关联
   - Marts层对应DWS/ADS层汇总
   - 所有模型添加列级描述

2. **实现增量模型处理每日新增数据**：选择至少2个Marts层模型改为增量模型，要求:
   - 使用merge策略处理订单事实表的更新
   - 使用insert_overwrite策略处理每日汇总表的分区刷新
   - 验证增量运行结果与全量运行一致

3. **编写至少10个数据质量测试**：包含:
   - 4个Schema Test（unique/not_null/accepted_values/relationships各至少1个）
   - 3个dbt_expectations扩展测试
   - 3个自定义SQL测试（业务规则验证）

4. **生成完整的数据文档**：运行 `dbt docs generate`，要求:
   - 每个模型有模型级描述
   - 关键列有列级描述和meta标注
   - 截图展示DAG血缘图

### 选做

1. 实现Snapshot追踪用户维度变化，查询某个用户的历史变更记录
2. 编写至少3个Macro，实现可复用的SQL逻辑
3. 配置Airflow + cosmos运营商编排dbt项目

---

## 十六、参考资料

- [dbt官方文档](https://docs.getdbt.com/)
- [dbt Core GitHub](https://github.com/dbt-labs/dbt-core)
- [dbt最佳实践：项目结构](https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview)
- [dbt增量模型](https://docs.getdbt.com/docs/build/incremental-models-overview)
- [dbt测试](https://docs.getdbt.com/docs/build/data-tests)
- [dbt Snapshot](https://docs.getdbt.com/docs/build/snapshots)
- [dbt Macros](https://docs.getdbt.com/docs/build/jinja-macros)
- [Astronomer Cosmos](https://astronomer.github.io/astronomer-cosmos/)
- [dbt DuckDB适配器](https://github.com/duckdb/dbt-duckdb)
- [dbt Expectations](https://github.com/calogica/dbt-expectations)
