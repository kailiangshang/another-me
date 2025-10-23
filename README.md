# Another Me 🌟

**世界上另一个我 —— AI 数字分身系统**

> 用你的聊天记录、日记、知识训练出一个"像你"的 AI。数据本地存储，隐私安全。

[![Version](https://img.shields.io/badge/version-0.6.0-blue.svg)](DOCUMENTATION.md#版本历史)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](streamlit_app/requirements.txt)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28-red.svg)](streamlit_app/)

---

## ✨ 最新更新 (v0.6.0) - 优化版本

### 🔧 **项目优化**
- ✅ 修复 streamlit_app 引用 ame 项目的 import 错误
- ✅ 删除后端相关的冗余文件，项目纯 Streamlit 化
- ✅ 集成 Logo 图片到侧边栏，提升品牌辨识度
- ✅ Docker 启动支持交互式配置（端口、数据目录）
- ✅ 数据持久化支持（知识库和 MEM 存储）
- ✅ 文档精简，只保留 README.md 和 DOCUMENTATION.md

### 🌊 **流式输出修复**
- 修复 LLM 流式输出支持，实现真正的实时对话
- MEM 对话页面流畅体验

---

## 🎯 核心理念

**业务功能驱动，技术模块支撑**

- 🔹 **业务功能**：面向用户价值，描述"能做什么"
- 🔹 **技术功能**：面向系统实现，描述"如何做到"

---

## 🎯 核心功能

### 📚 RAG - 知识库管理
上传个人笔记、文档、资料，构建专属知识库。

**功能**：
- 📁 文档上传（TXT, MD, PDF, DOCX）
- 🔍 智能检索（混合检索策略）
- 📂 知识库管理（查看、搜索、删除）
- 📊 统计分析（来源分布、时间趋势）

### 💬 MEM - 记忆与模仿
与 AI 分身对话，它会模仿你的说话风格。

**功能**：
- 📝 学习你的聊天记录
- 🌊 流式对话体验
- 🧠 记忆管理（查看、搜索、时间线）
- 💾 记忆导出（JSON 格式）

### 📊 分析报告
生成自我认知分析报告。

**功能**：
- 📝 情绪分析
- 🔑 关键词提取
- 📄 导出 MD/HTML/PDF



## 🏗️ 项目架构

```
another-me/
├── ame/                  # AME - Another Me Engine（独立技术模块）
│   ├── rag/              # RAG 模块：知识库管理
│   ├── mem/              # MEM 模块：记忆与模仿
│   ├── data_processor/   # 数据处理
│   ├── vector_store/     # 向量存储
│   ├── llm_caller/       # LLM 调用
│   └── retrieval/        # 复杂检索
├── streamlit_app/        # Streamlit 前端应用
│   ├── pages/            # 页面模块
│   │   ├── home_page.py         # 主页
│   │   ├── config_page.py       # 配置页面
│   │   ├── rag_page.py          # RAG 知识库
│   │   ├── knowledge_manager_page.py  # 知识库管理
│   │   ├── mem_page.py          # MEM 对话
│   │   ├── memory_manager_page.py     # 记忆管理
│   │   └── analysis_page.py     # 分析报告
│   ├── utils/            # 工具模块
│   └── app.py            # 主应用
├── docker-build-streamlit.sh
└── README.md
```

**三层分离架构**：
- **Streamlit UI**: Python 全栈前端，简洁高效
- **AME RAG**: 知识库管理、文档检索
- **AME MEM**: 记忆学习、风格模仿

## 🚀 快速开始

### 方式 1：Streamlit 本地运行（推荐）

```bash
cd streamlit_app
./run.sh

# 访问: http://localhost:8501
```

### 方式 2：Docker 部署

```bash
# 一键构建和启动
./docker-build-streamlit.sh

# 访问: http://localhost:8501
```

### 🔑 初次使用

1. 访问应用
2. 点击侧边栏 **“⚙️ 配置”**
3. 输入 OpenAI API Key
4. 点击 **“💾 保存配置”**
5. 开始使用！

## 📖 完整文档

- [**DOCUMENTATION.md**](DOCUMENTATION.md) - 完整的技术文档和使用指南
- [**ame/README.md**](ame/README.md) - AME 技术引擎文档

## 🔐 隐私保证

- ✅ 数据完全本地存储
- ✅ 支持离线运行
- ✅ 开源可审计

## 🛠️ 技术栈

**前端**: Streamlit (Python 全栈)  
**AME 引擎**: v0.6.0
- 📚 **RAG 模块**: 知识库管理、文档检索、知识分析
- 💬 **MEM 模块**: 记忆学习、风格模仿、记忆管理
- 📊 数据处理 + 📦 向量存储 (Memu/ChromaDB)
- 🤖 LLM 调用 + 🎯 复杂检索  
**特性**: 流式输出 + MD/PDF/HTML 导出 + 可视化统计  
**部署**: Docker 独立构建

> **AME (详见 `ame/README.md`)**: 独立的技术模块引擎，支持自定义扩展



## 📄 License

MIT License

---