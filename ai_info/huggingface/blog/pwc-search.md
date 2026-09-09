# Inference Endpoints、Jobs 与 Buckets 如何驱动 Papers with Code 的搜索（How Hugging Face Inference Endpoints, Jobs, and Buckets Power Search on Papers with Code）

- **原文链接**: [How Hugging Face Inference Endpoints, Jobs, and Buckets Power Search on Papers with Code](https://huggingface.co/blog/pwc-search)
- **作者**: Niels Rogge（Hugging Face）
- **发布日期**: 2026-08-21
- **检索日期**: 2026-09-09
- **标签**: #混合检索 #RAG #Embedding #基础设施 #PapersWithCode #HuggingFace

## 核心观点

Hugging Face 复活 Papers with Code 三个月后公开其搜索引擎架构：PostgreSQL 全文检索 + pgvector 语义检索 + 加权 RRF（k=60）融合的混合搜索，为超过 110,000 篇论文维护 embedding，同时服务网页与 `pwc search` CLI（agent 可经 Skill 调用）。论文搜索既要点中精确标题/arXiv ID，也要理解"小型代码生成语言模型"这类概念查询，混合检索兼顾两者。

架构按"离线吞吐 / 在线延迟"切分：HF Jobs（L4 GPU）批量刷语料向量，Storage Buckets 作为三个不同生命周期系统之间的不可变交接层，Inference Endpoint（TEI）只把"查询嵌入"这一小步放在请求路径上，可缩容到零；端点冷、忙或不健康时立即回退全文检索。

核心工程原则是把 embedding 格式当版本化 API 对待：为每次向量生成记录模型 repo 与精确 revision、输出维度、输入格式版本、query/document 角色、归一化方法与源内容哈希。

## 关键发现 / 关键技术

### 1. 严格的 embedding 契约
- 每篇论文编码为 normalized title + "\n\n" + normalized abstract
- 生产模型 Qwen/Qwen3-Embedding-0.6B，钉死精确 revision，256 维 L2 归一化向量（经 MTEB 榜选型）
- 利用 Qwen3 的两项新能力：MRL（Matryoshka）动态维度换取速度/存储；instruction prompt 区分 document（嵌语料）与 query（嵌在线查询）

### 2. Jobs + Buckets 的离线语料构建
- 可重复读 PostgreSQL 快照流式导出 → 有界 JSONL 分片 + manifest（行数 + SHA-256 校验和）
- l4x1 Job（L4 24GB）直挂 Bucket 跑嵌入：校验 manifest 与分片校验和、按长度排序减少 padding、OOM 自动降 batch、float16 Parquet 原子写出；分片级 complete 标记让重试可断点续跑
- 5,000 篇试点：L4 上 1024 维约 75 篇/秒；同一次推理可确定性物化 512/256 维对比存储与检索取舍
- 不可变 run 前缀（runs/<run-id>/input|output）带来：可复现、安全重试、廉价实验、受控灰度（导入不等于激活）、简单回滚

### 3. 在线服务与混合检索
- Inference Endpoint（TEI 后端）嵌查询向量：1 秒生产超时、非阻塞并发上限、维度/有限性/范数校验、查询级短缓存、反复失败熔断、日志不留原始查询——语义分支失效立即回退词法结果
- pgvector + HNSW：5,000 篇试点 256 维索引对精确检索 Recall@20 = 0.9955，p50 1.31 ms / p95 2.21 ms；表与索引存储约为 1024 维版本的 27%
- 每查询词法、语义各取 50 候选，等权 RRF（k=60）融合；精确标题与 arXiv ID 置顶，方法分类识别"the original BERT paper"式导航查询

### 4. 六条生产经验
吞吐型负载与延迟敏感负载分离；让存储成为计算与生产之间的显式契约；钉住的不止模型名（revision/维度/格式版本）；为冷启动而设计（scale-to-zero 是常态而非异常）；更小的向量是系统特性（27% 存储）；激活应当无聊（灰度 + 回滚）。

## 实践意义

这是中等规模（十万级文档）生产语义检索的完整参考架构：不引入新数据库、以 PostgreSQL + pgvector + RRF 起步，把工程重心放在契约版本化、不可变工件与优雅降级上。对 agent 开发者：搜索能力以 CLI + Skill 形式开放，是"给 agent 配研究检索工具"的直接范例。

## 跨厂商对比

- 与 [OLMo Earth 基础设施](olmoearth-infrastructure.md) 对比：同为开源机构公开大规模基础设施实录，OLMo Earth 面向预训练集群，本文面向生产检索服务，关注的故障模式（冷启动、回滚、灰度）不同
- 与 [vLLM Transformers 后端原生加速](native-speed-vllm-transformers-backend.md) 互补：一个优化生成式推理路径，一个优化 embedding/检索路径，合起来覆盖 HF 推理服务栈的两端

## 资源

- 论文：N/A
- 代码：https://github.com/huggingface/pwc-cli（pwc search CLI 与 agent Skill）
- Demo：https://paperswithcode.co
