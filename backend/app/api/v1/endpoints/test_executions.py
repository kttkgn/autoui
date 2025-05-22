from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Response
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.crud.test_case import test_case_crud
from app.crud.test_execution import test_execution_crud
from app.schemas.project import (
    TestExecutionCreate,
    TestExecutionResponse,
    TestExecutionResultResponse,
    TestExecutionSummary,
    TestStepResult
)
from app.services.test_executor import create_test_executor
from app.tasks.test_execution import execute_test_case_task, generate_test_report_task
from app.utils.report_generator import ReportGenerator
from datetime import datetime
from app.core.logger import logger

router = APIRouter()

@router.post("/test-cases/{test_case_id}/execute", response_model=TestExecutionResponse)
async def create_test_execution(
    test_case_id: int,
    device_id: str,
    background_tasks: BackgroundTasks
):
    """
    创建并执行测试用例
    """
    try:
        # 创建测试执行记录
        executor = create_test_executor(test_case_id, device_id)
        # 异步执行测试用例
        task = execute_test_case_task.delay(test_case_id, device_id)
        return {"task_id": task.id, "message": "测试用例已提交执行"}
    except Exception as e:
        logger.error(f"创建测试执行失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/executions/{execution_id}", response_model=TestExecutionResponse)
async def get_execution_result(execution_id: int):
    """
    获取测试执行结果
    """
    try:
        executor = create_test_executor(execution_id=execution_id)
        return executor.execution
    except Exception as e:
        logger.error(f"获取执行结果失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/executions/{execution_id}/steps", response_model=List[TestExecutionResultResponse])
async def get_step_results(execution_id: int):
    """
    获取测试步骤执行结果
    """
    try:
        executor = create_test_executor(execution_id=execution_id)
        return executor.step_results
    except Exception as e:
        logger.error(f"获取步骤结果失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/executions/{execution_id}/start")
async def start_execution(execution_id: int):
    """
    开始执行测试
    """
    try:
        executor = create_test_executor(execution_id=execution_id)
        if executor.execution.status != "pending":
            raise HTTPException(status_code=400, detail="测试执行状态不正确")
        task = execute_test_case_task.delay(executor.test_case_id, executor.device_id)
        return {"task_id": task.id, "message": "测试执行已开始"}
    except Exception as e:
        logger.error(f"开始测试执行失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/executions/{execution_id}/stop")
async def stop_execution(execution_id: int):
    """
    停止测试执行
    """
    try:
        executor = create_test_executor(execution_id=execution_id)
        if executor.execution.status != "running":
            raise HTTPException(status_code=400, detail="测试执行未在运行")
        executor.stop()
        return {"message": "测试执行已停止"}
    except Exception as e:
        logger.error(f"停止测试执行失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/test-cases/{test_case_id}/history", response_model=List[TestExecutionResponse])
async def get_execution_history(test_case_id: int):
    """
    获取测试用例执行历史
    """
    try:
        executor = create_test_executor(test_case_id=test_case_id)
        return executor.get_execution_history()
    except Exception as e:
        logger.error(f"获取执行历史失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/projects/{project_id}/summary", response_model=TestExecutionSummary)
async def get_project_execution_summary(project_id: int):
    """
    获取项目测试执行汇总报告
    """
    try:
        executor = create_test_executor()
        return executor.generate_project_summary(project_id)
    except Exception as e:
        logger.error(f"获取项目执行汇总失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/projects/{project_id}/export")
async def export_project_summary(
    project_id: int,
    format: str = "pdf"
):
    """
    导出项目测试执行汇总报告
    """
    try:
        executor = create_test_executor()
        report_path = executor.export_project_summary(project_id, format)
        return {"report_url": report_path}
    except Exception as e:
        logger.error(f"导出项目执行汇总失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/project/{execution_id}/steps", response_model=List[TestStepResult])
async def get_step_results(
    execution_id: int,
    db: AsyncSession = Depends(get_db)
):
    """获取测试步骤结果"""
    execution = await test_execution_crud.get(db, execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail="执行记录不存在")
    return execution.step_results

@router.get("/test-case/{test_case_id}/history", response_model=List[TestExecutionResponse])
async def get_execution_history(
    test_case_id: int,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """获取测试用例的执行历史"""
    test_case = await test_case_crud.get(db, test_case_id)
    if not test_case:
        raise HTTPException(status_code=404, detail="测试用例不存在")
    
    return await test_execution_crud.get_multi_by_test_case(db, test_case_id, skip, limit)

@router.get("/project/{project_id}/summary", response_model=TestExecutionSummary)
async def get_project_execution_summary(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    """获取项目测试执行摘要"""
    executions = await test_execution_crud.get_multi_by_project(db, project_id)
    
    report_generator = ReportGenerator()
    report_url = await report_generator.generate_summary_report(
        project_id=project_id,
        executions=executions
    )
    
    total = len(executions)
    success = sum(1 for e in executions if e.status == "success")
    failed = sum(1 for e in executions if e.status == "failed")
    running = sum(1 for e in executions if e.status == "running")
    
    return {
        "total": total,
        "success": success,
        "failed": failed,
        "running": running,
        "report_url": report_url,
        "executions": executions
    }

@router.get("/project/{project_id}/report")
async def export_project_summary(
    project_id: int,
    format: str = "pdf",
    db: AsyncSession = Depends(get_db)
):
    """导出项目测试报告"""
    executions = await test_execution_crud.get_multi_by_project(db, project_id)
    
    report_generator = ReportGenerator()
    report_path = await report_generator.generate_summary_report(
        project_id=project_id,
        executions=executions
    )
    
    return FileResponse(
        report_path,
        media_type="application/pdf",
        filename=f"project_{project_id}_report.pdf"
    ) 