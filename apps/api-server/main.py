from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 创建 FastAPI 应用
app = FastAPI(
    title="Dot-Store API",
    description="Dot-Store V1 API Documentation",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 根路由
@app.get("/")
def read_root():
    return {"message": "Welcome to Dot-Store API"}

# 健康检查
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# 导入路由（使用相对导入）
from routes import api_router

# 注册 API 路由
app.include_router(api_router, prefix="/api")
