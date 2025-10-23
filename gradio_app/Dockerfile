FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖（仅基础工具）
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 复制 AME 模块
COPY ame /app/ame

# 复制 Gradio 应用
COPY gradio_app /app/gradio_app

# 复制 Logo
COPY ["another me logo.jpg", "/app/"]

# 安装 Python 依赖
WORKDIR /app/gradio_app
RUN pip install --no-cache-dir -r requirements.txt

# 创建数据目录
RUN mkdir -p /app/data/rag_uploads \
    /app/data/mem_uploads \
    /app/data/reports \
    /app/data/rag_vector_store \
    /app/data/mem_vector_store

# 声明数据卷
VOLUME ["/app/data"]

# 暴露端口
EXPOSE 7860

# 设置环境变量
ENV PYTHONPATH=/app:/app/ame:/app/gradio_app
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=7860

# 启动命令
CMD ["python", "app.py"]
