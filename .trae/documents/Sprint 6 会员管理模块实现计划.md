## Sprint 6: 会员管理模块实现计划

### 一、后端开发

#### 1. 数据模型 (`apps/api-server/app/models/member.py`)
- `Member` 模型：会员信息（id, user_id, name, phone, level, points, created_at, updated_at）
- `PointsRecord` 模型：积分记录（id, member_id, user_id, type, points, reason, created_at）
- `PointsExchange` 模型：积分兑换（id, member_id, user_id, points, amount, created_at）

#### 2. Pydantic模式 (`apps/api-server/app/schemas/member.py`)
- `MemberCreate`, `MemberUpdate`, `MemberResponse`, `MemberListResponse`
- `PointsAddParams`, `PointsSubtractParams`, `PointsRecordResponse`
- `PointsExchangeParams`, `PointsExchangeResponse`

#### 3. 服务层 (`apps/api-server/app/services/member_service.py`)
- `MemberService`：会员CRUD操作
- `PointsService`：积分增减、兑换、记录查询

#### 4. API路由 (`apps/api-server/app/api/v1/member.py`)
- `POST /members` - 创建会员
- `GET /members` - 获取会员列表
- `GET /members/{id}` - 获取会员详情
- `PUT /members/{id}` - 更新会员
- `DELETE /members/{id}` - 删除会员
- `POST /members/points/add` - 增加积分
- `POST /members/points/subtract` - 减少积分
- `GET /members/points/{member_id}` - 获取会员积分记录
- `POST /members/exchange` - 积分兑换
- `GET /members/exchanges` - 获取积分兑换记录

### 二、前端开发

#### 1. 类型定义 (`apps/frontend/src/types/member.ts`)
- `Member`, `PointsRecord`, `PointsExchange` 接口
- 创建/更新参数类型

#### 2. API服务 (`apps/frontend/src/services/memberService.ts`)
- 会员CRUD API调用
- 积分操作API调用
- 积分兑换API调用

#### 3. 状态管理 (`apps/frontend/src/store/memberStore.ts`)
- 会员列表、当前会员
- 积分记录、兑换记录
- 加载状态、错误处理

#### 4. 页面组件
- `MemberList.tsx` - 会员列表页面（增删改查）
- `PointsRecord.tsx` - 积分记录页面（增加/减少积分）
- `PointsExchange.tsx` - 积分兑换页面

#### 5. 路由配置
- 更新 `App.tsx` 添加会员管理路由

### 三、测试与验证

1. 启动前后端服务
2. 测试会员管理功能（添加、编辑、删除、查看）
3. 测试积分操作（增加、减少、记录查看）
4. 测试积分兑换功能
5. 修复发现的BUG

### 四、文档更新

1. 更新 `README.md` 添加Sprint 6功能说明
2. 更新API接口文档

### 五、提交代码

1. 停止运行的服务
2. Git提交代码