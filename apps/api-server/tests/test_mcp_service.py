"""
Dot-Store V2.2 MCP服务测试
"""
import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


@pytest.fixture(scope="function")
def db_session():
    """创建测试数据库会话"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def test_user(db_session):
    """创建测试用户"""
    from app.models.user import User
    user = User(
        id=1,
        phone="13800138000",
        password_hash="hashed_password",
        shop_name="测试店铺",
        shop_type="restaurant",
        city="北京",
        role="owner",
        status="active",
        api_key="sk_test_api_key_12345678",
        api_key_created_at=datetime.utcnow(),
        api_key_expires_at=datetime.utcnow() + timedelta(days=30)
    )
    db_session.add(user)
    db_session.commit()
    return user


class TestMCPTools:
    """MCP工具定义测试"""

    def test_tool_list(self):
        """测试获取工具列表"""
        from app.core.mcp_tools import get_tool_list
        
        tools = get_tool_list()
        assert len(tools) > 0
        
        tool_names = [t.name for t in tools]
        assert "get_today_orders" in tool_names
        assert "get_stock_status" in tool_names
        assert "get_customer_balance" in tool_names

    def test_resource_list(self):
        """测试获取资源列表"""
        from app.core.mcp_tools import get_resource_list
        
        resources = get_resource_list()
        assert len(resources) > 0
        
        resource_uris = [r.uri for r in resources]
        assert "shop://info" in resource_uris
        assert "shop://orders/today" in resource_uris

    def test_tool_permission(self):
        """测试获取工具权限"""
        from app.core.mcp_tools import get_tool_permission
        
        permission = get_tool_permission("get_today_orders")
        assert permission == "order:read"
        
        permission = get_tool_permission("create_order")
        assert permission == "order:create"

    def test_tool_exists(self):
        """测试工具是否存在"""
        from app.core.mcp_tools import tool_exists
        
        assert tool_exists("get_today_orders") is True
        assert tool_exists("non_existent_tool") is False

    def test_resource_exists(self):
        """测试资源是否存在"""
        from app.core.mcp_tools import resource_exists
        
        assert resource_exists("shop://info") is True
        assert resource_exists("shop://nonexistent") is False


class TestMCPService:
    """MCP服务测试"""

    def test_initialize(self, db_session, test_user):
        """测试MCP初始化"""
        from app.services.mcp_service import MCPService
        
        mcp_service = MCPService(db_session)
        result = mcp_service.initialize(test_user, {"name": "test_client"})
        
        assert result.protocolVersion == "2024-11-05"
        assert result.serverInfo["name"] == "Dot-Store MCP Server"
        assert "tools" in result.capabilities

    def test_list_tools(self, db_session):
        """测试列出工具"""
        from app.services.mcp_service import MCPService
        
        mcp_service = MCPService(db_session)
        tools = mcp_service.list_tools()
        
        assert len(tools) > 0
        tool_names = [t.name for t in tools]
        assert "get_today_orders" in tool_names

    def test_list_resources(self, db_session):
        """测试列出资源"""
        from app.services.mcp_service import MCPService
        
        mcp_service = MCPService(db_session)
        resources = mcp_service.list_resources()
        
        assert len(resources) > 0
        resource_uris = [r.uri for r in resources]
        assert "shop://info" in resource_uris

    def test_call_tool_get_today_orders(self, db_session, test_user):
        """测试调用获取今日订单工具"""
        from app.services.mcp_service import MCPService
        
        mcp_service = MCPService(db_session)
        result = mcp_service.call_tool(test_user, "get_today_orders", {})
        
        assert result.isError is False
        assert len(result.content) > 0
        assert result.content[0].type == "text"

    def test_call_tool_get_stock_status(self, db_session, test_user):
        """测试调用获取库存状态工具"""
        from app.services.mcp_service import MCPService
        
        mcp_service = MCPService(db_session)
        result = mcp_service.call_tool(test_user, "get_stock_status", {})
        
        assert result.isError is False
        assert len(result.content) > 0

    def test_call_tool_get_cash_balance(self, db_session, test_user):
        """测试调用获取现金余额工具"""
        from app.services.mcp_service import MCPService
        
        mcp_service = MCPService(db_session)
        result = mcp_service.call_tool(test_user, "get_cash_balance", {})
        
        assert result.isError is False
        assert len(result.content) > 0

    def test_call_tool_nonexistent(self, db_session, test_user):
        """测试调用不存在的工具"""
        from app.services.mcp_service import MCPService
        
        mcp_service = MCPService(db_session)
        result = mcp_service.call_tool(test_user, "nonexistent_tool", {})
        
        assert result.isError is True
        assert "不存在" in result.content[0].text

    def test_read_resource_shop_info(self, db_session, test_user):
        """测试读取店铺信息资源"""
        from app.services.mcp_service import MCPService
        
        mcp_service = MCPService(db_session)
        result = mcp_service.read_resource(test_user, "shop://info")
        
        assert result.uri == "shop://info"
        assert result.text is not None

    def test_read_resource_nonexistent(self, db_session, test_user):
        """测试读取不存在的资源"""
        from app.services.mcp_service import MCPService
        
        mcp_service = MCPService(db_session)
        result = mcp_service.read_resource(test_user, "shop://nonexistent")
        
        assert "不存在" in result.text


class TestAPIKeyService:
    """API密钥服务测试"""

    def test_generate_api_key(self, db_session, test_user):
        """测试生成API密钥"""
        from app.services.auth_service import AuthService
        
        auth_service = AuthService(db_session)
        result = auth_service.generate_api_key(test_user.id, 30)
        
        assert "api_key" in result
        assert result["api_key"].startswith("sk_")
        assert result["expires_at"] is not None

    def test_revoke_api_key(self, db_session, test_user):
        """测试撤销API密钥"""
        from app.services.auth_service import AuthService
        
        auth_service = AuthService(db_session)
        auth_service.generate_api_key(test_user.id)
        
        result = auth_service.revoke_api_key(test_user.id)
        assert result is True
        
        status = auth_service.get_api_key_status(test_user.id)
        assert status["has_api_key"] is False

    def test_get_api_key_status(self, db_session, test_user):
        """测试获取API密钥状态"""
        from app.services.auth_service import AuthService
        
        auth_service = AuthService(db_session)
        status = auth_service.get_api_key_status(test_user.id)
        
        assert "has_api_key" in status
        assert "is_expired" in status

    def test_verify_api_key(self, db_session, test_user):
        """测试验证API密钥"""
        from app.services.auth_service import AuthService
        
        auth_service = AuthService(db_session)
        auth_service.generate_api_key(test_user.id)
        
        user = auth_service.verify_api_key(test_user.api_key)
        assert user is not None
        assert user.id == test_user.id

    def test_verify_invalid_api_key(self, db_session):
        """测试验证无效API密钥"""
        from app.services.auth_service import AuthService
        
        auth_service = AuthService(db_session)
        user = auth_service.verify_api_key("sk_invalid_key")
        assert user is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
