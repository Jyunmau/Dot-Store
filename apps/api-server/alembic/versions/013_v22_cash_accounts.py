"""V2.2 现金账户表迁移

Revision ID: 013
Revises: 012
Create Date: 2026-02-23

"""
from alembic import op
import sqlalchemy as sa

revision = '013'
down_revision = '012'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'cash_accounts',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('account_name', sa.String(64), nullable=False),
        sa.Column('account_type', sa.String(32), nullable=False, server_default='cash'),
        sa.Column('balance', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('total_income', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('total_expense', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('status', sa.String(32), nullable=False, server_default='active'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('version', sa.Integer(), nullable=False, server_default='0'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', name='uq_cash_accounts_user_id')
    )
    
    op.create_index('idx_cash_accounts_user_id', 'cash_accounts', ['user_id'])
    op.create_index('idx_cash_accounts_status', 'cash_accounts', ['status'])
    
    op.create_table(
        'cash_transactions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('account_id', sa.Integer(), nullable=False),
        sa.Column('transaction_no', sa.String(32), nullable=False),
        sa.Column('transaction_type', sa.String(32), nullable=False),
        sa.Column('category', sa.String(64), nullable=False),
        sa.Column('amount', sa.Numeric(12, 2), nullable=False),
        sa.Column('balance_before', sa.Numeric(12, 2), nullable=False),
        sa.Column('balance_after', sa.Numeric(12, 2), nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=True),
        sa.Column('customer_transaction_id', sa.Integer(), nullable=True),
        sa.Column('note', sa.Text(), nullable=True),
        sa.Column('operator_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['account_id'], ['cash_accounts.id']),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id']),
        sa.ForeignKeyConstraint(['customer_transaction_id'], ['customer_transactions.id']),
        sa.ForeignKeyConstraint(['operator_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('transaction_no', name='uq_cash_transactions_no')
    )
    
    op.create_index('idx_cash_transactions_user_id', 'cash_transactions', ['user_id'])
    op.create_index('idx_cash_transactions_account_id', 'cash_transactions', ['account_id'])
    op.create_index('idx_cash_transactions_type', 'cash_transactions', ['transaction_type'])
    op.create_index('idx_cash_transactions_category', 'cash_transactions', ['category'])
    op.create_index('idx_cash_transactions_created_at', 'cash_transactions', ['created_at'])


def downgrade():
    op.drop_index('idx_cash_transactions_created_at', 'cash_transactions')
    op.drop_index('idx_cash_transactions_category', 'cash_transactions')
    op.drop_index('idx_cash_transactions_type', 'cash_transactions')
    op.drop_index('idx_cash_transactions_account_id', 'cash_transactions')
    op.drop_index('idx_cash_transactions_user_id', 'cash_transactions')
    op.drop_table('cash_transactions')
    
    op.drop_index('idx_cash_accounts_status', 'cash_accounts')
    op.drop_index('idx_cash_accounts_user_id', 'cash_accounts')
    op.drop_table('cash_accounts')
