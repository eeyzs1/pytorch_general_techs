# L1 实验：电商离线数仓最小闭环

本实验用 Python 标准库 `sqlite3` 模拟 L1 的离线数仓练习：建模、装载样例数据、运行分析 SQL、输出报表。它不是 Hive/Spark 的替代品，而是让学员先理解 ODS/DWD/ADS 分层和可测试 SQL 的工程闭环。

## 学习目标

- 理解用户、商品、订单、订单明细的基础关系模型。
- 使用 SQL 完成 GMV、客单价、品类销售、活跃用户等指标统计。
- 形成“建库脚本 -> 分析脚本 -> JSON 报告 -> 单元测试”的可运行交付方式。

## 运行步骤

```bash
python3 build_db.py --output data/ecommerce.db
python3 run_analytics.py data/ecommerce.db --output output/report.json
python3 -m unittest test_sql_warehouse.py
```

仓库根目录也提供快捷命令：

```bash
make lab-l1-test
```

## 输出

`output/report.json` 包含：

- `gmv`: 总交易额
- `paid_orders`: 已支付订单数
- `avg_order_value`: 客单价
- `top_categories`: 销售额最高的品类
- `daily_gmv`: 每日 GMV
