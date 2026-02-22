"""V2.2 订单表结构更新

Revision ID: 010
Revises: 009
Create Date: 2026-02-22

"""
from alembic import op
import sqlalchemy as sa

revision = '010'
down_revision = '009'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('orders', sa.Column('order_no', sa.String(32), nullable=True))
    op.add_column('orders', sa.Column('payment_method', sa.String(32), nullable=True))
    op.add_column('orders', sa.Column('customer_account_id', sa.Integer(), nullable=True))
    op.add_column('orders', sa.Column('cash_transaction_id', sa.Integer(), nullable=True))
    
    op.execute("""
        UPDATE orders 
        SET order_no = 'O' || TO_CHAR(created_at, 'YYYYMMDD') || LPAD(id::TEXT, 4, '0') 
        WHERE order_no IS NULL
    """)
    
    op.alter_column('orders', 'order_no', nullable=False)
    op.create_index('idx_orders_order_no', 'orders', ['order_no'], unique=True)


def downgrade():
    op.drop_index('idx_orders_order_no', 'orders')
    op.drop_column('orders', 'cash_transaction_id')
    op.drop_column('orders', 'customer_account_id')
    op.drop_column('orders', 'payment_method')
    op.drop_column('orders', 'order_no')
