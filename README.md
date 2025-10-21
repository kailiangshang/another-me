# Another Me 🌟

**世界上另一个我 —— 隐私优先的 AI 分身系统**

> 用你的聊天记录、日记、照片训练出一个"像你"的 AI。所有数据仅存本地，无需联网。

[![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)](DOCUMENTATION.md#版本历史)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](backend/requirements.txt)
[![React](https://img.shields.io/badge/react-18.2-blue.svg)](frontend/package.json)

---

## 🎯 核心理念

**业务功能驱动，技术模块支撑**

- 🔹 **业务功能**：面向用户价值，描述"能做什么"
- 🔹 **技术功能**：面向系统实现，描述"如何做到"

---

## 💼 业务功能

### 1. 模仿我说话 (Mimic Me)
让 AI 用你的语气、风格和思维方式回应问题。

**场景示例：**
- "如果我在 2020 年听到这句话，我会怎么回答？"
- "帮我写一条朋友圈，要像我自己写的。"

### 2. 自我认知分析 (Know Myself)
帮你更客观地认识自己，发现盲点。

**场景示例：**
- "我最近情绪怎么样？"
- "我最常提到的人是谁？"
- "我的价值观有哪些关键词？"

### 3. 记忆回溯对话 (Remember Me)
唤醒你遗忘的记忆，实现"时空对话"。

**场景示例：**
- "去年这个时候我在想什么？"
- "上次我遇到类似问题是怎么解决的？"



## 🏗️ 项目架构

```
another-me/
├── ame/              # AME - Another Me Engine（独立技术模块引擎）
│   ├── data_processor/   # 数据处理模块
│   ├── vector_store/     # 向量存储模块（支持 Memu/ChromaDB）
│   ├── llm_caller/       # LLM 调用模块
│   └── rag_generator/    # RAG 生成模块
├── backend/          # 后端 Pipeline（业务编排层）
│   ├── app/
│   │   ├── api/         # API 路由
│   │   ├── services/    # 业务服务（调用 AME 模块）
│   │   └── core/        # 核心配置
├── frontend/         # 前端（用户交互层）
└── docker-compose.yml
```

**三层分离架构**：
- **Frontend**: 数据上传、业务选择、配置管理
- **Backend Pipeline**: 业务编排，调用 AME 技术模块
- **AME Engine**: 独立技术模块，可复用、可测试

## 🚀 快速开始

```bash
# 1. 配置环境变量
cp .env.example .env
vim .env  # 填入你的 OpenAI API Key

# 2. 一键启动
./start.sh

# 3. 访问应用
# 前端: http://localhost:3000
# 后端: http://localhost:8000
# API 文档: http://localhost:8000/docs
```

## 📖 完整文档

查看 [**DOCUMENTATION.md**](DOCUMENTATION.md) 获取：
- 详细使用指南
- 开发文档
- API 文档
- 技术优化说明
- 故障排查
- 更多示例

## 🔐 隐私保证

- ✅ 数据完全本地存储
- ✅ 支持离线运行
- ✅ 开源可审计

## 🛠️ 技术栈

**前端**: React + Vite + TypeScript + TailwindCSS  
**后端**: FastAPI + Python 3.11+  
**AME 引擎**: 独立技术模块（数据处理、向量存储、LLM调用、RAG生成）  
**向量库**: Memu / ChromaDB  
**部署**: Docker Compose

> **AME (另详见 `ame/README.md`)**: 独立的技术模块引擎，可在其他项目中复用



## 📄 License

MIT License

---


