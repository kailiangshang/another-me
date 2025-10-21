# AME - Another Me Engine

**AME (Another Me Engine)** 是 Another Me 项目的独立技术模块引擎，提供了所有核心技术功能的实现。

## 🎯 设计理念

AME 采用模块化设计，每个模块都是独立的技术单元，具有明确的输入输出接口。这种设计使得：
- ✅ 技术模块可以独立开发和测试
- ✅ 便于在其他项目中复用
- ✅ 方便进行技术升级和替换
- ✅ 降低系统耦合度

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

当前版本: **v0.2.0**
