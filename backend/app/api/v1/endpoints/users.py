# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.api.deps import get_db, get_current_user
# from app.schemas.user import UserResponse
#
# router = APIRouter()
#
# @router.get("/users/me", response_model=UserResponse)
# def get_current_user_info(
#     current_user: UserResponse = Depends(get_current_user)
# ):
#     """获取当前用户信息"""
#     return current_user