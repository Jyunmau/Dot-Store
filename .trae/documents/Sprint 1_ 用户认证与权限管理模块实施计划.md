## Sprint 1 实施计划概述

根据开发测试整体计划和技术设计文档，Sprint 1 需要实现用户认证与权限管理模块。

### 一、项目重构准备

1. **清理旧代码**

   * 删除 `apps/api-server/` 目录下的旧代码

   * 删除 `apps/frontend/` 目录下的旧代码

   * 清理根目录下的旧配置文件（保留 `.gitignore`、`README.md`）

2. **新建项目结构**

   ```
   Dot-Store/
   ├── backend/                    # 后端服务（新目录）
   │   ├── app/
   │   │   ├── api/               # API路由
   │   │   │   ├── v1/
   │   │   │   │   ├── auth.py    # 认证接口
   │   │   │   │   └── permission.py # 权限接口
   │   │   ├── core/              # 核心配置
   │   │   ├── models/            # 数据模型
   │   │   ├── schemas/           # Pydantic模型
   │   │   ├── services/          # 业务服务
   │   │   └── main.py            # 应用入口
   │   ├── alembic/               # 数据库迁移
   │   ├── tests/                 # 测试文件
   │   ├── requirements.txt
   │   └── Dockerfile
   ├── frontend/                   # 前端应用（新目录）
   │   ├── src/
   │   │   ├── components/        # 公共组件
   │   │   ├── pages/             # 页面组件
   │   │   │   └── auth/          # 认证相关页面
   │   │   ├── services/          # API服务
   │   │   ├── store/             # Zustand状态管理
   │   │   ├── hooks/             # 自定义hooks
   │   │   ├── types/             # TypeScript类型
   │   │   └── App.tsx
   │   ├── package.json
   │   └── Dockerfile
   ├── docker-compose.yml
   └── README.md
   ```

### 二、后端开发任务

1. **项目初始化**

   * 创建 FastAPI 项目结构

   * 配置 SQLAlchemy + PostgreSQL

   * 配置 Redis 连接

   * 配置 Alembic 数据库迁移

2. **数据模型实现**

   * User 模型（用户表）

   * 数据库迁移脚本

3. **认证服务实现**

   * 用户注册服务（手机号/邮箱）

   * 用户登录服务（JWT Token生成）

   * Token验证服务

   * 密码加密（bcrypt）

   * 登录失败锁定机制

4. **权限服务实现**

   * 权限检查服务

   * 店员管理服务（添加/删除/更新权限）

5. **API接口实现**

   * `/api/v1/auth/register` - 用户注册

   * `/api/v1/auth/login` - 用户登录

   * `/api/v1/auth/logout` - 用户登出

   * `/api/v1/auth/refresh` - 刷新令牌

   * `/api/v1/auth/users/me` - 获取当前用户

   * `/api/v1/auth/staff` - 店员管理接口

### 三、前端开发任务

1. **项目初始化**

   * 创建 React + TypeScript + Vite 项目

   * 配置 Tailwind CSS

   * 配置路由（React Router）

   * 配置状态管理（Zustand）

2. **基础组件开发**

   * Button 组件（符合设计规范）

   * Input 组件

   * Card 组件

   * Form 组件

3. **认证页面开发**

   * 登录页面

   * 注册页面

   * 店员管理页面（店主权限）

4. **状态管理实现**

   * AuthStore（认证状态）

   * Token管理

   * 自动刷新机制

5. **API服务封装**

   * Axios 实例配置

   * 请求/响应拦截器

   * 认证相关API

### 四、Docker配置

1. **后端Dockerfile**
2. **前端Dockerfile**
3. **docker-compose.yml**（PostgreSQL + Redis + API + Frontend）

### 五、测试任务

1. **后端单元测试**

   * 用户模型测试

   * 认证服务测试

   * 权限服务测试

2. **前端组件测试**

   * 登录组件测试

   * 注册组件测试

### 六、文档更新

1. **更新README.md**

   * 项目介绍

   * 技术栈说明

   * 项目结构说明

   * 开发环境搭建

   * 部署说明

### 实施顺序

1. 清理旧代码和配置
2. 创建新的项目结构
3. 后端项目初始化和配置
4. 后端数据模型和迁移
5. 后端认证服务实现
6. 后端API接口实现
7. 前端项目初始化和配置
8. 前端基础组件开发
9. 前端认证页面开发
10. 前后端联调
11. Docker配置
12. 测试编写
13. 文档更新

