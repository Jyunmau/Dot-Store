"""
Dot-Store V2.1 备份服务
"""
import os
import json
import zipfile
import tempfile
from datetime import datetime
from typing import Optional, List
from fastapi import HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ..models.backup import Backup, BackupSettings
from ..models.order import Order, OrderCategory
from ..models.transaction import Transaction, TransactionCategory
from ..models.user import User
from ..schemas.backup import BackupCreate, BackupSettingsUpdate


BACKUP_DIR = "backups"


class BackupService:
    """
    备份服务类
    """

    def __init__(self, db: Session):
        self.db = db
        self._ensure_backup_dir()

    def _ensure_backup_dir(self):
        """
        确保备份目录存在
        """
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)

    def _get_user_backup_dir(self, user_id: int) -> str:
        """
        获取用户备份目录
        """
        user_dir = os.path.join(BACKUP_DIR, str(user_id))
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        return user_dir

    def _collect_backup_data(self, user_id: int) -> dict:
        """
        收集用户备份数据
        """
        orders = self.db.query(Order).filter(Order.user_id == user_id).all()
        order_categories = self.db.query(OrderCategory).filter(OrderCategory.user_id == user_id).all()
        transactions = self.db.query(Transaction).filter(Transaction.user_id == user_id).all()
        transaction_categories = self.db.query(TransactionCategory).filter(
            TransactionCategory.user_id == user_id
        ).all()

        backup_data = {
            "version": "2.1",
            "backup_time": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "orders": [
                {
                    "id": o.id,
                    "amount": float(o.amount) if o.amount else 0,
                    "order_type": o.order_type,
                    "category_id": o.category_id,
                    "tags": o.tags,
                    "note": o.note,
                    "status": o.status,
                    "created_at": o.created_at.isoformat() if o.created_at else None,
                    "updated_at": o.updated_at.isoformat() if o.updated_at else None,
                    "deleted_at": o.deleted_at.isoformat() if o.deleted_at else None,
                }
                for o in orders
            ],
            "order_categories": [
                {
                    "id": c.id,
                    "name": c.name,
                    "description": c.description,
                    "sort_order": c.sort_order,
                    "is_active": c.is_active,
                    "created_at": c.created_at.isoformat() if c.created_at else None,
                }
                for c in order_categories
            ],
            "transactions": [
                {
                    "id": t.id,
                    "amount": float(t.amount) if t.amount else 0,
                    "transaction_type": t.transaction_type,
                    "category_id": t.category_id,
                    "note": t.note,
                    "attachment": t.attachment,
                    "transaction_date": t.transaction_date.isoformat() if t.transaction_date else None,
                    "created_at": t.created_at.isoformat() if t.created_at else None,
                    "updated_at": t.updated_at.isoformat() if t.updated_at else None,
                }
                for t in transactions
            ],
            "transaction_categories": [
                {
                    "id": c.id,
                    "name": c.name,
                    "category_type": c.category_type,
                    "description": c.description,
                    "sort_order": c.sort_order,
                    "is_active": c.is_active,
                    "created_at": c.created_at.isoformat() if c.created_at else None,
                }
                for c in transaction_categories
            ],
        }

        return backup_data

    def create_backup(self, user_id: int, backup_data: BackupCreate) -> Backup:
        """
        创建手动备份
        """
        backup = Backup(
            user_id=user_id,
            name=backup_data.name,
            description=backup_data.description,
            status="pending",
            backup_path="",
            backup_size=0,
            backup_type="manual",
        )
        self.db.add(backup)
        self.db.commit()
        self.db.refresh(backup)

        try:
            backup.status = "in_progress"
            self.db.commit()

            user_dir = self._get_user_backup_dir(user_id)
            backup_filename = f"backup_{backup.id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.zip"
            backup_path = os.path.join(user_dir, backup_filename)

            data = self._collect_backup_data(user_id)

            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                json_path = f.name

            try:
                with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                    zf.write(json_path, 'backup_data.json')

                backup_size = os.path.getsize(backup_path)
            finally:
                os.unlink(json_path)

            backup.backup_path = backup_path
            backup.backup_size = backup_size
            backup.status = "completed"
            backup.completed_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(backup)

        except Exception as e:
            backup.status = "failed"
            self.db.commit()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"备份创建失败: {str(e)}"
            )

        return backup

    def get_backups(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Backup]:
        """
        获取备份列表
        """
        return self.db.query(Backup).filter(
            Backup.user_id == user_id
        ).order_by(Backup.created_at.desc()).offset(skip).limit(limit).all()

    def get_backup(self, user_id: int, backup_id: int) -> Optional[Backup]:
        """
        获取备份详情
        """
        backup = self.db.query(Backup).filter(
            Backup.id == backup_id,
            Backup.user_id == user_id
        ).first()

        if not backup:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="备份不存在"
            )

        return backup

    def delete_backup(self, user_id: int, backup_id: int) -> bool:
        """
        删除备份
        """
        backup = self.get_backup(user_id, backup_id)

        if backup.backup_path and os.path.exists(backup.backup_path):
            os.remove(backup.backup_path)

        self.db.delete(backup)
        self.db.commit()

        return True

    def download_backup(self, user_id: int, backup_id: int) -> FileResponse:
        """
        下载备份文件
        """
        backup = self.get_backup(user_id, backup_id)

        if backup.status != "completed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="备份尚未完成，无法下载"
            )

        if not backup.backup_path or not os.path.exists(backup.backup_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="备份文件不存在"
            )

        filename = f"backup_{backup.name}_{datetime.utcnow().strftime('%Y%m%d')}.zip"

        return FileResponse(
            path=backup.backup_path,
            filename=filename,
            media_type="application/zip"
        )

    def restore_backup(self, user_id: int, backup_id: int) -> dict:
        """
        从备份恢复数据
        """
        backup = self.get_backup(user_id, backup_id)

        if backup.status != "completed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="备份尚未完成，无法恢复"
            )

        if not backup.backup_path or not os.path.exists(backup.backup_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="备份文件不存在"
            )

        try:
            with zipfile.ZipFile(backup.backup_path, 'r') as zf:
                json_data = zf.read('backup_data.json').decode('utf-8')
                data = json.loads(json_data)

            restored_counts = {
                "orders": 0,
                "order_categories": 0,
                "transactions": 0,
                "transaction_categories": 0,
            }

            self.db.query(Order).filter(Order.user_id == user_id).delete()
            self.db.query(OrderCategory).filter(OrderCategory.user_id == user_id).delete()
            self.db.query(Transaction).filter(Transaction.user_id == user_id).delete()
            self.db.query(TransactionCategory).filter(TransactionCategory.user_id == user_id).delete()
            self.db.commit()

            for cat_data in data.get("order_categories", []):
                category = OrderCategory(
                    id=cat_data["id"],
                    user_id=user_id,
                    name=cat_data["name"],
                    description=cat_data.get("description"),
                    sort_order=cat_data.get("sort_order", 0),
                    is_active=cat_data.get("is_active", True),
                    created_at=datetime.fromisoformat(cat_data["created_at"]) if cat_data.get("created_at") else None,
                )
                self.db.merge(category)
                restored_counts["order_categories"] += 1

            for order_data in data.get("orders", []):
                order = Order(
                    id=order_data["id"],
                    user_id=user_id,
                    amount=order_data["amount"],
                    order_type=order_data.get("order_type"),
                    category_id=order_data.get("category_id"),
                    tags=order_data.get("tags"),
                    note=order_data.get("note"),
                    status=order_data.get("status", "completed"),
                    created_at=datetime.fromisoformat(order_data["created_at"]) if order_data.get("created_at") else None,
                    updated_at=datetime.fromisoformat(order_data["updated_at"]) if order_data.get("updated_at") else None,
                    deleted_at=datetime.fromisoformat(order_data["deleted_at"]) if order_data.get("deleted_at") else None,
                )
                self.db.merge(order)
                restored_counts["orders"] += 1

            for cat_data in data.get("transaction_categories", []):
                category = TransactionCategory(
                    id=cat_data["id"],
                    user_id=user_id,
                    name=cat_data["name"],
                    category_type=cat_data.get("category_type", "income"),
                    description=cat_data.get("description"),
                    sort_order=cat_data.get("sort_order", 0),
                    is_active=cat_data.get("is_active", True),
                    created_at=datetime.fromisoformat(cat_data["created_at"]) if cat_data.get("created_at") else None,
                )
                self.db.merge(category)
                restored_counts["transaction_categories"] += 1

            for trans_data in data.get("transactions", []):
                transaction = Transaction(
                    id=trans_data["id"],
                    user_id=user_id,
                    amount=trans_data["amount"],
                    transaction_type=trans_data.get("transaction_type", "income"),
                    category_id=trans_data.get("category_id"),
                    note=trans_data.get("note"),
                    attachment=trans_data.get("attachment"),
                    transaction_date=datetime.fromisoformat(trans_data["transaction_date"]) if trans_data.get("transaction_date") else None,
                    created_at=datetime.fromisoformat(trans_data["created_at"]) if trans_data.get("created_at") else None,
                    updated_at=datetime.fromisoformat(trans_data["updated_at"]) if trans_data.get("updated_at") else None,
                )
                self.db.merge(transaction)
                restored_counts["transactions"] += 1

            self.db.commit()

            return {
                "message": "数据恢复成功",
                "restored_counts": restored_counts
            }

        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"数据恢复失败: {str(e)}"
            )

    def get_backup_settings(self, user_id: int) -> BackupSettings:
        """
        获取备份设置
        """
        settings = self.db.query(BackupSettings).filter(
            BackupSettings.user_id == user_id
        ).first()

        if not settings:
            settings = BackupSettings(
                user_id=user_id,
                auto_backup_enabled=False,
                backup_schedule="0 0 * * *",
                backup_retention_days=7,
            )
            self.db.add(settings)
            self.db.commit()
            self.db.refresh(settings)

        return settings

    def update_backup_settings(self, user_id: int, settings_data: BackupSettingsUpdate) -> BackupSettings:
        """
        更新备份设置
        """
        settings = self.get_backup_settings(user_id)

        settings.auto_backup_enabled = settings_data.auto_backup_enabled
        settings.backup_schedule = settings_data.backup_schedule
        settings.backup_retention_days = settings_data.backup_retention_days
        settings.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(settings)

        return settings

    def cleanup_old_backups(self, user_id: int, retention_days: int) -> int:
        """
        清理过期备份
        """
        from datetime import timedelta

        cutoff_date = datetime.utcnow() - timedelta(days=retention_days)

        old_backups = self.db.query(Backup).filter(
            Backup.user_id == user_id,
            Backup.created_at < cutoff_date,
            Backup.backup_type == "auto"
        ).all()

        deleted_count = 0
        for backup in old_backups:
            if backup.backup_path and os.path.exists(backup.backup_path):
                os.remove(backup.backup_path)
            self.db.delete(backup)
            deleted_count += 1

        self.db.commit()

        return deleted_count
