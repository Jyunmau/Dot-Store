Dot-Store Platform 层产品需求文档（PRD）

本文档描述 Dot-Store Platform 层的产品需求与功能设计，聚焦于餐饮/酒吧行业。

面向对象：产品设计 / 工程实现 / 未来合作者

⸻

1. 产品愿景与边界

1.1 产品愿景

Platform 层是 Dot-Store 针对餐饮/酒吧行业的操作系统，将 Kernel 层的抽象能力具体化，实现行业共识的业务模型和规则，为上层 App-Script 层提供标准化的行业能力。

1.2 核心价值主张
1. 实现餐饮/酒吧行业的标准化业务模型
2. 提供行业共识的业务规则和流程
3. 封装 Kernel 层复杂性，简化上层应用开发
4. 支持行业内不同业态的灵活扩展

1.3 明确不做的事情
- ❌ 不实现门店特定的定制化规则
- ❌ 不支持非餐饮/酒吧行业的业务模型
- ❌ 不提供门店级的活动策划功能
- ❌ 不参与临时的、试验性的业务创新

2. 目标用户

2.1 直接用户
- App-Script 层的开发者
- 餐饮/酒吧行业的系统集成商

2.2 间接用户
- 餐饮/酒吧门店的管理者和员工
- 餐饮/酒吧的会员和顾客

3. 核心模块与功能

3.1 台位管理系统（Table / Booth）

3.1.1 模块定位
将 Kernel 层的抽象 Resource 具体化为餐饮/酒吧行业的台位资源，包含行业特定的属性和规则。

3.1.2 核心功能
- 台位的创建、读取、更新、删除（CRUD）
- 台位区域管理（A区/B区/M区等）
- 台位状态的实时同步
- 台位可视化配置接口

3.1.3 数据模型
```
Table
- id: string (唯一标识符)
- resource_id: string (关联 Kernel Resource ID)
- name: string (台位名称，如"A1"、"B2")
- area: string (台位区域，如"A区"、"B区"、"M区")
- capacity: number (容纳人数)
- type: string (台位类型：table, booth, private_room)
- status: string (台位状态：available, occupied, reserved)
- minimum_consumption: number (最低消费，可选)
```

3.1.4 设计原则
- 台位是 Kernel Resource 的行业具体化
- 支持不同类型台位的灵活配置
- 台位状态与 Kernel ResourceEvent 保持同步

3.2 订台服务（Reservation Service）

3.2.1 模块定位
实现餐饮/酒吧行业的订台业务流程，处理台位的预订、占用、释放等操作。

3.2.2 核心功能
- 订台请求的创建与审批
- 台位占用的冲突检测
- 订台状态的管理与同步
- 订台历史记录查询

3.2.3 数据模型
```
Reservation
- id: string (唯一标识符)
- table_id: string (关联台位 ID)
- member_id: string (预订会员 ID)
- start_time: datetime (预订开始时间)
- end_time: datetime (预订结束时间)
- status: string (订台状态：pending, confirmed, occupied, completed, cancelled)
- minimum_consumption: number (本次订台最低消费)
- notes: string (备注信息)
```

3.2.4 设计原则
- 订台操作通过 Kernel ResourceEvent 实现
- 支持灵活的订台规则配置
- 保证订台数据的一致性和可靠性

3.3 会员/股东系统（Member / Shareholder）

3.3.1 模块定位
实现餐饮/酒吧行业的会员身份体系，包含会员等级、权益和晋升规则。

3.3.2 核心功能
- 会员注册与登录
- 会员信息管理
- 会员等级与权益管理
- 股东身份管理与晋升

3.3.3 数据模型
```
Member
- id: string (唯一标识符)
- account_id: string (关联 Kernel Account ID)
- phone: string (手机号)
- name: string (会员姓名)
- level: string (会员等级：regular, vip, shareholder)
- points: number (积分余额)
- join_date: datetime (入会日期)
- status: string (会员状态：active, inactive)

Shareholder
- id: string (唯一标识符)
- member_id: string (关联会员 ID)
- shares: number (持股数量)
- dividend_rate: number (分红比例)
- status: string (股东状态：active, suspended)
```

3.3.4 设计原则
- 会员/股东身份是 Kernel Account 的行业具体化
- 支持从普通会员到股东的身份晋升
- 与 Kernel Ledger 集成实现积分和余额管理

3.4 返现政策（CashbackPolicy）

3.4.1 模块定位
实现餐饮/酒吧行业的消费返现规则，基于 Kernel Ledger 提供具体的业务语义。

3.4.2 核心功能
- 返现规则的配置与管理
- 消费金额的返现计算
- 返现金额的发放与记录
- 返现规则的版本管理

3.4.3 数据模型
```
CashbackPolicy
- id: string (唯一标识符)
- name: string (政策名称)
- rate: number (返现比例，如 0.1 表示 10%)
- min_consumption: number (最低消费金额)
- start_date: datetime (生效开始时间)
- end_date: datetime (生效结束时间)
- status: string (政策状态：active, inactive)

CashbackRecord
- id: string (唯一标识符)
- policy_id: string (关联返现政策 ID)
- member_id: string (会员 ID)
- order_id: string (关联订单 ID)
- amount: number (返现金额)
- status: string (返现状态：pending, completed, cancelled)
- timestamp: datetime (记录时间)
```

3.4.4 设计原则
- 返现规则基于消费行为触发
- 返现金额通过 Kernel Ledger 实现记账
- 支持灵活的返现规则配置

3.5 抵扣政策（RedemptionPolicy）

3.5.1 模块定位
实现餐饮/酒吧行业的积分或余额抵扣规则，允许会员使用积累的数值抵扣消费金额。

3.5.2 核心功能
- 抵扣规则的配置与管理
- 积分/余额与现金的汇率管理
- 抵扣请求的处理与验证
- 抵扣记录的查询与统计

3.5.3 数据模型
```
RedemptionPolicy
- id: string (唯一标识符)
- name: string (政策名称)
- rate: number (抵扣汇率，如 100 表示 100 积分抵扣 1 元)
- min_redemption: number (最低抵扣数值)
- status: string (政策状态：active, inactive)

RedemptionRecord
- id: string (唯一标识符)
- policy_id: string (关联抵扣政策 ID)
- member_id: string (会员 ID)
- order_id: string (关联订单 ID)
- points: number (抵扣积分)
- amount: number (抵扣金额)
- status: string (抵扣状态：pending, completed, cancelled)
- timestamp: datetime (记录时间)
```

3.5.4 设计原则
- 抵扣规则与返现规则相互独立
- 抵扣操作通过 Kernel Ledger 实现数值变更
- 支持不同类型数值的抵扣（积分、余额等）

3.6 订单管理系统（Order）

3.6.1 模块定位
实现餐饮/酒吧行业的订单管理，包含消费订单、预订订单等业务类型。

3.6.2 核心功能
- 订单的创建、读取、更新、删除（CRUD）
- 订单状态的管理与同步
- 订单与台位、会员的关联
- 订单金额的计算与拆分

3.6.3 数据模型
```
Order
- id: string (唯一标识符)
- table_id: string (关联台位 ID)
- member_id: string (关联会员 ID)
- order_type: string (订单类型：dine_in, reservation, takeaway)
- total_amount: number (订单总金额)
- paid_amount: number (已支付金额)
- redeemed_amount: number (抵扣金额)
- status: string (订单状态：created, confirmed, paid, completed, cancelled)
- created_at: datetime (创建时间)
- completed_at: datetime (完成时间)

OrderItem
- id: string (唯一标识符)
- order_id: string (关联订单 ID)
- name: string (商品名称)
- quantity: number (数量)
- price: number (单价)
- amount: number (金额)
```

3.6.4 设计原则
- 订单是业务流程的核心载体
- 与 Kernel Ledger 集成实现财务记账
- 支持多种订单类型的统一管理

4. 非功能需求

4.1 性能要求
- 支持每秒至少 500 个订单创建
- 台位状态更新延迟不超过 500ms
- 会员信息查询响应时间不超过 200ms

4.2 可靠性要求
- 系统可用性不低于 99.5%
- 订单数据不丢失
- 支持事务处理，保证数据一致性

4.3 安全性要求
- 用户敏感信息加密存储
- 操作权限严格控制
- 防止订单篡改和数据伪造

4.4 可扩展性要求
- 支持新的台位类型扩展
- 支持新的会员等级和权益扩展
- 支持新的返现和抵扣规则扩展

5. API 设计原则

5.1 接口风格
采用 RESTful API 风格，使用 JSON 格式进行数据交互。

5.2 版本管理
使用 API 版本号进行接口管理，确保向后兼容。

5.3 错误处理
统一的错误码和错误信息格式，便于上层系统处理。

5.4 认证授权
基于 Kernel 层的认证授权机制，实现行业特定的权限控制。

6. 技术实现建议

6.1 架构设计
- 采用分层架构，与 Kernel 层松耦合集成
- 使用事件驱动模式处理业务流程
- 实现领域驱动设计（DDD），清晰划分业务边界

6.2 数据存储
- 业务数据：使用关系型数据库（如 PostgreSQL）
- 缓存：使用 Redis 提高查询性能
- 消息队列：使用 Kafka 或 RabbitMQ 处理异步事件

6.3 开发语言
- 后端：Node.js 或 Go
- 与 Kernel 层保持一致的技术栈

7. 验收标准

7.1 功能验收
- 台位管理功能正常工作
- 订台流程完整且可靠
- 会员/股东身份体系完整
- 返现和抵扣规则正确执行
- 订单管理功能完整

7.2 性能验收
- 系统性能达到设计要求
- 高并发场景下系统稳定运行
- 数据同步延迟符合要求

7.3 可靠性验收
- 系统故障后数据不丢失
- 事务处理保证数据一致性
- 系统恢复时间在可接受范围内

8. 行业扩展计划

8.1 近期扩展
- 支持卡座、包间等不同台位类型
- 实现会员等级晋升规则
- 支持多种返现和抵扣组合

8.2 远期扩展
- 支持酒吧、餐厅、咖啡厅等不同业态
- 实现供应链管理的标准化接口
- 支持多门店连锁管理

⸻

本 PRD 描述的是 Dot-Store Platform 层针对餐饮/酒吧行业的最小但完整产品形态。所有功能设计与工程实现应以此为依据，严格遵守行业边界。