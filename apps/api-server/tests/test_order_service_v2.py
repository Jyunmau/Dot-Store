"""
Dot-Store V2.2 订单服务V2测试
"""
import pytest
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.models.user import User
from app.models.order import Order
from app.models.order_item import OrderItem
from app.services.order_service_v2 import OrderServiceV2

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
    user = User(
        id=1,
        phone="13800138000",
        password_hash="hashed_password",
        shop_name="测试店铺",
        shop_type="restaurant",
        city="北京"
    )
    db_session.add(user)
    db_session.commit()
    return user


def test_generate_order_no(db_session, test_user):
    """测试生成订单编号"""
    order_no = OrderServiceV2.generate_order_no(db_session, test_user.id)
    assert order_no.startswith('O')
    assert len(order_no) == 13  # O + YYYYMMDD + 4位序号


def test_create_order(db_session, test_user):
    """测试创建订单"""
    order = OrderServiceV2.create_order(
        db=db_session,
        user_id=test_user.id,
        order_type='dine_in',
        amount=Decimal('100.00'),
        payment_method='cash',
        created_by=test_user.id
    )
    
    assert order.id is not None
    assert order.order_no.startswith('O')
    assert order.amount == Decimal('100.00')
    assert order.status == 'completed'


def test_create_order_with_items(db_session, test_user):
    """测试创建带订单项的订单"""
    items = [
        {
            'product_name': '奶茶',
            'quantity': 2,
            'unit_price': 15.00,
            'cost_price': 5.00
        }
    ]
    
    order = OrderServiceV2.create_order(
        db=db_session,
        user_id=test_user.id,
        order_type='dine_in',
        amount=Decimal('30.00'),
        items=items,
        created_by=test_user.id
    )
    
    assert order.id is not None


def test_get_orders(db_session, test_user):
    """测试获取订单列表"""
    for i in range(3):
        OrderServiceV2.create_order(
            db=db_session,
            user_id=test_user.id,
            order_type='dine_in',
            amount=Decimal(f'{(i+1) * 100}.00'),
            created_by=test_user.id
        )
    
    orders, total = OrderServiceV2.get_orders(
        db=db_session,
        user_id=test_user.id,
        page=1,
        page_size=10
    )
    
    assert total == 3
    assert len(orders) == 3


def test_void_order(db_session, test_user):
    """测试作废订单"""
    order = OrderServiceV2.create_order(
        db=db_session,
        user_id=test_user.id,
        order_type='dine_in',
        amount=Decimal('100.00'),
        created_by=test_user.id
    )
    
    voided_order = OrderServiceV2.void_order(
        db=db_session,
        user_id=test_user.id,
        order_id=order.id,
        reason='客户取消',
        voided_by=test_user.id
    )
    
    assert voided_order.is_deleted is True
    assert voided_order.status == 'voided'


def test_void_already_voided_order(db_session, test_user):
    """测试作废已作废的订单"""
    order = OrderServiceV2.create_order(
        db=db_session,
        user_id=test_user.id,
        order_type='dine_in',
        amount=Decimal('100.00'),
        created_by=test_user.id
    )
    
    OrderServiceV2.void_order(
        db=db_session,
        user_id=test_user.id,
        order_id=order.id,
        reason='客户取消',
        voided_by=test_user.id
    )
    
    with pytest.raises(ValueError, match="订单已作废"):
        OrderServiceV2.void_order(
            db=db_session,
            user_id=test_user.id,
            order_id=order.id,
            reason='再次作废',
            voided_by=test_user.id
        )


def test_add_order_item(db_session, test_user):
    """测试添加订单项"""
    order = OrderServiceV2.create_order(
        db=db_session,
        user_id=test_user.id,
        order_type='dine_in',
        amount=Decimal('100.00'),
        created_by=test_user.id
    )
    
    item = OrderServiceV2.add_order_item(
        db=db_session,
        user_id=test_user.id,
        order_id=order.id,
        product_name='珍珠奶茶',
        quantity=Decimal('2'),
        unit_price=Decimal('15'),
        cost_price=Decimal('5')
    )
    
    assert item.id is not None
    assert item.product_name == '珍珠奶茶'
    assert item.quantity == Decimal('2')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
