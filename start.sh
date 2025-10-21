#!/bin/bash

echo "🚀 Starting Another Me..."

# 检查 .env 文件
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your OpenAI API Key"
    exit 1
fi

# 创建数据目录
mkdir -p data/uploads data/vector_store

# 启动服务
echo "🐳 Starting Docker containers..."
docker-compose up -d

echo "✅ Another Me is running!"
echo ""
echo "📍 Frontend: http://localhost:3000"
echo "📍 Backend API: http://localhost:8000"
echo "📍 API Docs: http://localhost:8000/docs"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
