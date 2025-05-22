from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models.project import TestCase
from app.schemas.project import TestCaseCreate, TestCaseUpdate

class CRUDTestCase(CRUDBase[TestCase, TestCaseCreate, TestCaseUpdate]):
    async def get_multi_by_suite(
        self,
        db: AsyncSession,
        *,
        test_suite_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[TestCase]:
        """获取指定测试套件的测试用例列表"""
        query = select(self.model).where(
            self.model.suite_id == test_suite_id
        ).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

test_case_crud = CRUDTestCase(TestCase) 