# 数据库设计文档

## 1. 概述

本文档详细描述了Dot-Store系统的数据库设计，包括数据库架构、表结构、表关系和核心业务流程的数据流转。系统采用分层架构设计，数据库结构也相应地分为Kernel层和Platforms层，分别对应通用商业能力和行业特定业务逻辑。

## 2. 数据库架构

### 2.1 分层设计

系统数据库采用分层设计，与系统的三层架构（Kernel、Platforms、Script）保持一致：

| 层次 | 职责 | 核心模块 |
|------|------|----------|
| Kernel层 | 通用商业原子能力 | 账户、审计、配置、事件、账本、资源 |
| Platforms层 | 行业特定业务逻辑 | 台位、预订、会员、返现、订单 |
| Script层 | HTTP请求处理 | 无直接数据库模型，通过API调用Kernel和Platforms层服务 |

### 2.2 设计原则

- **松耦合**：各层之间通过外键关联，保持松耦合设计
- **可扩展性**：支持多行业扩展，新行业可以在Platforms层添加新的模型
- **数据一致性**：核心数据（如账务分录）采用强一致性设计
- **高性能**：通过索引优化查询性能，支持大规模数据存储
- **可审计性**：所有关键操作都有审计日志记录

## 3. 核心表结构设计

### 3.1 Kernel层表结构

#### 3.1.1 账户表 (accounts)

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| id | Integer | PRIMARY KEY, AUTO_INCREMENT | 账户ID |
| shop_id | Integer | NOT NULL, INDEX | 店铺ID |
| username | String(64) | UNIQUE, INDEX, NULL | 用户名 |
| phone | String(32) | UNIQUE, INDEX, NULL | 手机号 |
| email | String(128) | UNIQUE, INDEX, NULL | 邮箱 |
| password_hash | String(256) | NULL | 密码哈希 |
| role | String(32) | DEFAULT 'user' | 角色：user, admin, system, member, shareholder |
| status | String(32) | DEFAULT 'active' | 状态：active, inactive, suspended, deleted |
| profile_id | Integer | INDEX, NULL | 关联的用户资料ID |
| profile_type | String(32) | NULL | 关联的用户资料类型 |
| last_login_at | TIMESTAMP | NULL | 最后登录时间 |
| login_attempts | Integer | DEFAULT 0 | 登录尝试次数 |
| locked_until | TIMESTAMP | NULL | 账户锁定时间 |
| created_at | TIMESTAMP | DEFAULT NOW() | 创建时间 |
| updated_at | TIMESTAMP | DEFAULT NOW() ON UPDATE NOW() | 更新时间 |

#### 3.1.2 认证令牌表 (auth_tokens)

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| id | Integer | PRIMARY KEY, AUTO_INCREMENT | 令牌ID |
| account_id | Integer | NOT NULL, INDEX | 账户ID |
| token | String(512) | NOT NULL, UNIQUE | JWT令牌 |
| token_type | String(32) | DEFAULT 'access' | 令牌类型：access, refresh |
| expires_at | TIMESTAMP | NOT NULL | 令牌过期时间 |
| ip_address | String(64) | NULL | 生成令牌的IP地址 |
| user_agent | String(256) | NULL | 生成令牌的用户代理 |
| is_revoked | Integer | DEFAULT 0 | 令牌状态：0有效, 1已撤销 |
| created_at | TIMESTAMP | DEFAULT NOW() | 创建时间 |

#### 3.1.3 审计日志表 (audit_logs)

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| id | Integer | PRIMARY KEY, AUTO_INCREMENT | 日志ID |
| shop_id | Integer | NOT NULL, INDEX | 店铺ID |
| account_id | Integer | INDEX, NULL | 操作人账户ID |
| account_type | String(32) | NULL | 操作人类型 |
| actor_ip | String(64) | NULL | 操作人IP地址 |
| actor_agent | String(256) | NULL | 操作人用户代理 |
| action | String(64) | NOT NULL | 操作类型：create, update, delete, login, logout |
| resource_type | String(64) | NOT NULL, INDEX | 资源类型：order, event, ledger, resource |
| resource_id | Integer | INDEX, NULL | 资源ID |
| details | JSON | NULL | 操作详情，包含before和after状态 |
| change_summary | String(256) | NULL | 操作变更摘要 |
| result | String(32) | DEFAULT 'success' | 操作结果：success, failed, partial |
| error_message | String(512) | NULL | 错误信息 |
| created_at | TIMESTAMP | DEFAULT NOW(), INDEX | 创建时间 |

#### 3.1.4 配置表 (configs)

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| id | Integer | PRIMARY KEY, AUTO_INCREMENT | 配置ID |
| shop_id | Integer | NOT NULL, INDEX | 店铺ID |
| key | String(64) | NOT NULL, INDEX | 配置键 |
| value | JSON | NOT NULL | 配置值 |
| created_at | TIMESTAMP | DEFAULT NOW() | 创建时间 |
| updated_at | TIMESTAMP | DEFAULT NOW() ON UPDATE NOW() | 更新时间 |

#### 3.1.5 事件表 (events)

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| id | Integer | PRIMARY KEY, AUTO_INCREMENT | 事件ID |
| shop_id | Integer | NOT NULL, INDEX | 店铺ID |
| event_type | String(64) | NOT NULL | 事件类型 |
| related_resource_id | Integer | INDEX, NULL | 关联的资源ID |
| related_resource_type | String(64) | NULL | 关联的资源类型 |
| actor_id | Integer | INDEX, NULL | 执行该事件的参与者ID |
| actor_type | String(64) | NULL | 执行该事件的参与者类型 |
| payload | JSON | NULL | 事件负载 |
| created_at | TIMESTAMP | DEFAULT NOW(), INDEX | 创建时间 |

#### 3.1.6 分类账表 (ledger_accounts)

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| id | Integer | PRIMARY KEY, AUTO_INCREMENT | 分类账ID |
| shop_id | Integer | NOT NULL, INDEX | 店铺ID |
| code | String(64) | NOT NULL, INDEX | 分类编码 |
| name | String(128) | NOT NULL | 分类名称 |
| type | String(32) | NOT NULL | 账户类型：收入账、成本账、预充值/会员账、临时账 |
| account_owner_id | Integer | INDEX, NULL | 账户所有者ID |
| account_owner_type | String(32) | NULL | 账户所有者类型：shop, customer, member |
| is_customer_account | Integer | DEFAULT 0 | 客户账户标识：0店铺账户, 1客户账户 |
| created_at | TIMESTAMP | DEFAULT NOW() | 创建时间 |

#### 3.1.7 账务分录表 (ledger_entries)

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| id | Integer | PRIMARY KEY, AUTO_INCREMENT | 分录ID |
| shop_id | Integer | NOT NULL, INDEX | 店铺ID |
| account_id | Integer | NOT NULL, INDEX | 分类账ID |
| order_id | Integer | INDEX, NULL | 关联订单ID |
| event_id | Integer | INDEX, NULL | 关联事件ID |
| customer_id | Integer | INDEX, NULL | 关联客户ID |
| transaction_type | String(32) | NOT NULL | 交易类型：sale, refund, cashback, redemption |
| amount | NUMERIC(12,2) | NOT NULL | 金额，精确到分 |
| direction | String(8) | NOT NULL | 方向：IN收入/增加, OUT支出/减少 |
| description | Text | NULL | 描述 |
| balance_before | NUMERIC(12,2) | NULL | 交易前余额 |
| balance_after | NUMERIC(12,2) | NULL | 交易后余额 |
| created_at | TIMESTAMP | DEFAULT NOW(), INDEX | 创建时间 |

#### 3.1.8 资源表 (resources)

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| id | Integer | PRIMARY KEY, AUTO_INCREMENT | 资源ID |
| shop_id | Integer | NOT NULL, INDEX | 店铺ID |
| resource_type | String(64) | NOT NULL, INDEX | 资源类型：table, booth |
| name | String(128) | NULL | 资源名称 |
| resource_metadata | JSON | NULL | 资源元数据，用于存储行业特定属性 |

### 3.2 Platforms层表结构

#### 3.2.1 台位表 (tables)

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| id | Integer | PRIMARY KEY, AUTO_INCREMENT | 台位ID |
| shop_id | Integer | NOT NULL, INDEX | 店铺ID |
| resource_id | Integer | NOT NULL, INDEX, FOREIGN KEY | 关联的Resource ID |
| name | String(64) | NOT NULL | 台位名称：A01, B02, M03 |
| capacity | Integer | NOT NULL | 台位容量 |
| area | String(32) | NOT NULL, INDEX | 所属区域：A, B, M |
| min_consumption | NUMERIC(12,2) | NULL | 最低消费金额 |
| is_vip | Integer | DEFAULT 0 | VIP标识：0普通, 1VIP |
| is_smoking | Integer | DEFAULT 0 | 吸烟区标识：0非吸烟, 1吸烟 |
| position_x | Integer | NULL | 台位在布局中的X坐标 |
| position_y | Integer | NULL | 台位在布局中的Y坐标 |
| width | Integer | NULL | 台位宽度 |
| height | Integer | NULL | 台位高度 |
| rotation | Integer | NULL | 台位旋转角度 |
| features | JSON | NULL | 台位特色：电视, 投影仪 |
| equipment | JSON | NULL | 台位设备：麦克风, 音响 |
| table_group_id | Integer | INDEX, NULL | 关联的TableGroup ID |

#### 3.2.2 台位区域表 (table_groups)

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| id | Integer | PRIMARY KEY, AUTO_INCREMENT | 区域ID |
| shop_id | Integer | NOT NULL, INDEX | 店铺ID |
| name | String(64) | NOT NULL | 区域名称：A区, B区, M区 |
| description | String(256) | NULL | 区域描述 |
| is_vip_area | Integer | DEFAULT 0 | VIP区域标识：0普通, 1VIP |
| min_group_consumption | NUMERIC(12,2) | NULL | 区域最低消费 |
| position_x | Integer | NULL | 区域在布局中的X坐标 |
| position_y | Integer | NULL | 区域在布局中的Y坐标 |
| width | Integer | NULL | 区域宽度 |
| height | Integer | NULL | 区域高度 |

#### 3.2.3 预订表 (reservations)

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| id | Integer | PRIMARY KEY, AUTO_INCREMENT | 预订ID |
| shop_id | Integer | NOT NULL, INDEX | 店铺ID |
| reservation_no | String(64) | NOT NULL, UNIQUE, INDEX | 预订单号 |
| table_id | Integer | NOT NULL, INDEX, FOREIGN KEY | 预订的台位ID |
| customer_id | Integer | INDEX, NULL | 预订人ID |
| start_time | TIMESTAMP | NOT NULL, INDEX | 预订开始时间 |
| end_time | TIMESTAMP | NOT NULL, INDEX | 预订结束时间 |
| duration | Integer | NOT NULL | 预订时长（分钟） |
| people_count | Integer | NOT NULL | 预订人数 |
| status | String(32) | DEFAULT 'pending', INDEX | 预订状态：pending, confirmed, completed, cancelled, expired |
| special_requests | String(256) | NULL | 特殊要求 |
| resource_event_id | Integer | INDEX, NULL | 关联的ResourceEvent ID |
| deposit_amount | Integer | NULL | 定金金额（分） |
| deposit_status | String(32) | NULL | 定金状态：unpaid, paid, refunded |
| payment_method | String(32) | NULL | 支付方式 |
| created_by | Integer | NULL | 创建人ID |
| confirmed_by | Integer | NULL | 确认人ID |
| confirmed_at | TIMESTAMP | NULL | 确认时间 |
| cancelled_by | Integer | NULL | 取消人ID |
| cancelled_at | TIMESTAMP | NULL | 取消时间 |
| cancellation_reason | String(256) | NULL | 取消原因 |
| created_at | TIMESTAMP | DEFAULT NOW() | 创建时间 |
| updated_at | TIMESTAMP | DEFAULT NOW() ON UPDATE NOW() | 更新时间 |

#### 3.2.4 会员表 (members)

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| id | Integer | PRIMARY KEY, AUTO_INCREMENT | 会员ID |
| shop_id | Integer | NOT NULL, INDEX | 店铺ID |
| account_id | Integer | NOT NULL, UNIQUE, INDEX, FOREIGN KEY | 关联的Account ID |
| name | String(64) | NOT NULL | 会员姓名 |
| phone | String(32) | NOT NULL, INDEX | 会员手机号 |
| member_type | String(32) | NOT NULL, INDEX | 会员类型：member, shareholder |
| member_level | String(32) | NOT NULL, INDEX | 会员等级：bronze, silver, gold |
| membership_start | TIMESTAMP | NOT NULL | 会员开始时间 |
| membership_end | TIMESTAMP | NOT NULL, INDEX | 会员结束时间 |
| is_active | Integer | DEFAULT 1, INDEX | 会员状态：0过期, 1活跃 |
| points | Integer | DEFAULT 0 | 会员积分 |
| total_consumption | Integer | DEFAULT 0 | 累计消费金额（分） |
| cashback_balance | Integer | DEFAULT 0 | 返现余额（分） |
| shareholder_share | Integer | NULL | 股东持股比例（%） |
| shareholder_join_date | TIMESTAMP | NULL | 股东加入日期 |
| created_at | TIMESTAMP | DEFAULT NOW() | 创建时间 |
| updated_at | TIMESTAMP | DEFAULT NOW() ON UPDATE NOW() | 更新时间 |

#### 3.2.5 返现表 (cashbacks)

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| id | Integer | PRIMARY KEY, AUTO_INCREMENT | 返现ID |
| shop_id | Integer | NOT NULL, INDEX | 店铺ID |
| member_id | Integer | NOT NULL, INDEX, FOREIGN KEY | 关联会员ID |
| order_id | Integer | NOT NULL, INDEX, FOREIGN KEY | 关联订单ID |
| cashback_amount | Integer | NOT NULL | 返现金额（分） |
| cashback_ratio | Integer | NOT NULL | 返现比例（%） |
| status | String(32) | DEFAULT 'pending', INDEX | 返现状态：pending, confirmed, cancelled |
| created_at | TIMESTAMP | DEFAULT NOW() | 创建时间 |
| updated_at | TIMESTAMP | DEFAULT NOW() ON UPDATE NOW() | 更新时间 |

#### 3.2.6 订单表 (orders)

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| id | Integer | PRIMARY KEY, AUTO_INCREMENT | 订单ID |
| shop_id | Integer | NOT NULL, INDEX | 店铺ID |
| order_no | String(64) | NOT NULL, UNIQUE, INDEX | 订单号 |
| table_id | Integer | NOT NULL, INDEX, FOREIGN KEY | 关联台位ID |
| customer_id | Integer | INDEX, NULL | 关联客户ID |
| total_amount | Integer | NOT NULL | 订单总金额（分） |
| paid_amount | Integer | NOT NULL | 已支付金额（分） |
| payment_status | String(32) | DEFAULT 'pending', INDEX | 支付状态：pending, paid, refunded, partially_refunded |
| order_status | String(32) | DEFAULT 'active', INDEX | 订单状态：active, completed, cancelled |
| created_at | TIMESTAMP | DEFAULT NOW(), INDEX | 创建时间 |
| updated_at | TIMESTAMP | DEFAULT NOW() ON UPDATE NOW() | 更新时间 |

## 4. 表关系图

```
+----------------+     +----------------+     +----------------+     +----------------+
|    accounts    |     |   auth_tokens  |     |   audit_logs   |     |     configs    |
+----------------+     +----------------+     +----------------+     +----------------+
| id             |<----| account_id     |     | shop_id        |     | shop_id        |
| shop_id        |     +----------------+     | account_id     |     | key            |
| username       |                             | action         |     | value          |
| phone          |                             | resource_type  |     +----------------+
| password_hash  |                             | resource_id    |
| role           |                             +----------------+
| status         |
+----------------+      +----------------+      +----------------+
         ^               |    events      |      |    resources   |
         |               +----------------+      +----------------+
         |               | id             |      | id             |
         |               | shop_id        |      | shop_id        |
         |               | event_type     |      | resource_type  |
         |               | related_resource_id |<--| id             |
         |               +----------------+      +----------------+
         |                     ^                      ^
         |                     |                      |
+----------------+     +----------------+     +----------------+
|    members     |     | ledger_entries |     |    tables      |
+----------------+     +----------------+     +----------------+
| id             |     | id             |     | id             |
| shop_id        |     | shop_id        |     | shop_id        |
| account_id     |---->| customer_id    |     | resource_id    |<--+
| member_type    |     | transaction_type|     | name           |   |
| member_level   |     | amount         |     | capacity       |   |
+----------------+     +----------------+     +----------------+   |
         ^                                                         |
         |                                                         |
+----------------+     +----------------+     +----------------+   |
|   cashbacks    |     |    orders      |     | reservations   |   |
+----------------+     +----------------+     +----------------+   |
| id             |     | id             |     | id             |   |
| shop_id        |     | shop_id        |     | shop_id        |   |
| member_id      |<----| customer_id    |     | table_id       |---+
| order_id       |---->| id             |     | reservation_no |
| cashback_amount|     | total_amount   |     | status         |
+----------------+     +----------------+     +----------------+
```

## 5. 核心业务流程数据流转

### 5.1 订台业务流程

1. **创建预订**：
   - 插入`reservations`表记录
   - 插入`events`表记录，类型为"reservation_created"
   - 插入`audit_logs`表记录

2. **确认预订**：
   - 更新`reservations`表状态为"confirmed"
   - 插入`events`表记录，类型为"reservation_confirmed"
   - 插入`audit_logs`表记录

3. **完成预订**：
   - 更新`reservations`表状态为"completed"
   - 插入`events`表记录，类型为"reservation_completed"
   - 插入`audit_logs`表记录

### 5.2 订单交易流程

1. **创建订单**：
   - 插入`orders`表记录
   - 插入`events`表记录，类型为"order_created"
   - 插入`audit_logs`表记录

2. **支付订单**：
   - 更新`orders`表支付状态为"paid"
   - 插入`ledger_entries`表记录，记录收入
   - 插入`events`表记录，类型为"order_paid"
   - 插入`audit_logs`表记录

3. **完成订单**：
   - 更新`orders`表订单状态为"completed"
   - 插入`events`表记录，类型为"order_completed"
   - 插入`audit_logs`表记录

### 5.3 会员返现流程

1. **生成返现**：
   - 插入`cashbacks`表记录
   - 插入`events`表记录，类型为"cashback_generated"
   - 插入`audit_logs`表记录

2. **确认返现**：
   - 更新`cashbacks`表状态为"confirmed"
   - 更新`members`表返现余额
   - 插入`ledger_entries`表记录，记录返现
   - 插入`events`表记录，类型为"cashback_confirmed"
   - 插入`audit_logs`表记录

## 6. 索引设计

### 6.1 主键索引

所有表的`id`字段都创建了主键索引，确保数据的唯一性和快速查询。

### 6.2 外键索引

所有外键字段都创建了索引，包括：
- `auth_tokens.account_id`
- `members.account_id`
- `tables.resource_id`
- `reservations.table_id`
- `orders.table_id`
- `cashbacks.member_id`
- `cashbacks.order_id`

### 6.3 业务索引

针对频繁查询的字段创建了业务索引：
- `accounts.username`、`accounts.phone`、`accounts.email`：用于快速查找用户
- `events.shop_id`、`events.event_type`、`events.created_at`：用于事件查询和统计
- `ledger_entries.shop_id`、`ledger_entries.created_at`：用于账务查询和报表生成
- `reservations.shop_id`、`reservations.status`、`reservations.start_time`：用于预订查询和管理
- `orders.shop_id`、`orders.order_no`、`orders.created_at`：用于订单查询和统计

## 7. 数据安全与备份

### 7.1 数据安全

- 密码采用哈希存储，不存储明文密码
- 敏感数据传输采用HTTPS加密
- 数据库访问权限严格控制，仅允许必要的服务访问
- 定期进行安全审计和漏洞扫描

### 7.2 数据备份

- 定期进行数据库全量备份
- 关键业务数据实时增量备份
- 备份数据异地存储，确保数据安全
- 定期进行备份恢复测试，确保备份可用性

## 8. 性能优化

- 合理设计表结构，避免冗余字段
- 创建适当的索引，优化查询性能
- 针对大数据量的表，考虑分区策略
- 定期进行数据库优化和碎片整理
- 使用连接池管理数据库连接，提高并发性能

## 9. 版本管理

| 版本 | 日期 | 变更内容 | 作者 |
|------|------|----------|------|
| v1.0 | 2026-01-25 | 初始数据库设计文档 | AI助手 |

## 10. 附录

### 10.1 数据类型说明

- `Integer`：整数类型，用于ID和计数字段
- `String(n)`：字符串类型，n为最大长度
- `TIMESTAMP`：时间戳类型，存储日期和时间
- `NUMERIC(12,2)`：数值类型，精确到分，用于金额字段
- `JSON`：JSON类型，用于存储结构化数据
- `Text`：文本类型，用于存储长文本

### 10.2 状态码说明

| 模块 | 状态码 | 描述 |
|------|--------|------|
| 账户 | active | 活跃 |
| 账户 | inactive | 非活跃 |
| 账户 | suspended | 暂停 |
| 账户 | deleted | 已删除 |
| 预订 | pending | 待确认 |
| 预订 | confirmed | 已确认 |
| 预订 | completed | 已完成 |
| 预订 | cancelled | 已取消 |
| 预订 | expired | 已过期 |
| 订单 | pending | 待支付 |
| 订单 | paid | 已支付 |
| 订单 | refunded | 已退款 |
| 订单 | partially_refunded | 部分退款 |
| 返现 | pending | 待确认 |
| 返现 | confirmed | 已确认 |
| 返现 | cancelled | 已取消 |
