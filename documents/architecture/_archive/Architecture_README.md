# Dot-Store V1 Architecture README

> 本文档面向工程实现，作为 Dot-Store V1 的 **唯一架构与工程规范说明**。
> 覆盖：数据库设计（DDL 级）/ 核心 API 设计 / 模块拆分与代码结构。

---

## 0. 架构总览（一句话）

Dot-Store 是一个：

> **以 Event 为底座、以 Order 为业务锚点、以 Ledger 为权威事实层的
> 模块化单体系统（Modular Monolith）**

核心目标：

* 接受真实世界的不完美
* 保证数据可解释、可修正
* 为未来组件化 / 插件化 / 规则引擎留下空间

---

## 1. 数据库设计（DDL 级）

### 1.1 设计原则

* 日志优先于状态
* 追加优先于修改（账务）
* 弱约束、强审计

不追求：

* 业务强一致
* 金融级约束

---

### 1.2 核心表结构

> 说明：以下为 **逻辑 DDL**，字段类型可根据具体数据库（Postgres / MySQL）微调。

---

### 1.2.1 shops（店铺）

```sql
CREATE TABLE shops (
  id            BIGSERIAL PRIMARY KEY,
  name          VARCHAR(128) NOT NULL,
  status        VARCHAR(32) DEFAULT 'active',
  created_at    TIMESTAMP NOT NULL DEFAULT NOW()
);
```

---

### 1.2.2 events（事件，平台级）

> 最底层事实记录，不直接暴露给用户

```sql
CREATE TABLE events (
  id            BIGSERIAL PRIMARY KEY,
  shop_id       BIGINT NOT NULL,
  event_type    VARCHAR(64) NOT NULL,
  payload       JSONB,
  created_at    TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_events_shop_time ON events(shop_id, created_at);
```

---

### 1.2.3 orders（订单，业务级）

> 订单 = 被业务语义解释过的一组事件

```sql
CREATE TABLE orders (
  id              BIGSERIAL PRIMARY KEY,
  shop_id         BIGINT NOT NULL,
  status          VARCHAR(32) DEFAULT 'recorded',
  amount_estimate NUMERIC(12,2),
  tags            JSONB,
  metadata        JSONB,
  created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_orders_shop_time ON orders(shop_id, created_at);
```

---

### 1.2.4 order_events（订单-事件关联）

```sql
CREATE TABLE order_events (
  order_id    BIGINT NOT NULL,
  event_id    BIGINT NOT NULL,
  PRIMARY KEY(order_id, event_id)
);
```

---

### 1.2.5 ledger_accounts（分类账）

```sql
CREATE TABLE ledger_accounts (
  id          BIGSERIAL PRIMARY KEY,
  shop_id     BIGINT NOT NULL,
  code        VARCHAR(64) NOT NULL,
  name        VARCHAR(128) NOT NULL,
  type        VARCHAR(32) NOT NULL,
  created_at  TIMESTAMP NOT NULL DEFAULT NOW()
);
```

---

### 1.2.6 ledger_entries（账务分录）

> 权威事实层，追加写入

```sql
CREATE TABLE ledger_entries (
  id            BIGSERIAL PRIMARY KEY,
  shop_id       BIGINT NOT NULL,
  account_id    BIGINT NOT NULL,
  order_id      BIGINT,
  event_id      BIGINT,
  amount        NUMERIC(12,2) NOT NULL,
  direction     VARCHAR(8) NOT NULL,
  description   TEXT,
  created_at    TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_ledger_shop_time ON ledger_entries(shop_id, created_at);
```

---

### 1.2.7 audit_logs（审计日志）

```sql
CREATE TABLE audit_logs (
  id          BIGSERIAL PRIMARY KEY,
  entity_type VARCHAR(32) NOT NULL,
  entity_id   BIGINT NOT NULL,
  action      VARCHAR(32) NOT NULL,
  before_data JSONB,
  after_data  JSONB,
  created_at  TIMESTAMP NOT NULL DEFAULT NOW()
);
```

---

## 2. 核心 API 设计

### 2.1 API 设计原则

* 面向业务而非表结构
* 不隐藏“不完美”
* 所有修改都有来源

---

### 2.2 Order API

#### 创建订单

```
POST /api/orders
```

Request:

```json
{
  "shop_id": 1,
  "amount_estimate": 58.00,
  "tags": ["堂食", "活动"],
  "metadata": {"note": "新品测试"}
}
```

---

#### 更新订单（弱约束）

```
PUT /api/orders/{id}
```

* 允许修改任意业务字段
* 自动写入 audit_log

---

### 2.3 Ledger API

#### 新增分录

```
POST /api/ledger/entries
```

```json
{
  "shop_id": 1,
  "account_id": 3,
  "order_id": 10,
  "amount": 58.00,
  "direction": "IN",
  "description": "早餐销售"
}
```

---

### 2.4 汇总查询 API

```
GET /api/reports/summary?shop_id=1&date=2026-01-10
```

返回：

* 收入
* 成本
* 盈亏

---

## 3. 模块拆分与代码结构规范

### 3.1 架构风格

采用 **模块化单体（Modular Monolith）**：

* 单进程
* 模块强边界
* 内部通过接口通信

---

### 3.2 推荐目录结构

```
/apps
  /api-server

/modules
  /event
    event.model
    event.service

  /order
    order.model
    order.service
    order.controller

  /ledger
    ledger.model
    ledger.service
    ledger.controller

  /report
    report.service

  /audit
    audit.service

/shared
  /db
  /utils
```

---

### 3.3 模块边界规则（强制）

* Order 模块 **不能** 直接写 Ledger 表
* Ledger 模块 **不能** 推断业务流程
* Report 只读

---

## 4. 扩展与插件策略

### 4.1 V1 扩展方式

* 后端：代码级插件 / 分支
* 前端：定制页面 + UI 配置

### 4.2 明确禁止

* 跨模块直接访问数据库
* 在 Report 层写业务逻辑

---

## 5. 为什么不是 SAP / 不是纯 SaaS

* SAP 假设流程稳定 → 小店不是
* SaaS 强控制 → 真实世界反弹

Dot-Store 的选择是：

> **先解释世界，再试图优化它**

---

## 6. V1 工程完成判据

* 核心表结构稳定
* Order / Ledger API 可独立演进
* 无跨模块耦合

---

> 本文档是 Dot-Store V1 工程实现的最高准则。
> 所有代码评审与重构必须以此为依据。
