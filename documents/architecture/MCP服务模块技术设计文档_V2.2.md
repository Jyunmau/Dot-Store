# MCP服务模块技术设计文档

## 1. 模块概述

MCP服务模块是 Dot-Store V2.2 系统新增的核心模块，负责提供 AI Agent 接入能力。该模块基于 Model Context Protocol (MCP) 协议实现，允许 AI 助手（如 Claude、ChatGPT 等）通过标准化接口访问和操作店铺数据。

### 1.1 功能范围

- MCP协议服务端实现
- AI Agent 身份认证与授权
- 工具（Tool）注册与调用
- 资源（Resource）访问控制
- 提示词（Prompt）模板管理
- 会话管理与上下文保持
- 操作日志与审计

### 1.2 技术栈

- 后端：FastAPI + PostgreSQL + SQLAlchemy
- 协议：MCP (Model Context Protocol) - JSON-RPC 2.0
- 认证：API Key + JWT
- 缓存：Redis（会话状态缓存）

### 1.3 MCP协议概述

MCP (Model Context Protocol) 是一个开放协议，用于 AI 助手与外部工具之间的标准化通信。

```
┌─────────────────┐     MCP Protocol      ┌─────────────────┐
│   AI Agent      │ ◄──────────────────► │   MCP Server    │
│  (Claude/GPT)   │    JSON-RPC 2.0       │  (Dot-Store)    │
└─────────────────┘                       └─────────────────┘
```

### 1.4 V2.2版本新增功能

| 功能 | 说明 |
|------|------|
| MCP服务端 | 完整实现MCP协议服务端 |
| 工具调用 | 提供店铺数据查询和操作工具 |
| 资源访问 | 提供店铺数据资源访问 |
| 权限控制 | 基于API密钥的细粒度权限控制 |
| 操作审计 | 所有AI操作记录到事件日志 |

## 2. 对象设计

### 2.1 后端对象设计

#### 2.1.1 MCP工具定义

```python
# MCP工具定义
MCP_TOOLS = {
    # 订单相关工具
    'get_today_orders': {
        'name': 'get_today_orders',
        'description': '获取今日订单列表',
        'inputSchema': {
            'type': 'object',
            'properties': {},
            'required': []
        },
        'permission': 'order:read'
    },
    'create_order': {
        'name': 'create_order',
        'description': '创建新订单',
        'inputSchema': {
            'type': 'object',
            'properties': {
                'amount': {'type': 'number', 'description': '订单金额'},
                'order_type': {'type': 'string', 'description': '订单类型'},
                'note': {'type': 'string', 'description': '备注'}
            },
            'required': ['amount', 'order_type']
        },
        'permission': 'order:create'
    },
    
    # 库存相关工具
    'get_stock_status': {
        'name': 'get_stock_status',
        'description': '获取库存状态',
        'inputSchema': {
            'type': 'object',
            'properties': {
                'ingredient_name': {'type': 'string', 'description': '食材名称（可选）'}
            },
            'required': []
        },
        'permission': 'stock:read'
    },
    'get_stock_warnings': {
        'name': 'get_stock_warnings',
        'description': '获取库存预警列表',
        'inputSchema': {
            'type': 'object',
            'properties': {},
            'required': []
        },
        'permission': 'stock:read'
    },
    
    # 客户账户相关工具
    'get_customer_balance': {
        'name': 'get_customer_balance',
        'description': '查询客户账户余额',
        'inputSchema': {
            'type': 'object',
            'properties': {
                'phone': {'type': 'string', 'description': '客户手机号'}
            },
            'required': ['phone']
        },
        'permission': 'customer:read'
    },
    'customer_recharge': {
        'name': 'customer_recharge',
        'description': '客户充值',
        'inputSchema': {
            'type': 'object',
            'properties': {
                'phone': {'type': 'string', 'description': '客户手机号'},
                'amount': {'type': 'number', 'description': '充值金额'},
                'note': {'type': 'string', 'description': '备注'}
            },
            'required': ['phone', 'amount']
        },
        'permission': 'customer:recharge'
    },
    
    # 财务相关工具
    'get_today_summary': {
        'name': 'get_today_summary',
        'description': '获取今日经营概况',
        'inputSchema': {
            'type': 'object',
            'properties': {},
            'required': []
        },
        'permission': 'finance:read'
    },
    'get_cash_flow': {
        'name': 'get_cash_flow',
        'description': '获取现金流数据',
        'inputSchema': {
            'type': 'object',
            'properties': {
                'days': {'type': 'integer', 'description': '查询天数'}
            },
            'required': []
        },
        'permission': 'finance:read'
    },
    
    # 现金账户相关工具
    'get_cash_balance': {
        'name': 'get_cash_balance',
        'description': '获取现金账户余额',
        'inputSchema': {
            'type': 'object',
            'properties': {},
            'required': []
        },
        'permission': 'cash:read'
    },
}
```

#### 2.1.2 MCP资源定义

```python
# MCP资源定义
MCP_RESOURCES = {
    'shop://info': {
        'uri': 'shop://info',
        'name': '店铺信息',
        'description': '当前店铺的基本信息',
        'mimeType': 'application/json',
        'permission': 'mcp:read'
    },
    'shop://orders/today': {
        'uri': 'shop://orders/today',
        'name': '今日订单',
        'description': '今日所有订单数据',
        'mimeType': 'application/json',
        'permission': 'order:read'
    },
    'shop://stock/status': {
        'uri': 'shop://stock/status',
        'name': '库存状态',
        'description': '当前库存状态',
        'mimeType': 'application/json',
        'permission': 'stock:read'
    },
    'shop://finance/summary': {
        'uri': 'shop://finance/summary',
        'name': '财务概况',
        'description': '今日财务概况',
        'mimeType': 'application/json',
        'permission': 'finance:read'
    },
}
```

#### 2.1.3 MCP会话模型 (MCPSession)

| 属性 | 类型 | 描述 | 约束 |
|------|------|------|------|
| `id` | `SERIAL` | 会话唯一标识 | 主键 |
| `user_id` | `INTEGER` | 用户ID | 外键 |
| `session_id` | `String` | 会话ID | 唯一 |
| `api_key_id` | `INTEGER` | API密钥ID | 外键 |
| `client_info` | `JSONB` | 客户端信息 | 可选 |
| `status` | `String` | 会话状态 | 默认active |
| `created_at` | `DateTime` | 创建时间 | 非空 |
| `last_active_at` | `DateTime` | 最后活动时间 | 非空 |
| `expires_at` | `DateTime` | 过期时间 | 非空 |

#### 2.1.4 MCP操作日志模型 (MCPOperationLog)

| 属性 | 类型 | 描述 | 约束 |
|------|------|------|------|
| `id` | `SERIAL` | 日志唯一标识 | 主键 |
| `user_id` | `INTEGER` | 用户ID | 外键 |
| `session_id` | `String` | 会话ID | 非空 |
| `operation_type` | `String` | 操作类型 | 非空 |
| `tool_name` | `String` | 工具名称 | 可选 |
| `resource_uri` | `String` | 资源URI | 可选 |
| `input_params` | `JSONB` | 输入参数 | 可选 |
| `output_result` | `JSONB` | 输出结果 | 可选 |
| `status` | `String` | 执行状态 | 非空 |
| `error_message` | `String` | 错误信息 | 可选 |
| `duration_ms` | `INTEGER` | 执行耗时 | 非空 |
| `created_at` | `DateTime` | 创建时间 | 非空 |

#### 2.1.5 MCP服务 (MCPService)

| 方法 | 参数 | 返回值 | 描述 |
|------|------|--------|------|
| `initialize` | `protocol_version: str, capabilities: dict` | `dict` | 初始化MCP会话 |
| `list_tools` | 无 | `List[Tool]` | 列出可用工具 |
| `call_tool` | `name: str, arguments: dict` | `dict` | 调用工具 |
| `list_resources` | 无 | `List[Resource]` | 列出可用资源 |
| `read_resource` | `uri: str` | `dict` | 读取资源 |
| `list_prompts` | 无 | `List[Prompt]` | 列出可用提示词 |
| `get_prompt` | `name: str, arguments: dict` | `str` | 获取提示词 |
| `validate_permission` | `user: User, permission: str` | `bool` | 验证权限 |

### 2.2 JSON-RPC 2.0 消息格式

#### 2.2.1 请求格式

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "get_today_orders",
    "arguments": {}
  }
}
```

#### 2.2.2 响应格式

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "今日订单共15笔，总金额¥1,250.00"
      }
    ]
  }
}
```

#### 2.2.3 错误响应格式

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32602,
    "message": "Invalid params",
    "data": "缺少必填参数: phone"
  }
}
```

## 3. 数据设计

### 3.1 数据模型

#### 3.1.1 MCP会话表 (`mcp_sessions`)

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| `id` | `SERIAL` | `PRIMARY KEY` | 会话ID |
| `user_id` | `INTEGER` | `NOT NULL, REFERENCES users(id)` | 用户ID |
| `session_id` | `VARCHAR(64)` | `UNIQUE NOT NULL` | 会话标识 |
| `api_key_id` | `INTEGER` | `REFERENCES users(id)` | API密钥关联用户 |
| `client_info` | `JSONB` | | 客户端信息 |
| `status` | `VARCHAR(32)` | `DEFAULT 'active'` | 会话状态 |
| `created_at` | `TIMESTAMP` | `NOT NULL DEFAULT NOW()` | 创建时间 |
| `last_active_at` | `TIMESTAMP` | `NOT NULL DEFAULT NOW()` | 最后活动时间 |
| `expires_at` | `TIMESTAMP` | `NOT NULL` | 过期时间 |

#### 3.1.2 MCP操作日志表 (`mcp_operation_logs`)

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| `id` | `SERIAL` | `PRIMARY KEY` | 日志ID |
| `user_id` | `INTEGER` | `NOT NULL, REFERENCES users(id)` | 用户ID |
| `session_id` | `VARCHAR(64)` | `NOT NULL` | 会话标识 |
| `operation_type` | `VARCHAR(32)` | `NOT NULL` | 操作类型 |
| `tool_name` | `VARCHAR(64)` | | 工具名称 |
| `resource_uri` | `VARCHAR(256)` | | 资源URI |
| `input_params` | `JSONB` | | 输入参数 |
| `output_result` | `JSONB` | | 输出结果 |
| `status` | `VARCHAR(32)` | `NOT NULL` | 执行状态 |
| `error_message` | `TEXT` | | 错误信息 |
| `duration_ms` | `INTEGER` | `NOT NULL` | 执行耗时(ms) |
| `created_at` | `TIMESTAMP` | `NOT NULL DEFAULT NOW()` | 创建时间 |

### 3.2 数据关系

- MCP会话与用户：多对一关系
- MCP操作日志与用户：多对一关系
- MCP操作日志与会话：多对一关系

### 3.3 存储方案

- 使用 PostgreSQL 数据库存储会话和日志数据
- 会话状态使用 Redis 缓存，提高访问速度
- 操作日志按时间分区，便于归档和查询

## 4. 接口设计

### 4.1 MCP协议端点

#### 4.1.1 HTTP端点

| 端点 | 方法 | 描述 |
|------|------|------|
| `/mcp` | `POST` | MCP协议主入口，处理所有JSON-RPC请求 |

#### 4.1.2 支持的MCP方法

| 方法 | 描述 | 权限要求 |
|------|------|----------|
| `initialize` | 初始化会话 | 无 |
| `notifications/initialized` | 确认初始化完成 | 无 |
| `tools/list` | 列出可用工具 | mcp:read |
| `tools/call` | 调用工具 | 根据工具要求 |
| `resources/list` | 列出可用资源 | mcp:read |
| `resources/read` | 读取资源 | 根据资源要求 |
| `prompts/list` | 列出可用提示词 | mcp:read |
| `prompts/get` | 获取提示词 | mcp:read |

### 4.2 认证方式

#### 4.2.1 请求头认证

```
Authorization: Bearer sk_xxxxxxxxxxxxxxxx
```

或

```
X-API-Key: sk_xxxxxxxxxxxxxxxx
```

#### 4.2.2 认证流程

1. 客户端发送请求，携带API密钥
2. 服务端验证API密钥有效性
3. 获取API密钥关联的用户
4. 检查用户权限
5. 执行请求操作

### 4.3 工具调用示例

#### 4.3.1 获取今日订单

请求：
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "get_today_orders",
    "arguments": {}
  }
}
```

响应：
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "今日订单统计：\n- 总订单数：15笔\n- 堂食：8笔，¥680.00\n- 外卖：5笔，¥420.00\n- 自提：2笔，¥150.00\n- 总金额：¥1,250.00"
      }
    ]
  }
}
```

#### 4.3.2 客户充值

请求：
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "customer_recharge",
    "arguments": {
      "phone": "13800138000",
      "amount": 100,
      "note": "AI助手代充值"
    }
  }
}
```

响应：
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "充值成功！\n- 客户：张三\n- 手机号：138****8000\n- 充值金额：¥100.00\n- 当前余额：¥150.00\n- 交易编号：C20260301001"
      }
    ]
  }
}
```

## 5. 详细逻辑设计

### 5.1 MCP会话初始化流程

1. 客户端发送 `initialize` 请求
2. 服务端验证API密钥
3. 创建MCP会话记录
4. 返回服务端能力和协议版本
5. 客户端发送 `notifications/initialized`
6. 会话正式建立

### 5.2 工具调用流程

1. 客户端发送 `tools/call` 请求
2. 服务端验证会话有效性
3. 检查用户是否有工具所需权限
4. 执行工具逻辑
5. 记录操作日志
6. 返回执行结果

### 5.3 权限控制流程

```python
async def check_tool_permission(user: User, tool_name: str) -> bool:
    """
    检查用户是否有工具调用权限
    """
    tool = MCP_TOOLS.get(tool_name)
    if not tool:
        raise ToolNotFoundError(f"Tool {tool_name} not found")
    
    required_permission = tool.get('permission')
    if not required_permission:
        return True
    
    # 检查用户权限
    user_permissions = await permission_service.get_effective_permissions(user)
    return required_permission in user_permissions
```

### 5.4 工具实现示例

```python
async def execute_get_today_orders(user_id: int) -> dict:
    """
    获取今日订单工具实现
    """
    today = datetime.now().date()
    
    # 查询今日订单
    orders = await db.query("""
        SELECT 
            order_type,
            COUNT(*) as count,
            SUM(amount) as total_amount
        FROM orders
        WHERE user_id = $1 
          AND DATE(created_at) = $2
          AND is_deleted = false
        GROUP BY order_type
    """, user_id, today)
    
    # 格式化输出
    result_lines = ["今日订单统计："]
    total_count = 0
    total_amount = Decimal(0)
    
    type_names = {
        'dine_in': '堂食',
        'take_out': '外卖',
        'delivery': '配送'
    }
    
    for order in orders:
        type_name = type_names.get(order['order_type'], order['order_type'])
        result_lines.append(f"- {type_name}：{order['count']}笔，¥{order['total_amount']:.2f}")
        total_count += order['count']
        total_amount += order['total_amount']
    
    result_lines.append(f"- 总订单数：{total_count}笔")
    result_lines.append(f"- 总金额：¥{total_amount:.2f}")
    
    return {
        "content": [
            {
                "type": "text",
                "text": "\n".join(result_lines)
            }
        ]
    }
```

### 5.5 边缘场景处理

| 场景 | 处理方式 |
|------|----------|
| API密钥无效 | 返回 -32600 错误，Invalid request |
| 权限不足 | 返回 -32603 错误，Permission denied |
| 工具不存在 | 返回 -32601 错误，Method not found |
| 参数错误 | 返回 -32602 错误，Invalid params |
| 执行超时 | 返回 -32603 错误，Execution timeout |
| 会话过期 | 返回 -32600 错误，Session expired |

## 6. 前后端对接

### 6.1 AI Agent接入配置

AI Agent（如Claude）需要配置MCP服务器：

```json
{
  "mcpServers": {
    "dot-store": {
      "url": "https://api.dot-store.com/mcp",
      "headers": {
        "Authorization": "Bearer sk_xxxxxxxxxxxxxxxx"
      }
    }
  }
}
```

### 6.2 使用示例

用户可以通过AI助手进行自然语言交互：

```
用户: 帮我查一下今天卖了多少钱？

AI助手调用 get_today_summary 工具后回复：
根据系统数据，今天的经营情况如下：
- 总订单数：15笔
- 总销售额：¥1,250.00
- 现金收入：¥800.00
- 会员消费：¥450.00
- 当前现金余额：¥3,500.00
```

```
用户: 帮张三充值100块，手机号13800138000

AI助手调用 customer_recharge 工具后回复：
已成功为张三充值¥100.00，当前余额为¥150.00，交易编号为C20260301001。
```

## 7. 实现注意事项

### 7.1 后端实现注意事项

- 所有MCP请求必须验证API密钥
- 工具调用前必须检查权限
- 敏感操作需要额外确认（如大额充值）
- 所有操作记录到MCP操作日志
- 同时记录到业务事件日志
- 设置合理的请求超时时间

### 7.2 安全注意事项

- API密钥仅显示一次，后续不可查看
- 敏感数据脱敏处理（如手机号中间四位）
- 大额操作需要二次确认
- 定期审计MCP操作日志
- 异常操作告警

### 7.3 性能注意事项

- 会话状态使用Redis缓存
- 工具执行设置超时限制
- 批量操作限制数量
- 响应数据限制大小

## 8. 测试计划

### 8.1 后端测试

- 单元测试：测试MCP协议解析、工具执行
- 集成测试：测试完整MCP会话流程
- 权限测试：测试权限控制逻辑
- 性能测试：测试并发请求处理

### 8.2 集成测试

- 与Claude AI集成测试
- 与其他AI助手集成测试
- 错误处理测试
- 边缘场景测试

## 9. 部署与集成

### 9.1 部署方案

- MCP服务作为独立服务部署
- 使用HTTPS协议
- 配置API网关限流
- 监控MCP服务状态

### 9.2 集成要点

- 与用户认证模块集成：API密钥验证
- 与权限模块集成：权限检查
- 与各业务模块集成：工具调用
- 与事件日志模块集成：操作记录

## 10. 版本控制

- 文档版本：V2.2
- 对应产品版本：Dot-Store V2.2
- 最后更新时间：2026年2月

---

**文档结束**
