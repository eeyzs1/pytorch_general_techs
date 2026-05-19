# 项目1：Web日志分析系统

> **项目时长**：15小时（约3天）
> **项目类型**：独立完成
> **前置技能**：Python（文件操作、正则、面向对象）、命令行

---

## 一、项目概述

构建一个完整的Web日志采集与分析系统，从数据生成到最终输出分析报告。这是L0阶段最核心的项目，综合考察Python编程、数据分析和报告生成能力。

### 项目目标
- 独立完成数据生成、解析、分析、报告生成的完整流程
- 巩固Python面向对象编程和文件处理技能
- 掌握正则表达式在日志解析中的实战应用
- 培养数据处理Pipeline思维

---

## 二、项目需求

### 阶段1：数据生成（3h）

编写 `log_generator.py`，生成模拟Nginx访问日志。

**要求**：

```yaml
数据规模: 100万行Nginx访问日志

时间分布:
  - 模拟7天的数据（可配置）
  - 真实的时间分布：白天（8:00-22:00）占80%，凌晨（22:00-8:00）占20%
  - 周末流量比工作日高20%

IP地址:
  - 生成1000个不同IP
  - 符合长尾分布：20%的IP产生80%的请求
  - IP格式：IPv4标准格式

URL分布:
  - 20个不同页面
  - 符合长尾分布：80%的访问集中在5个页面
  - URL格式：模拟真实电商网站路径

状态码分布:
  - 200: 80%
  - 301/302: 5%
  - 404: 10%
  - 500/502/503: 5%

响应时间:
  - 符合对数正态分布
  - 中位数：200ms
  - 99分位：2000ms

日志格式（Nginx combined格式）:
  '$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent"'
```

**日志生成器代码框架**：

```python
"""
log_generator.py - 模拟Nginx日志生成器
生成100万行符合真实分布的模拟Web访问日志
"""
import random
import time
from datetime import datetime, timedelta


class LogGenerator:
    """Nginx日志生成器"""

    # 配置参数
    TOTAL_LINES = 1_000_000
    TOTAL_DAYS = 7
    UNIQUE_IPS = 1000
    URLS = [
        "/index.html", "/api/users", "/api/products", "/api/orders",
        "/login", "/register", "/dashboard", "/cart",
        "/api/search", "/products/category/1", "/products/category/2",
        "/checkout", "/account/settings", "/about",
        "/api/recommendations", "/blog/post-1", "/blog/post-2",
        "/static/css/main.css", "/static/js/app.js", "/faq",
    ]

    STATUS_CODES = [200] * 80 + [301, 302] * 5 + [404] * 10 + [500, 502, 503] * 5
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/17.0",
        "Mozilla/5.0 (X11; Linux x86_64) Firefox/121.0",
        "curl/8.0.1",
        "Python-requests/2.31.0",
    ]

    def __init__(self, output_file="access.log"):
        self.output_file = output_file
        self.ips = self._generate_ips()
        self.start_date = datetime.now() - timedelta(days=self.TOTAL_DAYS)

    def _generate_ips(self):
        """生成1000个IP，符合长尾分布"""
        ips = []
        for i in range(self.UNIQUE_IPS):
            # 生成随机IP
            octets = [random.randint(1, 254) for _ in range(4)]
            ips.append(".".join(map(str, octets)))
        return ips

    def _generate_request_time(self):
        """生成符合对数正态分布的响应时间（毫秒）"""
        # 对数正态分布，中位数约200ms
        return round(random.lognormvariate(5.3, 0.8))

    def _weighted_choice(self, items, weights=None):
        """带权重的随机选择"""
        if weights is None:
            return random.choice(items)
        # 使用轮盘赌算法
        total = sum(weights)
        r = random.uniform(0, total)
        cumulative = 0
        for item, weight in zip(items, weights):
            cumulative += weight
            if r <= cumulative:
                return item
        return items[-1]

    def generate(self):
        """生成日志文件"""
        print(f"开始生成 {self.TOTAL_LINES:,} 行日志...")
        start_time = time.time()

        # 生成IP权重（80/20法则）
        ip_weights = []
        for i in range(len(self.ips)):
            # 前20%的IP权重高
            if i < len(self.ips) * 0.2:
                ip_weights.append(80)
            else:
                ip_weights.append(20)

        # 生成URL权重
        url_weights = []
        for i in range(len(self.URLS)):
            if i < 5:
                url_weights.append(80)  # 前5个URL占80%
            else:
                url_weights.append(20)

        with open(self.output_file, "w", encoding="utf-8") as f:
            buffer = []
            for i in range(self.TOTAL_LINES):
                # 生成时间（白天多，凌晨少）
                day_offset = random.randint(0, self.TOTAL_DAYS - 1)
                # 使用加权生成小时
                hour_weights = [3]*8 + [10]*14 + [3]*2  # 0-7点少, 8-21点多, 22-23点少
                hour = self._weighted_choice(range(24), hour_weights)

                log_date = self.start_date + timedelta(
                    days=day_offset,
                    hours=hour,
                    minutes=random.randint(0, 59),
                    seconds=random.randint(0, 59)
                )

                ip = self._weighted_choice(self.ips, ip_weights)
                url = self._weighted_choice(self.URLS, url_weights)
                method = random.choice(["GET", "GET", "GET", "GET", "POST", "HEAD"])
                status = random.choice(self.STATUS_CODES)
                size = int(random.lognormvariate(7, 2)) if status == 200 else random.randint(100, 5000)
                referer = random.choice(["https://www.example.com/", "https://www.google.com/", "-"])
                ua = random.choice(self.USER_AGENTS)
                response_time = self._generate_request_time()

                # Nginx combined格式
                time_str = log_date.strftime("%d/%b/%Y:%H:%M:%S +0800")
                line = (f'{ip} - - [{time_str}] "{method} {url} HTTP/1.1" '
                        f'{status} {size} "{referer}" "{ua}" rt={response_time}ms\n')

                buffer.append(line)

                # 批量写入（提高性能）
                if len(buffer) >= 10000:
                    f.writelines(buffer)
                    buffer.clear()

                if (i + 1) % 100000 == 0:
                    elapsed = time.time() - start_time
                    rate = (i + 1) / elapsed
                    print(f"  已生成 {i+1:,} 行 ({rate:,.0f} 行/秒)")

            # 写入剩余缓冲
            if buffer:
                f.writelines(buffer)

        elapsed = time.time() - start_time
        print(f"\n生成完成！")
        print(f"  总行数: {self.TOTAL_LINES:,}")
        print(f"  耗时: {elapsed:.1f}秒")
        print(f"  速率: {self.TOTAL_LINES/elapsed:,.0f} 行/秒")
        print(f"  输出文件: {self.output_file}")


if __name__ == "__main__":
    generator = LogGenerator("access.log")
    generator.generate()
```

---

### 阶段2：日志解析（4h）

编写 `log_parser.py`，解析生成的日志文件。

**要求**：

```yaml
功能:
  - 正则表达式提取每条日志的所有字段
  - 异常处理: 处理格式错误的行
  - 输出结构化数据（CSV + JSON两种格式）
  - 支持大文件流式处理（不能一次加载全部到内存）

输出字段:
  - ip: 客户端IP
  - time: 请求时间（ISO格式）
  - method: HTTP方法
  - url: 请求路径
  - status: 状态码（整数）
  - size: 响应大小（字节）
  - referer: 来源页面
  - user_agent: 浏览器标识
  - response_time: 响应时间（毫秒）
```

**日志解析器核心代码**：

```python
"""
log_parser.py - Nginx日志解析器
解析access.log并输出CSV和JSON格式
"""
import re
import csv
import json
import time
from pathlib import Path


class AdvancedLogParser:
    """增强版Nginx日志解析器"""

    LOG_PATTERN = re.compile(
        r'(?P<ip>\d+\.\d+\.\d+\.\d+)\s+'           # IP
        r'\S+\s+\S+\s+'                              # 占位字段
        r'\[(?P<time>[^\]]+)\]\s+'                   # 时间
        r'"(?P<method>\S+)\s+'                        # 方法
        r'(?P<url>\S+)\s+'                            # URL
        r'\S+"\s+'                                    # HTTP版本
        r'(?P<status>\d{3})\s+'                       # 状态码
        r'(?P<size>\d+)\s+'                           # 大小
        r'"(?P<referer>[^"]*)"\s+'                    # 来源
        r'"(?P<ua>[^"]*)"\s*'                         # UA
        r'(?:rt=(?P<response_time>\d+))?'             # 响应时间（可选）
    )

    MONTH_MAP = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
        "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
        "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
    }

    def __init__(self):
        self.parse_errors = 0
        self.total_lines = 0
        self.success_lines = 0

    def parse_time(self, time_str):
        """将Nginx时间格式转为ISO格式"""
        # [15/Jan/2024:10:30:00 +0800]
        match = re.match(r'(\d+)/(\w+)/(\d+):(\d+):(\d+):(\d+)', time_str)
        if match:
            day, month, year, hour, minute, second = match.groups()
            month_num = self.MONTH_MAP.get(month, 1)
            return f"{year}-{month_num:02d}-{day} {hour}:{minute}:{second}"
        return time_str

    def parse_line(self, line):
        """解析单行日志"""
        match = self.LOG_PATTERN.match(line.strip())
        if not match:
            self.parse_errors += 1
            return None

        record = match.groupdict()

        # 类型转换
        record["status"] = int(record["status"])
        record["size"] = int(record["size"])
        record["response_time"] = int(record.get("response_time") or 0)

        # 时间格式化
        record["time"] = self.parse_time(record["time"])

        return record

    def parse_file(self, input_file, output_csv=None, output_json=None):
        """解析日志文件"""
        print(f"开始解析: {input_file}")
        start_time = time.time()

        records = []
        self.parse_errors = 0
        self.total_lines = 0

        with open(input_file, "r", encoding="utf-8") as f:
            csv_writer = None
            csv_file = None

            if output_csv:
                csv_file = open(output_csv, "w", encoding="utf-8", newline="")
                csv_writer = None  # 延迟初始化

            for line in f:
                self.total_lines += 1
                record = self.parse_line(line)
                if record:
                    records.append(record)
                    self.success_lines += 1

                    # 流式写入CSV
                    if output_csv and csv_file:
                        if csv_writer is None:
                            csv_writer = csv.DictWriter(csv_file, fieldnames=record.keys())
                            csv_writer.writeheader()
                        csv_writer.writerow(record)

                # 进度报告
                if self.total_lines % 100000 == 0:
                    elapsed = time.time() - start_time
                    rate = self.total_lines / elapsed
                    print(f"  已处理 {self.total_lines:,} 行 ({rate:,.0f} 行/秒)")

            if csv_file:
                csv_file.close()

        # 写入JSON
        if output_json:
            print(f"写入JSON: {output_json}")
            with open(output_json, "w", encoding="utf-8") as f:
                json.dump(records, f, ensure_ascii=False, indent=2)

        elapsed = time.time() - start_time
        print(f"\n解析完成！")
        print(f"  总行数: {self.total_lines:,}")
        print(f"  成功解析: {self.success_lines:,}")
        print(f"  解析失败: {self.parse_errors}")
        print(f"  成功率: {self.success_lines/self.total_lines*100:.2f}%")
        print(f"  耗时: {elapsed:.1f}秒")

        return records


if __name__ == "__main__":
    parser = AdvancedLogParser()
    parser.parse_file("access.log", "parsed_logs.csv", "parsed_logs.json")
```

---

### 阶段3：数据分析（5h）

编写 `log_analyzer.py`，对解析后的数据进行统计分析。

**分析维度**：

```yaml
必须完成的统计分析:
  1. 每日/每小时PV（页面浏览量）
  2. 每日/每小时UV（独立访客数）
  3. 每个URL的访问量排名（TOP 20）
  4. HTTP状态码分布（含百分比）
  5. 独立IP TOP 20
  6. 平均响应时间趋势（按小时）
  7. 流量突增检测（某小时PV超过前24小时均值的2倍）
  8. P50/P90/P99响应时间
  9. 爬虫请求占比（UA包含bot/crawler/spider）
  10. 错误率趋势（按天）
  11. 各HTTP方法使用占比
  12. 流量TOP 10 URL（按响应大小计算流量）
```

**分析器代码框架**：

```python
"""
log_analyzer.py - 日志数据分析器
"""
import json
import csv
from collections import defaultdict, Counter
from datetime import datetime


class LogAnalyzer:
    """日志数据分析器"""

    def __init__(self):
        self.records = []

    def load_json(self, filepath):
        """从JSON文件加载记录"""
        with open(filepath, "r", encoding="utf-8") as f:
            self.records = json.load(f)
        print(f"已加载 {len(self.records):,} 条记录")

    def load_csv(self, filepath):
        """从CSV文件加载记录"""
        self.records = []
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["status"] = int(row["status"])
                row["size"] = int(row["size"])
                row["response_time"] = int(row.get("response_time", 0))
                self.records.append(row)
        print(f"已加载 {len(self.records):,} 条记录")

    def analyze_all(self):
        """执行全部分析"""
        if not self.records:
            print("没有数据可分析！")
            return {}

        results = {}

        # 1. PV统计
        results["total_pv"] = len(self.records)

        # 2. UV统计
        results["total_uv"] = len(set(r["ip"] for r in self.records))

        # 3. 每日PV/UV
        daily_stats = {}
        for r in self.records:
            day = r["time"][:10]  # 取日期部分
            if day not in daily_stats:
                daily_stats[day] = {"pv": 0, "uv": set(), "total_rt": 0, "errors": 0}
            daily_stats[day]["pv"] += 1
            daily_stats[day]["uv"].add(r["ip"])
            daily_stats[day]["total_rt"] += r["response_time"]
            if r["status"] >= 400:
                daily_stats[day]["errors"] += 1

        results["daily"] = {}
        for day in sorted(daily_stats.keys()):
            stats = daily_stats[day]
            results["daily"][day] = {
                "pv": stats["pv"],
                "uv": len(stats["uv"]),
                "avg_rt": round(stats["total_rt"] / max(stats["pv"], 1)),
                "error_rate": round(stats["errors"] / stats["pv"] * 100, 2),
            }

        # 4. 每小时PV
        hourly_pv = defaultdict(int)
        for r in self.records:
            hour = r["time"][:13]  # YYYY-MM-DD HH
            hourly_pv[hour] += 1
        results["hourly_pv"] = dict(sorted(hourly_pv.items()))

        # 5. URL排名
        url_counter = Counter(r["url"] for r in self.records)
        results["top_urls"] = url_counter.most_common(20)

        # 6. 状态码分布
        status_counter = Counter(r["status"] for r in self.records)
        results["status_distribution"] = {
            str(k): {"count": v, "pct": round(v/len(self.records)*100, 2)}
            for k, v in status_counter.most_common()
        }

        # 7. IP TOP 20
        ip_counter = Counter(r["ip"] for r in self.records)
        results["top_ips"] = ip_counter.most_common(20)

        # 8. 响应时间统计
        response_times = sorted(r["response_time"] for r in self.records if r["response_time"] > 0)
        if response_times:
            results["response_time"] = {
                "avg": round(sum(response_times) / len(response_times)),
                "p50": response_times[len(response_times) // 2],
                "p90": response_times[int(len(response_times) * 0.9)],
                "p99": response_times[int(len(response_times) * 0.99)],
                "max": response_times[-1],
            }

        # 9. HTTP方法分布
        method_counter = Counter(r["method"] for r in self.records)
        results["method_distribution"] = dict(method_counter.most_common())

        # 10. 爬虫请求
        bot_pattern = re.compile(r'bot|crawler|spider|scraper', re.IGNORECASE)
        bot_requests = sum(1 for r in self.records if bot_pattern.search(r.get("ua", "")))
        results["bot_stats"] = {
            "count": bot_requests,
            "pct": round(bot_requests / len(self.records) * 100, 2),
        }

        # 11. URL流量TOP
        url_traffic = defaultdict(int)
        for r in self.records:
            url_traffic[r["url"]] += r["size"]
        results["top_url_traffic"] = sorted(
            url_traffic.items(), key=lambda x: x[1], reverse=True
        )[:10]

        # 12. 流量突增检测
        if results["hourly_pv"]:
            hourly_values = list(results["hourly_pv"].values())
            avg_pv = sum(hourly_values) / len(hourly_values)
            burst_threshold = avg_pv * 2
            bursts = []
            for i, (hour, pv) in enumerate(results["hourly_pv"].items()):
                if pv > burst_threshold:
                    # 计算超出倍数
                    prev_24h_avg = sum(
                        list(results["hourly_pv"].values())[max(0, i-24):i]
                    ) / min(24, i) if i > 0 else pv
                    if prev_24h_avg > 0 and pv > prev_24h_avg * 2:
                        bursts.append({
                            "hour": hour,
                            "pv": pv,
                            "ratio": round(pv / prev_24h_avg, 1),
                        })
            results["traffic_bursts"] = bursts

        return results

    def print_report(self, results):
        """打印分析报告"""
        print("\n" + "=" * 60)
        print("         Web日志分析报告")
        print("=" * 60)

        print(f"\n【基本概览】")
        print(f"  总PV: {results['total_pv']:,}")
        print(f"  总UV: {results['total_uv']:,}")
        print(f"  PV/UV比: {results['total_pv']/max(results['total_uv'], 1):.1f}")

        print(f"\n【每日趋势】")
        print(f"  {'日期':<12} {'PV':>8} {'UV':>6} {'平均RT':>8} {'错误率':>6}")
        print(f"  {'-'*45}")
        for day, stats in results.get("daily", {}).items():
            print(f"  {day:<12} {stats['pv']:>8,} {stats['uv']:>6,} "
                  f"{stats['avg_rt']:>6}ms {stats['error_rate']:>5.1f}%")

        print(f"\n【状态码分布】")
        for status, info in results.get("status_distribution", {}).items():
            print(f"  {status}: {info['count']:>8,} ({info['pct']:.1f}%)")

        print(f"\n【TOP 10 URL】")
        for rank, (url, count) in enumerate(results.get("top_urls", [])[:10], 1):
            print(f"  {rank:>2}. {url:<40} {count:>8,}")

        if "response_time" in results:
            rt = results["response_time"]
            print(f"\n【响应时间】")
            print(f"  平均: {rt['avg']}ms  P50: {rt['p50']}ms  "
                  f"P90: {rt['p90']}ms  P99: {rt['p99']}ms")

        print(f"\n【HTTP方法】")
        for method, count in results.get("method_distribution", {}).items():
            print(f"  {method}: {count:,}")

        if results.get("traffic_bursts"):
            print(f"\n【流量突增检测】")
            for burst in results["traffic_bursts"]:
                print(f"  {burst['hour']}: {burst['pv']:,} PV "
                      f"(超出{p2['ratio']}倍)")

        print(f"\n【爬虫请求】")
        bot = results.get("bot_stats", {})
        print(f"  数量: {bot.get('count', 0):,}")
        print(f"  占比: {bot.get('pct', 0)}%")


if __name__ == "__main__":
    import re
    analyzer = LogAnalyzer()
    analyzer.load_csv("parsed_logs.csv")
    results = analyzer.analyze_all()
    analyzer.print_report(results)
```

---

### 阶段4：报告生成（3h）

编写 `report_generator.py`，生成Markdown格式的分析报告。

**要求**：
- 包含所有统计结果
- 使用Markdown表格
- 包含趋势分析的文字解读
- 输出到 `analysis_report.md`

---

## 三、项目交付物

| 序号 | 文件名 | 说明 |
|------|--------|------|
| 1 | `log_generator.py` | 日志生成脚本 |
| 2 | `log_parser.py` | 日志解析脚本 |
| 3 | `log_analyzer.py` | 数据分析脚本 |
| 4 | `report_generator.py` | 报告生成脚本 |
| 5 | `analysis_report.md` | 最终分析报告（Markdown格式） |
| 6 | `sample_output/` | 各阶段的采样输出文件 |

**GitHub提交要求**：
- 完整的提交历史（至少15次commit）
- 每个阶段的代码独立提交
- README.md包含运行说明

---

## 四、评分标准

| 评分项 | 权重 | 满分标准 |
|--------|------|----------|
| 日志生成 | 20% | 数据量达标，分布合理，性能良好 |
| 日志解析 | 25% | 正则正确，异常处理完善，支持CSV+JSON输出 |
| 数据分析 | 25% | 统计维度完整，逻辑正确 |
| 报告生成 | 15% | 格式规范，包含图表和解读 |
| 代码质量 | 15% | 结构清晰，注释合理，命名规范 |

---

## 五、时间建议

| 阶段 | 建议时间 | 关键任务 |
|------|----------|----------|
| 阶段1 | 3h | 完成LogGenerator，生成100万行日志 |
| 阶段2 | 4h | 完成AdvancedLogParser，输出CSV/JSON |
| 阶段3 | 5h | 完成LogAnalyzer，覆盖所有分析维度 |
| 阶段4 | 3h | 完成ReportGenerator，输出analysis_report.md |