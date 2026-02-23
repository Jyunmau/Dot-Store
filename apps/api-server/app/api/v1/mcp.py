"""
Dot-Store V2.2 MCP服务API路由
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header, Request
from sqlalchemy.orm import Session
import json

from app.core.database import get_db
from app.models.user import User
from app.services.auth_service import AuthService
from app.services.mcp_service import MCPService
from app.schemas.mcp import (
    JSONRPCRequest,
    JSONRPCResponse,
    JSONRPCError,
)

router = APIRouter(prefix="/mcp", tags=["MCP服务"])


def get_user_by_api_key(
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """
    通过API密钥获取用户
    """
    api_key = None

    if x_api_key:
        api_key = x_api_key
    elif authorization:
        if authorization.startswith("Bearer "):
            api_key = authorization[7:]

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="缺少API密钥"
        )

    auth_service = AuthService(db)
    user = auth_service.verify_api_key(api_key)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API密钥无效或已过期"
        )

    return user


@router.post("", summary="MCP协议入口")
async def mcp_endpoint(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_user_by_api_key)
):
    """
    MCP协议主入口，处理所有JSON-RPC请求
    
    支持的方法：
    - initialize: 初始化会话
    - notifications/initialized: 确认初始化
    - tools/list: 列出可用工具
    - tools/call: 调用工具
    - resources/list: 列出可用资源
    - resources/read: 读取资源
    - prompts/list: 列出可用提示词
    - prompts/get: 获取提示词
    """
    try:
        body = await request.json()
    except Exception:
        return JSONRPCResponse(
            id=None,
            error=JSONRPCError(
                code=-32700,
                message="Parse error",
                data="Invalid JSON"
            )
        ).model_dump()

    jsonrpc = body.get("jsonrpc", "2.0")
    request_id = body.get("id")
    method = body.get("method", "")
    params = body.get("params", {})

    mcp_service = MCPService(db)

    try:
        if method == "initialize":
            client_info = params.get("clientInfo", {})
            result = mcp_service.initialize(user, client_info)
            return JSONRPCResponse(
                id=request_id,
                result=result.model_dump()
            ).model_dump()

        elif method == "notifications/initialized":
            return JSONRPCResponse(
                id=request_id,
                result={}
            ).model_dump()

        elif method == "tools/list":
            tools = mcp_service.list_tools()
            return JSONRPCResponse(
                id=request_id,
                result={"tools": [t.model_dump() for t in tools]}
            ).model_dump()

        elif method == "tools/call":
            tool_name = params.get("name", "")
            arguments = params.get("arguments", {})

            if not tool_name:
                return JSONRPCResponse(
                    id=request_id,
                    error=JSONRPCError(
                        code=-32602,
                        message="Invalid params",
                        data="缺少工具名称"
                    )
                ).model_dump()

            result = mcp_service.call_tool(user, tool_name, arguments)
            return JSONRPCResponse(
                id=request_id,
                result=result.model_dump()
            ).model_dump()

        elif method == "resources/list":
            resources = mcp_service.list_resources()
            return JSONRPCResponse(
                id=request_id,
                result={"resources": [r.model_dump() for r in resources]}
            ).model_dump()

        elif method == "resources/read":
            uri = params.get("uri", "")

            if not uri:
                return JSONRPCResponse(
                    id=request_id,
                    error=JSONRPCError(
                        code=-32602,
                        message="Invalid params",
                        data="缺少资源URI"
                    )
                ).model_dump()

            result = mcp_service.read_resource(user, uri)
            return JSONRPCResponse(
                id=request_id,
                result={"contents": [result.model_dump()]}
            ).model_dump()

        elif method == "prompts/list":
            return JSONRPCResponse(
                id=request_id,
                result={"prompts": []}
            ).model_dump()

        elif method == "prompts/get":
            return JSONRPCResponse(
                id=request_id,
                error=JSONRPCError(
                    code=-32601,
                    message="Method not found",
                    data="暂不支持提示词功能"
                )
            ).model_dump()

        else:
            return JSONRPCResponse(
                id=request_id,
                error=JSONRPCError(
                    code=-32601,
                    message="Method not found",
                    data=f"未知方法: {method}"
                )
            ).model_dump()

    except Exception as e:
        return JSONRPCResponse(
            id=request_id,
            error=JSONRPCError(
                code=-32603,
                message="Internal error",
                data=str(e)
            )
        ).model_dump()


@router.get("/tools", summary="获取工具列表（REST API）")
async def get_tools_list(
    user: User = Depends(get_user_by_api_key),
    db: Session = Depends(get_db)
):
    """
    获取可用工具列表（REST API方式）
    """
    mcp_service = MCPService(db)
    tools = mcp_service.list_tools()
    return {
        "tools": [t.model_dump() for t in tools]
    }


@router.get("/resources", summary="获取资源列表（REST API）")
async def get_resources_list(
    user: User = Depends(get_user_by_api_key),
    db: Session = Depends(get_db)
):
    """
    获取可用资源列表（REST API方式）
    """
    mcp_service = MCPService(db)
    resources = mcp_service.list_resources()
    return {
        "resources": [r.model_dump() for r in resources]
    }
