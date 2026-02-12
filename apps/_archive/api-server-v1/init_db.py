# 数据库初始化脚本
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

# 使用环境变量中的DATABASE_URL，如果没有则使用默认值
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dot_store.db")

# 从shared.db.base导入Base
from shared.db.base import Base

# 导入所有模型，确保它们被注册到Base.metadata中
from kernel.models import *
from platforms.models import *

# 创建数据库引擎
engine = create_engine(DATABASE_URL)

# 创建所有表结构
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created successfully!")
