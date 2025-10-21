# AME - Another Me Engine

**AME (Another Me Engine)** 是 Another Me 项目的独立技术模块引擎，提供了所有核心技术功能的实现。

**版本**: v0.3.0

## 🎯 设计理念

AME 采用完全模块化、可扩展的设计，每个模块都是独立的技术单元，具有明确的输入输出接口。

**核心特性**：
- ✅ **抽象基类**：所有模块都提供抽象基类，支持自定义实现
- ✅ **工厂模式**：通过工厂类创建实例，支持动态切换
- ✅ **独立可测**：模块之间低耦合，便于单元测试
- ✅ **易于复用**：可在其他项目中直接引用
- ✅ **性能优化**：内置缓存、重试、并发处理

## 📦 核心模块

### 1. Data Processor (数据处理模块)
- **processor.py**: 基础数据处理器，支持文本、图片、音频等多种格式
- **analyzer.py**: 数据分析器，提供情绪分析、关键词提取、关系分析等功能
- **async_processor.py**: 异步数据处理器，支持并发批量处理

### 2. Vector Store (向量存储模块)
- **base.py**: 向量存储抽象基类，定义统一接口
- **memu_store.py**: Memu 向量存储实现（轻量级）
- **store.py**: ChromaDB 向量存储实现（功能完整）
- **factory.py**: 工厂模式，支持动态切换向量存储引擎

### 3. LLM Caller (LLM调用模块)
- **caller.py**: LLM调用封装，支持OpenAI格式API
- 特性：重试机制、缓存支持、流式输出、错误处理

### 4. RAG Generator (RAG生成模块)
- **generator.py**: 检索增强生成器，结合向量检索和LLM生成

### 5. Retrieval (检索模块) ✨ **v0.3.0 新增**
- **base.py**: 检索器抽象基类 `RetrieverBase`
- **vector_retriever.py**: 纯向量检索
- **hybrid_retriever.py**: **混合检索**（向量 + 关键词 + 时间加权）
- **reranker.py**: **重排序器**（多样性/时效性/LLM重排序）
- **factory.py**: 工厂模式，创建检索器和重排序器

**复杂召回示例**：
```python
from ame import RetrieverFactory

# 混合检索：向量+关键词+时间
retriever = RetrieverFactory.create_retriever(
    retriever_type="hybrid",
    vector_store=vector_store,
    vector_weight=0.6,
    keyword_weight=0.3,
    time_weight=0.1
)
results = await retriever.retrieve(query="...", top_k=10)

# 重排序
reranker = RetrieverFactory.create_reranker("diversity")
reranked = await reranker.rerank(query="...", results=results)
```

## 🔧 使用示例

```python
from ame import DataProcessor, VectorStoreFactory, LLMCaller, RAGGenerator

# 1. 数据处理
processor = DataProcessor()
processed_data = processor.process_file("/path/to/file.txt")

# 2. 向量存储
vector_store = VectorStoreFactory.create(store_type="memu")
vector_store.add_documents(processed_data)

# 3. LLM调用
llm = LLMCaller(api_key="your-api-key")
response = llm.generate("你好，世界")

# 4. RAG生成
rag = RAGGenerator(vector_store=vector_store, llm_caller=llm)
answer = rag.generate_answer(query="我的兴趣爱好是什么？")
```

## 📋 模块依赖

```
ame/
├── data_processor/      # 独立，无依赖
├── vector_store/        # 独立，可选依赖 chromadb
├── llm_caller/          # 独立，依赖 openai
└── rag_generator/       # 依赖 vector_store + llm_caller
```

## 🚀 技术特性

- **模块化设计**: 每个模块独立运行，接口清晰
- **工厂模式**: 支持动态切换实现（如向量存储引擎）
- **性能优化**: 缓存机制、并发处理、重试策略
- **类型安全**: 完整的类型注解
- **可扩展性**: 易于添加新的实现

## 📝 版本

当前版本: **v0.3.0**

**v0.3.0 更新**：
- ✨ 新增复杂检索模块 (retrieval/)
- ✨ 支持混合检索策略（向量+关键词+时间）
- ✨ 支持多种重排序策略
- ✨ 所有模块均提供抽象基类，支持自定义扩展
