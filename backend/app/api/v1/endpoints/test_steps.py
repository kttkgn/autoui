from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_db
from app.crud.test_case import test_case_crud
from app.crud.test_step import test_step_crud
from app.schemas.project import TestStepCreate, TestStepUpdate, TestStepResponse

router = APIRouter()

@router.get("/{test_case_id}", response_model=List[TestStepResponse])
async def get_test_steps(
    test_case_id: int,
    db: AsyncSession = Depends(get_db)
):
    """获取测试步骤列表"""
    test_case = await test_case_crud.get(db, test_case_id)
    if not test_case:
        raise HTTPException(status_code=404, detail="测试用例不存在")
    return await test_step_crud.get_multi_by_test_case(db, test_case_id)

@router.post("/{test_case_id}", response_model=TestStepResponse)
async def create_test_step(
    test_case_id: int,
    test_step_in: TestStepCreate,
    db: AsyncSession = Depends(get_db)
):
    """创建测试步骤"""
    test_case = await test_case_crud.get(db, test_case_id)
    if not test_case:
        raise HTTPException(status_code=404, detail="测试用例不存在")
    
    # 获取当前最大步骤号
    steps = await test_step_crud.get_multi_by_test_case(db, test_case_id)
    max_step_number = max([step.step_number for step in steps], default=0)
    
    # 创建新步骤，步骤号加1
    test_step_in.step_number = max_step_number + 1
    return await test_step_crud.create(db, test_case_id, test_step_in)

@router.put("/{test_case_id}/{step_number}", response_model=TestStepResponse)
async def update_test_step(
    test_case_id: int,
    step_number: int,
    test_step_in: TestStepUpdate,
    db: AsyncSession = Depends(get_db)
):
    """更新测试步骤"""
    test_step = await test_step_crud.get_by_step_number(db, test_case_id, step_number)
    if not test_step:
        raise HTTPException(status_code=404, detail="测试步骤不存在")
    return await test_step_crud.update(db, test_case_id, step_number, test_step_in)

@router.delete("/{test_case_id}/{step_number}")
async def delete_test_step(
    test_case_id: int,
    step_number: int,
    db: AsyncSession = Depends(get_db)
):
    """删除测试步骤"""
    test_step = await test_step_crud.get_by_step_number(db, test_case_id, step_number)
    if not test_step:
        raise HTTPException(status_code=404, detail="测试步骤不存在")
    
    await test_step_crud.remove(db, test_case_id, step_number)
    return {"message": "删除成功"}

@router.put("/{test_case_id}/reorder")
async def reorder_test_steps(
    test_case_id: int,
    step_numbers: List[int],
    db: AsyncSession = Depends(get_db)
):
    """重排序测试步骤"""
    test_case = await test_case_crud.get(db, test_case_id)
    if not test_case:
        raise HTTPException(status_code=404, detail="测试用例不存在")
    
    # 验证步骤号列表
    steps = await test_step_crud.get_multi_by_test_case(db, test_case_id)
    existing_step_numbers = {step.step_number for step in steps}
    if set(step_numbers) != existing_step_numbers:
        raise HTTPException(status_code=400, detail="步骤号列表不匹配")
    
    # 更新步骤顺序
    await test_step_crud.reorder_steps(db, test_case_id, step_numbers)
    return {"message": "重排序成功"} 