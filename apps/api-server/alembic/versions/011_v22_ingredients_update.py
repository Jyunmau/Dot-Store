"""V2.2 食材表结构更新

Revision ID: 011
Revises: 010
Create Date: 2026-02-22

"""
from alembic import op
import sqlalchemy as sa

revision = '011'
down_revision = '010'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('ingredients', sa.Column('min_stock', sa.Numeric(10, 2), nullable=True, server_default='0'))
    op.add_column('ingredients', sa.Column('cost_per_unit', sa.Numeric(10, 2), nullable=True, server_default='0'))
    op.add_column('ingredients', sa.Column('category', sa.String(64), nullable=True))
    op.add_column('ingredients', sa.Column('supplier', sa.String(128), nullable=True))
    op.add_column('ingredients', sa.Column('expiry_date', sa.Date(), nullable=True))
    op.add_column('ingredients', sa.Column('status', sa.String(32), nullable=True, server_default='active'))


def downgrade():
    op.drop_column('ingredients', 'status')
    op.drop_column('ingredients', 'expiry_date')
    op.drop_column('ingredients', 'supplier')
    op.drop_column('ingredients', 'category')
    op.drop_column('ingredients', 'cost_per_unit')
    op.drop_column('ingredients', 'min_stock')
