from typing import Dict, Any, List, Optional
from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.test_execution import test_execution_crud
from app.crud.test_case import test_case_crud
from app.crud.test_suite import test_suite_crud
from app.models.project import TestExecution
from app.schemas.project import TestExecutionCreate, TestExecutionUpdate, TestStepResultCreate
from app.core.enums.project import TestExecutionStatus, TestStepStatus, ExecutionStatus
from app.services.test_executor import execute_test_case
from app.core.exceptions import ExecutionError
from app.services.device_service import DeviceService
from app.services.report_service import ReportService
from app.core.config import settings
import asyncio
import json
import os
from datetime import datetime

class ExecutionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def run_test(
        self,
        test_id: str,
        device_id: str,
        environment: str,
        background_tasks: BackgroundTasks
    ) -> TestExecution:
        """
        运行测试
        
        Args:
            test_id: 测试ID
            device_id: 设备ID
            environment: 环境名称
            background_tasks: 后台任务
            
        Returns:
            TestExecution: 执行记录
        """
        # 创建执行记录
        execution = await test_execution_crud.create(
            self.db,
            test_id=test_id,
            device_id=device_id,
            environment=environment,
            status=ExecutionStatus.PENDING
        )
        
        # 添加后台任务
        background_tasks.add_task(execute_test_case, self.db, execution.id)
        
        return execution

    async def run_test_suite(
        self,
        suite_id: str,
        device_id: str,
        environment: str,
        background_tasks: BackgroundTasks
    ) -> List[TestExecution]:
        """
        运行测试套件
        
        Args:
            suite_id: 套件ID
            device_id: 设备ID
            environment: 环境名称
            background_tasks: 后台任务
            
        Returns:
            List[TestExecution]: 执行记录列表
        """
        # 获取套件中的测试用例
        suite = await test_suite_crud.get(self.db, suite_id)
        if not suite:
            raise ExecutionError(f"测试套件不存在: {suite_id}")
            
        executions = []
        for test_case in suite.test_cases:
            # 为每个测试用例创建执行记录
            execution = await test_execution_crud.create(
                self.db,
                test_id=test_case.id,
                device_id=device_id,
                environment=environment,
                status=ExecutionStatus.PENDING
            )
            executions.append(execution)
            
            # 添加后台任务
            background_tasks.add_task(execute_test_case, self.db, execution.id)
            
        return executions

    async def stop_execution(self, execution_id: str) -> None:
        """
        停止执行
        
        Args:
            execution_id: 执行ID
        """
        execution = await test_execution_crud.get(self.db, execution_id)
        if not execution:
            raise ExecutionError(f"执行记录不存在: {execution_id}")
            
        if execution.status not in [ExecutionStatus.RUNNING, ExecutionStatus.PENDING]:
            raise ExecutionError(f"执行状态不允许停止: {execution.status}")
            
        await test_execution_crud.update_status(
            self.db,
            execution_id,
            ExecutionStatus.STOPPED
        )

    async def get_execution(self, execution_id: str) -> Optional[TestExecution]:
        """
        获取执行记录
        
        Args:
            execution_id: 执行ID
            
        Returns:
            Optional[TestExecution]: 执行记录
        """
        return await test_execution_crud.get(self.db, execution_id)

    async def get_execution_status(self, execution_id: str) -> Optional[ExecutionStatus]:
        """
        获取执行状态
        
        Args:
            execution_id: 执行ID
            
        Returns:
            Optional[ExecutionStatus]: 执行状态
        """
        execution = await test_execution_crud.get(self.db, execution_id)
        return execution.status if execution else None

    async def get_execution_result(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """
        获取执行结果
        
        Args:
            execution_id: 执行ID
            
        Returns:
            Optional[Dict[str, Any]]: 执行结果
        """
        execution = await test_execution_crud.get(self.db, execution_id)
        if not execution:
            return None
            
        return {
            "id": execution.id,
            "test_id": execution.test_id,
            "device_id": execution.device_id,
            "environment": execution.environment,
            "status": execution.status.value,
            "start_time": execution.start_time,
            "end_time": execution.end_time,
            "duration": execution.duration,
            "error_message": execution.error_message,
            "step_results": [
                {
                    "step_number": result.step_number,
                    "action": result.action,
                    "element": result.element,
                    "value": result.value,
                    "status": result.status,
                    "message": result.message,
                    "screenshot": result.screenshot
                }
                for result in execution.step_results
            ]
        }

    async def get_all_executions(self) -> List[TestExecution]:
        """
        获取所有执行记录
        
        Returns:
            List[TestExecution]: 执行记录列表
        """
        return await test_execution_crud.get_all(self.db)

    async def get_executions_by_status(self, status: ExecutionStatus) -> List[TestExecution]:
        """
        获取指定状态的执行记录
        
        Args:
            status: 执行状态
            
        Returns:
            List[TestExecution]: 执行记录列表
        """
        return await test_execution_crud.get_by_status(self.db, status)

    async def get_test_executions(self, test_id: str) -> List[TestExecution]:
        """
        获取测试的执行历史
        
        Args:
            test_id: 测试ID
            
        Returns:
            List[TestExecution]: 执行记录列表
        """
        return await test_execution_crud.get_by_test_id(self.db, test_id)

    async def get_suite_executions(self, suite_id: str) -> List[TestExecution]:
        """
        获取测试套件的执行历史
        
        Args:
            suite_id: 套件ID
            
        Returns:
            List[TestExecution]: 执行记录列表
        """
        return await test_execution_crud.get_by_suite_id(self.db, suite_id) 