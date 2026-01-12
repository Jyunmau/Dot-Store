Dot-Store V1 开发规则与技术栈规范（Dev Guide · Final）

本文档是 Dot-Store V1 的最终开发规则文档。
已移除所有方案对比，仅保留最终采用的技术选型与强制工程规范。

本文档与《Architecture README》共同构成 不可分割的工程最高准则。

⸻

1. 技术栈总览（最终结论）

Dot-Store V1 采用如下技术栈：

层级	技术选型
后端语言	Python 3.11+
Web 框架	FastAPI
ORM	SQLAlchemy 2.x
数据库	PostgreSQL 14+
数据迁移	Alembic
API 风格	RESTful JSON API
前端框架	React + Vite
UI 策略	Headless UI + 自建设计规范
状态管理	React Hooks / Context（不引入复杂状态库）
容器化	Docker + docker-compose
部署形态	单体服务（模块化单体）

核心原则：个人与小团队长期可控，而非一次性交付。

⸻

2. 后端开发规范（强制）

2.1 架构风格
	•	单进程、单服务
	•	模块化单体（Modular Monolith）
	•	不使用微服务、不使用消息队列

所有模块必须遵循 Architecture README 中定义的边界。

⸻

2.2 分层结构（不可违反）

API Controller
    ↓
Service（唯一业务逻辑层）
    ↓
Model / Repository

规则：
	•	Controller 只处理 HTTP / 参数校验
	•	所有业务逻辑必须在 Service 层
	•	Model 不包含业务判断

⸻

2.3 模块边界铁律
	•	Order 模块 禁止 直接操作 Ledger 表
	•	Ledger 模块 禁止 推导业务流程
	•	Report 模块 只读
	•	Event 模块 不暴露给前端

违反即视为架构缺陷，必须重构。

⸻

3. 数据与一致性规则

3.1 数据世界观

Dot-Store 接受：
	•	业务不规范
	•	数据可能滞后
	•	现实世界存在例外

系统的责任是：
	•	记录事实
	•	保留解释路径
	•	允许人工修正

⸻

3.2 数据写入规则
	•	Ledger（账务）：
	•	只允许追加（INSERT）
	•	禁止 UPDATE / DELETE
	•	业务表（如 Orders）：
	•	允许修改
	•	必须写 audit_log
	•	不强制数据库外键
	•	必须逻辑可追溯

⸻

4. API 设计规范

4.1 API 原则
	•	面向业务语义，而非数据库表
	•	不隐藏“不完美数据”
	•	API 行为必须可解释

⸻

4.2 API 约定
	•	使用 RESTful 风格
	•	JSON 作为唯一数据格式
	•	URL 表达资源，不表达动作

⸻

4.3 错误返回规范

{
  "error_code": "ORDER_NOT_FOUND",
  "message": "订单不存在"
}

	•	禁止向前端返回异常堆栈
	•	错误码必须稳定、可枚举

⸻

5. 前端与 UI 规范

5.1 前端定位

Dot-Store 前端不是“后台管理系统”，而是：

老板每天打开、快速理解自己生意的工具

⸻

5.2 UI 原则（强约束）
	1.	信息优先于操作
	2.	一屏只解决一个问题
	3.	默认展示结论，而非明细

⸻

5.3 UI 技术规范
	•	使用 Headless UI / Radix UI
	•	自建 Design Tokens（颜色 / 字号 / 间距）
	•	禁止直接引入大型 UI 框架（如 Ant Design）

⸻

6. 容器化与部署规范

6.1 Docker 原则
	•	一个容器只运行一个进程
	•	不在容器中运行数据库迁移以外的管理任务

⸻

6.2 docker-compose（V1）

必须包含：
	•	api
	•	postgres

可选：
	•	nginx

V1 明确 不引入 Kubernetes。

⸻

7. 测试与质量底线

7.1 最低测试要求
	•	Service 层必须可测试
	•	Ledger 相关逻辑必须有单元测试

⸻

7.2 不追求目标
	•	不追求 100% 覆盖率
	•	不构建复杂 CI/CD 流水线

⸻

8. V1 明确边界（禁止事项）

Dot-Store V1 明确不做：
	•	规则引擎
	•	脚本系统
	•	多租户复杂隔离
	•	高并发优化
	•	企业级权限体系

⸻

9. 演进声明

允许未来演进方向：
	•	Event → Rule Engine
	•	代码级插件 → 配置化插件
	•	单体 → 拆分（在真实压力出现之后）

⸻

10. 开发者心智模型（最终原则）

Dot-Store 不是一个“约束老板行为”的系统，
而是一个“帮助老板理解自己生意”的系统。

任何技术决策，如果：
	•	让解释变困难
	•	让修正成本升高

即视为 错误决策。

⸻

本文档是 Dot-Store V1 的最终 Dev Guide。
所有实现、重构、评审必须以此为依据。