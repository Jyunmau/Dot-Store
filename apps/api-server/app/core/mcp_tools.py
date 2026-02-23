"""
Dot-Store V2.2 MCP工具定义
"""
from typing import Dict, Any, List
from app.schemas.mcp import MCPTool, MCPToolInputSchema, MCPResource


MCP_TOOLS: Dict[str, Dict[str, Any]] = {
    "get_today_orders": {
        "name": "get_today_orders",
        "description": "获取今日订单列表，包含订单数量、金额等统计信息",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        },
        "permission": "order:read"
    },
    "create_order": {
        "name": "create_order",
        "description": "创建新订单，支持指定订单类型、金额等信息",
        "inputSchema": {
            "type": "object",
            "properties": {
                "amount": {"type": "number", "description": "订单金额"},
                "order_type": {"type": "string", "description": "订单类型：dine_in(堂食)/take_out(外卖)/delivery(配送)"},
                "note": {"type": "string", "description": "订单备注"}
            },
            "required": ["amount", "order_type"]
        },
        "permission": "order:create"
    },
    "get_stock_status": {
        "name": "get_stock_status",
        "description": "获取库存状态，可查询指定食材或全部食材的库存情况",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ingredient_name": {"type": "string", "description": "食材名称（可选，不填则返回全部）"}
            },
            "required": []
        },
        "permission": "stock:read"
    },
    "get_stock_warnings": {
        "name": "get_stock_warnings",
        "description": "获取库存预警列表，返回低于最低库存的食材",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        },
        "permission": "stock:read"
    },
    "get_customer_balance": {
        "name": "get_customer_balance",
        "description": "查询客户账户余额，通过手机号查询",
        "inputSchema": {
            "type": "object",
            "properties": {
                "phone": {"type": "string", "description": "客户手机号"}
            },
            "required": ["phone"]
        },
        "permission": "customer:read"
    },
    "customer_recharge": {
        "name": "customer_recharge",
        "description": "为客户账户充值，需要提供手机号和充值金额",
        "inputSchema": {
            "type": "object",
            "properties": {
                "phone": {"type": "string", "description": "客户手机号"},
                "amount": {"type": "number", "description": "充值金额"},
                "note": {"type": "string", "description": "充值备注"}
            },
            "required": ["phone", "amount"]
        },
        "permission": "customer:recharge"
    },
    "get_today_summary": {
        "name": "get_today_summary",
        "description": "获取今日经营概况，包含订单数、销售额、现金收入等",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        },
        "permission": "finance:read"
    },
    "get_cash_flow": {
        "name": "get_cash_flow",
        "description": "获取现金流数据，可指定查询天数",
        "inputSchema": {
            "type": "object",
            "properties": {
                "days": {"type": "integer", "description": "查询天数，默认7天"}
            },
            "required": []
        },
        "permission": "finance:read"
    },
    "get_cash_balance": {
        "name": "get_cash_balance",
        "description": "获取现金账户余额",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        },
        "permission": "cash:read"
    },
    "get_risk_alerts": {
        "name": "get_risk_alerts",
        "description": "获取现金流风险预警信息",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        },
        "permission": "finance:read"
    }
}


MCP_RESOURCES: Dict[str, Dict[str, Any]] = {
    "shop://info": {
        "uri": "shop://info",
        "name": "店铺信息",
        "description": "当前店铺的基本信息",
        "mimeType": "application/json",
        "permission": "mcp:read"
    },
    "shop://orders/today": {
        "uri": "shop://orders/today",
        "name": "今日订单",
        "description": "今日所有订单数据",
        "mimeType": "application/json",
        "permission": "order:read"
    },
    "shop://stock/status": {
        "uri": "shop://stock/status",
        "name": "库存状态",
        "description": "当前库存状态",
        "mimeType": "application/json",
        "permission": "stock:read"
    },
    "shop://finance/summary": {
        "uri": "shop://finance/summary",
        "name": "财务概况",
        "description": "今日财务概况",
        "mimeType": "application/json",
        "permission": "finance:read"
    }
}


MCP_PROMPTS: Dict[str, Dict[str, Any]] = {
    "shop_assistant": {
        "name": "shop_assistant",
        "description": "店铺经营助手提示词，帮助AI更好地理解店铺运营场景",
        "arguments": []
    },
    "daily_report": {
        "name": "daily_report",
        "description": "生成每日经营报告的提示词",
        "arguments": [
            {
                "name": "date",
                "description": "报告日期，格式YYYY-MM-DD",
                "required": False
            }
        ]
    }
}


def get_tool_list() -> List[MCPTool]:
    """
    获取工具列表
    """
    tools = []
    for tool_name, tool_def in MCP_TOOLS.items():
        tools.append(MCPTool(
            name=tool_def["name"],
            description=tool_def["description"],
            inputSchema=MCPToolInputSchema(**tool_def["inputSchema"])
        ))
    return tools


def get_resource_list() -> List[MCPResource]:
    """
    获取资源列表
    """
    resources = []
    for resource_uri, resource_def in MCP_RESOURCES.items():
        resources.append(MCPResource(
            uri=resource_def["uri"],
            name=resource_def["name"],
            description=resource_def.get("description"),
            mimeType=resource_def.get("mimeType", "application/json")
        ))
    return resources


def get_tool_permission(tool_name: str) -> str:
    """
    获取工具所需权限
    """
    tool = MCP_TOOLS.get(tool_name)
    if tool:
        return tool.get("permission", "")
    return ""


def get_resource_permission(resource_uri: str) -> str:
    """
    获取资源所需权限
    """
    resource = MCP_RESOURCES.get(resource_uri)
    if resource:
        return resource.get("permission", "")
    return ""


def tool_exists(tool_name: str) -> bool:
    """
    检查工具是否存在
    """
    return tool_name in MCP_TOOLS


def resource_exists(resource_uri: str) -> bool:
    """
    检查资源是否存在
    """
    return resource_uri in MCP_RESOURCES
