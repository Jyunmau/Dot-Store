"""V2.2 客户账户表迁移

Revision ID: 012
Revises: 011
Create Date: 2026-02-23

"""
from alembic import op
import sqlalchemy as sa

revision = '012'
down_revision = '011'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'customer_accounts',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('customer_name', sa.String(64), nullable=False),
        sa.Column('phone', sa.String(32), nullable=False),
        sa.Column('balance', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('total_recharged', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('total_consumed', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('status', sa.String(32), nullable=False, server_default='active'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('version', sa.Integer(), nullable=False, server_default='0'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'phone', name='uq_customer_accounts_user_phone')
    )
    
    op.create_index('idx_customer_accounts_user_id', 'customer_accounts', ['user_id'])
    op.create_index('idx_customer_accounts_phone', 'customer_accounts', ['phone'])
    op.create_index('idx_customer_accounts_status', 'customer_accounts', ['status'])
    
    op.create_table(
        'customer_transactions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('account_id', sa.Integer(), nullable=False),
        sa.Column('transaction_no', sa.String(32), nullable=False),
        sa.Column('transaction_type', sa.String(32), nullable=False),
        sa.Column('amount', sa.Numeric(12, 2), nullable=False),
        sa.Column('balance_before', sa.Numeric(12, 2), nullable=False),
        sa.Column('balance_after', sa.Numeric(12, 2), nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=True),
        sa.Column('note', sa.Text(), nullable=True),
        sa.Column('operator_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['account_id'], ['customer_accounts.id']),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id']),
        sa.ForeignKeyConstraint(['operator_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('transaction_no', name='uq_customer_transactions_no')
    )
    
    op.create_index('idx_customer_transactions_user_id', 'customer_transactions', ['user_id'])
    op.create_index('idx_customer_transactions_account_id', 'customer_transactions', ['account_id'])
    op.create_index('idx_customer_transactions_type', 'customer_transactions', ['transaction_type'])
    op.create_index('idx_customer_transactions_created_at', 'customer_transactions', ['created_at'])


def downgrade():
    op.drop_index('idx_customer_transactions_created_at', 'customer_transactions')
    op.drop_index('idx_customer_transactions_type', 'customer_transactions')
    op.drop_index('idx_customer_transactions_account_id', 'customer_transactions')
    op.drop_index('idx_customer_transactions_user_id', 'customer_transactions')
    op.drop_table('customer_transactions')
    
    op.drop_index('idx_customer_accounts_status', 'customer_accounts')
    op.drop_index('idx_customer_accounts_phone', 'customer_accounts')
    op.drop_index('idx_customer_accounts_user_id', 'customer_accounts')
    op.drop_table('customer_accounts')
