# Dot-Store 点单收银系统

## 项目简介

Dot-Store 是一款面向小微商户的点单收银系统，支持多店铺管理、店员权限管理、订单管理、收支管理等功能。

**当前版本：V2.1**

## 技术栈

### 后端
- **框架**: FastAPI (Python 3.11+)
- **数据库**: PostgreSQL 15
- **缓存**: Redis 7
- **认证**: JWT (python-jose)
- **ORM**: SQLAlchemy 2.0

### 前端
- **框架**: React 18 + TypeScript
- **构建工具**: Vite 5
- **UI组件库**: Ant Design 5
- **状态管理**: Zustand
- **HTTP客户端**: Axios
- **样式**: Tailwind CSS

## 项目结构

```
Dot-Store/
├── apps/
│   ├── api-server/          # 后端服务
│   │   ├── app/
│   │   │   ├── api/         # API路由
│   │   │   ├── core/        # 核心配置
│   │   │   ├── models/      # 数据模型
│   │   │   ├── schemas/     # Pydantic模型
│   │   │   ├── services/    # 业务服务
│   │   │   └── main.py      # 应用入口
│   │   ├── alembic/         # 数据库迁移
│   │   └── requirements.txt
│   ├── frontend/            # 前端应用
│   │   ├── src/
│   │   │   ├── pages/       # 页面组件
│   │   │   ├── store/       # 状态管理
│   │   │   ├── services/    # API服务
│   │   │   └── types/       # 类型定义
│   │   └── package.json
│   └── _archive/            # 归档代码
├── documents/               # 项目文档
│   ├── prd/                 # 产品需求文档
│   ├── architecture/        # 技术设计文档
│   ├── design/              # 设计文档
│   └── plan/                # 计划文档
├── docker-compose.yml
└── README.md
```

## 快速开始

### 环境要求
- Docker 20.10+
- Docker Compose 2.0+
- Node.js 20+ (本地开发)
- Python 3.11+ (本地开发)

### 使用Docker启动

```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 停止所有服务
docker-compose down
```

服务启动后：
- 前端：http://localhost
- 后端API：http://localhost:8000
- API文档：http://localhost:8000/docs

### 本地开发

#### 后端开发

```bash
cd apps/api-server

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn app.main:app --reload --port 8000
```

#### 前端开发

```bash
cd apps/frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## V2.1 版本功能

### Sprint 1: 用户认证与权限管理
- ✅ 用户注册（支持手机号/邮箱）
- ✅ 用户登录（登录失败锁定机制）
- ✅ JWT令牌认证
- ✅ 店员管理（添加/移除/权限设置）
- ✅ 权限分组与验证

### Sprint 2: 订单管理模块
- ✅ 快速记录订单（金额、订单类型、标签等）
- ✅ 查看订单列表（支持按日期、类型、标签筛选，分页加载）
- ✅ 编辑订单（修改订单信息）
- ✅ 删除订单（软删除，进入回收站）
- ✅ 订单回收站（支持恢复已删除订单）
- ✅ 订单分类管理（自定义订单分类）
- ✅ 订单标签管理（自定义订单标签）

### Sprint 3: 收支记录模块
- ✅ 收入记录（金额、收入类型、分类、凭证）
- ✅ 支出记录（金额、支出类型、分类、凭证）
- ✅ 收支分类管理（自定义收支分类）
- ✅ 凭证上传（图片上传，支持预览）
- ✅ 收支列表查看（按日期、类型、分类筛选）
- ✅ 收支汇总统计（总收入、总支出、净利润）

### Sprint 4: 报表功能模块
- ✅ 今日报表（今日订单、收入、支出、利润）
- ✅ 本周报表（本周订单、收入、支出、利润、每日趋势）
- ✅ 本月报表（本月订单、收入、支出、利润、每周趋势）
- ✅ 自定义报表（自定义日期范围、类型筛选、分类筛选）
- ✅ 报表导出（导出Excel格式）
- ✅ 分类分析（按订单类型、收支类型分析）

### Sprint 5: 库存管理模块
- ✅ 食材管理（添加/编辑/删除食材）
- ✅ 库存记录（入库/出库记录）
- ✅ 库存预警（库存低于阈值时预警）
- ✅ 库存统计（食材总数、预警数量统计）

## API接口

### 认证接口
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/v1/auth/register | 用户注册 |
| POST | /api/v1/auth/login | 用户登录 |
| POST | /api/v1/auth/logout | 用户登出 |
| POST | /api/v1/auth/refresh | 刷新令牌 |
| GET | /api/v1/auth/users/me | 获取当前用户信息 |

### 店员管理接口
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/v1/auth/staff | 添加店员 |
| GET | /api/v1/auth/staff | 获取店员列表 |
| GET | /api/v1/auth/staff/{id} | 获取店员详情 |
| PUT | /api/v1/auth/staff/{id}/permissions | 更新店员权限 |
| DELETE | /api/v1/auth/staff/{id} | 移除店员 |

### 权限接口
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/permission/groups | 获取权限分组 |
| GET | /api/v1/permission/me | 获取当前用户权限 |
| GET | /api/v1/permission/check | 检查权限 |

### 订单接口
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/v1/orders | 创建订单 |
| GET | /api/v1/orders | 获取订单列表（支持筛选分页） |
| GET | /api/v1/orders/{id} | 获取订单详情 |
| PUT | /api/v1/orders/{id} | 更新订单 |
| DELETE | /api/v1/orders/{id} | 删除订单（软删除） |
| GET | /api/v1/orders/recycle | 获取回收站订单 |
| POST | /api/v1/orders/{id}/restore | 恢复订单 |
| GET | /api/v1/orders/types | 获取订单类型列表 |
| GET | /api/v1/orders/tags | 获取订单标签列表 |

### 订单分类接口
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/v1/orders/categories | 创建订单分类 |
| GET | /api/v1/orders/categories | 获取订单分类列表 |
| GET | /api/v1/orders/categories/{id} | 获取订单分类详情 |
| PUT | /api/v1/orders/categories/{id} | 更新订单分类 |
| DELETE | /api/v1/orders/categories/{id} | 删除订单分类 |

### 收支记录接口
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/v1/transactions | 创建收支记录 |
| GET | /api/v1/transactions | 获取收支记录列表（支持筛选分页） |
| GET | /api/v1/transactions/{id} | 获取收支记录详情 |
| PUT | /api/v1/transactions/{id} | 更新收支记录 |
| DELETE | /api/v1/transactions/{id} | 删除收支记录 |
| GET | /api/v1/transactions/summary | 获取收支汇总统计 |
| GET | /api/v1/transactions/categories | 获取收支分类名称列表 |
| POST | /api/v1/transactions/batch | 批量创建收支记录 |

### 收支分类接口
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/v1/transactions/categories | 创建收支分类 |
| GET | /api/v1/transactions/categories | 获取收支分类列表 |
| GET | /api/v1/transactions/categories/{id} | 获取收支分类详情 |
| PUT | /api/v1/transactions/categories/{id} | 更新收支分类 |
| DELETE | /api/v1/transactions/categories/{id} | 删除收支分类 |

### 文件上传接口
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/v1/upload/attachment | 上传凭证图片 |

### 报表接口
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/reports/daily | 获取每日报表 |
| GET | /api/v1/reports/weekly | 获取每周报表 |
| GET | /api/v1/reports/monthly | 获取每月报表 |
| POST | /api/v1/reports/custom | 获取自定义报表 |
| GET | /api/v1/reports/category-analysis | 获取分类分析 |
| POST | /api/v1/reports/export/excel | 导出报表为Excel |
| POST | /api/v1/reports/export/pdf | 导出报表为PDF |

### 库存管理接口
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/v1/stock/ingredients | 创建食材 |
| GET | /api/v1/stock/ingredients | 获取食材列表 |
| GET | /api/v1/stock/ingredients/{id} | 获取食材详情 |
| PUT | /api/v1/stock/ingredients/{id} | 更新食材 |
| DELETE | /api/v1/stock/ingredients/{id} | 删除食材 |
| POST | /api/v1/stock/records/in | 记录库存入库 |
| POST | /api/v1/stock/records/out | 记录库存出库 |
| GET | /api/v1/stock/records | 获取库存记录列表 |
| GET | /api/v1/stock/warnings | 获取库存预警列表 |
| GET | /api/v1/stock/summary | 获取库存统计 |

## 开发规范

详见 [.trae/rules/project_rules.md](.trae/rules/project_rules.md)

## 文档

详细文档请查看 `documents/` 目录：
- 产品需求文档：`documents/prd/`
- 技术设计文档：`documents/architecture/`
- 设计文档：`documents/design/`
- 开发计划：`documents/plan/`

## 许可证

MIT License
