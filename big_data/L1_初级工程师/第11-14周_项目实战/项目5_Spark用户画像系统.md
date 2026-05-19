# 项目5：Spark用户画像系统

> **项目周期**：25小时（设计6h + 开发14h + 测试3h + 文档2h）
>
> **难度等级**：⭐⭐⭐⭐⭐ L1核心项目
>
> **小组人数**：2人协作

---

## 一、项目描述

基于Spark构建电商用户画像标签系统，从用户基础属性、行为偏好、消费能力、生命周期四个维度生成用户的360度画像标签。系统需要从DWD/DWS层读取数据，通过规则和统计方法生成标签，最终输出用户画像宽表。

---

## 二、项目目标

1. **掌握标签体系设计方法论**：理解标签分类、标签粒度、标签生命周期
2. **实践Spark数据处理**：综合运用DataFrame API和Spark SQL进行复杂数据加工
3. **理解RFM模型**：掌握Recency-Frequency-Monetary用户价值分析模型
4. **产出可用的用户画像系统**：生成每个用户完整标签的宽表

---

## 三、标签体系设计

```
用户画像标签体系（4大类 × 20+标签）:

┌─────────────────────────────────────────────────────────────┐
│                    用户360度画像标签                           │
├───────────────┬───────────────┬───────────────┬─────────────┤
│  基础属性标签  │  行为偏好标签  │  消费能力标签  │ 生命周期标签 │
├───────────────┼───────────────┼───────────────┼─────────────┤
│ 性别          │ 品类偏好TOP3  │ 消费能力等级   │ 用户阶段     │
│ 年龄段        │ 价格敏感度    │ R(最近消费)   │ 最近访问天数 │
│ 城市等级      │ 购物时段偏好  │ F(消费频率)   │ 7天活跃度    │
│ 会员等级      │ 购买频次级别  │ M(消费金额)   │ 30天活跃度   │
│ 注册天数      │ 平均客单价    │ RFM总分       │ 是否流失预警 │
│               │ 品牌偏好      │               │             │
└───────────────┴───────────────┴───────────────┴─────────────┘
```

### 3.1 基础属性标签

```yaml
标签1: 性别
  来源: dwd_user_register.gender
  类型: 离散值
  取值: 男 / 女 / 未知
  
标签2: 年龄段
  来源: dwd_user_register.age
  类型: 离散值
  规则:
    - 18岁以下  → 青少年
    - 18-24岁   → 青年
    - 25-34岁   → 中青年
    - 35-44岁   → 中年
    - 45岁以上  → 中老年

标签3: 城市等级
  来源: dwd_user_register.city
  类型: 离散值
  规则:
    一线:   北京/上海/广州/深圳
    新一线: 杭州/成都/武汉/南京/重庆/西安/苏州/天津
    二线:   长沙/郑州/东莞/青岛/沈阳/合肥/佛山/...
    其他:   三线及以下

标签4: 会员等级
  来源: dwd_user_register.user_level
  类型: 离散值
  取值: 普通/白银/黄金/VIP

标签5: 注册天数
  来源: dwd_user_register.register_date
  类型: 连续值
  公式: DATEDIFF(当前日期, register_date)
```

### 3.2 行为偏好标签

```yaml
标签6-8: 品类偏好TOP3
  来源: dws_sku_action_day (最近30天汇总)
  类型: 列表
  计算:
    1. 统计用户每个品类的PV
    2. 按PV降序排列
    3. 取TOP3

标签9: 价格敏感度
  来源: dwd_order_detail
  类型: 离散值
  计算: 用户购买商品的平均价格偏离度
  规则:
    - 价格低于品类均价50%  → 高敏感
    - 价格在均价±50%内     → 中敏感
    - 价格高于均价150%     → 低敏感

标签10: 购物时段偏好
  来源: dwd_user_log
  类型: 离散值
  规则:
    - 06:00-12:00  → 上午型
    - 12:00-18:00  → 下午型
    - 18:00-24:00  → 晚间型
    - 24:00-06:00  → 夜间型
    取行为占比最高的时段

标签11: 购买频次级别
  来源: dws_user_action_day (最近30天)
  类型: 离散值
  规则:
    - buy_count >= 30 → 高频(每天至少1次)
    - buy_count >= 10 → 中频
    - buy_count >= 3  → 低频
    - buy_count < 3   → 极低频

标签12: 平均客单价区间
  来源: dws_trade_user_order_day (最近30天)
  类型: 离散值
  规则:
    - avg >= 1000 → 高客单价
    - avg >= 300  → 中客单价
    - avg >= 100  → 标准客单价
    - avg < 100   → 低客单价

标签13: 品牌偏好
  来源: dwd_order_detail
  类型: 列表
  计算: 购买次数最多的TOP3品牌
```

### 3.3 消费能力标签（RFM模型）

```
RFM模型说明:
  R (Recency) - 最近一次消费时间: 越近越好
  F (Frequency) - 消费频率: 越高越好
  M (Monetary) - 消费金额: 越高越好

计算步骤:
  1. 计算每个用户的三项指标值
  2. 对每项指标进行评分(1-5分)
     - R: 越小越好 → 越近分越高 → 5级分段
     - F: 越大越好 → 越高分越高 → 5级分段
     - M: 越大越好 → 越高分越高 → 5级分段
  3. RFM总分 = R_score + F_score + M_score
  4. 用户分层:
     - 15分(5+5+5) → 顶级高价值
     - 12-14分      → 高价值
     - 8-11分       → 中等价值
     - 4-7分        → 低价值
     - 3分          → 流失风险
```

### 3.4 生命周期标签

```yaml
标签: 用户生命周期阶段
  规则:
    - 首次活跃在最近7天内                → 新用户
    - 最近7天有活跃，且非新用户           → 活跃用户
    - 最近7天无活跃，但30天内有活跃      → 沉默用户
    - 最近30天无活跃                     → 流失用户

标签: 最近访问距今天数
  来源: dws_user_action_day
  公式: DATEDIFF(当前日期, MAX(dt))

标签: 7天活跃度
  公式: 最近7天有行为的天数 / 7

标签: 30天活跃度
  公式: 最近30天有行为的天数 / 30

标签: 是否流失预警
  规则: 最近7天无活跃 且 历史总购买>0 → 预警
```

---

## 四、核心代码实现

### 4.1 主程序入口

```python
"""
user_profile_builder.py — 用户画像构建主程序

执行流程:
  1. 读取DWD/DWS层数据
  2. 构建基础属性标签
  3. 构建行为偏好标签
  4. 构建消费能力标签(RFM)
  5. 构建生命周期标签
  6. 合并所有标签输出画像宽表
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.window import Window

spark = SparkSession.builder \
    .appName("UserProfileBuilder") \
    .enableHiveSupport() \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.shuffle.partitions", "200") \
    .getOrCreate()

# 当前日期和30天前
CURRENT_DATE = "2024-03-31"
DATE_30_AGO = "2024-03-01"

# ============================================================
# 第一步：加载基础数据
# ============================================================

# 用户注册信息（最新快照）
users_df = spark.sql(f"""
    SELECT user_id, username, gender, age, province, city,
           register_date, user_level
    FROM dwd.dwd_user_register
    WHERE dt = '{CURRENT_DATE}'
""")

# 最近30天用户行为汇总
user_actions_30d = spark.sql(f"""
    SELECT user_id,
           SUM(pv_count) as pv_30d,
           SUM(cart_count) as cart_30d,
           SUM(fav_count) as fav_30d,
           SUM(buy_count) as buy_30d,
           COUNT(DISTINCT dt) as active_days_30d
    FROM dws.dws_user_action_day
    WHERE dt >= '{DATE_30_AGO}' AND dt <= '{CURRENT_DATE}'
    GROUP BY user_id
""")

# 最近7天用户行为
user_actions_7d = spark.sql(f"""
    SELECT user_id,
           COUNT(DISTINCT dt) as active_days_7d
    FROM dws.dws_user_action_day
    WHERE dt >= DATE_SUB('{CURRENT_DATE}', 7) AND dt <= '{CURRENT_DATE}'
    GROUP BY user_id
""")

# 最近30天订单数据
user_orders_30d = spark.sql(f"""
    SELECT user_id,
           COUNT(DISTINCT order_id) as order_count_30d,
           SUM(payment_amount) as total_payment_30d,
           AVG(payment_amount) as avg_payment_30d,
           MAX(dt) as last_purchase_date
    FROM dws.dws_trade_user_order_day
    WHERE dt >= '{DATE_30_AGO}' AND dt <= '{CURRENT_DATE}'
    GROUP BY user_id
""")

# 品类偏好数据
category_pref = spark.sql(f"""
    SELECT user_id, category_id, category_name,
           SUM(pv_count) as total_pv
    FROM dws.dws_sku_action_day
    WHERE dt >= '{DATE_30_AGO}' AND dt <= '{CURRENT_DATE}'
    GROUP BY user_id, category_id, category_name
""")


# ============================================================
# 第二步：构建基础属性标签
# ============================================================

def build_basic_tags(users_df):
    """构建基础属性标签"""
    return users_df \
        .withColumn("age_group",
            when(col("age") < 18, "青少年")
            .when(col("age") <= 24, "青年")
            .when(col("age") <= 34, "中青年")
            .when(col("age") <= 44, "中年")
            .otherwise("中老年")
        ) \
        .withColumn("city_level",
            when(col("city").isin("北京", "上海", "广州", "深圳"), "一线")
            .when(col("city").isin("杭州", "成都", "武汉", "南京",
                  "重庆", "西安", "苏州", "天津"), "新一线")
            .when(col("city").isin("长沙", "郑州", "东莞", "青岛",
                  "沈阳", "合肥", "佛山"), "二线")
            .otherwise("三线及以下")
        ) \
        .withColumn("register_days",
            datediff(lit(CURRENT_DATE), to_date(col("register_date")))
        ) \
        .select(
            "user_id", "gender", "age_group",
            "city_level", "user_level", "register_days"
        )
```

### 4.2 行为偏好标签

```python
def build_behavior_tags(spark, category_pref, user_actions_30d, user_orders_30d):
    """构建行为偏好标签"""

    # === 品类偏好TOP3 ===
    window_spec = Window.partitionBy("user_id").orderBy(col("total_pv").desc())
    top3_categories = category_pref \
        .withColumn("rank", row_number().over(window_spec)) \
        .filter(col("rank") <= 3) \
        .groupBy("user_id") \
        .agg(
            collect_list(
                struct(col("category_name"), col("total_pv"))
            ).alias("top3_categories")
        )

    # === 价格敏感度 ===
    price_sensitivity = user_orders_30d \
        .withColumn("price_sensitivity",
            when(col("avg_payment_30d") < 100, "高敏感")
            .when(col("avg_payment_30d") < 500, "中敏感")
            .otherwise("低敏感")
        ) \
        .select("user_id", "price_sensitivity")

    # === 购物频次级别 ===
    frequency_level = user_actions_30d \
        .withColumn("frequency_level",
            when(col("buy_30d") >= 30, "高频")
            .when(col("buy_30d") >= 10, "中频")
            .when(col("buy_30d") >= 3, "低频")
            .otherwise("极低频")
        ) \
        .select("user_id", "frequency_level")

    # === 客单价区间 ===
    avg_price_level = user_orders_30d \
        .withColumn("avg_price_level",
            when(col("avg_payment_30d") >= 1000, "高客单价")
            .when(col("avg_payment_30d") >= 300, "中客单价")
            .when(col("avg_payment_30d") >= 100, "标准客单价")
            .when(col("avg_payment_30d").isNull(), "无消费")
            .otherwise("低客单价")
        ) \
        .select("user_id", "avg_price_level")

    # 合并所有行为标签
    behavior_tags = top3_categories \
        .join(price_sensitivity, "user_id", "outer") \
        .join(frequency_level, "user_id", "outer") \
        .join(avg_price_level, "user_id", "outer") \
        .fillna({"price_sensitivity": "未知", "frequency_level": "无行为",
                 "avg_price_level": "无消费"})

    return behavior_tags
```

### 4.3 RFM消费能力标签

```python
def build_rfm_tags(user_orders_30d):
    """构建RFM消费能力标签"""

    rfm_raw = user_orders_30d \
        .withColumn("recency_days",
            datediff(lit(CURRENT_DATE), to_date(col("last_purchase_date")))
        ) \
        .fillna({"recency_days": 999, "order_count_30d": 0, "total_payment_30d": 0}) \
        .select("user_id", "recency_days", col("order_count_30d").alias("frequency"),
                col("total_payment_30d").alias("monetary"))

    # RFM评分 (1-5分)
    # R: 越小越好 → 需要反转排序
    rfm_scored = rfm_raw \
        .withColumn("r_score",
            ntile(5).over(Window.orderBy(col("recency_days").desc()))
        ) \
        .withColumn("f_score",
            ntile(5).over(Window.orderBy("frequency"))
        ) \
        .withColumn("m_score",
            ntile(5).over(Window.orderBy("monetary"))
        ) \
        .withColumn("rfm_total",
            col("r_score") + col("f_score") + col("m_score")
        ) \
        .withColumn("value_segment",
            when(col("rfm_total") >= 15, "顶级高价值")
            .when(col("rfm_total") >= 12, "高价值")
            .when(col("rfm_total") >= 8, "中等价值")
            .when(col("rfm_total") >= 4, "低价值")
            .otherwise("流失风险")
        ) \
        .select("user_id", "recency_days", "frequency", "monetary",
                "r_score", "f_score", "m_score", "rfm_total", "value_segment")

    return rfm_scored
```

### 4.4 生命周期标签

```python
def build_lifecycle_tags(users_df, user_actions_7d, user_actions_30d, user_orders_30d):
    """构建生命周期标签"""

    # 获取最后活跃日期
    last_active = user_actions_30d \
        .join(users_df.select("user_id", "register_date"), "user_id", "outer")

    lifecycle = users_df \
        .select("user_id", "register_date") \
        .join(user_actions_7d.select(
            col("user_id"), col("active_days_7d")), "user_id", "left") \
        .join(user_actions_30d.select(
            col("user_id"), col("active_days_30d")), "user_id", "left") \
        .withColumn("is_new_user",
            when(datediff(lit(CURRENT_DATE), to_date(col("register_date"))) <= 7, 1)
            .otherwise(0)
        ) \
        .withColumn("lifecycle_stage",
            when(col("is_new_user") == 1, "新用户")
            .when(col("active_days_7d") > 0, "活跃用户")
            .when(col("active_days_30d") > 0, "沉默用户")
            .otherwise("流失用户")
        ) \
        .withColumn("active_rate_7d",
            round(coalesce(col("active_days_7d"), lit(0)) / 7, 2)
        ) \
        .withColumn("active_rate_30d",
            round(coalesce(col("active_days_30d"), lit(0)) / 30, 2)
        ) \
        .withColumn("is_churn_risk",
            when((col("active_days_7d").isNull()) | (col("active_days_7d") == 0), 1)
            .otherwise(0)
        ) \
        .select("user_id", "lifecycle_stage", "active_rate_7d",
                "active_rate_30d", "is_churn_risk")

    return lifecycle
```

### 4.5 合并输出最终画像

```python
def build_final_profile():
    """构建最终用户画像宽表"""

    # 构建各维度标签
    basic_tags = build_basic_tags(users_df)
    behavior_tags = build_behavior_tags(spark, category_pref, user_actions_30d, user_orders_30d)
    rfm_tags = build_rfm_tags(user_orders_30d)
    lifecycle_tags = build_lifecycle_tags(users_df, user_actions_7d, user_actions_30d, user_orders_30d)

    # 合并所有标签
    user_profile = basic_tags \
        .join(behavior_tags, "user_id", "left") \
        .join(rfm_tags, "user_id", "left") \
        .join(lifecycle_tags, "user_id", "left") \
        .withColumn("dt", lit(CURRENT_DATE))

    # 写入Hive表
    user_profile.write \
        .mode("overwrite") \
        .partitionBy("dt") \
        .format("parquet") \
        .saveAsTable("ads.user_profile")

    print(f"[完成] 用户画像构建完成，用户数: {user_profile.count()}")
    return user_profile

if __name__ == "__main__":
    profile = build_final_profile()
    profile.show(20, truncate=False)
    spark.stop()
```

---

## 五、标签覆盖率报告

```python
"""
tag_coverage_report.py — 标签覆盖率统计
"""
def generate_coverage_report():
    """生成每个标签的有值率报告"""
    profile = spark.table("ads.user_profile").filter(col("dt") == CURRENT_DATE)
    total_users = profile.count()

    coverage_stats = profile.select([
        (count(when(col(c).isNotNull(), 1)) / total_users * 100).alias(c)
        for c in profile.columns 
        if c not in ["user_id", "dt"]
    ])

    print("=" * 60)
    print(f"标签覆盖率报告 (总用户数: {total_users})")
    print("=" * 60)
    for col_name, coverage in zip(
        [c for c in profile.columns if c not in ["user_id", "dt"]],
        coverage_stats.collect()[0]
    ):
        status = "✓" if coverage > 70 else "⚠" if coverage > 30 else "✗"
        print(f"  {status} {col_name:25s}: {coverage:6.2f}%")
```

---

## 六、典型用户画像展示

```python
"""
展示20个典型用户的完整画像
"""

# 高价值用户
spark.sql("""
    SELECT * FROM ads.user_profile
    WHERE dt = '2024-03-31' AND value_segment = '顶级高价值'
    LIMIT 5
""").show(5, truncate=False)

# 流失风险用户
spark.sql("""
    SELECT * FROM ads.user_profile
    WHERE dt = '2024-03-31' AND is_churn_risk = 1
    LIMIT 5
""").show(5, truncate=False)

# 新用户
spark.sql("""
    SELECT * FROM ads.user_profile
    WHERE dt = '2024-03-31' AND lifecycle_stage = '新用户'
    LIMIT 5
""").show(5, truncate=False)

# 高频+高客单价用户
spark.sql("""
    SELECT * FROM ads.user_profile
    WHERE dt = '2024-03-31'
      AND frequency_level = '高频'
      AND avg_price_level = '高客单价'
    LIMIT 5
""").show(5, truncate=False)
```

---

## 七、画像表DDL

```sql
CREATE DATABASE IF NOT EXISTS ads;
USE ads;

CREATE EXTERNAL TABLE user_profile (
    user_id BIGINT COMMENT '用户ID',

    -- 基础属性
    gender STRING COMMENT '性别',
    age_group STRING COMMENT '年龄段',
    city_level STRING COMMENT '城市等级',
    user_level STRING COMMENT '会员等级',
    register_days INT COMMENT '注册天数',

    -- 行为偏好
    top3_categories ARRAY<STRUCT<category_name:STRING, total_pv:BIGINT>>
        COMMENT '品类偏好TOP3',
    price_sensitivity STRING COMMENT '价格敏感度',
    frequency_level STRING COMMENT '购买频次级别',
    avg_price_level STRING COMMENT '客单价区间',

    -- 消费能力(RFM)
    recency_days INT COMMENT '最近消费距今天数',
    frequency INT COMMENT '近30天消费频率(订单数)',
    monetary DOUBLE COMMENT '近30天消费金额',
    r_score INT COMMENT 'R评分(1-5)',
    f_score INT COMMENT 'F评分(1-5)',
    m_score INT COMMENT 'M评分(1-5)',
    rfm_total INT COMMENT 'RFM总分(3-15)',
    value_segment STRING COMMENT '价值分层',

    -- 生命周期
    lifecycle_stage STRING COMMENT '生命周期阶段',
    active_rate_7d DOUBLE COMMENT '7天活跃率',
    active_rate_30d DOUBLE COMMENT '30天活跃率',
    is_churn_risk INT COMMENT '是否流失预警(1是0否)'
)
COMMENT 'ADS-用户画像标签宽表'
PARTITIONED BY (dt STRING COMMENT '日期分区')
STORED AS PARQUET
LOCATION '/warehouse/ads/user_profile'
TBLPROPERTIES ('parquet.compression'='SNAPPY');
```

---

## 八、交付物清单

| 序号 | 交付物 | 文件 | 要求 |
|------|--------|------|------|
| 1 | 标签体系设计文档 | `标签体系设计.md` | 20+标签的定义、规则、来源表 |
| 2 | 用户画像构建脚本 | `user_profile_builder.py` | 完整Spark代码 |
| 3 | 标签覆盖率报告 | `tag_coverage_report.py` | 每个标签的有值率 |
| 4 | 典型用户画像 | `典型画像展示.md` | 20个典型用户的完整标签 |
| 5 | RFM分析结果 | `rfm_analysis.md` | RFM分布统计和分层分析 |

---

## 九、评分标准

| 评分项 | 权重 | 要求 |
|--------|------|------|
| 标签体系完整性 | 25% | 4大类共20+标签，标签定义清晰 |
| 代码实现 | 30% | 代码可运行，逻辑正确，注释清晰 |
| RFM模型正确性 | 20% | 评分逻辑正确，分层合理 |
| 画像展示 | 15% | 典型用户画像可读性好，标签有意义 |
| 覆盖率统计 | 10% | 标签覆盖率报告完整 |

---

## 十、RFM模型完整计算实现

### 10.1 RFM理论详解

RFM模型是用户价值分析的经典模型，从三个维度刻画用户消费行为：

```
Recency (最近消费)    — 用户最近一次消费距今的天数
Frequency (消费频率)  — 用户在一段时间内的购买次数
Monetary (消费金额)   — 用户在一段时间内的总消费金额

核心假设:
  ┌─────────────────────────────────────────────────┐
  │ R: 最近消费越近 → 用户越活跃 → 价值越高         │
  │ F: 消费频率越高 → 用户越忠诚 → 价值越高         │
  │ M: 消费金额越大 → 用户消费力越强 → 价值越高     │
  └─────────────────────────────────────────────────┘
```

### 10.2 完整PySpark代码实现

```python
"""
rfm_full_implementation.py — RFM模型完整实现
每一行代码都有注释说明业务含义
"""
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import *
from pyspark.sql.window import Window
from datetime import datetime, timedelta

spark = SparkSession.builder \
    .appName("RFM_Full_Implementation") \
    .enableHiveSupport() \
    .getOrCreate()

# ============================================================
# 第一步: 计算原始R/F/M指标
# ============================================================

def compute_raw_rfm(analysis_date: str, lookback_days: int = 90) -> DataFrame:
    """
    计算每个用户原始R/F/M值

    参数:
        analysis_date: 分析日期，格式 'YYYY-MM-DD'
        lookback_days: 回溯天数，默认90天

    返回:
        DataFrame with columns: user_id, recency, frequency, monetary,
                                 first_order_date, last_order_date
    """

    start_date = (datetime.strptime(analysis_date, "%Y-%m-%d")
                  - timedelta(days=lookback_days)).strftime("%Y-%m-%d")

    rfm_raw = spark.sql(f"""
        SELECT
            user_id,
            DATEDIFF('{analysis_date}', MAX(order_date)) AS recency,
            COUNT(DISTINCT order_id) AS frequency,
            SUM(payment_amount) AS monetary,
            MIN(order_date) AS first_order_date,
            MAX(order_date) AS last_order_date
        FROM dwd.dwd_order_detail
        WHERE order_date >= '{start_date}'
          AND order_date <= '{analysis_date}'
          AND order_status IN ('paid', 'completed')
        GROUP BY user_id
    """)

    # 处理极端值：为recency设置合理上限
    # 对于从未消费的用户（无order记录），后续通过全外连接补充
    rfm_raw = rfm_raw.withColumn("recency",
        when(col("recency") > 365 * 3, 365 * 3).otherwise(col("recency"))
    )

    return rfm_raw


# ============================================================
# 第二步: R/F/M分别评分（1-5分）
# ============================================================

def score_rfm(rfm_raw: DataFrame) -> DataFrame:
    """
    对R/F/M各维度进行1-5分评分

    评分策略:
      R: 越小越好 → 逆序排名（recency越小排名越高）
      F: 越大越好 → 正序排名
      M: 越大越好 → 正序排名

    使用NTILE(5)将用户均匀分为5组
    """

    rfm_scored = rfm_raw \
        .withColumn("r_score",
            ntile(5).over(Window.orderBy(col("recency").desc()))
            # desc是因为recency越小越好，需要将小的映射为高分
        ) \
        .withColumn("f_score",
            ntile(5).over(Window.orderBy(col("frequency").asc()))
        ) \
        .withColumn("m_score",
            ntile(5).over(Window.orderBy(col("monetary").asc()))
        )

    return rfm_scored


# ============================================================
# 第三步: 计算RFM总分与用户分层
# ============================================================

def segment_users(rfm_scored: DataFrame) -> DataFrame:
    """
    根据RFM总分进行用户价值分层

    分层规则:
      - rfm_total >= 14: 顶级高价值 (Top 1%)
      - rfm_total >= 12: 高价值用户
      - rfm_total >= 9:  中等价值用户
      - rfm_total >= 6:  低价值用户
      - rfm_total < 6:   流失风险用户

    附: 每层用户的典型特征描述
    """

    rfm_segmented = rfm_scored \
        .withColumn("rfm_total",
            col("r_score") + col("f_score") + col("m_score")
        ) \
        .withColumn("rfm_avg",
            round((col("r_score") + col("f_score") + col("m_score")) / 3.0, 2)
        ) \
        .withColumn("value_segment",
            when(col("rfm_total") >= 14, "顶级高价值")
            .when(col("rfm_total") >= 12, "高价值")
            .when(col("rfm_total") >= 9, "中等价值")
            .when(col("rfm_total") >= 6, "低价值")
            .otherwise("流失风险")
        ) \
        .withColumn("segment_profile",
            when(col("r_score") >= 4, "活跃型")
            .when(col("f_score") >= 4, "忠诚型")
            .when(col("m_score") >= 4, "消费型")
            .when(col("r_score") <= 2, "沉睡型")
            .otherwise("一般型")
        )

    return rfm_segmented


# ============================================================
# 第四步: 精细用户分层（R/F/M组合分析）
# ============================================================

def fine_grained_segmentation(rfm_scored: DataFrame) -> DataFrame:
    """
    基于R/F/M组合进行更精细的用户分层

    将用户分为8个细分群体:

    ┌──────────────────────────────────────────────────────────┐
    │ R分数 │ F分数 │ M分数 │ 群体名称        │ 运营策略        │
    ├──────────────────────────────────────────────────────────┤
    │ 高(4-5)│ 高    │ 高    │ 重要价值客户   │ VIP专属服务     │
    │ 高     │ 低    │ 高    │ 重要发展客户   │ 提升购买频率    │
    │ 高     │ 高    │ 低    │ 重要保持客户   │ 提升客单价      │
    │ 高     │ 低    │ 低    │ 一般价值客户   │ 培养消费习惯    │
    │ 低(1-2)│ 高    │ 高    │ 重要挽留客户   │ 紧急召回        │
    │ 低     │ 低    │ 高    │ 一次性高消费   │ 引导复购        │
    │ 低     │ 高    │ 低    │ 频繁小消费     │ 推荐高价值商品  │
    │ 低     │ 低    │ 低    │ 流失用户       │ 低成本触达      │
    └──────────────────────────────────────────────────────────┘
    """

    # 定义高/低阈值函数
    def is_high(score_col):
        return col(score_col) >= 4

    fine_segments = rfm_scored \
        .withColumn("fine_segment",
            when(is_high("r_score") & is_high("f_score") & is_high("m_score"),
                 "重要价值客户")
            .when(is_high("r_score") & ~is_high("f_score") & is_high("m_score"),
                 "重要发展客户")
            .when(is_high("r_score") & is_high("f_score") & ~is_high("m_score"),
                 "重要保持客户")
            .when(is_high("r_score") & ~is_high("f_score") & ~is_high("m_score"),
                 "一般价值客户")
            .when(~is_high("r_score") & is_high("f_score") & is_high("m_score"),
                 "重要挽留客户")
            .when(~is_high("r_score") & ~is_high("f_score") & is_high("m_score"),
                 "一次性高消费")
            .when(~is_high("r_score") & is_high("f_score") & ~is_high("m_score"),
                 "频繁小消费")
            .otherwise("流失用户")
        )

    return fine_segments


# ============================================================
# 第五步: RFM分布统计
# ============================================================

def compute_rfm_statistics(rfm_segmented: DataFrame):
    """计算RFM各层的统计指标"""

    print("=" * 70)
    print("RFM用户价值分层统计")
    print("=" * 70)

    stats = rfm_segmented.groupBy("value_segment").agg(
        count("user_id").alias("user_count"),
        round(avg("recency"), 1).alias("avg_recency"),
        round(avg("frequency"), 1).alias("avg_frequency"),
        round(avg("monetary"), 2).alias("avg_monetary"),
        round(sum("monetary"), 2).alias("total_revenue"),
        round(avg("rfm_avg"), 2).alias("avg_rfm_score")
    ).orderBy(col("total_revenue").desc())

    stats.show(20, truncate=False)

    # 计算各层占比
    total_users = rfm_segmented.count()
    stats_with_pct = stats.withColumn("pct",
        round(col("user_count") / total_users * 100, 2)
    ).withColumn("revenue_pct",
        round(col("total_revenue") / stats.agg(sum("total_revenue")).collect()[0][0] * 100, 2)
    )

    print("\n各层用户占比与收入贡献:")
    stats_with_pct.select(
        "value_segment", "user_count", "pct", "revenue_pct",
        "avg_recency", "avg_frequency", "avg_monetary"
    ).show(20, truncate=False)

    return stats_with_pct


# ============================================================
# 第六步: 主执行流程
# ============================================================

def run_rfm_pipeline(analysis_date: str = "2024-03-31"):
    """执行完整RFM分析流水线"""

    print(f"[INFO] 开始RFM分析，分析日期: {analysis_date}")

    # Step 1: 计算原始RFM
    rfm_raw = compute_raw_rfm(analysis_date)

    # Step 2: RFM评分
    rfm_scored = score_rfm(rfm_raw)

    # Step 3: 用户分层
    rfm_segmented = segment_users(rfm_scored)

    # Step 4: 精细分层
    fine_segments = fine_grained_segmentation(rfm_scored)

    # Step 5: 合并所有RFM标签
    rfm_final = rfm_segmented.join(
        fine_segments.select("user_id", "fine_segment"),
        "user_id", "left"
    )

    # Step 6: 统计
    stats = compute_rfm_statistics(rfm_segmented)

    # Step 7: 写入Hive
    rfm_final.write \
        .mode("overwrite") \
        .partitionBy("dt") \
        .format("parquet") \
        .saveAsTable("ads.user_rfm_segments")

    print(f"[DONE] RFM分析完成，结果写入 ads.user_rfm_segments")
    return rfm_final, stats


if __name__ == "__main__":
    rfm_result, rfm_stats = run_rfm_pipeline()
    spark.stop()
```

---

## 十一、Spark SQL标签生成完整代码

### 11.1 全部20+标签的Spark SQL实现

```sql
-- ============================================================
-- 用户画像标签生成SQL：一次性生成全部标签
-- 执行环境：Spark SQL (enableHiveSupport)
-- 日期参数：${analysis_date} = '2024-03-31'
-- ============================================================

-- ----------------------------------------
-- 标签1: 性别
-- ----------------------------------------
-- 来源: dwd_user_register
-- 逻辑: 直接映射
SELECT
    user_id,
    COALESCE(gender, '未知') AS tag_gender
FROM dwd.dwd_user_register
WHERE dt = '${analysis_date}';


-- ----------------------------------------
-- 标签2: 年龄段
-- ----------------------------------------
SELECT
    user_id,
    CASE
        WHEN age IS NULL THEN '未知'
        WHEN age < 18  THEN '青少年'
        WHEN age <= 24 THEN '青年'
        WHEN age <= 34 THEN '中青年'
        WHEN age <= 44 THEN '中年'
        ELSE '中老年'
    END AS tag_age_group
FROM dwd.dwd_user_register
WHERE dt = '${analysis_date}';


-- ----------------------------------------
-- 标签3: 城市等级
-- ----------------------------------------
SELECT
    user_id,
    CASE
        WHEN city IN ('北京','上海','广州','深圳')               THEN '一线'
        WHEN city IN ('杭州','成都','武汉','南京','重庆','西安','苏州','天津') THEN '新一线'
        WHEN city IN ('长沙','郑州','东莞','青岛','沈阳','合肥','佛山',
                      '宁波','昆明','福州','无锡','厦门','济南','大连',
                      '哈尔滨','温州','石家庄','泉州','南宁','长春',
                      '南昌','贵阳','金华','珠海','惠州','常州','嘉兴') THEN '二线'
        ELSE '三线及以下'
    END AS tag_city_level
FROM dwd.dwd_user_register
WHERE dt = '${analysis_date}';


-- ----------------------------------------
-- 标签4: 会员等级
-- ----------------------------------------
SELECT
    user_id,
    COALESCE(user_level, '普通') AS tag_user_level
FROM dwd.dwd_user_register
WHERE dt = '${analysis_date}';


-- ----------------------------------------
-- 标签5: 注册天数
-- ----------------------------------------
SELECT
    user_id,
    DATEDIFF('${analysis_date}', register_date) AS tag_register_days
FROM dwd.dwd_user_register
WHERE dt = '${analysis_date}';


-- ----------------------------------------
-- 标签6-8: 品类偏好TOP3 (使用窗口函数)
-- ----------------------------------------
WITH category_rank AS (
    SELECT
        user_id,
        category_id,
        category_name,
        SUM(pv_count) AS total_pv,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY SUM(pv_count) DESC) AS rn
    FROM dws.dws_sku_action_day
    WHERE dt >= DATE_SUB('${analysis_date}', 30)
      AND dt <= '${analysis_date}'
    GROUP BY user_id, category_id, category_name
)
SELECT
    user_id,
    CONCAT_WS(',',
        MAX(CASE WHEN rn = 1 THEN category_name END),
        MAX(CASE WHEN rn = 2 THEN category_name END),
        MAX(CASE WHEN rn = 3 THEN category_name END)
    ) AS tag_top3_categories,
    CONCAT_WS(',',
        CAST(MAX(CASE WHEN rn = 1 THEN total_pv END) AS STRING),
        CAST(MAX(CASE WHEN rn = 2 THEN total_pv END) AS STRING),
        CAST(MAX(CASE WHEN rn = 3 THEN total_pv END) AS STRING)
    ) AS tag_top3_categories_pv
FROM category_rank
WHERE rn <= 3
GROUP BY user_id;


-- ----------------------------------------
-- 标签9: 价格敏感度
-- ----------------------------------------
WITH user_avg_price AS (
    SELECT
        o.user_id,
        AVG(o.payment_amount / o.sku_num) AS user_avg_unit_price
    FROM dwd.dwd_order_detail o
    WHERE o.dt >= DATE_SUB('${analysis_date}', 30)
      AND o.dt <= '${analysis_date}'
      AND o.order_status IN ('paid', 'completed')
    GROUP BY o.user_id
),
category_avg_price AS (
    SELECT
        category_id,
        AVG(payment_amount / sku_num) AS category_avg_unit_price
    FROM dwd.dwd_order_detail
    WHERE dt >= DATE_SUB('${analysis_date}', 30)
      AND dt <= '${analysis_date}'
      AND order_status IN ('paid', 'completed')
    GROUP BY category_id
)
SELECT
    u.user_id,
    CASE
        WHEN u.user_avg_unit_price < ca.category_avg_unit_price * 0.5
            THEN '高敏感'
        WHEN u.user_avg_unit_price <= ca.category_avg_unit_price * 1.5
            THEN '中敏感'
        ELSE '低敏感'
    END AS tag_price_sensitivity
FROM user_avg_price u
JOIN (
    SELECT DISTINCT od.user_id, od.category_id
    FROM dwd.dwd_order_detail od
    WHERE od.dt >= DATE_SUB('${analysis_date}', 30)
      AND od.dt <= '${analysis_date}'
) od ON u.user_id = od.user_id
JOIN category_avg_price ca ON od.category_id = ca.category_id;


-- ----------------------------------------
-- 标签10: 购物时段偏好
-- ----------------------------------------
WITH hour_behavior AS (
    SELECT
        user_id,
        HOUR(FROM_UNIXTIME(ts / 1000)) AS behavior_hour,
        COUNT(*) AS behavior_count,
        CASE
            WHEN HOUR(FROM_UNIXTIME(ts / 1000)) BETWEEN 6 AND 11  THEN '上午型'
            WHEN HOUR(FROM_UNIXTIME(ts / 1000)) BETWEEN 12 AND 17 THEN '下午型'
            WHEN HOUR(FROM_UNIXTIME(ts / 1000)) BETWEEN 18 AND 23 THEN '晚间型'
            ELSE '夜间型'
        END AS time_period
    FROM dwd.dwd_user_log
    WHERE dt >= DATE_SUB('${analysis_date}', 30)
      AND dt <= '${analysis_date}'
    GROUP BY user_id, HOUR(FROM_UNIXTIME(ts / 1000))
),
period_rank AS (
    SELECT
        user_id,
        time_period,
        SUM(behavior_count) AS total_count,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY SUM(behavior_count) DESC) AS rn
    FROM hour_behavior
    GROUP BY user_id, time_period
)
SELECT
    user_id,
    time_period AS tag_shopping_time_preference
FROM period_rank
WHERE rn = 1;


-- ----------------------------------------
-- 标签11: 购买频次级别
-- ----------------------------------------
SELECT
    user_id,
    CASE
        WHEN buy_count >= 30 THEN '高频'
        WHEN buy_count >= 10 THEN '中频'
        WHEN buy_count >= 3  THEN '低频'
        ELSE '极低频'
    END AS tag_buy_frequency_level
FROM (
    SELECT
        user_id,
        SUM(buy_count) AS buy_count
    FROM dws.dws_user_action_day
    WHERE dt >= DATE_SUB('${analysis_date}', 30)
      AND dt <= '${analysis_date}'
    GROUP BY user_id
) t;


-- ----------------------------------------
-- 标签12: 平均客单价区间
-- ----------------------------------------
SELECT
    user_id,
    CASE
        WHEN avg_payment >= 1000 THEN '高客单价'
        WHEN avg_payment >= 300  THEN '中客单价'
        WHEN avg_payment >= 100  THEN '标准客单价'
        WHEN avg_payment IS NULL THEN '无消费'
        ELSE '低客单价'
    END AS tag_avg_order_value_level
FROM (
    SELECT
        user_id,
        AVG(payment_amount) AS avg_payment
    FROM dws.dws_trade_user_order_day
    WHERE dt >= DATE_SUB('${analysis_date}', 30)
      AND dt <= '${analysis_date}'
    GROUP BY user_id
) t;


-- ----------------------------------------
-- 标签13: 品牌偏好TOP3
-- ----------------------------------------
WITH brand_rank AS (
    SELECT
        user_id,
        brand,
        COUNT(DISTINCT order_id) AS buy_count,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY COUNT(DISTINCT order_id) DESC) AS rn
    FROM dwd.dwd_order_detail
    WHERE dt >= DATE_SUB('${analysis_date}', 30)
      AND dt <= '${analysis_date}'
    GROUP BY user_id, brand
)
SELECT
    user_id,
    CONCAT_WS(',',
        MAX(CASE WHEN rn = 1 THEN brand END),
        MAX(CASE WHEN rn = 2 THEN brand END),
        MAX(CASE WHEN rn = 3 THEN brand END)
    ) AS tag_top3_brands
FROM brand_rank
WHERE rn <= 3
GROUP BY user_id;


-- ----------------------------------------
-- 标签14-18: RFM标签 (单个SQL生成)
-- ----------------------------------------
WITH rfm_raw AS (
    SELECT
        user_id,
        DATEDIFF('${analysis_date}', MAX(order_date)) AS recency_days,
        COUNT(DISTINCT order_id) AS frequency,
        SUM(payment_amount) AS monetary
    FROM dwd.dwd_order_detail
    WHERE order_date >= DATE_SUB('${analysis_date}', 90)
      AND order_date <= '${analysis_date}'
      AND order_status IN ('paid', 'completed')
    GROUP BY user_id
),
rfm_scored AS (
    SELECT
        user_id,
        recency_days,
        frequency,
        monetary,
        NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score,
        NTILE(5) OVER (ORDER BY frequency ASC)   AS f_score,
        NTILE(5) OVER (ORDER BY monetary ASC)    AS m_score
    FROM rfm_raw
)
SELECT
    user_id,
    recency_days             AS tag_recency_days,
    frequency                AS tag_frequency,
    ROUND(monetary, 2)       AS tag_monetary,
    r_score                  AS tag_r_score,
    f_score                  AS tag_f_score,
    m_score                  AS tag_m_score,
    r_score + f_score + m_score AS tag_rfm_total,
    CASE
        WHEN r_score + f_score + m_score >= 14 THEN '顶级高价值'
        WHEN r_score + f_score + m_score >= 12 THEN '高价值'
        WHEN r_score + f_score + m_score >= 9  THEN '中等价值'
        WHEN r_score + f_score + m_score >= 6  THEN '低价值'
        ELSE '流失风险'
    END AS tag_value_segment
FROM rfm_scored;


-- ----------------------------------------
-- 标签19: 用户生命周期阶段
-- ----------------------------------------
WITH last_active AS (
    SELECT
        user_id,
        MAX(dt) AS last_active_date
    FROM dws.dws_user_action_day
    WHERE dt <= '${analysis_date}'
    GROUP BY user_id
),
register_info AS (
    SELECT
        user_id,
        register_date
    FROM dwd.dwd_user_register
    WHERE dt = '${analysis_date}'
)
SELECT
    r.user_id,
    CASE
        WHEN DATEDIFF('${analysis_date}', r.register_date) <= 7
            THEN '新用户'
        WHEN DATEDIFF('${analysis_date}', COALESCE(la.last_active_date, '1970-01-01')) <= 7
            THEN '活跃用户'
        WHEN DATEDIFF('${analysis_date}', COALESCE(la.last_active_date, '1970-01-01')) <= 30
            THEN '沉默用户'
        ELSE '流失用户'
    END AS tag_lifecycle_stage
FROM register_info r
LEFT JOIN last_active la ON r.user_id = la.user_id;


-- ----------------------------------------
-- 标签20: 最近访问距今天数
-- ----------------------------------------
SELECT
    user_id,
    DATEDIFF('${analysis_date}', MAX(dt)) AS tag_last_active_days
FROM dws.dws_user_action_day
WHERE dt <= '${analysis_date}'
GROUP BY user_id;


-- ----------------------------------------
-- 标签21: 7天活跃度
-- ----------------------------------------
SELECT
    user_id,
    ROUND(COUNT(DISTINCT dt) / 7.0, 2) AS tag_active_rate_7d
FROM dws.dws_user_action_day
WHERE dt >= DATE_SUB('${analysis_date}', 7)
  AND dt <= '${analysis_date}'
GROUP BY user_id;


-- ----------------------------------------
-- 标签22: 30天活跃度
-- ----------------------------------------
SELECT
    user_id,
    ROUND(COUNT(DISTINCT dt) / 30.0, 2) AS tag_active_rate_30d
FROM dws.dws_user_action_day
WHERE dt >= DATE_SUB('${analysis_date}', 30)
  AND dt <= '${analysis_date}'
GROUP BY user_id;


-- ----------------------------------------
-- 标签23: 是否流失预警
-- ----------------------------------------
WITH user_last_activity AS (
    SELECT
        user_id,
        MAX(dt) AS last_active_date
    FROM dws.dws_user_action_day
    WHERE dt <= '${analysis_date}'
    GROUP BY user_id
),
user_has_purchase AS (
    SELECT DISTINCT
        user_id,
        1 AS has_purchased
    FROM dwd.dwd_order_detail
    WHERE order_date <= '${analysis_date}'
      AND order_status IN ('paid', 'completed')
)
SELECT
    u.user_id,
    CASE
        WHEN DATEDIFF('${analysis_date}', ula.last_active_date) > 7
         AND hp.has_purchased = 1 THEN 1
        ELSE 0
    END AS tag_is_churn_risk
FROM dwd.dwd_user_register u
LEFT JOIN user_last_activity ula ON u.user_id = ula.user_id
LEFT JOIN user_has_purchase hp  ON u.user_id = hp.user_id
WHERE u.dt = '${analysis_date}';


-- ----------------------------------------
-- 标签24: 用户活跃时段（最活跃的2小时窗口）
-- ----------------------------------------
WITH hour_detail AS (
    SELECT
        user_id,
        HOUR(FROM_UNIXTIME(ts / 1000)) AS h,
        COUNT(*) AS cnt
    FROM dwd.dwd_user_log
    WHERE dt >= DATE_SUB('${analysis_date}', 30)
      AND dt <= '${analysis_date}'
    GROUP BY user_id, HOUR(FROM_UNIXTIME(ts / 1000))
),
hour_rank AS (
    SELECT
        user_id,
        h,
        cnt,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY cnt DESC) AS rn
    FROM hour_detail
)
SELECT
    user_id,
    CONCAT(
        CAST(MAX(CASE WHEN rn = 1 THEN h END) AS STRING), ':00-',
        CAST(MAX(CASE WHEN rn = 1 THEN h END) + 2 AS STRING), ':00'
    ) AS tag_peak_active_hours
FROM hour_rank
WHERE rn = 1
GROUP BY user_id;


-- ----------------------------------------
-- 标签25: 优惠券敏感度
-- ----------------------------------------
SELECT
    user_id,
    CASE
        WHEN coupon_order_ratio >= 0.7 THEN '高敏感(优惠券驱动)'
        WHEN coupon_order_ratio >= 0.3 THEN '中敏感'
        WHEN coupon_order_ratio >= 0.1 THEN '低敏感'
        WHEN coupon_order_ratio IS NULL THEN '未使用优惠券'
        ELSE '无感'
    END AS tag_coupon_sensitivity
FROM (
    SELECT
        user_id,
        SUM(CASE WHEN coupon_id IS NOT NULL AND coupon_id > 0 THEN 1 ELSE 0 END) * 1.0
            / COUNT(*) AS coupon_order_ratio
    FROM dwd.dwd_order_detail
    WHERE dt >= DATE_SUB('${analysis_date}', 30)
      AND dt <= '${analysis_date}'
      AND order_status IN ('paid', 'completed')
    GROUP BY user_id
) t;
```

### 11.2 标签全量合并SQL

```sql
-- ============================================================
-- 将所有标签合并为一张画像宽表
-- 使用FULL OUTER JOIN确保所有用户都在结果中
-- ============================================================
INSERT OVERWRITE TABLE ads.user_profile PARTITION (dt = '${analysis_date}')
SELECT
    COALESCE(basic.user_id, behavior.user_id, rfm.user_id, lifecycle.user_id) AS user_id,

    -- 基础属性标签
    basic.gender                           AS gender,
    basic.age_group                        AS age_group,
    basic.city_level                       AS city_level,
    basic.user_level                       AS user_level,
    basic.register_days                    AS register_days,

    -- 行为偏好标签
    behavior.top3_categories               AS top3_categories,
    behavior.top3_categories_pv            AS top3_categories_pv,
    behavior.price_sensitivity             AS price_sensitivity,
    behavior.shopping_time_preference      AS shopping_time_preference,
    behavior.buy_frequency_level           AS buy_frequency_level,
    behavior.avg_order_value_level         AS avg_order_value_level,
    behavior.top3_brands                   AS top3_brands,
    behavior.peak_active_hours             AS peak_active_hours,
    behavior.coupon_sensitivity            AS coupon_sensitivity,

    -- RFM消费能力标签
    rfm.recency_days                       AS recency_days,
    rfm.frequency                          AS frequency,
    rfm.monetary                           AS monetary,
    rfm.r_score                            AS r_score,
    rfm.f_score                            AS f_score,
    rfm.m_score                            AS m_score,
    rfm.rfm_total                          AS rfm_total,
    rfm.value_segment                      AS value_segment,

    -- 生命周期标签
    lifecycle.lifecycle_stage              AS lifecycle_stage,
    lifecycle.last_active_days             AS last_active_days,
    lifecycle.active_rate_7d               AS active_rate_7d,
    lifecycle.active_rate_30d              AS active_rate_30d,
    lifecycle.is_churn_risk                AS is_churn_risk

FROM (
    SELECT user_id, gender, age_group, city_level, user_level, register_days
    FROM ads.user_basic_tags
    WHERE dt = '${analysis_date}'
) basic

FULL OUTER JOIN (
    SELECT user_id, top3_categories, top3_categories_pv, price_sensitivity,
           shopping_time_preference, buy_frequency_level, avg_order_value_level,
           top3_brands, peak_active_hours, coupon_sensitivity
    FROM ads.user_behavior_tags
    WHERE dt = '${analysis_date}'
) behavior
ON basic.user_id = behavior.user_id

FULL OUTER JOIN (
    SELECT user_id, recency_days, frequency, monetary,
           r_score, f_score, m_score, rfm_total, value_segment
    FROM ads.user_rfm_tags
    WHERE dt = '${analysis_date}'
) rfm
ON COALESCE(basic.user_id, behavior.user_id) = rfm.user_id

FULL OUTER JOIN (
    SELECT user_id, lifecycle_stage, last_active_days,
           active_rate_7d, active_rate_30d, is_churn_risk
    FROM ads.user_lifecycle_tags
    WHERE dt = '${analysis_date}'
) lifecycle
ON COALESCE(basic.user_id, behavior.user_id, rfm.user_id) = lifecycle.user_id;
```

---

## 十二、标签存储方案详细说明

### 12.1 整体存储架构

```
用户画像存储架构
┌─────────────────────────────────────────────────────────────────┐
│                      用户画像数据流                              │
├───────────────┬───────────────┬───────────────┬────────────────┤
│   中间标签表   │   画像宽表     │   查询服务层   │   应用消费层    │
│  (Intermediate)│   (Wide Table) │  (Query API)  │  (Applications)│
├───────────────┼───────────────┼───────────────┼────────────────┤
│ Parquet       │ Parquet       │ Hive/Spark SQL│ 推荐系统        │
│ 按标签分类存储 │ 按日期分区    │ Presto        │ 营销系统        │
│ SNAPPY压缩    │ SNAPPY+字典   │ Elasticsearch │ 用户分析        │
│               │ Bloom Filter  │ (按需同步)    │ BI报表          │
└───────────────┴───────────────┴───────────────┴────────────────┘
```

### 12.2 Parquet分区策略

```sql
-- ============================================================
-- 存储方案1: 中间标签表 — 按标签类别分表存储
-- ============================================================

-- 基础属性标签表
CREATE TABLE ads.user_basic_tags (
    user_id         BIGINT COMMENT '用户ID',
    gender          STRING COMMENT '性别标签',
    age_group       STRING COMMENT '年龄段标签',
    city_level      STRING COMMENT '城市等级标签',
    user_level      STRING COMMENT '会员等级标签',
    register_days   INT    COMMENT '注册天数标签'
)
COMMENT '用户基础属性标签'
PARTITIONED BY (dt STRING COMMENT '日期分区')
STORED AS PARQUET
LOCATION '/warehouse/ads/user_basic_tags'
TBLPROPERTIES (
    'parquet.compression' = 'SNAPPY',
    'parquet.bloom.filter.enabled' = 'true',
    'parquet.bloom.filter.columns' = 'user_id'
);

-- 行为偏好标签表
CREATE TABLE ads.user_behavior_tags (
    user_id                 BIGINT  COMMENT '用户ID',
    top3_categories         STRING  COMMENT '品类偏好TOP3',
    top3_categories_pv      STRING  COMMENT '品类偏好TOP3对应的PV',
    price_sensitivity       STRING  COMMENT '价格敏感度',
    shopping_time_preference STRING COMMENT '购物时段偏好',
    buy_frequency_level     STRING  COMMENT '购买频次级别',
    avg_order_value_level   STRING  COMMENT '客单价区间',
    top3_brands             STRING  COMMENT '品牌偏好TOP3',
    peak_active_hours       STRING  COMMENT '活跃高峰时段',
    coupon_sensitivity      STRING  COMMENT '优惠券敏感度'
)
COMMENT '用户行为偏好标签'
PARTITIONED BY (dt STRING COMMENT '日期分区')
STORED AS PARQUET
LOCATION '/warehouse/ads/user_behavior_tags'
TBLPROPERTIES (
    'parquet.compression' = 'SNAPPY'
);

-- RFM标签表
CREATE TABLE ads.user_rfm_tags (
    user_id         BIGINT  COMMENT '用户ID',
    recency_days    INT     COMMENT '最近消费距今天数',
    frequency       INT     COMMENT '消费频率',
    monetary        DOUBLE  COMMENT '消费金额',
    r_score         INT     COMMENT 'R评分(1-5)',
    f_score         INT     COMMENT 'F评分(1-5)',
    m_score         INT     COMMENT 'M评分(1-5)',
    rfm_total       INT     COMMENT 'RFM总分',
    value_segment   STRING  COMMENT '价值分层'
)
COMMENT '用户RFM消费能力标签'
PARTITIONED BY (dt STRING COMMENT '日期分区')
STORED AS PARQUET
LOCATION '/warehouse/ads/user_rfm_tags'
TBLPROPERTIES (
    'parquet.compression' = 'SNAPPY',
    'parquet.bloom.filter.enabled' = 'true',
    'parquet.bloom.filter.columns' = 'user_id,value_segment'
);

-- 生命周期标签表
CREATE TABLE ads.user_lifecycle_tags (
    user_id             BIGINT  COMMENT '用户ID',
    lifecycle_stage     STRING  COMMENT '生命周期阶段',
    last_active_days    INT     COMMENT '最近访问距今天数',
    active_rate_7d      DOUBLE  COMMENT '7天活跃率',
    active_rate_30d     DOUBLE  COMMENT '30天活跃率',
    is_churn_risk       INT     COMMENT '是否流失预警'
)
COMMENT '用户生命周期标签'
PARTITIONED BY (dt STRING COMMENT '日期分区')
STORED AS PARQUET
LOCATION '/warehouse/ads/user_lifecycle_tags'
TBLPROPERTIES (
    'parquet.compression' = 'SNAPPY'
);
```

### 12.3 存储选型理由

```
存储格式选型对照表:

┌──────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
│     维度      │   TextFile   │    ORC       │   Parquet    │    Avro      │
├──────────────┼──────────────┼──────────────┼──────────────┼──────────────┤
│ 列式存储      │     ✗        │     ✓        │     ✓        │     ✗        │
│ 压缩率        │    低        │    很高       │    高        │    中        │
│ 谓词下推      │     ✗        │     ✓        │     ✓        │     ✗        │
│ 嵌套结构      │     ✗        │   有限        │    优秀       │     ✓        │
│ Hive兼容性    │     ✓        │     ✓        │     ✓        │     ✓        │
│ Spark性能     │    低        │    高        │    最高       │    中        │
│ 列裁剪效率    │    无        │    高        │    高        │    无        │
│ 生态集成      │   通用       │   Hive为主    │  Spark为主   │   Kafka为主  │
└──────────────┴──────────────┴──────────────┴──────────────┴──────────────┘

选择Parquet的理由:
  1. 列式存储: 用户画像查询通常只需要几个标签列（如查询"高价值+高频"用户），
     Parquet的列裁剪可以只读取需要的列，对于宽表（20+列）效果显著
  2. 压缩率: SNAPPY压缩兼顾压缩比和CPU开销，画像数据压缩比可达3:1~5:1
  3. 嵌套结构支持: 画像中的品类偏好TOP3、品牌偏好TOP3是ARRAY/STRUCT类型，
     Parquet天然支持
  4. Spark原生优化: Parquet是Spark默认的列式格式，Catalyst优化器对其有最深度的优化
  5. Bloom Filter: Parquet支持布隆过滤器，在user_id等高频过滤列上建Bloom Filter
     可以显著加速点查（如"查询user_id=12345的画像"）

选择日期分区而非小时分区的理由:
  1. 用户画像是T+1更新的离线标签，不需要小时级时效性
  2. 日分区粒度适中，单个分区文件数可控（避免小文件问题）
  3. 查询时只需要指定dt分区即可实现分区裁剪

位图索引选型分析:
  位图索引适用于低基数列（如性别、城市等级、生命周期阶段），
  但Hive/Spark原生不支持传统位图索引，替代方案:
  
  方案A: Parquet Bloom Filter（推荐）
    - 在user_id上创建Bloom Filter索引
    - 加速点查: WHERE user_id = 12345
    - 配置: TBLPROPERTIES('parquet.bloom.filter.columns'='user_id')
  
  方案B: ORC的内置索引（备选）
    - ORC支持bloom filter和min/max索引
    - 但Spark对ORC的优化不如Parquet深
  
  方案C: 独立索引表（高频查询场景）
    - 创建 user_id → file_path 的映射表
    - 先查索引表定位文件，再读Parquet文件
    - 适用于超大规模（亿级用户）场景

  方案D: ClickHouse/Elasticsearch（实时查询场景）
    - 将画像数据同步到ES/ClickHouse
    - 提供毫秒级多维组合查询
    - 适用于需要实时交互式画像查询的场景
```

### 12.4 小文件合并策略

```python
"""
小文件合并工具: 防止画像表产生过多小文件
"""
def compact_small_files(spark, table_name: str, dt: str):
    """
    合并某个分区的小文件

    问题: 用户画像每日产出时，如果有200个Task，
         每个Task写一个小文件 → 200个小文件/天/表
         累积1年 → 73000个小文件 → NameNode压力巨大

    解决: 写入后执行REPARTITION合并
    """
    df = spark.table(table_name).filter(col("dt") == dt)

    # 策略1: 估算合适的分区数（每个文件128MB-256MB）
    file_size_mb = 128
    total_rows = df.count()
    estimated_row_size_bytes = 500  # 每行约500字节
    total_mb = total_rows * estimated_row_size_bytes / (1024 * 1024)
    target_partitions = max(1, int(total_mb / file_size_mb))

    print(f"[小文件合并] 表={table_name}, 行数={total_rows}, "
          f"估算大小={total_mb:.1f}MB, 目标分区数={target_partitions}")

    # 策略2: 重写分区
    df.repartition(target_partitions) \
      .write \
      .mode("overwrite") \
      .format("parquet") \
      .option("compression", "snappy") \
      .saveAsTable(f"{table_name}_compact")

    # 策略3: 替换原分区（原子操作）
    spark.sql(f"""
        ALTER TABLE {table_name} DROP IF EXISTS PARTITION (dt = '{dt}')
    """)

    df_compacted = spark.table(f"{table_name}_compact")
    df_compacted.write \
        .mode("append") \
        .format("parquet") \
        .saveAsTable(table_name)

    print(f"[合并完成] 分区 {dt} 已合并为 {target_partitions} 个文件")
```

---

## 十三、用户画像查询接口设计

### 13.1 常用查询场景与SQL

```sql
-- ============================================================
-- 场景1: 查询单个用户的完整画像
-- ============================================================
SELECT *
FROM ads.user_profile
WHERE dt = '2024-03-31'
  AND user_id = 10086;

-- ============================================================
-- 场景2: 批量查询高价值用户（用于精准营销）
-- ============================================================
SELECT
    user_id, gender, age_group, city_level,
    value_segment,
    top3_categories,
    top3_brands,
    coupon_sensitivity,
    lifecycle_stage
FROM ads.user_profile
WHERE dt = '2024-03-31'
  AND value_segment IN ('顶级高价值', '高价值')
  AND is_churn_risk = 0
ORDER BY rfm_total DESC
LIMIT 10000;

-- ============================================================
-- 场景3: 查找流失风险用户（用于召回活动）
-- ============================================================
SELECT
    user_id, gender, age_group, city_level,
    lifecycle_stage, last_active_days,
    recency_days, value_segment,
    top3_categories
FROM ads.user_profile
WHERE dt = '2024-03-31'
  AND is_churn_risk = 1
  AND value_segment IN ('高价值', '顶级高价值')
ORDER BY recency_days DESC
LIMIT 5000;

-- ============================================================
-- 场景4: 按标签组合圈选用户群
-- ============================================================
SELECT
    user_id, gender, age_group, city_level,
    buy_frequency_level, avg_order_value_level,
    value_segment, top3_categories
FROM ads.user_profile
WHERE dt = '2024-03-31'
  AND city_level = '一线'
  AND age_group IN ('青年', '中青年')
  AND price_sensitivity = '低敏感'
  AND buy_frequency_level IN ('高频', '中频')
  AND lifecycle_stage IN ('活跃用户', '新用户')
ORDER BY rfm_total DESC;

-- ============================================================
-- 场景5: 画像标签覆盖率分析
-- ============================================================
WITH tag_stats AS (
    SELECT
        COUNT(DISTINCT user_id) AS total_users,
        COUNT(DISTINCT CASE WHEN gender IS NOT NULL THEN user_id END) AS gender_cov,
        COUNT(DISTINCT CASE WHEN age_group IS NOT NULL THEN user_id END) AS age_cov,
        COUNT(DISTINCT CASE WHEN city_level IS NOT NULL THEN user_id END) AS city_cov,
        COUNT(DISTINCT CASE WHEN top3_categories IS NOT NULL THEN user_id END) AS category_cov,
        COUNT(DISTINCT CASE WHEN price_sensitivity IS NOT NULL THEN user_id END) AS sensitivity_cov,
        COUNT(DISTINCT CASE WHEN value_segment IS NOT NULL THEN user_id END) AS rfm_cov,
        COUNT(DISTINCT CASE WHEN lifecycle_stage IS NOT NULL THEN user_id END) AS lifecycle_cov
    FROM ads.user_profile
    WHERE dt = '2024-03-31'
)
SELECT
    'gender'              AS tag_name, ROUND(gender_cov / total_users * 100, 2) AS coverage_pct FROM tag_stats
UNION ALL
SELECT 'age_group',        ROUND(age_cov / total_users * 100, 2) FROM tag_stats
UNION ALL
SELECT 'city_level',       ROUND(city_cov / total_users * 100, 2) FROM tag_stats
UNION ALL
SELECT 'top3_categories',  ROUND(category_cov / total_users * 100, 2) FROM tag_stats
UNION ALL
SELECT 'price_sensitivity',ROUND(sensitivity_cov / total_users * 100, 2) FROM tag_stats
UNION ALL
SELECT 'value_segment',    ROUND(rfm_cov / total_users * 100, 2) FROM tag_stats
UNION ALL
SELECT 'lifecycle_stage',  ROUND(lifecycle_cov / total_users * 100, 2) FROM tag_stats;

-- ============================================================
-- 场景6: RFM分层价值统计（用于BI报表）
-- ============================================================
SELECT
    value_segment,
    COUNT(DISTINCT user_id) AS user_count,
    ROUND(COUNT(DISTINCT user_id) * 100.0 /
        SUM(COUNT(DISTINCT user_id)) OVER (), 2) AS user_pct,
    ROUND(AVG(recency_days), 1) AS avg_recency,
    ROUND(AVG(frequency), 1) AS avg_frequency,
    ROUND(AVG(monetary), 2) AS avg_monetary,
    ROUND(SUM(monetary), 2) AS total_revenue,
    ROUND(SUM(monetary) * 100.0 /
        SUM(SUM(monetary)) OVER (), 2) AS revenue_pct
FROM ads.user_profile
WHERE dt = '2024-03-31'
GROUP BY value_segment
ORDER BY total_revenue DESC;

-- ============================================================
-- 场景7: 用户群体交叉分析
-- ============================================================
SELECT
    lifecycle_stage,
    value_segment,
    gender,
    age_group,
    COUNT(DISTINCT user_id) AS user_count,
    ROUND(AVG(monetary), 2) AS avg_spend
FROM ads.user_profile
WHERE dt = '2024-03-31'
GROUP BY lifecycle_stage, value_segment, gender, age_group
ORDER BY user_count DESC
LIMIT 100;

-- ============================================================
-- 场景8: 优惠券敏感用户定向投放
-- ============================================================
SELECT
    user_id,
    coupon_sensitivity,
    top3_categories,
    avg_order_value_level,
    monetary
FROM ads.user_profile
WHERE dt = '2024-03-31'
  AND coupon_sensitivity = '高敏感(优惠券驱动)'
  AND lifecycle_stage IN ('活跃用户', '沉默用户')
  AND is_churn_risk = 0
ORDER BY monetary DESC
LIMIT 20000;

-- ============================================================
-- 场景9: 新用户转化分析
-- ============================================================
SELECT
    age_group,
    city_level,
    COUNT(DISTINCT user_id) AS new_user_count,
    COUNT(DISTINCT CASE WHEN frequency > 0 THEN user_id END) AS converted_user_count,
    ROUND(COUNT(DISTINCT CASE WHEN frequency > 0 THEN user_id END)
        * 100.0 / COUNT(DISTINCT user_id), 2) AS conversion_rate_pct,
    ROUND(AVG(COALESCE(monetary, 0)), 2) AS avg_revenue_per_user
FROM ads.user_profile
WHERE dt = '2024-03-31'
  AND lifecycle_stage = '新用户'
GROUP BY age_group, city_level
ORDER BY new_user_count DESC;
```

---

## 十四、标签更新增量策略

### 14.1 增量更新架构设计

```
标签更新分为三种策略:
┌──────────────────────────────────────────────────────────────────┐
│  策略类型        │ 适用标签             │ 更新方式                │
├──────────────────────────────────────────────────────────────────┤
│ 全量覆盖         │ 所有统计类标签       │ 每日T+1全量重算          │
│ (推荐L1阶段使用) │ (RFM/品类偏好/活跃度)│ 直接OVERWRITE分区        │
├──────────────────────────────────────────────────────────────────┤
│ 增量更新         │ 基础属性标签          │ 只更新有变更的用户       │
│ (进阶方案)       │ (性别/年龄/会员等级)  │ MERGE到存量分区          │
├──────────────────────────────────────────────────────────────────┤
│ 实时更新         │ 实时行为标签         │ 流式更新到HBase/Redis    │
│ (L2阶段学习)     │ (最近访问/实时意图)   │ + 离线画像T+1对齐       │
└──────────────────────────────────────────────────────────────────┘
```

### 14.2 增量更新代码实现

```python
"""
incremental_tag_update.py — 用户画像增量更新策略实现
"""
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import *
from datetime import datetime, timedelta

spark = SparkSession.builder \
    .appName("IncrementalTagUpdate") \
    .enableHiveSupport() \
    .getOrCreate()


def get_base_profile(dt: str) -> DataFrame:
    """加载基础画像（昨天的最新画像）"""
    return spark.sql(f"""
        SELECT * FROM ads.user_profile
        WHERE dt = '{dt}'
    """)


def identify_changed_users(current_dt: str, prev_dt: str) -> DataFrame:
    """
    识别需要更新的用户

    需要更新的场景:
      1. 新注册用户 → INSERT
      2. 基础属性变更（改性别/改会员等级等）→ UPDATE
      3. 新增行为/订单 → UPDATE行为标签+RFM标签
      4. 进入新生命周期阶段 → UPDATE生命周期标签
    """
    # 新注册用户
    new_users = spark.sql(f"""
        SELECT user_id
        FROM dwd.dwd_user_register
        WHERE dt = '{current_dt}'
          AND register_date = '{current_dt}'
    """)

    # 基础属性变更（通过CDC/快照对比）
    changed_attributes = spark.sql(f"""
        SELECT
            a.user_id
        FROM dwd.dwd_user_register a
        LEFT JOIN dwd.dwd_user_register b
            ON a.user_id = b.user_id AND b.dt = '{prev_dt}'
        WHERE a.dt = '{current_dt}'
          AND (a.gender != b.gender
            OR a.age != b.age
            OR a.city != b.city
            OR a.user_level != b.user_level
            OR b.user_id IS NULL)
    """)

    # 行为/订单变更
    active_users = spark.sql(f"""
        SELECT DISTINCT user_id
        FROM dws.dws_user_action_day
        WHERE dt = '{current_dt}'
    """)

    # 合并所有变更用户
    changed_users = new_users \
        .union(changed_attributes) \
        .union(active_users) \
        .distinct()

    print(f"[增量识别] 需更新用户数: {changed_users.count()}")
    return changed_users


def incremental_update_pipeline(current_dt: str, prev_dt: str):
    """
    增量更新主流程

    步骤:
      1. 识别变更用户
      2. 对变更用户完整重算标签
      3. 读取昨日画像，替换变更用户的记录
      4. 写入当日分区
    """

    # Step 1: 识别变更用户
    changed_users = identify_changed_users(current_dt, prev_dt)

    # Step 2: 仅对变更用户重算标签（复用build_basic_tags等函数）
    # 注意：使用JOIN过滤只处理变更用户
    changed_users_df = spark.table("dwd.dwd_user_register") \
        .filter(col("dt") == current_dt) \
        .join(changed_users, "user_id", "inner")

    # Step 3: 加载昨日画像，排除变更用户
    yesterday_profile = spark.table("ads.user_profile") \
        .filter(col("dt") == prev_dt) \
        .join(changed_users.select("user_id"),
              "user_id", "left_anti")

    # Step 4: 合并（未变更 + 已重算的变更用户）
    final_profile = yesterday_profile.unionByName(changed_users_df)

    return final_profile


def merge_to_partition(final_profile: DataFrame, dt: str):
    """
    将更新后的画像写入当日分区

    使用MERGE语义（Hive ACID表支持）:
      - 有主键冲突 → UPDATE
      - 无主键冲突 → INSERT
    """

    # 对于普通Parquet表，使用INSERT OVERWRITE整个分区
    final_profile \
        .repartition(50) \
        .write \
        .mode("overwrite") \
        .format("parquet") \
        .option("compression", "snappy") \
        .insertInto("ads.user_profile")

    print(f"[增量写入] 画像已更新到分区 dt={dt}")


# ============================================================
# 全量 vs 增量策略对比
# ============================================================

def compare_full_vs_incremental():
    """
    对比全量更新和增量更新的资源消耗

    假设:
      - 总用户数: 1亿
      - 每日变更用户: 约5% (500万)
      - 全量计算耗时: 2小时
      - 增量计算耗时: 10分钟

    结论:
      L1阶段推荐全量更新（简单可靠）
      L2阶段可引入增量更新（性能和复杂度权衡）
    """

    print("""
    ╔════════════════════════════════════════════════════════╗
    ║           全量更新 vs 增量更新对比                      ║
    ╠═══════════════╦══════════════╦════════════════════════╣
    ║   维度         ║  全量更新    ║   增量更新              ║
    ╠═══════════════╬══════════════╬════════════════════════╣
    ║ 计算资源       ║ 高(全量扫描) ║ 低(仅处理变更)         ║
    ║ 实现复杂度     ║ 简单         ║ 中等                   ║
    ║ 数据一致性     ║ 强一致       ║ 需处理CDC/迟到数据     ║
    ║ 容错能力       ║ 强(失败重跑) ║ 弱(需断点续传)        ║
    ║ 回刷支持       ║ 容易         ║ 困难                   ║
    ║ 适用数据量     ║ <5000万用户  ║ >5000万用户           ║
    ╚═══════════════╩══════════════╩════════════════════════╝
    """)
```

### 14.3 延迟数据处理

```python
"""
late_arriving_data_handler.py — 延迟数据处理策略
处理场景: 某些用户行为数据晚于分析日到达
"""

def handle_late_data(spark, analysis_dt: str, late_dt: str):
    """
    处理延迟到达的数据

    场景1: 订单数据晚到1天
      方案: 回溯重算对应日期的RFM标签

    场景2: 行为日志晚到数小时
      方案: 拉长回溯窗口，T+1计算时自然覆盖

    场景3: 基础属性变更
      方案: 取最新快照即可，无需回溯
    """

    # 对于延迟订单数据，更新对应日期的RFM标签
    late_orders = spark.sql(f"""
        SELECT *
        FROM dwd.dwd_order_detail
        WHERE dt = '{analysis_dt}'
          AND order_date = '{late_dt}'
          AND order_status IN ('paid', 'completed')
    """)

    if late_orders.count() > 0:
        print(f"[延迟数据] 发现 {late_orders.count()} 条延迟订单，触发RFM回溯重算")
        # 重新计算对应日期的RFM并UPDATE画像表
        # ...

    # 绘制延迟数据趋势
    late_stats = spark.sql(f"""
        SELECT
            order_date,
            dt AS processing_date,
            DATEDIFF(dt, order_date) AS delay_days,
            COUNT(*) AS late_order_count
        FROM dwd.dwd_order_detail
        WHERE dt >= DATE_SUB('{analysis_dt}', 7)
          AND order_status IN ('paid', 'completed')
        GROUP BY order_date, dt
        HAVING DATEDIFF(dt, order_date) > 0
        ORDER BY order_date, processing_date
    """)

    print("延迟数据监控:")
    late_stats.show(20, truncate=False)
```

---

## 十五、20个典型用户画像展示

### 15.1 画像展示SQL

```sql
-- ============================================================
-- 用户画像样例展示：20个典型用户
-- ============================================================

-- 类型1: 顶级高价值用户（5个）
-- 特征: RFM≥14, 高客单价, 高频
SELECT '顶级高价值' AS profile_type, user_id, gender, age_group, city_level,
       user_level, register_days, top3_categories, price_sensitivity,
       buy_frequency_level, avg_order_value_level, top3_brands,
       recency_days, frequency, ROUND(monetary, 2) AS monetary,
       r_score, f_score, m_score, rfm_total, value_segment,
       lifecycle_stage, active_rate_7d, is_churn_risk
FROM ads.user_profile
WHERE dt = '2024-03-31' AND value_segment = '顶级高价值'
ORDER BY rfm_total DESC LIMIT 5;

-- 类型2: 普通但活跃的新用户（5个）
-- 特征: 注册7天内, 已有行为
SELECT '活跃新用户' AS profile_type, user_id, gender, age_group, city_level,
       user_level, register_days, top3_categories, price_sensitivity,
       buy_frequency_level, avg_order_value_level, top3_brands,
       recency_days, frequency, ROUND(monetary, 2) AS monetary,
       r_score, f_score, m_score, rfm_total, value_segment,
       lifecycle_stage, active_rate_7d, is_churn_risk
FROM ads.user_profile
WHERE dt = '2024-03-31' AND lifecycle_stage = '新用户'
  AND buy_frequency_level IN ('高频', '中频')
ORDER BY register_days ASC LIMIT 5;

-- 类型3: 流失风险用户（5个）
-- 特征: 预警标记=1, 但上周仍有购买
SELECT '流失风险(曾高价值)' AS profile_type, user_id, gender, age_group,
       city_level, user_level, register_days, top3_categories,
       price_sensitivity, buy_frequency_level, avg_order_value_level,
       top3_brands, recency_days, frequency, ROUND(monetary, 2) AS monetary,
       r_score, f_score, m_score, rfm_total, value_segment,
       lifecycle_stage, active_rate_7d, is_churn_risk
FROM ads.user_profile
WHERE dt = '2024-03-31' AND is_churn_risk = 1
  AND value_segment IN ('顶级高价值', '高价值')
ORDER BY recency_days DESC LIMIT 5;

-- 类型4: 中等价值沉默用户（5个）
-- 特征: 30天内有行为但7天内无行为, RFM中等
SELECT '中等价值沉默用户' AS profile_type, user_id, gender, age_group,
       city_level, user_level, register_days, top3_categories,
       price_sensitivity, buy_frequency_level, avg_order_value_level,
       top3_brands, recency_days, frequency, ROUND(monetary, 2) AS monetary,
       r_score, f_score, m_score, rfm_total, value_segment,
       lifecycle_stage, active_rate_7d, is_churn_risk
FROM ads.user_profile
WHERE dt = '2024-03-31' AND lifecycle_stage = '沉默用户'
  AND value_segment = '中等价值'
ORDER BY active_rate_30d ASC LIMIT 5;
```

### 15.2 画像展示脚本

```python
"""
展示20个典型用户的完整画像，格式化为可读输出
"""
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("ProfileDisplay") \
    .enableHiveSupport() \
    .getOrCreate()

# 定义画像展示类型
profile_queries = {
    "顶级高价值用户 (Top 5)": """
        WHERE dt = '2024-03-31' AND value_segment = '顶级高价值'
        ORDER BY rfm_total DESC
    """,
    "高频高客单价用户 (Top 5)": """
        WHERE dt = '2024-03-31'
          AND buy_frequency_level = '高频'
          AND avg_order_value_level IN ('高客单价', '中客单价')
        ORDER BY monetary DESC
    """,
    "活跃新用户 (Top 5)": """
        WHERE dt = '2024-03-31' AND lifecycle_stage = '新用户'
          AND buy_frequency_level IN ('高频', '中频')
        ORDER BY register_days ASC
    """,
    "流失预警高价值用户 (Top 5)": """
        WHERE dt = '2024-03-31' AND is_churn_risk = 1
          AND value_segment IN ('顶级高价值', '高价值')
        ORDER BY recency_days DESC
    """
}

for title, where_clause in profile_queries.items():
    print(f"\n{'=' * 80}")
    print(f"  【{title}】")
    print(f"{'=' * 80}")

    sql = f"""
        SELECT user_id, gender, age_group, city_level, user_level,
               register_days, lifecycle_stage,
               top3_categories, price_sensitivity,
               buy_frequency_level, avg_order_value_level,
               ROUND(monetary, 2) AS total_spend,
               r_score, f_score, m_score, rfm_total, value_segment,
               active_rate_7d, is_churn_risk
        FROM ads.user_profile
        {where_clause}
        LIMIT 5
    """

    users = spark.sql(sql).collect()

    for i, user in enumerate(users, 1):
        print(f"\n  --- 用户 #{i} (ID: {user.user_id}) ---")
        print(f"  基础属性: {user.gender} | {user.age_group} | "
              f"{user.city_level} | {user.user_level} | 注册{user.register_days}天")
        print(f"  生命周期: {user.lifecycle_stage} | "
              f"7天活跃率 {user.active_rate_7d} | 流失预警:{user.is_churn_risk}")
        print(f"  消费能力: RFM总分={user.rfm_total} "
              f"(R={user.r_score} F={user.f_score} M={user.m_score}) | "
              f"{user.value_segment} | 总消费:{user.total_spend}")
        print(f"  行为偏好: 品类TOP3={user.top3_categories}")
        print(f"  购买特征: {user.buy_frequency_level} | {user.avg_order_value_level} "
              f"| {user.price_sensitivity}")

spark.stop()
```

### 15.3 20个典型用户画像数据样例

```
╔══════════════════════════════════════════════════════════════════════╗
║                    20个典型用户画像样例                              ║
╠══════════════════════════════════════════════════════════════════════╣

╔═══ 顶级高价值用户 (5个) ═════════════════════════════════════════════╗

用户 #1 (ID: 10001)
  基础属性: 女 | 中青年 | 一线 | VIP | 注册1200天
  生命周期: 活跃用户 | 7天活跃率 0.86 | 流失预警:0
  消费能力: RFM总分=15 (R=5 F=5 M=5) | 顶级高价值 | 总消费:285600.50
  行为偏好: 品类TOP3=美妆个护,母婴用品,食品饮料
  购买特征: 高频 | 高客单价 | 低敏感
  运营建议: VIP专属客服，新品首发通知

用户 #2 (ID: 10002)
  基础属性: 男 | 青年 | 新一线 | 黄金 | 注册890天
  生命周期: 活跃用户 | 7天活跃率 1.0 | 流失预警:0
  消费能力: RFM总分=15 (R=5 F=5 M=5) | 顶级高价值 | 总消费:195200.00
  行为偏好: 品类TOP3=数码电子,运动户外,图书文娱
  购买特征: 高频 | 中客单价 | 中敏感
  运营建议: 数码新品预售+VX，品牌联名活动

用户 #3 (ID: 10003)
  基础属性: 女 | 中青年 | 一线 | VIP | 注册2100天
  生命周期: 活跃用户 | 7天活跃率 0.71 | 流失预警:0
  消费能力: RFM总分=14 (R=4 F=5 M=5) | 顶级高价值 | 总消费:423100.80
  行为偏好: 品类TOP3=服装鞋包,美妆个护,母婴用品
  购买特征: 高频 | 高客单价 | 低敏感
  运营建议: 时尚搭配顾问，线下VIP沙龙

用户 #4 (ID: 10004)
  基础属性: 男 | 中年 | 一线 | 黄金 | 注册1500天
  生命周期: 活跃用户 | 7天活跃率 0.57 | 流失预警:0
  消费能力: RFM总分=14 (R=5 F=4 M=5) | 顶级高价值 | 总消费:178500.30
  行为偏好: 品类TOP3=数码电子,家用电器,食品饮料
  购买特征: 高频 | 高客单价 | 低敏感
  运营建议: 大额消费分期方案，品牌年度答谢

用户 #5 (ID: 10005)
  基础属性: 女 | 青年 | 新一线 | VIP | 注册650天
  生命周期: 活跃用户 | 7天活跃率 1.0 | 流失预警:0
  消费能力: RFM总分=14 (R=5 F=5 M=4) | 顶级高价值 | 总消费:156800.00
  行为偏好: 品类TOP3=美妆个护,服装鞋包,家居日用
  购买特征: 高频 | 中客单价 | 中敏感
  运营建议: 美妆KOL合作种草，会员日专属折扣

╔═══ 活跃新用户 (5个) ═════════════════════════════════════════════════╗

用户 #6 (ID: 20001)
  基础属性: 女 | 青年 | 一线 | 普通 | 注册3天
  生命周期: 新用户 | 7天活跃率 1.0 | 流失预警:0
  消费能力: RFM总分=9 (R=5 F=2 M=2) | 中等价值 | 总消费:860.00
  行为偏好: 品类TOP3=服装鞋包,美妆个护,食品饮料
  购买特征: 中频 | 标准客单价 | 中敏感
  运营建议: 新人专享大礼包，引导完善个人偏好信息

用户 #7 (ID: 20002)
  基础属性: 男 | 中青年 | 新一线 | 普通 | 注册5天
  生命周期: 新用户 | 7天活跃率 0.86 | 流失预警:0
  消费能力: RFM总分=8 (R=5 F=1 M=2) | 中等价值 | 总消费:1520.00
  行为偏好: 品类TOP3=数码电子,运动户外,图书文娱
  购买特征: 中频 | 中客单价 | 低敏感
  运营建议: 数码品类新人券，推荐高性价比产品

用户 #8 (ID: 20003)
  基础属性: 女 | 青年 | 二线 | 白银 | 注册2天
  生命周期: 新用户 | 7天活跃率 1.0 | 流失预警:0
  消费能力: RFM总分=7 (R=5 F=1 M=1) | 低价值 | 总消费:280.00
  行为偏好: 品类TOP3=食品饮料,家居日用,母婴用品
  购买特征: 低频 | 低客单价 | 高敏感
  运营建议: 拼团/秒杀活动，引导首单转化

用户 #9 (ID: 20004)
  基础属性: 男 | 青年 | 一线 | 普通 | 注册6天
  生命周期: 新用户 | 7天活跃率 0.71 | 流失预警:0
  消费能力: RFM总分=6 (R=5 F=0 M=1) | 低价值 | 总消费:350.00
  行为偏好: 品类TOP3=图书文娱,数码电子,食品饮料
  购买特征: 低频 | 低客单价 | 中敏感
  运营建议: 内容社区引导（书评、数码评测），培养浏览习惯

用户 #10 (ID: 20005)
  基础属性: 女 | 中青年 | 新一线 | 普通 | 注册4天
  生命周期: 新用户 | 7天活跃率 0.86 | 流失预警:0
  消费能力: RFM总分=10 (R=5 F=3 M=2) | 中等价值 | 总消费:2450.00
  行为偏好: 品类TOP3=服装鞋包,美妆个护,家居日用
  购买特征: 高频 | 标准客单价 | 中敏感
  运营建议: 会员等级引导升级，推荐办卡福利

╔═══ 流失预警高价值用户 (5个) ═════════════════════════════════════════╗

用户 #11 (ID: 30001)
  基础属性: 女 | 中年 | 一线 | 黄金 | 注册1800天
  生命周期: 沉默用户 | 7天活跃率 0.0 | 流失预警:1
  消费能力: RFM总分=13 (R=3 F=5 M=5) | 高价值 | 总消费:125000.00
  行为偏好: 品类TOP3=服装鞋包,美妆个护,母婴用品
  购买特征: 高频 | 高客单价 | 低敏感
  运营建议: 定向Coupon召回（满减券），App Push + 短信双通道

用户 #12 (ID: 30002)
  基础属性: 男 | 中青年 | 一线 | VIP | 注册2100天
  生命周期: 沉默用户 | 7天活跃率 0.0 | 流失预警:1
  消费能力: RFM总分=12 (R=2 F=5 M=5) | 高价值 | 总消费:198000.00
  行为偏好: 品类TOP3=数码电子,家用电器,图书文娱
  购买特征: 高频 | 高客单价 | 低敏感
  运营建议: 专属客服1v1电话回访，大促提前预约

用户 #13 (ID: 30003)
  基础属性: 女 | 青年 | 新一线 | 黄金 | 注册950天
  生命周期: 沉默用户 | 7天活跃率 0.0 | 流失预警:1
  消费能力: RFM总分=12 (R=2 F=5 M=5) | 高价值 | 总消费:98000.50
  行为偏好: 品类TOP3=美妆个护,服装鞋包,食品饮料
  购买特征: 高频 | 中客单价 | 中敏感
  运营建议: 生日月专属礼遇，邀请参与产品体验官

用户 #14 (ID: 30004)
  基础属性: 男 | 中年 | 二线 | 白银 | 注册1200天
  生命周期: 沉默用户 | 7天活跃率 0.0 | 流失预警:1
  消费能力: RFM总分=11 (R=2 F=4 M=5) | 中等价值 | 总消费:75600.00
  行为偏好: 品类TOP3=家用电器,食品饮料,家居日用
  购买特征: 中频 | 高客单价 | 低敏感
  运营建议: 家电以旧换新活动触达，周期购推荐

用户 #15 (ID: 30005)
  基础属性: 女 | 中青年 | 一线 | 黄金 | 注册780天
  生命周期: 沉默用户 | 7天活跃率 0.0 | 流失预警:1
  消费能力: RFM总分=10 (R=2 F=4 M=4) | 中等价值 | 总消费:89000.00
  行为偏好: 品类TOP3=母婴用品,食品饮料,家居日用
  购买特征: 中频 | 标准客单价 | 中敏感
  运营建议: 亲子活动邀请，会员权益提醒

╔═══ 中等价值沉默用户 (5个) ═══════════════════════════════════════════╗

用户 #16 (ID: 40001)
  基础属性: 女 | 中青年 | 三线及以下 | 普通 | 注册450天
  生命周期: 沉默用户 | 7天活跃率 0.0 | 流失预警:1
  消费能力: RFM总分=10 (R=3 F=3 M=4) | 中等价值 | 总消费:12500.00
  行为偏好: 品类TOP3=服装鞋包,食品饮料,家居日用
  购买特征: 低频 | 标准客单价 | 高敏感
  运营建议: 下沉市场品类推荐，单品爆款推送

用户 #17 (ID: 40002)
  基础属性: 男 | 青年 | 新一线 | 普通 | 注册320天
  生命周期: 沉默用户 | 7天活跃率 0.0 | 流失预警:1
  消费能力: RFM总分=9 (R=3 F=3 M=3) | 中等价值 | 总消费:8500.00
  行为偏好: 品类TOP3=数码电子,运动户外,图书文娱
  购买特征: 低频 | 中客单价 | 中敏感
  运营建议: 兴趣圈层内容推送（运动社区），场景化推荐

用户 #18 (ID: 40003)
  基础属性: 女 | 青年 | 二线 | 普通 | 注册600天
  生命周期: 沉默用户 | 7天活跃率 0.0 | 流失预警:1
  消费能力: RFM总分=9 (R=2 F=3 M=4) | 中等价值 | 总消费:15200.00
  行为偏好: 品类TOP3=美妆个护,服装鞋包,食品饮料
  购买特征: 中频 | 标准客单价 | 中敏感
  运营建议: 美妆试用装免费领，邀请回App领券

用户 #19 (ID: 40004)
  基础属性: 男 | 中青年 | 一线 | 白银 | 注册980天
  生命周期: 沉默用户 | 7天活跃率 0.0 | 流失预警:1
  消费能力: RFM总分=8 (R=2 F=3 M=3) | 中等价值 | 总消费:28600.00
  行为偏好: 品类TOP3=家用电器,数码电子,家居日用
  购买特征: 低频 | 高客单价 | 低敏感
  运营建议: 大件消费品分期免息，以旧换新

用户 #20 (ID: 40005)
  基础属性: 女 | 中年 | 三线及以下 | 普通 | 注册1500天
  生命周期: 沉默用户 | 7天活跃率 0.0 | 流失预警:1
  消费能力: RFM总分=8 (R=2 F=2 M=4) | 中等价值 | 总消费:18500.00
  行为偏好: 品类TOP3=食品饮料,家居日用,服装鞋包
  购买特征: 低频 | 标准客单价 | 高敏感
  运营建议: 周期性消耗品推荐（如粮油、日用品），高性价比推品
```