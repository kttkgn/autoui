from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_db
from app.schemas.project import TestCaseCreate, TestCaseResponse
from app.crud.test_case import test_case_crud
from app.core.test_engine import DataDrivenTestEngine, KeywordDrivenTestEngine

router = APIRouter()

@router.get("/test-suites/{test_suite_id}/test-cases", response_model=List[TestCaseResponse])
async def get_test_cases(
    test_suite_id: int,
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """获取测试用例列表"""
    return await test_case_crud.get_multi_by_suite(db, test_suite_id=test_suite_id, skip=skip, limit=limit)

@router.post("/test-suites/{test_suite_id}/test-cases", response_model=TestCaseResponse)
async def create_test_case(
    *,
    db: AsyncSession = Depends(get_db),
    test_suite_id: int,
    test_case_in: TestCaseCreate
):
    """创建新测试用例"""
    return await test_case_crud.create(db, obj_in=test_case_in)

@router.get("/{test_case_id}", response_model=TestCaseResponse)
async def get_test_case(
    test_case_id: int,
    db: AsyncSession = Depends(get_db)
):
    """获取测试用例详情"""
    test_case = await test_case_crud.get(db, id=test_case_id)
    if not test_case:
        raise HTTPException(status_code=404, detail="测试用例不存在")
    return test_case

@router.put("/{test_case_id}", response_model=TestCaseResponse)
async def update_test_case(
    *,
    db: AsyncSession = Depends(get_db),
    test_case_id: int,
    test_case_in: TestCaseCreate
):
    """更新测试用例"""
    test_case = await test_case_crud.get(db, id=test_case_id)
    if not test_case:
        raise HTTPException(status_code=404, detail="测试用例不存在")
    return await test_case_crud.update(db, db_obj=test_case, obj_in=test_case_in)

@router.delete("/{test_case_id}")
async def delete_test_case(
    *,
    db: AsyncSession = Depends(get_db),
    test_case_id: int
):
    """删除测试用例"""
    test_case = await test_case_crud.get(db, id=test_case_id)
    if not test_case:
        raise HTTPException(status_code=404, detail="测试用例不存在")
    await test_case_crud.remove(db, id=test_case_id)
    return {"message": "测试用例已删除"}

@router.post("/{test_case_id}/execute")
async def execute_test_case(
    *,
    db: AsyncSession = Depends(get_db),
    test_case_id: int,
    data: Optional[Dict[str, Any]] = None,
    engine_type: str = "data_driven"
):
    """
    执行测试用例
    
    Args:
        test_case_id: 测试用例ID
        data: 数据驱动参数
        engine_type: 执行引擎类型（data_driven/keyword_driven）
    """
    test_case = await test_case_crud.get(db, id=test_case_id)
    if not test_case:
        raise HTTPException(status_code=404, detail="测试用例不存在")
    
    if engine_type == "data_driven":
        engine = DataDrivenTestEngine()
    elif engine_type == "keyword_driven":
        engine = KeywordDrivenTestEngine()
    else:
        raise HTTPException(status_code=400, detail="不支持的执行引擎类型")
    
    result = engine.execute(test_case, data)
    return result

@router.post("/{test_case_id}/execute/keyword")
async def execute_keyword_test_case(
    *,
    db: AsyncSession = Depends(get_db),
    test_case_id: int,
    keyword: str,
    params: Optional[Dict[str, Any]] = None
):
    """
    执行关键字驱动测试用例
    
    Args:
        test_case_id: 测试用例ID
        keyword: 关键字
        params: 关键字参数
    """
    test_case = await test_case_crud.get(db, id=test_case_id)
    if not test_case:
        raise HTTPException(status_code=404, detail="测试用例不存在")
    
    engine = KeywordDrivenTestEngine()
    result = engine.execute(test_case, {"keyword": keyword, "params": params})
    return result

@router.post("/{test_case_id}/execute/data")
async def execute_data_driven_test_case(
    *,
    db: AsyncSession = Depends(get_db),
    test_case_id: int,
    data: List[Dict[str, Any]]
):
    """
    执行数据驱动测试用例
    
    Args:
        test_case_id: 测试用例ID
        data: 数据驱动参数列表
    """
    test_case = await test_case_crud.get(db, id=test_case_id)
    if not test_case:
        raise HTTPException(status_code=404, detail="测试用例不存在")
    
    engine = DataDrivenTestEngine()
    results = []
    for item in data:
        result = engine.execute(test_case, item)
        results.append(result)
    
    return {"test_case": test_case, "results": results}

@router.post("/{test_case_id}/execute/batch")
async def execute_batch_test_case(
    *,
    db: AsyncSession = Depends(get_db),
    test_case_id: int,
    data_list: List[Dict[str, Any]],
    engine_type: str = "data_driven"
):
    """
    批量执行测试用例
    
    Args:
        test_case_id: 测试用例ID
        data_list: 数据驱动参数列表
        engine_type: 执行引擎类型（data_driven/keyword_driven）
    """
    test_case = await test_case_crud.get(db, id=test_case_id)
    if not test_case:
        raise HTTPException(status_code=404, detail="测试用例不存在")
    
    if engine_type == "data_driven":
        engine = DataDrivenTestEngine()
    elif engine_type == "keyword_driven":
        engine = KeywordDrivenTestEngine()
    else:
        raise HTTPException(status_code=400, detail="不支持的执行引擎类型")
    
    results = []
    for data in data_list:
        result = engine.execute(test_case, data)
        results.append(result)
    
    return {"test_case": test_case, "results": results} 