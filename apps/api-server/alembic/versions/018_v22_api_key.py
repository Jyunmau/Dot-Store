"""add api_key fields to users table

Revision ID: 018_v22_api_key
Revises: 017_v22_user_preferences
Create Date: 2026-02-23

"""
from alembic import op
import sqlalchemy as sa

revision = '018_v22_api_key'
down_revision = '017_v22_user_preferences'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('api_key', sa.String(64), nullable=True, unique=True))
    op.add_column('users', sa.Column('api_key_created_at', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('api_key_expires_at', sa.DateTime(), nullable=True))
    op.create_index('ix_users_api_key', 'users', ['api_key'], unique=True)


def downgrade():
    op.drop_index('ix_users_api_key', table_name='users')
    op.drop_column('users', 'api_key_expires_at')
    op.drop_column('users', 'api_key_created_at')
    op.drop_column('users', 'api_key')
