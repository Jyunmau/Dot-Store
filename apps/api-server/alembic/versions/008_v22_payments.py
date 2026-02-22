"""V2.2 支付记录表迁移

Revision ID: 008
Revises: 007
Create Date: 2026-02-22

"""
from alembic import op
import sqlalchemy as sa

revision = '008'
down_revision = '007'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'payments',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('payment_method', sa.String(32), nullable=False),
        sa.Column('amount', sa.Numeric(12, 2), nullable=False),
        sa.Column('payment_time', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('note', sa.Text(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id']),
        sa.ForeignKeyConstraint(['created_by'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_index('idx_payments_order_id', 'payments', ['order_id'])
    op.create_index('idx_payments_payment_time', 'payments', ['payment_time'])


def downgrade():
    op.drop_index('idx_payments_payment_time', 'payments')
    op.drop_index('idx_payments_order_id', 'payments')
    op.drop_table('payments')
