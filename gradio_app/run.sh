#!/bin/bash

# Another Me - Gradio 本地运行脚本

echo "🌟 Another Me - 启动 Gradio 应用"
echo "===================================="

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3，请先安装 Python 3.11+"
    exit 1
fi

# 检查依赖
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

echo "🔄 激活虚拟环境..."
source venv/bin/activate

echo "📦 安装依赖..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo "🚀 启动 Gradio 应用..."
echo ""
echo "访问: http://localhost:7860"
echo ""

python app.py
