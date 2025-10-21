#!/bin/bash

# Another Me - Docker 构建脚本
# 使用独立构建方式，不依赖 docker-compose

set -e

echo "🚀 Another Me - Docker 构建与部署"
echo "=================================="

# 配置
NETWORK_NAME="another-me-network"
BACKEND_IMAGE="another-me-backend:latest"
FRONTEND_IMAGE="another-me-frontend:latest"
BACKEND_CONTAINER="another-me-backend"
FRONTEND_CONTAINER="another-me-frontend"
DATA_VOLUME="another-me-data"

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查 .env 文件
if [ ! -f .env ]; then
    echo -e "${YELLOW}📝 未找到 .env 文件，从模板创建...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠️  请编辑 .env 文件配置 API Key（可选，也可启动后在前端配置）${NC}"
fi

# 创建 Docker 网络
echo -e "${GREEN}🌐 创建 Docker 网络...${NC}"
docker network create ${NETWORK_NAME} 2>/dev/null || echo "网络已存在"

# 创建数据卷
echo -e "${GREEN}💾 创建数据卷...${NC}"
docker volume create ${DATA_VOLUME} 2>/dev/null || echo "数据卷已存在"

# 构建后端镜像
echo -e "${GREEN}🔨 构建后端镜像...${NC}"
docker build -t ${BACKEND_IMAGE} \
    --build-arg PYTHONPATH=.:./ame:./backend \
    -f backend/Dockerfile \
    .

# 构建前端镜像
echo -e "${GREEN}🔨 构建前端镜像...${NC}"
docker build -t ${FRONTEND_IMAGE} \
    -f frontend/Dockerfile \
    frontend/

# 停止并删除旧容器
echo -e "${GREEN}🧹 清理旧容器...${NC}"
docker stop ${BACKEND_CONTAINER} ${FRONTEND_CONTAINER} 2>/dev/null || true
docker rm ${BACKEND_CONTAINER} ${FRONTEND_CONTAINER} 2>/dev/null || true

# 启动后端容器
echo -e "${GREEN}🚀 启动后端容器...${NC}"
docker run -d \
    --name ${BACKEND_CONTAINER} \
    --network ${NETWORK_NAME} \
    -p 8000:8000 \
    -v ${DATA_VOLUME}:/app/data \
    -v "$(pwd)/ame:/app/ame" \
    --env-file .env \
    --restart unless-stopped \
    ${BACKEND_IMAGE}

# 等待后端启动
echo -e "${GREEN}⏳ 等待后端启动...${NC}"
sleep 5

# 启动前端容器
echo -e "${GREEN}🚀 启动前端容器...${NC}"
docker run -d \
    --name ${FRONTEND_CONTAINER} \
    --network ${NETWORK_NAME} \
    -p 3000:3000 \
    -e VITE_API_BASE_URL=http://localhost:8000 \
    --restart unless-stopped \
    ${FRONTEND_IMAGE}

echo ""
echo -e "${GREEN}✅ Another Me 已成功启动！${NC}"
echo "=================================="
echo -e "📍 前端: ${GREEN}http://localhost:3000${NC}"
echo -e "📍 后端 API: ${GREEN}http://localhost:8000${NC}"
echo -e "📍 API 文档: ${GREEN}http://localhost:8000/docs${NC}"
echo ""
echo "💡 提示："
echo "  - API Key 可以启动后在前端配置，或在 .env 文件中预先配置"
echo "  - 查看日志: docker logs -f ${BACKEND_CONTAINER}"
echo "  - 停止服务: ./docker-stop.sh"
echo ""
