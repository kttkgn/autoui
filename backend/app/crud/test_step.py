from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models.project import TestStep
from app.schemas.project import TestStepCreate, TestStepUpdate

class CRUDTestStep(CRUDBase[TestStep, TestStepCreate, TestStepUpdate]):
    async def get_multi_by_test_case(
        self,
        db: AsyncSession,
        test_case_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[TestStep]:
        """获取测试用例的所有步骤"""
        query = select(TestStep).where(
            TestStep.test_case_id == test_case_id
        ).order_by(TestStep.step_number)
        
        if skip:
            query = query.offset(skip)
        if limit:
            query = query.limit(limit)
            
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_by_step_number(
        self,
        db: AsyncSession,
        test_case_id: int,
        step_number: int
    ) -> Optional[TestStep]:
        """根据步骤号获取测试步骤"""
        query = select(TestStep).where(
            TestStep.test_case_id == test_case_id,
            TestStep.step_number == step_number
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def create(
        self,
        db: AsyncSession,
        test_case_id: int,
        obj_in: TestStepCreate
    ) -> TestStep:
        """创建测试步骤"""
        db_obj = TestStep(
            test_case_id=test_case_id,
            step_number=obj_in.step_number,
            action=obj_in.action,
            element=obj_in.element,
            value=obj_in.value
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def update(
        self,
        db: AsyncSession,
        test_case_id: int,
        step_number: int,
        obj_in: TestStepUpdate
    ) -> TestStep:
        """更新测试步骤"""
        db_obj = await self.get_by_step_number(db, test_case_id, step_number)
        if not db_obj:
            return None
            
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
            
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def remove(
        self,
        db: AsyncSession,
        test_case_id: int,
        step_number: int
    ) -> None:
        """删除测试步骤"""
        db_obj = await self.get_by_step_number(db, test_case_id, step_number)
        if db_obj:
            await db.delete(db_obj)
            await db.commit()
            
            # 重新编号后续步骤
            steps = await self.get_multi_by_test_case(db, test_case_id)
            for i, step in enumerate(steps, 1):
                step.step_number = i
            await db.commit()
    
    async def reorder_steps(
        self,
        db: AsyncSession,
        test_case_id: int,
        step_numbers: List[int]
    ) -> None:
        """重排序测试步骤"""
        steps = await self.get_multi_by_test_case(db, test_case_id)
        step_map = {step.step_number: step for step in steps}
        
        # 更新步骤顺序
        for i, step_number in enumerate(step_numbers, 1):
            step = step_map[step_number]
            step.step_number = i
            
        await db.commit()

test_step_crud = CRUDTestStep(TestStep) 