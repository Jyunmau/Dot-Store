-- 创建现金流分析表
CREATE TABLE IF NOT EXISTS cash_flow_analyses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    analysis_date DATE NOT NULL,
    analysis_type VARCHAR(32) NOT NULL DEFAULT 'monthly',
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    total_income NUMERIC(12, 2) NOT NULL DEFAULT 0,
    total_expense NUMERIC(12, 2) NOT NULL DEFAULT 0,
    net_cash_flow NUMERIC(12, 2) NOT NULL DEFAULT 0,
    avg_daily_income NUMERIC(12, 2) NOT NULL DEFAULT 0,
    avg_daily_expense NUMERIC(12, 2) NOT NULL DEFAULT 0,
    income_structure JSONB NOT NULL DEFAULT '{}',
    expense_structure JSONB NOT NULL DEFAULT '{}',
    health_score NUMERIC(5, 2) NOT NULL DEFAULT 0,
    risk_level VARCHAR(32) NOT NULL DEFAULT 'low',
    recommendations JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_cash_flow_analyses_user_id ON cash_flow_analyses(user_id);
CREATE INDEX IF NOT EXISTS ix_cash_flow_analyses_analysis_date ON cash_flow_analyses(analysis_date);
CREATE INDEX IF NOT EXISTS ix_cash_flow_analyses_user_date ON cash_flow_analyses(user_id, analysis_date);

-- 创建现金流预测表
CREATE TABLE IF NOT EXISTS cash_flow_forecasts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    forecast_date DATE NOT NULL,
    target_date DATE NOT NULL,
    predicted_income NUMERIC(12, 2) NOT NULL DEFAULT 0,
    predicted_expense NUMERIC(12, 2) NOT NULL DEFAULT 0,
    predicted_balance NUMERIC(12, 2) NOT NULL DEFAULT 0,
    confidence_level NUMERIC(5, 2) NOT NULL DEFAULT 0,
    risk_alert BOOLEAN NOT NULL DEFAULT FALSE,
    alert_message TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_cash_flow_forecasts_user_id ON cash_flow_forecasts(user_id);
CREATE INDEX IF NOT EXISTS ix_cash_flow_forecasts_forecast_date ON cash_flow_forecasts(forecast_date);
CREATE INDEX IF NOT EXISTS ix_cash_flow_forecasts_target_date ON cash_flow_forecasts(target_date);
CREATE INDEX IF NOT EXISTS ix_cash_flow_forecasts_user_date ON cash_flow_forecasts(user_id, forecast_date);

-- 创建风险预警表
CREATE TABLE IF NOT EXISTS risk_alerts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    alert_date DATE NOT NULL,
    alert_level VARCHAR(32) NOT NULL,
    alert_type VARCHAR(64) NOT NULL,
    message TEXT NOT NULL,
    suggestions JSONB,
    is_read BOOLEAN NOT NULL DEFAULT FALSE,
    is_resolved BOOLEAN NOT NULL DEFAULT FALSE,
    resolved_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_risk_alerts_user_id ON risk_alerts(user_id);
CREATE INDEX IF NOT EXISTS ix_risk_alerts_alert_date ON risk_alerts(alert_date);
CREATE INDEX IF NOT EXISTS ix_risk_alerts_alert_level ON risk_alerts(alert_level);
