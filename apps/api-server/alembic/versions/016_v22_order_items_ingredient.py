"""V2.2 订单项添加食材关联

Revision ID: 016
Revises: 015
Create Date: 2026-02-23

"""
from alembic import op
import sqlalchemy as sa

revision = '016'
down_revision = '015'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('order_items', sa.Column('ingredient_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_order_items_ingredient_id', 'order_items', 'ingredients', ['ingredient_id'], ['id'])
    op.create_index('idx_order_items_ingredient_id', 'order_items', ['ingredient_id'])


def downgrade():
    op.drop_index('idx_order_items_ingredient_id', 'order_items')
    op.drop_constraint('fk_order_items_ingredient_id', 'order_items', type_='foreignkey')
    op.drop_column('order_items', 'ingredient_id')
