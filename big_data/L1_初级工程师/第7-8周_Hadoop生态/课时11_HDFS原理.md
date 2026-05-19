# 课时11：大数据概念与HDFS原理

> **课时时长**：8小时（理论3h + 实验3h + 练习2h）
>
> **难度等级**：⭐⭐⭐ 入门核心

---

## 一、教学目标

1. **理解大数据核心概念**：掌握大数据的4V特征，能用自己的话解释为什么传统方案处理不了大数据
2. **掌握HDFS架构原理**：能手绘HDFS架构图，解释NameNode、DataNode、SecondaryNameNode的职责
3. **理解数据块与副本策略**：掌握Block大小设置（128MB）的原因，副本放置策略
4. **能手绘HDFS读写流程图**：标注每一步角色的RPC调用和数据传输
5. **能独立部署HDFS集群**：使用Docker Compose部署3节点集群，完成Shell操作
6. **理解联邦HDFS与高可用架构**：了解生产级HDFS的演进方向

---

## 二、教学内容

### 2.1 大数据4V特征与起源（30min）

**Google三篇论文开启的大数据时代：**

| 论文 | 年份 | 解决的问题 | 对应开源实现 |
|------|------|------------|-------------|
| GFS (Google File System) | 2003 | 大规模分布式文件存储 | HDFS |
| MapReduce | 2004 | 大规模分布式计算 | Hadoop MapReduce |
| BigTable | 2006 | 大规模分布式结构化存储 | HBase |

**大数据的4V特征：**

```
Volume（海量）:    TB级→PB级数据量，传统单机无法存储和处理
Velocity（高速）:   数据产生速度快，需要实时/近实时处理
Variety（多样）:   结构化(DB表) + 半结构化(JSON/XML) + 非结构化(日志/图片/视频)
Value（价值）:     数据密度低，需要通过分析提取有价值的信息
```

**一个生动的案例——电商平台一天的数据：**

```
用户行为日志:        500GB/天  (浏览、点击、加购、收藏)
订单交易数据:        50GB/天   (100万笔订单)
商品数据:            10GB/天   (新增/修改的商品)
图片视频:            2TB/天    (商品图片、用户评价图片)

传统方案(单机MySQL)的问题:
  - 磁盘: 单机最大2TB，存储不了2周的数据
  - 查询: 扫描500GB日志，单机需要数小时
  - 可靠性: 单机宕机，所有数据不可用
  
分布式方案(HDFS)的优势:
  - 多台机器组成集群，轻松扩展
  - 数据分块并行处理
  - 多副本保证高可用
```

---

### 2.2 HDFS架构设计（60min）

**HDFS核心设计思想（来自GFS论文）：**

```
设计假设:
  1. 硬件故障是常态，不是例外
  2. 文件以大文件为主（GB~TB级别）
  3. 写入一次，多次读取（Write Once, Read Many）
  4. 流式数据访问，追求高吞吐量而非低延迟
```

**HDFS架构图（必画）：**

```
┌──────────────────────────────────────────────────────────┐
│                      客户端 (Client)                       │
│            (应用程序通过HDFS API读写文件)                    │
└─────┬──────────────────┬──────────────────┬──────────────┘
      │ 元数据操作        │ 读数据请求        │ 写数据请求
      ▼                  ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  NameNode    │  │  DataNode-1  │  │  DataNode-2  │  ...
│  (主节点)     │  │  (从节点)     │  │  (从节点)     │
│              │  │              │  │              │
│ - 管理文件   │  │ - 存储数据块  │  │ - 存储数据块  │
│   命名空间    │  │ - 执行读写   │  │ - 执行读写   │
│ - 维护文件到 │  │ - 定期向     │  │ - 定期向     │
│   Block映射  │  │   NameNode   │  │   NameNode   │
│ - 管理副本   │  │   发送心跳    │  │   发送心跳    │
│   放置策略    │  │   和块报告    │  │   和块报告    │
└──────────────┘  └──────────────┘  └──────────────┘
      ▲
      │ fsimage + edits log 定期合并
┌──────────────┐
│  Secondary   │
│  NameNode    │
│  (辅助节点)   │
│ - 定期合并   │
│   fsimage和  │
│   edits log  │
│ - 不是热备！ │
└──────────────┘
```

**各组件的核心职责：**

| 组件 | 职责 | 关键数据 | 故障影响 |
|------|------|----------|----------|
| NameNode | 管理文件系统命名空间；维护文件→Block映射；管理副本策略；处理客户端请求 | fsimage(元数据镜像) + edits(操作日志) | 宕机则整个集群不可用 |
| DataNode | 存储实际数据块；执行读写操作；定期向NameNode汇报(心跳+块报告) | 磁盘上的Block文件和校验和 | 单个宕机不影响，数据可从副本恢复 |
| SecondaryNameNode | 定期合并fsimage和edits log；减少NameNode重启时间 | 合并后的fsimage | 宕机不影响（不是热备） |

**Block（数据块）概念：**

```
为什么HDFS的Block是128MB（传统文件系统一般是4KB）？

1. 减少寻址开销：
   - 寻址时间约10ms，传输速率约100MB/s
   - 如果Block太小(4KB)，寻址时间占比过高
   - 最佳Block大小 = 让寻址时间约为传输时间的1%
   - 即：寻址10ms ≈ 传输100MB所需时间的1%
   → Block大小约128MB

2. 减少NameNode元数据存储压力：
   假设有1TB的文件：
   - Block=128MB → 约8000个Block → NameNode内存占用小
   - Block=4KB → 约2.5亿个Block → NameNode内存爆炸
```

---

### 2.3 HDFS写数据流程（必背）（40min）

**完整写流程（7步）：**

```
步骤1: 客户端向NameNode发起创建文件请求
        └─ RPC: create(path, permission, clientName)

步骤2: NameNode检查：
        ├─ 文件是否已存在？（存在则抛异常）
        ├─ 客户端是否有写权限？
        └─ 父目录是否存在？
            └─ 通过检查 → 在edits log中记录创建操作

步骤3: 客户端开始写入第一个Block
        └─ 向NameNode请求DataNode列表
        └─ NameNode根据副本放置策略返回DataNode列表

步骤4: NameNode返回DataNode列表（副本放置策略）：
        ┌─ 第一个副本：与客户端同机架的节点（网络最近）
        ├─ 第二个副本：不同机架的节点（跨机架容灾）
        └─ 第三个副本：与第二个副本同机架的不同节点

步骤5: 客户端建立数据传输管道（Pipeline）：
        客户端 ──→ dn1 ──→ dn2 ──→ dn3
        （数据包沿着管道流式传输）

步骤6: 数据以Packet为单位传输（默认64KB）：
        ┌─ 客户端将数据写入本地缓存
        ├─ 缓存满一个Packet → 发送给dn1
        ├─ dn1收到后 → 写入本地磁盘 → 转发给dn2
        ├─ dn2收到后 → 写入本地磁盘 → 转发给dn3
        └─ dn3收到后 → 写入本地磁盘 → 返回ACK

步骤7: ACK沿管道反向传播：
        dn3 → ACK → dn2 → ACK → dn1 → ACK → 客户端
        └─ 所有副本写入成功 → 客户端向NameNode确认
        └─ NameNode在内存中更新Block映射关系

重复步骤3-7写入下一个Block，直到文件完全写入。
```

**写流程图（简化版）：**

```
客户端 ──(1)创建文件请求──→ NameNode
                               │
                          (2)检查权限/路径
                               │
                          (3)返回DataNode列表
                      (dn1: rack1, dn2: rack2, dn3: rack2)
                               │
客户端 ──(4)建立Pipeline──→ dn1 ──(5)转发──→ dn2 ──(6)转发──→ dn3
  │                          │                │                │
  └──(8)ACK────────────────←┘               ←┘               ←┘
                               │
                          (9)通知NameNode写入完成
                               │
                          NameNode更新元数据
```

---

### 2.4 HDFS读数据流程（30min）

**完整读流程：**

```
步骤1: 客户端向NameNode发起读文件请求
        └─ RPC: getBlockLocations(path)

步骤2: NameNode检查权限后，返回文件的所有Block位置信息
        └─ 返回: BlockID列表 + 每个Block所在的DataNode列表
        └─ DataNode列表按"网络距离"排序（就近原则）

步骤3: 客户端选择最近的DataNode读取Block
        └─ 建立Socket连接，流式读取

步骤4: 读取第一个Block后，关闭与当前DataNode的连接
        └─ 切换到下一个Block所在的最优DataNode

步骤5: 重复步骤3-4，读取所有Block
        └─ 如果读取过程中DataNode故障，尝试下一个副本

步骤6: 所有Block读取完毕，客户端组装完整文件
```

**读流程图：**

```
客户端 ──(1)打开文件请求──→ NameNode
                               │
                          (2)返回Block位置列表
                      [Blk1: dn1,dn2,dn3]
                      [Blk2: dn2,dn3,dn1]
                      [Blk3: dn3,dn1,dn2]
                               │
                    ┌──────────┼──────────┐
                    ▼          ▼          ▼
                   dn1        dn2        dn3
              (读取Blk1)  (读取Blk2)  (读取Blk3)
                    │          │          │
                    └──────────┼──────────┘
                               ▼
                          客户端组装完整文件
```

---

### 2.5 联邦HDFS与高可用（30min）

**传统HDFS的单点问题：**

```
NameNode是单点故障(SPOF):
  - NameNode宕机 → 整个集群不可用
  - 需要手动恢复（从SecondaryNameNode获取fsimage，回放edits log）
  - 恢复时间可能长达30分钟以上
```

**HDFS高可用（HA）架构：**

```
┌─────────────────────────────────────────────┐
│            ZooKeeper集群 (奇数台)              │
│         ┌─────┐  ┌─────┐  ┌─────┐          │
│         │ ZK1 │  │ ZK2 │  │ ZK3 │          │
│         └──┬──┘  └──┬──┘  └──┬──┘          │
└────────────┼────────┼────────┼──────────────┘
             │        │        │
        ┌────┴────────┴────────┴────┐
        │      JournalNode集群       │
        │   (奇数台，存储edits log)   │
        │   JN1    JN2    JN3       │
        └────────┬────────┬─────────┘
                 │        │
     ┌───────────┴┐      ┌└───────────┐
     │ Active     │      │ Standby    │
     │ NameNode   │      │ NameNode   │
     │            │      │            │
     │ - 处理请求 │      │ - 同步     │
     │ - 写edits  │      │   edits    │
     │  到JN      │      │ - 随时接管 │
     └────────────┘      └────────────┘
```

**联邦HDFS（Federation）：**

```
解决问题: 单NameNode内存成为瓶颈

方案: 多个NameNode分管不同目录
  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │ NN-1     │  │ NN-2     │  │ NN-3     │
  │ /data    │  │ /user    │  │ /tmp     │
  └────┬─────┘  └────┬─────┘  └────┬─────┘
       │             │             │
       └─────────────┼─────────────┘
                     │
          共享的DataNode集群
```

---

## 三、实验任务：Docker Compose部署HDFS集群

### 3.1 docker-compose-bigdata.yml

```yaml
version: "3.8"

services:
  namenode:
    image: apache/hadoop:3.3.6
    hostname: namenode
    container_name: namenode
    environment:
      - HADOOP_HOME=/opt/hadoop
      - ENSURE_NAMENODE_DIR=/tmp/hadoop-hadoop/dfs/name
    ports:
      - "9870:9870"
      - "8020:8020"
    volumes:
      - namenode-data:/opt/hadoop/data
    command: ["hdfs", "namenode"]
    networks:
      - hadoop-net

  datanode1:
    image: apache/hadoop:3.3.6
    hostname: datanode1
    container_name: datanode1
    environment:
      - HADOOP_HOME=/opt/hadoop
      - CORE_CONF_fs_defaultFS=hdfs://namenode:8020
    volumes:
      - dn1-data:/opt/hadoop/data
    command: ["hdfs", "datanode"]
    depends_on:
      - namenode
    networks:
      - hadoop-net

  datanode2:
    image: apache/hadoop:3.3.6
    hostname: datanode2
    container_name: datanode2
    environment:
      - HADOOP_HOME=/opt/hadoop
      - CORE_CONF_fs_defaultFS=hdfs://namenode:8020
    volumes:
      - dn2-data:/opt/hadoop/data
    command: ["hdfs", "datanode"]
    depends_on:
      - namenode
    networks:
      - hadoop-net

  datanode3:
    image: apache/hadoop:3.3.6
    hostname: datanode3
    container_name: datanode3
    environment:
      - HADOOP_HOME=/opt/hadoop
      - CORE_CONF_fs_defaultFS=hdfs://namenode:8020
    volumes:
      - dn3-data:/opt/hadoop/data
    command: ["hdfs", "datanode"]
    depends_on:
      - namenode
    networks:
      - hadoop-net

volumes:
  namenode-data:
  dn1-data:
  dn2-data:
  dn3-data:

networks:
  hadoop-net:
    driver: bridge
```

### 3.2 部署步骤

```bash
# 步骤1: 启动HDFS集群
docker-compose -f docker-compose-bigdata.yml up -d

# 步骤2: 验证集群状态
docker exec namenode hdfs dfsadmin -report

# 步骤3: 进入NameNode容器
docker exec -it namenode bash

# 步骤4: 查看Web UI
# 浏览器访问: http://localhost:9870
```

### 3.3 HDFS Shell命令实战

```bash
# ========== 基础文件操作 ==========

# 1. 查看根目录
hdfs dfs -ls /

# 2. 创建目录
hdfs dfs -mkdir -p /user/student/data
hdfs dfs -mkdir -p /user/student/output

# 3. 上传本地文件到HDFS
echo "Hello Big Data" > /tmp/test.txt
hdfs dfs -put /tmp/test.txt /user/student/data/

# 4. 查看文件内容
hdfs dfs -cat /user/student/data/test.txt

# 5. 查看文件末尾
hdfs dfs -tail /user/student/data/test.txt

# 6. 从HDFS下载文件
hdfs dfs -get /user/student/data/test.txt /tmp/downloaded.txt

# 7. 复制文件（HDFS内部）
hdfs dfs -cp /user/student/data/test.txt /user/student/data/test_copy.txt

# 8. 移动/重命名文件
hdfs dfs -mv /user/student/data/test_copy.txt /user/student/data/renamed.txt

# 9. 查看文件大小
hdfs dfs -du -h /user/student/data/

# 10. 统计目录信息
hdfs dfs -count /user/student/data/

# ========== 权限管理 ==========

# 11. 修改文件权限
hdfs dfs -chmod 755 /user/student/data/test.txt

# 12. 修改文件所有者
hdfs dfs -chown student:student /user/student/data/test.txt

# 13. 查看文件详细信息
hdfs dfs -stat "%n %b %o %r %Y" /user/student/data/test.txt
# 输出: 文件名 大小 Block大小 副本数 修改时间

# ========== 数据块信息 ==========

# 14. 上传大文件观察分块
dd if=/dev/zero of=/tmp/bigfile bs=1M count=300
hdfs dfs -put /tmp/bigfile /user/student/data/

# 15. 查看文件的Block信息（重点！）
hdfs fsck /user/student/data/bigfile -files -blocks -locations

# 输出示例:
# /user/student/data/bigfile 314572800 bytes, 3 block(s):
# 0. BP-xxxx:blk_1073741825_1001 len=134217728 Live_repl=3 [dn1:9866,dn2:9866,dn3:9866]
# 1. BP-xxxx:blk_1073741826_1002 len=134217728 Live_repl=3 [dn2:9866,dn3:9866,dn1:9866]
# 2. BP-xxxx:blk_1073741827_1003 len=46137344  Live_repl=3 [dn3:9866,dn1:9866,dn2:9866]

# ========== 副本管理 ==========

# 16. 设置文件副本数
hdfs dfs -setrep -w 2 /user/student/data/test.txt

# 17. 删除文件
hdfs dfs -rm /user/student/data/test.txt

# 18. 删除目录（递归）
hdfs dfs -rm -r /user/student/output/

# 19. 移动到回收站
hdfs dfs -rm -skipTrash /user/student/data/renamed.txt

# ========== 管理命令 ==========

# 20. 查看集群状态
hdfs dfsadmin -report

# 21. 进入安全模式
hdfs dfsadmin -safemode enter
hdfs dfsadmin -safemode leave
hdfs dfsadmin -safemode get

# 22. 刷新节点
hdfs dfsadmin -refreshNodes

# 23. 查看HDFS使用情况
hdfs dfs -df -h

# 24. 检查文件健康状态
hdfs fsck / -files -blocks -locations
```

---

## 四、课堂练习（90min）

### 练习1：手绘HDFS读写流程图（30min）

```
要求:
  1. 在纸上画出HDFS写数据完整流程图
  2. 标注每一步的角色（NameNode/DataNode/Client）
  3. 标注每一步的RPC调用和数据类型
  4. 标注Pipeline管道建立过程
  5. 标注ACK确认机制

评分标准:
  - 步骤完整（7步不缺）: 40%
  - 角色标注正确: 20%
  - 数据流方向正确: 20%
  - 副本放置策略说明: 20%
```

### 练习2：HDFS Shell操作闯关（30min）

```bash
# 关卡1：创建以下目录结构
#   /data/logs/2024/01/
#   /data/logs/2024/02/
#   /data/db/user/
#   /data/db/order/

# 关卡2：生成一个200MB的测试文件并上传到/data/logs/2024/01/
#   (提示: dd if=/dev/urandom bs=1M count=200)

# 关卡3：查看该文件的Block分布，回答：
#   - 一共几个Block？
#   - 每个Block的副本分布在哪些DataNode上？
#   - Block大小是多少？

# 关卡4：修改文件副本数为1，再次查看Block分布
#   - 观察副本数变化
#   - 观察DataNode分布变化

# 关卡5：删除/data/logs/2024/01/目录下的所有文件
#   - 确认已删除
#   - 检查HDFS使用空间变化
```

### 练习3：故障模拟观察（30min）

```bash
# 任务1: 停止一个DataNode
docker stop datanode3

# 观察：
# 1. hdfs dfsadmin -report 的输出变化
# 2. Web UI 上的变化
# 3. 副本数不足的Block如何表现

# 任务2: 等待2分钟后重启DataNode
docker start datanode3

# 观察：
# 1. 副本自动恢复的过程
# 2. hdfs fsck 输出的变化

# 任务3: 在DataNode停止期间上传新文件
# - 观察副本策略如何调整
# - DataNode恢复后副本如何重新分布
```

---

## 五、课后作业

### 作业1：HDFS Shell命令30条（必做）

要求：
- 必须手打（不能复制粘贴）
- 截图每条命令的执行结果
- 整理成Markdown文档提交到GitHub

### 作业2：手绘HDFS读写流程图（必做）

要求：
- 用白纸手绘（不要用画图工具）
- 标注每一步的角色和RPC调用
- 拍照提交到GitHub
- 下次课随机抽3人上台讲解

### 作业3：深入思考题（选做）

```yaml
题目1: NameNode内存估算
  场景: HDFS集群存储了100TB数据，平均文件大小100MB
  请估算: NameNode需要多少内存来存储元数据？
  已知: 每个Block的元数据约150字节

题目2: 小文件问题
  场景: HDFS上存了1000万个1KB的小文件
  问题: 会有什么问题？为什么说"HDFS不适合存小文件"？
  请从NameNode内存和MapReduce性能两个角度分析

题目3: 副本放置策略设计
  场景: 你的集群部署在北京和上海两个机房
  要求: 保证任意一个机房故障时数据不丢失
  请设计: 3副本的放置策略
```

### 作业4：预习准备

阅读 [课时12_MapReduce原理与实战]() 的预习材料：
- MapReduce编程模型简介
- 理解Map和Reduce的概念

---

## 六、参考资料

1. **GFS论文**：*The Google File System (2003)* — HDFS的设计原型
2. **Hadoop官方文档**：https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html
3. **《Hadoop权威指南》**：第3章 Hadoop分布式文件系统
4. **Docker Hub**：https://hub.docker.com/r/apache/hadoop