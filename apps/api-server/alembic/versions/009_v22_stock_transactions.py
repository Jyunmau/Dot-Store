"""V2.2 库存流水表迁移

Revision ID: 009
Revises: 008
Create Date: 2026-02-22

"""
from alembic import op
import sqlalchemy as sa

revision = '009'
down_revision = '008'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'stock_transactions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('ingredient_id', sa.Integer(), nullable=False),
        sa.Column('transaction_no', sa.String(32), nullable=False),
        sa.Column('transaction_type', sa.String(32), nullable=False),
        sa.Column('quantity', sa.Numeric(10, 2), nullable=False),
        sa.Column('stock_before', sa.Numeric(10, 2), nullable=False),
        sa.Column('stock_after', sa.Numeric(10, 2), nullable=False),
        sa.Column('unit_cost', sa.Numeric(10, 2), nullable=True),
        sa.Column('total_cost', sa.Numeric(12, 2), nullable=True),
        sa.Column('note', sa.Text(), nullable=True),
        sa.Column('operator_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['ingredient_id'], ['ingredients.id']),
        sa.ForeignKeyConstraint(['operator_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('transaction_no')
    )
    
    op.create_index('idx_stock_trans_user_id', 'stock_transactions', ['user_id'])
    op.create_index('idx_stock_trans_ingredient_id', 'stock_transactions', ['ingredient_id'])
    op.create_index('idx_stock_trans_type', 'stock_transactions', ['transaction_type'])
    op.create_index('idx_stock_trans_created_at', 'stock_transactions', ['created_at'])


def downgrade():
    op.drop_index('idx_stock_trans_created_at', 'stock_transactions')
    op.drop_index('idx_stock_trans_type', 'stock_transactions')
    op.drop_index('idx_stock_trans_ingredient_id', 'stock_transactions')
    op.drop_index('idx_stock_trans_user_id', 'stock_transactions')
    op.drop_table('stock_transactions')
