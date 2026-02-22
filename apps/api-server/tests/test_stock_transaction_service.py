"""
Dot-Store V2.2 库存流水服务测试
"""
import pytest
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.models.user import User
from app.models.stock import Ingredient
from app.models.stock_transaction import StockTransaction
from app.services.stock_transaction_service import StockTransactionService

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


@pytest.fixture
def test_ingredient(db_session, test_user):
    """创建测试食材"""
    ingredient = Ingredient(
        id=1,
        user_id=test_user.id,
        name='珍珠',
        unit='kg',
        current_stock=Decimal('0'),
        cost_per_unit=Decimal('0'),
        status='active'
    )
    db_session.add(ingredient)
    db_session.commit()
    return ingredient


def test_generate_transaction_no():
    """测试生成交易编号"""
    transaction_no = StockTransactionService.generate_transaction_no('I')
    assert transaction_no.startswith('I')
    assert len(transaction_no) > 10


def test_stock_in(db_session, test_user, test_ingredient):
    """测试入库"""
    transaction = StockTransactionService.stock_in(
        db=db_session,
        user_id=test_user.id,
        ingredient_id=test_ingredient.id,
        quantity=Decimal('10'),
        cost=Decimal('50'),
        operator_id=test_user.id
    )
    
    assert transaction.id is not None
    assert transaction.transaction_type == 'purchase'
    assert transaction.quantity == Decimal('10')
    assert transaction.stock_before == Decimal('0')
    assert transaction.stock_after == Decimal('10')
    
    db_session.refresh(test_ingredient)
    assert test_ingredient.current_stock == Decimal('10')
    assert test_ingredient.cost_per_unit == Decimal('50')


def test_stock_out(db_session, test_user, test_ingredient):
    """测试出库"""
    test_ingredient.current_stock = Decimal('10')
    db_session.commit()
    
    transaction = StockTransactionService.stock_out(
        db=db_session,
        user_id=test_user.id,
        ingredient_id=test_ingredient.id,
        quantity=Decimal('5'),
        operator_id=test_user.id
    )
    
    assert transaction.transaction_type == 'consume'
    assert transaction.quantity == Decimal('5')
    assert transaction.stock_before == Decimal('10')
    assert transaction.stock_after == Decimal('5')
    
    db_session.refresh(test_ingredient)
    assert test_ingredient.current_stock == Decimal('5')


def test_stock_out_insufficient(db_session, test_user, test_ingredient):
    """测试库存不足出库"""
    test_ingredient.current_stock = Decimal('5')
    db_session.commit()
    
    with pytest.raises(ValueError, match="库存不足"):
        StockTransactionService.stock_out(
            db=db_session,
            user_id=test_user.id,
            ingredient_id=test_ingredient.id,
            quantity=Decimal('10'),
            operator_id=test_user.id
        )


def test_adjust_stock(db_session, test_user, test_ingredient):
    """测试库存调整"""
    test_ingredient.current_stock = Decimal('10')
    db_session.commit()
    
    transaction = StockTransactionService.adjust_stock(
        db=db_session,
        user_id=test_user.id,
        ingredient_id=test_ingredient.id,
        quantity=Decimal('5'),
        operator_id=test_user.id
    )
    
    assert transaction.transaction_type == 'adjust_add'
    assert transaction.stock_after == Decimal('15')
    
    db_session.refresh(test_ingredient)
    assert test_ingredient.current_stock == Decimal('15')


def test_get_transactions(db_session, test_user, test_ingredient):
    """测试获取库存流水列表"""
    StockTransactionService.stock_in(
        db=db_session,
        user_id=test_user.id,
        ingredient_id=test_ingredient.id,
        quantity=Decimal('10'),
        operator_id=test_user.id
    )
    
    StockTransactionService.stock_out(
        db=db_session,
        user_id=test_user.id,
        ingredient_id=test_ingredient.id,
        quantity=Decimal('5'),
        operator_id=test_user.id
    )
    
    transactions, total = StockTransactionService.get_transactions(
        db=db_session,
        user_id=test_user.id,
        page=1,
        page_size=10
    )
    
    assert total == 2
    assert len(transactions) == 2


def test_get_stock_warnings(db_session, test_user):
    """测试获取库存预警"""
    ingredient1 = Ingredient(
        user_id=test_user.id,
        name='珍珠',
        unit='kg',
        current_stock=Decimal('1'),
        min_stock=Decimal('5'),
        status='active'
    )
    ingredient2 = Ingredient(
        user_id=test_user.id,
        name='奶茶粉',
        unit='kg',
        current_stock=Decimal('10'),
        min_stock=Decimal('2'),
        status='active'
    )
    db_session.add_all([ingredient1, ingredient2])
    db_session.commit()
    
    warnings = StockTransactionService.get_stock_warnings(db_session, test_user.id)
    
    assert len(warnings) == 1
    assert warnings[0]['ingredient_name'] == '珍珠'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
