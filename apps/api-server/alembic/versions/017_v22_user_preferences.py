"""create user_preferences table

Revision ID: 017_v22_user_preferences
Revises: 016_v22_order_items_ingredient
Create Date: 2026-02-23

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '017_v22_user_preferences'
down_revision = '016'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user_preferences',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('weekly_reminder_enabled', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('weekly_reminder_day', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('weekly_reminder_time', sa.Time(), nullable=False, server_default='10:00:00'),
        sa.Column('monthly_report_enabled', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('monthly_report_day', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('monthly_report_time', sa.Time(), nullable=False, server_default='09:00:00'),
        sa.Column('risk_alert_enabled', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('risk_alert_threshold', sa.String(32), nullable=False, server_default='medium'),
        sa.Column('notification_channels', postgresql.JSONB(), nullable=False, server_default='["push"]::jsonb'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('user_id'),
    )
    op.create_index('ix_user_preferences_user_id', 'user_preferences', ['user_id'], unique=True)


def downgrade():
    op.drop_index('ix_user_preferences_user_id', table_name='user_preferences')
    op.drop_table('user_preferences')
