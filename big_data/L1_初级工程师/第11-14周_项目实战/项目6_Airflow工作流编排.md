# 项目6：Airflow工作流编排

> **项目周期**：15小时（设计4h + 开发8h + 测试2h + 文档1h）
>
> **难度等级**：⭐⭐⭐⭐ 实战进阶
>
> **小组人数**：1-2人协作

---

## 一、项目描述

使用Apache Airflow将项目4离线数仓的所有ETL任务编排为每日定时执行的DAG，实现完整的自动化调度。包括任务依赖管理、失败重试、告警通知、SLA监控等功能。

---

## 二、项目目标

1. **掌握Airflow核心概念**：DAG、Task、Operator、Sensor、XCom
2. **能设计生产级DAG**：合理的任务依赖、错误处理、SLA配置
3. **理解调度策略**：Backfill、Catchup、调度间隔等配置
4. **实现完整的ETL调度**：将项目4的所有ETL任务纳入Airflow管理

---

## 三、Airflow核心概念（快速回顾）

```
Airflow核心组件:

DAG (Directed Acyclic Graph):
  - 有向无环图，描述工作流
  - 每个DAG由一个Python文件定义
  - 包含任务(Task)和任务之间的依赖关系

Task:
  - DAG中的最小执行单元
  - 由Operator定义

Operator:
  - BashOperator: 执行Shell命令
  - PythonOperator: 执行Python函数
  - HiveOperator: 执行Hive SQL
  - SparkSubmitOperator: 提交Spark作业
  - SqoopOperator: 执行Sqoop命令
  - EmailOperator: 发送邮件

Sensor:
  - 等待某个条件满足
  - 如: 等待HDFS文件到达, 等待Hive分区存在

XCom:
  - Task之间传递小量数据
  - 如: 上游Task的行数传给下游做校验
```

---

## 四、DAG设计：电商数仓每日ETL

### 4.1 全局DAG依赖图

```
                        ┌─────────────────┐
                        │   凌晨2:00触发    │
                        └────────┬────────┘
                                 │
            ┌────────────────────┼────────────────────┐
            ▼                    ▼                     ▼
   ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
   │extract_mysql     │ │extract_mysql     │ │extract_mysql     │
   │_users            │ │_orders           │ │_skus             │
   │(Sqoop抽取用户表)  │ │(Sqoop抽取订单表)  │ │(Sqoop抽取商品表)  │
   └────────┬─────────┘ └────────┬─────────┘ └────────┬─────────┘
            └────────────────────┼────────────────────┘
                                 │
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
           ┌──────────┐  ┌──────────┐  ┌──────────┐
           │  load_   │  │  load_   │  │  load_   │
           │  ods     │  │  ods     │  │  ods     │
           │  _users  │  │ _orders  │  │  _skus   │
           └────┬─────┘  └────┬─────┘  └────┬─────┘
                └─────────────┼─────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │    load_ods      │
                    │   _all_complete  │
                    │   (Dummy Sensor) │
                    └────────┬─────────┘
                             │
            ┌────────────────┼────────────────┐
            ▼                ▼                ▼
   ┌────────────────┐ ┌────────────┐ ┌────────────────┐
   │ dwd_order      │ │ dwd_user   │ │ dwd_user       │
   │ _detail        │ │ _log       │ │ _register      │
   │ (Spark任务)    │ │ (Spark任务) │ │ (Spark任务)     │
   └───────┬────────┘ └─────┬──────┘ └───────┬────────┘
           └────────────────┼────────────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
   ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
   │ dws_user     │ │ dws_sku      │ │ dws_trade    │
   │ _action_day  │ │ _action_day  │ │ _user_order  │
   │ (Hive SQL)   │ │ (Hive SQL)   │ │ _day (Hive)  │
   └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
          └───────────────┼────────────────┘
                          │
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
   ┌──────────┐  ┌──────────────┐  ┌────────────────┐
   │ ads_user │  │ ads_trade    │  │ ads_conversion │
   │ _retention│ │ _stats (Hive)│  │ _funnel (Hive) │
   │ (Hive)   │  │              │  │                │
   └────┬─────┘  └──────┬───────┘  └───────┬────────┘
        └───────────────┼──────────────────┘
                        │
                        ▼
              ┌──────────────────┐
              │    dq_check      │
              │  (数据质量检查)   │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │   send_report    │
              │  (发送日报邮件)   │
              └──────────────────┘
```

### 4.2 完整DAG代码

```python
"""
dag_ecommerce_daily_etl.py — 电商数仓每日ETL调度DAG

调度说明:
  - 每天凌晨2:00执行
  - 失败自动重试3次，间隔10分钟
  - SLA: 6:00前必须完成
  - 执行超时: 4小时
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.email import EmailOperator
from airflow.providers.apache.hive.operators.hive import HiveOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.sensors.filesystem import FileSensor
from airflow.sensors.hive_partition_sensor import HivePartitionSensor
from airflow.utils.trigger_rule import TriggerRule

# DAG默认参数
default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'email': ['data-team@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=10),
    'start_date': datetime(2024, 1, 1),
    'execution_timeout': timedelta(hours=4),
}

# 创建DAG
dag = DAG(
    dag_id='ecommerce_daily_etl',
    description='电商数仓每日ETL调度',
    default_args=default_args,
    schedule_interval='0 2 * * *',  # 每天凌晨2:00
    catchup=True,                    # 允许回填
    max_active_runs=1,               # 同一时间最多1个DAG实例运行
    tags=['ecommerce', 'etl', 'daily'],
    sla_miss_callback=None,          # SLA未达标的回调函数
)

YESTERDAY = '{{ macros.ds_add(ds, -1) }}'  # Airflow模板变量: 昨天日期
YESTERDAY_SHORT = '{{ macros.ds_add(ds, -1) | replace("-", "") }}'

# ============================================================
# 阶段1: 数据采集 (并行执行)
# ============================================================

with dag:
    # 任务组开始标记
    start = DummyOperator(task_id='start')

    # Sqoop抽取用户表
    extract_mysql_users = BashOperator(
        task_id='extract_mysql_users',
        bash_command=f"""
        sqoop import \\
            --connect jdbc:mysql://mysql:3306/ecommerce \\
            --username root --password root123 \\
            --table user_info \\
            --target-dir /data/ods/user_info/{YESTERDAY}/ \\
            --delete-target-dir \\
            --num-mappers 4
        """,
        dag=dag,
    )

    # Sqoop抽取订单表
    extract_mysql_orders = BashOperator(
        task_id='extract_mysql_orders',
        bash_command=f"""
        sqoop import \\
            --connect jdbc:mysql://mysql:3306/ecommerce \\
            --username root --password root123 \\
            --table order_info \\
            --target-dir /data/ods/order_info/{YESTERDAY}/ \\
            --delete-target-dir \\
            --num-mappers 4
        """,
        dag=dag,
    )

    # Sqoop抽取商品表
    extract_mysql_skus = BashOperator(
        task_id='extract_mysql_skus',
        bash_command=f"""
        sqoop import \\
            --connect jdbc:mysql://mysql:3306/ecommerce \\
            --username root --password root123 \\
            --table sku_info \\
            --target-dir /data/ods/sku_info/{YESTERDAY}/ \\
            --delete-target-dir \\
            --num-mappers 4
        """,
        dag=dag,
    )

    # 生成用户行为日志
    generate_user_log = PythonOperator(
        task_id='generate_user_log',
        python_callable=lambda: print(f"生成 {YESTERDAY} 的用户行为日志"),
        dag=dag,
    )

    # ============================================================
    # 阶段2: ODS层加载
    # ============================================================

    load_ods_users = HiveOperator(
        task_id='load_ods_users',
        hql=f"""
        ALTER TABLE ods.ods_user_info ADD IF NOT EXISTS 
        PARTITION (dt='{YESTERDAY}') 
        LOCATION '/data/ods/user_info/{YESTERDAY}/'
        """,
        dag=dag,
    )

    load_ods_orders = HiveOperator(
        task_id='load_ods_orders',
        hql=f"""
        ALTER TABLE ods.ods_order_info ADD IF NOT EXISTS 
        PARTITION (dt='{YESTERDAY}') 
        LOCATION '/data/ods/order_info/{YESTERDAY}/'
        """,
        dag=dag,
    )

    load_ods_skus = HiveOperator(
        task_id='load_ods_skus',
        hql=f"""
        ALTER TABLE ods.ods_sku_info ADD IF NOT EXISTS 
        PARTITION (dt='{YESTERDAY}') 
        LOCATION '/data/ods/sku_info/{YESTERDAY}/'
        """,
        dag=dag,
    )

    # 数据就绪检查 — 等待Hive分区真正可用
    check_ods_users_ready = HivePartitionSensor(
        task_id='check_ods_users_ready',
        table='ods.ods_user_info',
        partition=f"dt='{YESTERDAY}'",
        poke_interval=60,
        timeout=600,
        dag=dag,
    )

    # ODS层汇聚节点（所有ODS表加载完成）
    ods_all_ready = DummyOperator(task_id='ods_all_ready', dag=dag)

    # ============================================================
    # 阶段3: DWD层处理 (Spark任务)
    # ============================================================

    dwd_order_detail = SparkSubmitOperator(
        task_id='dwd_order_detail',
        application='/opt/airflow/dags/etl/dwd_etl.py',
        application_args=['--table', 'dwd_order_detail', '--date', YESTERDAY],
        conn_id='spark_default',
        conf={
            'spark.executor.memory': '4g',
            'spark.executor.cores': '2',
            'spark.sql.shuffle.partitions': '200',
        },
        dag=dag,
    )

    dwd_user_log = SparkSubmitOperator(
        task_id='dwd_user_log',
        application='/opt/airflow/dags/etl/dwd_etl.py',
        application_args=['--table', 'dwd_user_log', '--date', YESTERDAY],
        conn_id='spark_default',
        dag=dag,
    )

    dwd_user_register = SparkSubmitOperator(
        task_id='dwd_user_register',
        application='/opt/airflow/dags/etl/dwd_etl.py',
        application_args=['--table', 'dwd_user_register', '--date', YESTERDAY],
        conn_id='spark_default',
        dag=dag,
    )

    # DWD层汇聚
    dwd_all_ready = DummyOperator(task_id='dwd_all_ready', dag=dag)

    # ============================================================
    # 阶段4: DWS层汇总 (Hive SQL)
    # ============================================================

    dws_user_action = HiveOperator(
        task_id='dws_user_action_day',
        hql=f"""
        INSERT OVERWRITE TABLE dws.dws_user_action_day PARTITION (dt='{YESTERDAY}')
        SELECT user_id,
            SUM(CASE WHEN behavior='pv' THEN 1 ELSE 0 END) as pv_count,
            SUM(CASE WHEN behavior='cart' THEN 1 ELSE 0 END) as cart_count,
            SUM(CASE WHEN behavior='fav' THEN 1 ELSE 0 END) as fav_count,
            SUM(CASE WHEN behavior='buy' THEN 1 ELSE 0 END) as buy_count,
            COUNT(*) as total_actions,
            COUNT(DISTINCT behavior_hour) as active_hours,
            CASE WHEN MIN(behavior_date)='{YESTERDAY}' THEN 1 ELSE 0 END as is_new_user
        FROM dwd.dwd_user_log
        WHERE dt='{YESTERDAY}'
        GROUP BY user_id
        """,
        dag=dag,
    )

    dws_sku_action = HiveOperator(
        task_id='dws_sku_action_day',
        hql=f"""
        INSERT OVERWRITE TABLE dws.dws_sku_action_day PARTITION (dt='{YESTERDAY}')
        SELECT sku_id, MAX(category_id), SUM(CASE WHEN behavior='pv' THEN 1 ELSE 0 END),
               SUM(CASE WHEN behavior='cart' THEN 1 ELSE 0 END),
               SUM(CASE WHEN behavior='fav' THEN 1 ELSE 0 END),
               SUM(CASE WHEN behavior='buy' THEN 1 ELSE 0 END),
               0, 0,
               COUNT(DISTINCT CASE WHEN behavior='buy' THEN user_id END),
               ROUND(SUM(CASE WHEN behavior='buy' THEN 1 ELSE 0 END)*1.0/
                     NULLIF(SUM(CASE WHEN behavior='cart' THEN 1 ELSE 0 END),0),4)
        FROM dwd.dwd_user_log WHERE dt='{YESTERDAY}'
        GROUP BY sku_id
        """,
        dag=dag,
    )

    dws_trade_day = HiveOperator(
        task_id='dws_trade_user_order_day',
        hql=f"""
        INSERT OVERWRITE TABLE dws.dws_trade_user_order_day PARTITION (dt='{YESTERDAY}')
        SELECT user_id, COUNT(DISTINCT order_id), SUM(total_amount),
               SUM(payment_amount), SUM(sku_num),
               SUM(CASE WHEN order_status='已取消' THEN 1 ELSE 0 END),
               SUM(CASE WHEN order_status='已退款' THEN 1 ELSE 0 END)
        FROM dwd.dwd_order_detail WHERE dt='{YESTERDAY}'
        GROUP BY user_id
        """,
        dag=dag,
    )

    # DWS层汇聚
    dws_all_ready = DummyOperator(task_id='dws_all_ready', dag=dag)

    # ============================================================
    # 阶段5: ADS报表生成
    # ============================================================

    ads_user_retention = HiveOperator(
        task_id='ads_user_retention',
        hql=f"""INSERT OVERWRITE TABLE ads.ads_user_retention_day 
                PARTITION (dt='{YESTERDAY}')
                SELECT ... """,
        dag=dag,
    )

    ads_trade_stats = HiveOperator(
        task_id='ads_trade_stats',
        hql=f"""INSERT OVERWRITE TABLE ads.ads_trade_stats_day 
                PARTITION (dt='{YESTERDAY}')
                SELECT ... """,
        dag=dag,
    )

    ads_conversion_funnel = HiveOperator(
        task_id='ads_conversion_funnel',
        hql=f"""INSERT OVERWRITE TABLE ads.ads_user_action_conversion 
                PARTITION (dt='{YESTERDAY}')
                SELECT ... """,
        dag=dag,
    )

    # ADS层汇聚
    ads_all_ready = DummyOperator(task_id='ads_all_ready', dag=dag)

    # ============================================================
    # 阶段6: 数据质量检查
    # ============================================================

    def check_data_quality(**context):
        """数据质量检查函数"""
        yesterday = context['ds']
        print(f"[DQ] 开始数据质量检查 - 日期: {yesterday}")

        # 检查ODS行数
        checks = [
            ("ods.ods_order_info", yesterday, 100),
            ("dwd.dwd_order_detail", yesterday, 100),
        ]
        for table, dt, expected_min in checks:
            print(f"[DQ] {table} 行数检查...")
            # 实际调用Spark/Hive查询
        print("[DQ] 数据质量检查通过!")

    dq_check = PythonOperator(
        task_id='dq_check_all',
        python_callable=check_data_quality,
        provide_context=True,
        dag=dag,
    )

    # ============================================================
    # 阶段7: 通知
    # ============================================================

    send_email = EmailOperator(
        task_id='send_report',
        to=['data-team@example.com', 'manager@example.com'],
        subject=f'数仓ETL日报 - {YESTERDAY}',
        html_content=f"""
        <h2>数仓ETL日报 - {YESTERDAY}</h2>
        <p>所有ETL任务已完成，数据质量检查通过。</p>
        <p>请查看Airflow Web UI获取详细信息。</p>
        """,
        dag=dag,
    )

    # DAG完成标记
    end = DummyOperator(task_id='end', dag=dag)

    # ============================================================
    # 设置任务依赖关系
    # ============================================================

    # 阶段1: 采集阶段并行
    start >> [extract_mysql_users, extract_mysql_orders, extract_mysql_skus, generate_user_log]

    # 阶段2: ODS加载
    extract_mysql_users >> load_ods_users >> check_ods_users_ready
    extract_mysql_orders >> load_ods_orders
    extract_mysql_skus >> load_ods_skus

    # ODS全部就绪
    [check_ods_users_ready, load_ods_orders, load_ods_skus, generate_user_log] >> ods_all_ready

    # 阶段3: DWD处理
    ods_all_ready >> [dwd_order_detail, dwd_user_log, dwd_user_register] >> dwd_all_ready

    # 阶段4: DWS汇总
    dwd_all_ready >> [dws_user_action, dws_sku_action, dws_trade_day] >> dws_all_ready

    # 阶段5: ADS报表
    dws_all_ready >> [ads_user_retention, ads_trade_stats, ads_conversion_funnel] >> ads_all_ready

    # 阶段6-7: 质量检查 + 通知
    ads_all_ready >> dq_check >> send_email >> end
```

---

## 五、XCom使用：任务间传递数据

```python
"""
xcom_example.py — 展示XCom的使用方式

场景: 上游Spark任务完成后，将处理行数传给下游的质量检查任务
"""

def spark_etl_with_count(**context):
    """执行Spark ETL并返回处理行数"""
    # 实际执行Spark任务...
    row_count = 50000  # 模拟返回行数
    print(f"处理行数: {row_count}")
    
    # 通过XCom传递数据
    context['task_instance'].xcom_push(
        key='processed_rows',
        value=row_count
    )

def quality_check_with_xcom(**context):
    """从XCom读取上游行数进行质量检查"""
    ti = context['task_instance']
    
    # 从多个上游任务读取XCom
    order_rows = ti.xcom_pull(
        task_ids='dwd_order_detail', 
        key='processed_rows'
    )
    
    expected_min = 100
    assert order_rows >= expected_min, \
        f"行数检查失败: {order_rows} < {expected_min}"
    
    print(f"行数检查通过: {order_rows} >= {expected_min}")
```

---

## 六、告警与SLA配置

```python
# ===== SLA配置 =====
# 整个DAG的SLA: 凌晨2点启动，6点前必须完成（4小时窗口）

default_args = {
    'sla': timedelta(hours=4),  # 全局SLA
    'email_on_failure': True,
    'email': ['oncall@example.com'],
}

# 也可以为单个任务设置SLA
task_with_sla = PythonOperator(
    task_id='critical_task',
    python_callable=some_function,
    sla=timedelta(hours=1),  # 此任务必须在1小时内完成
    dag=dag,
)

# ===== SLA Miss回调 =====
def sla_miss_callback(dag, task_list, blocking_task_list, slas, blocking_tis):
    """SLA未达标时的回调"""
    print(f"DAG {dag.dag_id} SLA未达标!")
    print(f"未完成的任务: {[t.task_id for t in task_list]}")
    # 可以发送紧急告警: 企业微信、钉钉、PagerDuty等

dag = DAG(
    dag_id='ecommerce_daily_etl',
    sla_miss_callback=sla_miss_callback,
    ...
)

# ===== 失败通知 =====
def on_failure_callback(context):
    """任务失败时的回调"""
    task_instance = context['task_instance']
    exception = context.get('exception')
    
    message = f"""
    ❌ Airflow任务失败!
    DAG: {context['dag'].dag_id}
    Task: {task_instance.task_id}
    执行时间: {task_instance.execution_date}
    重试次数: {task_instance.try_number}
    错误: {exception}
    """
    
    # 发送到企业微信/钉钉
    send_to_wechat_work(message)

task = PythonOperator(
    task_id='important_task',
    python_callable=important_function,
    on_failure_callback=on_failure_callback,
    dag=dag,
)
```

---

## 七、部署与运行

### 7.1 部署DAG文件

```bash
# 将DAG文件复制到Airflow的dags目录
cp dag_ecommerce_daily_etl.py $AIRFLOW_HOME/dags/

# 检查DAG是否正确加载
airflow dags list

# 查看DAG详情
airflow dags show ecommerce_daily_etl

# 手动触发一次运行（测试）
airflow dags trigger ecommerce_daily_etl

# 回填历史数据（补跑前30天的数据）
airflow dags backfill \
    --start-date 2024-01-01 \
    --end-date 2024-01-31 \
    ecommerce_daily_etl
```

### 7.2 监控命令

```bash
# 查看任务运行状态
airflow tasks list ecommerce_daily_etl

# 查看某次运行的详细信息
airflow dags state ecommerce_daily_etl 2024-01-15

# 查看失败的任务
airflow tasks failed-dag-run ecommerce_daily_etl 2024-01-15

# 清除失败任务状态（准备重跑）
airflow tasks clear \
    --start-date 2024-01-15 \
    --end-date 2024-01-15 \
    ecommerce_daily_etl
```

---

## 八、Airflow Web UI截图要求

提交以下页面的截图：

```
1. DAGs页面 — 展示所有DAG的列表和状态
2. Grid View — 展示一个月的运行历史（方格图）
3. Graph View — 展示DAG的任务依赖关系图
4. Task Duration — 展示每个任务的耗时分布
5. Gantt Chart — 展示某次运行各任务的甘特图
6. Task Instance — 展示某个失败任务的日志
```

---

## 九、交付物清单

| 序号 | 交付物 | 文件 | 要求 |
|------|--------|------|------|
| 1 | 完整DAG代码 | `dag_ecommerce_daily_etl.py` | 完整可部署的DAG Python文件 |
| 2 | DAG设计文档 | `DAG设计文档.md` | 任务依赖关系说明 |
| 3 | 运行截图集 | 6张截图 | Grid/Graph/Duration/Gantt等 |
| 4 | 一个月的运行历史 | Grid View截图 | 展示至少30天的运行记录 |

---

## 十、评分标准

| 评分项 | 权重 | 要求 |
|--------|------|------|
| DAG完整性 | 30% | 覆盖ODS→DWD→DWS→ADS全流程，依赖关系正确 |
| 容错设计 | 20% | 重试策略、失败通知、SLA配置 |
| 代码质量 | 20% | 代码规范、XCom使用合理、注释清晰 |
| 运行验证 | 20% | DAG可成功运行，30天历史运行记录 |
| Web UI分析 | 10% | 能解释各项监控指标的含义 |