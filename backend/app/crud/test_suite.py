from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models.project import TestSuite
from app.schemas.project import TestSuiteCreate, TestSuiteUpdate

class CRUDTestSuite(CRUDBase[TestSuite, TestSuiteCreate, TestSuiteUpdate]):
    async def get_multi_by_project(
        self,
        db: AsyncSession,
        *,
        project_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[TestSuite]:
        """获取项目的所有测试套件"""
        query = select(TestSuite).where(
            TestSuite.project_id == project_id
        ).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_by_name(
        self,
        db: AsyncSession,
        *,
        project_id: int,
        name: str
    ) -> Optional[TestSuite]:
        """通过名称获取测试套件"""
        query = select(TestSuite).where(
            TestSuite.project_id == project_id,
            TestSuite.name == name
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()

test_suite_crud = CRUDTestSuite(TestSuite) 