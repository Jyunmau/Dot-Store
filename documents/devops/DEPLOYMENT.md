# Dot-Store V1 部署文档

## 1. 项目概述

Dot-Store 是一个面向小微实体店铺的轻量化经营记录与理解工具，采用前后端分离架构，后端使用 FastAPI + PostgreSQL，前端使用 React + Vite。

## 2. 技术栈

| 层级 | 技术选型 |
|------|----------|
| 后端语言 | Python 3.11+ |
| Web 框架 | FastAPI |
| ORM | SQLAlchemy 2.x |
| 数据库 | PostgreSQL 14+ |
| 数据迁移 | Alembic |
| 前端框架 | React + Vite |
| UI 策略 | Headless UI + 自建设计规范 |
| 状态管理 | React Hooks / Context |
| 容器化 | Docker + docker-compose |

## 3. 部署方式

### 3.1 Docker Compose 部署（推荐）

#### 3.1.1 前置条件

- 已安装 Docker 和 docker-compose
- 确保所需端口（默认：5432, 8000, 80）未被占用

#### 3.1.2 部署步骤

1. 克隆项目代码到服务器

```bash
git clone <repository-url>
cd Dot-Store
```

2. 配置环境变量

复制 `.env.example` 文件为 `.env`，并根据实际情况修改配置：

```bash
cp .env.example .env
# 编辑 .env 文件，修改数据库连接等配置
```

可配置的环境变量包括：

| 变量名 | 描述 | 默认值 |
|--------|------|--------|
| DB_USER | 数据库用户名 | postgres |
| DB_PASSWORD | 数据库密码 | postgres |
| DB_NAME | 数据库名称 | dot_store |
| DB_PORT | 数据库端口 | 5432 |
| API_PORT | API 服务端口 | 8000 |
| API_HOST | API 服务主机名 | localhost |
| APP_DEBUG | 是否开启调试模式 | false |
| LOG_LEVEL | 日志级别 | INFO |
| FRONTEND_PORT | 前端服务端口 | 80 |

3. 启动 Docker Compose 服务

```bash
docker-compose up -d
```

4. 执行数据库迁移

```bash
docker-compose exec api python -m alembic upgrade head
```

5. 验证服务是否正常运行

- API 服务：访问 http://localhost:8000/docs，应该能看到 Swagger 文档
- API 健康检查：访问 http://localhost:8000/health，应该返回 {"status": "healthy"}
- 前端应用：访问 http://localhost:80（默认），应该能看到 Dot-Store 应用

### 3.2 一键部署脚本（推荐）

我们提供了一键部署脚本，可以简化部署流程。

#### 3.2.1 使用方法

```bash
chmod +x deploy.sh
./deploy.sh
```

脚本会自动完成以下操作：
1. 检查 Docker 和 docker-compose 是否安装
2. 配置环境变量
3. 启动 Docker Compose 服务
4. 执行数据库迁移
5. 验证服务是否正常运行

### 3.3 手动部署

#### 3.3.1 后端部署

1. 安装 Python 依赖

```bash
cd apps/api-server
pip3 install -r requirements.txt
```

2. 配置环境变量

创建 `.env` 文件，配置数据库连接等信息：

```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/dot_store
APP_DEBUG=True
LOG_LEVEL=INFO
```

3. 执行数据库迁移

```bash
python3 -m alembic upgrade head
```

4. 启动 API 服务

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

#### 3.3.2 前端部署

1. 安装前端依赖

```bash
cd apps/frontend
npm install
```

2. 构建前端应用

```bash
npm run build
```

3. 部署构建后的静态文件

将 `dist` 目录下的文件部署到 Nginx 或其他静态文件服务器。

示例 Nginx 配置：

```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        root /path/to/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
}
```

#### 3.3.2 前端部署

1. 安装前端依赖

```bash
cd apps/frontend
npm install
```

2. 构建前端应用

```bash
npm run build
```

3. 部署构建后的静态文件

将 `dist` 目录下的文件部署到 Nginx 或其他静态文件服务器。

## 4. 目录结构说明

```
Dot-Store/
├── apps/              # 应用目录
│   ├── api-server/    # 后端 API 服务
│   └── frontend/      # 前端应用
├── modules/           # 核心模块
│   ├── event/         # 事件模块
│   ├── order/         # 订单模块
│   ├── ledger/        # 账务模块
│   ├── report/        # 报表模块
│   ├── audit/         # 审计模块
│   └── config/        # 配置模块
├── shared/            # 共享组件
│   ├── db/            # 数据库相关
│   └── utils/         # 工具函数
├── .env               # 环境变量配置
├── docker-compose.yml # Docker 配置
└── DEPLOYMENT.md      # 部署文档
```

## 5. API 文档

API 服务启动后，可以通过以下地址访问 Swagger 文档：

```
http://localhost:8000/docs
```

主要 API 端点：

| 模块 | API 路径 | 说明 |
|------|----------|------|
| 订单 | POST /api/orders | 创建订单 |
| 订单 | GET /api/orders/{id} | 获取订单详情 |
| 订单 | PUT /api/orders/{id} | 更新订单 |
| 订单 | GET /api/orders | 获取订单列表 |
| 账务 | POST /api/ledger/accounts | 创建分类账 |
| 账务 | GET /api/ledger/accounts | 获取分类账列表 |
| 账务 | POST /api/ledger/entries | 创建账务分录 |
| 账务 | GET /api/ledger/entries | 获取账务分录列表 |
| 报表 | GET /api/reports/summary | 获取报表汇总 |
| 报表 | GET /api/reports/income-structure | 获取收入结构 |
| 报表 | GET /api/reports/expense-structure | 获取成本结构 |
| 配置 | POST /api/config | 创建/更新配置 |
| 配置 | GET /api/config | 获取配置列表 |
| 配置 | GET /api/config/{key} | 根据 Key 获取配置 |

## 6. 数据库维护

### 6.1 数据迁移

创建新的迁移脚本：

```bash
docker-compose exec api python -m alembic revision --autogenerate -m "Migration message"
```

应用所有迁移：

```bash
docker-compose exec api python -m alembic upgrade head
```

回滚到上一个版本：

```bash
docker-compose exec api python -m alembic downgrade -1
```

### 6.2 数据库备份

使用 `pg_dump` 命令备份数据库：

```bash
docker-compose exec db pg_dump -U postgres dot_store > dot_store_backup.sql
```

恢复数据库：

```bash
docker-compose exec -T db psql -U postgres dot_store < dot_store_backup.sql
```

## 7. 常见问题与解决方案

### 7.1 服务启动失败

- 检查 Docker 容器状态：`docker-compose ps`
- 查看容器日志：`docker-compose logs <service-name>`
- 检查端口是否被占用：`lsof -i :8000` 或 `netstat -tlnp | grep 8000`

### 7.2 数据库连接失败

- 确保 PostgreSQL 服务正在运行：`docker-compose ps db`
- 检查 `.env` 文件中的数据库连接配置是否正确
- 确保数据库用户和密码正确

### 7.3 API 访问返回 500 错误

- 查看 API 服务日志：`docker-compose logs api`
- 检查数据库连接是否正常
- 检查相关业务逻辑是否存在错误

## 8. 监控与日志

### 8.1 查看服务日志

```bash
# 查看所有服务日志
docker-compose logs

# 查看指定服务日志
docker-compose logs <service-name>

# 实时查看日志
docker-compose logs -f <service-name>
```

### 8.2 日志配置

日志配置在 `.env` 文件中，可根据需要修改 `LOG_LEVEL` 配置项（可选值：DEBUG, INFO, WARNING, ERROR, CRITICAL）。

## 9. 安全建议

1. 生产环境中修改默认的数据库密码
2. 配置 Nginx 反向代理，添加 HTTPS 支持
3. 限制 API 服务的访问 IP
4. 定期备份数据库
5. 定期更新依赖包，修复安全漏洞

## 10. 版本升级

1. 备份当前代码和数据库
2. 拉取最新代码
3. 执行数据库迁移：`docker-compose exec api python -m alembic upgrade head`
4. 重启服务：`docker-compose restart`

## 11. 联系方式

如遇到部署问题，可通过以下方式获取帮助：

- 提交 Issue 到 GitHub 仓库
- 联系项目维护人员

---

**Dot-Store V1 - 帮助老板从第一天开始，看清楚自己的生意，并且越用越清楚。**
