from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from models.config import Config
from models.database import get_db

# 创建配置路由
router = APIRouter()

@router.post("/", response_model=dict)
def create_config(config_data: dict, db: Session = Depends(get_db)):
    """创建配置"""
    try:
        # 检查配置是否已存在
        existing_config = db.query(Config).filter(
            Config.shop_id == config_data.get("shop_id"),
            Config.key == config_data.get("key")
        ).first()
        
        if existing_config:
            # 更新现有配置
            existing_config.value = config_data.get("value")
            db.commit()
            db.refresh(existing_config)
            return {"id": existing_config.id, "message": "配置更新成功"}
        else:
            # 创建新配置
            config = Config(
                shop_id=config_data.get("shop_id"),
                key=config_data.get("key"),
                value=config_data.get("value")
            )
            db.add(config)
            db.commit()
            db.refresh(config)
            return {"id": config.id, "message": "配置创建成功"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"创建/更新配置失败: {str(e)}")

@router.get("/", response_model=List[dict])
def get_configs(shop_id: int, db: Session = Depends(get_db)):
    """获取配置列表"""
    configs = db.query(Config).filter(Config.shop_id == shop_id).all()
    
    return [{
        "id": config.id,
        "shop_id": config.shop_id,
        "key": config.key,
        "value": config.value,
        "created_at": config.created_at,
        "updated_at": config.updated_at
    } for config in configs]

@router.get("/{config_key}", response_model=dict)
def get_config_by_key(shop_id: int, config_key: str, db: Session = Depends(get_db)):
    """根据 Key 获取配置"""
    config = db.query(Config).filter(
        Config.shop_id == shop_id,
        Config.key == config_key
    ).first()
    
    if not config:
        raise HTTPException(status_code=404, detail="配置不存在")
    
    return {
        "id": config.id,
        "shop_id": config.shop_id,
        "key": config.key,
        "value": config.value,
        "created_at": config.created_at,
        "updated_at": config.updated_at
    }
