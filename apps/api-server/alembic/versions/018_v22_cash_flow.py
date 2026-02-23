"""V2.2 现金流分析模块

Revision ID: 018_v22_cash_flow
Revises: 017_v22_user_preferences
Create Date: 2026-02-23

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '018_v22_cash_flow'
down_revision = '017_v22_user_preferences'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'cash_flow_analyses',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('analysis_date', sa.Date(), nullable=False),
        sa.Column('analysis_type', sa.String(32), nullable=False, server_default='monthly'),
        sa.Column('period_start', sa.Date(), nullable=False),
        sa.Column('period_end', sa.Date(), nullable=False),
        sa.Column('total_income', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('total_expense', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('net_cash_flow', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('avg_daily_income', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('avg_daily_expense', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('income_structure', postgresql.JSONB, nullable=False, server_default='{}'),
        sa.Column('expense_structure', postgresql.JSONB, nullable=False, server_default='{}'),
        sa.Column('health_score', sa.Numeric(5, 2), nullable=False, server_default='0'),
        sa.Column('risk_level', sa.String(32), nullable=False, server_default='low'),
        sa.Column('recommendations', postgresql.JSONB, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_cash_flow_analyses_user_date', 'cash_flow_analyses', ['user_id', 'analysis_date'])
    op.create_index(op.f('ix_cash_flow_analyses_user_id'), 'cash_flow_analyses', ['user_id'])
    op.create_index(op.f('ix_cash_flow_analyses_analysis_date'), 'cash_flow_analyses', ['analysis_date'])

    op.create_table(
        'cash_flow_forecasts',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('forecast_date', sa.Date(), nullable=False),
        sa.Column('target_date', sa.Date(), nullable=False),
        sa.Column('predicted_income', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('predicted_expense', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('predicted_balance', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('confidence_level', sa.Numeric(5, 2), nullable=False, server_default='0'),
        sa.Column('risk_alert', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('alert_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_cash_flow_forecasts_user_date', 'cash_flow_forecasts', ['user_id', 'forecast_date'])
    op.create_index(op.f('ix_cash_flow_forecasts_user_id'), 'cash_flow_forecasts', ['user_id'])
    op.create_index(op.f('ix_cash_flow_forecasts_forecast_date'), 'cash_flow_forecasts', ['forecast_date'])
    op.create_index(op.f('ix_cash_flow_forecasts_target_date'), 'cash_flow_forecasts', ['target_date'])

    op.create_table(
        'risk_alerts',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('alert_date', sa.Date(), nullable=False),
        sa.Column('alert_level', sa.String(32), nullable=False),
        sa.Column('alert_type', sa.String(64), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('suggestions', postgresql.JSONB, nullable=True),
        sa.Column('is_read', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('is_resolved', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('resolved_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_risk_alerts_user_id'), 'risk_alerts', ['user_id'])
    op.create_index(op.f('ix_risk_alerts_alert_date'), 'risk_alerts', ['alert_date'])
    op.create_index(op.f('ix_risk_alerts_alert_level'), 'risk_alerts', ['alert_level'])


def downgrade():
    op.drop_index(op.f('ix_risk_alerts_alert_level'), table_name='risk_alerts')
    op.drop_index(op.f('ix_risk_alerts_alert_date'), table_name='risk_alerts')
    op.drop_index(op.f('ix_risk_alerts_user_id'), table_name='risk_alerts')
    op.drop_table('risk_alerts')

    op.drop_index(op.f('ix_cash_flow_forecasts_target_date'), table_name='cash_flow_forecasts')
    op.drop_index(op.f('ix_cash_flow_forecasts_forecast_date'), table_name='cash_flow_forecasts')
    op.drop_index(op.f('ix_cash_flow_forecasts_user_id'), table_name='cash_flow_forecasts')
    op.drop_index('ix_cash_flow_forecasts_user_date', table_name='cash_flow_forecasts')
    op.drop_table('cash_flow_forecasts')

    op.drop_index(op.f('ix_cash_flow_analyses_analysis_date'), table_name='cash_flow_analyses')
    op.drop_index(op.f('ix_cash_flow_analyses_user_id'), table_name='cash_flow_analyses')
    op.drop_index('ix_cash_flow_analyses_user_date', table_name='cash_flow_analyses')
    op.drop_table('cash_flow_analyses')
