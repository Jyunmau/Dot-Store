FROM python:3.11-alpine

WORKDIR /app

# 安装依赖
COPY ./apps/api-server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . /app

# 暴露端口
EXPOSE 8000

# 运行应用
CMD ["uvicorn", "apps.api-server.main:app", "--host", "0.0.0.0", "--port", "8000"]
