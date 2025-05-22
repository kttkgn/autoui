from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Body
from app.services.resource_service import ResourceService
from app.core.resource_pool import ResourceType, ResourceStatus
from app.core.exceptions import ResourceHealthCheckError

router = APIRouter()
resource_service = ResourceService()

@router.post("/")
async def add_resource(
    id: str = Body(...),
    type: ResourceType = Body(...),
    config: Dict[str, Any] = Body(...),
    description: Optional[str] = Body(None)
) -> Dict[str, Any]:
    """
    添加资源
    
    Args:
        id: 资源ID
        type: 资源类型
        config: 资源配置
        description: 资源描述
        
    Returns:
        Dict[str, Any]: 添加结果
    """
    try:
        resource = resource_service.add_resource(id, type, config, description)
        return {
            "message": "资源添加成功",
            "resource": resource.to_dict()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{resource_id}")
async def remove_resource(resource_id: str) -> Dict[str, Any]:
    """
    移除资源
    
    Args:
        resource_id: 资源ID
        
    Returns:
        Dict[str, Any]: 移除结果
    """
    try:
        resource_service.remove_resource(resource_id)
        return {
            "message": "资源移除成功"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{resource_id}")
async def get_resource(resource_id: str) -> Dict[str, Any]:
    """
    获取资源
    
    Args:
        resource_id: 资源ID
        
    Returns:
        Dict[str, Any]: 资源信息
    """
    try:
        resource = resource_service.get_resource(resource_id)
        if not resource:
            raise HTTPException(status_code=404, detail=f"资源不存在: {resource_id}")
        return resource.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{resource_id}/health")
async def check_resource_health(resource_id: str) -> Dict[str, Any]:
    """
    检查资源健康状态
    
    Args:
        resource_id: 资源ID
        
    Returns:
        Dict[str, Any]: 健康状态
    """
    try:
        is_healthy = await resource_service.check_resource_health(resource_id)
        return {
            "resource_id": resource_id,
            "is_healthy": is_healthy
        }
    except ResourceHealthCheckError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def check_all_resources_health() -> Dict[str, Any]:
    """
    检查所有资源健康状态
    
    Returns:
        Dict[str, Any]: 健康状态
    """
    try:
        results = await resource_service.check_all_resources_health()
        return {
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/allocate")
async def allocate_resource(
    type: ResourceType = Body(...),
    user: str = Body(...)
) -> Dict[str, Any]:
    """
    分配资源
    
    Args:
        type: 资源类型
        user: 用户标识
        
    Returns:
        Dict[str, Any]: 分配结果
    """
    try:
        resource = resource_service.allocate_resource(type, user)
        if not resource:
            raise HTTPException(
                status_code=404,
                detail=f"没有可用的{type.value}资源"
            )
        return {
            "message": "资源分配成功",
            "resource": resource.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{resource_id}/release")
async def release_resource(resource_id: str) -> Dict[str, Any]:
    """
    释放资源
    
    Args:
        resource_id: 资源ID
        
    Returns:
        Dict[str, Any]: 释放结果
    """
    try:
        resource_service.release_resource(resource_id)
        return {
            "message": "资源释放成功"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{resource_id}/status")
async def update_resource_status(
    resource_id: str,
    status: ResourceStatus = Body(...)
) -> Dict[str, Any]:
    """
    更新资源状态
    
    Args:
        resource_id: 资源ID
        status: 资源状态
        
    Returns:
        Dict[str, Any]: 更新结果
    """
    try:
        resource_service.update_resource_status(resource_id, status)
        return {
            "message": "资源状态更新成功"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{resource_id}/status")
async def get_resource_status(resource_id: str) -> Dict[str, Any]:
    """
    获取资源状态
    
    Args:
        resource_id: 资源ID
        
    Returns:
        Dict[str, Any]: 资源状态
    """
    try:
        status = resource_service.get_resource_status(resource_id)
        if not status:
            raise HTTPException(status_code=404, detail=f"资源不存在: {resource_id}")
        return {
            "status": status.value
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def get_all_resources() -> Dict[str, Any]:
    """
    获取所有资源
    
    Returns:
        Dict[str, Any]: 资源列表
    """
    try:
        resources = resource_service.get_all_resources()
        return {
            "resources": {
                id: resource.to_dict()
                for id, resource in resources.items()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/type/{type}")
async def get_resources_by_type(type: ResourceType) -> Dict[str, Any]:
    """
    获取指定类型的资源
    
    Args:
        type: 资源类型
        
    Returns:
        Dict[str, Any]: 资源列表
    """
    try:
        resources = resource_service.get_resources_by_type(type)
        return {
            "resources": [resource.to_dict() for resource in resources]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{status}")
async def get_resources_by_status(status: ResourceStatus) -> Dict[str, Any]:
    """
    获取指定状态的资源
    
    Args:
        status: 资源状态
        
    Returns:
        Dict[str, Any]: 资源列表
    """
    try:
        resources = resource_service.get_resources_by_status(status)
        return {
            "resources": [resource.to_dict() for resource in resources]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/usage")
async def get_resource_usage() -> Dict[str, Any]:
    """
    获取资源使用情况
    
    Returns:
        Dict[str, Any]: 使用情况统计
    """
    try:
        usage = resource_service.get_resource_usage()
        return {
            "usage": usage
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/available")
async def get_available_resources(
    type: Optional[ResourceType] = None
) -> Dict[str, Any]:
    """
    获取可用资源
    
    Args:
        type: 资源类型
        
    Returns:
        Dict[str, Any]: 可用资源列表
    """
    try:
        resources = resource_service.get_available_resources(type)
        return {
            "resources": [resource.to_dict() for resource in resources]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 