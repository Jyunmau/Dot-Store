# script层 - HTTP请求处理

## 1. 概述

script层是Dot-Store系统的HTTP请求处理层，负责接收和处理客户端的HTTP请求，返回相应的响应。它将客户端请求转换为对Platform层服务的调用，并将结果转换为客户端可以理解的格式。

## 2. 核心职责

- HTTP请求处理：接收和处理客户端的HTTP请求
- 请求验证：验证请求参数的合法性
- 响应格式化：将Platform层返回的结果格式化为HTTP响应
- 路由管理：管理API路由
- 中间件：处理认证、授权、日志等横切关注点

## 3. 目录结构

```
script/
├── routes/          # API路由定义
│   ├── __init__.py         # 路由初始化
│   ├── order.py            # 订单路由
│   ├── ledger.py           # 账本路由
│   ├── report.py           # 报表路由
│   ├── config.py           # 配置路由
│   └── resource_event.py   # 资源事件路由
├── middlewares/     # 中间件
├── schemas/         # 请求响应模型
└── utils/           # 工具函数
```

## 4. 设计原则

- 只处理HTTP请求和响应
- 不包含业务逻辑
- 基于Platform层提供的服务构建
- 保持与Platform层的松耦合
- 支持RESTful API设计

## 5. 关键模块说明

### 5.1 API路由

API路由模块负责定义系统的API接口，包括：
- 订单API：处理订单的创建、查询、更新和删除
- 账本API：处理分类账和账务分录的管理
- 报表API：提供各种报表查询功能
- 配置API：处理系统配置的管理
- 资源事件API：处理资源事件的管理

### 5.2 请求响应模型

请求响应模型定义了API接口的请求和响应格式，包括：
- 请求模型：定义API接口的输入参数格式
- 响应模型：定义API接口的输出格式

### 5.3 中间件

中间件模块负责处理横切关注点，包括：
- 认证中间件：处理用户认证
- 授权中间件：处理权限验证
- 日志中间件：记录请求和响应日志
- 错误处理中间件：统一处理错误

## 6. 使用方法

script层通过FastAPI框架提供HTTP服务，客户端可以通过HTTP请求调用系统的API接口。

```bash
# 示例：创建订单
curl -X POST http://localhost:8000/api/orders \
  -H "Content-Type: application/json" \
  -d '{"shop_id": 1, "amount_estimate": 1000, "tags": ["test"]}'

# 示例：获取订单列表
curl http://localhost:8000/api/orders?shop_id=1
```

## 7. 扩展说明

script层的扩展应遵循以下原则：
- 只处理HTTP请求和响应
- 不包含业务逻辑
- 基于Platform层提供的服务构建
- 保持与Platform层的松耦合
- 支持RESTful API设计

## 8. 与Platform层的关系

script层依赖于Platform层提供的业务服务，通过依赖注入的方式使用Platform层的服务。script层将客户端请求转换为对Platform层服务的调用，并将结果转换为HTTP响应返回给客户端。