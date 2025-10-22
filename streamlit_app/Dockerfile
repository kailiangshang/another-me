FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    xfonts-75dpi \
    xfonts-base \
    fontconfig \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# 安装 wkhtmltopdf（从官方源）
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.bullseye_amd64.deb \
    && apt-get update \
    && apt-get install -y ./wkhtmltox_0.12.6.1-2.bullseye_amd64.deb \
    && rm wkhtmltox_0.12.6.1-2.bullseye_amd64.deb \
    && rm -rf /var/lib/apt/lists/*

# 复制 AME 模块
COPY ame /app/ame

# 复制 Streamlit 应用
COPY streamlit_app /app/streamlit_app

# 安装 Python 依赖
WORKDIR /app/streamlit_app
RUN pip install --no-cache-dir -r requirements.txt

# 创建数据目录
RUN mkdir -p /app/data/rag_uploads \
    /app/data/mem_uploads \
    /app/data/reports \
    /app/data/rag_vector_store \
    /app/data/mem_vector_store

# 暴露端口
EXPOSE 8501

# 设置环境变量
ENV PYTHONPATH=/app:/app/ame:/app/streamlit_app

# 启动命令
CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--theme.base=light"]
