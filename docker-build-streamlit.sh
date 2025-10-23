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

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo -e "${BLUE}📝 请配置启动参数（直接回车使用默认值）${NC}"
echo "===================================================="

# 端口配置
echo ""
read -p "请输入 Streamlit 端口 [默认: 8501]: " STREAMLIT_PORT
STREAMLIT_PORT=${STREAMLIT_PORT:-8501}

# 数据持久化目录配置
echo ""
read -p "请输入数据持久化目录 [默认: ./data]: " DATA_DIR
DATA_DIR=${DATA_DIR:-./data}

# 创建数据目录
if [ ! -d "$DATA_DIR" ]; then
    echo -e "${YELLOW}📁 创建数据目录: $DATA_DIR${NC}"
    mkdir -p "$DATA_DIR"
fi

# 显示配置总结
echo ""
echo -e "${GREEN}✅ 配置总结${NC}"
echo "===================================================="
echo "Streamlit 端口: $STREAMLIT_PORT"
echo "数据目录: $DATA_DIR"
echo "===================================================="
echo ""
read -p "按回车继续构建，或 Ctrl+C 取消..."

# 检查 .env 文件
if [ ! -f .env ]; then
    echo -e "${YELLOW}📝 未找到 .env 文件，从模板创建...${NC}"
    if [ -f .env.example ]; then
        cp .env.example .env
    else
        # 创建基础 .env 文件
        cat > .env << EOF
# OpenAI API Configuration
OPENAI_API_KEY=
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-3.5-turbo
EOF
    fi
    echo -e "${YELLOW}⚠️  可以在启动后在前端配置 API Key（也可预先在 .env 中配置）${NC}"
fi

# 创建 Docker 网络
echo -e "${GREEN}🌐 创建 Docker 网络...${NC}"
docker network create ${NETWORK_NAME} 2>/dev/null || echo "网络已存在"

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
    -p ${STREAMLIT_PORT}:8501 \
    -v "$(pwd)/${DATA_DIR}:/app/data" \
    -v "$(pwd)/ame:/app/ame" \
    --env-file .env \
    --restart unless-stopped \
    ${APP_IMAGE}

echo ""
echo -e "${GREEN}✅ Another Me 已成功启动！${NC}"
echo "===================================================="
echo -e "📍 Streamlit 应用: ${GREEN}http://localhost:${STREAMLIT_PORT}${NC}"
echo ""
echo "💡 提示："
echo "  - API Key 可以在应用的配置页面设置"
echo "  - 数据已持久化到: ${DATA_DIR}"
echo "  - 查看日志: docker logs -f ${APP_CONTAINER}"
echo "  - 停止服务: docker stop ${APP_CONTAINER}"
echo "  - 删除容器: docker rm ${APP_CONTAINER}"
echo ""
