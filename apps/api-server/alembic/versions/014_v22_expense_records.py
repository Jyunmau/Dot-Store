"""V2.2 成本记录表迁移

Revision ID: 014
Revises: 013
Create Date: 2026-02-23

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision = '014'
down_revision = '013'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'expense_records',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('category', sa.String(64), nullable=False),
        sa.Column('amount', sa.Numeric(12, 2), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('expense_date', sa.Date(), nullable=False),
        sa.Column('cost_behavior', sa.String(32), nullable=True),
        sa.Column('cost_function', sa.String(32), nullable=True),
        sa.Column('extra_data', JSONB, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_index('idx_expense_records_user_id', 'expense_records', ['user_id'])
    op.create_index('idx_expense_records_category', 'expense_records', ['category'])
    op.create_index('idx_expense_records_date', 'expense_records', ['expense_date'])
    op.create_index('idx_expense_records_created_at', 'expense_records', ['created_at'])


def downgrade():
    op.drop_index('idx_expense_records_created_at', 'expense_records')
    op.drop_index('idx_expense_records_date', 'expense_records')
    op.drop_index('idx_expense_records_category', 'expense_records')
    op.drop_index('idx_expense_records_user_id', 'expense_records')
    op.drop_table('expense_records')
