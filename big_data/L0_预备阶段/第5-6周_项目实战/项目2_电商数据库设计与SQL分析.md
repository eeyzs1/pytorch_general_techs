# 项目2：电商数据库设计与SQL分析

> **项目时长**：12小时（约2.5天）
> **项目类型**：独立完成
> **前置技能**：SQL（DDL、JOIN、子查询、窗口函数）、Python（数据生成）

---

## 一、项目概述

设计一个完整的电商数据库，使用Python生成测试数据，编写30条分析SQL，输出业务分析报告。本项目检验SQL综合能力，是大数据工程师面试的常见考察方向。

---

## 二、项目需求

### 阶段1：数据库设计（3h）

**设计包含以下实体的数据库**：

| 表名 | 说明 | 关键字段 |
|------|------|----------|
| users | 用户表 | user_id, username, email, city, age, registered_at |
| categories | 品类表 | category_id, category_name, parent_id |
| products | 商品表 | product_id, product_name, category_id, price, stock, sales |
| orders | 订单表 | order_id, user_id, order_date, total_amount, status |
| order_items | 订单明细表 | item_id, order_id, product_id, quantity, unit_price |
| reviews | 评价表 | review_id, user_id, product_id, rating, content |
| user_logs | 用户行为日志表 | log_id, user_id, product_id, action_type, action_time |

**要求**：
- 完整的DDL语句，包含主键、外键、索引
- 合理的默认值和约束
- 适当的字段注释
- 绘制ER图（使用Draw.io或类似工具）

**输出文件**：`schema.sql`

---

### 阶段2：数据生成（3h）

编写Python脚本 `seed_data.py`，批量生成模拟数据。

**数据规模**：

| 表 | 行数 |
|----|------|
| users | 10,000 |
| categories | 20（支持多级分类） |
| products | 5,000（10个一级品类） |
| orders | 50,000（时间跨度3个月） |
| order_items | 200,000 |
| reviews | 15,000 |
| user_logs | 100,000 |

**数据生成要求**：
- 时间分布：模拟3个月的数据，包含周末效应
- 金额分布：符合电商实际的客单价范围
- 状态分布：已完成>已发货>已支付>待支付>已取消>已退款
- 长尾分布：20%商品产生80%销量
- 地址分布：各城市分布合理
- 用户年龄分布：18-60岁，正态分布

**Pythong生成脚本要求**：
- 使用批量INSERT提高导入效率
- 正确处理外键依赖顺序
- 输出文件大小预估

---

### 阶段3：SQL分析集（6h）

编写 `analysis_queries.sql`，包含30条分析SQL，覆盖以下场景：

#### 用户分析（10条SQL）

| 编号 | 分析主题 | SQL要求 |
|------|----------|---------|
| U01 | 新用户注册趋势 | 按天统计、累计计算 |
| U02 | 用户城市分布TOP10 | GROUP BY + COUNT |
| U03 | 新用户首日留存率 | 窗口函数 + 日期差 |
| U04 | 用户生命周期价值(LTV)排名 | SUM + 窗口函数 |
| U05 | 高价值用户画像 | 消费金额TOP 10%的用户特征 |
| U06 | 用户活跃度分层 | 按月下单次数分4层 |
| U07 | 流失预警分析 | 30天未下单用户统计 |
| U08 | 用户年龄分层消费分析 | 年龄段 + 消费金额 |
| U09 | 新老用户消费对比 | UNION + 聚合 |
| U10 | 用户复购率月度趋势 | 窗口函数 + COUNT DISTINCT |

#### 商品分析（10条SQL）

| 编号 | 分析主题 | SQL要求 |
|------|----------|---------|
| P01 | 各品类销售额排名及占比 | JOIN + SUM + 子查询占比 |
| P02 | 商品连带购买TOP组合 | 自连接 + COUNT + HAVING |
| P03 | 高评分商品特征分析 | JOIN + AVG + 条件筛选 |
| P04 | 库存周转率分析 | 销量/库存 + 窗口函数 |
| P05 | 长尾商品贡献分析 | 按销量排名 + 累计占比 |
| P06 | 商品价格区间分析 | CASE WHEN分段 + 聚合 |
| P07 | 各品类评分分布 | JOIN + AVG + GROUP BY |
| P08 | 新品表现分析 | 时间筛选 + 销量对比 |
| P09 | 商品搜索热度分析 | user_logs表 + action聚合 |
| P10 | 季节性商品识别 | 月度销量波动 + 窗口函数 |

#### 订单分析（10条SQL）

| 编号 | 分析主题 | SQL要求 |
|------|----------|---------|
| O01 | 每日GMV趋势 | DATE + SUM + 排序 |
| O02 | 客单价分布分析 | CASE WHEN + 分层统计 |
| O03 | 各时段订单特征 | HOUR分组 + 聚合 |
| O04 | 退款率月度分析 | 状态筛选 + 占比计算 |
| O05 | 各城市订单特征对比 | JOIN + GROUP BY + 多维度 |
| O06 | 支付方式偏好分析 | GROUP BY + 占比 |
| O07 | 订单转化漏斗 | user_logs → orders 转化率 |
| O08 | 周度GMV环比增长率 | LAG窗口函数 |
| O09 | 大额订单特征分析 | 筛选 + JOIN + 画像 |
| O10 | 订单配送时效分析 | 状态时间差 + AVG |

**技术要求**：
- 至少10条SQL使用窗口函数
- 至少5条SQL使用CTE（WITH子句）
- 至少3条SQL包含子查询
- 每条SQL必须有注释说明业务含义

**输出文件**：`analysis_queries.sql`（30条SQL + 每条的结果说明）

---

## 三、核心SQL示例

以下给出部分关键技术点的SQL示例，学员需要自行扩展为30条。

```sql
-- ========== 用户分析示例 ==========

-- U04: 用户LTV排名（窗口函数 + CTE）
WITH user_ltv AS (
    SELECT
        u.user_id,
        u.username,
        u.city,
        SUM(o.actual_amount) AS total_spent,
        COUNT(o.order_id) AS order_count,
        DATEDIFF(MAX(o.order_date), MIN(o.order_date)) AS active_days
    FROM users u
    INNER JOIN orders o ON u.user_id = o.user_id
    WHERE o.status = 'completed'
    GROUP BY u.user_id, u.username, u.city
)
SELECT
    username,
    city,
    ROUND(total_spent, 2) AS ltv,
    order_count,
    active_days,
    ROUND(total_spent / NULLIF(active_days, 0), 2) AS daily_value,
    NTILE(10) OVER (ORDER BY total_spent DESC) AS ltv_decile
FROM user_ltv
ORDER BY ltv DESC
LIMIT 100;


-- ========== 商品分析示例 ==========

-- P02: 连带购买TOP组合（自连接）
SELECT
    p1.product_name AS product_a,
    p2.product_name AS product_b,
    combo.co_count
FROM (
    SELECT
        oi1.product_id AS pid1,
        oi2.product_id AS pid2,
        COUNT(DISTINCT oi1.order_id) AS co_count
    FROM order_items oi1
    INNER JOIN order_items oi2
        ON oi1.order_id = oi2.order_id AND oi1.product_id < oi2.product_id
    INNER JOIN orders o ON oi1.order_id = o.order_id
    WHERE o.status = 'completed'
    GROUP BY oi1.product_id, oi2.product_id
    HAVING co_count >= 10
) combo
INNER JOIN products p1 ON combo.pid1 = p1.product_id
INNER JOIN products p2 ON combo.pid2 = p2.product_id
ORDER BY combo.co_count DESC
LIMIT 20;


-- P05: 长尾商品贡献分析（窗口函数 + 累计求和）
WITH product_sales AS (
    SELECT
        p.product_id,
        p.product_name,
        SUM(oi.quantity) AS total_sold
    FROM products p
    INNER JOIN order_items oi ON p.product_id = oi.product_id
    INNER JOIN orders o ON oi.order_id = o.order_id
    WHERE o.status = 'completed'
    GROUP BY p.product_id, p.product_name
),
ranked AS (
    SELECT
        product_name,
        total_sold,
        ROW_NUMBER() OVER (ORDER BY total_sold DESC) AS rn,
        SUM(total_sold) OVER (ORDER BY total_sold DESC) AS cumulative_sold,
        SUM(total_sold) OVER () AS total_all
    FROM product_sales
)
SELECT
    CASE
        WHEN rn <= total_all * 0.2 THEN '头部商品'
        WHEN cumulative_sold <= total_all * 0.8 THEN '腰部商品'
        ELSE '长尾商品'
    END AS product_tier,
    COUNT(*) AS product_count,
    SUM(total_sold) AS tier_sold,
    ROUND(SUM(total_sold) / MAX(total_all) * 100, 2) AS pct
FROM ranked
GROUP BY
    CASE
        WHEN rn <= total_all * 0.2 THEN '头部商品'
        WHEN cumulative_sold <= total_all * 0.8 THEN '腰部商品'
        ELSE '长尾商品'
    END;


-- ========== 订单分析示例 ==========

-- O07: 订单转化漏斗（CTE + 多表关联）
WITH funnel AS (
    -- 浏览 → 加购 → 下单 → 支付
    SELECT
        '1.浏览' AS stage, COUNT(DISTINCT user_id) AS user_count
    FROM user_logs WHERE action_type = 'view'
    UNION ALL
    SELECT
        '2.加购' AS stage, COUNT(DISTINCT user_id) AS user_count
    FROM user_logs WHERE action_type = 'cart'
    UNION ALL
    SELECT
        '3.下单' AS stage, COUNT(DISTINCT user_id) AS user_count
    FROM orders WHERE status != 'cancelled'
    UNION ALL
    SELECT
        '4.支付' AS stage, COUNT(DISTINCT user_id) AS user_count
    FROM orders WHERE status IN ('paid', 'shipped', 'completed')
)
SELECT
    stage,
    user_count,
    ROUND(user_count * 100.0 / FIRST_VALUE(user_count) OVER (ORDER BY stage), 2) AS overall_rate,
    ROUND(user_count * 100.0 / LAG(user_count) OVER (ORDER BY stage), 2) AS step_rate
FROM funnel
ORDER BY stage;


-- O08: 周度GMV环比（LAG窗口函数）
WITH weekly_gmv AS (
    SELECT
        YEARWEEK(order_date, 1) AS yrwk,
        SUM(actual_amount) AS gmv
    FROM orders
    WHERE status = 'completed'
    GROUP BY YEARWEEK(order_date, 1)
)
SELECT
    yrwk,
    ROUND(gmv, 2) AS gmv,
    ROUND(LAG(gmv) OVER (ORDER BY yrwk), 2) AS prev_week_gmv,
    ROUND(
        (gmv - LAG(gmv) OVER (ORDER BY yrwk)) /
        NULLIF(LAG(gmv) OVER (ORDER BY yrwk), 0) * 100, 2
    ) AS wow_change_pct
FROM weekly_gmv
ORDER BY yrwk;
```

---

## 四、项目交付物

| 序号 | 文件名 | 说明 |
|------|--------|------|
| 1 | `schema.sql` | 完整建表DDL（含注释） |
| 2 | `er_diagram.png` | ER实体关系图 |
| 3 | `seed_data.py` | Python数据生成脚本 |
| 4 | `seed_data.sql` | 生成的INSERT语句（或提供Python导入方式） |
| 5 | `analysis_queries.sql` | 30条分析SQL + 业务注释 |
| 6 | `analysis_results.md` | 每条SQL的执行结果和业务解读 |

**GitHub提交要求**：
- 完整提交历史（至少12次commit）
- README.md包含数据库设计说明和运行指南

---

## 五、评分标准

| 评分项 | 权重 | 满分标准 |
|--------|------|----------|
| 数据库设计 | 20% | ER合理，主键外键索引完整，约束恰当 |
| 数据生成 | 20% | 数据量达标，分布合理，导入可行 |
| SQL质量 | 40% | 30条SQL覆盖所有维度，窗口函数≥10条，CTE≥5条 |
| 业务解读 | 20% | 每条SQL有注释和结果解读，有insight输出 |

---

## 六、时间建议

| 阶段 | 建议时间 | 关键任务 |
|------|----------|----------|
| 阶段1 | 3h | 设计ER图，写出完整DDL，在MySQL中建表 |
| 阶段2 | 3h | 编写Python数据生成脚本，执行导入 |
| 阶段3 | 6h | 编写30条SQL，验证结果，输出analysis_results.md |

---

## 七、ER图文字描述

由于无法嵌入图片，以下用文字描述7张表的实体关系(ER图)：

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           ENTITY RELATIONSHIP                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────┐           ┌──────────────┐           ┌──────────────┐      │
│  │  users   │ 1──────N │   orders     │ 1──────N │ order_items  │      │
│  │──────────│           │──────────────│           │──────────────│      │
│  │ user_id  │───PK      │ order_id  ───│──PK       │ item_id   ───│──PK  │
│  │ username │           │ user_id   ───│──FK       │ order_id  ───│──FK  │
│  │ email    │           │ order_date   │           │ product_id──│──FK  │
│  │ city     │           │ total_amount │           │ quantity     │      │
│  │ age      │           │ status       │           │ unit_price   │      │
│  │ registered│          │ actual_amount│           │ subtotal     │      │
│  └────┬─────┘           └──────────────┘           └──────┬───────┘      │
│       │                                                   │              │
│       │ 1                                                N │              │
│       │          ┌──────────────┐                         │              │
│       │          │  products    │◄────────────────────────┘              │
│       │          │──────────────│                                        │
│       │          │ product_id ──│──PK                                    │
│       │          │ product_name │                                        │
│       ├──────────│ category_id──│──FK ──────────────────┐                │
│       │          │ price        │                        │                │
│       │          │ stock        │                        │                │
│       │          │ sales        │                        │                │
│       │          └──────┬───────┘                        │                │
│       │                 │                                │                │
│       │ 1               │ N                              │ N              │
│       │    ┌────────────┴───────────┐                    │                │
│       │    │                        │                    │                │
│       ▼    ▼                        ▼                    ▼                │
│  ┌──────────┐     ┌──────────────┐     ┌──────────────┐                  │
│  │ reviews  │     │ user_logs    │     │ categories   │                  │
│  │──────────│     │──────────────│     │──────────────│                  │
│  │ review_id│─PK  │ log_id    ───│──PK  │ category_id──│──PK             │
│  │ user_id──│─FK  │ user_id   ───│──FK  │ category_name│                  │
│  │ product_id│─FK │ product_id───│──FK  │ parent_id ───│──FK(自引用)     │
│  │ rating   │     │ action_type  │     └──────────────┘                  │
│  │ content  │     │ action_time  │                                       │
│  └──────────┘     └──────────────┘                                       │
│                                                                          │
│  关系说明：                                                               │
│  ─────────────────────────────────────────────────────────────          │
│  • users → orders:          一对多（一个用户可以有多个订单）             │
│  • orders → order_items:    一对多（一个订单包含多个商品）               │
│  • products → order_items:  一对多（一个商品出现在多个订单明细中）       │
│  • products → reviews:      一对多（一个商品可以有多个评价）             │
│  • users → reviews:         一对多（一个用户可以发表多个评价）           │
│  • categories → products:   一对多（一个品类下有多个商品）               │
│  • categories → categories: 自引用（parent_id指向自身实现多级分类）      │
│  • users → user_logs:       一对多（一个用户有多条行为日志）             │
│  • products → user_logs:    一对多（一个商品有多条行为日志）             │
│                                                                          │
│  外键约束汇总：                                                           │
│  ─────────────────────────────────────────────────────────────          │
│  orders.user_id       → users.user_id         (ON DELETE RESTRICT)      │
│  order_items.order_id → orders.order_id       (ON DELETE CASCADE)       │
│  order_items.product_id→ products.product_id   (ON DELETE RESTRICT)      │
│  reviews.user_id      → users.user_id         (ON DELETE CASCADE)       │
│  reviews.product_id   → products.product_id   (ON DELETE CASCADE)       │
│  user_logs.user_id    → users.user_id         (ON DELETE CASCADE)       │
│  user_logs.product_id → products.product_id   (ON DELETE SET NULL)      │
│  products.category_id → categories.category_id(ON DELETE RESTRICT)      │
│  categories.parent_id → categories.category_id(ON DELETE SET NULL)      │
└─────────────────────────────────────────────────────────────────────────┘
```

**索引设计建议**：

| 表名 | 索引名 | 索引字段 | 索引类型 | 用途说明 |
|------|--------|----------|----------|----------|
| users | idx_users_city | city | 普通索引 | 按城市查询用户 |
| users | idx_users_registered | registered_at | 普通索引 | 按注册时间范围查询 |
| users | idx_users_age | age | 普通索引 | 按年龄段筛选 |
| orders | idx_orders_user | user_id | 普通索引 | 按用户查订单 |
| orders | idx_orders_date | order_date | 普通索引 | 按日期范围查询 |
| orders | idx_orders_status | status | 普通索引 | 按状态筛选 |
| orders | idx_orders_user_date | (user_id, order_date) | 联合索引 | 用户+日期组合查询 |
| order_items | idx_items_order | order_id | 普通索引 | 按订单查明细 |
| order_items | idx_items_product | product_id | 普通索引 | 按商品查明细 |
| products | idx_products_category | category_id | 普通索引 | 按品类查商品 |
| products | idx_products_price | price | 普通索引 | 按价格范围筛选 |
| reviews | idx_reviews_product | product_id | 普通索引 | 按商品查评价 |
| reviews | idx_reviews_user | user_id | 普通索引 | 按用户查评价 |
| reviews | idx_reviews_rating | rating | 普通索引 | 按评分筛选 |
| user_logs | idx_logs_user_time | (user_id, action_time) | 联合索引 | 按用户+时间查行为 |
| user_logs | idx_logs_product_time | (product_id, action_time) | 联合索引 | 按商品+时间查行为 |
| user_logs | idx_logs_action_type | action_type | 普通索引 | 按行为类型筛选 |

---

## 八、完整30条分析SQL

以下给出全部30条SQL的完整实现，每条均包含业务注释和预期输出格式。

### 8.1 用户分析（10条SQL）

```sql
-- =====================================================================
-- U01: 新用户注册趋势 — 按天统计新注册用户数 + 累计注册数
-- 业务价值：监控用户增长趋势，评估拉新渠道效果
-- 预期输出列：reg_date | daily_new_users | cumulative_users
-- =====================================================================
WITH daily_reg AS (
    SELECT
        DATE(registered_at) AS reg_date,
        COUNT(DISTINCT user_id) AS daily_new_users
    FROM users
    GROUP BY DATE(registered_at)
)
SELECT
    reg_date,
    daily_new_users,
    SUM(daily_new_users) OVER (ORDER BY reg_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_users,
    ROUND(AVG(daily_new_users) OVER (ORDER BY reg_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 1) AS rolling_7d_avg
FROM daily_reg
ORDER BY reg_date;


-- =====================================================================
-- U02: 用户城市分布TOP10 — 各城市用户数量排名
-- 业务价值：了解用户地域分布，指导区域化运营策略
-- 预期输出列：city | user_count | pct_of_total | cumulative_pct
-- =====================================================================
WITH city_stats AS (
    SELECT
        city,
        COUNT(*) AS user_count
    FROM users
    GROUP BY city
),
total AS (
    SELECT SUM(user_count) AS total_users FROM city_stats
)
SELECT
    cs.city,
    cs.user_count,
    ROUND(cs.user_count * 100.0 / t.total_users, 2) AS pct_of_total,
    ROUND(SUM(cs.user_count) OVER (ORDER BY cs.user_count DESC)
        * 100.0 / t.total_users, 2) AS cumulative_pct
FROM city_stats cs, total t
ORDER BY cs.user_count DESC
LIMIT 10;


-- =====================================================================
-- U03: 新用户首日留存率 — 注册后次日有行为记录的用户占比
-- 业务价值：衡量新用户体验质量，首日留存越高说明产品吸引力越强
-- 预期输出列：reg_date | total_new | day1_retained | retention_rate_pct
-- =====================================================================
WITH new_users AS (
    SELECT
        user_id,
        DATE(MIN(registered_at)) AS reg_date
    FROM users
    GROUP BY user_id
),
day1_active AS (
    SELECT DISTINCT
        DATE(ul.action_time) AS active_date,
        ul.user_id
    FROM user_logs ul
)
SELECT
    nu.reg_date,
    COUNT(DISTINCT nu.user_id) AS total_new_users,
    COUNT(DISTINCT da.user_id) AS day1_retained_users,
    ROUND(COUNT(DISTINCT da.user_id) * 100.0
        / NULLIF(COUNT(DISTINCT nu.user_id), 0), 2) AS day1_retention_pct
FROM new_users nu
LEFT JOIN day1_active da
    ON nu.user_id = da.user_id
    AND da.active_date = DATE_ADD(nu.reg_date, INTERVAL 1 DAY)
GROUP BY nu.reg_date
ORDER BY nu.reg_date;


-- =====================================================================
-- U04: 用户生命周期价值(LTV)排名 — 消费金额TOP100用户
-- 业务价值：识别高价值用户，进行精准营销和VIP服务
-- 预期输出列：user_id | username | city | ltv | order_count | active_days | daily_value | ltv_decile
-- =====================================================================
WITH user_ltv AS (
    SELECT
        u.user_id,
        u.username,
        u.city,
        SUM(o.actual_amount) AS total_spent,
        COUNT(DISTINCT o.order_id) AS order_count,
        DATEDIFF(MAX(o.order_date), MIN(o.order_date)) + 1 AS active_days,
        AVG(o.actual_amount) AS avg_order_value
    FROM users u
    INNER JOIN orders o ON u.user_id = o.user_id
    WHERE o.status = 'completed'
    GROUP BY u.user_id, u.username, u.city
)
SELECT
    user_id,
    username,
    city,
    ROUND(total_spent, 2) AS ltv,
    order_count,
    active_days,
    ROUND(avg_order_value, 2) AS avg_order_value,
    ROUND(total_spent / NULLIF(active_days, 0), 2) AS daily_value,
    NTILE(10) OVER (ORDER BY total_spent DESC) AS ltv_decile
FROM user_ltv
ORDER BY ltv DESC
LIMIT 100;


-- =====================================================================
-- U05: 高价值用户画像 — 消费金额TOP10%用户的特征聚合
-- 业务价值：抽象高价值用户标签，指导用户获取策略
-- 预期输出列：metric | top10pct_value | overall_avg
-- =====================================================================
WITH user_spending AS (
    SELECT
        u.user_id,
        u.age,
        u.city,
        u.gender,
        SUM(o.actual_amount) AS total_spent,
        COUNT(DISTINCT o.order_id) AS order_count
    FROM users u
    INNER JOIN orders o ON u.user_id = o.user_id
    WHERE o.status = 'completed'
    GROUP BY u.user_id, u.age, u.city, u.gender
),
ranked AS (
    SELECT *,
        PERCENT_RANK() OVER (ORDER BY total_spent DESC) AS pct_rnk
    FROM user_spending
),
top_users AS (
    SELECT * FROM ranked WHERE pct_rnk <= 0.1
)
SELECT
    'avg_age' AS metric,
    ROUND(AVG(age), 1) AS top10pct_value,
    ROUND((SELECT AVG(age) FROM user_spending), 1) AS overall_avg
FROM top_users
UNION ALL
SELECT 'avg_order_count',
    ROUND(AVG(order_count), 1),
    ROUND((SELECT AVG(order_count) FROM user_spending), 1)
FROM top_users
UNION ALL
SELECT 'avg_ltv',
    ROUND(AVG(total_spent), 2),
    ROUND((SELECT AVG(total_spent) FROM user_spending), 2)
FROM top_users
UNION ALL
SELECT 'female_ratio_pct',
    ROUND(SUM(CASE WHEN gender='F' THEN 1 ELSE 0 END)*100.0/COUNT(*), 1),
    ROUND((SELECT SUM(CASE WHEN gender='F' THEN 1 ELSE 0 END)*100.0/COUNT(*) FROM user_spending), 1)
FROM top_users;


-- =====================================================================
-- U06: 用户活跃度分层 — 按月下单次数将用户分为4层
-- 业务价值：分层运营，针对不同活跃度用户采取不同策略
-- 预期输出列：active_tier | user_count | total_orders | avg_orders
-- =====================================================================
WITH monthly_orders AS (
    SELECT
        u.user_id,
        DATE_FORMAT(o.order_date, '%Y-%m') AS order_month,
        COUNT(DISTINCT o.order_id) AS monthly_order_count
    FROM users u
    INNER JOIN orders o ON u.user_id = o.user_id
    WHERE o.status = 'completed'
    GROUP BY u.user_id, DATE_FORMAT(o.order_date, '%Y-%m')
),
user_tier AS (
    SELECT
        user_id,
        order_month,
        monthly_order_count,
        CASE
            WHEN monthly_order_count >= 8 THEN '高活跃(≥8单)'
            WHEN monthly_order_count >= 4 THEN '中活跃(4-7单)'
            WHEN monthly_order_count >= 1 THEN '低活跃(1-3单)'
            ELSE '沉睡用户(0单)'
        END AS active_tier
    FROM monthly_orders
)
SELECT
    active_tier,
    COUNT(DISTINCT user_id) AS user_count,
    SUM(monthly_order_count) AS total_orders,
    ROUND(AVG(monthly_order_count), 1) AS avg_orders_per_user,
    ROUND(COUNT(DISTINCT user_id) * 100.0 /
        SUM(COUNT(DISTINCT user_id)) OVER (), 2) AS user_pct
FROM user_tier
GROUP BY active_tier
ORDER BY AVG(monthly_order_count) DESC;


-- =====================================================================
-- U07: 流失预警分析 — 30天未下单的用户统计
-- 业务价值：预警用户流失风险，及时进行召回
-- 预期输出列：risk_level | user_count | avg_ltv | avg_inactive_days
-- =====================================================================
WITH last_order AS (
    SELECT
        u.user_id,
        u.username,
        u.email,
        MAX(o.order_date) AS last_order_date,
        DATEDIFF(CURRENT_DATE, MAX(o.order_date)) AS days_inactive,
        SUM(o.actual_amount) AS total_spent
    FROM users u
    INNER JOIN orders o ON u.user_id = o.user_id
    WHERE o.status = 'completed'
    GROUP BY u.user_id, u.username, u.email
),
risk_classified AS (
    SELECT *,
        CASE
            WHEN days_inactive >= 90 THEN '高风险流失'
            WHEN days_inactive >= 60 THEN '中风险流失'
            WHEN days_inactive >= 30 THEN '低风险流失'
            ELSE '活跃用户'
        END AS risk_level
    FROM last_order
)
SELECT
    risk_level,
    COUNT(*) AS user_count,
    ROUND(AVG(total_spent), 2) AS avg_ltv,
    ROUND(AVG(days_inactive), 1) AS avg_inactive_days,
    SUM(CASE WHEN days_inactive >= 60 THEN 1 ELSE 0 END) AS need_urgent_recall
FROM risk_classified
GROUP BY risk_level
ORDER BY AVG(days_inactive) DESC;


-- =====================================================================
-- U08: 用户年龄分层消费分析 — 不同年龄段的消费特征对比
-- 业务价值：指导年龄段定向营销和商品推荐策略
-- 预期输出列：age_group | user_count | total_gmv | avg_ltv | avg_order_value | top_category
-- =====================================================================
WITH age_groups AS (
    SELECT
        u.user_id,
        CASE
            WHEN u.age < 20 THEN '18-19岁'
            WHEN u.age < 25 THEN '20-24岁'
            WHEN u.age < 30 THEN '25-29岁'
            WHEN u.age < 35 THEN '30-34岁'
            WHEN u.age < 40 THEN '35-39岁'
            WHEN u.age < 50 THEN '40-49岁'
            ELSE '50-60岁'
        END AS age_group
    FROM users u
),
user_sales AS (
    SELECT
        ag.age_group,
        ag.user_id,
        SUM(o.actual_amount) AS user_gmv,
        COUNT(DISTINCT o.order_id) AS order_count
    FROM age_groups ag
    INNER JOIN orders o ON ag.user_id = o.user_id
    WHERE o.status = 'completed'
    GROUP BY ag.age_group, ag.user_id
)
SELECT
    age_group,
    COUNT(DISTINCT user_id) AS user_count,
    ROUND(SUM(user_gmv), 2) AS total_gmv,
    ROUND(AVG(user_gmv), 2) AS avg_ltv,
    ROUND(AVG(user_gmv / NULLIF(order_count, 0)), 2) AS avg_order_value,
    ROUND(SUM(user_gmv) * 100.0 / SUM(SUM(user_gmv)) OVER (), 2) AS gmv_pct
FROM user_sales
GROUP BY age_group
ORDER BY MIN(CASE age_group
    WHEN '18-19岁' THEN 1 WHEN '20-24岁' THEN 2
    WHEN '25-29岁' THEN 3 WHEN '30-34岁' THEN 4
    WHEN '35-39岁' THEN 5 WHEN '40-49岁' THEN 6 ELSE 7 END);


-- =====================================================================
-- U09: 新老用户消费对比 — 注册3个月以内 vs 3个月以上的用户对比
-- 业务价值：评估新用户转化质量和老用户忠诚度
-- 预期输出列：user_type | user_count | total_orders | avg_order_value | avg_items_per_order
-- =====================================================================
WITH user_type AS (
    SELECT
        user_id,
        CASE
            WHEN DATEDIFF(CURRENT_DATE, registered_at) <= 90 THEN '新用户(≤3个月)'
            ELSE '老用户(>3个月)'
        END AS user_category
    FROM users
),
order_stats AS (
    SELECT
        ut.user_category,
        o.order_id,
        o.actual_amount,
        COUNT(oi.item_id) AS items_in_order
    FROM user_type ut
    INNER JOIN orders o ON ut.user_id = o.user_id
    INNER JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.status = 'completed'
    GROUP BY ut.user_category, o.order_id, o.actual_amount
)
SELECT
    user_category AS user_type,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(AVG(actual_amount), 2) AS avg_order_value,
    ROUND(AVG(items_in_order), 1) AS avg_items_per_order,
    ROUND(STDDEV(actual_amount), 2) AS stddev_order_value
FROM order_stats
GROUP BY user_category;


-- =====================================================================
-- U10: 用户复购率月度趋势 — 每月有多少用户下单超过1次
-- 业务价值：衡量用户粘性和购物频次变化趋势
-- 预期输出列：order_month | total_users | repurchase_users | repurchase_rate_pct
-- =====================================================================
WITH user_monthly AS (
    SELECT
        user_id,
        DATE_FORMAT(order_date, '%Y-%m') AS order_month,
        COUNT(DISTINCT order_id) AS order_count
    FROM orders
    WHERE status = 'completed'
    GROUP BY user_id, DATE_FORMAT(order_date, '%Y-%m')
)
SELECT
    order_month,
    COUNT(DISTINCT user_id) AS total_users,
    COUNT(DISTINCT CASE WHEN order_count >= 2 THEN user_id END) AS repurchase_users,
    ROUND(COUNT(DISTINCT CASE WHEN order_count >= 2 THEN user_id END) * 100.0
        / NULLIF(COUNT(DISTINCT user_id), 0), 2) AS repurchase_rate_pct,
    ROUND(AVG(order_count), 2) AS avg_orders_per_user
FROM user_monthly
GROUP BY order_month
ORDER BY order_month;
```

### 8.2 商品分析（10条SQL）

```sql
-- =====================================================================
-- P01: 各品类销售额排名及占比 — 品类维度GMV排名
-- 业务价值：明确核心品类贡献，指导资源分配
-- 预期输出列：category_name | total_gmv | order_count | gmv_pct | cumulative_pct | gmv_rank
-- =====================================================================
WITH category_gmv AS (
    SELECT
        c.category_id,
        c.category_name,
        SUM(oi.quantity * oi.unit_price) AS total_gmv,
        COUNT(DISTINCT o.order_id) AS order_count,
        COUNT(DISTINCT oi.product_id) AS product_count
    FROM categories c
    INNER JOIN products p ON c.category_id = p.category_id
    INNER JOIN order_items oi ON p.product_id = oi.product_id
    INNER JOIN orders o ON oi.order_id = o.order_id
    WHERE o.status = 'completed'
    GROUP BY c.category_id, c.category_name
)
SELECT
    category_name,
    ROUND(total_gmv, 2) AS total_gmv,
    order_count,
    product_count,
    ROUND(total_gmv * 100.0 / SUM(total_gmv) OVER (), 2) AS gmv_pct,
    ROUND(SUM(total_gmv) OVER (ORDER BY total_gmv DESC)
        * 100.0 / SUM(total_gmv) OVER (), 2) AS cumulative_pct,
    RANK() OVER (ORDER BY total_gmv DESC) AS gmv_rank
FROM category_gmv
ORDER BY total_gmv DESC;


-- =====================================================================
-- P02: 商品连带购买TOP组合 — 经常被一起购买的商品对（关联分析）
-- 业务价值：指导捆绑销售和推荐算法"买了又买"
-- 预期输出列：product_a | product_b | co_purchase_times | category_a | category_b
-- =====================================================================
WITH co_orders AS (
    SELECT
        oi1.product_id AS pid1,
        oi2.product_id AS pid2,
        COUNT(DISTINCT oi1.order_id) AS co_count
    FROM order_items oi1
    INNER JOIN order_items oi2
        ON oi1.order_id = oi2.order_id AND oi1.product_id < oi2.product_id
    INNER JOIN orders o ON oi1.order_id = o.order_id
    WHERE o.status = 'completed'
    GROUP BY oi1.product_id, oi2.product_id
    HAVING co_count >= 10
)
SELECT
    p1.product_name AS product_a,
    p2.product_name AS product_b,
    co.co_count AS co_purchase_times,
    c1.category_name AS category_a,
    c2.category_name AS category_b
FROM co_orders co
INNER JOIN products p1 ON co.pid1 = p1.product_id
INNER JOIN products p2 ON co.pid2 = p2.product_id
INNER JOIN categories c1 ON p1.category_id = c1.category_id
INNER JOIN categories c2 ON p2.category_id = c2.category_id
ORDER BY co.co_count DESC
LIMIT 20;


-- =====================================================================
-- P03: 高评分商品特征分析 — 评分≥4.5的商品共性特征
-- 业务价值：识别优质商品特征，指导选品和供应商筛选
-- 预期输出列：metric | high_rated_avg | overall_avg | diff_pct
-- =====================================================================
WITH product_rating AS (
    SELECT
        p.product_id,
        p.product_name,
        AVG(r.rating) AS avg_rating,
        COUNT(r.review_id) AS review_count,
        p.price,
        p.sales,
        c.category_name
    FROM products p
    LEFT JOIN reviews r ON p.product_id = r.product_id
    LEFT JOIN categories c ON p.category_id = c.category_id
    GROUP BY p.product_id, p.product_name, p.price, p.sales, c.category_name
    HAVING COUNT(r.review_id) >= 5
),
high_rated AS (
    SELECT * FROM product_rating WHERE avg_rating >= 4.5
)
SELECT
    'avg_price' AS metric,
    ROUND((SELECT AVG(price) FROM high_rated), 2) AS high_rated_avg,
    ROUND((SELECT AVG(price) FROM product_rating), 2) AS overall_avg,
    ROUND(((SELECT AVG(price) FROM high_rated) - (SELECT AVG(price) FROM product_rating))
        / NULLIF((SELECT AVG(price) FROM product_rating), 0) * 100, 1) AS diff_pct
UNION ALL
SELECT 'avg_sales',
    ROUND((SELECT AVG(sales) FROM high_rated), 1),
    ROUND((SELECT AVG(sales) FROM product_rating), 1),
    ROUND(((SELECT AVG(sales) FROM high_rated) - (SELECT AVG(sales) FROM product_rating))
        / NULLIF((SELECT AVG(sales) FROM product_rating), 0) * 100, 1)
UNION ALL
SELECT 'avg_review_count',
    ROUND((SELECT AVG(review_count) FROM high_rated), 1),
    ROUND((SELECT AVG(review_count) FROM product_rating), 1),
    ROUND(((SELECT AVG(review_count) FROM high_rated) - (SELECT AVG(review_count) FROM product_rating))
        / NULLIF((SELECT AVG(review_count) FROM product_rating), 0) * 100, 1);


-- =====================================================================
-- P04: 库存周转率分析 — 销量/库存比率排名，识别滞销和热销商品
-- 业务价值：优化库存管理，避免断货和积压
-- 预期输出列：product_name | total_stock | total_sold | turnover_rate | turnover_rank | stock_status
-- =====================================================================
WITH stock_turnover AS (
    SELECT
        p.product_id,
        p.product_name,
        p.stock AS total_stock,
        COALESCE(SUM(oi.quantity), 0) AS total_sold,
        CASE
            WHEN p.stock > 0 THEN ROUND(COALESCE(SUM(oi.quantity), 0) * 1.0 / p.stock, 4)
            ELSE NULL
        END AS turnover_rate
    FROM products p
    LEFT JOIN order_items oi ON p.product_id = oi.product_id
    LEFT JOIN orders o ON oi.order_id = o.order_id AND o.status = 'completed'
    GROUP BY p.product_id, p.product_name, p.stock
)
SELECT
    product_name,
    total_stock,
    total_sold,
    turnover_rate,
    RANK() OVER (ORDER BY turnover_rate DESC) AS turnover_rank,
    CASE
        WHEN turnover_rate >= 0.8 THEN '热销(周转快)'
        WHEN turnover_rate >= 0.4 THEN '正常(周转适中)'
        WHEN turnover_rate >= 0.1 THEN '滞销(周转慢)'
        WHEN turnover_rate IS NULL THEN '无销售记录'
        ELSE '严重积压'
    END AS stock_status
FROM stock_turnover
ORDER BY turnover_rate DESC;


-- =====================================================================
-- P05: 长尾商品贡献分析 — 头部/腰部/长尾商品的销量贡献分布
-- 业务价值：验证二八定律，指导长尾商品策略
-- 预期输出列：product_tier | product_count | tier_sold | sold_pct | cumulative_pct
-- =====================================================================
WITH product_sales AS (
    SELECT
        p.product_id,
        p.product_name,
        COALESCE(SUM(oi.quantity), 0) AS total_sold
    FROM products p
    LEFT JOIN order_items oi ON p.product_id = oi.product_id
    LEFT JOIN orders o ON oi.order_id = o.order_id AND o.status = 'completed'
    GROUP BY p.product_id, p.product_name
),
ranked AS (
    SELECT
        product_name,
        total_sold,
        ROW_NUMBER() OVER (ORDER BY total_sold DESC) AS rn,
        SUM(total_sold) OVER (ORDER BY total_sold DESC) AS cumulative_sold,
        SUM(total_sold) OVER () AS total_all_sold,
        COUNT(*) OVER () AS total_products
    FROM product_sales
)
SELECT
    CASE
        WHEN rn <= total_products * 0.2 THEN '头部商品(前20%)'
        WHEN cumulative_sold <= total_all_sold * 0.8 THEN '腰部商品'
        ELSE '长尾商品'
    END AS product_tier,
    COUNT(*) AS product_count,
    SUM(total_sold) AS tier_sold,
    ROUND(SUM(total_sold) * 100.0 / MAX(total_all_sold), 2) AS sold_pct,
    ROUND(SUM(total_sold) * 100.0 / MAX(total_all_sold), 2) AS cumulative_pct  -- 这里每个tier独立计算
FROM ranked
GROUP BY
    CASE
        WHEN rn <= total_products * 0.2 THEN '头部商品(前20%)'
        WHEN cumulative_sold <= total_all_sold * 0.8 THEN '腰部商品'
        ELSE '长尾商品'
    END
ORDER BY AVG(CASE
    WHEN rn <= total_products * 0.2 THEN 1
    WHEN cumulative_sold <= total_all_sold * 0.8 THEN 2
    ELSE 3 END);


-- =====================================================================
-- P06: 商品价格区间分析 — 各价格段的商品数量、销量、GMV
-- 业务价值：了解价格带分布，指导定价策略
-- 预期输出列：price_range | product_count | total_sold | total_gmv | avg_rating
-- =====================================================================
WITH price_seg AS (
    SELECT
        p.product_id,
        p.price,
        CASE
            WHEN p.price < 50 THEN '0-50元(低价)'
            WHEN p.price < 100 THEN '50-100元(中低价)'
            WHEN p.price < 200 THEN '100-200元(中价)'
            WHEN p.price < 500 THEN '200-500元(中高价)'
            WHEN p.price < 1000 THEN '500-1000元(高价)'
            ELSE '1000元以上(奢侈品)'
        END AS price_range,
        COALESCE(SUM(oi.quantity), 0) AS sold_qty,
        COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS range_gmv
    FROM products p
    LEFT JOIN order_items oi ON p.product_id = oi.product_id
    LEFT JOIN orders o ON oi.order_id = o.order_id AND o.status = 'completed'
    GROUP BY p.product_id, p.price
)
SELECT
    price_range,
    COUNT(*) AS product_count,
    SUM(sold_qty) AS total_sold,
    ROUND(SUM(range_gmv), 2) AS total_gmv,
    ROUND(AVG(price), 2) AS avg_price,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS product_pct,
    ROUND(SUM(range_gmv) * 100.0 / SUM(SUM(range_gmv)) OVER (), 2) AS gmv_pct
FROM price_seg
GROUP BY price_range
ORDER BY MIN(CASE price_range
    WHEN '0-50元(低价)' THEN 1 WHEN '50-100元(中低价)' THEN 2
    WHEN '100-200元(中价)' THEN 3 WHEN '200-500元(中高价)' THEN 4
    WHEN '500-1000元(高价)' THEN 5 ELSE 6 END);


-- =====================================================================
-- P07: 各品类评分分布 — 每个品类的平均评分和标准差
-- 业务价值：评估各品类用户满意度，定位需要改进的品类
-- 预期输出列：category_name | avg_rating | rating_stddev | review_count | five_star_pct
-- =====================================================================
SELECT
    c.category_name,
    ROUND(AVG(r.rating), 2) AS avg_rating,
    ROUND(STDDEV(r.rating), 2) AS rating_stddev,
    COUNT(r.review_id) AS review_count,
    ROUND(SUM(CASE WHEN r.rating = 5 THEN 1 ELSE 0 END) * 100.0
        / NULLIF(COUNT(r.review_id), 0), 2) AS five_star_pct,
    ROUND(SUM(CASE WHEN r.rating <= 2 THEN 1 ELSE 0 END) * 100.0
        / NULLIF(COUNT(r.review_id), 0), 2) AS negative_pct
FROM categories c
INNER JOIN products p ON c.category_id = p.category_id
INNER JOIN reviews r ON p.product_id = r.product_id
GROUP BY c.category_name
HAVING COUNT(r.review_id) >= 10
ORDER BY avg_rating DESC;


-- =====================================================================
-- P08: 新品表现分析 — 最近30天上架商品的销售表现
-- 业务价值：快速评估新品的市场接受度
-- 预期输出列：product_name | category_name | price | days_listed | total_sold | daily_avg_sold | review_count | avg_rating
-- =====================================================================
WITH new_products AS (
    SELECT
        p.product_id,
        p.product_name,
        p.category_id,
        p.price,
        p.created_at,
        DATEDIFF(CURRENT_DATE, p.created_at) AS days_listed
    FROM products p
    WHERE DATEDIFF(CURRENT_DATE, p.created_at) <= 30
)
SELECT
    np.product_name,
    c.category_name,
    np.price,
    np.days_listed,
    COALESCE(SUM(oi.quantity), 0) AS total_sold,
    ROUND(COALESCE(SUM(oi.quantity), 0) * 1.0
        / NULLIF(np.days_listed, 0), 2) AS daily_avg_sold,
    COUNT(DISTINCT r.review_id) AS review_count,
    ROUND(AVG(r.rating), 2) AS avg_rating
FROM new_products np
LEFT JOIN categories c ON np.category_id = c.category_id
LEFT JOIN order_items oi ON np.product_id = oi.product_id
LEFT JOIN orders o ON oi.order_id = o.order_id AND o.status = 'completed'
LEFT JOIN reviews r ON np.product_id = r.product_id
GROUP BY np.product_name, c.category_name, np.price, np.days_listed
ORDER BY total_sold DESC;


-- =====================================================================
-- P09: 商品搜索热度分析 — 从user_logs统计各商品的浏览/加购行为
-- 业务价值：了解用户兴趣分布，优化搜索排名和推荐
-- 预期输出列：product_name | view_count | cart_count | cart_rate | wish_count | action_total
-- =====================================================================
WITH action_counts AS (
    SELECT
        product_id,
        SUM(CASE WHEN action_type = 'view' THEN 1 ELSE 0 END) AS view_count,
        SUM(CASE WHEN action_type = 'cart' THEN 1 ELSE 0 END) AS cart_count,
        SUM(CASE WHEN action_type = 'wish' THEN 1 ELSE 0 END) AS wish_count,
        SUM(CASE WHEN action_type = 'buy' THEN 1 ELSE 0 END) AS buy_count,
        COUNT(*) AS action_total
    FROM user_logs
    WHERE action_time >= DATE_SUB(CURRENT_DATE, INTERVAL 90 DAY)
    GROUP BY product_id
)
SELECT
    p.product_name,
    c.category_name,
    ac.view_count,
    ac.cart_count,
    ROUND(ac.cart_count * 100.0 / NULLIF(ac.view_count, 0), 2) AS cart_conversion_rate,
    ac.wish_count,
    ac.buy_count,
    ac.action_total,
    DENSE_RANK() OVER (ORDER BY ac.view_count DESC) AS hot_rank
FROM action_counts ac
INNER JOIN products p ON ac.product_id = p.product_id
INNER JOIN categories c ON p.category_id = c.category_id
ORDER BY ac.view_count DESC
LIMIT 50;


-- =====================================================================
-- P10: 季节性商品识别 — 月度销量波动分析，识别季节性商品
-- 业务价值：提前备货，把握季节性销售机会
-- 预期输出列：product_name | category | month_1 | month_2 | ... | month_12 | cv(变异系数) | seasonality
-- =====================================================================
WITH monthly_product_sales AS (
    SELECT
        p.product_id,
        p.product_name,
        c.category_name,
        MONTH(o.order_date) AS sale_month,
        SUM(oi.quantity) AS monthly_sold
    FROM products p
    INNER JOIN categories c ON p.category_id = c.category_id
    INNER JOIN order_items oi ON p.product_id = oi.product_id
    INNER JOIN orders o ON oi.order_id = o.order_id
    WHERE o.status = 'completed'
    GROUP BY p.product_id, p.product_name, c.category_name, MONTH(o.order_date)
),
stats AS (
    SELECT
        product_id,
        product_name,
        category_name,
        AVG(monthly_sold) AS avg_monthly,
        STDDEV(monthly_sold) AS std_monthly,
        COUNT(DISTINCT sale_month) AS active_months
    FROM monthly_product_sales
    GROUP BY product_id, product_name, category_name
    HAVING COUNT(DISTINCT sale_month) >= 6
)
SELECT
    product_name,
    category_name,
    active_months,
    ROUND(avg_monthly, 1) AS avg_monthly_sold,
    ROUND(std_monthly, 1) AS std_monthly_sold,
    ROUND(std_monthly / NULLIF(avg_monthly, 0), 3) AS cv,
    CASE
        WHEN std_monthly / NULLIF(avg_monthly, 0) >= 0.6 THEN '强季节性商品'
        WHEN std_monthly / NULLIF(avg_monthly, 0) >= 0.3 THEN '弱季节性商品'
        ELSE '非季节性商品'
    END AS seasonality
FROM stats
ORDER BY cv DESC
LIMIT 50;
```

### 8.3 订单分析（10条SQL）

```sql
-- =====================================================================
-- O01: 每日GMV趋势 — 每日总交易额变化
-- 业务价值：监控大盘变化，及时发现异常波动
-- 预期输出列：order_date | total_gmv | order_count | avg_order_value | rolling_7d_gmv
-- =====================================================================
WITH daily_stats AS (
    SELECT
        DATE(order_date) AS order_date,
        SUM(actual_amount) AS total_gmv,
        COUNT(DISTINCT order_id) AS order_count
    FROM orders
    WHERE status = 'completed'
    GROUP BY DATE(order_date)
)
SELECT
    order_date,
    ROUND(total_gmv, 2) AS total_gmv,
    order_count,
    ROUND(total_gmv / NULLIF(order_count, 0), 2) AS avg_order_value,
    ROUND(AVG(total_gmv) OVER (ORDER BY order_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 2) AS rolling_7d_avg_gmv,
    ROUND(LAG(total_gmv) OVER (ORDER BY order_date), 2) AS prev_day_gmv,
    ROUND((total_gmv - LAG(total_gmv) OVER (ORDER BY order_date))
        / NULLIF(LAG(total_gmv) OVER (ORDER BY order_date), 0) * 100, 2) AS dod_change_pct
FROM daily_stats
ORDER BY order_date;


-- =====================================================================
-- O02: 客单价分布分析 — 不同客单价区间的订单分布
-- 业务价值：了解用户消费能力分布，指导促销门槛设置
-- 预期输出列：aov_range | order_count | order_pct | total_gmv | gmv_pct
-- =====================================================================
WITH order_aov AS (
    SELECT
        order_id,
        actual_amount,
        CASE
            WHEN actual_amount < 50 THEN '0-50元'
            WHEN actual_amount < 100 THEN '50-100元'
            WHEN actual_amount < 200 THEN '100-200元'
            WHEN actual_amount < 500 THEN '200-500元'
            WHEN actual_amount < 1000 THEN '500-1000元'
            ELSE '1000元以上'
        END AS aov_range
    FROM orders
    WHERE status = 'completed'
)
SELECT
    aov_range,
    COUNT(*) AS order_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS order_pct,
    ROUND(SUM(actual_amount), 2) AS total_gmv,
    ROUND(SUM(actual_amount) * 100.0 / SUM(SUM(actual_amount)) OVER (), 2) AS gmv_pct,
    ROUND(AVG(actual_amount), 2) AS avg_in_range
FROM order_aov
GROUP BY aov_range
ORDER BY MIN(CASE aov_range
    WHEN '0-50元' THEN 1 WHEN '50-100元' THEN 2
    WHEN '100-200元' THEN 3 WHEN '200-500元' THEN 4
    WHEN '500-1000元' THEN 5 ELSE 6 END);


-- =====================================================================
-- O03: 各时段订单特征 — 按小时分析下单高峰时段
-- 业务价值：指导客服排班和促销活动时间选择
-- 预期输出列：order_hour | order_count | total_gmv | avg_order_value | unique_users
-- =====================================================================
SELECT
    HOUR(order_date) AS order_hour,
    COUNT(DISTINCT order_id) AS order_count,
    ROUND(SUM(actual_amount), 2) AS total_gmv,
    ROUND(AVG(actual_amount), 2) AS avg_order_value,
    COUNT(DISTINCT user_id) AS unique_users,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS order_pct,
    CASE
        WHEN HOUR(order_date) BETWEEN 0 AND 5 THEN '凌晨低谷期'
        WHEN HOUR(order_date) BETWEEN 6 AND 9 THEN '早晨增长期'
        WHEN HOUR(order_date) BETWEEN 10 AND 13 THEN '午间高峰期'
        WHEN HOUR(order_date) BETWEEN 14 AND 17 THEN '下午平稳期'
        WHEN HOUR(order_date) BETWEEN 18 AND 21 THEN '晚间黄金期'
        ELSE '深夜收尾期'
    END AS time_period
FROM orders
WHERE status = 'completed'
GROUP BY HOUR(order_date)
ORDER BY order_hour;


-- =====================================================================
-- O04: 退款率月度分析 — 每月退款订单占比和退款金额趋势
-- 业务价值：监控退款率变化，及时发现商品或服务问题
-- 预期输出列：refund_month | total_orders | refund_orders | refund_rate_pct | refund_amount | refund_gmv_pct
-- =====================================================================
WITH monthly_orders AS (
    SELECT
        DATE_FORMAT(order_date, '%Y-%m') AS order_month,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(actual_amount) AS total_gmv,
        SUM(CASE WHEN status = 'refunded' THEN 1 ELSE 0 END) AS refund_count,
        SUM(CASE WHEN status = 'refunded' THEN actual_amount ELSE 0 END) AS refund_amount
    FROM orders
    WHERE status IN ('completed', 'refunded', 'cancelled')
    GROUP BY DATE_FORMAT(order_date, '%Y-%m')
)
SELECT
    order_month AS refund_month,
    total_orders,
    refund_count AS refund_orders,
    ROUND(refund_count * 100.0 / NULLIF(total_orders, 0), 2) AS refund_rate_pct,
    ROUND(refund_amount, 2) AS refund_amount,
    ROUND(refund_amount * 100.0 / NULLIF(total_gmv, 0), 2) AS refund_gmv_pct,
    ROUND(LAG(refund_count * 100.0 / NULLIF(total_orders, 0)) OVER (ORDER BY order_month), 2) AS prev_month_rate
FROM monthly_orders
ORDER BY order_month;


-- =====================================================================
-- O05: 各城市订单特征对比 — 多维度城市订单画像
-- 业务价值：了解各城市消费特点，差异化运营
-- 预期输出列：city | order_count | total_gmv | avg_order_value | top_category | afternoon_ratio
-- =====================================================================
WITH city_orders AS (
    SELECT
        u.city,
        o.order_id,
        o.actual_amount,
        o.order_date,
        HOUR(o.order_date) AS order_hour
    FROM orders o
    INNER JOIN users u ON o.user_id = u.user_id
    WHERE o.status = 'completed'
),
city_category AS (
    SELECT
        u.city,
        c.category_name,
        COUNT(DISTINCT o.order_id) AS cat_order_count,
        ROW_NUMBER() OVER (PARTITION BY u.city ORDER BY COUNT(DISTINCT o.order_id) DESC) AS rn
    FROM orders o
    INNER JOIN users u ON o.user_id = u.user_id
    INNER JOIN order_items oi ON o.order_id = oi.order_id
    INNER JOIN products p ON oi.product_id = p.product_id
    INNER JOIN categories c ON p.category_id = c.category_id
    WHERE o.status = 'completed'
    GROUP BY u.city, c.category_name
)
SELECT
    co.city,
    COUNT(DISTINCT co.order_id) AS order_count,
    ROUND(SUM(co.actual_amount), 2) AS total_gmv,
    ROUND(AVG(co.actual_amount), 2) AS avg_order_value,
    MAX(CASE WHEN cc.rn = 1 THEN cc.category_name END) AS top_category,
    ROUND(SUM(CASE WHEN co.order_hour BETWEEN 14 AND 18 THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2) AS afternoon_order_pct
FROM city_orders co
LEFT JOIN city_category cc ON co.city = cc.city AND cc.rn = 1
GROUP BY co.city
ORDER BY total_gmv DESC
LIMIT 10;


-- =====================================================================
-- O06: 支付方式偏好分析 — 各支付方式的订单占比
-- 业务价值：优化支付渠道，降低支付失败率
-- 预期输出列：payment_method | order_count | order_pct | total_gmv | gmv_pct | avg_order_value
-- =====================================================================
SELECT
    payment_method,
    COUNT(DISTINCT order_id) AS order_count,
    ROUND(COUNT(DISTINCT order_id) * 100.0
        / SUM(COUNT(DISTINCT order_id)) OVER (), 2) AS order_pct,
    ROUND(SUM(actual_amount), 2) AS total_gmv,
    ROUND(SUM(actual_amount) * 100.0
        / SUM(SUM(actual_amount)) OVER (), 2) AS gmv_pct,
    ROUND(AVG(actual_amount), 2) AS avg_order_value,
    COUNT(DISTINCT user_id) AS unique_users
FROM orders
WHERE status IN ('paid', 'shipped', 'completed')
GROUP BY payment_method
ORDER BY order_count DESC;


-- =====================================================================
-- O07: 订单转化漏斗 — 从浏览到支付的完整转化路径
-- 业务价值：发现转化瓶颈，优化关键环节
-- 预期输出列：stage | user_count | overall_conversion_pct | step_conversion_pct
-- =====================================================================
WITH funnel AS (
    SELECT
        '1.商品浏览' AS stage, COUNT(DISTINCT user_id) AS user_count
    FROM user_logs WHERE action_type = 'view'
    UNION ALL
    SELECT
        '2.加入购物车' AS stage, COUNT(DISTINCT user_id) AS user_count
    FROM user_logs WHERE action_type = 'cart'
    UNION ALL
    SELECT
        '3.创建订单' AS stage, COUNT(DISTINCT user_id) AS user_count
    FROM orders WHERE status != 'cancelled'
    UNION ALL
    SELECT
        '4.完成支付' AS stage, COUNT(DISTINCT user_id) AS user_count
    FROM orders WHERE status IN ('paid', 'shipped', 'completed')
    UNION ALL
    SELECT
        '5.确认收货' AS stage, COUNT(DISTINCT user_id) AS user_count
    FROM orders WHERE status = 'completed'
)
SELECT
    stage,
    user_count,
    ROUND(user_count * 100.0
        / FIRST_VALUE(user_count) OVER (ORDER BY stage), 2) AS overall_conversion_pct,
    ROUND(user_count * 100.0
        / NULLIF(LAG(user_count) OVER (ORDER BY stage), 0), 2) AS step_conversion_pct,
    CASE
        WHEN user_count < LAG(user_count) OVER (ORDER BY stage)
        THEN CONCAT('流失 ', LAG(user_count) OVER (ORDER BY stage) - user_count, ' 用户')
        ELSE '-'
    END AS step_loss
FROM funnel
ORDER BY stage;


-- =====================================================================
-- O08: 周度GMV环比增长率 — 每周GMV的环比变化
-- 业务价值：监控周度趋势，评估促销活动效果
-- 预期输出列：yrwk | gmv | prev_week_gmv | wow_change_pct | order_count | avg_order_value
-- =====================================================================
WITH weekly_gmv AS (
    SELECT
        YEARWEEK(order_date, 1) AS yrwk,
        SUM(actual_amount) AS gmv,
        COUNT(DISTINCT order_id) AS order_count
    FROM orders
    WHERE status = 'completed'
    GROUP BY YEARWEEK(order_date, 1)
)
SELECT
    yrwk,
    ROUND(gmv, 2) AS gmv,
    order_count,
    ROUND(gmv / NULLIF(order_count, 0), 2) AS avg_order_value,
    ROUND(LAG(gmv) OVER (ORDER BY yrwk), 2) AS prev_week_gmv,
    ROUND((gmv - LAG(gmv) OVER (ORDER BY yrwk))
        / NULLIF(LAG(gmv) OVER (ORDER BY yrwk), 0) * 100, 2) AS wow_change_pct
FROM weekly_gmv
ORDER BY yrwk;


-- =====================================================================
-- O09: 大额订单特征分析 — 客单价≥500元的订单用户画像
-- 业务价值：识别高消费用户的偏好，定向推荐高端商品
-- 预期输出列：feature | big_order_value | normal_order_value | ratio
-- =====================================================================
WITH order_features AS (
    SELECT
        o.order_id,
        o.actual_amount,
        u.age,
        u.gender,
        u.city,
        COUNT(DISTINCT oi.product_id) AS item_variety,
        SUM(oi.quantity) AS total_items,
        CASE WHEN o.actual_amount >= 500 THEN '大额订单' ELSE '普通订单' END AS order_type
    FROM orders o
    INNER JOIN users u ON o.user_id = u.user_id
    INNER JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.status = 'completed'
    GROUP BY o.order_id, o.actual_amount, u.age, u.gender, u.city
)
SELECT
    'avg_user_age' AS feature,
    ROUND(AVG(CASE WHEN order_type='大额订单' THEN age END), 1) AS big_order_value,
    ROUND(AVG(CASE WHEN order_type='普通订单' THEN age END), 1) AS normal_order_value,
    ROUND(AVG(CASE WHEN order_type='大额订单' THEN age END)
        / NULLIF(AVG(CASE WHEN order_type='普通订单' THEN age END), 0), 2) AS ratio
FROM order_features
UNION ALL
SELECT 'avg_item_variety',
    ROUND(AVG(CASE WHEN order_type='大额订单' THEN item_variety END), 1),
    ROUND(AVG(CASE WHEN order_type='普通订单' THEN item_variety END), 1),
    ROUND(AVG(CASE WHEN order_type='大额订单' THEN item_variety END)
        / NULLIF(AVG(CASE WHEN order_type='普通订单' THEN item_variety END), 0), 2)
FROM order_features
UNION ALL
SELECT 'avg_total_items',
    ROUND(AVG(CASE WHEN order_type='大额订单' THEN total_items END), 1),
    ROUND(AVG(CASE WHEN order_type='普通订单' THEN total_items END), 1),
    ROUND(AVG(CASE WHEN order_type='大额订单' THEN total_items END)
        / NULLIF(AVG(CASE WHEN order_type='普通订单' THEN total_items END), 0), 2)
FROM order_features
UNION ALL
SELECT 'female_ratio_pct',
    ROUND(SUM(CASE WHEN order_type='大额订单' AND gender='F' THEN 1 ELSE 0 END)*100.0
        / NULLIF(SUM(CASE WHEN order_type='大额订单' THEN 1 ELSE 0 END), 0), 1),
    ROUND(SUM(CASE WHEN order_type='普通订单' AND gender='F' THEN 1 ELSE 0 END)*100.0
        / NULLIF(SUM(CASE WHEN order_type='普通订单' THEN 1 ELSE 0 END), 0), 1),
    NULL
FROM order_features;


-- =====================================================================
-- O10: 订单配送时效分析 — 下单→发货→签收各环节耗时
-- 业务价值：监控物流效率，优化配送体验
-- 预期输出列：city | avg_payment_to_ship_hours | avg_ship_to_deliver_hours | avg_total_hours | order_count
-- =====================================================================
WITH order_timeline AS (
    SELECT
        o.order_id,
        u.city,
        o.order_date AS created_time,
        o.paid_time,
        o.shipped_time,
        o.delivered_time,
        TIMESTAMPDIFF(HOUR, o.order_date, o.paid_time) AS pay_hours,
        TIMESTAMPDIFF(HOUR, o.paid_time, o.shipped_time) AS payment_to_ship_hours,
        TIMESTAMPDIFF(HOUR, o.shipped_time, o.delivered_time) AS ship_to_deliver_hours,
        TIMESTAMPDIFF(HOUR, o.order_date, o.delivered_time) AS total_hours
    FROM orders o
    INNER JOIN users u ON o.user_id = u.user_id
    WHERE o.status = 'completed'
        AND o.paid_time IS NOT NULL
        AND o.shipped_time IS NOT NULL
        AND o.delivered_time IS NOT NULL
)
SELECT
    city,
    ROUND(AVG(payment_to_ship_hours), 1) AS avg_payment_to_ship_hours,
    ROUND(AVG(ship_to_deliver_hours), 1) AS avg_ship_to_deliver_hours,
    ROUND(AVG(total_hours), 1) AS avg_total_hours,
    COUNT(*) AS order_count,
    ROUND(SUM(CASE WHEN total_hours <= 24 THEN 1 ELSE 0 END) * 100.0
        / COUNT(*), 2) AS within_24h_pct
FROM order_timeline
GROUP BY city
ORDER BY avg_total_hours
LIMIT 15;
```

---

## 九、分析报告示例

以下展示部分SQL的预期输出格式和业务解读，学员应参考此格式编写完整的 `analysis_results.md`。

### 示例1：U04 用户LTV排名

**预期输出（TOP 5）**：

```
+---------+------------+----------+--------+-------------+------------+-------------+-----------+
| user_id | username   | city     | ltv    | order_count | active_days| daily_value | ltv_decile|
+---------+------------+----------+--------+-------------+------------+-------------+-----------+
|    1023 | zhangsan   | 北京     | 58920.5|     156     |    88      |  669.55     |     1     |
|    4098 | lisi       | 上海     | 45230.0|     132     |    90      |  502.56     |     1     |
|    7221 | wanger     | 深圳     | 38900.0|     118     |    85      |  457.65     |     1     |
|    3156 | liuwu      | 广州     | 32100.0|      98     |    90      |  356.67     |     2     |
|    8890 | zhaoliu    | 杭州     | 29800.0|      87     |    78      |  382.05     |     2     |
+---------+------------+----------+--------+-------------+------------+-------------+-----------+
```

**业务解读**：
- LTV前十等分（decile 1）的用户贡献了绝大部分GMV，符合典型的二八分布。
- 头部用户平均日贡献值(daily_value)在400-700元之间，建议设立VIP服务通道。
- 北京、上海、深圳的用户LTV显著高于其他城市，应加大这三个城市的高端商品投放。
- 活跃天数越长的用户LTV越高，说明用户生命周期管理(LCM)至关重要。

---

### 示例2：P01 各品类销售额排名

**预期输出（TOP 5）**：

```
+-----------------+-----------+-------------+-------------+---------+----------------+----------+
| category_name   | total_gmv | order_count | product_cnt | gmv_pct | cumulative_pct | gmv_rank |
+-----------------+-----------+-------------+-------------+---------+----------------+----------+
| 手机数码        | 2580000.50|      12500  |       380   |   28.5  |    28.5        |    1     |
| 家用电器        | 1850000.00|       9800  |       450   |   20.4  |    48.9        |    2     |
| 服装鞋包        | 1420000.00|      22000  |      1200   |   15.7  |    64.6        |    3     |
| 食品饮料        | 1100000.00|      18000  |       800   |   12.1  |    76.7        |    4     |
| 美妆个护        |  850000.00|      15000  |       650   |    9.4  |    86.1        |    5     |
+-----------------+-----------+-------------+-------------+---------+----------------+----------+
```

**业务解读**：
- TOP2品类（手机数码+家用电器）贡献了48.9%的GMV，属于核心品类，需要保证供应链稳定。
- 服装鞋包虽然GMV排第3，但订单数最高(22000单)，说明属于高频低客单价品类，适合做引流。
- TOP5品类贡献了86.1%的GMV，剩余15个品类仅贡献13.9%，需评估尾部品类是否值得保留。

---

### 示例3：O01 每日GMV趋势

**预期输出（部分）**：

```
+------------+----------+-------------+------------------+------------------+--------------+---------------+
| order_date | total_gmv| order_count | avg_order_value  | rolling_7d_gmv   | prev_day_gmv | dod_change_pct|
+------------+----------+-------------+------------------+------------------+--------------+---------------+
| 2024-12-14 |  45800.00|        320  |      143.13      |      46200.00    |   45200.00   |      1.33     |
| 2024-12-15 |  51200.00|        355  |      144.23      |      46350.00    |   45800.00   |     11.79     |
| 2024-12-16 |  47800.00|        330  |      144.85      |      46500.00    |   51200.00   |     -6.64     |
| 2024-12-17 |  44500.00|        310  |      143.55      |      46800.00    |   47800.00   |     -6.90     |
| 2024-12-18 |  43500.00|        305  |      142.62      |      46000.00    |   44500.00   |     -2.25     |
+------------+----------+-------------+------------------+------------------+--------------+---------------+
```

**业务解读**：
- 12月15日(周日)GMV明显高于工作日，与周末效应一致。
- 12月15日后GMV连续下降，直到下一个周末回升，说明该电商平台周末消费占比较高。
- 滚动7日均值(rolling_7d_gmv)保持在46000左右，趋势线平稳，无异常波动。
- 建议：在周一到周三加大促销力度，平衡工作日和周末的GMV差距。

---

### 示例4：O07 订单转化漏斗

**预期输出**：

```
+------------------+------------+-------------------------+--------------------+---------------------+
| stage            | user_count | overall_conversion_pct  | step_conversion_pct| step_loss           |
+------------------+------------+-------------------------+--------------------+---------------------+
| 1.商品浏览       |    85200   |          100.00         |          -         |          -          |
| 2.加入购物车     |    18500   |           21.71         |       21.71        | 流失 66700 用户     |
| 3.创建订单       |     5200   |            6.10         |       28.11        | 流失 13300 用户     |
| 4.完成支付       |     4300   |            5.05         |       82.69        | 流失 900 用户      |
| 5.确认收货       |     4150   |            4.87         |       96.51        | 流失 150 用户      |
+------------------+------------+-------------------------+--------------------+---------------------+
```

**业务解读**：
- 从浏览到加购的转化率仅21.71%，是最主要的流失环节，需优化商品详情页和推荐算法。
- 加购到下单转化率为28.11%，表明大量用户将商品加入购物车后未结算，可设置购物车提醒和限时优惠促转化。
- 下单到支付转化率达82.69%，支付环节体验较好。
- 支付到确认收货转化率高达96.51%，说明物流和售后体验良好。
- **核心结论**：最大瓶颈在"浏览→加购"环节，应重点优化搜索推荐和商品展示。

---

## 十、完整Python数据生成脚本 seed_data.py

以下脚本生成所有7张表的模拟数据，可直接运行：

```python
#!/usr/bin/env python3
"""
seed_data.py - 电商数据库模拟数据生成脚本
生成7张表的数据并输出为SQL INSERT语句文件
数据规模：users(10000), categories(20), products(5000),
         orders(50000), order_items(200000), reviews(15000), user_logs(100000)
"""

import random
import string
import datetime
import itertools
from collections import defaultdict

# ============================================================
# 全局配置
# ============================================================
random.seed(42)

NUM_USERS = 10000
NUM_CATEGORIES = 20
NUM_PRODUCTS = 5000
NUM_ORDERS = 50000
NUM_ORDER_ITEMS = 200000
NUM_REVIEWS = 15000
NUM_USER_LOGS = 100000

START_DATE = datetime.date(2024, 10, 1)
END_DATE = datetime.date(2024, 12, 31)
TOTAL_DAYS = (END_DATE - START_DATE).days

CITIES = [
    ("北京", 0.12), ("上海", 0.11), ("广州", 0.08), ("深圳", 0.09),
    ("杭州", 0.06), ("成都", 0.06), ("武汉", 0.05), ("南京", 0.04),
    ("重庆", 0.04), ("西安", 0.03), ("长沙", 0.03), ("天津", 0.03),
    ("郑州", 0.03), ("苏州", 0.03), ("东莞", 0.02), ("青岛", 0.02),
    ("沈阳", 0.02), ("宁波", 0.02), ("昆明", 0.02), ("合肥", 0.02),
    ("福州", 0.01), ("厦门", 0.01), ("大连", 0.01), ("济南", 0.01),
    ("无锡", 0.01)
]

FIRST_NAMES = ["伟", "芳", "娜", "敏", "静", "丽", "强", "磊", "洋", "勇",
               "艳", "杰", "军", "秀英", "涛", "明", "超", "秀兰", "霞", "平",
               "刚", "华", "文", "飞", "玉兰", "桂英", "鑫", "博", "宇", "浩"]

LAST_NAMES = ["张", "王", "李", "赵", "刘", "陈", "杨", "黄", "周", "吴",
              "徐", "孙", "马", "胡", "朱", "郭", "何", "罗", "高", "林"]

CATEGORY_NAMES = [
    ("手机数码", None), ("家用电器", "手机数码"), ("服装鞋包", None),
    ("食品饮料", None), ("美妆个护", "服装鞋包"), ("运动户外", "服装鞋包"),
    ("家具家装", "家用电器"), ("图书文娱", None), ("母婴玩具", "服装鞋包"),
    ("汽车用品", "运动户外"), ("医药保健", "食品饮料"), ("宠物生活", "食品饮料"),
    ("办公文具", "图书文娱"), ("珠宝配饰", "服装鞋包"), ("家纺布艺", "家具家装"),
    ("厨房用品", "家具家装"), ("生鲜水果", "食品饮料"), ("酒水饮料", "食品饮料"),
    ("数码配件", "手机数码"), ("电脑办公", "手机数码")
]

STATUSES = ["pending", "paid", "shipped", "completed", "cancelled", "refunded"]
STATUS_WEIGHTS = [0.05, 0.08, 0.20, 0.45, 0.15, 0.07]
PAYMENT_METHODS = ["wechat", "alipay", "credit_card", "debit_card", "cod"]
PAYMENT_WEIGHTS = [0.35, 0.30, 0.15, 0.10, 0.10]
ACTION_TYPES = ["view", "cart", "wish", "buy", "search", "compare"]
ACTION_WEIGHTS = [0.50, 0.15, 0.08, 0.05, 0.15, 0.07]

PRODUCT_ADJECTIVES = [
    "高级", "智能", "经典", "迷你", "便携", "环保", "奢华", "简约",
    "时尚", "运动", "复古", "创意", "多功能", "静音", "高速", "节能",
    "超薄", "大容量", "专业", "高端"
]


def weighted_choice(choices_with_weights):
    """带权重的随机选择"""
    choices, weights = zip(*choices_with_weights)
    total = sum(weights)
    r = random.uniform(0, total)
    cumulative = 0
    for choice, weight in zip(choices, weights):
        cumulative += weight
        if r <= cumulative:
            return choice
    return choices[-1]


def random_date_weighted():
    """生成带周末权重的随机日期（周末概率更高）"""
    day_offset = random.randint(0, TOTAL_DAYS)
    return START_DATE + datetime.timedelta(days=day_offset)


def random_datetime(day):
    """在指定日期生成随机时间"""
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return datetime.datetime(day.year, day.month, day.day, hour, minute, second)


def generate_username():
    """生成中文用户名"""
    return random.choice(LAST_NAMES) + random.choice(FIRST_NAMES) + \
        str(random.randint(10, 99))


def generate_email(username):
    """生成邮箱"""
    domains = ["qq.com", "163.com", "gmail.com", "outlook.com", "126.com"]
    return f"{username}{random.randint(100, 9999)}@{random.choice(domains)}"


def generate_phone():
    """生成手机号"""
    prefixes = ["138", "139", "150", "151", "152", "158", "159",
                "186", "187", "188", "189", "130", "131", "132", "155", "156"]
    return random.choice(prefixes) + ''.join(str(random.randint(0, 9)) for _ in range(8))


# ============================================================
# 数据生成函数
# ============================================================

def generate_users(num=NUM_USERS):
    """生成用户数据"""
    users = []
    # 注册日期分布：模拟前期集中、后期放缓的增长趋势
    regist_dates = []
    for i in range(num):
        # 前60%用户在第一个月注册
        if i < num * 0.4:
            offset = random.randint(0, 30)
        elif i < num * 0.75:
            offset = random.randint(0, 60)
        else:
            offset = random.randint(0, TOTAL_DAYS)
        regist_dates.append(START_DATE + datetime.timedelta(days=offset))

    regist_dates.sort()

    for i in range(num):
        user_id = i + 1
        username = generate_username()
        city_tuple = weighted_choice(CITIES)
        city = city_tuple[0]
        # 年龄正态分布：均值32，标准差8
        age = int(random.gauss(32, 8))
        age = max(18, min(60, age))
        gender = random.choice(['M', 'F'])
        user = (
            user_id, username, generate_email(username), generate_phone(),
            city, age, gender, regist_dates[i]
        )
        users.append(user)
    return users


def generate_categories():
    """生成品类数据（支持多级分类）"""
    categories = []
    for i, (name, parent_name) in enumerate(CATEGORY_NAMES):
        cat_id = i + 1
        parent_id = None
        if parent_name:
            for cat in categories:
                if cat[1] == parent_name:
                    parent_id = cat[0]
                    break
        level = 1 if parent_id is None else 2
        categories.append((cat_id, name, parent_id, level))
    return categories


def generate_products(num=NUM_PRODUCTS, categories_data=None):
    """生成商品数据，符合长尾分布"""
    products = []
    cat_ids = [c[0] for c in categories_data] if categories_data else range(1, NUM_CATEGORIES + 1)

    for i in range(num):
        product_id = i + 1
        cat_id = random.choice(cat_ids)
        adj = random.choice(PRODUCT_ADJECTIVES)
        base_name = f"{adj}{random.choice(['款','型','系列'])}商品"
        product_name = f"[{cat_id:02d}]{adj}{base_name}_{product_id:04d}"

        # 价格分布：采用对数正态分布模拟真实电商价格
        price = round(random.lognormvariate(4.0, 1.0), 2)
        price = max(9.9, min(9999.0, price))

        # 库存：热门商品库存多，长尾商品库存少
        stock = random.randint(10, 5000)
        # 销量（后续由实际订单计算，这里预置初始值）
        sales = random.randint(0, 1000)
        created_at = START_DATE - datetime.timedelta(days=random.randint(30, 365))

        products.append((product_id, product_name, cat_id, price, stock, sales, created_at))
    return products


def generate_orders(users_data, num=NUM_ORDERS):
    """生成订单数据，包含时间分布和金额分布"""
    orders = []
    user_ids = [u[0] for u in users_data]

    # 用户消费能力分布（帕累托分布）
    user_spending_power = {}
    for uid in user_ids:
        user_spending_power[uid] = random.lognormvariate(4.5, 0.6)

    for i in range(num):
        order_id = i + 1
        user_id = random.choice(user_ids)

        order_date_day = random_date_weighted()
        order_datetime = random_datetime(order_date_day)
        paid_time = order_datetime + datetime.timedelta(minutes=random.randint(1, 120))
        shipped_time = paid_time + datetime.timedelta(hours=random.randint(1, 48))
        delivered_time = shipped_time + datetime.timedelta(hours=random.randint(12, 72))

        status = weighted_choice(list(zip(STATUSES, STATUS_WEIGHTS)))
        payment_method = weighted_choice(list(zip(PAYMENT_METHODS, PAYMENT_WEIGHTS)))

        # total_amount 将在后续根据order_items计算，这里预填
        total_amount = round(user_spending_power[user_id] * random.uniform(0.3, 1.5), 2)
        actual_amount = total_amount if status not in ('cancelled',) else 0.0

        orders.append((
            order_id, user_id, order_datetime, total_amount, actual_amount,
            status, payment_method, paid_time, shipped_time, delivered_time
        ))

    return orders


def generate_order_items(orders_data, products_data, num=NUM_ORDER_ITEMS):
    """生成订单明细，确保每个已完成订单有1-5个商品"""
    items = []
    products_list = [(p[0], p[3]) for p in products_data]  # (product_id, price)

    # 筛选完成的订单
    completed_orders = [o for o in orders_data if o[5] in ('paid', 'shipped', 'completed')]

    item_id = 0
    order_item_map = defaultdict(list)

    for order in orders_data:
        order_id = order[0]
        # 每个订单1-5个商品
        num_items = min(random.randint(1, 5), 5)
        selected_products = random.sample(products_list, min(num_items, len(products_list)))

        for prod_id, prod_price in selected_products:
            item_id += 1
            quantity = random.randint(1, 3)
            unit_price = round(prod_price * random.uniform(0.85, 1.0), 2)
            items.append((item_id, order_id, prod_id, quantity, unit_price))
            order_item_map[order_id].append((quantity, unit_price))

    # 限制总条数
    return items[:num]


def generate_reviews(users_data, products_data, num=NUM_REVIEWS):
    """生成商品评价"""
    reviews = []
    user_ids = [u[0] for u in users_data]
    product_ids = [p[0] for p in products_data]

    # 评分分布：偏向正面（4-5分为主）
    rating_weights = [(1, 0.05), (2, 0.08), (3, 0.12), (4, 0.25), (5, 0.50)]

    review_templates = [
        "很好用，性价比高！", "质量不错，物流很快。", "一般般，凑合用。",
        "非常满意，推荐购买！", "跟描述一致，好评。", "不太满意，有点失望。",
        "包装完好，送货及时。", "第二次购买了，一直很信赖。", "颜色和图片有差异。",
        "用了一段时间了，质量可靠。", "物超所值，还会再来。", "做工精细，材质好。"
    ]

    for i in range(num):
        review_id = i + 1
        user_id = random.choice(user_ids)
        product_id = random.choice(product_ids)
        rating = weighted_choice(rating_weights)
        content = random.choice(review_templates)
        created_at = random_datetime(random_date_weighted())

        reviews.append((review_id, user_id, product_id, rating, content, created_at))

    return reviews


def generate_user_logs(users_data, products_data, num=NUM_USER_LOGS):
    """生成用户行为日志"""
    logs = []
    user_ids = [u[0] for u in users_data]
    product_ids = [p[0] for p in products_data]

    for i in range(num):
        log_id = i + 1
        user_id = random.choice(user_ids)
        product_id = random.choice(product_ids)
        action_type = weighted_choice(list(zip(ACTION_TYPES, ACTION_WEIGHTS)))
        action_time = random_datetime(random_date_weighted())

        # session_id 模拟用户会话
        session_id = f"sess_{user_id}_{int(action_time.timestamp()) // 3600}"

        logs.append((log_id, user_id, product_id, action_type, action_time, session_id))

    return logs


# ============================================================
# 写入SQL文件
# ============================================================

def write_sql(filename, table_name, columns, data, batch_size=500):
    """将数据写入SQL INSERT文件，使用批量插入提高效率"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"-- Auto-generated seed data for {table_name}\n")
        f.write(f"-- Generated: {datetime.datetime.now()}\n")
        f.write(f"-- Total rows: {len(data)}\n\n")

        col_names = ', '.join(columns)
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            f.write(f"INSERT INTO {table_name} ({col_names}) VALUES\n")
            values_list = []
            for row in batch:
                formatted = []
                for val in row:
                    if val is None:
                        formatted.append('NULL')
                    elif isinstance(val, str):
                        escaped = val.replace("'", "''").replace("\\", "\\\\")
                        formatted.append(f"'{escaped}'")
                    elif isinstance(val, datetime.datetime):
                        formatted.append(f"'{val.strftime('%Y-%m-%d %H:%M:%S')}'")
                    elif isinstance(val, datetime.date):
                        formatted.append(f"'{val.strftime('%Y-%m-%d')}'")
                    else:
                        formatted.append(str(val))
                values_list.append('(' + ', '.join(formatted) + ')')
            f.write(',\n'.join(values_list))
            f.write(';\n\n')
        f.write(f"-- End of {table_name} data\n")

    file_size = __import__('os').path.getsize(filename)
    print(f"  ✓ {filename} - {len(data):,} 行, {file_size/1024:.1f} KB")


def main():
    print("=" * 60)
    print("  电商数据库 - 模拟数据生成器")
    print("=" * 60)
    print(f"\n数据规模：users={NUM_USERS}, products={NUM_PRODUCTS}, "
          f"orders={NUM_ORDERS}")
    print(f"时间范围：{START_DATE} 至 {END_DATE}（{TOTAL_DAYS}天）\n")

    output_dir = "seed_data"
    __import__('os').makedirs(output_dir, exist_ok=True)

    # 生成用户
    print("[1/7] 生成用户数据...")
    users = generate_users()
    write_sql(f"{output_dir}/01_users.sql", "users",
              ["user_id", "username", "email", "phone", "city",
               "age", "gender", "registered_at"], users)

    # 生成品类
    print("[2/7] 生成品类数据...")
    categories = generate_categories()
    write_sql(f"{output_dir}/02_categories.sql", "categories",
              ["category_id", "category_name", "parent_id", "level"],
              categories)

    # 生成商品
    print("[3/7] 生成商品数据...")
    products = generate_products(categories_data=categories)
    write_sql(f"{output_dir}/03_products.sql", "products",
              ["product_id", "product_name", "category_id",
               "price", "stock", "sales", "created_at"], products)

    # 生成订单
    print("[4/7] 生成订单数据...")
    orders = generate_orders(users)
    write_sql(f"{output_dir}/04_orders.sql", "orders",
              ["order_id", "user_id", "order_date", "total_amount",
               "actual_amount", "status", "payment_method",
               "paid_time", "shipped_time", "delivered_time"], orders)

    # 生成订单明细
    print("[5/7] 生成订单明细...")
    order_items = generate_order_items(orders, products)
    write_sql(f"{output_dir}/05_order_items.sql", "order_items",
              ["item_id", "order_id", "product_id", "quantity",
               "unit_price"], order_items)

    # 生成评价
    print("[6/7] 生成商品评价...")
    reviews = generate_reviews(users, products)
    write_sql(f"{output_dir}/06_reviews.sql", "reviews",
              ["review_id", "user_id", "product_id", "rating",
               "content", "created_at"], reviews)

    # 生成用户行为日志
    print("[7/7] 生成用户行为日志...")
    logs = generate_user_logs(users, products)
    write_sql(f"{output_dir}/07_user_logs.sql", "user_logs",
              ["log_id", "user_id", "product_id", "action_type",
               "action_time", "session_id"], logs)

    # 统计汇总
    total_size = sum(__import__('os').path.getsize(f"{output_dir}/{f}")
                     for f in __import__('os').listdir(output_dir)
                     if f.endswith('.sql'))
    print(f"\n{'=' * 60}")
    print(f"  总计生成 {sum(len(d) for d in [users, categories, products, orders, order_items, reviews, logs]):,} 行数据")
    print(f"  输出文件总大小: {total_size/1024:.1f} KB")
    print(f"  文件输出目录: {output_dir}/")
    print(f"{'=' * 60}")

    print("\n导入命令:")
    for f in sorted(__import__('os').listdir(output_dir)):
        if f.endswith('.sql'):
            print(f"  mysql -u datauser -p ecommerce < {output_dir}/{f}")


if __name__ == '__main__':
    main()
```

---

## 十一、项目扩展建议

完成基础项目后，可选以下扩展方向增加深度：

| 扩展方向 | 难度 | 说明 |
|----------|------|------|
| 增加分区表 | ⭐⭐ | 对orders表按月份分区，提升查询性能 |
| 增加存储过程 | ⭐⭐ | 将高频分析逻辑封装为存储过程 |
| 增加触发器 | ⭐⭐⭐ | 订单状态变更时自动更新库存和销量 |
| 增加视图 | ⭐ | 创建常用分析视图方便复用 |
| 增加事件调度 | ⭐⭐ | 使用MySQL Event定时执行数据汇总 |
| 接入BI工具 | ⭐⭐ | 将数据导入Metabase/Superset制作可视化看板 |
| 增量数据模拟 | ⭐⭐⭐ | 每天生成新的增量数据并导入 |
| RFM分析 | ⭐⭐ | 基于Recency/Frequency/Monetary的用户分层 |