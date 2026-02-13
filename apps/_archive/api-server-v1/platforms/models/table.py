from sqlalchemy import Column, Integer, String, NUMERIC, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Table(Base):
    """酒台资源模型 - Platform层核心模块，用于餐饮/酒吧行业的酒台资源建模"""
    __tablename__ = "tables"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    shop_id = Column(Integer, nullable=False, index=True)
    
    # 与Kernel层Resource模块的映射关系
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False, index=True)  # 关联的Resource ID
    
    # 酒台基本信息
    name = Column(String(64), nullable=False)  # 酒台名称：A01, B02, M03等
    capacity = Column(Integer, nullable=False)  # 酒台容量
    area = Column(String(32), nullable=False, index=True)  # 所属区域：A, B, M等
    
    # 酒台业务属性
    min_consumption = Column(NUMERIC(12, 2), nullable=True)  # 最低消费金额
    is_vip = Column(Integer, default=0)  # 是否VIP酒台：0: 普通, 1: VIP
    is_smoking = Column(Integer, default=0)  # 是否吸烟区：0: 非吸烟, 1: 吸烟
    
    # 酒台布局属性（用于可视化）
    position_x = Column(Integer, nullable=True)  # 酒台在布局中的X坐标
    position_y = Column(Integer, nullable=True)  # 酒台在布局中的Y坐标
    width = Column(Integer, nullable=True)  # 酒台宽度
    height = Column(Integer, nullable=True)  # 酒台高度
    rotation = Column(Integer, nullable=True)  # 酒台旋转角度
    
    # 酒台状态：通过ResourceEvent计算得出，不在数据库中直接存储
    # 状态包括：available, occupied, reserved, maintenance等
    
    # 扩展字段：酒台设备或特色
    features = Column(JSON, nullable=True)  # 酒台特色：电视, 投影仪, 等
    equipment = Column(JSON, nullable=True)  # 酒台设备：麦克风, 音响, 等
    
    # 关联关系
    table_group_id = Column(Integer, nullable=True, index=True)  # 关联的TableGroup ID
    
    def __repr__(self):
        return f"<Table(id={self.id}, shop_id={self.shop_id}, name={self.name}, area={self.area}, capacity={self.capacity})>"

class TableGroup(Base):
    """区域管理模型 - Platform层核心模块，用于管理酒台的区域划分"""
    __tablename__ = "table_groups"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    shop_id = Column(Integer, nullable=False, index=True)
    name = Column(String(64), nullable=False)  # 区域名称：A区, B区, M区等
    description = Column(String(256), nullable=True)  # 区域描述
    
    # 区域业务属性
    is_vip_area = Column(Integer, default=0)  # 是否VIP区域：0: 普通, 1: VIP
    min_group_consumption = Column(NUMERIC(12, 2), nullable=True)  # 区域最低消费
    
    # 区域布局属性
    position_x = Column(Integer, nullable=True)  # 区域在布局中的X坐标
    position_y = Column(Integer, nullable=True)  # 区域在布局中的Y坐标
    width = Column(Integer, nullable=True)  # 区域宽度
    height = Column(Integer, nullable=True)  # 区域高度
    
    def __repr__(self):
        return f"<TableGroup(id={self.id}, shop_id={self.shop_id}, name={self.name}, is_vip_area={self.is_vip_area})>"