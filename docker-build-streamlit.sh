#!/bin/bash

# Another Me - Docker 构建脚本 (Streamlit 版本)
# 使用独立构建方式，不依赖 docker-compose

set -e

echo "🌟 Another Me - Docker 构建与部署 (Streamlit 版本)"
echo "===================================================="

# 配置
NETWORK_NAME="another-me-network"
APP_IMAGE="another-me-streamlit:latest"
APP_CONTAINER="another-me-app"
DATA_VOLUME="another-me-data"

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查 .env 文件
if [ ! -f .env ]; then
    echo -e "${YELLOW}📝 未找到 .env 文件，从模板创建...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠️  可以在启动后在前端配置 API Key（也可预先在 .env 中配置）${NC}"
fi

# 创建 Docker 网络
echo -e "${GREEN}🌐 创建 Docker 网络...${NC}"
docker network create ${NETWORK_NAME} 2>/dev/null || echo "网络已存在"

# 创建数据卷
echo -e "${GREEN}💾 创建数据卷...${NC}"
docker volume create ${DATA_VOLUME} 2>/dev/null || echo "数据卷已存在"

# 构建 Streamlit 应用镜像
echo -e "${GREEN}🔨 构建 Streamlit 应用镜像...${NC}"
docker build -t ${APP_IMAGE} \
    -f streamlit_app/Dockerfile \
    .

# 停止并删除旧容器
echo -e "${GREEN}🧹 清理旧容器...${NC}"
docker stop ${APP_CONTAINER} 2>/dev/null || true
docker rm ${APP_CONTAINER} 2>/dev/null || true

# 启动 Streamlit 应用容器
echo -e "${GREEN}🚀 启动 Streamlit 应用容器...${NC}"
docker run -d \
    --name ${APP_CONTAINER} \
    --network ${NETWORK_NAME} \
    -p 8501:8501 \
    -v ${DATA_VOLUME}:/app/data \
    -v "$(pwd)/ame:/app/ame" \
    --env-file .env \
    --restart unless-stopped \
    ${APP_IMAGE}

echo ""
echo -e "${GREEN}✅ Another Me 已成功启动！${NC}"
echo "===================================================="
echo -e "📍 Streamlit 应用: ${GREEN}http://localhost:8501${NC}"
echo ""
echo "💡 提示："
echo "  - API Key 可以在应用的配置页面设置"
echo "  - 查看日志: docker logs -f ${APP_CONTAINER}"
echo "  - 停止服务: docker stop ${APP_CONTAINER}"
echo ""
