"""
Dot-Store V2.1 文件上传API路由
"""
import os
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.schemas.transaction import UploadResponse
from app.models.user import User

router = APIRouter(prefix="/upload", tags=["文件上传"])

UPLOAD_DIR = "uploads"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024


def ensure_upload_dir():
    """
    确保上传目录存在
    """
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)


def get_file_extension(filename: str) -> str:
    """
    获取文件扩展名
    """
    return os.path.splitext(filename)[1].lower()


def generate_filename(original_filename: str) -> str:
    """
    生成唯一文件名
    """
    ext = get_file_extension(original_filename)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = uuid.uuid4().hex[:8]
    return f"{timestamp}_{unique_id}{ext}"


@router.post("/attachment", response_model=UploadResponse, summary="上传凭证图片")
async def upload_attachment(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
):
    """
    上传凭证图片接口
    
    - 支持的图片格式：jpg, jpeg, png, gif, webp
    - 最大文件大小：5MB
    - 返回图片URL和文件名
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="文件名不能为空"
        )

    ext = get_file_extension(file.filename)
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"不支持的文件格式，支持的格式：{', '.join(ALLOWED_EXTENSIONS)}",
        )

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"文件大小超过限制，最大支持{MAX_FILE_SIZE // (1024 * 1024)}MB",
        )

    ensure_upload_dir()

    filename = generate_filename(file.filename)
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(content)

    url = f"/uploads/{filename}"

    return UploadResponse(url=url, filename=file.filename)
