# Dot-Store V1

## 项目概述

Dot-Store 是一个面向小微实体店铺的轻量化经营记录与理解工具，帮助老板从第一天开始，看清楚自己的生意，并且越用越清楚。

## 产品愿景与核心价值

### 产品愿景

Dot-Store 的核心目标不是：
- 管住老板
- 规范流程
- 复制大型企业 ERP

而是：

帮助老板从第一天开始，看清楚自己的生意，并且越用越清楚。

### 核心价值主张

1. 开箱即用的账务可见性
2. 接受真实世界的混乱，而不是强行规范
3. 所有数据都可解释、可修正
4. 记录成本低于人工记账

## 技术栈实现

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

## 核心功能模块

### 后端模块

1. **Event 模块** - 最底层事实记录层，记录系统中的所有事件
2. **Order 模块** - 业务理解层，用于记录订单和交易
3. **Ledger 模块** - 权威事实层，记录账务分录
4. **Report 模块** - 只读视图层，提供报表和汇总数据
5. **Audit 模块** - 记录数据修改历史，支持审计追踪
6. **Config 模块** - 用于存储系统配置

### 前端页面

1. **今日页面** - 显示今日盈亏和发生的记录
2. **记录页面** - 用于创建和管理记录
3. **账本页面** - 显示账务明细和分类账
4. **报表页面** - 提供盈亏趋势和分类分析
5. **设置页面** - 用于配置系统参数

## 项目结构

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

## API 文档

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

## 部署方式

### Docker Compose 部署（推荐）

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

3. 启动 Docker Compose 服务

```bash
docker-compose up -d
```

4. 执行数据库迁移

```bash
docker-compose exec api python -m alembic upgrade head
```

5. 验证服务是否正常运行

- API 服务：访问 http://localhost:8000/docs
- 前端应用：访问 http://localhost:3000

### 手动部署

详见 `DEPLOYMENT.md` 文档

## 开发规范

- 严格遵循 Architecture_README.md 进行系统架构设计
- 后端采用分层结构：Controller → Service → Model
- 前端采用组件化开发，使用 React Hooks 和 Context 管理状态
- 代码添加函数级注释
- 保持代码风格一致性

## 核心设计原则

1. **记录优先于规范** - 允许先记下来，再补充细节
2. **可解释优先于准确** - 数据可以不完美，但必须可解释
3. **修正优先于约束** - 允许手工调整，系统留下痕迹
4. **真实世界优先于系统优雅** - 接受业务不规范，数据可能滞后

## 后续发展方向

1. 进行单元测试和集成测试
2. 优化前端 UI/UX 设计
3. 添加更多报表类型和数据分析功能
4. 实现用户认证和权限管理
5. 优化性能和安全性
6. 支持更多数据源导入（如外卖平台数据）

## 项目亮点

- 模块化设计，便于扩展和维护
- 接受真实世界的不完美，允许数据不完整
- 支持手工修正和审计追踪
- 简洁易用的界面设计
- 容器化部署，便于快速上线

**Dot-Store V1 - 帮助老板从第一天开始，看清楚自己的生意，并且越用越清楚。**
