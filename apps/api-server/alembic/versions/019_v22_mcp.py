"""create mcp_sessions and mcp_operation_logs tables

Revision ID: 019_v22_mcp
Revises: 018_v22_api_key
Create Date: 2026-02-23

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '019_v22_mcp'
down_revision = '020_v22_cash_flow'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'mcp_sessions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.String(64), nullable=False),
        sa.Column('api_key_id', sa.Integer(), nullable=True),
        sa.Column('client_info', postgresql.JSONB(), nullable=True),
        sa.Column('status', sa.String(32), nullable=False, server_default='active'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('last_active_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['api_key_id'], ['users.id'], ondelete='SET NULL'),
        sa.UniqueConstraint('session_id'),
    )
    op.create_index('ix_mcp_sessions_user_id', 'mcp_sessions', ['user_id'])
    op.create_index('ix_mcp_sessions_session_id', 'mcp_sessions', ['session_id'], unique=True)
    op.create_index('ix_mcp_sessions_status', 'mcp_sessions', ['status'])

    op.create_table(
        'mcp_operation_logs',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.String(64), nullable=False),
        sa.Column('operation_type', sa.String(32), nullable=False),
        sa.Column('tool_name', sa.String(64), nullable=True),
        sa.Column('resource_uri', sa.String(256), nullable=True),
        sa.Column('input_params', postgresql.JSONB(), nullable=True),
        sa.Column('output_result', postgresql.JSONB(), nullable=True),
        sa.Column('status', sa.String(32), nullable=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('duration_ms', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_mcp_operation_logs_user_id', 'mcp_operation_logs', ['user_id'])
    op.create_index('ix_mcp_operation_logs_session_id', 'mcp_operation_logs', ['session_id'])
    op.create_index('ix_mcp_operation_logs_operation_type', 'mcp_operation_logs', ['operation_type'])
    op.create_index('ix_mcp_operation_logs_status', 'mcp_operation_logs', ['status'])
    op.create_index('ix_mcp_operation_logs_created_at', 'mcp_operation_logs', ['created_at'])


def downgrade():
    op.drop_index('ix_mcp_operation_logs_created_at', table_name='mcp_operation_logs')
    op.drop_index('ix_mcp_operation_logs_status', table_name='mcp_operation_logs')
    op.drop_index('ix_mcp_operation_logs_operation_type', table_name='mcp_operation_logs')
    op.drop_index('ix_mcp_operation_logs_session_id', table_name='mcp_operation_logs')
    op.drop_index('ix_mcp_operation_logs_user_id', table_name='mcp_operation_logs')
    op.drop_table('mcp_operation_logs')

    op.drop_index('ix_mcp_sessions_status', table_name='mcp_sessions')
    op.drop_index('ix_mcp_sessions_session_id', table_name='mcp_sessions')
    op.drop_index('ix_mcp_sessions_user_id', table_name='mcp_sessions')
    op.drop_table('mcp_sessions')
