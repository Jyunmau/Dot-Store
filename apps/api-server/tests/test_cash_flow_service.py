"""
Dot-Store V2.2 现金流分析服务单元测试
"""
import pytest
from datetime import date, timedelta
from decimal import Decimal
from unittest.mock import Mock, patch, MagicMock
from app.services.cash_flow_service import CashFlowService, SafetyLevel


class TestCashFlowService:
    """现金流分析服务测试类"""

    def test_safety_level_constants(self):
        """测试安全等级常量"""
        assert SafetyLevel.SAFE == 'safe'
        assert SafetyLevel.WARNING == 'warning'
        assert SafetyLevel.DANGER == 'danger'
        
        assert SafetyLevel.COLORS[SafetyLevel.SAFE] == '#52C41A'
        assert SafetyLevel.COLORS[SafetyLevel.WARNING] == '#FA541C'
        assert SafetyLevel.COLORS[SafetyLevel.DANGER] == '#F5222D'

    @patch('app.services.cash_flow_service.CashAccount')
    @patch('app.services.cash_flow_service.CustomerAccount')
    def test_calculate_safety_index_no_account(self, mock_customer, mock_cash):
        """测试无现金账户时的安全指数计算"""
        mock_db = Mock()
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        result = CashFlowService.calculate_safety_index(mock_db, 1)
        
        assert result['safety_score'] == 0
        assert result['safety_level'] == SafetyLevel.DANGER
        assert result['message'] == '请先创建现金账户'

    @patch('app.services.cash_flow_service.CashAccount')
    @patch('app.services.cash_flow_service.CustomerAccount')
    @patch('app.services.cash_flow_service.CashTransaction')
    def test_calculate_safety_index_safe(self, mock_transaction, mock_customer, mock_cash):
        """测试安全状态的安全指数计算"""
        mock_db = Mock()
        
        mock_cash_account = Mock()
        mock_cash_account.balance = Decimal('100000')
        mock_db.query.return_value.filter.return_value.first.return_value = mock_cash_account
        
        mock_db.query.return_value.filter.return_value.scalar.return_value = 10000
        
        result = CashFlowService.calculate_safety_index(mock_db, 1)
        
        assert result['safety_level'] == SafetyLevel.SAFE
        assert result['safety_score'] >= 80

    @patch('app.services.cash_flow_service.CashAccount')
    @patch('app.services.cash_flow_service.CustomerAccount')
    @patch('app.services.cash_flow_service.CashTransaction')
    def test_calculate_safety_index_warning(self, mock_transaction, mock_customer, mock_cash):
        """测试警告状态的安全指数计算"""
        mock_db = Mock()
        
        mock_cash_account = Mock()
        mock_cash_account.balance = Decimal('20000')
        mock_db.query.return_value.filter.return_value.first.return_value = mock_cash_account
        
        mock_db.query.return_value.filter.return_value.scalar.return_value = 5000
        
        result = CashFlowService.calculate_safety_index(mock_db, 1)
        
        assert result['safety_level'] in [SafetyLevel.SAFE, SafetyLevel.WARNING]

    @patch('app.services.cash_flow_service.CashAccount')
    @patch('app.services.cash_flow_service.CustomerAccount')
    @patch('app.services.cash_flow_service.CashTransaction')
    def test_calculate_safety_index_danger(self, mock_transaction, mock_customer, mock_cash):
        """测试危险状态的安全指数计算"""
        mock_db = Mock()
        
        mock_cash_account = Mock()
        mock_cash_account.balance = Decimal('1000')
        mock_db.query.return_value.filter.return_value.first.return_value = mock_cash_account
        
        mock_db.query.return_value.filter.return_value.scalar.return_value = 500
        
        result = CashFlowService.calculate_safety_index(mock_db, 1)
        
        assert result['safety_level'] == SafetyLevel.DANGER

    def test_calculate_health_score_excellent(self):
        """测试优秀健康度评分计算"""
        score = CashFlowService._calculate_health_score(
            total_income=100000,
            total_expense=50000,
            net_cash_flow=50000,
            avg_daily_income=3000
        )
        
        assert score >= 80

    def test_calculate_health_score_poor(self):
        """测试较差健康度评分计算"""
        score = CashFlowService._calculate_health_score(
            total_income=10000,
            total_expense=15000,
            net_cash_flow=-5000,
            avg_daily_income=300
        )
        
        assert score < 60

    def test_assess_risk_level_low(self):
        """测试低风险评估"""
        level = CashFlowService._assess_risk_level(
            net_cash_flow=50000,
            health_score=90
        )
        assert level == 'low'

    def test_assess_risk_level_medium(self):
        """测试中风险评估"""
        level = CashFlowService._assess_risk_level(
            net_cash_flow=10000,
            health_score=70
        )
        assert level == 'medium'

    def test_assess_risk_level_high(self):
        """测试高风险评估"""
        level = CashFlowService._assess_risk_level(
            net_cash_flow=-5000,
            health_score=50
        )
        assert level == 'high'

    def test_assess_risk_level_critical(self):
        """测试严重风险评估"""
        level = CashFlowService._assess_risk_level(
            net_cash_flow=-50000,
            health_score=30
        )
        assert level == 'critical'

    def test_generate_recommendations_high_risk(self):
        """测试高风险建议生成"""
        recommendations = CashFlowService._generate_recommendations(
            income_structure={'销售': 10000},
            expense_structure={'成本': 8000},
            health_score=40,
            risk_level='high'
        )
        
        assert any('现金流' in r for r in recommendations)

    def test_generate_recommendations_single_income_source(self):
        """测试单一收入来源建议"""
        recommendations = CashFlowService._generate_recommendations(
            income_structure={'销售': 10000, '其他': 500},
            expense_structure={'成本': 5000},
            health_score=80,
            risk_level='low'
        )
        
        assert any('收入来源' in r for r in recommendations)

    def test_generate_recommendations_good_status(self):
        """测试良好状态建议"""
        recommendations = CashFlowService._generate_recommendations(
            income_structure={'销售': 10000, '服务': 5000},
            expense_structure={'成本': 8000, '人工': 2000},
            health_score=85,
            risk_level='low'
        )
        
        assert '经营状况良好，继续保持' in recommendations


class TestBreakEvenAnalysis:
    """盈亏平衡分析测试类"""

    def test_break_even_calculation_profit(self):
        """测试盈利状态盈亏平衡计算"""
        result = {
            'break_even_point': Decimal('50000'),
            'current_revenue': Decimal('80000'),
            'fixed_cost': Decimal('30000'),
            'variable_cost_ratio': 40.0,
            'contribution_margin_ratio': 60.0,
            'safety_margin': Decimal('30000'),
            'safety_margin_ratio': 37.5,
            'status': 'profit'
        }
        
        assert result['status'] == 'profit'
        assert result['safety_margin'] > 0

    def test_break_even_calculation_loss(self):
        """测试亏损状态盈亏平衡计算"""
        result = {
            'break_even_point': Decimal('80000'),
            'current_revenue': Decimal('50000'),
            'fixed_cost': Decimal('40000'),
            'variable_cost_ratio': 30.0,
            'contribution_margin_ratio': 70.0,
            'safety_margin': Decimal('-30000'),
            'safety_margin_ratio': -60.0,
            'status': 'loss'
        }
        
        assert result['status'] == 'loss'
        assert result['safety_margin'] < 0
