# 使用多阶段构建：第一阶段 - 构建依赖
FROM python:3.11-alpine AS build-stage

# 设置工作目录
WORKDIR /app

# 复制requirements.txt到工作目录
COPY ./apps/api-server/requirements.txt .

# 安装依赖（使用--no-cache-dir减少镜像大小，使用--root-user-action=ignore避免权限问题）
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

# 第二阶段 - 运行应用
FROM python:3.11-alpine AS production-stage

# 设置工作目录
WORKDIR /app

# 复制依赖
COPY --from=build-stage /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=build-stage /usr/local/bin /usr/local/bin

# 复制应用代码（仅复制必要的文件）
COPY ./apps/api-server/main.py ./apps/api-server/
COPY ./apps/api-server/alembic ./alembic/
COPY ./apps/api-server/alembic.ini .

# 复制新的目录结构（已迁移到apps/api-server下）
COPY ./apps/api-server/kernel ./kernel/
COPY ./apps/api-server/platforms ./platforms/
COPY ./apps/api-server/script ./script/

# 复制共享组件（已迁移到apps/api-server下）
COPY ./apps/api-server/shared ./shared/

# 暴露端口
EXPOSE 8000

# 运行应用
CMD ["uvicorn", "apps.api-server.main:app", "--host", "0.0.0.0", "--port", "8000"]
