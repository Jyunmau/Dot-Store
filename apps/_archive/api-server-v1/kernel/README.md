# Kernel层 - 商业计算内核

## 1. 概述

Kernel层是Dot-Store系统的核心，提供去行业化的原子能力，是整个系统的基础。它不包含任何行业特定语义，只提供通用的商业计算能力。

## 2. 核心职责

- 资源系统：提供资源的CRUD操作和资源占用事件管理
- 账户与数值系统：提供账户管理和数值记账功能
- 交易与可靠性：确保事件的可靠写入和幂等性保证
- 审计日志：记录关键操作的审计记录

## 3. 目录结构

```
kernel/
├── models/          # 数据模型定义
│   ├── base.py      # 模型基类
│   ├── resource.py  # 资源模型
│   ├── event.py     # 事件模型
│   ├── account.py   # 账户模型
│   ├── ledger.py    # 账本模型
│   ├── audit.py     # 审计模型
│   └── config.py    # 配置模型
├── services/        # 服务接口定义
│   ├── resource_service.py   # 资源服务接口
│   ├── account_service.py    # 账户服务接口
│   └── ledger_service.py     # 账本服务接口
└── utils/           # 工具函数
```

## 4. 设计原则

- 不包含任何行业特定语义
- 不定义业务规则
- 只提供原子级别的能力
- 确保高可靠性和高性能
- 支持水平扩展

## 5. 关键模块说明

### 5.1 资源系统

资源系统是Kernel层的核心模块，提供以下能力：
- 资源的创建、查询、更新和删除
- 资源占用事件的管理
- 并发冲突检测
- 资源状态的派生

### 5.2 账户与数值系统

账户与数值系统提供以下能力：
- 账户的创建和管理
- 数值的记账和查询
- 账户余额的计算
- 支持多种数值类型

### 5.3 交易与可靠性

交易与可靠性模块确保：
- 事件的可靠写入
- 幂等性保证
- 事件的可回放
- 数据的一致性

## 6. 使用方法

Kernel层通过服务接口向Platform层提供能力，Platform层通过依赖注入的方式使用Kernel层的服务。

```python
# Platform层使用Kernel层服务的示例
from kernel.services.resource_service import ResourceService

class ReservationService:
    def __init__(self, resource_service: ResourceService):
        self.resource_service = resource_service
    
    def create_reservation(self, reservation_data):
        # 使用Kernel层的资源服务创建资源事件
        event_data = {
            "shop_id": reservation_data["shop_id"],
            "event_type": "reservation_created",
            "related_resource_id": reservation_data["resource_id"],
            "related_resource_type": "table",
            "payload": reservation_data
        }
        return self.resource_service.create_resource_event(event_data)
```

## 7. 扩展说明

Kernel层的扩展应遵循以下原则：
- 只添加原子级别的能力
- 不添加任何行业特定语义
- 保持接口的稳定性
- 确保向后兼容