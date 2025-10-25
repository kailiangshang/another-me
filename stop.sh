#!/bin/bash

###############################################################################
# Another Me - 停止脚本
# 用途：停止所有运行中的前后端服务
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

# PID 文件
BACKEND_PID_FILE="$PROJECT_ROOT/.backend.pid"
FRONTEND_PID_FILE="$PROJECT_ROOT/.frontend.pid"

###############################################################################
# 工具函数
###############################################################################

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

###############################################################################
# 停止服务
###############################################################################

stop_service() {
    local service_name=$1
    local pid_file=$2
    
    if [ -f "$pid_file" ]; then
        PID=$(cat "$pid_file")
        if ps -p $PID > /dev/null 2>&1; then
            print_info "停止 $service_name (PID: $PID)..."
            kill $PID
            sleep 2
            
            # 强制停止
            if ps -p $PID > /dev/null 2>&1; then
                kill -9 $PID
            fi
            
            print_success "$service_name 已停止"
        else
            print_info "$service_name 未运行"
        fi
        rm -f "$pid_file"
    else
        print_info "$service_name 未运行（没有找到 PID 文件）"
    fi
}

###############################################################################
# 主函数
###############################################################################

main() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  停止 Another Me 服务${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    
    # 停止后端
    stop_service "后端服务" "$BACKEND_PID_FILE"
    
    # 停止前端
    stop_service "前端服务" "$FRONTEND_PID_FILE"
    
    # 清理日志文件（可选）
    if [ -f "$PROJECT_ROOT/backend.log" ] || [ -f "$PROJECT_ROOT/frontend.log" ]; then
        read -p "是否清理日志文件？(y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -f "$PROJECT_ROOT/backend.log"
            rm -f "$PROJECT_ROOT/frontend.log"
            print_success "日志文件已清理"
        fi
    fi
    
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  所有服务已停止${NC}"
    echo -e "${GREEN}========================================${NC}"
}

# 执行主函数
main
