"""修改订单表JSON列为JSONB类型

Revision ID: 003
Revises: 002
Create Date: 2026-02-12

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade():
    # 修改tags和order_metadata列类型为JSONB
    op.execute("""
        ALTER TABLE orders 
        ALTER COLUMN tags TYPE JSONB USING tags::jsonb,
        ALTER COLUMN order_metadata TYPE JSONB USING order_metadata::jsonb
    """)


def downgrade():
    # 回滚到JSON类型
    op.execute("""
        ALTER TABLE orders 
        ALTER COLUMN tags TYPE JSON USING tags::json,
        ALTER COLUMN order_metadata TYPE JSON USING order_metadata::json
    """)
