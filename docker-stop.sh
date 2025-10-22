#!/bin/bash

# Another Me - Docker 停止脚本

set -e

STREAMLIT_CONTAINER="another-me-streamlit"

echo "🛑 停止 Another Me..."

# 停止容器
docker stop ${STREAMLIT_CONTAINER} 2>/dev/null || true

# 删除容器
docker rm ${STREAMLIT_CONTAINER} 2>/dev/null || true

echo "✅ Another Me 已停止"
echo ""
echo "💡 提示："
echo "  - 数据已保存在 Docker 卷中"
echo "  - 重新启动: ./docker-build.sh"
echo "  - 完全清理（包括数据）: docker volume rm another-me-data"
