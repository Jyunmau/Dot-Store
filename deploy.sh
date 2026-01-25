#!/bin/bash

# Dot-Store 服务部署脚本
# 用于启动、停止、重启和查看服务状态

# 定义颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 显示帮助信息
show_help() {
    echo -e "${BLUE}Dot-Store 服务部署脚本${NC}"
    echo -e "
用法: $0 [选项] [服务名]

选项:
  up          启动所有服务或指定服务
  down        停止所有服务或指定服务
  restart     重启所有服务或指定服务
  status      查看所有服务或指定服务状态
  logs        查看所有服务或指定服务日志
  help        显示帮助信息

服务名:
  所有服务: api-gateway, order-service, ledger-service, event-service, config-service, report-service, auth-service, frontend
  基础设施: db, consul, rabbitmq, prometheus, grafana, elasticsearch, kibana
  
示例:
  $0 up                    # 启动所有服务
  $0 up api-gateway order-service  # 启动指定服务
  $0 down                  # 停止所有服务
  $0 status                # 查看所有服务状态
  $0 logs api-gateway      # 查看指定服务日志
"
}

# 检查是否安装了 docker-compose
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}错误: docker-compose 未安装${NC}"
        echo -e "请安装 docker-compose 后再运行此脚本"
        exit 1
    fi
}

# 启动服务
start_services() {
    if [ $# -eq 0 ]; then
        echo -e "${GREEN}启动所有服务...${NC}"
        docker-compose up -d
    else
        echo -e "${GREEN}启动指定服务: $*${NC}"
        docker-compose up -d "$@"
    fi
}

# 停止服务
stop_services() {
    if [ $# -eq 0 ]; then
        echo -e "${YELLOW}停止所有服务...${NC}"
        docker-compose down
    else
        echo -e "${YELLOW}停止指定服务: $*${NC}"
        docker-compose stop "$@"
    fi
}

# 重启服务
restart_services() {
    if [ $# -eq 0 ]; then
        echo -e "${BLUE}重启所有服务...${NC}"
        docker-compose restart
    else
        echo -e "${BLUE}重启指定服务: $*${NC}"
        docker-compose restart "$@"
    fi
}

# 查看服务状态
show_status() {
    echo -e "${BLUE}查看服务状态...${NC}"
    docker-compose ps "$@"
}

# 查看服务日志
show_logs() {
    if [ $# -eq 0 ]; then
        echo -e "${BLUE}查看所有服务日志...${NC}"
        docker-compose logs -f
    else
        echo -e "${BLUE}查看指定服务日志: $*${NC}"
        docker-compose logs -f "$@"
    fi
}

# 主函数
main() {
    check_docker_compose
    
    case "$1" in
        up)
            shift
            start_services "$@"
            ;;
        down)
            shift
            stop_services "$@"
            ;;
        restart)
            shift
            restart_services "$@"
            ;;
        status)
            shift
            show_status "$@"
            ;;
        logs)
            shift
            show_logs "$@"
            ;;
        help)
            show_help
            ;;
        *)
            echo -e "${RED}错误: 无效选项 '$1'${NC}"
            show_help
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"