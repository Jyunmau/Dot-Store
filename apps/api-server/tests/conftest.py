"""
Dot-Store V2.2 测试配置
"""
import pytest
from datetime import datetime
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
        status="active"
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def test_staff(db_session, test_user):
    """创建测试店员"""
    from app.models.user import User
    staff = User(
        id=2,
        phone="13800138001",
        password_hash="hashed_password",
        shop_name=test_user.shop_name,
        shop_type=test_user.shop_type,
        city=test_user.city,
        role="staff",
        status="active",
        permissions='["order:read"]'
    )
    db_session.add(staff)
    db_session.commit()
    return staff
