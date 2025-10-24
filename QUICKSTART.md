# Another Me - 快速启动指南

## 🚀 一键启动（推荐）

### 本地开发环境

```bash
# 一键启动前后端服务
chmod +x start.sh
./start.sh

# 服务会在后台运行，访问：
# - 前端: http://localhost:5173
# - 后端 API: http://localhost:8000
# - API 文档: http://localhost:8000/docs
```

### 停止服务

```bash
chmod +x stop.sh
./stop.sh
```

**功能**：
- ✅ 自动检查环境 (Python 3.11+, Node.js 18+)
- ✅ 自动安装依赖
- ✅ 后台运行服务
- ✅ 实时日志输出

---

## 🚀 后端启动

### 方式 1：直接运行

```bash
# 1. 进入后端目录
cd backend

# 2. 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt
pip install -r ../ame/requirements.txt

# 4. 启动服务
chmod +x run.sh
./run.sh

# 或直接运行
cd app
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**访问**:
- API 文档: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- 健康检查: http://localhost:8000/api/v1/health

### 测试 API

```bash
# 健康检查
curl http://localhost:8000/api/v1/health

# 测试配置（需要先配置 API Key）
curl -X POST http://localhost:8000/api/v1/config/save \
  -H "Content-Type: application/json" \
  -d '{"api_key":"sk-xxx","base_url":"https://api.openai.com/v1","model":"gpt-3.5-turbo"}'
```

---

## 🎨 前端启动

### 方式 1：直接运行

```bash
# 1. 进入前端目录
cd frontend

# 2. 安装依赖
npm install
# 或
yarn install

# 3. 启动开发服务器
chmod +x run.sh
./run.sh

# 或直接运行
npm run dev
```

**访问**: http://localhost:5173

### 构建生产版本

```bash
cd frontend
npm run build
npm run preview
```

---

## 🐳 Docker 部署

### 完整部署（推荐）

```bash
# 一键部署
chmod +x deployment/deploy.sh
./deployment/deploy.sh
```

**访问**:
- 前端: http://localhost
- 后端 API: http://localhost:8000
- API 文档: http://localhost:8000/docs

### 查看日志

```bash
# 查看所有服务日志
docker-compose -f deployment/docker-compose.yml logs -f

# 查看后端日志
docker-compose -f deployment/docker-compose.yml logs -f backend

# 查看前端日志
docker-compose -f deployment/docker-compose.yml logs -f frontend
```

### 停止服务

```bash
docker-compose -f deployment/docker-compose.yml down
```

---

## ⚙️ 配置说明

### 环境变量

创建 `.env` 文件（可选）：

```env
OPENAI_API_KEY=sk-your-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-3.5-turbo
```

### 首次使用

1. 启动后端和前端服务
2. 访问前端页面 http://localhost:5173
3. 点击侧边栏 **"配置"**
4. 输入 OpenAI API Key 和相关配置
5. 点击 **"测试配置"** 验证
6. 点击 **"保存配置"**
7. 开始使用！

---

## 🧪 功能测试

### 1. 配置管理

访问配置页面，测试：
- ✅ API Key 保存
- ✅ 配置加载
- ✅ 配置测试

### 2. MEM 对话

访问对话页面，测试：
- ✅ 发送消息
- ✅ 接收 AI 回复
- ✅ 消息历史记录

### 3. RAG 知识库（开发中）

访问知识库页面（骨架已实现）

### 4. 记忆管理（开发中）

访问记忆管理页面（骨架已实现）

---

## 🐛 常见问题

### 后端无法启动

**问题**: `ModuleNotFoundError`
**解决**: 确保安装了所有依赖
```bash
pip install -r requirements.txt
pip install -r ../ame/requirements.txt
```

**问题**: 端口 8000 被占用
**解决**: 修改端口或停止占用进程
```bash
lsof -i :8000  # 查看占用进程
kill -9 <PID>  # 停止进程
```

### 前端无法启动

**问题**: `node_modules` 错误
**解决**: 删除重新安装
```bash
rm -rf node_modules package-lock.json
npm install
```

**问题**: 端口 5173 被占用
**解决**: 修改 `vite.config.ts` 中的端口配置

### Docker 部署问题

**问题**: Docker 未安装
**解决**: 安装 Docker Desktop
- Mac: https://docs.docker.com/desktop/install/mac-install/
- Windows: https://docs.docker.com/desktop/install/windows-install/
- Linux: https://docs.docker.com/engine/install/

**问题**: 镜像构建失败
**解决**: 检查 Dockerfile 和网络连接

---

## 📝 下一步

1. ✅ 启动后端和前端服务
2. ✅ 配置 API Key
3. ✅ 测试对话功能
4. 🔄 完善 RAG 知识库页面
5. 🔄 完善记忆管理页面

---

## 📚 更多文档

- [PROJECT_SUMMARY.md](../PROJECT_SUMMARY.md) - 项目总结
- [IMPLEMENTATION_REPORT.md](../IMPLEMENTATION_REPORT.md) - 实施报告
- [docs/README.md](./README.md) - 完整文档

---

**祝使用愉快！** 🎉
