# Platforms层 - 行业操作系统

## 1. 概述

Platforms层是Dot-Store系统的行业实现层，负责将Kernel层提供的原子能力封装为行业特定的业务逻辑。当前版本主要针对餐饮/酒吧行业，实现了行业标准化的业务流程。

## 2. 核心职责

- 行业资源建模：将Kernel层的抽象资源映射为行业特定资源（如酒台、包间等）
- 行业身份系统：实现会员、股东等行业特定身份管理
- 行业规则：实现订台规则、消费规则、返现/抵扣规则等
- 业务流程：实现行业标准化的业务流程

## 3. 目录结构

```
platforms/
├── models/          # 行业模型定义
│   ├── base.py          # 模型基类
│   ├── table.py         # 台位模型
│   ├── reservation.py   # 订台模型
│   ├── member.py        # 会员模型
│   ├── cashback.py      # 返现模型
│   └── order.py         # 订单模型
├── services/        # 业务服务接口
│   ├── reservation_service.py   # 订台服务接口
│   ├── member_service.py        # 会员服务接口
│   └── cashback_service.py      # 返现服务接口
├── repositories/    # 数据访问层
├── schemas/         # 数据传输对象
└── utils/           # 工具函数
```

## 4. 设计原则

- 只包含行业共识的业务逻辑
- 不包含门店特定的定制化规则
- 基于Kernel层提供的原子能力构建
- 保持与Kernel层的松耦合
- 支持多行业扩展

## 5. 关键模块说明

### 5.1 台位管理系统

台位管理系统提供以下能力：
- 台位的创建、查询、更新和删除
- 台位区域管理
- 台位状态管理
- 台位可视化布局

### 5.2 订台服务

订台服务提供以下能力：
- 订台的创建、查询、更新和取消
- 订台状态流转
- 可用台位查询
- 订台冲突检测

### 5.3 会员/股东系统

会员/股东系统提供以下能力：
- 会员的创建和管理
- 会员等级管理
- 会员周期管理
- 股东权益管理

### 5.4 返现政策

返现政策系统提供以下能力：
- 返现规则的创建和管理
- 返现计算
- 返现记录管理
- 积分抵扣规则

## 6. 使用方法

Platforms层通过服务接口向script层提供能力，script层通过依赖注入的方式使用Platforms层的服务。

```python
# script层使用Platforms层服务的示例
from fastapi import Depends
from platforms.services.reservation_service import ReservationService
from script.schemas.reservation import ReservationCreate, ReservationResponse

@router.post("/reservations", response_model=ReservationResponse)
def create_reservation(
    reservation_data: ReservationCreate,
    db: Session = Depends(get_db),
    reservation_service: ReservationService = Depends(get_reservation_service)
):
    """创建订台"""
    reservation = reservation_service.create_reservation(db, reservation_data.dict())
    return reservation
```

## 7. 扩展说明

Platforms层的扩展应遵循以下原则：
- 只包含行业共识的业务逻辑
- 不包含门店特定的定制化规则
- 基于Kernel层提供的原子能力构建
- 保持与Kernel层的松耦合
- 支持多行业扩展

## 8. 多行业支持

Platforms层设计支持多行业扩展，每个行业可以有自己的Platforms实现，共享同一套Kernel层。未来计划支持：
- 零售行业
- 服务行业
- 其他行业

## 9. 与Kernel层的关系

Platforms层依赖于Kernel层提供的原子能力，通过服务接口调用Kernel层的功能。Platforms层将Kernel层的抽象能力封装为行业特定的业务逻辑，向script层提供行业标准化的服务。