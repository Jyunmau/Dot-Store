#!/bin/bash

# Dot-Store 一键部署脚本

# 定义颜色常量
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 打印信息
function echo_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

function echo_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

function echo_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查 Docker 是否安装
function check_docker() {
    echo_info "检查 Docker 是否安装..."
    if ! command -v docker &> /dev/null; then
        echo_error "Docker 未安装，请先安装 Docker"
        exit 1
    fi
    echo_info "Docker 已安装: $(docker --version)"
}

# 检查 docker-compose 是否安装
function check_docker_compose() {
    echo_info "检查 docker-compose 是否安装..."
    if ! command -v docker-compose &> /dev/null; then
        echo_error "docker-compose 未安装，请先安装 docker-compose"
        exit 1
    fi
    echo_info "docker-compose 已安装: $(docker-compose --version)"
}

# 配置环境变量
function config_env() {
    echo_info "配置环境变量..."
    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            cp .env.example .env
            echo_info "已从 .env.example 创建 .env 文件"
        else
            echo_error ".env.example 文件不存在，请手动创建 .env 文件"
            exit 1
        fi
    else
        echo_warning ".env 文件已存在，将使用现有配置"
    fi
}

# 启动 Docker Compose 服务
function start_services() {
    echo_info "启动 Docker Compose 服务..."
    docker-compose up -d
    if [ $? -ne 0 ]; then
        echo_error "启动服务失败，请检查日志: docker-compose logs"
        exit 1
    fi
    echo_info "服务启动成功"
}

# 执行数据库迁移
function run_migrations() {
    echo_info "执行数据库迁移..."
    # 等待数据库服务启动
    echo_info "等待数据库服务启动..."
    sleep 10
    docker-compose exec api python -m alembic upgrade head
    if [ $? -ne 0 ]; then
        echo_error "数据库迁移失败，请检查日志: docker-compose logs api"
        exit 1
    fi
    echo_info "数据库迁移成功"
}

# 验证服务是否正常运行
function verify_services() {
    echo_info "验证服务是否正常运行..."
    
    # 检查 API 服务健康状态
    echo_info "检查 API 服务健康状态..."
    API_HEALTH=$(curl -s http://localhost:8000/health)
    if [ "$API_HEALTH" == '{"status":"healthy"}' ]; then
        echo_info "API 服务健康状态正常"
    else
        echo_error "API 服务健康检查失败，请检查日志: docker-compose logs api"
        exit 1
    fi
    
    # 检查前端服务是否可访问
    echo_info "检查前端服务是否可访问..."
    FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:80)
    if [ "$FRONTEND_STATUS" == "200" ]; then
        echo_info "前端服务可正常访问"
    else
        echo_error "前端服务访问失败，HTTP 状态码: $FRONTEND_STATUS，请检查日志: docker-compose logs frontend"
        exit 1
    fi
    
    echo_info "所有服务验证通过！"
}

# 显示部署结果
function show_result() {
    echo_info "部署完成！"
    echo_info "服务访问地址："
    echo_info "- 前端应用：http://localhost:80"
    echo_info "- API 文档：http://localhost:8000/docs"
    echo_info "- API 健康检查：http://localhost:8000/health"
}

# 主函数
function main() {
    echo_info "开始部署 Dot-Store..."
    check_docker
    check_docker_compose
    config_env
    start_services
    run_migrations
    verify_services
    show_result
    echo_info "部署完成！"
}

# 执行主函数
main