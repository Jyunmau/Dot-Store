"""
Dot-Store V2.2 MCP服务数据模式
"""
from datetime import datetime
from typing import Optional, List, Any, Dict, Union
from pydantic import BaseModel, Field


class JSONRPCRequest(BaseModel):
    """
    JSON-RPC 2.0 请求模式
    """
    jsonrpc: str = Field(default="2.0", description="JSON-RPC版本")
    id: Optional[Union[int, str]] = Field(None, description="请求ID")
    method: str = Field(..., description="方法名")
    params: Optional[Dict[str, Any]] = Field(None, description="参数")


class JSONRPCError(BaseModel):
    """
    JSON-RPC 2.0 错误模式
    """
    code: int = Field(..., description="错误码")
    message: str = Field(..., description="错误消息")
    data: Optional[Any] = Field(None, description="错误详情")


class JSONRPCResponse(BaseModel):
    """
    JSON-RPC 2.0 响应模式
    """
    jsonrpc: str = Field(default="2.0", description="JSON-RPC版本")
    id: Optional[Union[int, str]] = Field(None, description="请求ID")
    result: Optional[Any] = Field(None, description="结果")
    error: Optional[JSONRPCError] = Field(None, description="错误")


class MCPToolInputSchema(BaseModel):
    """
    MCP工具输入模式
    """
    type: str = Field(default="object", description="类型")
    properties: Dict[str, Any] = Field(default_factory=dict, description="属性定义")
    required: List[str] = Field(default_factory=list, description="必填字段")


class MCPTool(BaseModel):
    """
    MCP工具模式
    """
    name: str = Field(..., description="工具名称")
    description: str = Field(..., description="工具描述")
    inputSchema: MCPToolInputSchema = Field(..., description="输入模式")


class MCPResource(BaseModel):
    """
    MCP资源模式
    """
    uri: str = Field(..., description="资源URI")
    name: str = Field(..., description="资源名称")
    description: Optional[str] = Field(None, description="资源描述")
    mimeType: str = Field(default="application/json", description="MIME类型")


class MCPPromptArgument(BaseModel):
    """
    MCP提示词参数模式
    """
    name: str = Field(..., description="参数名")
    description: Optional[str] = Field(None, description="参数描述")
    required: bool = Field(default=False, description="是否必填")


class MCPPrompt(BaseModel):
    """
    MCP提示词模式
    """
    name: str = Field(..., description="提示词名称")
    description: Optional[str] = Field(None, description="提示词描述")
    arguments: List[MCPPromptArgument] = Field(default_factory=list, description="参数列表")


class MCPInitializeParams(BaseModel):
    """
    MCP初始化参数模式
    """
    protocolVersion: str = Field(..., description="协议版本")
    capabilities: Dict[str, Any] = Field(default_factory=dict, description="客户端能力")
    clientInfo: Optional[Dict[str, Any]] = Field(None, description="客户端信息")


class MCPInitializeResult(BaseModel):
    """
    MCP初始化结果模式
    """
    protocolVersion: str = Field(..., description="协议版本")
    capabilities: Dict[str, Any] = Field(default_factory=dict, description="服务端能力")
    serverInfo: Dict[str, Any] = Field(..., description="服务端信息")


class MCPToolCallParams(BaseModel):
    """
    MCP工具调用参数模式
    """
    name: str = Field(..., description="工具名称")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="工具参数")


class MCPResourceReadParams(BaseModel):
    """
    MCP资源读取参数模式
    """
    uri: str = Field(..., description="资源URI")


class MCPPromptGetParams(BaseModel):
    """
    MCP提示词获取参数模式
    """
    name: str = Field(..., description="提示词名称")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="提示词参数")


class MCPContent(BaseModel):
    """
    MCP内容模式
    """
    type: str = Field(..., description="内容类型")
    text: Optional[str] = Field(None, description="文本内容")
    data: Optional[Any] = Field(None, description="数据内容")
    mimeType: Optional[str] = Field(None, description="MIME类型")


class MCPToolResult(BaseModel):
    """
    MCP工具调用结果模式
    """
    content: List[MCPContent] = Field(..., description="内容列表")
    isError: bool = Field(default=False, description="是否错误")


class MCPResourceContent(BaseModel):
    """
    MCP资源内容模式
    """
    uri: str = Field(..., description="资源URI")
    mimeType: Optional[str] = Field(None, description="MIME类型")
    text: Optional[str] = Field(None, description="文本内容")
    blob: Optional[str] = Field(None, description="二进制内容(Base64)")


class MCPSessionResponse(BaseModel):
    """
    MCP会话响应模式
    """
    id: int
    user_id: int
    session_id: str
    status: str
    created_at: datetime
    last_active_at: datetime
    expires_at: datetime

    class Config:
        from_attributes = True


class MCPOperationLogResponse(BaseModel):
    """
    MCP操作日志响应模式
    """
    id: int
    user_id: int
    session_id: str
    operation_type: str
    tool_name: Optional[str] = None
    resource_uri: Optional[str] = None
    status: str
    duration_ms: int
    created_at: datetime

    class Config:
        from_attributes = True
