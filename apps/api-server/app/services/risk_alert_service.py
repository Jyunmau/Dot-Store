"""
Dot-Store V2.2 风险预警服务
实现风险检测、预警生成、预警管理等功能
"""
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_

from app.models.cash_flow import RiskAlert, CashFlowForecast
from app.models.cash_account import CashAccount, CashTransaction
from app.models.customer_account import CustomerAccount
from app.models.expense_record import ExpenseRecord
from app.models.user_preference import UserPreference
from app.services.event_service import EventService


class AlertLevel:
    """预警等级"""
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    CRITICAL = 'critical'
    
    LABELS = {
        LOW: '低风险',
        MEDIUM: '中风险',
        HIGH: '高风险',
        CRITICAL: '严重风险',
    }
    
    COLORS = {
        LOW: '#52C41A',
        MEDIUM: '#FAAD14',
        HIGH: '#FA541C',
        CRITICAL: '#F5222D',
    }


class AlertType:
    """预警类型"""
    CASH_SHORTAGE = 'cash_shortage'
    NEGATIVE_BALANCE = 'negative_balance'
    HIGH_EXPENSE = 'high_expense'
    LOW_INCOME = 'low_income'
    RECEIVABLE_OVERDUE = 'receivable_overdue'
    BREAK_EVEN_RISK = 'break_even_risk'
    FORECAST_RISK = 'forecast_risk'
    
    LABELS = {
        CASH_SHORTAGE: '现金不足',
        NEGATIVE_BALANCE: '余额为负',
        HIGH_EXPENSE: '支出过高',
        LOW_INCOME: '收入过低',
        RECEIVABLE_OVERDUE: '应收账款逾期',
        BREAK_EVEN_RISK: '盈亏平衡风险',
        FORECAST_RISK: '预测风险',
    }


class RiskAlertService:
    """风险预警服务"""
    
    @staticmethod
    def check_all_risks(db: Session, user_id: int) -> List[RiskAlert]:
        """
        检查所有风险并生成预警
        """
        alerts = []
        
        cash_alert = RiskAlertService._check_cash_shortage(db, user_id)
        if cash_alert:
            alerts.append(cash_alert)
        
        balance_alert = RiskAlertService._check_negative_balance(db, user_id)
        if balance_alert:
            alerts.append(balance_alert)
        
        expense_alert = RiskAlertService._check_high_expense(db, user_id)
        if expense_alert:
            alerts.append(expense_alert)
        
        income_alert = RiskAlertService._check_low_income(db, user_id)
        if income_alert:
            alerts.append(income_alert)
        
        receivable_alert = RiskAlertService._check_receivable_overdue(db, user_id)
        if receivable_alert:
            alerts.append(receivable_alert)
        
        forecast_alert = RiskAlertService._check_forecast_risk(db, user_id)
        if forecast_alert:
            alerts.append(forecast_alert)
        
        for alert in alerts:
            db.add(alert)
        
        if alerts:
            db.commit()
        
        return alerts
    
    @staticmethod
    def _check_cash_shortage(db: Session, user_id: int) -> Optional[RiskAlert]:
        """
        检查现金不足风险
        """
        cash_account = db.query(CashAccount).filter(
            CashAccount.user_id == user_id
        ).first()
        
        if not cash_account:
            return None
        
        balance = float(cash_account.balance or 0)
        
        liability = db.query(func.sum(CustomerAccount.balance)).filter(
            CustomerAccount.user_id == user_id
        ).scalar() or 0
        liability = float(liability)
        
        net_available = balance - liability
        
        end_date = date.today()
        start_date = end_date - timedelta(days=30)
        
        total_expense = db.query(func.sum(CashTransaction.amount)).filter(
            and_(
                CashTransaction.user_id == user_id,
                CashTransaction.transaction_type == 'expense',
                CashTransaction.created_at >= start_date
            )
        ).scalar() or 0
        
        daily_expense = float(total_expense) / 30
        
        if daily_expense > 0:
            days_of_operation = net_available / daily_expense
        else:
            days_of_operation = 999 if net_available > 0 else 0
        
        existing_alert = db.query(RiskAlert).filter(
            and_(
                RiskAlert.user_id == user_id,
                RiskAlert.alert_type == AlertType.CASH_SHORTAGE,
                RiskAlert.is_resolved == False,
                RiskAlert.alert_date == date.today()
            )
        ).first()
        
        if existing_alert:
            return None
        
        if days_of_operation < 7:
            level = AlertLevel.CRITICAL
            message = f"可用现金仅够运营{days_of_operation:.1f}天，请立即补充资金"
            suggestions = [
                "立即安排资金补充",
                "暂停非必要支出",
                "加速应收账款回收",
            ]
        elif days_of_operation < 14:
            level = AlertLevel.HIGH
            message = f"可用现金仅够运营{days_of_operation:.1f}天，建议关注现金流"
            suggestions = [
                "关注现金流变化",
                "优化支出结构",
                "提前安排资金",
            ]
        elif days_of_operation < 30:
            level = AlertLevel.MEDIUM
            message = f"可用现金可运营{days_of_operation:.1f}天，建议关注"
            suggestions = [
                "定期检查现金流",
                "保持合理现金储备",
            ]
        else:
            return None
        
        return RiskAlert(
            user_id=user_id,
            alert_date=date.today(),
            alert_level=level,
            alert_type=AlertType.CASH_SHORTAGE,
            message=message,
            suggestions=suggestions
        )
    
    @staticmethod
    def _check_negative_balance(db: Session, user_id: int) -> Optional[RiskAlert]:
        """
        检查余额为负风险
        """
        cash_account = db.query(CashAccount).filter(
            CashAccount.user_id == user_id
        ).first()
        
        if not cash_account:
            return None
        
        balance = float(cash_account.balance or 0)
        
        existing_alert = db.query(RiskAlert).filter(
            and_(
                RiskAlert.user_id == user_id,
                RiskAlert.alert_type == AlertType.NEGATIVE_BALANCE,
                RiskAlert.is_resolved == False,
                RiskAlert.alert_date == date.today()
            )
        ).first()
        
        if existing_alert:
            return None
        
        if balance < 0:
            return RiskAlert(
                user_id=user_id,
                alert_date=date.today(),
                alert_level=AlertLevel.CRITICAL,
                alert_type=AlertType.NEGATIVE_BALANCE,
                message=f"现金账户余额为负({balance:.2f})，请立即处理",
                suggestions=[
                    "立即补充账户资金",
                    "检查是否有错误的支出记录",
                    "联系客户催收欠款",
                ]
            )
        
        return None
    
    @staticmethod
    def _check_high_expense(db: Session, user_id: int) -> Optional[RiskAlert]:
        """
        检查支出过高风险
        """
        today = date.today()
        month_start = date(today.year, today.month, 1)
        
        current_expense = db.query(func.sum(CashTransaction.amount)).filter(
            and_(
                CashTransaction.user_id == user_id,
                CashTransaction.transaction_type == 'expense',
                func.date(CashTransaction.created_at) >= month_start
            )
        ).scalar() or 0
        current_expense = float(current_expense)
        
        if today.month == 1:
            prev_month = 12
            prev_year = today.year - 1
        else:
            prev_month = today.month - 1
            prev_year = today.year
        
        prev_month_start = date(prev_year, prev_month, 1)
        if prev_month == 12:
            prev_month_end = date(prev_year + 1, 1, 1) - timedelta(days=1)
        else:
            prev_month_end = date(prev_year, prev_month + 1, 1) - timedelta(days=1)
        
        prev_expense = db.query(func.sum(CashTransaction.amount)).filter(
            and_(
                CashTransaction.user_id == user_id,
                CashTransaction.transaction_type == 'expense',
                func.date(CashTransaction.created_at) >= prev_month_start,
                func.date(CashTransaction.created_at) <= prev_month_end
            )
        ).scalar() or 0
        prev_expense = float(prev_expense)
        
        existing_alert = db.query(RiskAlert).filter(
            and_(
                RiskAlert.user_id == user_id,
                RiskAlert.alert_type == AlertType.HIGH_EXPENSE,
                RiskAlert.is_resolved == False,
                RiskAlert.alert_date == date.today()
            )
        ).first()
        
        if existing_alert:
            return None
        
        if prev_expense > 0:
            increase_ratio = (current_expense - prev_expense) / prev_expense * 100
            
            if increase_ratio > 50:
                return RiskAlert(
                    user_id=user_id,
                    alert_date=date.today(),
                    alert_level=AlertLevel.HIGH,
                    alert_type=AlertType.HIGH_EXPENSE,
                    message=f"本月支出较上月增长{increase_ratio:.1f}%，请关注支出情况",
                    suggestions=[
                        "分析支出增长原因",
                        "审查非必要支出",
                        "制定成本控制计划",
                    ]
                )
            elif increase_ratio > 30:
                return RiskAlert(
                    user_id=user_id,
                    alert_date=date.today(),
                    alert_level=AlertLevel.MEDIUM,
                    alert_type=AlertType.HIGH_EXPENSE,
                    message=f"本月支出较上月增长{increase_ratio:.1f}%，建议关注",
                    suggestions=[
                        "检查支出明细",
                        "评估支出必要性",
                    ]
                )
        
        return None
    
    @staticmethod
    def _check_low_income(db: Session, user_id: int) -> Optional[RiskAlert]:
        """
        检查收入过低风险
        """
        today = date.today()
        month_start = date(today.year, today.month, 1)
        
        current_income = db.query(func.sum(CashTransaction.amount)).filter(
            and_(
                CashTransaction.user_id == user_id,
                CashTransaction.transaction_type == 'income',
                func.date(CashTransaction.created_at) >= month_start
            )
        ).scalar() or 0
        current_income = float(current_income)
        
        if today.month == 1:
            prev_month = 12
            prev_year = today.year - 1
        else:
            prev_month = today.month - 1
            prev_year = today.year
        
        prev_month_start = date(prev_year, prev_month, 1)
        if prev_month == 12:
            prev_month_end = date(prev_year + 1, 1, 1) - timedelta(days=1)
        else:
            prev_month_end = date(prev_year, prev_month + 1, 1) - timedelta(days=1)
        
        prev_income = db.query(func.sum(CashTransaction.amount)).filter(
            and_(
                CashTransaction.user_id == user_id,
                CashTransaction.transaction_type == 'income',
                func.date(CashTransaction.created_at) >= prev_month_start,
                func.date(CashTransaction.created_at) <= prev_month_end
            )
        ).scalar() or 0
        prev_income = float(prev_income)
        
        existing_alert = db.query(RiskAlert).filter(
            and_(
                RiskAlert.user_id == user_id,
                RiskAlert.alert_type == AlertType.LOW_INCOME,
                RiskAlert.is_resolved == False,
                RiskAlert.alert_date == date.today()
            )
        ).first()
        
        if existing_alert:
            return None
        
        if prev_income > 0:
            decrease_ratio = (prev_income - current_income) / prev_income * 100
            
            if decrease_ratio > 50:
                return RiskAlert(
                    user_id=user_id,
                    alert_date=date.today(),
                    alert_level=AlertLevel.HIGH,
                    alert_type=AlertType.LOW_INCOME,
                    message=f"本月收入较上月下降{decrease_ratio:.1f}%，请关注收入情况",
                    suggestions=[
                        "分析收入下降原因",
                        "考虑推出促销活动",
                        "拓展新的收入渠道",
                    ]
                )
            elif decrease_ratio > 30:
                return RiskAlert(
                    user_id=user_id,
                    alert_date=date.today(),
                    alert_level=AlertLevel.MEDIUM,
                    alert_type=AlertType.LOW_INCOME,
                    message=f"本月收入较上月下降{decrease_ratio:.1f}%，建议关注",
                    suggestions=[
                        "检查收入来源",
                        "分析市场变化",
                    ]
                )
        
        return None
    
    @staticmethod
    def _check_receivable_overdue(db: Session, user_id: int) -> Optional[RiskAlert]:
        """
        检查应收账款逾期风险
        """
        overdue_accounts = db.query(CustomerAccount).filter(
            and_(
                CustomerAccount.user_id == user_id,
                CustomerAccount.balance > 0,
                CustomerAccount.status == 'overdue'
            )
        ).all()
        
        existing_alert = db.query(RiskAlert).filter(
            and_(
                RiskAlert.user_id == user_id,
                RiskAlert.alert_type == AlertType.RECEIVABLE_OVERDUE,
                RiskAlert.is_resolved == False,
                RiskAlert.alert_date == date.today()
            )
        ).first()
        
        if existing_alert:
            return None
        
        if overdue_accounts:
            total_overdue = sum(float(a.balance or 0) for a in overdue_accounts)
            count = len(overdue_accounts)
            
            return RiskAlert(
                user_id=user_id,
                alert_date=date.today(),
                alert_level=AlertLevel.MEDIUM,
                alert_type=AlertType.RECEIVABLE_OVERDUE,
                message=f"有{count}笔应收账款逾期，总计{total_overdue:.2f}元",
                suggestions=[
                    "联系客户催收欠款",
                    "考虑提供分期付款方案",
                    "评估客户信用风险",
                ]
            )
        
        return None
    
    @staticmethod
    def _check_forecast_risk(db: Session, user_id: int) -> Optional[RiskAlert]:
        """
        检查预测风险
        """
        today = date.today()
        
        risky_forecasts = db.query(CashFlowForecast).filter(
            and_(
                CashFlowForecast.user_id == user_id,
                CashFlowForecast.target_date >= today,
                CashFlowForecast.target_date <= today + timedelta(days=7),
                CashFlowForecast.risk_alert == True
            )
        ).order_by(CashFlowForecast.target_date).all()
        
        existing_alert = db.query(RiskAlert).filter(
            and_(
                RiskAlert.user_id == user_id,
                RiskAlert.alert_type == AlertType.FORECAST_RISK,
                RiskAlert.is_resolved == False,
                RiskAlert.alert_date == date.today()
            )
        ).first()
        
        if existing_alert:
            return None
        
        if risky_forecasts:
            first_risk = risky_forecasts[0]
            return RiskAlert(
                user_id=user_id,
                alert_date=date.today(),
                alert_level=AlertLevel.HIGH,
                alert_type=AlertType.FORECAST_RISK,
                message=f"预计{first_risk.target_date}现金余额不足，请提前安排",
                suggestions=[
                    "提前安排资金补充",
                    "调整支出计划",
                    "加速应收账款回收",
                ]
            )
        
        return None
    
    @staticmethod
    def get_alerts(
        db: Session, 
        user_id: int, 
        include_resolved: bool = False,
        level: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Tuple[List[RiskAlert], int]:
        """
        获取预警列表
        """
        query = db.query(RiskAlert).filter(RiskAlert.user_id == user_id)
        
        if not include_resolved:
            query = query.filter(RiskAlert.is_resolved == False)
        
        if level:
            query = query.filter(RiskAlert.alert_level == level)
        
        total = query.count()
        
        alerts = query.order_by(
            RiskAlert.is_read.asc(),
            RiskAlert.created_at.desc()
        ).offset(offset).limit(limit).all()
        
        return alerts, total
    
    @staticmethod
    def get_alert_stats(db: Session, user_id: int) -> Dict[str, Any]:
        """
        获取预警统计
        """
        total_alerts = db.query(RiskAlert).filter(
            RiskAlert.user_id == user_id
        ).count()
        
        unread_count = db.query(RiskAlert).filter(
            and_(
                RiskAlert.user_id == user_id,
                RiskAlert.is_read == False
            )
        ).count()
        
        resolved_count = db.query(RiskAlert).filter(
            and_(
                RiskAlert.user_id == user_id,
                RiskAlert.is_resolved == True
            )
        ).count()
        
        by_level = {}
        for level in [AlertLevel.LOW, AlertLevel.MEDIUM, AlertLevel.HIGH, AlertLevel.CRITICAL]:
            count = db.query(RiskAlert).filter(
                and_(
                    RiskAlert.user_id == user_id,
                    RiskAlert.alert_level == level,
                    RiskAlert.is_resolved == False
                )
            ).count()
            by_level[level] = count
        
        by_type = {}
        for alert_type in [
            AlertType.CASH_SHORTAGE,
            AlertType.NEGATIVE_BALANCE,
            AlertType.HIGH_EXPENSE,
            AlertType.LOW_INCOME,
            AlertType.RECEIVABLE_OVERDUE,
            AlertType.FORECAST_RISK,
        ]:
            count = db.query(RiskAlert).filter(
                and_(
                    RiskAlert.user_id == user_id,
                    RiskAlert.alert_type == alert_type,
                    RiskAlert.is_resolved == False
                )
            ).count()
            by_type[alert_type] = count
        
        recent_alerts = db.query(RiskAlert).filter(
            RiskAlert.user_id == user_id
        ).order_by(RiskAlert.created_at.desc()).limit(5).all()
        
        return {
            'total_alerts': total_alerts,
            'unread_count': unread_count,
            'resolved_count': resolved_count,
            'by_level': by_level,
            'by_type': by_type,
            'recent_alerts': recent_alerts
        }
    
    @staticmethod
    def mark_as_read(db: Session, user_id: int, alert_id: int) -> Optional[RiskAlert]:
        """
        标记预警为已读
        """
        alert = db.query(RiskAlert).filter(
            and_(
                RiskAlert.id == alert_id,
                RiskAlert.user_id == user_id
            )
        ).first()
        
        if alert:
            alert.is_read = True
            db.commit()
            db.refresh(alert)
        
        return alert
    
    @staticmethod
    def mark_all_as_read(db: Session, user_id: int) -> int:
        """
        标记所有预警为已读
        """
        result = db.query(RiskAlert).filter(
            and_(
                RiskAlert.user_id == user_id,
                RiskAlert.is_read == False
            )
        ).update({'is_read': True})
        
        db.commit()
        return result
    
    @staticmethod
    def resolve_alert(
        db: Session, 
        user_id: int, 
        alert_id: int,
        resolution_note: Optional[str] = None
    ) -> Optional[RiskAlert]:
        """
        解决预警
        """
        alert = db.query(RiskAlert).filter(
            and_(
                RiskAlert.id == alert_id,
                RiskAlert.user_id == user_id
            )
        ).first()
        
        if alert:
            alert.is_resolved = True
            alert.resolved_at = datetime.utcnow()
            db.commit()
            db.refresh(alert)
            
            EventService.log_event(
                db=db,
                user_id=user_id,
                event_type='risk_alert_resolved',
                event_category='alert',
                entity_type='risk_alert',
                entity_id=alert.id,
                description=f'已解决风险预警: {alert.message}',
                metadata={
                    'alert_level': alert.alert_level,
                    'alert_type': alert.alert_type,
                    'resolution_note': resolution_note
                }
            )
        
        return alert
    
    @staticmethod
    def get_user_preference(db: Session, user_id: int) -> Optional[UserPreference]:
        """
        获取用户预警偏好设置
        """
        return db.query(UserPreference).filter(
            UserPreference.user_id == user_id
        ).first()
    
    @staticmethod
    def should_send_alert(db: Session, user_id: int, alert: RiskAlert) -> bool:
        """
        判断是否应该发送预警通知
        """
        preference = RiskAlertService.get_user_preference(db, user_id)
        
        if not preference:
            return True
        
        if not preference.risk_alert_enabled:
            return False
        
        threshold = preference.risk_alert_threshold
        
        level_priority = {
            AlertLevel.LOW: 1,
            AlertLevel.MEDIUM: 2,
            AlertLevel.HIGH: 3,
            AlertLevel.CRITICAL: 4,
        }
        
        threshold_priority = {
            'low': 1,
            'medium': 2,
            'high': 3,
        }
        
        return level_priority.get(alert.alert_level, 0) >= threshold_priority.get(threshold, 0)
