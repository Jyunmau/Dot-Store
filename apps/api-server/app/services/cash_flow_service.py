"""
Dot-Store V2.2 现金流分析服务
实现现金流预测、收入结构分析、成本结构分析、盈亏平衡分析等功能
"""
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, case
import numpy as np

from app.models.cash_flow import CashFlowAnalysis, CashFlowForecast
from app.models.cash_account import CashAccount, CashTransaction
from app.models.customer_account import CustomerAccount
from app.models.expense_record import ExpenseRecord
from app.models.financial_snapshot import FinancialSnapshot
from app.models.order import Order
from app.services.event_service import EventService


class SafetyLevel:
    """三色安全等级"""
    SAFE = 'safe'
    WARNING = 'warning'
    DANGER = 'danger'
    
    COLORS = {
        SAFE: '#52C41A',
        WARNING: '#FA541C',
        DANGER: '#F5222D',
    }
    
    MESSAGES = {
        SAFE: '现金流充裕，经营状态良好',
        WARNING: '现金流偏紧，建议关注收支情况',
        DANGER: '现金流紧张，需要立即采取措施',
    }


class CashFlowService:
    """现金流分析服务"""
    
    @staticmethod
    def calculate_safety_index(db: Session, user_id: int) -> Dict[str, Any]:
        """
        计算三色安全指数
        
        计算规则：
        - 可用净现金 = 现金余额 - 预收款负债
        - 可运营天数 = 可用净现金 / 日均支出
        - 安全指数 = min(100, 可运营天数 * 2.5)
        
        分级标准：
        - 80-100分（绿色）：可运营天数 > 30天
        - 50-79分（黄色）：可运营天数 7-30天
        - 0-49分（红色）：可运营天数 < 7天
        """
        cash_account = db.query(CashAccount).filter(
            CashAccount.user_id == user_id
        ).first()
        
        if not cash_account:
            return {
                'safety_score': 0,
                'safety_level': SafetyLevel.DANGER,
                'color_code': SafetyLevel.COLORS[SafetyLevel.DANGER],
                'message': '请先创建现金账户',
                'factors': {
                    'cash_balance': 0,
                    'liability': 0,
                    'net_available': 0,
                    'days_of_operation': 0,
                }
            }
        
        cash_balance = float(cash_account.balance or 0)
        
        liability = db.query(func.sum(CustomerAccount.balance)).filter(
            CustomerAccount.user_id == user_id
        ).scalar() or 0
        liability = float(liability)
        
        net_available = cash_balance - liability
        
        daily_expense = CashFlowService._calculate_daily_expense(db, user_id)
        
        if daily_expense > 0:
            days_of_operation = net_available / daily_expense
        else:
            days_of_operation = 999 if net_available > 0 else 0
        
        safety_score = min(100, days_of_operation * 2.5)
        safety_score = max(0, safety_score)
        
        if safety_score >= 80:
            level = SafetyLevel.SAFE
        elif safety_score >= 50:
            level = SafetyLevel.WARNING
        else:
            level = SafetyLevel.DANGER
        
        return {
            'safety_score': round(safety_score, 1),
            'safety_level': level,
            'color_code': SafetyLevel.COLORS[level],
            'message': SafetyLevel.MESSAGES[level],
            'factors': {
                'cash_balance': round(cash_balance, 2),
                'liability': round(liability, 2),
                'net_available': round(net_available, 2),
                'days_of_operation': round(days_of_operation, 1),
            }
        }
    
    @staticmethod
    def _calculate_daily_expense(db: Session, user_id: int, days: int = 30) -> float:
        """计算日均支出"""
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        total_expense = db.query(func.sum(CashTransaction.amount)).filter(
            and_(
                CashTransaction.user_id == user_id,
                CashTransaction.transaction_type == 'expense',
                CashTransaction.created_at >= start_date,
                CashTransaction.created_at <= end_date
            )
        ).scalar() or 0
        
        return float(total_expense) / days if days > 0 else 0
    
    @staticmethod
    def forecast_cash_flow(db: Session, user_id: int, days: int = 30) -> List[CashFlowForecast]:
        """
        预测未来现金流 - 使用移动平均法
        """
        end_date = date.today()
        start_date = end_date - timedelta(days=30)
        
        history = db.query(
            func.date(CashTransaction.created_at).label('date'),
            func.sum(case(
                (CashTransaction.transaction_type == 'income', CashTransaction.amount),
                else_=0
            )).label('income'),
            func.sum(case(
                (CashTransaction.transaction_type == 'expense', CashTransaction.amount),
                else_=0
            )).label('expense')
        ).filter(
            and_(
                CashTransaction.user_id == user_id,
                CashTransaction.created_at >= start_date
            )
        ).group_by(func.date(CashTransaction.created_at)).order_by('date').all()
        
        if len(history) < 7:
            return CashFlowService._simple_forecast(db, user_id, days)
        
        income_values = [float(h.income) for h in history]
        expense_values = [float(h.expense) for h in history]
        
        window = 7
        avg_income = np.mean(income_values[-window:])
        avg_expense = np.mean(expense_values[-window:])
        
        income_std = np.std(income_values[-window:]) if len(income_values) >= window else 0
        expense_std = np.std(expense_values[-window:]) if len(expense_values) >= window else 0
        
        cash_account = db.query(CashAccount).filter(
            CashAccount.user_id == user_id
        ).first()
        current_balance = float(cash_account.balance) if cash_account else 0
        
        forecasts = []
        predicted_balance = Decimal(str(current_balance))
        
        for i in range(1, days + 1):
            target_date = date.today() + timedelta(days=i)
            
            predicted_income = Decimal(str(round(avg_income, 2)))
            predicted_expense = Decimal(str(round(avg_expense, 2)))
            predicted_balance = predicted_balance + predicted_income - predicted_expense
            
            confidence = CashFlowService._calculate_confidence(income_std, expense_std, i)
            
            risk_alert = predicted_balance < 0
            alert_message = None
            if risk_alert:
                alert_message = f"预计{target_date}现金余额不足，请及时补充资金"
            
            forecast = CashFlowForecast(
                user_id=user_id,
                forecast_date=date.today(),
                target_date=target_date,
                predicted_income=predicted_income,
                predicted_expense=predicted_expense,
                predicted_balance=predicted_balance,
                confidence_level=Decimal(str(round(confidence, 2))),
                risk_alert=risk_alert,
                alert_message=alert_message
            )
            forecasts.append(forecast)
        
        db.add_all(forecasts)
        db.commit()
        
        return forecasts
    
    @staticmethod
    def _simple_forecast(db: Session, user_id: int, days: int) -> List[CashFlowForecast]:
        """简单预测（数据不足时使用）"""
        cash_account = db.query(CashAccount).filter(
            CashAccount.user_id == user_id
        ).first()
        current_balance = float(cash_account.balance) if cash_account else 0
        
        forecasts = []
        predicted_balance = Decimal(str(current_balance))
        
        for i in range(1, days + 1):
            target_date = date.today() + timedelta(days=i)
            
            forecast = CashFlowForecast(
                user_id=user_id,
                forecast_date=date.today(),
                target_date=target_date,
                predicted_income=Decimal('0'),
                predicted_expense=Decimal('0'),
                predicted_balance=predicted_balance,
                confidence_level=Decimal('50'),
                risk_alert=predicted_balance < 0,
                alert_message=None
            )
            forecasts.append(forecast)
        
        db.add_all(forecasts)
        db.commit()
        
        return forecasts
    
    @staticmethod
    def _calculate_confidence(income_std: float, expense_std: float, day: int) -> float:
        """计算预测置信度"""
        base_confidence = 85
        
        volatility_penalty = (income_std + expense_std) / 1000
        
        day_penalty = day * 0.5
        
        confidence = base_confidence - volatility_penalty - day_penalty
        return max(30, min(95, confidence))
    
    @staticmethod
    def analyze_cash_flow(
        db: Session, 
        user_id: int, 
        period_start: date, 
        period_end: date,
        analysis_type: str = 'monthly'
    ) -> CashFlowAnalysis:
        """
        分析指定周期的现金流
        """
        income_data = db.query(
            CashTransaction.category,
            func.sum(CashTransaction.amount).label('total')
        ).filter(
            and_(
                CashTransaction.user_id == user_id,
                CashTransaction.transaction_type == 'income',
                func.date(CashTransaction.created_at) >= period_start,
                func.date(CashTransaction.created_at) <= period_end
            )
        ).group_by(CashTransaction.category).all()
        
        expense_data = db.query(
            CashTransaction.category,
            func.sum(CashTransaction.amount).label('total')
        ).filter(
            and_(
                CashTransaction.user_id == user_id,
                CashTransaction.transaction_type == 'expense',
                func.date(CashTransaction.created_at) >= period_start,
                func.date(CashTransaction.created_at) <= period_end
            )
        ).group_by(CashTransaction.category).all()
        
        total_income = sum(float(item.total or 0) for item in income_data)
        total_expense = sum(float(item.total or 0) for item in expense_data)
        net_cash_flow = total_income - total_expense
        
        days = (period_end - period_start).days + 1
        avg_daily_income = total_income / days if days > 0 else 0
        avg_daily_expense = total_expense / days if days > 0 else 0
        
        income_structure = {item.category or '其他': float(item.total or 0) for item in income_data}
        expense_structure = {item.category or '其他': float(item.total or 0) for item in expense_data}
        
        health_score = CashFlowService._calculate_health_score(
            total_income, total_expense, net_cash_flow, avg_daily_income
        )
        
        risk_level = CashFlowService._assess_risk_level(net_cash_flow, health_score)
        
        recommendations = CashFlowService._generate_recommendations(
            income_structure, expense_structure, health_score, risk_level
        )
        
        analysis = CashFlowAnalysis(
            user_id=user_id,
            analysis_date=date.today(),
            analysis_type=analysis_type,
            period_start=period_start,
            period_end=period_end,
            total_income=Decimal(str(total_income)),
            total_expense=Decimal(str(total_expense)),
            net_cash_flow=Decimal(str(net_cash_flow)),
            avg_daily_income=Decimal(str(avg_daily_income)),
            avg_daily_expense=Decimal(str(avg_daily_expense)),
            income_structure=income_structure,
            expense_structure=expense_structure,
            health_score=Decimal(str(health_score)),
            risk_level=risk_level,
            recommendations=recommendations
        )
        
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        
        EventService.log_event(
            db=db,
            user_id=user_id,
            event_type='cash_flow_analysis',
            event_category='analysis',
            entity_type='cash_flow_analysis',
            entity_id=analysis.id,
            description=f'完成现金流分析: {period_start} 至 {period_end}',
            metadata={
                'total_income': float(total_income),
                'total_expense': float(total_expense),
                'health_score': float(health_score)
            }
        )
        
        return analysis
    
    @staticmethod
    def _calculate_health_score(
        total_income: float, 
        total_expense: float, 
        net_cash_flow: float,
        avg_daily_income: float
    ) -> float:
        """计算经营健康度评分 (0-100)"""
        score = 0.0
        
        if total_income > 0:
            profit_margin = net_cash_flow / total_income
            score += min(30, profit_margin * 100)
        
        if net_cash_flow > 0:
            score += 25
        elif net_cash_flow > -avg_daily_income:
            score += 15
        else:
            score += 5
        
        if avg_daily_income >= 1000:
            score += 25
        elif avg_daily_income >= 500:
            score += 20
        elif avg_daily_income >= 200:
            score += 15
        else:
            score += 10
        
        if total_income > 0:
            expense_ratio = total_expense / total_income
            if expense_ratio <= 0.5:
                score += 20
            elif expense_ratio <= 0.7:
                score += 15
            elif expense_ratio <= 0.9:
                score += 10
            else:
                score += 5
        
        return min(100, max(0, score))
    
    @staticmethod
    def _assess_risk_level(net_cash_flow: float, health_score: float) -> str:
        """评估风险等级"""
        if health_score >= 80 and net_cash_flow > 0:
            return 'low'
        elif health_score >= 60 and net_cash_flow >= 0:
            return 'medium'
        elif health_score >= 40 or net_cash_flow > -1000:
            return 'high'
        else:
            return 'critical'
    
    @staticmethod
    def _generate_recommendations(
        income_structure: Dict[str, float],
        expense_structure: Dict[str, float],
        health_score: float,
        risk_level: str
    ) -> List[str]:
        """生成优化建议"""
        recommendations = []
        
        if risk_level in ['high', 'critical']:
            recommendations.append('建议立即关注现金流状况，确保有足够的运营资金')
        
        if health_score < 60:
            recommendations.append('建议优化成本结构，减少非必要支出')
        
        if income_structure:
            max_income_category = max(income_structure, key=income_structure.get)
            if income_structure[max_income_category] / sum(income_structure.values()) > 0.8:
                recommendations.append(f'收入来源过于依赖{max_income_category}，建议拓展其他收入渠道')
        
        if expense_structure:
            max_expense_category = max(expense_structure, key=expense_structure.get)
            if sum(expense_structure.values()) > 0:
                if expense_structure[max_expense_category] / sum(expense_structure.values()) > 0.5:
                    recommendations.append(f'{max_expense_category}占比较高，建议评估是否可以优化')
        
        if not recommendations:
            recommendations.append('经营状况良好，继续保持')
        
        return recommendations
    
    @staticmethod
    def get_income_structure(
        db: Session, 
        user_id: int, 
        period_start: date, 
        period_end: date
    ) -> Dict[str, Any]:
        """获取收入结构分析"""
        income_by_category = db.query(
            CashTransaction.category,
            func.sum(CashTransaction.amount).label('total')
        ).filter(
            and_(
                CashTransaction.user_id == user_id,
                CashTransaction.transaction_type == 'income',
                func.date(CashTransaction.created_at) >= period_start,
                func.date(CashTransaction.created_at) <= period_end
            )
        ).group_by(CashTransaction.category).all()
        
        income_by_mode = db.query(
            Order.order_type,
            func.sum(Order.amount).label('total')
        ).filter(
            and_(
                Order.user_id == user_id,
                func.date(Order.created_at) >= period_start,
                func.date(Order.created_at) <= period_end,
                Order.status != 'cancelled'
            )
        ).group_by(Order.order_type).all()
        
        daily_income = db.query(
            func.date(CashTransaction.created_at).label('date'),
            func.sum(CashTransaction.amount).label('total')
        ).filter(
            and_(
                CashTransaction.user_id == user_id,
                CashTransaction.transaction_type == 'income',
                func.date(CashTransaction.created_at) >= period_start,
                func.date(CashTransaction.created_at) <= period_end
            )
        ).group_by(func.date(CashTransaction.created_at)).order_by('date').all()
        
        income_trend = [
            {'date': str(item.date), 'amount': float(item.total or 0)}
            for item in daily_income
        ]
        
        total_income = sum(float(item.total or 0) for item in income_by_category)
        
        values = [float(item.total or 0) for item in daily_income]
        stability_score = 100 - (np.std(values) / np.mean(values) * 100) if values and np.mean(values) > 0 else 100
        stability_score = max(0, min(100, stability_score))
        
        prev_start = period_start - (period_end - period_start) - timedelta(days=1)
        prev_end = period_start - timedelta(days=1)
        
        prev_total = db.query(func.sum(CashTransaction.amount)).filter(
            and_(
                CashTransaction.user_id == user_id,
                CashTransaction.transaction_type == 'income',
                func.date(CashTransaction.created_at) >= prev_start,
                func.date(CashTransaction.created_at) <= prev_end
            )
        ).scalar() or 0
        
        growth_rate = None
        if prev_total > 0:
            growth_rate = ((total_income - float(prev_total)) / float(prev_total)) * 100
        
        return {
            'total_income': Decimal(str(total_income)),
            'income_by_category': {item.category or '其他': Decimal(str(item.total or 0)) for item in income_by_category},
            'income_by_mode': {item.income_mode or '其他': Decimal(str(item.total or 0)) for item in income_by_mode},
            'income_trend': income_trend,
            'stability_score': round(stability_score, 1),
            'growth_rate': round(growth_rate, 1) if growth_rate is not None else None
        }
    
    @staticmethod
    def get_expense_structure(
        db: Session, 
        user_id: int, 
        period_start: date, 
        period_end: date
    ) -> Dict[str, Any]:
        """获取成本结构分析"""
        expense_by_category = db.query(
            CashTransaction.category,
            func.sum(CashTransaction.amount).label('total')
        ).filter(
            and_(
                CashTransaction.user_id == user_id,
                CashTransaction.transaction_type == 'expense',
                func.date(CashTransaction.created_at) >= period_start,
                func.date(CashTransaction.created_at) <= period_end
            )
        ).group_by(CashTransaction.category).all()
        
        expense_records = db.query(ExpenseRecord).filter(
            and_(
                ExpenseRecord.user_id == user_id,
                func.date(ExpenseRecord.expense_date) >= period_start,
                func.date(ExpenseRecord.expense_date) <= period_end
            )
        ).all()
        
        expense_by_behavior = {}
        expense_by_function = {}
        for record in expense_records:
            behavior = record.cost_behavior or '其他'
            function = record.cost_function or '其他'
            expense_by_behavior[behavior] = expense_by_behavior.get(behavior, 0) + float(record.amount or 0)
            expense_by_function[function] = expense_by_function.get(function, 0) + float(record.amount or 0)
        
        daily_expense = db.query(
            func.date(CashTransaction.created_at).label('date'),
            func.sum(CashTransaction.amount).label('total')
        ).filter(
            and_(
                CashTransaction.user_id == user_id,
                CashTransaction.transaction_type == 'expense',
                func.date(CashTransaction.created_at) >= period_start,
                func.date(CashTransaction.created_at) <= period_end
            )
        ).group_by(func.date(CashTransaction.created_at)).order_by('date').all()
        
        expense_trend = [
            {'date': str(item.date), 'amount': float(item.total or 0)}
            for item in daily_expense
        ]
        
        total_expense = sum(float(item.total or 0) for item in expense_by_category)
        
        anomaly_detected = False
        if len(expense_trend) >= 7:
            values = [item['amount'] for item in expense_trend[-7:]]
            mean = np.mean(values)
            std = np.std(values)
            if std > 0 and (values[-1] - mean) / std > 2:
                anomaly_detected = True
        
        return {
            'total_expense': Decimal(str(total_expense)),
            'expense_by_category': {item.category or '其他': Decimal(str(item.total or 0)) for item in expense_by_category},
            'expense_by_behavior': {k: Decimal(str(v)) for k, v in expense_by_behavior.items()},
            'expense_by_function': {k: Decimal(str(v)) for k, v in expense_by_function.items()},
            'expense_trend': expense_trend,
            'anomaly_detected': anomaly_detected
        }
    
    @staticmethod
    def calculate_break_even(db: Session, user_id: int) -> Dict[str, Any]:
        """计算盈亏平衡点"""
        today = date.today()
        month_start = date(today.year, today.month, 1)
        
        expense_records = db.query(ExpenseRecord).filter(
            and_(
                ExpenseRecord.user_id == user_id,
                ExpenseRecord.expense_date >= month_start
            )
        ).all()
        
        fixed_cost = sum(
            float(r.amount or 0) for r in expense_records 
            if r.cost_behavior == 'fixed'
        )
        
        variable_cost = sum(
            float(r.amount or 0) for r in expense_records 
            if r.cost_behavior == 'variable'
        )
        
        total_revenue = db.query(func.sum(CashTransaction.amount)).filter(
            and_(
                CashTransaction.user_id == user_id,
                CashTransaction.transaction_type == 'income',
                func.date(CashTransaction.created_at) >= month_start
            )
        ).scalar() or 0
        
        current_revenue = float(total_revenue)
        
        variable_cost_ratio = variable_cost / current_revenue if current_revenue > 0 else 0.5
        
        contribution_margin_ratio = 1 - variable_cost_ratio
        
        if contribution_margin_ratio > 0:
            break_even_point = fixed_cost / contribution_margin_ratio
        else:
            break_even_point = fixed_cost
        
        safety_margin = current_revenue - break_even_point
        safety_margin_ratio = (safety_margin / current_revenue * 100) if current_revenue > 0 else 0
        
        if safety_margin > 0:
            status = 'profit'
        elif safety_margin < 0:
            status = 'loss'
        else:
            status = 'break_even'
        
        return {
            'break_even_point': Decimal(str(round(break_even_point, 2))),
            'current_revenue': Decimal(str(round(current_revenue, 2))),
            'fixed_cost': Decimal(str(round(fixed_cost, 2))),
            'variable_cost_ratio': round(variable_cost_ratio * 100, 1),
            'contribution_margin_ratio': round(contribution_margin_ratio * 100, 1),
            'safety_margin': Decimal(str(round(safety_margin, 2))),
            'safety_margin_ratio': round(safety_margin_ratio, 1),
            'status': status
        }
    
    @staticmethod
    def generate_monthly_report(
        db: Session, 
        user_id: int, 
        year: int, 
        month: int
    ) -> Dict[str, Any]:
        """生成月度健康报告"""
        period_start = date(year, month, 1)
        if month == 12:
            period_end = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            period_end = date(year, month + 1, 1) - timedelta(days=1)
        
        analysis = CashFlowService.analyze_cash_flow(
            db, user_id, period_start, period_end, 'monthly'
        )
        
        income_structure = CashFlowService.get_income_structure(
            db, user_id, period_start, period_end
        )
        
        expense_structure = CashFlowService.get_expense_structure(
            db, user_id, period_start, period_end
        )
        
        break_even = CashFlowService.calculate_break_even(db, user_id)
        
        safety_index = CashFlowService.calculate_safety_index(db, user_id)
        
        recommendations = analysis.recommendations or []
        
        action_items = []
        if safety_index['safety_level'] == SafetyLevel.DANGER:
            action_items.append('立即补充运营资金')
            action_items.append('暂停非必要支出')
        elif safety_index['safety_level'] == SafetyLevel.WARNING:
            action_items.append('关注现金流变化')
            action_items.append('优化应收账款')
        
        if break_even['status'] == 'loss':
            action_items.append('分析亏损原因')
            action_items.append('制定增收节支计划')
        
        comparison = None
        if month > 1:
            prev_month = month - 1
            prev_year = year
        else:
            prev_month = 12
            prev_year = year - 1
        
        prev_start = date(prev_year, prev_month, 1)
        if prev_month == 12:
            prev_end = date(prev_year + 1, 1, 1) - timedelta(days=1)
        else:
            prev_end = date(prev_year, prev_month + 1, 1) - timedelta(days=1)
        
        prev_snapshot = db.query(FinancialSnapshot).filter(
            and_(
                FinancialSnapshot.user_id == user_id,
                FinancialSnapshot.snapshot_date == prev_end
            )
        ).first()
        
        curr_snapshot = db.query(FinancialSnapshot).filter(
            and_(
                FinancialSnapshot.user_id == user_id,
                FinancialSnapshot.snapshot_date == period_end
            )
        ).first()
        
        if prev_snapshot and curr_snapshot:
            comparison = {
                'cash_balance_change': float(curr_snapshot.cash_balance - prev_snapshot.cash_balance),
                'inventory_value_change': float(curr_snapshot.inventory_value - prev_snapshot.inventory_value),
                'prepaid_balance_change': float(curr_snapshot.prepaid_balance - prev_snapshot.prepaid_balance),
            }
        
        return {
            'year': year,
            'month': month,
            'period_start': period_start,
            'period_end': period_end,
            'total_income': analysis.total_income,
            'total_expense': analysis.total_expense,
            'net_cash_flow': analysis.net_cash_flow,
            'income_structure': income_structure,
            'expense_structure': expense_structure,
            'break_even': break_even,
            'safety_index': safety_index,
            'health_score': float(analysis.health_score),
            'risk_level': analysis.risk_level,
            'recommendations': recommendations,
            'action_items': action_items,
            'comparison': comparison
        }
    
    @staticmethod
    def analyze_income_volatility(db: Session, user_id: int) -> Dict[str, Any]:
        """分析收入波动归因"""
        today = date.today()
        period_start = today - timedelta(days=30)
        period_end = today
        
        daily_income = db.query(
            func.date(CashTransaction.created_at).label('date'),
            func.sum(CashTransaction.amount).label('total')
        ).filter(
            and_(
                CashTransaction.user_id == user_id,
                CashTransaction.transaction_type == 'income',
                func.date(CashTransaction.created_at) >= period_start,
                func.date(CashTransaction.created_at) <= period_end
            )
        ).group_by(func.date(CashTransaction.created_at)).order_by('date').all()
        
        if len(daily_income) < 7:
            return {
                'volatility_score': 0,
                'trend': 'stable',
                'change_percentage': 0,
                'factors': [],
                'main_cause': '数据不足，无法分析',
                'suggestions': ['建议积累更多数据后再进行分析']
            }
        
        values = [float(item.total or 0) for item in daily_income]
        
        volatility_score = (np.std(values) / np.mean(values) * 100) if np.mean(values) > 0 else 0
        
        first_half = values[:len(values)//2]
        second_half = values[len(values)//2:]
        
        first_avg = np.mean(first_half)
        second_avg = np.mean(second_half)
        
        if first_avg > 0:
            change_percentage = ((second_avg - first_avg) / first_avg) * 100
        else:
            change_percentage = 0
        
        if change_percentage > 10:
            trend = 'up'
        elif change_percentage < -10:
            trend = 'down'
        else:
            trend = 'stable'
        
        income_by_category = db.query(
            CashTransaction.category,
            func.sum(CashTransaction.amount).label('total')
        ).filter(
            and_(
                CashTransaction.user_id == user_id,
                CashTransaction.transaction_type == 'income',
                func.date(CashTransaction.created_at) >= period_start
            )
        ).group_by(CashTransaction.category).all()
        
        factors = []
        for item in income_by_category:
            category = item.category or '其他'
            amount = float(item.total or 0)
            factors.append({
                'category': category,
                'amount': amount,
                'percentage': round(amount / sum(values) * 100, 1) if sum(values) > 0 else 0
            })
        
        main_cause = '整体市场变化'
        if factors:
            main_factor = max(factors, key=lambda x: x['amount'])
            main_cause = f"{main_factor['category']}收入变化"
        
        suggestions = []
        if trend == 'down':
            suggestions.append('建议分析收入下降的具体原因')
            suggestions.append('考虑推出促销活动增加收入')
            suggestions.append('拓展新的收入渠道')
        elif trend == 'up':
            suggestions.append('保持当前经营策略')
            suggestions.append('考虑扩大经营规模')
        else:
            suggestions.append('收入稳定，继续保持')
        
        return {
            'volatility_score': round(volatility_score, 1),
            'trend': trend,
            'change_percentage': round(change_percentage, 1),
            'factors': factors,
            'main_cause': main_cause,
            'suggestions': suggestions
        }
    
    @staticmethod
    def get_dashboard_data(db: Session, user_id: int) -> Dict[str, Any]:
        """
        获取仪表盘数据
        """
        safety_index = CashFlowService.calculate_safety_index(db, user_id)
        
        cash_account = db.query(CashAccount).filter(
            CashAccount.user_id == user_id
        ).first()
        current_balance = Decimal('0')
        if cash_account:
            current_balance = cash_account.balance or Decimal('0')
        
        today = date.today()
        yesterday = today - timedelta(days=1)
        
        yesterday_income = db.query(func.sum(CashTransaction.amount)).filter(
            and_(
                CashTransaction.user_id == user_id,
                CashTransaction.transaction_type == 'income',
                func.date(CashTransaction.created_at) == yesterday
            )
        ).scalar() or 0
        
        yesterday_expense = db.query(func.sum(CashTransaction.amount)).filter(
            and_(
                CashTransaction.user_id == user_id,
                CashTransaction.transaction_type == 'expense',
                func.date(CashTransaction.created_at) == yesterday
            )
        ).scalar() or 0
        
        yesterday_change = Decimal(str(float(yesterday_income) - float(yesterday_expense)))
        
        month_start = date(today.year, today.month, 1)
        
        monthly_income = db.query(func.sum(CashTransaction.amount)).filter(
            and_(
                CashTransaction.user_id == user_id,
                CashTransaction.transaction_type == 'income',
                func.date(CashTransaction.created_at) >= month_start
            )
        ).scalar() or 0
        
        monthly_expense = db.query(func.sum(CashTransaction.amount)).filter(
            and_(
                CashTransaction.user_id == user_id,
                CashTransaction.transaction_type == 'expense',
                func.date(CashTransaction.created_at) >= month_start
            )
        ).scalar() or 0
        
        monthly_profit = Decimal(str(float(monthly_income) - float(monthly_expense)))
        
        recent_start = today - timedelta(days=7)
        recent_trend = db.query(
            func.date(CashTransaction.created_at).label('date'),
            func.sum(case(
                (CashTransaction.transaction_type == 'income', CashTransaction.amount),
                else_=0
            )).label('income'),
            func.sum(case(
                (CashTransaction.transaction_type == 'expense', CashTransaction.amount),
                else_=0
            )).label('expense')
        ).filter(
            and_(
                CashTransaction.user_id == user_id,
                func.date(CashTransaction.created_at) >= recent_start
            )
        ).group_by(func.date(CashTransaction.created_at)).order_by('date').all()
        
        recent_trend_data = [
            {
                'date': str(item.date),
                'income': float(item.income or 0),
                'expense': float(item.expense or 0)
            }
            for item in recent_trend
        ]
        
        from app.models.cash_flow import RiskAlert
        active_alerts = db.query(RiskAlert).filter(
            and_(
                RiskAlert.user_id == user_id,
                RiskAlert.is_resolved == False
            )
        ).order_by(RiskAlert.created_at.desc()).limit(5).all()
        
        active_alerts_data = [
            {
                'id': alert.id,
                'alert_level': alert.alert_level,
                'alert_type': alert.alert_type,
                'message': alert.message,
                'created_at': str(alert.created_at)
            }
            for alert in active_alerts
        ]
        
        forecasts = CashFlowService.forecast_cash_flow(db, user_id, days=7)
        
        forecast_summary = {
            'has_risk': any(f.risk_alert for f in forecasts),
            'predicted_balance_end': float(forecasts[-1].predicted_balance) if forecasts else 0,
            'avg_daily_income': float(sum(f.predicted_income for f in forecasts) / len(forecasts)) if forecasts else 0,
            'avg_daily_expense': float(sum(f.predicted_expense for f in forecasts) / len(forecasts)) if forecasts else 0,
        }
        
        return {
            'safety_index': safety_index,
            'current_balance': current_balance,
            'yesterday_change': yesterday_change,
            'monthly_income': Decimal(str(monthly_income)),
            'monthly_expense': Decimal(str(monthly_expense)),
            'monthly_profit': monthly_profit,
            'recent_trend': recent_trend_data,
            'active_alerts': active_alerts_data,
            'forecast_summary': forecast_summary
        }
