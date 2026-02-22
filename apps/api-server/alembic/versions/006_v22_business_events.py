"""V2.2 业务事件表迁移

Revision ID: 006
Revises: 005_push
Create Date: 2026-02-22

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '006'
down_revision = '005'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'business_events',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('event_type', sa.String(64), nullable=False),
        sa.Column('event_category', sa.String(32), nullable=False),
        sa.Column('entity_type', sa.String(64), nullable=True),
        sa.Column('entity_id', sa.Integer(), nullable=True),
        sa.Column('operator_id', sa.Integer(), nullable=False),
        sa.Column('operator_type', sa.String(32), nullable=False),
        sa.Column('data', postgresql.JSONB, nullable=True),
        sa.Column('ip_address', sa.String(45), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['operator_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_index('idx_events_user_id', 'business_events', ['user_id'])
    op.create_index('idx_events_event_type', 'business_events', ['event_type'])
    op.create_index('idx_events_entity', 'business_events', ['entity_type', 'entity_id'])
    op.create_index('idx_events_created_at', 'business_events', ['created_at'])
    op.create_index('idx_events_category', 'business_events', ['event_category'])


def downgrade():
    op.drop_index('idx_events_category', 'business_events')
    op.drop_index('idx_events_created_at', 'business_events')
    op.drop_index('idx_events_entity', 'business_events')
    op.drop_index('idx_events_event_type', 'business_events')
    op.drop_index('idx_events_user_id', 'business_events')
    op.drop_table('business_events')
