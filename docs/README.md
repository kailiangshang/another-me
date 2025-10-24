# Another Me - 项目文档

## 概述

Another Me 是一个基于 RAG (Retrieval-Augmented Generation) 技术和记忆模仿的 AI 数字分身系统。

**版本**: v1.0.0  
**架构**: 前后端分离

## 技术栈

### 后端
- **框架**: FastAPI (Python 3.11+)
- **技术引擎**: AME (Another Me Engine)
- **向量数据库**: Memu
- **LLM**: OpenAI API 兼容接口

### 前端
- **框架**: React 18 + TypeScript
- **构建工具**: Vite
- **状态管理**: Zustand
- **UI 组件库**: Ant Design
- **样式**: TailwindCSS

## 核心功能

### 1. RAG 知识库
- 文档上传和向量化存储
- 智能检索和问答
- 多种文档格式支持

### 2. MEM 记忆对话
- 学习用户说话风格
- 模仿用户表达方式
- 流式对话体验

### 3. 配置管理
- API Key 配置
- 模型选择
- 系统参数调整

## 目录结构

```
another-me/
├── ame/                    # AME 技术引擎
│   ├── rag/                # RAG 模块
│   ├── mem/                # MEM 模块
│   ├── vector_store/       # 向量存储
│   ├── retrieval/          # 检索模块
│   ├── llm_caller/         # LLM 调用
│   └── data_processor/     # 数据处理
├── backend/                # 后端 API
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── services/       # 业务逻辑
│   │   ├── middleware/     # 中间件
│   │   ├── core/           # 核心配置
│   │   └── models/         # 数据模型
│   └── requirements.txt
├── frontend/               # 前端应用 (待实现)
├── data/                   # 数据存储
│   ├── rag_vector_store/
│   ├── mem_vector_store/
│   ├── uploads/
│   ├── logs/
│   └── config/
└── docs/                   # 文档
```

## 快速开始

### 环境要求
- Python 3.11+
- Node.js 18+ (前端)
- pip

### 后端启动

1. 进入后端目录:
```bash
cd backend
```

2. 创建虚拟环境:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\\Scripts\\activate  # Windows
```

3. 安装依赖:
```bash
pip install -r requirements.txt
# 同时安装 AME 引擎依赖
pip install -r ../ame/requirements.txt
```

4. 配置环境变量（可选）:
```bash
cp ../.env.example .env
# 编辑 .env 文件，配置 API Key
```

5. 启动服务:
```bash
chmod +x run.sh
./run.sh
```

服务将在 http://localhost:8000 启动

### API 文档

启动后访问:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 配置说明

### API Key 配置

系统支持通过以下方式配置:

1. **环境变量** (.env 文件):
```env
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-3.5-turbo
```

2. **配置 API**:
通过前端界面或 API 调用 `/api/v1/config/save` 配置

### 数据路径配置

默认数据存储在 `data/` 目录:
- RAG 向量库: `data/rag_vector_store/`
- MEM 向量库: `data/mem_vector_store/`
- 上传文件: `data/uploads/`
- 日志: `data/logs/`

## 开发指南

详见 [DEVELOPMENT.md](./DEVELOPMENT.md)

## 部署指南

详见 [DEPLOYMENT.md](./DEPLOYMENT.md)

## API 文档

详见 [API.md](./API.md)

## 许可证

MIT License
