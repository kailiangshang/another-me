# Another Me 🌟

**世界上另一个我 —— AI 数字分身系统**

> 用你的聊天记录、日记、知识训练出一个"像你"的 AI。数据本地存储，隐私安全。

[![Version](https://img.shields.io/badge/version-0.7.0-blue.svg)](DOCUMENTATION.md#版本历史)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](gradio_app/requirements.txt)
[![Gradio](https://img.shields.io/badge/gradio-4.0-orange.svg)](gradio_app/)

---

## ✨ 最新更新 (v0.7.0) - Gradio 框架迁移

### 🎨 **前端框架升级**
- ❌ ~~Streamlit~~ → ✅ **Gradio 4.0** (更适合 AI 应用)
- 更优雅的组件设计，更强大的自定义能力
- 原生支持流式输出，对话体验更流畅
- 更好的移动端适配

### 🛠️ **功能完善**
- ✅ 完整的主页和系统状态展示
- ✅ 配置页面：API Key 设置和测试
- ✅ MEM 对话：实时流式输出，支持学习
- ✅ Logo 集成，品牌形象更统一

### 💡 **为什么选择 Gradio？**
- 🚀 专为 AI/ML 应用设计
- 🌊 原生流式输出支持
- 🎨 丰富的组件库
- 📱 更好的移动端体验
- 🌐 内置分享功能

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
├── gradio_app/           # Gradio 前端应用
│   ├── components/       # 页面组件
│   │   ├── home_tab.py        # 主页
│   │   ├── config_tab.py      # 配置页面
│   │   └── mem_tab.py         # MEM 对话
│   ├── utils/            # 工具模块
│   └── app.py            # 主应用
├── docker-build-gradio.sh
└── README.md
```

**三层分离架构**：
- **Gradio UI**: Python 前端，专为 AI 应用设计
- **AME RAG**: 知识库管理、文档检索
- **AME MEM**: 记忆学习、风格模仿

## 🚀 快速开始

### 方式 1：Gradio 本地运行（推荐）

```bash
cd gradio_app
./run.sh

# 访问: http://localhost:7860
```

### 方式 2：Docker 部署

```bash
# 一键构建和启动
./docker-build-gradio.sh

# 访问: http://localhost:7860
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

**前端**: Gradio 4.0 (专为 AI 应用设计)  
**AME 引擎**: v0.7.0
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