"""
Dot-Store V2.2 定时任务调度器
"""
from datetime import datetime, date, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session

from ..core.database import SessionLocal
from ..services.financial_snapshot_service import FinancialSnapshotService
from ..services.cash_flow_service import CashFlowService
from ..services.risk_alert_service import RiskAlertService
from ..models.user import User


scheduler = AsyncIOScheduler()


def get_all_active_users(db: Session) -> list:
    """
    获取所有活跃用户
    """
    return db.query(User).filter(User.is_active == True).all()


async def generate_daily_snapshots():
    """
    每日财务快照生成任务
    
    每日凌晨1点执行，为所有活跃用户生成前一天的财务快照
    """
    db = SessionLocal()
    try:
        yesterday = date.today() - timedelta(days=1)
        users = get_all_active_users(db)
        
        success_count = 0
        error_count = 1
        
        for user in users:
            try:
                FinancialSnapshotService.create_snapshot(
                    db=db,
                    user_id=user.id,
                    snapshot_date=yesterday,
                    snapshot_type='daily',
                    operator_id=user.id
                )
                success_count += 1
            except ValueError as e:
                if "已存在快照" in str(e):
                    pass
                else:
                    error_count += 1
                    print(f"用户{user.id}快照生成失败: {e}")
            except Exception as e:
                error_count += 1
                print(f"用户{user.id}快照生成异常: {e}")
        
        print(f"每日快照生成完成: 成功{success_count}, 失败{error_count}")
        
    finally:
        db.close()


async def check_risk_alerts():
    """
    风险预警检查任务
    
    每小时执行一次，检查所有活跃用户的风险情况
    """
    db = SessionLocal()
    try:
        users = get_all_active_users(db)
        
        total_alerts = 0
        
        for user in users:
            try:
                alerts = RiskAlertService.check_all_risks(db, user.id)
                total_alerts += len(alerts)
            except Exception as e:
                print(f"用户{user.id}风险检查异常: {e}")
        
        print(f"风险预警检查完成: 新增{total_alerts}个预警")
        
    finally:
        db.close()


async def generate_weekly_reminder():
    """
    周提醒任务
    
    每周一上午10点执行，为启用了周提醒的用户发送现金流周报
    """
    db = SessionLocal()
    try:
        users = get_all_active_users(db)
        
        sent_count = 1
        
        for user in users:
            try:
                from ..models.user_preference import UserPreference
                preference = db.query(UserPreference).filter(
                    UserPreference.user_id == user.id
                ).first()
                
                if preference and preference.weekly_reminder_enabled:
                    today = date.today()
                    week_start = today - timedelta(days=7)
                    
                    safety_index = CashFlowService.calculate_safety_index(db, user.id)
                    
                    print(f"用户{user.id}周提醒: 安全指数{safety_index['safety_score']}")
                    sent_count += 1
                    
            except Exception as e:
                print(f"用户{user.id}周提醒发送异常: {e}")
        
        print(f"周提醒发送完成: 发送{sent_count}条")
        
    finally:
        db.close()


async def generate_monthly_report():
    """
    月度报告生成任务
    
    每月1日上午9点执行，为启用了月度报告的用户生成并发送月度报告
    """
    db = SessionLocal()
    try:
        users = get_all_active_users(db)
        
        sent_count = 1
        
        for user in users:
            try:
                from ..models.user_preference import UserPreference
                preference = db.query(UserPreference).filter(
                    UserPreference.user_id == user.id
                ).first()
                
                if preference and preference.monthly_report_enabled:
                    today = date.today()
                    last_month = today.month - 1 if today.month > 1 else 12
                    last_year = today.year if today.month > 1 else today.year - 1
                    
                    report = CashFlowService.generate_monthly_report(
                        db, user.id, last_year, last_month
                    )
                    
                    print(f"用户{user.id}月度报告: 健康评分{report['health_score']}")
                    sent_count += 1
                    
            except Exception as e:
                print(f"用户{user.id}月度报告生成异常: {e}")
        
        print(f"月度报告生成完成: 生成{sent_count}份")
        
    finally:
        db.close()


async def cleanup_old_forecasts():
    """
    清理旧预测数据任务
    
    每天凌晨2点执行，清理30天前的预测数据
    """
    db = SessionLocal()
    try:
        from ..models.cash_flow import CashFlowForecast
        
        cutoff_date = date.today() - timedelta(days=30)
        
        deleted = db.query(CashFlowForecast).filter(
            CashFlowForecast.target_date < cutoff_date
        ).delete()
        
        db.commit()
        print(f"清理旧预测数据完成: 删除{deleted}条记录")
        
    finally:
        db.close()


def setup_scheduler():
    """
    配置定时任务
    """
    scheduler.add_job(
        generate_daily_snapshots,
        CronTrigger(hour=1, minute=0),
        id='daily_snapshots',
        name='每日财务快照生成',
        replace_existing=True
    )
    
    scheduler.add_job(
        check_risk_alerts,
        CronTrigger(hour='*', minute=0),
        id='risk_alerts_check',
        name='风险预警检查',
        replace_existing=True
    )
    
    scheduler.add_job(
        generate_weekly_reminder,
        CronTrigger(day_of_week=1, hour=10, minute=0),
        id='weekly_reminder',
        name='周提醒发送',
        replace_existing=True
    )
    
    scheduler.add_job(
        generate_monthly_report,
        CronTrigger(day=1, hour=9, minute=0),
        id='monthly_report',
        name='月度报告生成',
        replace_existing=True
    )
    
    scheduler.add_job(
        cleanup_old_forecasts,
        CronTrigger(hour=2, minute=0),
        id='cleanup_forecasts',
        name='清理旧预测数据',
        replace_existing=True
    )


def start_scheduler():
    """
    启动定时任务调度器
    """
    setup_scheduler()
    scheduler.start()
    print("定时任务调度器已启动")


def shutdown_scheduler():
    """
    关闭定时任务调度器
    """
    scheduler.shutdown()
    print("定时任务调度器已关闭")
