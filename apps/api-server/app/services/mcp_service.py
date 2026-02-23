"""
Dot-Store V2.2 MCP服务实现
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import secrets
import json
import time
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ..models.mcp import MCPSession, MCPOperationLog
from ..models.user import User
from ..models.order import Order
from ..models.stock import Ingredient
from ..models.customer_account import CustomerAccount, CustomerTransaction
from ..models.cash_account import CashAccount, CashTransaction
from ..models.cash_flow import CashFlowAnalysis
from ..schemas.mcp import (
    MCPToolResult,
    MCPContent,
    MCPInitializeResult,
    MCPTool,
    MCPResource,
    MCPResourceContent,
)
from ..core.mcp_tools import (
    MCP_TOOLS,
    MCP_RESOURCES,
    get_tool_list,
    get_resource_list,
    get_tool_permission,
    get_resource_permission,
    tool_exists,
    resource_exists,
)
from ..services.event_service import EventService


class MCPService:
    """
    MCP服务类
    """

    SERVER_INFO = {
        "name": "Dot-Store MCP Server",
        "version": "2.2.0"
    }

    SERVER_CAPABILITIES = {
        "tools": {},
        "resources": {},
        "prompts": {}
    }

    def __init__(self, db: Session):
        self.db = db

    def initialize(self, user: User, client_info: Optional[Dict] = None) -> MCPInitializeResult:
        """
        初始化MCP会话
        """
        session_id = f"mcp_{secrets.token_hex(16)}"
        expires_at = datetime.utcnow() + timedelta(hours=24)

        session = MCPSession(
            user_id=user.id,
            session_id=session_id,
            api_key_id=user.id,
            client_info=client_info,
            status="active",
            expires_at=expires_at
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        return MCPInitializeResult(
            protocolVersion="2024-11-05",
            capabilities=self.SERVER_CAPABILITIES,
            serverInfo=self.SERVER_INFO
        )

    def get_session(self, session_id: str) -> Optional[MCPSession]:
        """
        获取会话
        """
        return self.db.query(MCPSession).filter(
            MCPSession.session_id == session_id,
            MCPSession.status == "active"
        ).first()

    def update_session_activity(self, session: MCPSession):
        """
        更新会话活动时间
        """
        session.last_active_at = datetime.utcnow()
        self.db.commit()

    def log_operation(
        self,
        user_id: int,
        session_id: str,
        operation_type: str,
        status: str,
        tool_name: Optional[str] = None,
        resource_uri: Optional[str] = None,
        input_params: Optional[Dict] = None,
        output_result: Optional[Dict] = None,
        error_message: Optional[str] = None,
        duration_ms: int = 0
    ):
        """
        记录操作日志
        """
        log = MCPOperationLog(
            user_id=user_id,
            session_id=session_id,
            operation_type=operation_type,
            tool_name=tool_name,
            resource_uri=resource_uri,
            input_params=input_params,
            output_result=output_result,
            status=status,
            error_message=error_message,
            duration_ms=duration_ms
        )
        self.db.add(log)
        self.db.commit()

    def list_tools(self) -> List[MCPTool]:
        """
        列出可用工具
        """
        return get_tool_list()

    def list_resources(self) -> List[MCPResource]:
        """
        列出可用资源
        """
        return get_resource_list()

    def call_tool(self, user: User, tool_name: str, arguments: Dict[str, Any]) -> MCPToolResult:
        """
        调用工具
        """
        start_time = time.time()

        if not tool_exists(tool_name):
            return MCPToolResult(
                content=[MCPContent(type="text", text=f"工具 '{tool_name}' 不存在")],
                isError=True
            )

        try:
            result_text = self._execute_tool(user, tool_name, arguments)
            duration_ms = int((time.time() - start_time) * 1000)

            self.log_operation(
                user_id=user.id,
                session_id="",
                operation_type="tools/call",
                tool_name=tool_name,
                input_params=arguments,
                output_result={"text": result_text},
                status="success",
                duration_ms=duration_ms
            )

            EventService.log(
                db=self.db,
                user_id=user.id,
                event_type="mcp_tool_call",
                operator_id=user.id,
                entity_type="mcp_tool",
                entity_id=0,
                data={
                    "tool_name": tool_name,
                    "arguments": arguments,
                    "result": "success"
                }
            )

            return MCPToolResult(
                content=[MCPContent(type="text", text=result_text)],
                isError=False
            )

        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            error_msg = str(e)

            self.log_operation(
                user_id=user.id,
                session_id="",
                operation_type="tools/call",
                tool_name=tool_name,
                input_params=arguments,
                status="error",
                error_message=error_msg,
                duration_ms=duration_ms
            )

            return MCPToolResult(
                content=[MCPContent(type="text", text=f"执行错误: {error_msg}")],
                isError=True
            )

    def read_resource(self, user: User, uri: str) -> MCPResourceContent:
        """
        读取资源
        """
        start_time = time.time()

        if not resource_exists(uri):
            return MCPResourceContent(
                uri=uri,
                text=f"资源 '{uri}' 不存在"
            )

        try:
            result = self._read_resource(user, uri)
            duration_ms = int((time.time() - start_time) * 1000)

            self.log_operation(
                user_id=user.id,
                session_id="",
                operation_type="resources/read",
                resource_uri=uri,
                output_result=result,
                status="success",
                duration_ms=duration_ms
            )

            return MCPResourceContent(
                uri=uri,
                mimeType="application/json",
                text=json.dumps(result, ensure_ascii=False, default=str)
            )

        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            error_msg = str(e)

            self.log_operation(
                user_id=user.id,
                session_id="",
                operation_type="resources/read",
                resource_uri=uri,
                status="error",
                error_message=error_msg,
                duration_ms=duration_ms
            )

            return MCPResourceContent(
                uri=uri,
                text=f"读取错误: {error_msg}"
            )

    def _execute_tool(self, user: User, tool_name: str, arguments: Dict[str, Any]) -> str:
        """
        执行工具逻辑
        """
        if tool_name == "get_today_orders":
            return self._get_today_orders(user.id)
        elif tool_name == "create_order":
            return self._create_order(user.id, arguments)
        elif tool_name == "get_stock_status":
            return self._get_stock_status(user.id, arguments.get("ingredient_name"))
        elif tool_name == "get_stock_warnings":
            return self._get_stock_warnings(user.id)
        elif tool_name == "get_customer_balance":
            return self._get_customer_balance(user.id, arguments.get("phone"))
        elif tool_name == "customer_recharge":
            return self._customer_recharge(user.id, arguments)
        elif tool_name == "get_today_summary":
            return self._get_today_summary(user.id)
        elif tool_name == "get_cash_flow":
            return self._get_cash_flow(user.id, arguments.get("days", 7))
        elif tool_name == "get_cash_balance":
            return self._get_cash_balance(user.id)
        elif tool_name == "get_risk_alerts":
            return self._get_risk_alerts(user.id)
        else:
            return f"工具 '{tool_name}' 未实现"

    def _read_resource(self, user: User, uri: str) -> Dict[str, Any]:
        """
        读取资源数据
        """
        if uri == "shop://info":
            return self._get_shop_info(user)
        elif uri == "shop://orders/today":
            return self._get_today_orders_data(user.id)
        elif uri == "shop://stock/status":
            return self._get_stock_status_data(user.id)
        elif uri == "shop://finance/summary":
            return self._get_finance_summary_data(user.id)
        else:
            return {"error": f"资源 '{uri}' 未实现"}

    def _get_today_orders(self, user_id: int) -> str:
        """
        获取今日订单统计
        """
        today = datetime.now().date()
        orders = self.db.query(Order).filter(
            Order.user_id == user_id,
            Order.is_deleted == False
        ).all()

        today_orders = [o for o in orders if o.created_at.date() == today]

        if not today_orders:
            return "今日暂无订单"

        type_stats = {}
        total_count = 0
        total_amount = 0

        type_names = {
            "dine_in": "堂食",
            "take_out": "外卖",
            "delivery": "配送"
        }

        for order in today_orders:
            order_type = order.order_type or "dine_in"
            if order_type not in type_stats:
                type_stats[order_type] = {"count": 0, "amount": 0}
            type_stats[order_type]["count"] += 1
            type_stats[order_type]["amount"] += float(order.amount or 0)
            total_count += 1
            total_amount += float(order.amount or 0)

        lines = ["今日订单统计："]
        for order_type, stats in type_stats.items():
            type_name = type_names.get(order_type, order_type)
            lines.append(f"- {type_name}：{stats['count']}笔，¥{stats['amount']:.2f}")
        lines.append(f"- 总订单数：{total_count}笔")
        lines.append(f"- 总金额：¥{total_amount:.2f}")

        return "\n".join(lines)

    def _create_order(self, user_id: int, arguments: Dict[str, Any]) -> str:
        """
        创建订单
        """
        amount = arguments.get("amount", 0)
        order_type = arguments.get("order_type", "dine_in")
        note = arguments.get("note", "")

        order = Order(
            user_id=user_id,
            order_type=order_type,
            amount=amount,
            note=note,
            status="pending"
        )
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)

        return f"订单创建成功！\n- 订单ID：{order.id}\n- 订单类型：{order_type}\n- 金额：¥{amount:.2f}"

    def _get_stock_status(self, user_id: int, ingredient_name: Optional[str] = None) -> str:
        """
        获取库存状态
        """
        query = self.db.query(Ingredient).filter(
            Ingredient.user_id == user_id,
            Ingredient.status == "active"
        )

        if ingredient_name:
            query = query.filter(Ingredient.name.ilike(f"%{ingredient_name}%"))

        ingredients = query.all()

        if not ingredients:
            return "暂无库存数据"

        lines = ["库存状态："]
        for ing in ingredients:
            status_icon = "⚠️" if ing.quantity <= (ing.min_quantity or 0) else "✅"
            lines.append(f"- {status_icon} {ing.name}：{ing.quantity} {ing.unit}（成本：¥{ing.cost or 0:.2f}/{ing.unit}）")

        return "\n".join(lines)

    def _get_stock_warnings(self, user_id: int) -> str:
        """
        获取库存预警
        """
        ingredients = self.db.query(Ingredient).filter(
            Ingredient.user_id == user_id,
            Ingredient.status == "active",
            Ingredient.quantity <= Ingredient.min_quantity
        ).all()

        if not ingredients:
            return "✅ 暂无库存预警"

        lines = ["⚠️ 库存预警列表："]
        for ing in ingredients:
            lines.append(f"- {ing.name}：当前库存 {ing.quantity} {ing.unit}，最低库存 {ing.min_quantity} {ing.unit}")

        return "\n".join(lines)

    def _get_customer_balance(self, user_id: int, phone: Optional[str] = None) -> str:
        """
        查询客户余额
        """
        if not phone:
            return "请提供客户手机号"

        account = self.db.query(CustomerAccount).filter(
            CustomerAccount.user_id == user_id,
            CustomerAccount.phone == phone
        ).first()

        if not account:
            return f"未找到手机号为 {phone} 的客户"

        masked_phone = phone[:3] + "****" + phone[-4:] if len(phone) >= 7 else phone

        return f"客户账户信息：\n- 姓名：{account.name}\n- 手机号：{masked_phone}\n- 当前余额：¥{account.balance:.2f}"

    def _customer_recharge(self, user_id: int, arguments: Dict[str, Any]) -> str:
        """
        客户充值
        """
        phone = arguments.get("phone")
        amount = arguments.get("amount", 0)
        note = arguments.get("note", "AI助手代充值")

        if not phone:
            return "请提供客户手机号"

        account = self.db.query(CustomerAccount).filter(
            CustomerAccount.user_id == user_id,
            CustomerAccount.phone == phone
        ).first()

        if not account:
            return f"未找到手机号为 {phone} 的客户"

        old_balance = float(account.balance)
        account.balance += amount

        transaction = CustomerTransaction(
            user_id=user_id,
            account_id=account.id,
            transaction_type="recharge",
            amount=amount,
            balance_after=account.balance,
            note=note
        )
        self.db.add(transaction)
        self.db.commit()

        masked_phone = phone[:3] + "****" + phone[-4:] if len(phone) >= 7 else phone

        return f"充值成功！\n- 客户：{account.name}\n- 手机号：{masked_phone}\n- 充值金额：¥{amount:.2f}\n- 当前余额：¥{account.balance:.2f}"

    def _get_today_summary(self, user_id: int) -> str:
        """
        获取今日经营概况
        """
        today = datetime.now().date()

        orders = self.db.query(Order).filter(
            Order.user_id == user_id,
            Order.is_deleted == False
        ).all()

        today_orders = [o for o in orders if o.created_at.date() == today]

        total_orders = len(today_orders)
        total_sales = sum(float(o.amount or 0) for o in today_orders)

        cash_account = self.db.query(CashAccount).filter(
            CashAccount.user_id == user_id
        ).first()

        cash_balance = float(cash_account.balance) if cash_account else 0

        lines = [
            "今日经营概况：",
            f"- 总订单数：{total_orders}笔",
            f"- 总销售额：¥{total_sales:.2f}",
            f"- 当前现金余额：¥{cash_balance:.2f}"
        ]

        return "\n".join(lines)

    def _get_cash_flow(self, user_id: int, days: int = 7) -> str:
        """
        获取现金流数据
        """
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)

        transactions = self.db.query(CashTransaction).filter(
            CashTransaction.user_id == user_id,
            CashTransaction.created_at >= start_date,
            CashTransaction.created_at <= end_date
        ).all()

        income = sum(float(t.amount) for t in transactions if t.transaction_type == "income")
        expense = sum(float(t.amount) for t in transactions if t.transaction_type == "expense")
        net_flow = income - expense

        lines = [
            f"近{days}天现金流数据：",
            f"- 总收入：¥{income:.2f}",
            f"- 总支出：¥{expense:.2f}",
            f"- 净现金流：¥{net_flow:.2f}"
        ]

        return "\n".join(lines)

    def _get_cash_balance(self, user_id: int) -> str:
        """
        获取现金账户余额
        """
        cash_account = self.db.query(CashAccount).filter(
            CashAccount.user_id == user_id
        ).first()

        if not cash_account:
            return "现金账户不存在"

        return f"现金账户余额：¥{cash_account.balance:.2f}"

    def _get_risk_alerts(self, user_id: int) -> str:
        """
        获取风险预警
        """
        analysis = self.db.query(CashFlowAnalysis).filter(
            CashFlowAnalysis.user_id == user_id
        ).order_by(desc(CashFlowAnalysis.created_at)).first()

        if not analysis:
            return "暂无风险分析数据"

        risk_level = analysis.risk_level or "unknown"
        risk_score = analysis.risk_score or 0

        risk_icons = {
            "low": "🟢",
            "medium": "🟡",
            "high": "🟠",
            "critical": "🔴"
        }

        icon = risk_icons.get(risk_level, "⚪")

        lines = [
            f"{icon} 风险等级：{risk_level.upper()}",
            f"- 风险评分：{risk_score}",
        ]

        if analysis.risk_factors:
            lines.append("- 风险因素：")
            for factor in analysis.risk_factors[:3]:
                lines.append(f"  - {factor}")

        return "\n".join(lines)

    def _get_shop_info(self, user: User) -> Dict[str, Any]:
        """
        获取店铺信息
        """
        return {
            "shop_name": user.shop_name,
            "shop_type": user.shop_type,
            "city": user.city,
            "role": user.role
        }

    def _get_today_orders_data(self, user_id: int) -> Dict[str, Any]:
        """
        获取今日订单数据
        """
        today = datetime.now().date()
        orders = self.db.query(Order).filter(
            Order.user_id == user_id,
            Order.is_deleted == False
        ).all()

        today_orders = [o for o in orders if o.created_at.date() == today]

        return {
            "total_count": len(today_orders),
            "total_amount": sum(float(o.amount or 0) for o in today_orders),
            "orders": [
                {
                    "id": o.id,
                    "order_type": o.order_type,
                    "amount": float(o.amount or 0),
                    "status": o.status,
                    "created_at": o.created_at.isoformat()
                }
                for o in today_orders[:10]
            ]
        }

    def _get_stock_status_data(self, user_id: int) -> Dict[str, Any]:
        """
        获取库存状态数据
        """
        ingredients = self.db.query(Ingredient).filter(
            Ingredient.user_id == user_id,
            Ingredient.status == "active"
        ).all()

        warnings = [i for i in ingredients if i.quantity <= (i.min_quantity or 0)]

        return {
            "total_count": len(ingredients),
            "warning_count": len(warnings),
            "ingredients": [
                {
                    "id": i.id,
                    "name": i.name,
                    "quantity": float(i.quantity or 0),
                    "unit": i.unit,
                    "cost": float(i.cost or 0),
                    "is_low": i.quantity <= (i.min_quantity or 0)
                }
                for i in ingredients[:20]
            ]
        }

    def _get_finance_summary_data(self, user_id: int) -> Dict[str, Any]:
        """
        获取财务概况数据
        """
        today = datetime.now().date()

        cash_account = self.db.query(CashAccount).filter(
            CashAccount.user_id == user_id
        ).first()

        orders = self.db.query(Order).filter(
            Order.user_id == user_id,
            Order.is_deleted == False
        ).all()

        today_orders = [o for o in orders if o.created_at.date() == today]

        return {
            "cash_balance": float(cash_account.balance) if cash_account else 0,
            "today_orders": len(today_orders),
            "today_sales": sum(float(o.amount or 0) for o in today_orders)
        }
