# 课时29：LLM与RAG应用开发

> **所属阶段**：L3 高级工程师 | **模块**：补充模块_MLOps与AI工程 | **课时**：4h | **难度**：★★★★★

---

## 一、教学目标

1. 理解LLM基础：Transformer架构核心、Tokenization、Prompt Engineering
2. 掌握RAG架构：检索增强生成的完整流程
3. 掌握Milvus向量数据库：Collection、Partition、Index、CRUD操作
4. 掌握LangChain核心抽象：Chain、Agent、Tool、Retriever
5. 能构建完整的RAG Pipeline：文档解析→分块→Embedding→索引→检索→生成
6. 了解生产级考量：延迟优化、成本控制、幻觉检测、评估框架

---

## 二、LLM基础

### 2.1 Transformer架构核心

```
Transformer 架构（简化版）:

  输入Token序列: [T1, T2, T3, ..., Tn]
       │
       ▼
  ┌──────────────────────────────────────────────────────────┐
  │                  Token Embedding                          │
  │                  + Positional Encoding                    │
  └──────────────────────────┬───────────────────────────────┘
                             │
       ┌─────────────────────▼─────────────────────┐
       │          Multi-Head Self-Attention          │
       │                                             │
       │  Q = X·Wq,  K = X·Wk,  V = X·Wv           │
       │                                             │
       │  Attention(Q,K,V) = softmax(QK^T/√d_k)·V  │
       │                                             │
       │  ┌──────┐ ┌──────┐ ┌──────┐    ┌──────┐   │
       │  │Head 1│ │Head 2│ │Head 3│ ...│Head h│   │
       │  └──┬───┘ └──┬───┘ └──┬───┘    └──┬───┘   │
       │     └────────┴────────┴────────────┘       │
       │                  │ Concat + W_o             │
       └──────────────────┼─────────────────────────┘
                          │
       ┌──────────────────▼─────────────────────────┐
       │          Add & Layer Norm (残差连接)         │
       └──────────────────┬─────────────────────────┘
                          │
       ┌──────────────────▼─────────────────────────┐
       │          Feed-Forward Network               │
       │          FFN(x) = ReLU(x·W1+b1)·W2+b2      │
       └──────────────────┬─────────────────────────┘
                          │
       ┌──────────────────▼─────────────────────────┐
       │          Add & Layer Norm                    │
       └──────────────────┬─────────────────────────┘
                          │
                    × N 层堆叠
                          │
                          ▼
                    输出表示

  关键理解:
  1. Self-Attention: 每个Token可以关注序列中所有其他Token
  2. Multi-Head: 多个注意力头捕获不同类型的关系
  3. Positional Encoding: 注入位置信息（Transformer本身无位置感知）
  4. 残差连接: 缓解深层网络的梯度消失问题
```

### 2.2 Tokenization

```
Tokenization: 文本 → Token序列

  BPE (Byte Pair Encoding) 示例:

  原始文本: "用户画像系统"
  Token序列: ["用户", "画像", "系统"]  (3个Token)

  原始文本: "Hello, world!"
  Token序列: ["Hello", ",", " world", "!"]  (4个Token)

  关键概念:
  ┌──────────────────────────────────────────────────────────┐
  │  Token: 模型处理的最小单位，不等于字符也不等于词          │
  │  Tokenizer: 文本↔Token的转换器                            │
  │  Context Length: 模型一次能处理的最大Token数               │
  │                                                          │
  │  常见模型的Context Length:                                │
  │  - GPT-3.5: 4K / 16K                                    │
  │  - GPT-4: 8K / 32K / 128K                               │
  │  - Claude 3: 200K                                       │
  │  - GLM-4: 128K                                          │
  │                                                          │
  │  中文Token效率: 1个汉字 ≈ 1-2个Token                     │
  │  英文Token效率: 1个单词 ≈ 1-1.5个Token                   │
  │  计费: 按Token数量计费（输入+输出）                       │
  └──────────────────────────────────────────────────────────┘
```

### 2.3 Prompt Engineering

```
Prompt Engineering 核心技巧:

  1. 系统提示(System Prompt): 定义模型角色和行为约束
  ┌──────────────────────────────────────────────────────────┐
  │  System: 你是一个电商数据分析助手。                       │
  │  - 只回答与电商数据相关的问题                              │
  │  - 如果不确定，请明确说明                                 │
  │  - 回答使用中文                                          │
  │  - 数据来源: 电商数仓(ODS/DWD/DWS/ADS)                  │
  └──────────────────────────────────────────────────────────┘

  2. Few-Shot: 提供示例引导输出格式
  ┌──────────────────────────────────────────────────────────┐
  │  将以下自然语言查询转换为SQL:                              │
  │                                                          │
  │  查询: 昨天的总销售额是多少？                              │
  │  SQL: SELECT SUM(total_amount) FROM dws.dws_trade_day    │
  │       WHERE dt = DATE_SUB(CURRENT_DATE(), 1)             │
  │                                                          │
  │  查询: 上周每个省份的订单量排名                            │
  │  SQL: SELECT shipping_province, COUNT(*) AS order_count   │
  │       FROM dwd.dwd_order_detail                           │
  │       WHERE dt >= DATE_SUB(CURRENT_DATE(), 7)            │
  │       GROUP BY shipping_province ORDER BY order_count DESC│
  │                                                          │
  │  查询: {用户输入}                                         │
  │  SQL:                                                    │
  └──────────────────────────────────────────────────────────┘

  3. Chain-of-Thought: 引导逐步推理
  ┌──────────────────────────────────────────────────────────┐
  │  请一步步分析以下问题:                                    │
  │                                                          │
  │  问题: 为什么本周用户留存率下降了5%？                      │
  │                                                          │
  │  分析步骤:                                                │
  │  1. 确认数据: 留存率的计算口径是否一致？                   │
  │  2. 时间维度: 是否有季节性因素？                           │
  │  3. 渠道维度: 哪些渠道的留存下降最明显？                   │
  │  4. 用户维度: 新用户还是老用户的留存下降？                 │
  │  5. 外部因素: 是否有竞品活动或技术故障？                   │
  └──────────────────────────────────────────────────────────┘
```

---

## 三、RAG架构

### 3.1 RAG核心流程

```
RAG (Retrieval-Augmented Generation) 架构:

  ┌──────────────────────────────────────────────────────────┐
  │                    离线索引阶段                            │
  │                                                          │
  │  文档 ──→ 解析 ──→ 分块 ──→ Embedding ──→ 向量数据库     │
  │  (PDF)   (提取文本) (Chunking) (向量化)    (Milvus)      │
  │                                                          │
  │  ┌──────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐  │
  │  │ PDF  │→ │ PyPDF2   │→ │ 512Token │→ │ BGE/OpenAI │→ │
  │  │ Doc  │  │ Unstruct │  │ 重叠64   │  │ Embedding  │  │
  │  │ HTML │  │ Beautiful│  │          │  │ Model      │  │
  │  └──────┘  └──────────┘  └──────────┘  └────────────┘  │
  └──────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────┐
  │                    在线查询阶段                            │
  │                                                          │
  │  用户问题                                                │
  │      │                                                   │
  │      ▼                                                   │
  │  ┌──────────┐                                            │
  │  │ 问题     │                                            │
  │  │ Embedding│──→ 向量相似度搜索 ──→ Top-K相关文档片段     │
  │  └──────────┘    (ANN Search)        │                   │
  │                                     ▼                    │
  │                              ┌──────────────┐            │
  │                              │ Prompt组装    │            │
  │                              │              │            │
  │                              │ System: 角色  │            │
  │                              │ Context: 检索 │            │
  │                              │ Question: 问题│            │
  │                              └──────┬───────┘            │
  │                                     │                    │
  │                                     ▼                    │
  │                              ┌──────────────┐            │
  │                              │ LLM生成回答   │            │
  │                              └──────────────┘            │
  └──────────────────────────────────────────────────────────┘
```

### 3.2 RAG vs Fine-tuning

| 维度 | RAG | Fine-tuning |
|------|-----|-------------|
| 知识更新 | ✅ 实时更新索引即可 | ❌ 需要重新训练 |
| 成本 | 低（只需Embedding+检索） | 高（需要GPU训练） |
| 可解释性 | ✅ 可追溯来源文档 | ❌ 黑盒 |
| 幻觉控制 | ✅ 基于检索内容生成 | ⚠️ 仍可能产生幻觉 |
| 领域适配 | 适合知识密集型 | 适合风格/格式适配 |
| 延迟 | 中（检索+生成） | 低（仅生成） |
| 数据隐私 | ✅ 数据可本地存储 | ⚠️ 训练数据可能泄露 |

---

## 四、向量数据库：Milvus

### 4.1 Milvus架构

```
Milvus 架构:

  ┌──────────────────────────────────────────────────────────┐
  │                    Access Layer                           │
  │  ┌──────────────────────────────────────────────────┐   │
  │  │  SDK (Python/Java/Go/Node.js) + RESTful API      │   │
  │  └──────────────────────────────────────────────────┘   │
  │                                                          │
  │  ┌──────────────────────────────────────────────────┐   │
  │  │               Coordinator Service                  │   │
  │  │  ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │   │
  │  │  │Root Coord│ │Query Coord│ │Data Coord        │ │   │
  │  │  │(DDL/DML) │ │(查询调度) │ │(数据写入/索引构建)│ │   │
  │  │  └──────────┘ └──────────┘ └──────────────────┘ │   │
  │  └──────────────────────────────────────────────────┘   │
  │                                                          │
  │  ┌──────────────────────────────────────────────────┐   │
  │  │               Worker Node                         │   │
  │  │  ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │   │
  │  │  │Query Node│ │Data Node │ │Index Node        │ │   │
  │  │  │(查询执行)│ │(数据写入)│ │(索引构建)        │ │   │
  │  │  └──────────┘ └──────────┘ └──────────────────┘ │   │
  │  └──────────────────────────────────────────────────┘   │
  │                                                          │
  │  ┌──────────────────────────────────────────────────┐   │
  │  │               Storage Layer                        │   │
  │  │  ┌──────────┐ ┌──────────────────────────────┐   │   │
  │  │  │  MinIO   │ │       etcd (元数据)           │   │   │
  │  │  │  (数据)  │ │                               │   │   │
  │  │  └──────────┘ └──────────────────────────────┘   │   │
  │  └──────────────────────────────────────────────────┘   │
  └──────────────────────────────────────────────────────────┘
```

### 4.2 Docker启动Milvus

```yaml
version: '3.8'

services:
  etcd:
    image: quay.io/coreos/etcd:v3.5.5
    environment:
      ETCD_AUTO_COMPACTION_MODE: revision
      ETCD_AUTO_COMPACTION_RETENTION: "1000"
      ETCD_QUOTA_BACKEND_BYTES: "4294967296"
      ETCD_SNAPSHOT_COUNT: "50000"
    volumes:
      - etcd_data:/etcd

  minio:
    image: minio/minio:latest
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    ports:
      - "9001:9001"
      - "9000:9000"
    volumes:
      - minio_data:/data
    command: minio server /data --console-address ":9001"

  milvus:
    image: milvusdb/milvus:v2.3.4
    ports:
      - "19530:19530"
      - "9091:9091"
    depends_on:
      - etcd
      - minio
    environment:
      ETCD_ENDPOINTS: etcd:2379
      MINIO_ADDRESS: minio:9000
    volumes:
      - milvus_data:/var/lib/milvus

  attu:
    image: zilliz/attu:v2.3.4
    ports:
      - "8000:3000"
    depends_on:
      - milvus
    environment:
      MILVUS_URL: milvus:19530

volumes:
  etcd_data:
  minio_data:
  milvus_data:
```

```bash
docker-compose up -d

docker-compose ps
```

### 4.3 创建Collection与CRUD操作

```python
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
import numpy as np

connections.connect(host="localhost", port="19530")

COLLECTION_NAME = "ecommerce_faq"
DIMENSION = 768

if utility.has_collection(COLLECTION_NAME):
    utility.drop_collection(COLLECTION_NAME)

fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="question", dtype=DataType.VARCHAR, max_length=512),
    FieldSchema(name="answer", dtype=DataType.VARCHAR, max_length=2048),
    FieldSchema(name="category", dtype=DataType.VARCHAR, max_length=64),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=DIMENSION),
]

schema = CollectionSchema(fields=fields, description="电商FAQ知识库")
collection = Collection(name=COLLECTION_NAME, schema=schema)

index_params = {
    "metric_type": "COSINE",
    "index_type": "IVF_FLAT",
    "params": {"nlist": 128},
}

collection.create_index(field_name="embedding", index_params=index_params)
print(f"Collection {COLLECTION_NAME} 创建完成")
```

### 4.4 插入向量数据

```python
from pymilvus import Collection
import numpy as np

collection = Collection("ecommerce_faq")

faq_data = [
    {
        "question": "如何申请退款？",
        "answer": "在订单详情页点击'申请退款'按钮，选择退款原因并提交。审核通过后，退款将在3-5个工作日内原路返回。",
        "category": "售后",
    },
    {
        "question": "配送需要多长时间？",
        "answer": "标准配送2-5个工作日，加急配送1-2个工作日，同城配送当日可达。偏远地区可能额外增加2-3天。",
        "category": "物流",
    },
    {
        "question": "如何修改收货地址？",
        "answer": "订单未发货前，可在订单详情页修改收货地址。已发货订单请联系客服协助修改。",
        "category": "订单",
    },
    {
        "question": "支持哪些支付方式？",
        "answer": "支持微信支付、支付宝、银行卡、信用卡、花呗分期等多种支付方式。",
        "category": "支付",
    },
    {
        "question": "商品质量问题如何处理？",
        "answer": "收到商品7天内可申请退换货，请拍照上传质量问题凭证。审核通过后免费退换，运费由商家承担。",
        "category": "售后",
    },
    {
        "question": "如何查看物流信息？",
        "answer": "在订单详情页点击'查看物流'即可实时追踪包裹位置。也可通过快递单号在快递公司官网查询。",
        "category": "物流",
    },
    {
        "question": "优惠券如何使用？",
        "answer": "结算时在优惠券栏选择可用优惠券，系统自动计算优惠金额。注意优惠券的使用条件和有效期。",
        "category": "优惠",
    },
    {
        "question": "如何联系客服？",
        "answer": "可通过APP内在线客服、客服热线400-xxx-xxxx、官方微信公众号等多种渠道联系7×24小时客服。",
        "category": "客服",
    },
]

np.random.seed(42)
embeddings = np.random.randn(len(faq_data), 768).tolist()
for i in range(len(faq_data)):
    vec = np.array(embeddings[i])
    embeddings[i] = (vec / np.linalg.norm(vec)).tolist()

entities = [
    [item["question"] for item in faq_data],
    [item["answer"] for item in faq_data],
    [item["category"] for item in faq_data],
    embeddings,
]

insert_result = collection.insert(entities)
collection.flush()
print(f"插入 {len(faq_data)} 条FAQ数据")
```

### 4.5 ANN搜索

```python
from pymilvus import Collection
import numpy as np

collection = Collection("ecommerce_faq")
collection.load()

query_embedding = np.random.randn(768)
query_embedding = (query_embedding / np.linalg.norm(query_embedding)).tolist()

search_params = {
    "metric_type": "COSINE",
    "params": {"nprobe": 16},
}

results = collection.search(
    data=[query_embedding],
    anns_field="embedding",
    param=search_params,
    limit=3,
    output_fields=["question", "answer", "category"],
)

for hits in results:
    for hit in hits:
        print(f"相似度: {hit.distance:.4f}")
        print(f"  问题: {hit.entity.get('question')}")
        print(f"  回答: {hit.entity.get('answer')}")
        print(f"  分类: {hit.entity.get('category')}")
        print()
```

### 4.6 Partition与过滤搜索

```python
from pymilvus import Collection
import numpy as np

collection = Collection("ecommerce_faq")

collection.create_partition("after_sale")
collection.create_partition("logistics")
collection.create_partition("payment")

after_sale_data = [
    ["如何退货？", "在订单详情页申请退货，7天无理由退货。", "售后"],
    ["换货流程是什么？", "申请换货→审核通过→寄回商品→发出新商品。", "售后"],
]
after_sale_embeddings = [np.random.randn(768) for _ in range(2)]
after_sale_embeddings = [(v / np.linalg.norm(v)).tolist() for v in after_sale_embeddings]

collection.insert(
    [
        [d[0] for d in after_sale_data],
        [d[1] for d in after_sale_data],
        [d[2] for d in after_sale_data],
        after_sale_embeddings,
    ],
    partition_name="after_sale",
)
collection.flush()

query_embedding = (np.random.randn(768) / np.linalg.norm(np.random.randn(768))).tolist()

results = collection.search(
    data=[query_embedding],
    anns_field="embedding",
    param={"metric_type": "COSINE", "params": {"nprobe": 16}},
    limit=5,
    expr='category == "售后"',
    output_fields=["question", "answer", "category"],
)

for hits in results:
    for hit in hits:
        print(f"[售后] 相似度: {hit.distance:.4f}, 问题: {hit.entity.get('question')}")
```

---

## 五、LLM应用框架：LangChain

### 5.1 核心抽象

```
LangChain 核心抽象:

  ┌──────────────────────────────────────────────────────────┐
  │  Model                                                    │
  │  ├── LLM: 文本输入→文本输出 (如GPT-4, GLM-4)             │
  │  └── ChatModel: 消息列表→消息输出 (如ChatGPT)            │
  │                                                          │
  │  Prompt Template                                          │
  │  ├── PromptTemplate: 格式化输入变量为Prompt               │
  │  └── ChatPromptTemplate: 格式化消息列表                   │
  │                                                          │
  │  Retriever                                                │
  │  ├── VectorStoreRetriever: 从向量数据库检索               │
  │  ├── MultiQueryRetriever: 多查询检索                      │
  │  └── ContextualCompressionRetriever: 上下文压缩           │
  │                                                          │
  │  Chain                                                    │
  │  ├── LLMChain: Prompt → LLM → Output                     │
  │  ├── RetrievalQA: Question → Retriever → LLM → Answer    │
  │  └── SequentialChain: 多步骤串联                          │
  │                                                          │
  │  Agent                                                    │
  │  ├── ReAct Agent: 推理+行动循环                           │
  │  ├── Tool: Agent可调用的外部工具                          │
  │  └── AgentExecutor: Agent执行器                           │
  └──────────────────────────────────────────────────────────┘
```

### 5.2 构建RAG Chain

```python
from langchain_community.vectorstores import Milvus
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-large-zh-v1.5",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)

vectorstore = Milvus(
    embedding_function=embedding_model,
    connection_args={"host": "localhost", "port": "19530"},
    collection_name="ecommerce_faq",
)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3},
)

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0,
    base_url="https://api.openai.com/v1",
)

template = """你是一个电商客服助手。请根据以下检索到的知识回答用户问题。
如果检索结果中没有相关信息，请明确说明，不要编造答案。

检索到的知识:
{context}

用户问题: {question}

请给出准确、完整的回答:"""

prompt = ChatPromptTemplate.from_template(template)

def format_docs(docs):
    return "\n\n".join([f"Q: {doc.page_content}\nA: {doc.metadata.get('answer', '')}" for doc in docs])

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

answer = rag_chain.invoke("如何申请退款？")
print(answer)

answer = rag_chain.invoke("配送需要多久？")
print(answer)
```

### 5.3 Agent与Tool

```python
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate

@tool
def query_order(order_id: str) -> str:
    """查询订单状态和物流信息。参数: order_id - 订单编号"""
    orders = {
        "ORD001": "状态: 已发货, 快递: 顺丰SF123456, 预计明天送达",
        "ORD002": "状态: 待发货, 预计今日发货",
        "ORD003": "状态: 已完成, 签收时间: 2024-01-15 14:30",
    }
    return orders.get(order_id, f"未找到订单 {order_id}")

@tool
def query_product(product_name: str) -> str:
    """查询商品信息和库存。参数: product_name - 商品名称"""
    products = {
        "iPhone 15": "价格: ¥6999, 库存: 500台, 评分: 4.8",
        "MacBook Pro": "价格: ¥14999, 库存: 200台, 评分: 4.9",
        "AirPods Pro": "价格: ¥1899, 库存: 1000台, 评分: 4.7",
    }
    return products.get(product_name, f"未找到商品 {product_name}")

@tool
def query_refund_policy(order_amount: str) -> str:
    """查询退款政策和预计到账时间。参数: order_amount - 订单金额"""
    try:
        amount = float(order_amount)
        if amount > 10000:
            return f"大额订单(¥{amount})退款需3-5个工作日审核，审核通过后1-2个工作日到账"
        else:
            return f"普通订单(¥{amount})退款1-3个工作日到账"
    except ValueError:
        return "请提供有效的订单金额"

tools = [query_order, query_product, query_refund_policy]

llm = ChatOpenAI(model="gpt-4", temperature=0)

prompt = PromptTemplate.from_template(
    """你是一个电商客服助手，可以使用工具回答用户问题。

可用工具:
{tools}

使用格式:
Question: 用户问题
Thought: 思考应该使用什么工具
Action: 工具名称
Action Input: 工具参数
Observation: 工具返回结果
... (可以多次使用工具)
Thought: 我已经获得足够信息
Final Answer: 最终回答

开始!

Question: {input}
Thought: {agent_scratchpad}"""
)

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

result = agent_executor.invoke({"input": "我的订单ORD001到哪了？"})
print(result["output"])

result = agent_executor.invoke({"input": "iPhone 15还有货吗？退款多久到账？"})
print(result["output"])
```

---

## 六、RAG Pipeline完整实现

### 6.1 文档解析

```python
from langchain_community.document_loaders import PyPDFLoader, UnstructuredMarkdownLoader, TextLoader
from langchain_core.documents import Document
import os

def load_documents(directory: str) -> list[Document]:
    documents = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if file.endswith(".pdf"):
                    loader = PyPDFLoader(file_path)
                    docs = loader.load()
                    for doc in docs:
                        doc.metadata["source_file"] = file
                        doc.metadata["file_type"] = "pdf"
                    documents.extend(docs)
                elif file.endswith(".md"):
                    loader = UnstructuredMarkdownLoader(file_path)
                    docs = loader.load()
                    for doc in docs:
                        doc.metadata["source_file"] = file
                        doc.metadata["file_type"] = "markdown"
                    documents.extend(docs)
                elif file.endswith(".txt"):
                    loader = TextLoader(file_path, encoding="utf-8")
                    docs = loader.load()
                    for doc in docs:
                        doc.metadata["source_file"] = file
                        doc.metadata["file_type"] = "text"
                    documents.extend(docs)
            except Exception as e:
                print(f"加载文件失败 {file_path}: {e}")

    print(f"共加载 {len(documents)} 个文档片段")
    return documents

documents = load_documents("./faq_docs")
```

### 6.2 文本分块

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=64,
    separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""],
    length_function=len,
)

chunks = text_splitter.split_documents(documents)

print(f"原始文档: {len(documents)} 个")
print(f"分块后: {len(chunks)} 个")
print(f"\n示例分块:")
print(f"  内容: {chunks[0].page_content[:100]}...")
print(f"  元数据: {chunks[0].metadata}")
```

### 6.3 Embedding生成与索引

```python
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Milvus

embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-large-zh-v1.5",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)

vectorstore = Milvus.from_documents(
    documents=chunks,
    embedding=embedding_model,
    connection_args={"host": "localhost", "port": "19530"},
    collection_name="ecommerce_knowledge",
    drop_old=True,
)

print(f"索引构建完成，共 {len(chunks)} 个文档块")
```

### 6.4 完整RAG Pipeline

```python
from langchain_community.vectorstores import Milvus
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory

embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-large-zh-v1.5",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)

vectorstore = Milvus(
    embedding_function=embedding_model,
    connection_args={"host": "localhost", "port": "19530"},
    collection_name="ecommerce_knowledge",
)

retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 5, "fetch_k": 10},
)

llm = ChatOpenAI(model="gpt-4", temperature=0)

system_template = """你是一个专业的电商数据助手。请根据检索到的知识回答用户问题。

规则:
1. 只基于检索到的知识回答，不要编造信息
2. 如果检索结果不足以回答问题，请明确说明
3. 引用来源时标注文档名称
4. 回答使用中文

检索到的知识:
{context}"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("human", "{question}"),
])

def format_docs(docs):
    formatted = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("source_file", "未知来源")
        formatted.append(f"[{i}] (来源: {source})\n{doc.page_content}")
    return "\n\n---\n\n".join(formatted)

rag_chain = (
    RunnableParallel(
        context=retriever | format_docs,
        question=RunnablePassthrough(),
    )
    | prompt
    | llm
    | StrOutputParser()
)

questions = [
    "如何申请退款？",
    "配送需要多长时间？",
    "优惠券怎么使用？",
]

for q in questions:
    print(f"\n{'='*60}")
    print(f"问题: {q}")
    print(f"{'='*60}")
    answer = rag_chain.invoke(q)
    print(f"回答: {answer}")
```

---

## 七、生产级考量

### 7.1 延迟优化

```
RAG Pipeline 延迟分解与优化:

  典型延迟分布 (总延迟 ~3-5秒):
  ┌──────────────────────────────────────────────────────────┐
  │  1. 问题Embedding:  50-200ms                             │
  │  2. 向量检索:        10-50ms                              │
  │  3. Prompt组装:       <1ms                                │
  │  4. LLM生成:       2000-4000ms  ← 主要瓶颈              │
  │                                                          │
  │  优化策略:                                                │
  │  ┌──────────────────────────────────────────────────┐   │
  │  │  Embedding优化:                                   │   │
  │  │  - 缓存热门问题的Embedding                        │   │
  │  │  - 使用更小的Embedding模型(bge-small)             │   │
  │  │  - 本地部署Embedding模型避免网络延迟              │   │
  │  ├──────────────────────────────────────────────────┤   │
  │  │  检索优化:                                        │   │
  │  │  - 使用IVF_PQ索引减少内存占用                     │   │
  │  │  - 预加载Collection到内存                         │   │
  │  │  - 减少output_fields减少传输量                    │   │
  │  ├──────────────────────────────────────────────────┤   │
  │  │  LLM优化:                                        │   │
  │  │  - 使用流式输出(Streaming)降低首Token延迟         │   │
  │  │  - 使用更快的模型(GPT-3.5/GLM-3)                 │   │
  │  │  - 本地部署开源模型(vLLM/TGI)                    │   │
  │  │  - 减少max_tokens限制输出长度                     │   │
  │  └──────────────────────────────────────────────────┘   │
  └──────────────────────────────────────────────────────────┘
```

### 7.2 成本控制

```python
from langchain.callbacks import get_openai_callback

with get_openai_callback() as cb:
    answer = rag_chain.invoke("如何申请退款？")
    print(f"回答: {answer}")
    print(f"\n成本统计:")
    print(f"  Token使用: {cb.total_tokens}")
    print(f"  Prompt Token: {cb.prompt_tokens}")
    print(f"  Completion Token: {cb.completion_tokens}")
    print(f"  总成本: ${cb.total_cost:.4f}")
```

### 7.3 幻觉检测

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4", temperature=0)

hallucination_prompt = ChatPromptTemplate.from_template(
    """请判断以下回答是否基于给定的上下文信息。如果回答中包含了上下文中没有的信息，则判定为幻觉。

上下文:
{context}

回答:
{answer}

请输出JSON格式:
{{
    "is_hallucination": true/false,
    "hallucinated_parts": ["具体哪些部分是幻觉"],
    "confidence": 0.0-1.0
}}"""
)

hallucination_chain = hallucination_prompt | llm | StrOutputParser()

def check_hallucination(context, answer):
    result = hallucination_chain.invoke({"context": context, "answer": answer})
    return result
```

### 7.4 评估框架：RAGAS

```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from datasets import Dataset

test_data = {
    "question": [
        "如何申请退款？",
        "配送需要多长时间？",
        "优惠券如何使用？",
    ],
    "answer": [
        "在订单详情页点击'申请退款'按钮，选择退款原因并提交。审核通过后3-5个工作日到账。",
        "标准配送2-5个工作日，加急配送1-2个工作日，同城配送当日可达。",
        "结算时在优惠券栏选择可用优惠券，系统自动计算优惠金额。注意使用条件和有效期。",
    ],
    "contexts": [
        ["在订单详情页点击'申请退款'按钮，选择退款原因并提交。审核通过后，退款将在3-5个工作日内原路返回。"],
        ["标准配送2-5个工作日，加急配送1-2个工作日，同城配送当日可达。偏远地区可能额外增加2-3天。"],
        ["结算时在优惠券栏选择可用优惠券，系统自动计算优惠金额。注意优惠券的使用条件和有效期。"],
    ],
    "ground_truth": [
        "在订单详情页申请退款，3-5个工作日到账。",
        "标准2-5天，加急1-2天，同城当日达。",
        "结算时选择优惠券，注意使用条件和有效期。",
    ],
}

dataset = Dataset.from_dict(test_data)

results = evaluate(
    dataset=dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
    ],
)

print("RAGAS评估结果:")
for metric, value in results.items():
    print(f"  {metric}: {value:.4f}")
```

---

## 八、课堂练习（60min）

### 练习1：Docker启动Milvus（10min）

```bash
curl -o docker-compose-milvus.yml https://github.com/milvus-io/milvus/releases/download/v2.3.4/milvus-standalone-docker-compose.yml

docker-compose -f docker-compose-milvus.yml up -d

docker-compose -f docker-compose-milvus.yml ps

pip install pymilvus
```

```python
from pymilvus import connections

connections.connect(host="localhost", port="19530")
print("Milvus连接成功!")
```

### 练习2：将电商FAQ文档向量化并索引（25min）

```python
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
import numpy as np

connections.connect(host="localhost", port="19530")

COLLECTION = "lab_ecommerce_faq"
DIM = 768

if utility.has_collection(COLLECTION):
    utility.drop_collection(COLLECTION)

fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="question", dtype=DataType.VARCHAR, max_length=512),
    FieldSchema(name="answer", dtype=DataType.VARCHAR, max_length=2048),
    FieldSchema(name="category", dtype=DataType.VARCHAR, max_length=64),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=DIM),
]

schema = CollectionSchema(fields=fields, description="电商FAQ练习")
collection = Collection(name=COLLECTION, schema=schema)

collection.create_index(
    field_name="embedding",
    index_params={"metric_type": "COSINE", "index_type": "IVF_FLAT", "params": {"nlist": 64}},
)

faqs = [
    ("如何注册账号？", "点击首页'注册'按钮，填写手机号和验证码即可完成注册。", "账号"),
    ("忘记密码怎么办？", "点击登录页'忘记密码'，通过手机验证码重置密码。", "账号"),
    ("如何绑定手机号？", "进入'我的→设置→账号安全→绑定手机'，输入新手机号和验证码。", "账号"),
    ("如何查看历史订单？", "进入'我的→全部订单'可查看所有历史订单及状态。", "订单"),
    ("如何取消订单？", "未发货订单可在订单详情页点击'取消订单'。已发货订单需联系客服。", "订单"),
    ("如何开发票？", "订单完成后在订单详情页申请电子发票，填写开票信息即可。", "订单"),
    ("支持哪些快递？", "合作快递包括顺丰、中通、圆通、韵达、申通等主流快递。", "物流"),
    ("如何查询物流？", "在订单详情页点击'查看物流'即可实时追踪包裹位置。", "物流"),
    ("可以指定快递吗？", "暂不支持指定快递，系统根据收货地址自动选择最优快递。", "物流"),
    ("如何使用积分？", "结算时在支付页面勾选'使用积分抵扣'，100积分=1元。", "优惠"),
]

np.random.seed(42)
embeddings = []
for _ in faqs:
    vec = np.random.randn(DIM)
    embeddings.append((vec / np.linalg.norm(vec)).tolist())

collection.insert([
    [f[0] for f in faqs],
    [f[1] for f in faqs],
    [f[2] for f in faqs],
    embeddings,
])
collection.flush()

collection.load()

query_vec = np.random.randn(DIM)
query_vec = (query_vec / np.linalg.norm(query_vec)).tolist()

results = collection.search(
    data=[query_vec],
    anns_field="embedding",
    param={"metric_type": "COSINE", "params": {"nprobe": 16}},
    limit=3,
    output_fields=["question", "answer", "category"],
)

print("搜索结果:")
for hits in results:
    for hit in hits:
        print(f"  相似度: {hit.distance:.4f}")
        print(f"  问题: {hit.entity.get('question')}")
        print(f"  回答: {hit.entity.get('answer')}")
        print()
```

### 练习3：构建一个简单的RAG问答系统（25min）

```python
from pymilvus import Collection
import numpy as np

collection = Collection("lab_ecommerce_faq")
collection.load()

def simple_rag_query(question: str, collection, top_k: int = 3) -> str:
    query_vec = np.random.randn(768)
    query_vec = (query_vec / np.linalg.norm(query_vec)).tolist()

    results = collection.search(
        data=[query_vec],
        anns_field="embedding",
        param={"metric_type": "COSINE", "params": {"nprobe": 16}},
        limit=top_k,
        output_fields=["question", "answer", "category"],
    )

    context_parts = []
    for hits in results:
        for hit in hits:
            context_parts.append(
                f"Q: {hit.entity.get('question')}\nA: {hit.entity.get('answer')}"
            )

    context = "\n\n".join(context_parts)

    prompt = f"""基于以下知识回答用户问题。如果知识中没有相关信息，请说明"抱歉，我暂时无法回答这个问题"。

知识:
{context}

用户问题: {question}

回答:"""

    print(f"\n问题: {question}")
    print(f"检索到 {len(context_parts)} 条相关知识")
    print(f"\nPrompt:\n{prompt[:500]}...")
    print(f"\n--- 请将上述Prompt发送给LLM获取回答 ---")

    return prompt

simple_rag_query("如何取消订单？", collection)
simple_rag_query("如何使用积分？", collection)
simple_rag_query("如何开发票？", collection)
```

---

## 九、课后作业

### 必做

1. **数据助手**：为L1项目4的数仓构建"数据助手"，支持用自然语言查询数据（如"昨天的GMV是多少"→生成SQL→执行→返回结果）
2. **完整RAG Pipeline**：实现文档→向量→检索→生成的完整Pipeline，至少索引50个FAQ文档
3. **RAG评估**：使用RAGAS评估RAG系统的检索准确率和生成质量，faithfulness > 0.8

### 选做

1. 实现流式输出的RAG系统，使用SSE（Server-Sent Events）向前端推送生成结果
2. 实现多轮对话RAG，维护对话历史，支持追问和上下文理解
3. 实现混合检索：向量检索 + 关键词检索(BM25) + 重排序(Reranker)

---

## 十、参考资料

- [Milvus官方文档](https://milvus.io/docs/)
- [LangChain官方文档](https://python.langchain.com/docs/get_started)
- [RAGAS评估框架](https://docs.ragas.io/)
- [BGE Embedding模型](https://huggingface.co/BAAI/bge-large-zh-v1.5)
- [Attention Is All You Need (Transformer论文)](https://arxiv.org/abs/1706.03762)
- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)
- [Attu - Milvus可视化管理工具](https://github.com/zilliztech/attu)
