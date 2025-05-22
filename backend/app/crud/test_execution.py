from typing import List, Optional, Dict, Any, Union
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models.project import TestExecution, TestStepResult
from app.schemas.project import TestExecutionCreate, TestExecutionUpdate, TestStepResultCreate, TestStepResultUpdate
from app.core.enums.project import TestExecutionStatus, TestStepStatus

class CRUDTestExecution(CRUDBase[TestExecution, TestExecutionCreate, TestExecutionUpdate]):
    async def get_multi_by_test_case(
        self,
        db: AsyncSession,
        *,
        test_case_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[TestExecution]:
        """获取测试用例的所有执行记录"""
        query = select(TestExecution).where(
            TestExecution.test_case_id == test_case_id
        ).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_multi_by_device(
        self,
        db: AsyncSession,
        *,
        device_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[TestExecution]:
        """获取设备的所有执行记录"""
        query = select(TestExecution).where(
            TestExecution.device_id == device_id
        ).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def create_execution(
        self,
        db: AsyncSession,
        test_case_id: int,
        device_name: str
    ) -> TestExecution:
        """创建测试执行记录"""
        db_obj = TestExecution(
            test_case_id=test_case_id,
            status="running",
            start_time=datetime.utcnow(),
            device_name=device_name
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def update_execution_status(
        self,
        db: AsyncSession,
        execution_id: int,
        status: str,
        error_message: Optional[str] = None
    ) -> TestExecution:
        """更新测试执行状态"""
        db_obj = await self.get(db, execution_id)
        if not db_obj:
            return None
            
        db_obj.status = status
        db_obj.end_time = datetime.utcnow()
        db_obj.duration = int((db_obj.end_time - db_obj.start_time).total_seconds())
        if error_message:
            db_obj.error_message = error_message
            
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def create_step_result(
        self,
        db: AsyncSession,
        *,
        obj_in: TestStepResultCreate
    ) -> TestStepResult:
        """创建测试步骤结果"""
        db_obj = TestStepResult(**obj_in.dict())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def get_step_results(
        self,
        db: AsyncSession,
        *,
        execution_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[TestStepResult]:
        """获取执行记录的所有步骤结果"""
        query = select(TestStepResult).where(
            TestStepResult.test_execution_id == execution_id
        ).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_step_result(
        self,
        db: AsyncSession,
        *,
        execution_id: int,
        step_id: int
    ) -> Optional[TestStepResult]:
        """获取执行记录的指定步骤结果"""
        query = select(TestStepResult).where(
            TestStepResult.test_execution_id == execution_id,
            TestStepResult.test_step_id == step_id
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def update_step_result(
        self,
        db: AsyncSession,
        *,
        db_obj: TestStepResult,
        obj_in: Union[Dict[str, Any], TestStepResultUpdate]
    ) -> TestStepResult:
        """更新测试步骤结果"""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

test_execution_crud = CRUDTestExecution(TestExecution) 