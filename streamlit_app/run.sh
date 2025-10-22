#!/bin/bash

# Another Me - Streamlit 应用启动脚本

echo "🌟 Another Me - Streamlit 版本"
echo "================================"

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 未安装"
    exit 1
fi

# 设置 PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/..:$(pwd)/../ame"

# 检查依赖
echo "📦 检查依赖..."
pip install -r requirements.txt -q

# 创建必要的目录
mkdir -p ../data/rag_uploads
mkdir -p ../data/mem_uploads
mkdir -p ../data/reports
mkdir -p ../data/rag_vector_store
mkdir -p ../data/mem_vector_store

# 启动 Streamlit
echo "🚀 启动 Streamlit..."
echo ""
echo "访问: http://localhost:8501"
echo ""

streamlit run app.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --theme.base="light" \
    --theme.primaryColor="#3498db" \
    --theme.backgroundColor="#ffffff" \
    --theme.secondaryBackgroundColor="#f0f2f6"
