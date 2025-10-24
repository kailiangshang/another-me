#!/bin/bash
# Another Me 部署脚本

set -e

echo "========================================="
echo "Another Me - 一键部署脚本"
echo "========================================="

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "错误: Docker 未安装"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "错误: Docker Compose 未安装"
    exit 1
fi

# 进入项目根目录
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

echo ""
echo "开始构建镜像..."
docker-compose -f deployment/docker-compose.yml build

echo ""
echo "启动服务..."
docker-compose -f deployment/docker-compose.yml up -d

echo ""
echo "========================================="
echo "部署完成!"
echo "========================================="
echo "前端地址: http://localhost"
echo "后端 API: http://localhost:8000"
echo "API 文档: http://localhost:8000/docs"
echo ""
echo "查看日志: docker-compose -f deployment/docker-compose.yml logs -f"
echo "停止服务: docker-compose -f deployment/docker-compose.yml down"
echo "========================================="
