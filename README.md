# Another Me 🌟

**世界上另一个我 —— AI 数字分身系统**

> 用你的聊天记录、日记、知识训练出一个"像你"的 AI。数据本地存储，隐私安全。

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](DOCUMENTATION.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](backend/requirements.txt)
[![React](https://img.shields.io/badge/react-18.0+-blue.svg)](frontend/package.json)
[![FastAPI](https://img.shields.io/badge/fastapi-0.104+-green.svg)](backend/requirements.txt)

---

## ✨ 最新更新 (v1.0.0) - 架构优化版

### 🚀 **架构升级**
- ✅ **统一架构**: React + FastAPI，移除 Gradio 依赖
- ✅ **现代前端**: TypeScript + Vite + Zustand 状态管理
- ✅ **一键启动**: 全新的 start.sh 和 stop.sh 脚本
- ✅ **Docker 优化**: 简化的容器化部署方案

### 🔧 **功能增强**
- ✅ **RAG 完整实现**: 文档上传、知识检索、智能问答
- ✅ **真实 Embedding**: 集成 OpenAI Embedding API
- ✅ **流式输出**: 实时对话响应
- ✅ **状态持久化**: 聊天记录本地保存

### 📚 **代码质量**
- ✅ **TypeScript**: 完整的类型安全
- ✅ **模块化**: 前后端分离，清晰的代码组织
- ✅ **可扩展**: AME 引擎独立，易于扩展

📄 **[完整文档](DOCUMENTATION.md)**

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



## 🏗️ 项目架构

```
another-me/
├── frontend/              # React 前端应用
│   ├── src/
│   │   ├── api/           # API 客户端
│   │   ├── pages/         # 页面组件
│   │   ├── store/         # Zustand 状态管理
│   │   ├── types/         # TypeScript 类型
│   │   └── App.tsx        # 主应用
│   └── vite.config.ts   # Vite 配置
├── backend/               # FastAPI 后端
│   ├── app/
│   │   ├── api/v1/        # API 端点
│   │   ├── core/          # 核心配置
│   │   ├── middleware/    # 中间件
│   │   ├── models/        # 数据模型
│   │   ├── services/      # 业务逻辑
│   │   └── main.py        # 应用入口
│   └── requirements.txt
├── ame/                   # AME 技术引擎（独立模块）
│   ├── rag/               # RAG 模块：知识库管理
│   ├── mem/               # MEM 模块：记忆与模仿
│   ├── data_processor/    # 数据处理
│   ├── vector_store/      # 向量存储
│   ├── llm_caller/        # LLM 调用
│   └── retrieval/         # 复杂检索
├── deployment/            # Docker 部署
│   ├── docker/
│   │   ├── Dockerfile.backend
│   │   ├── Dockerfile.frontend
│   │   └── nginx.conf
│   ├── docker-compose.yml
│   └── deploy.sh
├── start.sh               # 本地一键启动
├── stop.sh                # 停止服务
└── README.md
```

**三层分离架构**：
- **React 前端**: TypeScript + Vite + Zustand，现代化的用户界面
- **FastAPI 后端**: Python 3.11+，高性能 API 服务
- **AME 引擎**: 独立的技术模块，支持 RAG 和 MEM 功能

## 🚀 快速开始

### 方式 1：本地开发运行（推荐）

```bash
# 一键启动前后端服务
./start.sh

# 访问:
# - 前端: http://localhost:5173
# - 后端API: http://localhost:8000
# - API文档: http://localhost:8000/docs

# 停止服务
./stop.sh
```

**功能特性**：
- ✅ 自动检查环境 (Python 3.11+, Node.js 18+)
- ✅ 自动安装依赖
- ✅ 后台运行，日志文件记录

### 方式 2：Docker 部署

```bash
# 一键构建和启动
cd deployment
./deploy.sh

# 访问:
# - 前端: http://localhost
# - 后端API: http://localhost:8000
```

### 🔑 初次使用

1. 访问应用 http://localhost:5173
2. 点击 **"配置"** 页面
3. 输入 OpenAI API Key 和相关配置
4. 点击 **"保存配置"**
5. 开始使用！

## 📖 完整文档

- [**DOCUMENTATION.md**](DOCUMENTATION.md) - 完整的技术文档和使用指南
- [**ame/README.md**](ame/README.md) - AME 技术引擎文档

## 🔐 隐私保证

- ✅ 数据完全本地存储
- ✅ 支持离线运行
- ✅ 开源可审计

## 🛠️ 技术栈

**前端**: React 18 + TypeScript + Vite + Zustand  
**后端**: FastAPI 0.104+ + Python 3.11+  
**AME 引擎**: v1.0.0
- 📚 **RAG 模块**: 知识库管理、文档检索、智能问答
- 💬 **MEM 模块**: 记忆学习、风格模仿、记忆管理
- 📊 数据处理 + 📦 向量存储 (Memu/ChromaDB)
- 🤖 LLM 调用 (异步+缓存+重试) + 🎯 混合检索  
**特性**: 流式输出 + 状态持久化 + 真实 Embedding + 响应式设计  
**部署**: Docker Compose 一键部署

> **AME (详见 `ame/README.md`)**: 独立的技术模块引擎，支持自定义扩展，v1.0.0 新增：
> - ✅ 异步处理系统
> - ✅ 真实 Embedding 支持
> - ✅ 智能缓存策略
> - ✅ 完善的错误处理



## 📄 License

MIT License

---