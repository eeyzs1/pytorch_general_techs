# 课时12：MapReduce原理与实战

> **课时时长**：8小时（理论3h + 编码实战3h + 练习2h）
>
> **难度等级**：⭐⭐⭐⭐ 核心重点

---

## 一、教学目标

1. **理解MapReduce编程模型**：掌握"分而治之"思想，能解释Map和Reduce两个阶段的作用
2. **掌握Shuffle核心机制**：理解Partition、Sort、Group三个核心过程
3. **能独立编写MapReduce程序**：WordCount的每一行代码都能解释清楚
4. **理解Combiner和Partitioner**：掌握优化思路和适用场景
5. **能在集群上运行MapReduce作业**：编译→打包→提交→查看结果
6. **理解MapReduce vs Spark的本质差异**：为后续Spark学习做铺垫

---

## 二、教学内容

### 2.1 "分而治之"思想（30min）

**生活中的MapReduce——统计全校学生身高：**

```
传统方法（单机串行）:
  一个老师拿着全校5000名学生的名单，逐个记录身高
  → 耗时: 5000 × 30秒 = 约42小时 → 不可行！

MapReduce方法（分布式并行）:
  Step 1 - Map阶段（分）:
    把5000名学生分成50组，每组100人
    50个老师同时测量各组学生的身高
    每组产生: [("男", 175), ("女", 162), ("男", 180), ...]
    → 耗时: 100 × 30秒 = 50分钟（并行）

  Step 2 - Shuffle阶段（洗牌）:
    把Map的输出按性别分组:
    男生组: [175, 180, 170, 185, ...]
    女生组: [162, 165, 158, 170, ...]

  Step 3 - Reduce阶段（合）:
    2个老师分别计算:
    男老师: 男生身高平均值 = sum(男生身高)/男同学数量
    女老师: 女生身高平均值 = sum(女生身高)/女同学数量
    → 耗时: 1分钟（并行）
```

**MapReduce核心思想：**

```
输入数据 → Map(映射) → Shuffle(混洗) → Reduce(归约) → 输出结果

Map:    并行处理每个数据片段，转换为<Key, Value>对
Shuffle: 将相同Key的数据汇集到一起（最复杂、最耗时的阶段）
Reduce:  对每个Key的数据进行聚合计算
```

---

### 2.2 MapReduce编程模型详解（60min）

**数据流转全过程（以WordCount为例）：**

```
输入数据（HDFS上的文本文件）:
  File1: "Hello World Hello Hadoop"
  File2: "Hello MapReduce World"

┌──────────── InputFormat ────────────┐
│ 将文件切分为InputSplit（每个Split≈一个Block） │
│ Split1: "Hello World Hello Hadoop"         │
│ Split2: "Hello MapReduce World"            │
└────────────────┬───────────────────┘
                 ▼
┌──────────── Map Phase ──────────────┐
│ LineRecordReader逐行读取:                   │
│                                            │
│ Map Task 1处理Split1:                      │
│   输入: (0, "Hello World Hello Hadoop")    │
│   输出: ("Hello",1), ("World",1),          │
│         ("Hello",1), ("Hadoop",1)           │
│                                            │
│ Map Task 2处理Split2:                      │
│   输入: (0, "Hello MapReduce World")       │
│   输出: ("Hello",1), ("MapReduce",1),      │
│         ("World",1)                        │
└────────────────┬───────────────────┘
                 ▼
┌────────── Shuffle Phase ────────────┐
│ 1. Partition（分区）:                      │
│    根据Key的hash值决定去哪个Reducer         │
│    (默认: hash(Key) % numReducers)         │
│                                            │
│ 2. Sort（排序）:                           │
│    每个Reducer收到的数据按Key排序           │
│                                            │
│ 3. Group（分组）:                          │
│    将相同Key的Value合并                     │
│                                            │
│ Reducer 1收到:                             │
│   ("Hadoop", [1])                         │
│   ("Hello", [1,1,1])                      │
│   ("MapReduce", [1])                      │
│                                            │
│ Reducer 2收到:                             │
│   ("World", [1,1])                        │
└────────────────┬───────────────────┘
                 ▼
┌────────── Reduce Phase ─────────────┐
│ Reduce Task 1:                             │
│   ("Hadoop", [1]) → sum → ("Hadoop", 1)    │
│   ("Hello", [1,1,1]) → sum → ("Hello", 3) │
│   ("MapReduce", [1]) → sum →               │
│                      ("MapReduce", 1)      │
│                                            │
│ Reduce Task 2:                             │
│   ("World", [1,1]) → sum → ("World", 2)    │
└────────────────┬───────────────────┘
                 ▼
┌────────── Output Phase ─────────────┐
│ OutputFormat将结果写入HDFS                  │
│ part-r-00000:                             │
│   Hadoop  1                               │
│   Hello   3                               │
│   MapReduce 1                             │
│                                           │
│ part-r-00001:                             │
│   World   2                               │
└───────────────────────────────────────────┘
```

**MapReduce中的Key/Value类型（必记）：**

| 阶段 | 输入Key | 输入Value | 输出Key | 输出Value |
|------|---------|-----------|---------|-----------|
| Map | LongWritable(行偏移) | Text(一行文本) | Text(单词) | IntWritable(1) |
| Combine | Text | IntWritable | Text | IntWritable |
| Reduce | Text | Iterable\<IntWritable\> | Text | IntWritable |

---

### 2.3 完整WordCount代码（Java）（90min）

**完整可运行的项目结构：**

```
wordcount/
├── src/main/java/com/bigdata/
│   └── WordCount.java
├── pom.xml
└── input/
    └── sample.txt
```

**pom.xml（Maven依赖配置）：**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.bigdata</groupId>
    <artifactId>wordcount</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>

    <properties>
        <maven.compiler.source>8</maven.compiler.source>
        <maven.compiler.target>8</maven.compiler.target>
        <hadoop.version>3.3.6</hadoop.version>
    </properties>

    <dependencies>
        <!-- Hadoop Common -->
        <dependency>
            <groupId>org.apache.hadoop</groupId>
            <artifactId>hadoop-common</artifactId>
            <version>${hadoop.version}</version>
            <scope>provided</scope>
        </dependency>

        <!-- Hadoop MapReduce Client -->
        <dependency>
            <groupId>org.apache.hadoop</groupId>
            <artifactId>hadoop-mapreduce-client-core</artifactId>
            <version>${hadoop.version}</version>
            <scope>provided</scope>
        </dependency>

        <!-- Hadoop HDFS Client -->
        <dependency>
            <groupId>org.apache.hadoop</groupId>
            <artifactId>hadoop-hdfs-client</artifactId>
            <version>${hadoop.version}</version>
            <scope>provided</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-jar-plugin</artifactId>
                <version>3.2.0</version>
                <configuration>
                    <archive>
                        <manifest>
                            <mainClass>com.bigdata.WordCount</mainClass>
                        </manifest>
                    </archive>
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-shade-plugin</artifactId>
                <version>3.3.0</version>
                <executions>
                    <execution>
                        <phase>package</phase>
                        <goals>
                            <goal>shade</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
```

**WordCount.java（完整代码，逐行可讲解）：**

```java
package com.bigdata;

import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

/**
 * 经典MapReduce WordCount程序
 * 这是每个大数据工程师必须能手写的代码
 *
 * 功能: 统计文本文件中每个单词的出现次数
 * 输入: HDFS上的文本文件
 * 输出: HDFS上的<单词, 计数>文件
 */
public class WordCount extends Configured implements Tool {

    /**
     * Mapper类: 负责将输入文本分解为<单词, 1>键值对
     *
     * 泛型参数说明:
     *   LongWritable  → 输入Key类型（行偏移量）
     *   Text          → 输入Value类型（一行文本）
     *   Text          → 输出Key类型（单词）
     *   IntWritable   → 输出Value类型（计数1）
     */
    public static class TokenizerMapper
            extends Mapper<LongWritable, Text, Text, IntWritable> {

        // 预先创建对象，避免反复new（序列化优化）
        private final static IntWritable one = new IntWritable(1);
        private Text word = new Text();

        /**
         * map方法: 每读取一行文本就调用一次
         *
         * @param key     当前行在文件中的偏移量（通常不使用）
         * @param value   当前行的文本内容
         * @param context 用于输出键值对的上下文对象
         */
        @Override
        public void map(LongWritable key, Text value, Context context)
                throws IOException, InterruptedException {

            // 将Text转为String，按空白字符分割
            StringTokenizer tokenizer = new StringTokenizer(value.toString());

            // 遍历每个单词，输出<word, 1>
            while (tokenizer.hasMoreTokens()) {
                word.set(tokenizer.nextToken().toLowerCase());
                context.write(word, one);
            }
        }
    }

    /**
     * Reducer类: 负责将相同单词的计数加总
     *
     * 泛型参数说明:
     *   Text          → 输入Key类型（单词，与Mapper输出Key一致）
     *   IntWritable   → 输入Value类型（计数，与Mapper输出Value一致）
     *   Text          → 输出Key类型（单词）
     *   IntWritable   → 输出Value类型（总计数）
     */
    public static class IntSumReducer
            extends Reducer<Text, IntWritable, Text, IntWritable> {

        private IntWritable result = new IntWritable();

        /**
         * reduce方法: 每个不同的Key调用一次
         *
         * @param key     当前的单词
         * @param values  该单词所有计数的迭代器，如 [1, 1, 1, 1, 1]
         * @param context 用于输出结果的上下文对象
         */
        @Override
        public void reduce(Text key, Iterable<IntWritable> values,
                           Context context)
                throws IOException, InterruptedException {

            int sum = 0;
            // 遍历该单词的所有计数，累加
            for (IntWritable val : values) {
                sum += val.get();
            }
            result.set(sum);
            context.write(key, result);
        }
    }

    /**
     * 添加Combiner优化（本地预聚合）
     * Combiner其实就是Reducer，在Map端提前聚合，减少网络传输
     */
    public static class WordCountCombiner
            extends Reducer<Text, IntWritable, Text, IntWritable> {

        private IntWritable result = new IntWritable();

        @Override
        public void reduce(Text key, Iterable<IntWritable> values,
                           Context context)
                throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            result.set(sum);
            context.write(key, result);
        }
    }

    /**
     * 自定义Partitioner: 控制数据分发到哪个Reducer
     * 例如: 将所有以字母'a'开头的单词发到Reducer 0
     */
    public static class AlphaPartitioner
            extends org.apache.hadoop.mapreduce.Partitioner<Text, IntWritable> {

        @Override
        public int getPartition(Text key, IntWritable value, int numPartitions) {
            // 根据首字母分区
            String word = key.toString().toLowerCase();
            if (word.isEmpty()) {
                return 0;
            }
            char firstChar = word.charAt(0);
            // 字母分为2组: a-m → partition 0, n-z → partition 1
            if (firstChar >= 'a' && firstChar <= 'm') {
                return 0;
            } else {
                return 1 % numPartitions;
            }
        }
    }

    /**
     * run方法: 配置和提交MapReduce作业
     */
    @Override
    public int run(String[] args) throws Exception {
        // 参数检查
        if (args.length < 2) {
            System.err.println("Usage: WordCount <input path> <output path>");
            System.err.println("Example: WordCount /user/student/input /user/student/output");
            return -1;
        }

        // 创建Configuration对象（读取Hadoop配置文件）
        Configuration conf = getConf();

        // 创建Job对象
        Job job = Job.getInstance(conf, "WordCount");

        // 设置Jar包（让集群能找到我们的类）
        job.setJarByClass(WordCount.class);

        // ===== 设置Mapper =====
        job.setMapperClass(TokenizerMapper.class);
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(IntWritable.class);

        // ===== 设置Combiner（可选，本地预聚合，减少网络IO） =====
        job.setCombinerClass(WordCountCombiner.class);

        // ===== 设置Partitioner（可选，控制分区逻辑） =====
        // job.setPartitionerClass(AlphaPartitioner.class);

        // ===== 设置Reducer =====
        job.setReducerClass(IntSumReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        // ===== 设置Reduce Task数量 =====
        job.setNumReduceTasks(2);

        // ===== 设置输入输出路径 =====
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        // 等待作业完成并返回状态
        boolean success = job.waitForCompletion(true);
        return success ? 0 : 1;
    }

    /**
     * 程序入口
     */
    public static void main(String[] args) throws Exception {
        // 使用ToolRunner可以方便地处理命令行参数中的 -D 配置项
        int exitCode = ToolRunner.run(new Configuration(), new WordCount(), args);
        System.exit(exitCode);
    }
}
```

---

### 2.4 编译与运行（30min）

**步骤1：准备测试数据**

```bash
# 在本地创建测试文件
cat > sample.txt << 'EOF'
Hello World Hello Hadoop
Hello MapReduce World
Hadoop is a big data framework
MapReduce is a programming model for big data
Big data is transforming the world
Hadoop ecosystem includes HDFS MapReduce Hive
Spark is faster than MapReduce
Hello Big Data World
EOF

# 上传到HDFS
hdfs dfs -mkdir -p /user/student/input
hdfs dfs -put sample.txt /user/student/input/
hdfs dfs -ls /user/student/input/
```

**步骤2：编译打包**

```bash
# 使用Maven编译打包
cd wordcount
mvn clean package -DskipTests

# 查看生成的Jar包
ls -lh target/wordcount-1.0.0.jar
```

**步骤3：提交到集群运行**

```bash
# 运行WordCount
hadoop jar target/wordcount-1.0.0.jar \
    com.bigdata.WordCount \
    /user/student/input \
    /user/student/output/wc_$(date +%Y%m%d_%H%M%S)

# 查看运行日志
# 浏览器访问: http://localhost:8088 (YARN ResourceManager Web UI)
```

**步骤4：查看结果**

```bash
# 查看输出目录
hdfs dfs -ls /user/student/output/wc_20240101_120000/

# 应该看到:
# _SUCCESS          (空文件，标记作业成功)
# part-r-00000      (Reducer 0的输出)
# part-r-00001      (Reducer 1的输出)

# 查看结果
hdfs dfs -cat /user/student/output/wc_20240101_120000/part-r-00000
hdfs dfs -cat /user/student/output/wc_20240101_120000/part-r-00001

# 排序查看（按单词）
hdfs dfs -cat /user/student/output/wc_20240101_120000/part-* | sort

# 按计数降序排序
hdfs dfs -cat /user/student/output/wc_20240101_120000/part-* | sort -k2 -rn
```

---

### 2.5 MapReduce进阶实战（60min）

**实战1：TopN问题——找出出现频率最高的N个单词**

```java
package com.bigdata;

import java.io.IOException;
import java.util.Map;
import java.util.TreeMap;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

/**
 * TopN: 找出出现频率最高的N个单词
 * 设计思路:
 *   1. Mapper: 与WordCount相同，输出<word, 1>
 *   2. Reducer: 使用TreeMap维护TopN（利用TreeMap自动排序特性）
 */
public class TopNWordCount {

    public static class TokenizerMapper
            extends Mapper<LongWritable, Text, Text, IntWritable> {
        private final static IntWritable one = new IntWritable(1);
        private Text word = new Text();

        @Override
        public void map(LongWritable key, Text value, Context context)
                throws IOException, InterruptedException {
            String[] tokens = value.toString().toLowerCase().split("\\s+");
            for (String token : tokens) {
                if (token.length() > 0) {
                    word.set(token);
                    context.write(word, one);
                }
            }
        }
    }

    public static class TopNReducer
            extends Reducer<Text, IntWritable, Text, IntWritable> {

        // TreeMap自动按键（计数）排序
        private TreeMap<Integer, String> topN = new TreeMap<>();
        private int N = 10; // 默认Top 10

        @Override
        protected void setup(Context context) {
            // 从配置中读取N的值
            N = context.getConfiguration().getInt("top.n", 10);
        }

        @Override
        public void reduce(Text key, Iterable<IntWritable> values, Context context)
                throws IOException, InterruptedException {
            // 计算该单词的总计数
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }

            // 维护TopN
            topN.put(sum, key.toString());
            if (topN.size() > N) {
                topN.remove(topN.firstKey()); // 移除最小的
            }
        }

        @Override
        protected void cleanup(Context context)
                throws IOException, InterruptedException {
            // Reduce结束时输出TopN结果
            for (Map.Entry<Integer, String> entry : topN.descendingMap().entrySet()) {
                context.write(new Text(entry.getValue()),
                              new IntWritable(entry.getKey()));
            }
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        conf.setInt("top.n", 20); // 设置Top 20

        Job job = Job.getInstance(conf, "TopN WordCount");
        job.setJarByClass(TopNWordCount.class);
        job.setMapperClass(TokenizerMapper.class);
        job.setReducerClass(TopNReducer.class);

        // TopN通常只用1个Reducer，便于全局排序
        job.setNumReduceTasks(1);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
```

**实战2：Reduce-side Join——关联两个数据集**

```java
package com.bigdata;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

/**
 * Reduce-side Join：关联用户表和订单表
 *
 * 输入1 - users.txt:
 *   U001,张三,北京
 *   U002,李四,上海
 *   U003,王五,广州
 *
 * 输入2 - orders.txt:
 *   O001,U001,100.00
 *   O002,U002,200.00
 *   O003,U001,150.00
 *   O004,U003,300.00
 *
 * 输出:
 *   U001,张三,北京,O001,100.00
 *   U001,张三,北京,O003,150.00
 *   U002,李四,上海,O002,200.00
 *   U003,王五,广州,O004,300.00
 */
public class ReduceSideJoin {

    /**
     * Mapper: 给每条记录打标签（标记来自哪个文件）
     */
    public static class JoinMapper
            extends Mapper<LongWritable, Text, Text, Text> {

        private Text outputKey = new Text();
        private Text outputValue = new Text();

        @Override
        public void map(LongWritable key, Text value, Context context)
                throws IOException, InterruptedException {

            // 获取当前正在处理的文件名
            FileSplit fileSplit = (FileSplit) context.getInputSplit();
            String filename = fileSplit.getPath().getName();

            String line = value.toString();
            String[] fields = line.split(",");

            if (filename.startsWith("users")) {
                // 用户表: U001,张三,北京
                // 输出: Key=U001, Value="USER,张三,北京"
                outputKey.set(fields[0]);
                outputValue.set("USER," + fields[1] + "," + fields[2]);
            } else if (filename.startsWith("orders")) {
                // 订单表: O001,U001,100.00
                // 输出: Key=U001, Value="ORDER,O001,100.00"
                outputKey.set(fields[1]);
                outputValue.set("ORDER," + fields[0] + "," + fields[2]);
            }
            context.write(outputKey, outputValue);
        }
    }

    /**
     * Reducer: 将同一个用户的数据合并
     */
    public static class JoinReducer
            extends Reducer<Text, Text, Text, Text> {

        private Text result = new Text();

        @Override
        public void reduce(Text key, Iterable<Text> values, Context context)
                throws IOException, InterruptedException {

            // 存储用户信息和订单列表
            String userName = "";
            String userCity = "";
            List<String> orders = new ArrayList<>();

            for (Text val : values) {
                String[] parts = val.toString().split(",", 3);
                if (parts[0].equals("USER")) {
                    userName = parts[1];
                    userCity = parts[2];
                } else if (parts[0].equals("ORDER")) {
                    orders.add(parts[1] + "," + parts[2]);
                }
            }

            // 对每个订单输出一条关联结果
            for (String order : orders) {
                result.set(userName + "," + userCity + "," + order);
                context.write(key, result);
            }
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "Reduce-side Join");
        job.setJarByClass(ReduceSideJoin.class);

        job.setMapperClass(JoinMapper.class);
        job.setReducerClass(JoinReducer.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
```

---

### 2.6 Combiner优化对比（20min）

**Combiner的作用：**

```
没有Combiner:
  Map Task输出 → 网络传输(数据量大) → Reduce Task

  示例: Map输出100万条<"hello", 1>
        需要传输100万条记录到Reducer

有Combiner:
  Map Task输出 → Combiner本地聚合 → 网络传输(数据量小) → Reduce Task

  示例: Map输出100万条<"hello", 1>
        Combiner聚合后 → <"hello", 1000000>
        只需传输1条记录到Reducer

条件:
  Combiner适用于满足交换律和结合律的操作:
  ✅ count → sum(1,1,1,1) = 4
  ✅ sum → sum(10,20,30) = 60
  ✅ max → max(10,20,30) = 30
  ❌ avg → avg(avg(1,2), avg(3,4)) ≠ avg(1,2,3,4)
```

---

### 2.7 MapReduce vs Spark 思想对比（15min）

| 维度 | MapReduce | Spark |
|------|-----------|-------|
| 计算模型 | 批处理（Map→Shuffle→Reduce） | DAG（有向无环图） |
| 中间结果 | 写入磁盘（HDFS） | 优先内存（可溢出磁盘） |
| 迭代计算 | 每轮都读写磁盘，极慢 | 在内存中迭代，快10-100倍 |
| 编程模型 | 只有Map和Reduce两个操作 | 20+种Transformation和Action |
| 语言支持 | 主要是Java | Java/Scala/Python/R |
| 适用场景 | 简单ETL、离线报表 | 迭代算法/交互分析/流处理 |

---

## 三、课堂练习（90min）

### 练习1：手写WordCount代码（30min）

```
要求:
  1. 关闭IDE和参考材料
  2. 手写完整的WordCount.java
  3. 包含: Mapper类、Reducer类、main方法(含Job配置)
  4. 在纸上写出（或纯文本编辑器，不使用代码提示）

评分:
  - Mapper类的泛型参数正确: 25%
  - map方法逻辑正确: 25%
  - Reducer类的泛型参数正确: 25%
  - reduce方法逻辑正确 + Job配置: 25%
```

### 练习2：运行并观察作业（30min）

```bash
# 任务1: 运行WordCount并观察
# - 提交作业后，打开YARN Web UI查看任务执行过程
# - 记录: Map Task数量、Reduce Task数量、执行时间

# 任务2: 修改Reduce Task数量
# - 先用1个Reduce Task运行
# - 再用4个Reduce Task运行
# - 对比输出文件数量和每个文件的内容

# 任务3: 添加Combiner对比性能
# - 用大文件（100MB+）测试
# - 记录有/无Combiner的执行时间
# - 观察Shuffle阶段的数据量差异
```

### 练习3：扩展题（30min）

```yaml
题目: 编写"平均成绩"MapReduce程序

输入文件(scores.txt):
  张三,数学,85
  张三,英语,92
  张三,语文,78
  李四,数学,96
  李四,英语,88
  李四,语文,91

要求输出:
  张三,85.0    (85+92+78)/3
  李四,91.67   (96+88+91)/3

思考题:
  1. 能用Combiner吗？为什么？
  2. 如果要把所有学生的成绩排序输出怎么办？
```

---

## 四、课后作业

### 作业1：完成所有课堂代码（必做）

- WordCount.java（完整编译运行，截图提交）
- TopNWordCount.java
- ReduceSideJoin.java
- 平均成绩程序

### 作业2：手绘MapReduce数据流（必做）

画一张完整的WordCount数据流转图，标注：
- InputFormat如何切分数据
- Map阶段输出什么
- Shuffle阶段的Partition/Sort/Group
- Reduce阶段的聚合过程
- OutputFormat如何写入

### 作业3：性能对比实验报告（必做）

设计实验对比以下配置的性能差异，写出报告：
1. Combiner开启 vs 关闭
2. Reduce Task 1个 vs 2个 vs 4个
3. Block Size 64MB vs 128MB

每个实验需要：实验数据 + 运行时间 + Shuffle数据量 + 分析结论

### 作业4：思考题（选做）

```
1. MapReduce的Shuffle阶段为什么是最耗时的？
2. 如果输入数据有2TB，Map Task大约有多少个？
3. 为什么MapReduce不适合迭代计算（如机器学习）？
```

---

## 五、参考资料

1. **MapReduce论文**：*MapReduce: Simplified Data Processing on Large Clusters (2004)*
2. **《Hadoop权威指南》**：第2章 MapReduce、第7章 MapReduce编程
3. **Hadoop官方教程**：https://hadoop.apache.org/docs/stable/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html