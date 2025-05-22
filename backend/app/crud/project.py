from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.crud.base import CRUDBase
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate

class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Project]:
        result = await db.execute(select(Project).filter(Project.name == name))
        return result.scalar_one_or_none()

    async def get_multi_by_project(
        self, db: AsyncSession, *, project_id: int, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        result = await db.execute(
            select(Project)
            .filter(Project.id == project_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

project_crud = CRUDProject(Project) 