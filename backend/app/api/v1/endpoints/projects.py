from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Body
from app.services.project_service import ProjectService
from app.core.enums.project import ProjectStatus
from app.core.exceptions import ProjectError

router = APIRouter()
project_service = ProjectService()

@router.post("/")
async def create_project(
    name: str = Body(...),
    description: Optional[str] = Body(None)
) -> Dict[str, Any]:
    """
    创建项目
    
    Args:
        name: 项目名称
        description: 项目描述
        
    Returns:
        Dict[str, Any]: 创建结果
    """
    try:
        project = await project_service.create_project(
            name,
            description,
            "1"  # 使用默认用户ID
        )
        return {
            "message": "项目创建成功",
            "project": project.to_dict()
        }
    except ProjectError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{project_id}")
async def get_project(
    project_id: str
) -> Dict[str, Any]:
    """
    获取项目信息
    
    Args:
        project_id: 项目ID
        
    Returns:
        Dict[str, Any]: 项目信息
    """
    try:
        project = await project_service.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail=f"项目不存在: {project_id}")
        return project.to_dict()
    except ProjectError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{project_id}")
async def update_project(
    project_id: str,
    name: Optional[str] = Body(None),
    description: Optional[str] = Body(None),
    status: Optional[ProjectStatus] = Body(None)
) -> Dict[str, Any]:
    """
    更新项目信息
    
    Args:
        project_id: 项目ID
        name: 新项目名称
        description: 新项目描述
        status: 新项目状态
        
    Returns:
        Dict[str, Any]: 更新结果
    """
    try:
        project = await project_service.update_project(
            project_id,
            name=name,
            description=description,
            status=status
        )
        return {
            "message": "项目信息更新成功",
            "project": project.to_dict()
        }
    except ProjectError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{project_id}")
async def delete_project(
    project_id: str
) -> Dict[str, Any]:
    """
    删除项目
    
    Args:
        project_id: 项目ID
        
    Returns:
        Dict[str, Any]: 删除结果
    """
    try:
        await project_service.delete_project(project_id)
        return {
            "message": "项目删除成功"
        }
    except ProjectError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def get_all_projects() -> Dict[str, Any]:
    """
    获取所有项目
    
    Returns:
        Dict[str, Any]: 项目列表
    """
    try:
        projects = await project_service.get_all_projects()
        return {
            "projects": [project.to_dict() for project in projects]
        }
    except ProjectError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}")
async def get_user_projects(
    user_id: str
) -> Dict[str, Any]:
    """
    获取用户的项目
    
    Args:
        user_id: 用户ID
        
    Returns:
        Dict[str, Any]: 项目列表
    """
    try:
        projects = await project_service.get_user_projects(user_id)
        return {
            "projects": [project.to_dict() for project in projects]
        }
    except ProjectError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{status}")
async def get_projects_by_status(
    status: ProjectStatus
) -> Dict[str, Any]:
    """
    获取指定状态的项目
    
    Args:
        status: 项目状态
        
    Returns:
        Dict[str, Any]: 项目列表
    """
    try:
        projects = await project_service.get_projects_by_status(status)
        return {
            "projects": [project.to_dict() for project in projects]
        }
    except ProjectError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{project_id}/members")
async def add_project_member(
    project_id: str,
    user_id: str = Body(...),
    role: str = Body(...)
) -> Dict[str, Any]:
    """
    添加项目成员
    
    Args:
        project_id: 项目ID
        user_id: 用户ID
        role: 角色
        
    Returns:
        Dict[str, Any]: 添加结果
    """
    try:
        await project_service.add_project_member(project_id, user_id, role)
        return {
            "message": "项目成员添加成功"
        }
    except ProjectError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{project_id}/members/{user_id}")
async def remove_project_member(
    project_id: str,
    user_id: str
) -> Dict[str, Any]:
    """
    移除项目成员
    
    Args:
        project_id: 项目ID
        user_id: 用户ID
        
    Returns:
        Dict[str, Any]: 移除结果
    """
    try:
        await project_service.remove_project_member(project_id, user_id)
        return {
            "message": "项目成员移除成功"
        }
    except ProjectError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{project_id}/members")
async def get_project_members(
    project_id: str
) -> Dict[str, Any]:
    """
    获取项目成员
    
    Args:
        project_id: 项目ID
        
    Returns:
        Dict[str, Any]: 成员列表
    """
    try:
        members = await project_service.get_project_members(project_id)
        return {
            "members": members
        }
    except ProjectError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 