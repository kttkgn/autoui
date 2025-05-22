from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.user import UserResponse

router = APIRouter()

@router.get("/tasks/", response_model=list[dict])
def get_tasks(
    db: Session = Depends(get_db),
):
    """获取任务列表"""
    # 这里添加获取任务列表的逻辑
    return []

@router.post("/tasks/", response_model=dict)
def create_task(
    *,
    db: Session = Depends(get_db),
    task_data: dict
):
    """创建新任务"""
    # 这里添加创建任务的逻辑
    return {"message": "任务已创建"} 