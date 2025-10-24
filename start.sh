#!/bin/bash

###############################################################################
# Another Me - 统一启动脚本
# 用途：一键启动前后端开发环境
###############################################################################

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

# PID 文件
BACKEND_PID_FILE="$PROJECT_ROOT/.backend.pid"
FRONTEND_PID_FILE="$PROJECT_ROOT/.frontend.pid"

###############################################################################
# 工具函数
###############################################################################

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  Another Me - AI 分身系统${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

check_command() {
    if ! command -v $1 &> /dev/null; then
        print_error "$1 未安装，请先安装 $1"
        return 1
    fi
    return 0
}

###############################################################################
# 环境检查
###############################################################################

check_environment() {
    print_info "检查运行环境..."
    
    # 检查 Python
    if ! check_command python3; then
        exit 1
    fi
    
    # 检查 Python 版本
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    REQUIRED_VERSION="3.11"
    if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
        print_error "Python 版本需要 >= 3.11，当前版本: $PYTHON_VERSION"
        exit 1
    fi
    print_success "Python 版本: $PYTHON_VERSION"
    
    # 检查 Node.js
    if ! check_command node; then
        exit 1
    fi
    
    NODE_VERSION=$(node --version | sed 's/v//')
    REQUIRED_NODE="18.0.0"
    if [ "$(printf '%s\n' "$REQUIRED_NODE" "$NODE_VERSION" | sort -V | head -n1)" != "$REQUIRED_NODE" ]; then
        print_error "Node.js 版本需要 >= 18.0，当前版本: $NODE_VERSION"
        exit 1
    fi
    print_success "Node.js 版本: $NODE_VERSION"
    
    # 检查 npm
    if ! check_command npm; then
        exit 1
    fi
    print_success "npm 版本: $(npm --version)"
    
    echo ""
}

###############################################################################
# 后端启动
###############################################################################

start_backend() {
    print_info "准备启动后端服务..."
    
    # 进入后端目录
    cd "$BACKEND_DIR"
    
    # 检查虚拟环境
    if [ ! -d "venv" ]; then
        print_info "创建 Python 虚拟环境..."
        python3 -m venv venv
        print_success "虚拟环境创建成功"
    fi
    
    # 激活虚拟环境
    source venv/bin/activate
    
    # 安装依赖
    print_info "安装后端依赖..."
    pip install -q --upgrade pip
    pip install -q -r requirements.txt
    print_success "后端依赖安装完成"
    
    # 检查 AME 模块
    if [ -d "$PROJECT_ROOT/ame" ]; then
        print_info "安装 AME 引擎..."
        cd "$PROJECT_ROOT/ame"
        pip install -q -e .
        print_success "AME 引擎安装完成"
        cd "$BACKEND_DIR"
    fi
    
    # 启动后端服务（后台运行）
    print_info "启动 FastAPI 后端服务..."
    nohup python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > "$PROJECT_ROOT/backend.log" 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > "$BACKEND_PID_FILE"
    
    # 等待后端启动
    sleep 3
    
    # 检查后端是否成功启动
    if ps -p $BACKEND_PID > /dev/null; then
        print_success "后端服务已启动 (PID: $BACKEND_PID)"
        print_success "后端地址: http://localhost:8000"
        print_info "API 文档: http://localhost:8000/docs"
    else
        print_error "后端启动失败，请检查日志: $PROJECT_ROOT/backend.log"
        exit 1
    fi
    
    echo ""
}

###############################################################################
# 前端启动
###############################################################################

start_frontend() {
    print_info "准备启动前端服务..."
    
    # 进入前端目录
    cd "$FRONTEND_DIR"
    
    # 安装依赖
    if [ ! -d "node_modules" ]; then
        print_info "安装前端依赖..."
        npm install
        print_success "前端依赖安装完成"
    else
        print_success "前端依赖已存在"
    fi
    
    # 启动前端服务（后台运行）
    print_info "启动 React 前端服务..."
    nohup npm run dev > "$PROJECT_ROOT/frontend.log" 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > "$FRONTEND_PID_FILE"
    
    # 等待前端启动
    sleep 5
    
    # 检查前端是否成功启动
    if ps -p $FRONTEND_PID > /dev/null; then
        print_success "前端服务已启动 (PID: $FRONTEND_PID)"
        print_success "前端地址: http://localhost:5173"
    else
        print_error "前端启动失败，请检查日志: $PROJECT_ROOT/frontend.log"
        exit 1
    fi
    
    echo ""
}

###############################################################################
# 主函数
###############################################################################

main() {
    print_header
    echo ""
    
    # 检查环境
    check_environment
    
    # 启动后端
    start_backend
    
    # 启动前端
    start_frontend
    
    # 显示访问信息
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  服务启动成功！${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "  前端界面: ${BLUE}http://localhost:5173${NC}"
    echo -e "  后端 API: ${BLUE}http://localhost:8000${NC}"
    echo -e "  API 文档: ${BLUE}http://localhost:8000/docs${NC}"
    echo ""
    echo -e "  后端日志: ${YELLOW}$PROJECT_ROOT/backend.log${NC}"
    echo -e "  前端日志: ${YELLOW}$PROJECT_ROOT/frontend.log${NC}"
    echo ""
    echo -e "  停止服务: ${RED}./stop.sh${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    
    # 提示查看日志
    print_info "服务正在后台运行，使用 ./stop.sh 停止服务"
    print_info "实时查看后端日志: tail -f backend.log"
    print_info "实时查看前端日志: tail -f frontend.log"
}

# 执行主函数
main
