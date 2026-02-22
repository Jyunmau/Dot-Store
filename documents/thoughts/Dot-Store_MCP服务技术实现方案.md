# Dot-Store MCP服务技术实现方案

## 一、技术可行性分析

### 1.1 现有技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | FastAPI |
| 数据库 | PostgreSQL |
| ORM | SQLAlchemy |
| 服务架构 | 分层设计(Service Layer) V2.1 |

### 1.2 可行性评估

| 维度 | 评估 | 说明 |
|------|------|------|
| 协议兼容 | ✅ 高 | MCP基于JSON-RPC 2.0，FastAPI可轻松实现 |
| 代码复用 | ✅ 高 | 现有`OrderService`、`MemberService`、`PointsService`可直接复用 |
| 认证集成 | ✅ 中等 | 需扩展MCP认证机制，可复用现有JWT方案 |
| 数据安全 | ✅ 高 | 现有user_id隔离机制可直接移植 |
| 维护成本 | ✅ 低 | 单一代码库，统一管理 |

---

## 二、实施方案

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                    AI Agent / Client                    │
│              (Cherry Studio / Claude Desktop)          │
└─────────────────────┬───────────────────────────────────┘
                      │ MCP Protocol (JSON-RPC 2.0)
                      │ stdio / HTTP + SSE
┌─────────────────────▼───────────────────────────────────┐
│                   MCP Server (FastAPI)                 │
│  ┌─────────────────────────────────────────────────────┐│
│  │              MCP Protocol Handler                  ││
│  │  - tools/list                                       ││
│  │  - tools/call                                       ││
│  │  - resources/list                                   ││
│  └─────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────┐│
│  │              Business Logic Layer                   ││
│  │  - OrderService      (现有)                         ││
│  │  - MemberService    (现有)                         ││
│  │  - PointsService    (现有)                         ││
│  └─────────────────────────────────────────────────────┘│
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│                   Database (PostgreSQL)                │
└─────────────────────────────────────────────────────────┘
```

### 2.2 部署模式

| 模式 | 适用场景 | 优点 | 缺点 |
|------|----------|------|------|
| stdio模式 | 本地AI工具连接 | 简单，无需网络 | 需要本地运行 |
| HTTP + SSE | 远程AI服务 | 可远程访问 | 需要认证 |
| **推荐** | HTTP + SSE | 兼容Cherry Studio | 需要简单认证 |

---

## 三、MCP工具设计

### 3.1 订单管理工具

| 工具名 | 功能 | 必填参数 |
|--------|------|----------|
| `create_order` | 创建订单 | user_id, amount, order_type |
| `list_orders` | 查询订单列表 | user_id |
| `get_order` | 获取订单详情 | user_id, order_id |
| `update_order` | 更新订单 | user_id, order_id |
| `delete_order` | 删除订单(软删除) | user_id, order_id |
| `restore_order` | 恢复订单 | user_id, order_id |

### 3.2 会员管理工具

| 工具名 | 功能 | 必填参数 |
|--------|------|----------|
| `create_member` | 创建会员 | user_id, name, phone |
| `list_members` | 查询会员列表 | user_id |
| `get_member` | 获取会员详情 | user_id, member_id |
| `update_member` | 更新会员 | user_id, member_id |
| `delete_member` | 删除会员 | user_id, member_id |

### 3.3 积分管理工具

| 工具名 | 功能 | 必填参数 |
|--------|------|----------|
| `add_points` | 增加积分 | user_id, member_id, points |
| `subtract_points` | 扣减积分 | user_id, member_id, points |
| `get_points_records` | 查询积分记录 | user_id |
| `exchange_points` | 积分兑换 | user_id, member_id, points |
| `get_exchanges` | 查询兑换记录 | user_id |

---

## 四、认证方案

### 4.1 API Key模式（推荐）

```python
# 客户端传入api_key，MCP请求头中携带 X-API-Key
# 后端验证后转换为user_id
```

---

## 五、目录结构

```
apps/api-server/
├── app/
│   ├── mcp/
│   │   ├── __init__.py
│   │   ├── server.py          # MCP服务器主入口
│   │   ├── protocol.py        # MCP协议处理
│   │   ├── tools/             # 工具定义
│   │   │   ├── __init__.py
│   │   │   ├── order_tools.py
│   │   │   ├── member_tools.py
│   │   │   └── points_tools.py
│   │   └── auth.py            # MCP认证
│   └── main.py                # 扩展以支持MCP端点
```

---

## 六、实施计划

| 阶段 | 任务 | 预估工作量 |
|------|------|-----------|
| Phase 1 | MCP基础框架搭建 | 1-2天 |
| Phase 2 | 工具定义与注册 | 1天 |
| Phase 3 | 认证集成 | 0.5天 |
| Phase 4 | 订单模块对接 | 1天 |
| Phase 5 | 会员模块对接 | 1天 |
| Phase 6 | 积分模块对接 | 1天 |
| Phase 7 | 测试与调试 | 1天 |

**总计：约7-8个工作日**

---

## 七、风险与应对

| 风险 | 影响 | 应对措施 |
|------|------|----------|
| MCP协议理解偏差 | 中 | 参考官方SDK实现 |
| 大数据量查询 | 低 | 添加分页和限制 |
| 并发安全 | 低 | 复用现有事务机制 |
| 认证安全 | 中 | 使用API Key + HTTPS |

---

## 八、结论

技术方案可行。现有代码架构清晰，服务层可直接复用；FastAPI天然支持JSON-RPC，易于实现MCP协议；推荐采用HTTP + SSE模式，兼容主流AI工具；实施难度中等，预计7-8天可完成基础功能。
