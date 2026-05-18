# 大数据技术全栈课件：从初学者到CTO

> **课件定位**：面向零基础学员，通过"螺旋式上升"教学法，6个阶段24个月，将学员培养至CTO级别技术视野。
>
> **核心教学理念**：不做PPT讲师，做项目教练。每个技术点按照"感性认识→动手搭建→原理深挖→实战项目"四步走。

---

## 课件总览

| 阶段 | 名称 | 周期 | 课时 | 项目数 | 目标角色 |
|------|------|------|------|--------|----------|
| L0 | 预备阶段：编程基本功 | 8周 | 160h | 3 | 编程入门 |
| L1 | 初级工程师：大数据入门 | 12周 | 240h | 3 | 大数据初级工程师 |
| L2 | 中级工程师：工程深化 | 16周 | 320h | 4 | 大数据中级工程师 |
| L3 | 高级工程师：技术深度 | 20周 | 400h | 2 | 大数据高级工程师 |
| L4 | 架构师：全局设计 | 24周 | 480h | 3 | 数据架构师 |
| L5 | CTO视野：战略领导 | 持续 | 按需 | 1 | CTO/技术VP |

> **总课时**：约1600小时面授 + 2000小时自学，按每天8小时计算约24个月。

---

# L0 预备阶段：编程基本功

## 阶段目标
学员结业时能够：独立使用Python进行数据处理；熟练编写中等复杂的SQL查询；在纯命令行环境下管理Linux服务器；使用Git进行日常代码版本管理。

---

## 第1周：Python基础（一）

### 课时1：开发环境搭建（2h）

**教学内容**：
1. Python解释器安装（Anaconda发行版）
2. VS Code安装与Python插件配置
3. 虚拟环境创建（conda create）
4. 第一个Python程序：`print("Hello, Big Data")`
5. Jupyter Notebook基本使用

**课堂练习**（30min）：
```python
# 练习：创建一个虚拟环境并运行以下代码
import sys
print(f"Python版本: {sys.version}")
print(f"运行平台: {sys.platform}")

# 安装numpy并验证
import numpy as np
arr = np.arange(10)
print(f"numpy数组: {arr}")
```

**课后作业**：
- 在GitHub创建仓库 `big-data-journey`
- 提交第一份代码：环境验证脚本，包含README.md说明运行方式

---

### 课时2：数据类型与控制流（3h）

**教学内容**：
1. 基本数据类型：int、float、str、bool
2. 容器类型：list、tuple、dict、set
3. 条件判断：if-elif-else
4. 循环：for、while、列表推导式
5. 函数定义：def、参数、返回值

**代码示例**：
```python
# 用列表推导式处理数据——大数据工程师日常操作
log_lines = [
    "192.168.1.1 - GET /index.html 200",
    "192.168.1.2 - POST /login 401",
    "192.168.1.1 - GET /api/users 200",
    "192.168.1.3 - GET /index.html 500",
]

# 统计每个IP的请求次数
from collections import Counter
ips = [line.split()[0] for line in log_lines]
ip_counts = Counter(ips)
print(ip_counts)

# 过滤出错误请求（状态码不是200）
errors = [line for line in log_lines if not line.endswith("200")]
print(f"错误请求: {errors}")
```

**课堂练习**（45min）：
```python
# 练习：不使用Counter，手写代码统计IP出现次数
# 要求：只使用字典和循环
log_lines = [...]  # 同上
# TODO: 你的代码
```

**课后作业**：
- 完成LeetCode数组类题目 5 道（Two Sum, Contains Duplicate等）
- 提交代码到GitHub

---

### 课时3：文件操作与异常处理（2h）

**教学内容**：
1. 文件读写：open、read、write、with语句
2. CSV文件处理：csv模块
3. JSON文件处理：json模块
4. 异常处理：try-except-finally
5. 上下文管理器原理

**实战代码**：
```python
# 模拟数据工程师日常：读取CSV，清洗，写入
import csv
import json

def clean_csv(input_file, output_file):
    """清洗CSV文件：去空行、去重复、标准化格式"""
    seen = set()
    cleaned = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 跳过空行
            if not any(row.values()):
                continue
            # 去重（以ID为准）
            if row['id'] in seen:
                continue
            seen.add(row['id'])
            # 标准化：去除两端空格
            row = {k: v.strip() for k, v in row.items()}
            cleaned.append(row)
    
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=cleaned[0].keys())
        writer.writeheader()
        writer.writerows(cleaned)
    
    # 同时输出JSON版本（大数据生态常用格式）
    with open(output_file.replace('.csv', '.json'), 'w') as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)
    
    return len(cleaned)
```

**课后作业**：
- 自己生成包含1000行的模拟订单CSV文件（含空行和重复数据）
- 运行clean_csv并提交清理前后的文件到GitHub

---

## 第2周：Python基础（二）

### 课时4：面向对象与模块化（3h）

**教学内容**：
1. 类与对象：class、__init__、self
2. 继承与多态
3. 模块导入：import、from...import
4. 包管理：pip、requirements.txt
5. 常用标准库：datetime、os、pathlib、logging

**实战代码——构建一个数据处理基类**：
```python
import logging
from pathlib import Path
from abc import ABC, abstractmethod

class DataProcessor(ABC):
    """数据处理基类——所有ETL任务的模板"""
    
    def __init__(self, name):
        self.name = name
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')
        )
        logger.addHandler(handler)
        return logger
    
    @abstractmethod
    def extract(self, source):
        """从数据源提取数据"""
        pass
    
    @abstractmethod
    def transform(self, data):
        """转换数据"""
        pass
    
    @abstractmethod
    def load(self, data, target):
        """加载数据到目标"""
        pass
    
    def run(self, source, target):
        """执行完整ETL流程"""
        self.logger.info(f"开始ETL任务: {self.name}")
        try:
            raw = self.extract(source)
            self.logger.info(f"提取完成: {len(raw)} 行")
            cleaned = self.transform(raw)
            self.logger.info(f"转换完成: {len(cleaned)} 行")
            self.load(cleaned, target)
            self.logger.info(f"加载完成: {target}")
            return True
        except Exception as e:
            self.logger.error(f"ETL失败: {e}")
            return False
```

**课后作业**：
- 继承DataProcessor基类，实现一个CSV转JSON的ETL处理器
- 要求：添加进度条（tqdm）、记录运行耗时

---

### 课时5：Python数据处理三板斧（3h）

**教学内容**：
1. 内置函数高级用法：map、filter、reduce、zip、enumerate
2. itertools模块：常用迭代器
3. collections模块：Counter、defaultdict、OrderedDict
4. 正则表达式：re模块（重点：日志解析）
5. 函数式编程思维

**重点示例——Nginx日志解析器**：
```python
import re
from collections import defaultdict
from datetime import datetime

class NginxLogParser:
    """Nginx日志解析——大数据工程师面试必考"""
    
    LOG_PATTERN = re.compile(
        r'(?P<ip>\S+)\s+\S+\s+\S+\s+'
        r'\[(?P<time>[^\]]+)\]\s+'
        r'"(?P<method>\S+)\s+(?P<url>\S+)\s+\S+"\s+'
        r'(?P<status>\d+)\s+'
        r'(?P<size>\d+)\s+'
        r'"(?P<referer>[^"]*)"\s+'
        r'"(?P<ua>[^"]*)"'
    )
    
    def parse_line(self, line):
        match = self.LOG_PATTERN.match(line)
        if not match:
            return None
        return match.groupdict()
    
    def parse_file(self, filepath):
        records = []
        with open(filepath, 'r') as f:
            for line in f:
                record = self.parse_line(line.strip())
                if record:
                    records.append(record)
        return records
    
    def analyze(self, records):
        """分析日志——输出报告"""
        stats = {
            'total_requests': len(records),
            'unique_ips': len(set(r['ip'] for r in records)),
            'status_distribution': defaultdict(int),
            'top_urls': defaultdict(int),
            'requests_per_hour': defaultdict(int),
        }
        for r in records:
            stats['status_distribution'][r['status']] += 1
            stats['top_urls'][r['url']] += 1
            hour = r['time'].split(':')[1]  # 提取小时
            stats['requests_per_hour'][hour] += 1
        
        return stats

# 使用示例
parser = NginxLogParser()
logs = parser.parse_file('access.log')
report = parser.analyze(logs)

print(f"总请求数: {report['total_requests']}")
print(f"独立IP数: {report['unique_ips']}")
print(f"状态码分布: {dict(report['status_distribution'])}")
print(f"TOP5 URL: {sorted(report['top_urls'].items(), key=lambda x: -x[1])[:5]}")
```

**课堂练习**（45min）：
- 生成包含100行模拟Nginx日志的文件
- 用NginxLogParser解析并输出分析报告

**课后作业**：
- 增强NginxLogParser：添加慢请求检测（响应大小>1MB的标记为慢请求）
- 支持从gzip压缩文件中读取日志

---

## 第3周：SQL深度训练

### 课时6：关系型数据库基础（3h）

**教学内容**：
1. 数据库核心概念：表、行、列、主键、外键、索引
2. MySQL安装与基本操作
3. CRUD操作：INSERT、SELECT、UPDATE、DELETE
4. WHERE条件筛选、ORDER BY排序、LIMIT分页
5. 数据类型理解与选择

**动手任务——搭建练习环境**：
```sql
-- 创建电商数据库
CREATE DATABASE ecommerce;
USE ecommerce;

-- 用户表
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    city VARCHAR(50),
    registered_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 商品表
CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(200) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10, 2),
    stock INT DEFAULT 0
);

-- 订单表
CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2),
    status VARCHAR(20) DEFAULT 'pending',
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- 订单明细表
CREATE TABLE order_items (
    item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10, 2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
```

**课堂练习**：
- 插入1000条模拟数据（用Python脚本批量生成INSERT语句）
- 基础查询练习：筛选、排序、分页

---

### 课时7：SQL核心——多表查询（3h）

**教学内容**：
1. JOIN全家桶：INNER JOIN、LEFT JOIN、RIGHT JOIN、FULL JOIN、CROSS JOIN
2. 自连接与子查询
3. UNION与UNION ALL
4. GROUP BY与聚合函数（COUNT/SUM/AVG/MAX/MIN）
5. HAVING vs WHERE的区别

**关键示例——电商分析核心查询**：
```sql
-- 查询1：各城市的用户消费TOP5（面试高频题）
SELECT 
    u.city,
    COUNT(DISTINCT o.user_id) AS user_count,
    COUNT(o.order_id) AS order_count,
    ROUND(SUM(o.total_amount), 2) AS total_revenue,
    ROUND(AVG(o.total_amount), 2) AS avg_order_value
FROM users u
INNER JOIN orders o ON u.user_id = o.user_id
WHERE o.status = 'completed'
GROUP BY u.city
ORDER BY total_revenue DESC
LIMIT 5;

-- 查询2：找出"沉默用户"（注册超过30天但从未下单）
SELECT u.user_id, u.username, u.registered_at
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
WHERE o.order_id IS NULL
  AND u.registered_at < DATE_SUB(NOW(), INTERVAL 30 DAY);

-- 查询3：商品的连带购买分析（买了A也买了B）
SELECT 
    oi1.product_id AS product_a,
    oi2.product_id AS product_b,
    COUNT(DISTINCT oi1.order_id) AS co_purchase_count
FROM order_items oi1
INNER JOIN order_items oi2 
    ON oi1.order_id = oi2.order_id 
    AND oi1.product_id < oi2.product_id
GROUP BY oi1.product_id, oi2.product_id
HAVING co_purchase_count >= 5
ORDER BY co_purchase_count DESC;
```

**课后作业**：
- 生成10000行模拟电商数据
- 完成10道SQL练习题（涵盖所有JOIN类型 + 子查询 + GROUP BY）

---

### 课时8：SQL进阶——窗口函数（3h）

**教学内容**：
1. 窗口函数概念：PARTITION BY vs GROUP BY的区别
2. 排名函数：ROW_NUMBER、RANK、DENSE_RANK、NTILE
3. 偏移函数：LAG、LEAD
4. 聚合窗口：SUM/AVG OVER
5. 累积统计：移动平均、累计求和

**重点示例——窗口函数实战**：
```sql
-- 查询1：每个品类价格排名前3的商品
SELECT * FROM (
    SELECT 
        product_name,
        category,
        price,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY price DESC) AS rank_in_category
    FROM products
) ranked
WHERE rank_in_category <= 3;

-- 查询2：用户连续下单天数（留存分析核心）
WITH daily_orders AS (
    SELECT 
        user_id,
        DATE(order_date) AS order_day,
        LAG(DATE(order_date)) OVER (PARTITION BY user_id ORDER BY DATE(order_date)) AS prev_day
    FROM orders
)
SELECT 
    user_id,
    order_day,
    DATEDIFF(order_day, prev_day) AS days_since_last_order
FROM daily_orders
WHERE prev_day IS NOT NULL;

-- 查询3：每月销售额环比增长率
WITH monthly_revenue AS (
    SELECT 
        DATE_FORMAT(order_date, '%Y-%m') AS month,
        SUM(total_amount) AS revenue
    FROM orders
    WHERE status = 'completed'
    GROUP BY DATE_FORMAT(order_date, '%Y-%m')
)
SELECT 
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY month) AS prev_month_revenue,
    ROUND((revenue - LAG(revenue) OVER (ORDER BY month)) / LAG(revenue) OVER (ORDER BY month) * 100, 2) AS growth_rate
FROM monthly_revenue;
```

**课后作业（本周核心考核）**：
- LeetCode SQL题库完成50道（重点：排名类、连续类、累计类）
- 窗口函数专项：务必手写理解每一个PARTITION BY和ORDER BY的作用

---

## 第4周：Linux与Git实战

### 课时9：Linux核心命令（3h）

**教学内容**：
1. 文件系统导航：cd、ls、pwd、mkdir、rm、cp、mv
2. 文件查看与处理：cat、less、head、tail、grep、awk、sed
3. 权限管理：chmod、chown、umask
4. 进程管理：ps、top、kill、nohup、&
5. 磁盘与网络：df、du、netstat、curl、wget

**重点训练——用awk/sed处理百万行日志**：
```bash
# 场景：生产环境100万行Nginx日志，需要快速分析

# 1. 统计每个HTTP状态码的数量
awk '{print $9}' access.log | sort | uniq -c | sort -rn

# 2. 找出响应时间超过1秒的慢请求
awk '$NF > 1 {print $0}' access.log > slow_requests.log

# 3. 统计每分钟的QPS
awk '{print substr($4,2,17)}' access.log | uniq -c

# 4. 提取TOP 10 IP并统计请求数
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -10

# 5. 替换配置文件中的端口号
sed -i 's/port=8080/port=9090/g' application.conf

# 6. 找出包含ERROR且不包含IGNORE的行
grep ERROR application.log | grep -v IGNORE
```

**课堂练习**（45min）：
- 教师提供1万行模拟Nginx日志
- 学员用命令行完成：统计状态码分布、TOP10 IP、每分钟QPS变化趋势
- **禁止使用Python，只能用bash命令**

**课后作业**：
- 搭建Ubuntu Server虚拟机（VirtualBox + 最小化安装）
- 纯命令行环境完成：安装MySQL、创建数据库、导入数据、执行SQL查询

---

### 课时10：Git核心工作流（3h）

**教学内容**：
1. Git三区概念：工作区、暂存区、版本库
2. 核心操作：clone、add、commit、push、pull、fetch
3. 分支管理：branch、checkout、merge、rebase
4. 历史查看：log、diff、show、blame
5. 撤销操作：reset、revert、checkout --

**实战模拟——团队协作工作流**：
```bash
# 场景：模拟3人团队协作开发

# 开发者A：创建项目并提交
git init big-data-project
echo "# Big Data Project" > README.md
git add README.md
git commit -m "docs: 初始化项目文档"
git branch -M main
git remote add origin <repo-url>
git push -u origin main

# 开发者A：创建feature分支开发
git checkout -b feature/add-log-parser
echo "print('log parser')" > log_parser.py
git add log_parser.py
git commit -m "feat: 添加日志解析器"
git push origin feature/add-log-parser

# 开发者B：clone项目，创建另一个feature分支
git clone <repo-url>
git checkout -b feature/add-csv-cleaner
echo "print('csv cleaner')" > csv_cleaner.py
git add csv_cleaner.py
git commit -m "feat: 添加CSV清洗器"

# 开发者B：拉取A的最新代码后push
git fetch origin
git rebase origin/main
git push origin feature/add-csv-cleaner

# 代码审查通过后合并到main（在GitHub上操作PR merge）

# 开发者A：更新本地main分支
git checkout main
git pull origin main
```

**课堂练习**（30min）：
- 两人一组，各自创建feature分支
- 故意制造merge conflict并手动解决
- 要求：使用git log --graph --all查看完整的分支树

**课后作业（本周核心考核）**：
- GitHub绿点连续7天
- 至少产生3次PR（可以是对自己仓库的）
- 至少解决一次merge conflict

---

## 第5-6周：L0项目实战

### 项目1：Web日志分析系统（15h）

**项目描述**：构建一个完整的Web日志采集与分析系统，从数据生成到最终输出分析报告。

**项目需求**：

```yaml
阶段1 - 数据生成（3h）:
  编写Python脚本生成模拟日志:
    - 生成100万行Nginx访问日志
    - 模拟7天的数据，包含真实的时间分布（白天多，凌晨少）
    - IP地址模拟: 生成1000个不同IP，部分IP高频访问
    - URL模拟: 20个不同页面，符合长尾分布（80%访问集中在5个页面）
    - 状态码分布: 200(80%), 301(5%), 404(10%), 500(5%)
    - 响应时间: 符合对数正态分布，中位数200ms

阶段2 - 日志解析（4h）:
  用Python解析生成的文件:
    - 正则表达式提取每条日志的字段
    - 异常处理: 处理格式错误的行
    - 输出结构化数据（CSV + JSON两种格式）

阶段3 - 数据分析（5h）:
  统计分析:
    - 每日/每小时PV/UV
    - 每个URL的访问量排名
    - HTTP状态码分布
    - 独立IP TOP 20
    - 平均响应时间趋势
    - 流量突增检测（某小时PV超过前24小时均值的2倍）

阶段4 - 报告生成（3h）:
  生成Markdown格式的分析报告:
    - 包含上述所有统计结果
    - 使用Python markdown库生成表格
    - 输出到analysis_report.md
```

**交付物**：
1. `log_generator.py` — 日志生成脚本
2. `log_parser.py` — 日志解析脚本
3. `log_analyzer.py` — 数据分析脚本
4. `report_generator.py` — 报告生成脚本
5. `analysis_report.md` — 最终分析报告
6. GitHub仓库完整提交记录

---

### 项目2：电商数据库设计与SQL分析（12h）

**项目描述**：设计电商数据库，生成测试数据，编写30条分析SQL。

**项目需求**：

```yaml
阶段1 - 数据库设计（3h）:
  设计包含以下实体的数据库:
    - users（用户）
    - products（商品，支持多级分类）
    - orders（订单）
    - order_items（订单明细）
    - reviews（评价）
    - user_logs（用户行为日志：浏览/加购/收藏）
  
  要求:
    - 完整的DDL，包含主键、外键、索引
    - 合理的默认值和约束
    - ER图（用Draw.io绘制）

阶段2 - 数据生成（3h）:
  Python脚本批量生成:
    - 10000用户
    - 5000商品（10个品类）
    - 50000订单（时间跨度3个月）
    - 200000订单明细
    - 15000评价
    - 100000用户行为日志

阶段3 - SQL分析集（6h）:
  编写30条SQL，涵盖以下场景:
  
  用户分析（10条）:
    1. 新用户留存率（注册后第1/3/7/30天回访）
    2. 用户生命周期价值(LTV)排名
    3. 高价值用户特征分析（消费TOP 10%的用户画像）
    4. 用户活跃度分层（按月度下单次数）
    5. 流失预警（30天未下单的用户）
    6-10. 自行设计分析维度
  
  商品分析（10条）:
    1. 各品类销售额排名及占比
    2. 商品连带购买Top组合
    3. 高评分商品特征分析
    4. 库存周转率
    5. 长尾商品贡献分析
    6-10. 自行设计分析维度
  
  订单分析（10条）:
    1. 每日/每周/每月GMV趋势
    2. 客单价分布
    3. 复购率趋势
    4. 退款率分析
    5. 各城市/时段订单特征
    6-10. 自行设计分析维度
  
  技术要求:
    - 至少10条SQL使用窗口函数
    - 至少5条SQL使用CTE
    - 至少3条SQL包含子查询
    - 每条SQL必须有注释说明业务含义
```

**交付物**：
1. `schema.sql` — 完整建表语句
2. `er_diagram.png` — ER图
3. `seed_data.py` — 数据生成脚本
4. `analysis_queries.sql` — 30条分析SQL
5. `analysis_results.md` — 每条SQL的结果说明和业务解读

---

### 项目3：命令行环境运维实战（12h）

**项目描述**：完全在命令行环境下完成一系列运维任务。

**项目需求**：

```yaml
任务1 - 环境初始化（2h）:
  - 在VirtualBox中安装Ubuntu Server 22.04
  - 配置静态IP、SSH免密登录
  - 安装常用工具: vim, htop, nginx, mysql-server, python3-pip

任务2 - 服务搭建（4h）:
  - 安装并配置Nginx作为反向代理
  - 安装MySQL，创建数据库和用户
  - 安装Python虚拟环境，部署项目1的日志分析脚本
  - 配置systemd服务，使脚本开机自启

任务3 - 日志与监控（3h）:
  - 配置logrotate管理日志
  - 编写shell脚本监控CPU/内存/磁盘使用率
  - 设置crontab定时执行监控脚本
  - 配置邮件告警（模拟：写入告警日志即可）

任务4 - 脚本自动化（3h）:
  编写bash脚本实现:
  - backup.sh: 每日自动备份MySQL数据库
  - deploy.sh: 一键部署Python项目（git pull + 安装依赖 + 重启服务）
  - health_check.sh: 检查所有服务状态
  - cleanup.sh: 自动清理30天前的日志文件
```

**交付物**：
1. 所有bash脚本文件
2. Nginx/MySQL/systemd配置文件
3. 运维操作手册（记录每一步的命令和注意事项）

---

## L0 结业考核

| 考核项 | 方式 | 通过标准 |
|--------|------|----------|
| Python编码 | 现场编程 | 2小时内完成一个CSV数据清洗脚本 |
| SQL能力 | 现场笔试 | 10道SQL题，涵盖JOIN、子查询、窗口函数，正确率≥80% |
| Linux操作 | 现场实操 | 在SSH终端完成：建用户、安装Nginx、配置开机自启 |
| Git操作 | 现场演示 | 创建分支→commit→push→创建PR→解决conflict |
| 项目答辩 | PPT + 演示 | 项目1-3任选其一，15分钟演示+5分钟问答 |

**GitHub贡献度要求**：L0阶段累计代码提交 ≥ 60次

---

# L1 初级工程师：大数据入门

## 阶段目标
学员结业时能够：搭建Hadoop/Spark/Hive分布式环境；使用MapReduce和Spark完成数据处理；使用Hive进行离线数据分析；理解HDFS和YARN的架构原理。

---

## 第7-8周：Hadoop生态基础

### 课时11：大数据概念与HDFS原理（3h）

**教学内容**：
1. 大数据4V特征与实际案例
2. Google GFS论文核心思想
3. HDFS架构：NameNode、DataNode、SecondaryNameNode
4. 数据块（Block）概念与副本策略
5. HDFS读写数据流程（手绘时序图）
6. 联邦HDFS与高可用架构

**关键原理——HDFS写流程（必背）**：
```
客户端 ──创建文件请求──→ NameNode
                          ↓
                   检查权限/路径合法性
                          ↓
                   返回DataNode列表 (dn1, dn2, dn3)
                          ↓
客户端 ──数据包──→ dn1 ──转发──→ dn2 ──转发──→ dn3
  ↓                    ↓            ↓            ↓
  └──ack──────────────←┘          ←┘           ←┘
                          ↓
                   写入完成确认→ NameNode
```

**实验任务**（2h）：
- Docker Compose部署3节点HDFS集群
- HDFS Shell操作：上传/下载/查看/删除
- 观察数据块分布：`hdfs fsck /path -files -blocks -locations`

**课后作业**：
- HDFS Shell命令30条练习（必须手打，不能复制粘贴）
- 手画HDFS读/写流程图，标注每一步的角色和RPC调用

---

### 课时12：MapReduce原理与实战（3h）

**教学内容**：
1. MapReduce编程模型：分而治之思想
2. Map、Shuffle、Reduce三个阶段详解
3. WordCount源码逐行解读
4. MapReduce优化：Combiner、Partitioner
5. MapReduce vs Spark的思想对比

**核心代码——MapReduce WordCount**：
```java
// 这是每个大数据工程师必须手写过的代码
public class WordCount {
    
    public static class TokenizerMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
        private final static IntWritable one = new IntWritable(1);
        private Text word = new Text();
        
        public void map(LongWritable key, Text value, Context context) {
            String[] tokens = value.toString().split("\\s+");
            for (String token : tokens) {
                word.set(token.toLowerCase());
                context.write(word, one);
            }
        }
    }
    
    public static class IntSumReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
        public void reduce(Text key, Iterable<IntWritable> values, Context context) {
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            context.write(key, new IntWritable(sum));
        }
    }
}
```

**实验任务**（2h）：
- 编译并运行WordCount on HDFS
- 对比：加Combiner vs 不加Combiner的性能差异
- 观察JobHistory Server的Map/Reduce任务执行细节

---

### 课时13：Hive数据仓库入门（3h）

**教学内容**：
1. Hive架构：Metastore + SQL编译器 + 执行引擎
2. HiveQL与SQL的异同
3. 内部表 vs 外部表的区别与使用场景
4. 分区表（Partition）与分桶表（Bucket）
5. 文件格式选择：TextFile、Parquet、ORC对比
6. Hive on Tez/Spark的性能提升原理

**关键操作——分区表实战**：
```sql
-- 创建分区表（大数据建表标准写法）
CREATE EXTERNAL TABLE user_behavior (
    user_id BIGINT,
    item_id BIGINT,
    category_id INT,
    behavior STRING,
    ts BIGINT
)
PARTITIONED BY (dt STRING, hr STRING)
STORED AS PARQUET
LOCATION '/warehouse/user_behavior';

-- 加载分区数据
ALTER TABLE user_behavior ADD PARTITION (dt='2024-01-01', hr='00')
LOCATION '/data/user_behavior/dt=2024-01-01/hr=00';

-- 高效查询（分区裁剪）
SELECT category_id, COUNT(*) as pv
FROM user_behavior
WHERE dt = '2024-01-01'
  AND hr BETWEEN '08' AND '22'
  AND behavior = 'buy'
GROUP BY category_id
ORDER BY pv DESC;
```

**实验任务**：
- 创建Hive表，加载CSV数据
- 对比TextFile vs Parquet的存储空间和查询速度
- 体验分区裁剪的效果（EXPLAIN查看执行计划）

**课后作业**：
- HQL练习题20道（覆盖建表、分区、JOIN、窗口函数、文件格式优化）

---

## 第9-10周：Spark核心

### 课时14：Spark RDD核心原理（3h）

**教学内容**：
1. Spark vs MapReduce：为什么Spark快100倍？
2. RDD（弹性分布式数据集）概念
3. RDD五大特性（必背）：分区列表、计算函数、依赖关系、分区器、优先位置
4. Transformation vs Action：惰性求值
5. 宽依赖 vs 窄依赖：Shuffle的触发条件
6. DAG调度与Stage划分

**核心代码——RDD实战**：
```python
from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName("RDDBasics")
sc = SparkContext(conf=conf)

# 从HDFS读取文本文件
lines = sc.textFile("hdfs://namenode:9000/data/sample.txt")

# 经典WordCount——理解RDD的每一步操作
word_counts = (lines
    .flatMap(lambda line: line.split())       # Transformation(窄依赖)
    .map(lambda word: (word.lower(), 1))       # Transformation(窄依赖)
    .reduceByKey(lambda a, b: a + b)           # Transformation(宽依赖, 触发Shuffle)
    .filter(lambda x: x[1] > 10)               # Transformation(窄依赖)
    .sortBy(lambda x: -x[1])                   # Transformation(宽依赖)
)

# Action——此时才真正执行计算
result = word_counts.collect()
for word, count in result[:20]:
    print(f"{word}: {count}")

# 查看RDD的DAG（非常重要！）
word_counts.toDebugString()
```

**关键理解——手动划分Stage**（课堂板书）：
```
RDD1(textFile) → RDD2(flatMap) → RDD3(map) → RDD4(reduceByKey) → RDD5(filter) → RDD6(sortBy)
        窄依赖        窄依赖        宽依赖(Shuffle)       窄依赖        宽依赖(Shuffle)
Stage0: [RDD1→RDD2→RDD3]      Stage1: [RDD4→RDD5]      Stage2: [RDD6]
```

**课后作业**：
- 用RDD API实现：日志PV/UV统计、Top-N问题、Join操作
- 每个作业都要查看Spark UI并截图记录DAG图

---

### 课时15：Spark SQL与DataFrame（3h）

**教学内容**：
1. DataFrame vs RDD的区别与选择
2. SparkSession统一入口
3. DataFrame API：select、filter、groupBy、join、agg
4. Spark SQL：临时视图 + SQL查询
5. Catalyst优化器简介：逻辑计划→物理计划
6. Encoder与Tungsten项目：堆外内存与代码生成

**核心代码——数据分析实战**：
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import Window

spark = SparkSession.builder \
    .appName("DataAnalysis") \
    .config("spark.sql.adaptive.enabled", "true") \
    .enableHiveSupport() \
    .getOrCreate()

# 读取Parquet文件（生产标准格式）
df = spark.read.parquet("hdfs:///warehouse/user_behavior")

# 用DataFrame API做分析
daily_stats = (df
    .filter(col("behavior") == "buy")
    .groupBy("dt", "category_id")
    .agg(
        count("*").alias("orders"),
        countDistinct("user_id").alias("users"),
        sum("amount").alias("revenue")
    )
    .withColumn("arpu", col("revenue") / col("users"))
    .orderBy("dt", col("revenue").desc())
)

# 窗口函数——用户连续购买天数
user_purchase_days = (df
    .filter(col("behavior") == "buy")
    .select("user_id", "dt")
    .distinct()
)

window_spec = Window.partitionBy("user_id").orderBy("dt")
user_purchase_pattern = user_purchase_days.withColumn(
    "days_since_last",
    datediff(col("dt"), lag("dt").over(window_spec))
)

# 直接用SQL（更直观）
df.createOrReplaceTempView("behavior")
result = spark.sql("""
    SELECT 
        category_id,
        dt,
        COUNT(*) as pv,
        COUNT(DISTINCT user_id) as uv,
        SUM(CASE WHEN behavior = 'buy' THEN 1 ELSE 0 END) as orders
    FROM behavior
    WHERE dt >= '2024-01-01'
    GROUP BY category_id, dt
    ORDER BY dt, pv DESC
""")

# 写入Hive分区表
result.write \
    .mode("overwrite") \
    .partitionBy("dt") \
    .format("parquet") \
    .saveAsTable("category_daily_stats")
```

**课后作业**：
1. 用DataFrame API重写L0项目1的所有分析逻辑（对比Python和Spark的差异）
2. 用Spark SQL完成至少10条分析查询
3. 尝试通过EXPLAIN对比不同写法的执行计划差异

---

### 课时16：Spark性能调优基础（3h）

**教学内容**：
1. 数据倾斜诊断：通过Spark UI查看Task数据量分布
2. 倾斜解决方案：加盐（Salt）、Broadcast Join、调整并行度
3. Shuffle优化：spark.sql.shuffle.partitions、AQE
4. 内存管理：spark.memory.fraction、Cache与Persist策略
5. 序列化：Kryo vs Java序列化

**实战——数据倾斜处理**：
```python
# 场景：某category_id的数据量是其他类别的100倍

# 方案1：加盐打散（适用于groupBy操作）
salt_num = 100
skewed_df = df.withColumn("salt", (rand() * salt_num).cast("int"))

salted_result = skewed_df \
    .groupBy("salt", "category_id") \
    .agg(count("*").alias("cnt")) \
    .groupBy("category_id") \
    .agg(sum("cnt").alias("total_cnt"))

# 方案2：Broadcast Join（小表Join大表）
from pyspark.sql.functions import broadcast

small_df = spark.read.parquet("category_info")  # 1000行
big_df = spark.read.parquet("user_behavior")     # 1亿行

result = big_df.join(broadcast(small_df), "category_id")

# 方案3：AQE自适应查询（Spark 3.0+）
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
```

**课后作业**：
- 故意制造数据倾斜场景，尝试三种方案解决
- 输出对比报告：解决前后的Shuffle数据量、Task耗时分布、总运行时间

---

## 第11-14周：L1项目实战

### 项目4：离线数仓构建（30h）

**项目描述**：从0到1构建一个电商离线数仓，遵循ODS→DWD→DWS→ADS分层架构。

**项目需求**：

```yaml
数据源:
  1. 业务数据库(MySQL): 用户表、商品表、订单表、订单明细
  2. 埋点日志(HDFS): 用户行为日志(浏览/点击/加购/收藏)
  3. 外部数据: 天气数据(简单模拟)

环境要求:
  - HDFS + YARN + Hive + Spark
  - Docker Compose一键启动
  - 模拟3个月的数据，总量约100GB

数仓分层设计:

ODS层（原始数据层）:
  - ods_order_info: 订单主表(每日全量快照)
  - ods_order_detail: 订单明细(增量合并)
  - ods_user_info: 用户信息(每日全量)
  - ods_sku_info: 商品信息(每日全量)
  - ods_user_log: 用户行为日志(按天分区)

DWD层（明细数据层）:
  - dwd_order_detail: 订单明细宽表
    (关联用户、商品信息，增加日期维度字段)
  - dwd_user_log: 用户行为明细(解析埋点数据，标准化)
  - dwd_user_register: 用户注册明细

DWS层（汇总数据层）:
  - dws_user_action_day: 用户日行为汇总
  - dws_sku_action_day: 商品日行为汇总
  - dws_trade_user_order_day: 用户日订单汇总
  - dws_trade_province_order_day: 省份日订单汇总

ADS层（应用数据层）:
  - ads_user_retention_day: 用户留存率报表
  - ads_sku_sales_top10: 商品销量TOP10
  - ads_trade_stats_day: 日交易统计
  - ads_user_action_conversion: 行为转化漏斗

ETL流程:
  每日凌晨2点执行:
  1. Sqoop从MySQL全量抽取订单和用户数据到HDFS
  2. Spark清洗ODS数据生成DWD层宽表
  3. Hive SQL聚合生成DWS层汇总表
  4. Hive SQL生成ADS层应用报表
  5. 数据质量校验(行数检查、空值检查)
```

**技术栈要求**：
- 数据采集：Sqoop + 模拟日志生成器
- 数据存储：HDFS + Hive
- 数据计算：Spark + Hive on Tez
- 任务调度：Airflow（简单用crontab也可以）

**交付物**：
1. 完整的数仓DDL建表语句(包含分区、分桶、存储格式)
2. 各层ETL脚本(Sqoop/Spark/Hive SQL)
3. 数据质量校验脚本
4. 数仓架构文档(包含分层设计理由)
5. 数据字典(每个表的字段说明)
6. 运行结果样例(每层抽样10行数据)

---

### 项目5：Spark用户画像系统（25h）

**项目描述**：基于Spark构建用户画像标签系统，生成用户的360度画像标签。

**项目需求**：

```yaml
标签体系设计:

基础属性标签:
  - 性别(预测)
  - 年龄段(预测)
  - 城市等级(一线/新一线/二线/三线)
  - 会员等级
  - 注册天数

行为偏好标签:
  - 品类偏好(TOP3品类)
  - 价格敏感度(高/中/低)
  - 购物时段偏好(早/中/晚/夜)
  - 购买频次级别(高频/中频/低频)
  - 平均客单价区间

消费能力标签:
  - 消费能力等级(高/中/低)
  - 最近一次消费时间(R)
  - 消费频率(F)
  - 消费金额(M)
  - RFM分值

生命周期标签:
  - 用户生命周期阶段(新客/活跃/沉默/流失)
  - 最近一次访问距今天数
  - 7天活跃度
  - 30天活跃度

技术实现:
  1. Spark读取DWD和DWS层数据
  2. 基于规则和统计生成标签
  3. 输出格式: 每个用户一行，每个标签一列
  4. 存储为Parquet文件(按日期分区)
  5. 建立Hive外部表供查询

高级要求:
  - 标签血缘追踪: 哪个标签由哪个SQL生成
  - 标签覆盖率统计: 每个标签的有值率
  - 增量更新: 只更新有变化的用户标签
```

**交付物**：
1. 标签体系设计文档
2. Spark标签生成脚本
3. 标签覆盖率报告
4. 20个典型用户的完整画像展示

---

### 项目6：Airflow工作流编排（15h）

**项目描述**：用Airflow将所有ETL任务编排为定时执行的DAG。

**项目需求**：

```yaml
DAG设计——电商数仓每日ETL:

Task依赖关系:
  数据抽取阶段:
    task_extract_mysql_users  ──┐
    task_extract_mysql_orders ──┤ 并行执行
    task_extract_mysql_skus   ──┤
    task_generate_user_log    ──┘
           │
           ▼
  ODS加载阶段:
    task_load_ods_all         ← 等待所有抽取完成
           │
           ▼
  DWD处理阶段:
    task_dwd_order_detail ──┐
    task_dwd_user_log     ──┤ 并行执行
    task_dwd_user_register──┘
           │
           ▼
  DWS汇总阶段:
    task_dws_user_action_day ──┐
    task_dws_sku_action_day  ──┤ 按顺序执行
    task_dws_trade_day       ──┘
           │
           ▼
  ADS报表生成:
    task_ads_user_retention
    task_ads_trade_stats
    task_ads_conversion_funnel
           │
           ▼
  数据质量检查:
    task_dq_check_all
           │
           ▼
  告警/通知:
    task_send_report

Airflow配置:
  - 每天凌晨2:00执行
  - 重试策略: 失败重试3次，间隔10分钟
  - 告警: 失败后发送邮件/企业微信通知
  - SLA: 必须在6:00前完成
  - xcom传递: 上一步的记录数传给下一步做校验
```

**交付物**：
1. Airflow DAG Python代码
2. DAG运行截图(Grid View + Task Duration)
3. 一个月的DAG运行历史记录

---

## L1 结业考核

| 考核项 | 方式 | 通过标准 |
|--------|------|----------|
| HDFS原理 | 现场手绘 | 画出读写流程图，标注每个组件的交互 |
| Hive SQL | 现场编码 | 写出分区表建表语句，完成一个JOIN+聚合查询 |
| Spark RDD | 现场编码 | 用RDD API完成WordCount和TopN |
| Spark SQL | 现场编码 | 用DataFrame/SQL完成一次完整的分析 |
| 性能调优 | 案例分析 | 给定倾斜场景，说出3种解决方案 |
| 综合项目 | 答辩+演示 | 项目4/5/6任选其一，20分钟演示+问答 |

---

# L2 中级工程师：工程深化

## 阶段目标
学员结业时能够：独立设计分布式数据管道；理解Kafka核心原理并配置生产级集群；使用Flink进行有状态流处理；理解DDIA核心章节并能应用到实际架构设计；具备生产环境故障排查能力。

---

## 第15-16周：Kafka深入

### 课时17：Kafka架构与核心概念（3h）

**教学内容**：
1. Kafka设计目标：高吞吐、持久化、可回放
2. Topic、Partition、Replica概念
3. Producer发送流程：序列化→分区路由→RecordAccumulator→Sender线程
4. Broker存储机制：Log Segment、Page Cache、零拷贝(sendfile)
5. Consumer Group与Rebalance机制
6. ISR（In-Sync Replicas）与高可用

**关键原理——Kafka高吞吐的秘密（板书）**：
```
传统方式(四次拷贝):
磁盘 → OS Buffer → 应用Buffer → Socket Buffer → 网卡

Kafka零拷贝(sendfile):
磁盘 → OS Buffer ──→ Socket Buffer → 网卡
              └──→ DMA copy(描述信息)
应用层完全不参与数据拷贝！
```

**动手实验**（2h）：
```bash
# Docker Compose部署3节点Kafka集群
# 观察各Broker上的Partition分布

# 创建Topic（3分区 + 3副本）
kafka-topics.sh --create \
  --topic user-events \
  --partitions 3 \
  --replication-factor 3 \
  --bootstrap-server localhost:9092

# Producer压测
kafka-producer-perf-test.sh \
  --topic user-events \
  --num-records 10000000 \
  --record-size 1000 \
  --throughput -1 \
  --producer-props acks=all \
  --bootstrap-server localhost:9092

# Consumer消费（不同Consumer Group对比）
# 组1: 3个Consumer(每个消费1个Partition)
# 组2: 2个Consumer(Consumer1消费2个Partition)
# 观察Rebalance过程
```

**课后作业**：
- 深入阅读《Kafka权威指南》第5-6章（Producer和Broker内部原理）
- 动手：手动Kill一个Broker，观察ISR变化和Leader切换

---

### 课时18：Kafka Exactly-Once与事务（3h）

**教学内容**：
1. 消息投递语义：At-Most-Once、At-Least-Once、Exactly-Once
2. Producer幂等性：PID + Sequence Number
3. Kafka事务：Transaction Coordinator
4. 两阶段提交(2PC)在Kafka中的应用
5. Kafka Streams Exactly-Once实现

**关键理解——Why Exactly-Once is Hard**：
```
场景：Flink从Kafka读数据 → 处理 → 写回Kafka

问题：Checkpoint恢复时可能导致重复写入

Flink两阶段提交方案:
阶段1(PreCommit):
  - Flink做Checkpoint时，Kafka Sink开启事务
  - 将所有数据写入Kafka但标记为"未提交"
  
阶段2(Commit):
  - Checkpoint成功后，提交Kafka事务
  - 数据变为可见
  
如果失败(回滚):
  - Abort Kafka事务，所有"未提交"数据丢弃
  - 从上一个Checkpoint恢复状态，重新消费
```

**课后作业**：
- 编写Producer和Consumer程序
- 对比：acks=0 / acks=1 / acks=all 的性能和可靠性差异
- 事务Producer的实现代码（Java/Python）

---

## 第17-18周：Flink流处理

### 课时19：Flink核心概念（3h）

**教学内容**：
1. Flink vs Spark Streaming的架构差异（真流 vs 微批）
2. DataStream API核心抽象
3. Event Time vs Processing Time vs Ingestion Time
4. Watermark机制：解决乱序数据问题
5. Window类型：Tumbling、Sliding、Session、Global
6. Trigger与Evictor

**核心代码——实时统计PV/UV**：
```java
DataStream<UserBehavior> stream = env
    .addSource(new FlinkKafkaConsumer<>(
        "user-behavior",
        new UserBehaviorSchema(),
        properties
    ))
    .assignTimestampsAndWatermarks(
        WatermarkStrategy
            .<UserBehavior>forBoundedOutOfOrderness(Duration.ofSeconds(5))
            .withTimestampAssigner((event, ts) -> event.getTimestamp())
    );

// 每分钟各品类的PV/UV
DataStream<CategoryStats> stats = stream
    .keyBy(UserBehavior::getCategoryId)
    .window(TumblingEventTimeWindows.of(Time.minutes(1)))
    .aggregate(new PvUvAggregator(), new CategoryStatsWindow());

// 输出到ClickHouse/Kafka
stats.addSink(new ClickHouseSink());
```

**Watermark原理图解（课堂板书）**：
```
时间轴 ──────────────────────────────────────────→
事件    1    3    5    2    4    6    7    8

Watermark = Max(已见EventTime) - 允许延迟

事件1到达: WM=0 (1-5<0, 取0)
事件3到达: WM=0
事件5到达: WM=0
事件2到达: WM=0 (迟到数据不推进WM)
事件4到达: WM=0
事件6到达: WM=1 → 触发时间<WM=1的窗口关闭
事件7到达: WM=2 → 触发更多窗口
...
```

**课后作业**：
- 编写Flink程序：从Kafka读取交易数据，1分钟窗口统计交易量和交易金额
- 故意制造乱序数据，观察Watermark和窗口触发行为

---

### 课时20：Flink Checkpoint与容错（3h）

**教学内容**：
1. Checkpoint机制：Chandy-Lamport算法变体
2. Checkpoint Barrier：如何在流中插入"分隔符"
3. State Backend：HashMapStateBackend vs EmbeddedRocksDBStateBackend
4. Savepoint vs Checkpoint的区别
5. 端到端Exactly-Once：TwoPhaseCommitSinkFunction
6. Checkpoint调优：间隔、超时、并发

**Checkpoint流程详解（必画图）**：
```
                     ┌── Source ──┐
                     │   (Kafka)  │
Checkpoint           │  offset=100│
Coordinator          └────────────┘
    │                      │
    ├─ Inject Barrier 1 ──→│
    │                      ├─→ Map Operator ──┐
    │                      │                    │
    │                      │   Barrier对齐       │
    │                      │   (所有上游通道     │
    │                      │    收到Barrier前    │
    │                      │    阻塞该通道)      │
    │                      │                    │
    │                      ├─→ Window Operator ─┤
    │                      │   Snapshot State   │
    │                      │   (窗口累积值)      │
    │                      │                    │
    │                      └─→ Sink ────────────┘
    │                          (Kafka事务)
    │
    ├─ 收到所有Operator的ACK ──→ Checkpoint完成
```

**灾备演练（课堂练习1h）**：
1. 启动Flink任务（带Checkpoint）
2. 运行5分钟后，手动Kill TaskManager进程
3. 观察JobManager自动从Checkpoint恢复
4. 验证Exactly-Once：统计Sink端写入的数据行数，不应重复或丢失

**课后作业**：
- 对比RocksDB vs Heap State Backend的性能差异（状态大小100MB+）
- 配置增量Checkpoint并观察存储空间节省

---

### 课时21：Flink SQL与CDC（3h）

**教学内容**：
1. Flink SQL：流上的声明式查询
2. CDC Connector：MySQL Binlog实时同步
3. 动态表(Dynamic Table)概念
4. 时态表Join(Temporal Table Join)
5. 宽表实时构建：多流Join

**核心代码——Flink SQL CDC**：
```sql
-- 1. 创建MySQL CDC源表
CREATE TABLE mysql_orders (
    order_id BIGINT,
    user_id BIGINT,
    amount DECIMAL(10,2),
    status STRING,
    create_time TIMESTAMP(3),
    PRIMARY KEY (order_id) NOT ENFORCED
) WITH (
    'connector' = 'mysql-cdc',
    'hostname' = 'mysql',
    'port' = '3306',
    'username' = 'root',
    'database-name' = 'ecommerce',
    'table-name' = 'orders'
);

-- 2. 创建Kafka Sink表
CREATE TABLE kafka_order_stats (
    window_start TIMESTAMP(3),
    window_end TIMESTAMP(3),
    total_orders BIGINT,
    total_amount DECIMAL(20,2),
    PRIMARY KEY (window_start, window_end) NOT ENFORCED
) WITH (
    'connector' = 'upsert-kafka',
    'topic' = 'order-stats',
    'key.format' = 'json',
    'value.format' = 'json'
);

-- 3. 实时聚合写入Kafka
INSERT INTO kafka_order_stats
SELECT 
    TUMBLE_START(create_time, INTERVAL '1' MINUTE) AS window_start,
    TUMBLE_END(create_time, INTERVAL '1' MINUTE) AS window_end,
    COUNT(*) AS total_orders,
    SUM(amount) AS total_amount
FROM mysql_orders
WHERE status = 'completed'
GROUP BY TUMBLE(create_time, INTERVAL '1' MINUTE);
```

**课后作业**：
- 搭建Flink SQL CDC从MySQL到Kafka的实时同步管道
- 实现：MySQL订单表 → Flink CDC → Kafka → Flink SQL → ClickHouse

---

## 第19-22周：DDIA精读 + L2项目

### 课时22-25：DDIA核心章节精读（每周2次，每次3h）

**DDIA学习方式**（不是讲座，是读书会）：

```
每周流程:
  Day1: 个人阅读指定章节（30-50页）
  Day2: 小组讨论（每人分享3个最受启发的点 + 2个疑问）
  Day3: 讲师深度解读（结合工业实践案例）
  Day4: 写读书笔记（强制输出）
```

**核心章节学习重点**：

| 章节 | 核心概念 | 对应技术栈 |
|------|----------|------------|
| Ch3: 存储引擎 | LSM-Tree vs B-Tree | HBase、Cassandra、RocksDB |
| Ch4: 编码与演化 | Avro/Protobuf/Thrift | Kafka Schema Registry |
| Ch5: 复制 | Leader-based、Multi-leader | Kafka ISR、MySQL主从 |
| Ch6: 分区 | Key-range vs hash partitioning | Kafka partition、HBase region |
| Ch7: 事务 | ACID、隔离级别、MVCC | Delta Lake ACID、HBase MVCC |
| Ch8: 分布式问题 | 网络故障、时钟问题、拜占庭 | 所有分布式系统的理论基础 |
| Ch9: 共识 | Paxos/Raft/Zab | ZooKeeper、Kafka Controller |
| Ch10: 批处理 | MapReduce、物化中间状态 | Spark、Hive |
| Ch11: 流处理 | 事件时间、CEP、消息队列 | Flink、Kafka Streams |
| Ch12: 数据未来 | 分拆数据库、端到端原则 | 现代数据架构选型 |

**DDIA读书笔记模板**：
```markdown
# DDIA ChX 读书笔记

## 1. 本章核心观点（用自己的话总结3点）
1. 
2. 
3. 

## 2. 与实际技术的映射
- 书中提到的XXX → 对应我们使用的YYY
- 书中说的ZZZ问题 → 我在生产环境遇到过类似场景...

## 3. 一个仍不理解的问题

## 4. 一个可以用在项目中的启发
```

---

### 项目7：实时交易监控大屏（40h）

**项目描述**：构建从CDC采集到实时大屏的端到端实时数据处理管道。

**项目需求**：

```yaml
整体架构:
  MySQL → Debezium+Kafka → Flink → ClickHouse → Grafana

数据流设计:
  
  第1层 - CDC采集:
    源: MySQL ecommerce数据库（order、order_item、user表）
    工具: Debezium MySQL Connector
    格式: Kafka Topic中的Debezium JSON事件
    Topic设计:
      - mysql.ecommerce.orders
      - mysql.ecommerce.order_items
      - mysql.ecommerce.users

  第2层 - 流式ETL:
    引擎: Apache Flink
    任务:
      1. 订单宽表生成(订单JOIN用户信息)
      2. 实时统计指标计算:
         - 每分钟交易额(按品类分组)
         - 每分钟订单数
         - 实时UV(独立用户数)
         - 异常检测(单用户1分钟下单>3次)
      3. 数据标准化(CDC JSON → 业务结构化)

  第3层 - OLAP存储:
    存储: ClickHouse
    建表: ReplicatedMergeTree + 按天分区
    TTL: 72小时过期(只保留最近数据)

  第4层 - 可视化:
    工具: Grafana + ClickHouse数据源
    仪表盘:
      1. 实时交易概览:
         - 今日累计GMV(数字)
         - 实时下单速度(折线图，每分钟)
         - 各品类交易分布(饼图)
         - TOP 10畅销商品(柱状图)
      
      2. 实时用户分析:
         - 实时在线下单用户数
         - 新老用户占比
         - 用户地域分布(地图)
      
      3. 异常监控:
         - 下单量异常波动的品类(告警)
         - 疑似刷单用户列表
      
      4. 系统健康:
         - Kafka Lag监控
         - Flink Checkpoint耗时
         - ClickHouse写入延迟

  高级要求:
    - 延迟监控: 端到端延迟 < 5秒
    - 混沌工程: 手动Kill Flink TM，观察自愈
    - 流量回放: 用历史数据验证系统正确性
    - 数据一致性: 结果与MySQL直接查询对比
```

**交付物**：
1. 所有Flink作业代码
2. ClickHouse建表语句（含TTL和分区策略）
3. Grafana Dashboard JSON
4. 延迟测试报告（各环节耗时拆解）
5. 异常演练报告（故障注入→现象→恢复过程）

---

### 项目8：Kafka深度调优（20h）

**项目描述**：对Kafka集群进行系统性的性能调优和故障演练。

**项目需求**：

```yaml
调优维度:

Partition级别:
  - 探索：不同Partition数(1/3/10/30)对吞吐量的影响
  - 找出最佳Partition数（vs CPU核数的关系）
  - 结论输出：Partition不是越多越好

Producer调优:
  参数矩阵实验:
    acks: [0, 1, all]
    batch.size: [16KB, 64KB, 256KB, 1MB]
    linger.ms: [0, 5, 20, 100]
    compression.type: [none, gzip, snappy, lz4, zstd]
  
  每个组合测试1分钟，记录吞吐量和P99延迟
  找出: 吞吐最优配置 / 延迟最优配置 / 折中最优配置

Consumer调优:
  - fetch.min.bytes不同值的影响
  - max.poll.records vs 处理时间
  - Rebalance速度对比(CooperativeSticky vs Range)

故障演练:
  场景1: Broker宕机
    - Kill 1个Broker
    - 观察: ISR变化、Leader切换时间、Producer重试
    - 目标: 生产者无感知，切换时间<5秒
  
  场景2: 磁盘满
    - 模拟Broker磁盘使用率>90%
    - 观察: Kafka如何处理、告警如何触发
  
  场景3: 网络分区
    - 用iptables模拟Broker间网络延迟500ms
    - 观察: ISR收缩、Producer超时、Consumer Lag飙升
    - 恢复网络后，观察: 系统自愈过程

  场景4: Consumer Lag雪崩
    - 停止Consumer 10分钟
    - 观察: Lag堆积量、Consumer恢复后的追赶速度
    - 调优: fetch.max.bytes提升追赶速度

基准测试报告格式:
  每个实验包含:
    - 实验配置(参数组合)
    - 测试方法(perf-test.sh参数)
    - 结果数据(吞吐量、延迟分位数、资源使用)
    - 结论与生产建议
```

**交付物**：
1. Kafka调优基准测试报告（至少20个实验组合）
2. 生产环境推荐配置
3. 故障演练SOP（标准操作手册）
4. Kafka监控Dashboard配置（Prometheus + Grafana）

---

### 项目9：数据管道故障排查手册（15h）

**项目描述**：模拟生产环境常见故障，编写排查SOP。

**项目需求**：

```yaml
故障场景库（至少10个）:

场景1: Spark任务OOM
  现象: Executor OOM killed
  排查步骤:
    1. Spark UI看各Stage的Task数据量分布
    2. 定位数据倾斜的Key
    3. 分析Shuffle数据量
  解决方案: (提供3种)
    1. 加盐打散倾斜Key
    2. 增加executor memory
    3. 提前聚合减少数据量

场景2: Kafka Consumer Lag持续增长
  排查步骤:
    1. 计算Lag/(消费速率) 预估恢复时间
    2. 检查: Consumer是否有慢处理逻辑
    3. 检查: Broker是否有IO瓶颈
  解决方案: (根据排查结果选择)
    - 扩容Consumer
    - 加大fetch.max.bytes
    - 减少处理链路的耗时操作

场景3: Hive查询超慢
  排查步骤:
    1. EXPLAIN查看执行计划和Stage数量
    2. 检查分区裁剪是否生效
    3. 检查JOIN的Shuffle数据量
    4. 对比文件格式(Text vs Parquet)的性能差异
  解决方案:
    - 加分区条件
    - 小表Broadcast Join
    - 转Parquet格式

场景4-10: 自行调研添加
  (Flink反压、HDFS小文件问题、Kafka磁盘满、
   MySQL连接池耗尽、ClickHouse Merge慢查询等)
```

**交付物**：
- 《大数据平台常见故障排查SOP》手册（Markdown）
- 每个场景包含：现象描述→根因分析→排查步骤→解决方案→预防措施

---

## L2 结业考核

| 考核项 | 方式 | 通过标准 |
|--------|------|----------|
| Kafka调优 | 现场实操 | 给定一个Topic，调优达到基准吞吐量×1.5 |
| Flink开发 | 现场编码 | 1小时内完成一个带Window和Checkpoint的Flink任务 |
| 故障排查 | 模拟演练 | 讲师注入故障，学员30分钟内定位并解决 |
| 架构讲解 | 投影问答 | 完整讲解项目7的架构设计，回答5个Why |
| DDIA答辩 | PPT + 问答 | DDIA读书笔记分享，回答"与实际工作的映射" |

---

# L3 高级工程师：技术深度

## 阶段目标
深入组件源代码（Spark/Flink/Kafka至少各3000行核心代码），精读经典论文，具备性能调优攻坚能力，完成1个开源贡献PR。

---

## 第23-26周：源码深潜 + 论文精读

### 论文精读清单（12篇，每周1-2篇）

| 序号 | 论文 | 年份 | 阅读重点 |
|------|------|------|----------|
| 1 | Google File System | 2003 | 大块存储、追加写、Snapshot机制 |
| 2 | MapReduce | 2004 | 编程模型、容错策略、Locality优化 |
| 3 | BigTable | 2006 | SSTable、Compaction、列族设计 |
| 4 | Dremel | 2010 | 列式存储嵌套数据、SQL on Columnar |
| 5 | Resilient Distributed Datasets (Spark) | 2012 | Lineage、窄/宽依赖、Checkpoint |
| 6 | Kafka: a Distributed Messaging System | 2011 | 日志存储模型、Consumer Group |
| 7 | Apache Flink: Stream Processing at Scale | 若干 | Checkpoint、Savepoint、State管理 |
| 8 | Dynamo (Amazon) | 2007 | 最终一致性、一致性哈希、Gossip |
| 9 | Raft Consensus Algorithm | 2014 | Leader选举、Log Replication、安全性 |
| 10 | Data Lakehouse (CIDR) | 2021 | 开放格式、ACID on Data Lake |
| 11 | Photon (Databricks) | 2022 | Native向量化引擎、Runtime Filter |
| 12 | Spanner (Google) | 2012 | TrueTime、全球分布式事务 |

**论文阅读方法论**：
```
第一遍（30分钟）: 海量阅读
  - 只读: Abstract + Introduction + Conclusion + 所有图表
  - 目标: 知道这篇论文在解决什么问题，核心思路是什么
  - 输出: 一段话总结

第二遍（2小时）: 深度理解
  - 阅读全文，理解每个算法的步骤
  - 尝试用自己的话复述核心设计
  - 目标: 可以跟同事讲清楚这篇论文的核心设计
  - 输出: 详细的读书笔记（包含你对设计的评价）

第三遍（可选·精读）: 批判思考
  - 思考: 开源实现和论文有什么差异？
  - 思考: 论文的假设在什么情况下不成立？
  - 思考: 如果让你重新设计，你会怎么做？
```

---

### 源码深潜计划（Spark/Flink/Kafka三选一深入）

**Spark SQL Catalyst优化器源码阅读路线**（示例）：

```
路线图（由浅入深）:
  
  第1周: DataFrame API表层
    阅读: DataFrame.scala → Dataset.scala
    重点: select/filter/groupBy 如何构建 LogicalPlan
    任务: 写一篇"一个DataFrame.select()到底做了什么"
    
  第2周: Catalyst逻辑优化
    阅读: RuleExecutor.scala + Optimizer.scala
    重点: 20+个优化Rule(PushDownPredicate/ColumnPruning等)
    任务: 挑3个优化Rule，写清楚优化前后的Plan变化
    
  第3周: Catalyst物理计划
    阅读: SparkPlanner.scala + execution包
    重点: HashAggregateExec/SortMergeJoinExec的实现
    任务: 对比SortMergeJoin vs BroadcastHashJoin的执行代码
    
  第4周: WholeStageCodegen
    阅读: WholeStageCodegenExec.scala
    重点: 如何生成Janino编译的Java代码
    任务: 打开DEBUG日志，看生成的Java代码长什么样

每周强制输出:
  - 一篇源码分析文章(不少于2000字)
  - 包含: 架构图 + 关键代码注释 + 设计模式分析
```

---

### 项目10：Spark/Flink生产级调优攻坚（40h）

**项目描述**：给定一个故意构造的"烂任务"，从倾斜→Shuffle→GC一路调优至生产标准。

**项目需求**：

```yaml
初始任务（故意构造的问题）:
  - 100TB输入数据，严重数据倾斜(1个Key占80%)
  - Shuffle分区数设置不合理(默认200)
  - UDF实现低效(Python UDF逐行处理)
  - 没有任何Cache策略
  - Executor配置不合理(内存过小导致频繁GC)

调优步骤（每个步骤必须有对比数据）:

第1步: 数据倾斜解决
  方法对比:
    - 加盐(Salt)重分区
    - Broadcast小表(tips: 哪张表能被Broadcast?)
    - AQE自动倾斜处理(Spark 3.0+)
  记录: 每个方法的倾斜Key处理时间对比

第2步: Shuffle优化
  参数调优:
    spark.sql.shuffle.partitions: [200→800→1600→3200]
    spark.shuffle.compress: [true/false]
    spark.shuffle.file.buffer: [32K→64K→128K]
  记录: Shuffle Write/Read时间 + 磁盘IO使用

第3步: UDF优化
  是否可以用内置函数替代UDF？
  如果用UDF，Pandas UDF vs Python UDF性能差异
  记录: 每个方案的执行时间

第4步: 内存与GC调优
  对比GC策略:
    G1GC vs ParallelGC
  观察指标: GC次数、单次GC耗时、Full GC频率
  工具: GCViewer分析GC日志
  记录: GC优化前后的YARN监控截图

第5步: Cache策略对比
  对比:
    - 不Cache
    - Cache(MEMORY_ONLY)  
    - Cache(MEMORY_AND_DISK)
    - Checkpoint
  场景: 一个被多次使用的中间DataFrame
  记录: 每种策略下的总耗时和Storage内存使用

最终报告:
  - 初始状态: 运行时间/资源使用/失败原因
  - 每步优化后的数据
  - 最终状态: 运行时间缩短XX%、资源节省XX%
  - 《Spark性能调优Checklist》(可直接用于生产评审)
```

**考核要点**：
- 每个优化步骤必须有**数据支撑**，不能说"感觉变快了"
- 必须能解释**为什么变快了**（原理层面）
- 最好能提炼出**通用的调优方法论**，而不是只针对这个任务

---

### 开源贡献任务

```yaml
目标: 提交至少1个PR到Apache Spark/Flink/Kafka社区
  
  可选方向:
    - 修复一个"Good First Issue"标记的Bug
    - 改进文档或错误信息
    - 优化某个算子的实现
    - 添加一个新的Connector/Sink

  过程要求:
    1. 在JIRA上Claim一个Issue
    2. 在GitHub提交PR
    3. 响应Code Review意见（可能要修改多次）
    4. 最终PR被合入(merged)

  即使没合入，至少要有:
    - 社区互动的邮件/JIRA记录
    - PR中的Code Review讨论
    - 从中学到的开源协作规范
```

---

## L3 结业考核

| 考核项 | 方式 | 通过标准 |
|--------|------|----------|
| 源码阅读 | 现场问答 | 给定一段核心代码，解释设计意图和运行流程 |
| 论文复述 | PPT答辩 | 选1篇论文，15分钟讲清楚解决了什么、怎么解决的 |
| 性能调优 | 实战演示 | 原始任务运行30分钟→调优后<3分钟，能解释每个优化 |
| 技术深度 | 交叉面试 | 由L4以上评委随意提问，考察知识广度和深度 |

---

# L4 架构师：全局设计

## 阶段目标
具备独立完成大数据平台架构设计的能力；能在技术选型中做合理的Trade-Off；具备跨团队协调和Mentor能力；建立成本意识和数据驱动的决策习惯。

---

## 第27-30周：系统设计训练

### 系统设计方法论

**架构设计五步法**：
```
1. 需求澄清（最重要的一步）
   - 功能性需求(要做什么)
   - 非功能性需求(性能、可用性、一致性、成本)
   - 问10个问题再动笔

2. 容量估算
   - 数据量: 每日新增、存储周期
   - QPS: 读写比例、峰值倍数
   - 带宽: 数据传输量
   - 成本: 存储成本 + 计算成本

3. 高层设计
   - 划出子系统边界
   - 确定子系统间的接口(API/消息队列/文件)
   - 画出数据流向图

4. 深入设计
   - 每个子系统的技术选型
   - 不只是一个候选，而是2-3个候选的对比
   - 数据模型设计(存储格式、分区策略、索引)

5. 权衡分析
   - 列出每个关键决策的Trade-Off
   - 为什么选A而不是B？（不能只说A好）
   - 风险点 + 应对预案
```

---

### 系统设计题目（每周2题，共16题）

**题目1：设计一个日处理100TB的实时数仓**

```yaml
需求分析:
  - 数据源: MySQL(DMS)、Nginx日志、IoT传感器
  - 延迟要求: DWD层5分钟，DWS/ADS层15分钟
  - 存储周期: 原始数据7天，汇总数据3年
  - 查询要求: 报表查询<3秒，自助分析<30秒

候选方案:
  方案A: Kafka + Flink + ClickHouse + Iceberg
    优点: 端到端低延迟、ClickHouse查询快
    缺点: ClickHouse大宽表JOIN弱、Iceberg查询需Trino
  
  方案B: Kafka + Flink + StarRocks + Hudi
    优点: StarRocks分布式Join强、Hudi Upsert强
    缺点: 运维复杂度较高
  
  方案C: 全云托管方案(AWS Kinesis + EMR + Athena)
    优点: 运维成本低
    缺点: 成本高、供应商锁定

最终选择: （学员自行判断并写理由）
```

**题目2-8（必做）**：
1. 设计支持10万QPS的实时特征平台
2. 设计跨多云的数据联邦查询引擎
3. 设计支持PB级数据的数据湖仓系统
4. 设计超大规模离线计算平台
5. 设计实时用户画像系统
6. 设计数据质量监控平台
7. 设计数据血缘追踪系统

**题目9-16（选做4题）**：
- 参考 Alex Xu《系统设计面试》书中的题目，结合大数据场景改编

---

### 项目11：企业大数据平台架构设计（60h）

**项目描述**：模拟为一家中型电商公司（日活500万，日订单100万）设计完整的大数据平台。

**项目需求**：

```yaml
背景:
  公司现状:
    - 已有MySQL、MongoDB、Redis等30+个数据源
    - 当前用Python脚本定时拉数据，经常中断
    - 数据分析靠Excel，每周出一次周报
    - 没有数据质量体系，经常出现"同一个指标两个数字"
  
  业务目标:
    - 报表时效从T+7提升到T+0(当天可看)
    - 数据质量达到95%准确率
    - 能支持20人同时自助分析

交付文档结构:

第1章: 业务需求分析 (10h)
  1.1 现有数据源盘点(类型、数据量、更新频率)
  1.2 核心业务指标定义(GMV/留存/转化等)
  1.3 数据使用场景(报表/自助/ML/实时/离线)
  1.4 利益相关者访谈摘要(CEO/运营/产品/技术)

第2章: 技术架构设计 (20h)
  2.1 整体架构图(画清楚数据流向)
  2.2 组件选型对比
    每个关键组件至少对比3个候选:
    - 消息队列: Kafka vs Pulsar vs RocketMQ
    - 计算引擎: Flink vs Spark vs Storm
    - 存储引擎: ClickHouse vs Doris vs Druid
    - 数据湖: Iceberg vs Delta vs Hudi
    - 调度器: Airflow vs DolphinScheduler vs Prefect
    每个对比包含: 适用场景/性能基准/运维成本/社区活跃度
  
  2.3 数据模型设计
  2.4 容量规划(存储/计算/带宽)
  2.5 高可用设计(容灾/RTO/RPO)
  2.6 安全设计(认证/授权/审计/脱敏)

第3章: 实施路线图 (10h)
  3.1 分阶段实施计划
    Phase 1(1-3月): 离线数仓(MVP)
    Phase 2(4-6月): 实时管道
    Phase 3(7-12月): 数据湖仓升级 + 治理平台
  3.2 每个Phase的里程碑和验收标准
  3.3 人力规划(需要几个工程师、什么级别)

第4章: 成本预算 (10h)
  4.1 基础设施成本(服务器/云资源)
  4.2 人力成本
  4.3 总拥有成本(TCO) vs 预期收益
  4.4 ROI分析(何时回本)

第5章: 风险与应对 (10h)
  5.1 技术风险(新技术不成熟、性能不达标)
  5.2 组织风险(团队能力不足、业务方不配合)
  5.3 数据风险(数据源变更、数据质量)
  5.4 每个风险的应对预案
```

**交付物**：
- 完整的技术方案文档（预计80-120页）
- 1小时的方案汇报PPT（面对"CTO评审团"）
- 关键组件的POC验证报告（至少3个组件）

---

### 项目12：FinOps——大数据平台成本优化（20h）

**项目描述**：对现有大数据平台进行成本审计与优化。

**项目需求**：

```yaml
成本审计:
  
  计算资源审计:
    分析所有Spark/Flink任务:
    - 哪些任务占用了最多CPU/内存但是没有产出价值？
    - 哪些任务可以通过优化运行时间缩短50%以上？
    - 是否存在"僵尸任务"(每天跑但没人用结果)？
  
  存储审计:
    分析HDFS/对象存储:
    - 冷数据占比(超过30天未访问)
    - 重复数据(同一个数据存了多份)
    - 临时数据(ETL中间结果没清理)
  
  Kafka审计:
    - 哪些Topic的数据量最大但消费最少？
    - Retention设置是否合理？

优化方案:
  
  方案1: 冷热数据分层
    热数据(<7天): SSD/高频访问
    温数据(7-30天): HDD/低频访问
    冷数据(>30天): 归档存储(对象存储低频)
    策略: Iceberg表按天分区 → TTL自动迁移
    预期: 存储成本降低40%
  
  方案2: 计算资源弹性伸缩
    场景: 离线ETL任务(凌晨跑，白天资源闲置)
    方案: K8s + Spark on K8s，根据任务队列动态扩缩
    预期: 计算成本降低30%
  
  方案3: 任务合并与去重
    发现: 3个不同团队在做几乎相同的用户画像
    方案: 建立公共数据集市，统一提供基础画像
    预期: 计算成本降低20% + 数据一致性提升

  方案4: 查询优化
    分析: SQL查询日志，找出最耗资源的Top10查询
    方案: 物化视图、预聚合、分区裁剪
    预期: 查询成本降低50%

成本优化报告:
  - 现状: 月成本XX万
  - 优化后: 月成本XX万(降低XX%)
  - 措施清单(优先级排序)
  - 实施路径(哪些立即做、哪些需要规划)
  - 优化效果的量化评估方式
```

**交付物**：
1. 成本审计报告
2. 优化实施方案
3. ROI测算
4. 成本监控Dashboard（持续跟踪优化效果）

---

## L4 结业考核

| 考核项 | 方式 | 通过标准 |
|--------|------|----------|
| 系统设计面试 | 现场设计 | 2小时内完成一个大数据平台的系统设计 |
| 架构方案答辩 | PPT + 评审 | 项目11的方案通过"CTO评审团"（3位以上评委） |
| 成本优化 | 方案评估 | 方案可量化节省成本≥30%，有说服力的ROI |
| Mentor成果 | 学员评价 | 带的初级学员L2结业通过率≥80% |

---

# L5 CTO视野：战略与领导力

## 阶段目标
能够制定技术战略和路线图；建立团队的工程文化和人才梯队；能用业务语言翻译技术价值；具备行业级技术影响力。

---

## 第31+周：持续进化模块

### 模块1：技术战略工作坊（每月1次）

```yaml
工作坊形式: 模拟公司CTO季度战略会

议题模板:
  
  第1季度: 技术债务评估
    - 列出平台Top 10技术债务
    - 每项债务的影响(团队效率/系统稳定性/业务风险)
    - 优先级排序: 影响×修复成本
    - 制定还债路线图(未来2个季度的还债计划)
  
  第2季度: 新技术评估
    - 调研3-4个新技术方向
    - 每个方向: 
      * 调研报告(技术成熟度、竞品使用情况、社区活跃度)
      * POC验证(花1-2周搭原型)
      * 引入建议(引入/观察/放弃，给出理由)
  
  第3季度: 年度技术规划
    - 回顾过去一年技术投入的效果
    - 下一年技术投入的预算分配
    - 各团队的技术OKR

输出产物:
  - 《Qx技术战略备忘录》(给CEO看的精简版)
  - 《技术债务台账》(持续更新)
  - 《技术雷达》(团队的技术方向指引)
```

---

### 模块2：组织建设实践

```yaml
任务1: 制定工程师能力模型
  定义各职级(L1-L5)的能力标准:
    - 技术能力(各职级需要掌握的技术栈)
    - 业务能力(对业务理解的深度)
    - 软技能(沟通/协作/领导力)
    - 影响力(对内/对外)
  
  要求:
    - 不能只是"熟练使用XXX"，要有可评估的行为描述
    - 区分I/C (Individual Contributor) vs M (Manager) track

任务2: 设计技术评审流程
  - 什么级别的方案需要什么级别的评审？
  - 评审Checklist(架构/安全/成本/运维)
  - 如何避免评审沦为"盖章通过"？

任务3: 建立工程文化
  - Code Review文化: 如何让团队从"抵触"到"习惯"？
  - 技术分享文化: 如何让分享不是走过场？
  - 数据驱动文化: 如何让决策靠数据不靠感觉？

任务4: 招聘体系设计
  - 各职级面试流程
  - 面试题库(技术+行为)
  - 面试官培训计划
```

---

### 模块3：商业翻译训练

```yaml
训练方法: 角色扮演 + 实际案例

训练1: "一句话解释你的方案"
  场景: 在电梯里遇到CEO，你有30秒解释大数据平台的价值
  要求: 不用任何技术术语
  范例: 
    ✗ "我们搭建了Hadoop+Spark集群，支持PB级数据处理"
    ✓ "我们把看数据报告的时间从每周一等到了每天早上9点，
        而且所有人都能自己查数据，不用再发邮件问数据组"

训练2: "给董事会做技术提案"
  场景: 申请2000万预算升级数据平台
  要求: 5页PPT，每页都要回答"What's in it for me?"
  内容: 
    Page1: 我们现在的问题(不要用技术语言，用业务影响)
    Page2: 如果什么都不做，明年会怎样
    Page3: 我们建议的方案(只说"做什么"，不说"怎么做")
    Page4: 方案的投资回报(ROI)、风险
    Page5: 需要董事会做什么决定

训练3: "技术事故的外部沟通"
  场景: 数据平台宕机4小时，影响了100万用户的推荐结果
  要求: 分别准备
    - 给CEO的内部报告(5分钟)
    - 给客户的公开说明(200字)
    - 给投资人的情况说明(如果有必要)
```

---

### 项目13：CTO年度述职报告（持续项目）

**项目描述**：模拟一次CTO的年度述职汇报。

**要求**：

```yaml
述职报告结构:

Part 1: 回顾过去一年(30%)
  - 技术目标达成情况(用数字说话)
  - 关键项目的ROI复盘
  - 团队成长数据(晋升率/流失率/人才密度)

Part 2: 行业趋势分析(20%)
  - 大数据/AI行业的3个关键趋势
  - 竞品/标杆公司的技术动态
  - 对我们公司的影响分析

Part 3: 下一年规划(40%)
  - 技术路线图(按季度拆解)
  - 资源需求(钱+人+时间)
  - 预期产出与业务价值
  - 关键风险与应对

Part 4: 团队发展(10%)
  - 组织架构建议
  - 关键人才计划(招聘+培养)
  - 工程文化目标

交付物:
  - 20页PPT(每页思考时间≥30分钟)
  - 30分钟演讲(录像)
  - 财务模型(支撑资源需求)
```

---

## L5 持续评定标准

| 维度 | 评估方式 | 卓越标准 |
|------|----------|----------|
| 技术战略 | 年度技术规划文档 | 规划被采纳，12个月后回顾准确率>70% |
| 团队建设 | 团队360评估 | 团队满意度>85%，关键人才保留率>90% |
| 商业价值 | ROI量化 | 能证明每项技术投入的商业回报 |
| 行业影响 | 外部活动 | 每年至少1次大会演讲/技术博客阅读量>5万 |

---

# 附录

---

## 附录A：实验室环境搭建指南

### A.1 L0阶段环境（个人电脑即可）

```yaml
硬件要求:
  CPU: 4核以上
  内存: 16GB
  磁盘: 500GB SSD

软件清单:
  - Python 3.10+ (Anaconda)
  - VS Code + Python插件
  - MySQL 8.0
  - VirtualBox 7.0+
  - Git for Windows
  - Docker Desktop

验证命令:
  python --version     # 3.10+
  mysql --version      # 8.0+
  git --version        # 2.40+
  docker --version     # 24.0+
```

---

### A.2 L1-L2阶段环境（本地 + 云）

```yaml
本地开发环境:
  硬件: 32GB内存 + 1TB SSD + 8核CPU

Docker Compose栈（一键启动）:
  文件: docker-compose-bigdata.yml
  
  服务清单:
    hadoop-namenode:1     端口9870
    hadoop-datanode:3     端口9864
    hive-metastore:1      端口9083
    hive-server:1         端口10000
    spark-master:1        端口8080
    spark-worker:2        端口8081
    mysql:1               端口3306
    zookeeper:3           端口2181
    kafka-broker:3        端口9092
    flink-jobmanager:1    端口8081
    flink-taskmanager:2
    clickhouse:1          端口8123/9000
    airflow:1             端口8080

阿里云/AWS沙箱（L2-L3阶段必需）:
  - ECS 4核16GB × 1 (管理节点)
  - ECS 8核32GB × 3 (计算节点)
  - OSS/S3: 1TB (对象存储)
  - 月预算: 1500-3000元

  重要: 学生必须自己支付部分云费用，体验成本意识。
```

---

### A.3 L3-L4阶段（云原生）

```yaml
Kubernetes环境:
  方案1（本地）: Kind / Minikube / K3s
  方案2（云端）: 阿里云ACK / AWS EKS / GCP GKE
  
大数据on K8s组件:
  - Spark Operator (Google)
  - Flink Operator (Apache)
  - Kafka Strimzi Operator
  - Trino on K8s
  - MinIO (S3兼容对象存储)

部署工具: Helm Charts统一管理
```

---

## 附录B：必读论文清单

| 序号 | 论文 | 年份 | L级别 | 一句话描述 |
|------|------|------|--------|------------|
| 1 | The Google File System | 2003 | L1 | HDFS的设计原型 |
| 2 | MapReduce: Simplified Data Processing | 2004 | L1 | 分布式计算的经典范式 |
| 3 | Bigtable: A Distributed Storage System | 2006 | L1 | HBase/Cassandra的设计灵感 |
| 4 | Dynamo: Amazon's Highly Available KV Store | 2007 | L2 | 最终一致性 + Gossip协议 |
| 5 | Kafka: a Distributed Messaging System | 2011 | L2 | Kafka的原始设计论文 |
| 6 | Resilient Distributed Datasets (Spark) | 2012 | L2 | RDD的起源与设计 |
| 7 | Dremel: Interactive Analysis of Web-Scale Data | 2010 | L2 | Trino/Presto的列式存储思想 |
| 8 | In Search of an Understandable Consensus Algorithm (Raft) | 2014 | L3 | 共识算法的科普性版本 |
| 9 | Apache Flink®: Stream Processing at Scale | 若干 | L3 | Flink核心设计理念 |
| 10 | Data Lakehouse (CIDR) | 2021 | L3 | 湖仓一体架构的提出 |
| 11 | Photon: A Fast Query Engine for Lakehouse Systems | 2022 | L4 | Databricks Native引擎 |
| 12 | Spanner: Google's Globally-Distributed Database | 2012 | L4 | TrueTime与全球分布式事务 |

---

## 附录C：关键考核时间线

```
周次    L级别    考核/里程碑
──────────────────────────────────────────────
 4      L0        Python爬虫 + SQL 50题 + Git绿点30天
 6      L0结业    L0项目3个完成 + 综合笔试通过 → 升L1
14      L1结业    离线数仓 + 用户画像 + Airflow → 升L2
22      L2结业    实时管道 + DDIA读书笔记 → 升L3
26      L3中期    论文精读6篇 + 源码3000行
32      L3结业    调优攻坚 + 开源PR → 升L4
38      L4中期    系统设计8题完成
44      L4结业    架构方案通过评审团 → 升L5
52+     L5持续    年度述职 + 技术战略输出
```

---

## 附录D：课件使用说明（给讲师）

```yaml
讲师角色定位:
  - 不做PPT讲师，做项目教练
  - 80%时间不在讲台上，在学员工位上答疑
  - 核心价值: 指出盲区 + 追问Why + 强迫复盘

教学节奏:
  周一到周四: 上午理论(2h) + 下午动手(6h)
  周五: 项目阶段评审(集中答疑)
  周六: 技术分享会(学员主讲，讲师点评)
  周日: 休息

纪律要求（必须严格执行）:
  - GitHub每日提交: 缺1天警告，连续缺3天淘汰
  - 技术Blog每周1篇: 不交不进入下一周
  - 每周复盘笔记: 记录"本周最大的1个收获 + 1个踩坑"
  - 迟到: 第二次开始，每次罚讲1小时技术分享

淘汰机制:
  以下情况启动退出流程:
    - 连续4周GitHub提交不足
    - 项目答辩2次不通过
    - 明显态度问题(抄袭、敷衍)
  
  重磅: 每个阶段允许10%淘汰率，保持学员质量
```

---

## 附录E：推荐阅读书单（按阶段排序）

| 阶段 | 书名 | 作者 | 必读/选读 |
|------|------|------|-----------|
| L0 | Python编程：从入门到实践 | Eric Matthes | 必读 |
| L0 | SQL必知必会 | Ben Forta | 必读 |
| L0 | 鸟哥的Linux私房菜(基础篇) | 鸟哥 | 必读(前12章) |
| L1 | Hadoop权威指南 | Tom White | 必读(前10章) |
| L1 | Spark快速大数据分析 | Holden Karau | 必读(1-6章) |
| L1 | 数据仓库工具箱(维度建模指南) | Kimball | 必读(1-6章) |
| L2 | Kafka权威指南 | Neha Narkhede | 必读 |
| L2 | 基于Apache Flink的流处理 | Fabian Hueske | 必读(1-8章) |
| L2 | 数据密集型应用系统设计(DDIA) | Kleppmann | 必读全书(至少2遍) |
| L2 | 大数据之路：阿里巴巴大数据实践 | 阿里巴巴 | 必读 |
| L3 | Apache Flink源码解析 | - | 选读(源码为主) |
| L3 | Spark SQL内核剖析 | - | 选读(源码为主) |
| L4 | 系统设计面试 | Alex Xu | 必读 |
| L4 | The Manager's Path | Camille Fournier | 必读 |
| L4 | 企业IT架构转型之道 | 钟华 | 选读 |
| L5 | 从0到1 | Peter Thiel | 选读 |
| L5 | 成为CTO | 若干 | 选读 |
| L5 | Google软件工程 | Titus Winters | 必读 |