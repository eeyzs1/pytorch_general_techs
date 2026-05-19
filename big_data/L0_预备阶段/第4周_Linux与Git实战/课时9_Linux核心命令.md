# 课时9：Linux核心命令

> **课时时长**：3小时
> **教学方式**：讲演 + 动手实操（纯命令行）
> **前置要求**：课时1-8完成

---

## 一、教学目标

1. 熟练掌握Linux文件系统导航和基本文件操作命令
2. 理解Linux权限模型并能正确设置
3. 掌握进程管理基本命令
4. 重点掌握文本处理三剑客：grep、awk、sed
5. 能够用纯命令行处理百万行日志数据

---

## 二、教学内容

### 2.1 文件系统导航（20分钟）

```bash
# ========== 基础导航命令 ==========

# 查看当前目录
pwd

# 列出目录内容
ls                  # 基本列表
ls -l               # 详细列表（权限、大小、时间）
ls -la              # 包含隐藏文件
ls -lh              # 人类可读的文件大小
ls -ltr             # 按时间排序（最新的在最后）

# 切换目录
cd /home/user       # 绝对路径
cd ../              # 上级目录
cd ~                # 家目录
cd -                # 返回上次目录

# 创建目录
mkdir project       # 创建单个目录
mkdir -p a/b/c      # 递归创建多级目录

# ========== 文件操作 ==========

# 创建文件
touch file.txt      # 创建空文件
echo "hello" > file.txt     # 创建并写入内容（覆盖）
echo "world" >> file.txt    # 追加内容

# 查看文件
cat file.txt        # 查看整个文件
less file.txt       # 分页查看（q退出，/搜索）
head -n 10 file.txt # 查看前十行
tail -n 20 file.txt # 查看后二十行
tail -f app.log     # 实时跟踪文件更新

# 复制/移动/删除
cp source dest      # 复制文件
cp -r dir1 dir2     # 递归复制目录
mv old new          # 移动/重命名
rm file.txt         # 删除文件
rm -r directory     # 递归删除目录
rm -rf directory    # 强制删除（危险！）

# 文件信息
wc -l file.txt      # 统计行数
wc -w file.txt      # 统计单词数
wc -c file.txt      # 统计字节数
file file.txt       # 查看文件类型
stat file.txt       # 查看详细状态信息

# ========== 目录大小 ==========
du -sh .            # 当前目录总大小
du -sh *            # 每个文件/目录的大小
du -h --max-depth=1 # 一级子目录大小

# ========== 磁盘空间 ==========
df -h               # 磁盘使用情况（人类可读）
df -i               # inode使用情况
```

### 2.2 权限管理（15分钟）

```bash
# ========== Linux权限模型 ==========
# 每个文件有三组权限：所有者(user) | 所属组(group) | 其他人(other)
# 每组有三种权限：读(r=4) | 写(w=2) | 执行(x=1)

# 查看权限
ls -l file.txt
# -rwxr-xr-- 1 user group 1024 Jan 1 10:00 file.txt
#  └─┬─┘└─┬─┘└─┬─┘
#   user group other
#   rwx  r-x  r--

# ========== 修改权限 ==========
# 数字方式:
chmod 755 script.sh      # rwxr-xr-x (所有者全权限，其他读+执行)
chmod 644 file.txt       # rw-r--r-- (所有者读写，其他只读)
chmod 600 secret.key     # rw------- (只有所有者能读写)

# 常用权限:
# 777: 所有人全权限（危险！一般不要用）
# 755: 目录或可执行文件
# 644: 普通文件
# 600: 私密文件

# 符号方式:
chmod u+x script.sh      # 给所有者添加执行权限
chmod g-w file.txt       # 移除组的写权限
chmod o= file.txt        # 清空其他人的所有权限
chmod a+r file.txt       # 所有人添加读权限

# ========== 修改所有者和组 ==========
chown user:group file.txt           # 修改所有者和组
chown -R user:group directory/      # 递归修改

# ========== 特殊权限 ==========
# SUID(4): 以文件所有者身份执行
# SGID(2): 以文件所属组身份执行
# Sticky(1): 只有文件所有者能删除（用于/tmp）
chmod 1777 /tmp          # Sticky bit

# ========== 默认权限 ==========
umask                    # 查看当前默认权限掩码
umask 022                # 设置掩码（新文件默认644，新目录默认755）
```

### 2.3 进程管理（15分钟）

```bash
# ========== 查看进程 ==========

ps aux                  # 查看所有进程
ps aux | grep nginx     # 查找特定进程
ps -ef                  # 另一种格式

top                     # 实时进程监控（q退出）
# top交互命令:
#   P: 按CPU排序
#   M: 按内存排序
#   1: 显示每个CPU核心
#   k: 杀死进程

htop                    # 更友好的top（需安装）

# ========== 进程树 ==========
pstree                  # 树状显示进程关系
pstree -p               # 显示PID

# ========== 管理进程 ==========
kill PID                # 正常终止
kill -9 PID             # 强制终止（不推荐）
kill -15 PID            # 优雅终止

killall process_name    # 按名称终止所有匹配进程

# ========== 后台运行 ==========
command &               # 后台运行
nohup command &         # 后台运行且不受终端关闭影响
nohup python script.py > output.log 2>&1 &

# jobs: 查看当前终端的后台任务
# fg: 将后台任务调回前台
# bg: 让暂停的任务继续后台运行

# Ctrl+Z: 暂停当前任务
# Ctrl+C: 终止当前任务
```

### 2.4 文本处理三剑客（60分钟）

#### 2.4.1 grep（30分钟核心内容）

```bash
# ========== grep 基础 ==========
# grep = Global Regular Expression Print
# 语法: grep [选项] '模式' 文件名

# 基本搜索
grep "ERROR" app.log                    # 搜索包含ERROR的行
grep -i "error" app.log                 # 忽略大小写
grep -v "DEBUG" app.log                 # 反向匹配（排除DEBUG）
grep -c "ERROR" app.log                 # 统计匹配行数
grep -n "ERROR" app.log                 # 显示行号

# 正则表达式
grep -E "ERROR|WARN" app.log            # 扩展正则（-E）
grep "^2024-01-15" app.log              # 以指定日期开头
grep "\.com$" urls.txt                  # 以.com结尾
grep "[0-9]\{3\}-[0-9]\{4\}" file.txt   # 匹配电话号码格式

# 递归搜索
grep -r "TODO" .                        # 递归搜索目录
grep -rl "TODO" .                       # 只显示文件名
grep -r --include="*.py" "main" .       # 只搜索.py文件
grep -r --exclude="*.log" "ERROR" .     # 排除.log文件

# 上下文显示
grep -A 3 "ERROR" app.log               # 显示匹配行及后3行（After）
grep -B 2 "ERROR" app.log               # 显示匹配行及前2行（Before）
grep -C 5 "ERROR" app.log               # 显示匹配行及前后5行（Context）

# 常见组合
grep ERROR app.log | grep -v IGNORE     # 包含ERROR但不含IGNORE
grep -c "ERROR" app.log                 # 统计ERROR数量
```

#### 2.4.2 awk（25分钟核心内容）

```bash
# ========== awk 基础 ==========
# awk是一个强大的文本处理语言
# 工作方式: 逐行读取 → 按分隔符切分字段 → 执行动作

# 基本语法: awk '条件 {动作}' 文件名
# $0: 整行  $1: 第一个字段  $2: 第二个字段  NF: 字段数量  NR: 行号

# ---- 基础用法 ----

# 打印指定列
awk '{print $1}' access.log             # 打印第1列(IP)
awk '{print $1, $9}' access.log         # 打印第1列和第9列
awk '{print NR, $0}' access.log        # 打印行号和整行

# 条件过滤
awk '$9 == 200 {print $0}' access.log   # 状态码为200的行
awk '$9 >= 400 {print $1, $9, $7}' access.log  # 错误请求
awk '$NF > 1 {print $0}' access.log     # 最后一个字段>1的

# 内置变量
# NR: 当前行号
# NF: 当前行字段数
# $NF: 最后一个字段
# FS: 输入字段分隔符（默认空格）
# OFS: 输出字段分隔符

# 指定分隔符
awk -F',' '{print $1, $3}' data.csv     # CSV文件
awk -F':' '{print $1, $3}' /etc/passwd  # 冒号分隔

# ---- 生产实战：100万行Nginx日志分析 ----

# 1. 统计每个HTTP状态码的数量
awk '{print $9}' access.log | sort | uniq -c | sort -rn

# 2. 找出响应时间超过1秒的慢请求
awk '$NF > 1 {print $0}' access.log > slow_requests.log

# 3. 统计每个URL的访问量
awk '{print $7}' access.log | sort | uniq -c | sort -rn | head -20

# 4. 统计TOP 10 IP
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -10

# 5. 统计每分钟的QPS（请求量）
# Nginx日志时间格式: [15/Jan/2024:10:30:00 +0800]
awk '{print substr($4,2,17)}' access.log | uniq -c

# 6. 计算平均响应时间
awk '{sum+=$NF; count++} END {print sum/count}' access.log

# 7. 计算总流量（GB）
awk '{sum+=$10} END {printf "%.2f GB\n", sum/1024/1024/1024}' access.log

# 8. 统计各时段的请求量
awk '{print substr($4,14,3)":00"}' access.log | sort | uniq -c | sort -n

# 9. 找出产生404的URL
awk '$9 == 404 {print $7}' access.log | sort | uniq -c | sort -rn

# 10. 统计每个IP的平均响应时间
awk '{ip[$1]++; time[$1]+=$NF}
     END {for (i in ip) printf "%s: requests=%d, avg_time=%.2fms\n",
          i, ip[i], time[i]/ip[i]}' access.log | sort -t= -k3 -rn

# 11. 统计独立IP数
awk '{print $1}' access.log | sort -u | wc -l

# 12. 流量TOP 10 URL（按流量排序）
awk '{traffic[$7]+=$10} END {for (url in traffic)
     print traffic[url], url}' access.log | sort -rn | head -10
```

#### 2.4.3 sed（15分钟核心内容）

```bash
# ========== sed 基础 ==========
# sed = Stream Editor（流编辑器）
# 语法: sed [选项] '命令' 文件名

# ---- 替换（最常用）----
# 语法: sed 's/原始/替换/标志' 文件

# 基本替换
sed 's/8080/9090/g' config.conf                # 替换所有8080为9090
sed 's/^#//' config.conf                       # 去掉行首注释符
sed 's/[[:space:]]*$//' file.txt               # 去掉行尾空格

# 标志:
# g: 全局替换（一行中所有匹配）
# i: 忽略大小写
# 数字: 只替换第N个匹配

# ---- 行操作 ----

# 删除行
sed '5d' file.txt              # 删除第5行
sed '5,10d' file.txt           # 删除第5到10行
sed '/^$/d' file.txt           # 删除空行
sed '/^#/d' config.conf        # 删除注释行

# 打印行
sed -n '5p' file.txt           # 只打印第5行
sed -n '10,20p' file.txt       # 打印第10到20行

# 插入和追加
sed '2i\新插入的行' file.txt          # 在第2行前插入
sed '2a\新追加的行' file.txt          # 在第2行后追加

# ---- 实际应用 ----

# 1. 替换配置文件中的端口号（-i直接修改文件）
sed -i 's/port=8080/port=9090/g' application.conf

# 2. 删除文件中的空行和注释行
sed -i '/^$/d; /^#/d' config.conf

# 3. 给文件每行加行号
sed = file.txt | sed 'N;s/\n/\t/'

# 4. 提取IP地址
sed -n 's/.*from \(.*\) port.*/\1/p' ssh.log

# 5. JSON中的简单替换
sed 's/"status": "pending"/"status": "completed"/g' data.json

# 6. 在匹配行前后添加内容
sed '/ERROR/i\===== 以下是错误日志 =====' app.log
sed '/ERROR/a\----- 错误日志结束 -----' app.log

# 7. 删除HTML标签（简单情况）
sed 's/<[^>]*>//g' page.html

# 8. 多条件处理
sed -e 's/foo/bar/g' -e '/^$/d' -e 's/^\s*//' file.txt

# ---- sed地址范围 ----
sed '2,5s/old/new/g' file.txt      # 只在第2-5行内替换
sed '/start/,/end/s/old/new/g' file.txt  # 从start到end的行内替换
```

### 2.5 管道、重定向与常用组合（15分钟）

```bash
# ========== 管道 ==========
# | 将前一个命令的输出作为后一个命令的输入

# 常见的管道组合
cat access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head -10
#   读取文件   →  提取IP    →  排序  →  统计  →  逆序排列 →  前10

# ========== 标准输入输出重定向 ==========
# stdin(0): 标准输入
# stdout(1): 标准输出
# stderr(2): 标准错误

command > file.txt          # 输出重定向（覆盖）
command >> file.txt         # 输出重定向（追加）
command 2> error.log        # 错误重定向
command > out.log 2>&1      # 输出和错误都重定向到同一文件
command &> all.log          # 同上（简洁写法）

command < input.txt         # 输入重定向

# ========== 常用命令组合 ==========

# 查找大文件
find . -type f -size +100M -exec ls -lh {} \;

# 查找10天前的日志并删除
find ./logs -name "*.log" -mtime +10 -delete

# 统计代码行数
find . -name "*.py" | xargs wc -l | tail -1

# 批量重命名
for f in *.txt; do mv "$f" "${f%.txt}.md"; done

# 查找并压缩
find ./logs -name "*.log" -mtime +30 -exec gzip {} \;

# 查看端口占用
netstat -tlnp | grep :8080
lsof -i :8080

# 查看最耗CPU的进程
ps aux --sort=-%cpu | head -10

# 查看最耗内存的进程
ps aux --sort=-%mem | head -10
```

---

## 三、课堂练习（45分钟）

### 练习：纯命令行日志分析挑战

**规则：禁止使用Python，只能用bash命令完成以下任务**

提供1万行模拟Nginx日志，完成以下分析：

```bash
# 准备工作：生成模拟日志（如果还没有的话，教师会提供）
# 假设日志文件名为: access.log

# ========== 任务1：统计状态码分布 ==========
echo "=== 状态码分布 ==="
awk '{print $9}' access.log | sort | uniq -c | sort -rn

# ========== 任务2：TOP 10 IP ==========
echo "=== TOP 10 IP ==="
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -10

# ========== 任务3：每分钟QPS变化趋势 ==========
echo "=== 每分钟QPS ==="
awk '{print substr($4,2,17)}' access.log | uniq -c

# ========== 任务4：找出所有慢请求（响应时间>1秒）==========
echo "=== 慢请求 ==="
# 假设最后一列是响应时间（秒）
awk '$NF > 1 {print $0}' access.log | wc -l
echo "慢请求数量: $(awk '$NF > 1' access.log | wc -l)"

# ========== 任务5：错误率统计 ==========
echo "=== 错误率 ==="
total=$(wc -l < access.log)
errors=$(awk '$9 >= 400' access.log | wc -l)
echo "总请求: $total"
echo "错误请求: $errors"
echo "错误率: $(echo "scale=2; $errors * 100 / $total" | bc)%"

# ========== 任务6：最热门的5个URL ==========
echo "=== TOP 5 URL ==="
awk '{print $7}' access.log | sort | uniq -c | sort -rn | head -5

# ========== 任务7：每小时请求量分布 ==========
echo "=== 每小时请求量 ==="
awk '{print substr($4,14,3)}' access.log | sort | uniq -c | sort -n

# ========== 任务8：各HTTP方法使用次数 ==========
echo "=== HTTP方法分布 ==="
awk -F'"' '{print $2}' access.log | awk '{print $1}' | sort | uniq -c | sort -rn

# ========== 任务9：大于1MB的响应统计 ==========
echo "=== 大响应(>1MB)统计 ==="
awk '$10 > 1048576 {count++; sum+=$10} END {
    print "数量:", count;
    printf "总流量: %.2f MB\n", sum/1024/1024
}' access.log

# ========== 任务10：生成简易报告 ==========
echo "=== 日志分析报告 ===" > report.txt
echo "生成时间: $(date)" >> report.txt
echo "" >> report.txt
echo "总请求数: $(wc -l < access.log)" >> report.txt
echo "独立IP数: $(awk '{print $1}' access.log | sort -u | wc -l)" >> report.txt
echo "" >> report.txt
echo "状态码分布:" >> report.txt
awk '{print $9}' access.log | sort | uniq -c | sort -rn >> report.txt
echo "" >> report.txt
echo "TOP 5 IP:" >> report.txt
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -5 >> report.txt

cat report.txt
```

### 进阶挑战

```bash
# 挑战1：用sed提取access.log中所有POST请求的URL
sed -n 's/.*"POST \(.*\) HTTP.*/\1/p' access.log

# 挑战2：用awk统计每个URL的总流量（MB）
awk '{traffic[$7]+=$10} END {
    for(url in traffic) {
        printf "%.2f MB\t%s\n", traffic[url]/1024/1024, url
    }
}' access.log | sort -rn | head -5

# 挑战3：用一行命令找出访问最多的3个IP和它们的请求次数
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -3 | \
    awk '{print "IP: "$2", 请求: "$1"次"}'

# 挑战4：用grep统计出现"bot"关键词的请求占比
echo "$(grep -ci 'bot' access.log) / $(wc -l < access.log)" | \
    awk -F/ '{printf "Bot占比: %.2f%%\n", ($1/$2)*100}'
```

---

## 四、课后作业

### 必做作业

**1. 搭建Ubuntu Server虚拟机**

- 安装VirtualBox，创建Ubuntu Server 22.04虚拟机
- 最小化安装（不要GUI）
- 配置网络（桥接或NAT）
- 实现SSH远程连接

**2. 纯命令行环境完成以下任务**

```bash
# 任务1: 安装MySQL 8.0
sudo apt update
sudo apt install mysql-server -y
sudo systemctl enable mysql
sudo systemctl start mysql

# 任务2: 创建数据库和用户
sudo mysql -e "CREATE DATABASE testdb;"
sudo mysql -e "CREATE USER 'student'@'localhost' IDENTIFIED BY 'password123';"
sudo mysql -e "GRANT ALL PRIVILEGES ON testdb.* TO 'student'@'localhost';"

# 任务3: 导入SQL数据
mysql -u student -ppassword123 testdb < ecommerce_schema.sql

# 任务4: 执行SQL查询
mysql -u student -ppassword123 testdb -e "
    SELECT city, COUNT(*) as cnt
    FROM users
    GROUP BY city
    ORDER BY cnt DESC
    LIMIT 5;
"
```

**3. 命令行文本处理练习（200条命令）**

- 使用grep完成20个不同的搜索任务
- 使用awk完成20个不同的数据提取任务
- 使用sed完成20个不同的文本替换任务
- 使用管道组合完成10个综合任务

### 选做作业

**编写一个shell脚本监控系统状态：**

```bash
#!/bin/bash
# monitor.sh - 系统监控脚本

THRESHOLD_CPU=80
THRESHOLD_MEM=80
THRESHOLD_DISK=80
LOG_FILE="/var/log/system_monitor.log"

timestamp() {
    date '+%Y-%m-%d %H:%M:%S'
}

# CPU使用率
cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
if (( $(echo "$cpu_usage > $THRESHOLD_CPU" | bc -l) )); then
    echo "[$(timestamp)] ⚠️ CPU使用率过高: ${cpu_usage}%" >> $LOG_FILE
fi

# 内存使用率
mem_usage=$(free | grep Mem | awk '{printf "%.1f", $3/$2 * 100}')
if (( $(echo "$mem_usage > $THRESHOLD_MEM" | bc -l) )); then
    echo "[$(timestamp)] ⚠️ 内存使用率过高: ${mem_usage}%" >> $LOG_FILE
fi

# 磁盘使用率
disk_usage=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if (( disk_usage > THRESHOLD_DISK )); then
    echo "[$(timestamp)] ⚠️ 磁盘使用率过高: ${disk_usage}%" >> $LOG_FILE
fi

echo "[$(timestamp)] CPU:${cpu_usage}% MEM:${mem_usage}% DISK:${disk_usage}%" >> $LOG_FILE
```

---

## 五、Linux命令速查表

| 分类 | 命令 | 用途 |
|------|------|------|
| 导航 | cd, ls, pwd, mkdir | 目录操作 |
| 文件 | cat, less, head, tail, touch | 查看文件 |
| 操作 | cp, mv, rm, find | 文件操作 |
| 权限 | chmod, chown, umask | 权限管理 |
| 进程 | ps, top, kill, nohup | 进程管理 |
| 文本 | grep, awk, sed | 文本处理 |
| 管道 | \|, >, >>, < | 重定向 |
| 网络 | curl, wget, netstat, ss | 网络操作 |
| 磁盘 | df, du, mount | 磁盘管理 |
| 压缩 | tar, gzip, gunzip, zip | 压缩解压 |

---

## 六、参考资源

- [鸟哥的Linux私房菜](http://linux.vbird.org/)
- [Linux命令行大全](https://linuxcommand.org/)
- [awk入门教程](https://www.gnu.org/software/gawk/manual/gawk.html)
- [sed入门教程](https://www.gnu.org/software/sed/manual/sed.html)
- [explainshell.com - 命令解释器](https://explainshell.com/)