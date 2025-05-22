from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Body, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.execution_service import ExecutionService
from app.core.enums.project import ExecutionStatus
from app.core.exceptions import ExecutionError
from app.core.deps import get_db

router = APIRouter()

@router.post("/run")
async def run_test(
    *,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    test_id: str = Body(...),
    device_id: str = Body(...),
    environment: str = Body(...)
) -> Dict[str, Any]:
    """
    运行测试
    
    Args:
        background_tasks: 后台任务
        test_id: 测试ID
        device_id: 设备ID
        environment: 环境名称
        
    Returns:
        Dict[str, Any]: 执行结果
    """
    execution_service = ExecutionService(db)
    try:
        execution = await execution_service.run_test(
            test_id,
            device_id,
            environment,
            background_tasks
        )
        return {
            "message": "测试开始执行",
            "execution": execution.to_dict()
        }
    except ExecutionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/run-suite")
async def run_test_suite(
    *,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    suite_id: str = Body(...),
    device_id: str = Body(...),
    environment: str = Body(...)
) -> Dict[str, Any]:
    """
    运行测试套件
    
    Args:
        background_tasks: 后台任务
        suite_id: 套件ID
        device_id: 设备ID
        environment: 环境名称
        
    Returns:
        Dict[str, Any]: 执行结果
    """
    execution_service = ExecutionService(db)
    try:
        executions = await execution_service.run_test_suite(
            suite_id,
            device_id,
            environment,
            background_tasks
        )
        return {
            "message": "测试套件开始执行",
            "executions": [execution.to_dict() for execution in executions]
        }
    except ExecutionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stop")
async def stop_execution(
    *,
    db: AsyncSession = Depends(get_db),
    execution_id: str = Body(...)
) -> Dict[str, Any]:
    """
    停止执行
    
    Args:
        execution_id: 执行ID
        
    Returns:
        Dict[str, Any]: 停止结果
    """
    execution_service = ExecutionService(db)
    try:
        await execution_service.stop_execution(execution_id)
        return {
            "message": "执行已停止"
        }
    except ExecutionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{execution_id}")
async def get_execution(
    *,
    db: AsyncSession = Depends(get_db),
    execution_id: str
) -> Dict[str, Any]:
    """
    获取执行信息
    
    Args:
        execution_id: 执行ID
        
    Returns:
        Dict[str, Any]: 执行信息
    """
    execution_service = ExecutionService(db)
    try:
        execution = await execution_service.get_execution(execution_id)
        if not execution:
            raise HTTPException(status_code=404, detail=f"执行不存在: {execution_id}")
        return execution.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{execution_id}/status")
async def get_execution_status(
    *,
    db: AsyncSession = Depends(get_db),
    execution_id: str
) -> Dict[str, Any]:
    """
    获取执行状态
    
    Args:
        execution_id: 执行ID
        
    Returns:
        Dict[str, Any]: 执行状态
    """
    execution_service = ExecutionService(db)
    try:
        status = await execution_service.get_execution_status(execution_id)
        if not status:
            raise HTTPException(status_code=404, detail=f"执行不存在: {execution_id}")
        return {
            "status": status.value
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{execution_id}/result")
async def get_execution_result(
    *,
    db: AsyncSession = Depends(get_db),
    execution_id: str
) -> Dict[str, Any]:
    """
    获取执行结果
    
    Args:
        execution_id: 执行ID
        
    Returns:
        Dict[str, Any]: 执行结果
    """
    execution_service = ExecutionService(db)
    try:
        result = await execution_service.get_execution_result(execution_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"执行不存在: {execution_id}")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def get_all_executions(
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取所有执行
    
    Returns:
        Dict[str, Any]: 执行列表
    """
    execution_service = ExecutionService(db)
    try:
        executions = await execution_service.get_all_executions()
        return {
            "executions": [execution.to_dict() for execution in executions]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{status}")
async def get_executions_by_status(
    *,
    db: AsyncSession = Depends(get_db),
    status: ExecutionStatus
) -> Dict[str, Any]:
    """
    获取指定状态的执行
    
    Args:
        status: 执行状态
        
    Returns:
        Dict[str, Any]: 执行列表
    """
    execution_service = ExecutionService(db)
    try:
        executions = await execution_service.get_executions_by_status(status)
        return {
            "executions": [execution.to_dict() for execution in executions]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/test/{test_id}")
async def get_test_executions(
    *,
    db: AsyncSession = Depends(get_db),
    test_id: str
) -> Dict[str, Any]:
    """
    获取测试的执行
    
    Args:
        test_id: 测试ID
        
    Returns:
        Dict[str, Any]: 执行列表
    """
    execution_service = ExecutionService(db)
    try:
        executions = await execution_service.get_test_executions(test_id)
        return {
            "executions": [execution.to_dict() for execution in executions]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/suite/{suite_id}")
async def get_suite_executions(
    *,
    db: AsyncSession = Depends(get_db),
    suite_id: str
) -> Dict[str, Any]:
    """
    获取套件的执行
    
    Args:
        suite_id: 套件ID
        
    Returns:
        Dict[str, Any]: 执行列表
    """
    execution_service = ExecutionService(db)
    try:
        executions = await execution_service.get_suite_executions(suite_id)
        return {
            "executions": [execution.to_dict() for execution in executions]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 