from app.crud.project import project_crud
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.core.exceptions import ResourceNotFoundError

class ProjectService:
    """项目服务"""
    
    async def create_project(self, project: ProjectCreate) -> ProjectResponse:
        """创建项目"""
        return await project_crud.create(project)
    
    async def get_project(self, project_id: int) -> ProjectResponse:
        """获取项目"""
        project = await project_crud.get(project_id)
        if not project:
            raise ResourceNotFoundError(f"项目不存在: {project_id}")
        return project
    
    async def update_project(self, project_id: int, project: ProjectUpdate) -> ProjectResponse:
        """更新项目"""
        project = await project_crud.update(project_id, project)
        if not project:
            raise ResourceNotFoundError(f"项目不存在: {project_id}")
        return project
    
    async def delete_project(self, project_id: int) -> None:
        """删除项目"""
        project = await project_crud.delete(project_id)
        if not project:
            raise ResourceNotFoundError(f"项目不存在: {project_id}")
        return project
    
    async def get_projects(self, skip: int = 0, limit: int = 100) -> list[ProjectResponse]:
        """获取项目列表"""
        return await project_crud.get_multi(skip=skip, limit=limit) 