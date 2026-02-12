"""收支记录表和收支分类表迁移

Revision ID: 004
Create Date: 2026-02-12

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '004'
down_revision: Union[str, None] = '003'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    创建收支分类表和收支记录表
    """
    op.create_table(
        'transaction_categories',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=64), nullable=False),
        sa.Column('type', sa.String(length=32), nullable=False),
        sa.Column('description', sa.String(length=256), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transaction_categories_user_id'), 'transaction_categories', ['user_id'], unique=False)
    op.create_index(op.f('ix_transaction_categories_type'), 'transaction_categories', ['type'], unique=False)

    op.create_table(
        'transactions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(length=32), nullable=False),
        sa.Column('category', sa.String(length=64), nullable=False),
        sa.Column('amount', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=True),
        sa.Column('note', sa.Text(), nullable=True),
        sa.Column('attachment_url', sa.String(length=256), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('created_by', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transactions_user_id'), 'transactions', ['user_id'], unique=False)
    op.create_index(op.f('ix_transactions_type'), 'transactions', ['type'], unique=False)
    op.create_index(op.f('ix_transactions_category'), 'transactions', ['category'], unique=False)
    op.create_index(op.f('ix_transactions_created_at'), 'transactions', ['created_at'], unique=False)


def downgrade() -> None:
    """
    删除收支记录表和收支分类表
    """
    op.drop_index(op.f('ix_transactions_created_at'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_category'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_type'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_user_id'), table_name='transactions')
    op.drop_table('transactions')

    op.drop_index(op.f('ix_transaction_categories_type'), table_name='transaction_categories')
    op.drop_index(op.f('ix_transaction_categories_user_id'), table_name='transaction_categories')
    op.drop_table('transaction_categories')
