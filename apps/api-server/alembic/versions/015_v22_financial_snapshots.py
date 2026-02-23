"""V2.2 财务快照表迁移

Revision ID: 015
Revises: 014
Create Date: 2026-02-23

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision = '015'
down_revision = '014'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'financial_snapshots',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('snapshot_date', sa.Date(), nullable=False),
        sa.Column('snapshot_type', sa.String(32), nullable=False, server_default='daily'),
        sa.Column('cash_balance', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('customer_prepaid', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('inventory_value', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('total_assets', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('total_liabilities', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('net_assets', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('daily_revenue', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('daily_expense', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('daily_profit', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('order_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('validation_status', sa.String(32), nullable=False, server_default='pending'),
        sa.Column('validation_errors', JSONB, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'snapshot_date', name='uq_financial_snapshots_user_date')
    )
    
    op.create_index('idx_financial_snapshots_user_id', 'financial_snapshots', ['user_id'])
    op.create_index('idx_financial_snapshots_date', 'financial_snapshots', ['snapshot_date'])
    op.create_index('idx_financial_snapshots_type', 'financial_snapshots', ['snapshot_type'])


def downgrade():
    op.drop_index('idx_financial_snapshots_type', 'financial_snapshots')
    op.drop_index('idx_financial_snapshots_date', 'financial_snapshots')
    op.drop_index('idx_financial_snapshots_user_id', 'financial_snapshots')
    op.drop_table('financial_snapshots')
