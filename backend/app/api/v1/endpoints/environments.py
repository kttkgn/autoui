from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Body
from app.services.environment_service import EnvironmentService

router = APIRouter()
environment_service = EnvironmentService()

@router.post("/")
async def create_environment(
    *,
    name: str = Body(...),
    config: Dict[str, Any] = Body(...),
    description: Optional[str] = Body(None)
) -> Dict[str, Any]:
    """
    创建环境配置
    
    Args:
        name: 环境名称
        config: 环境配置
        description: 环境描述
        
    Returns:
        Dict[str, Any]: 创建结果
    """
    try:
        env = environment_service.create_environment(name, config, description)
        return {
            "message": "环境配置创建成功",
            "environment": env.to_dict()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{name}")
async def update_environment(
    *,
    name: str,
    config: Dict[str, Any] = Body(...),
    description: Optional[str] = Body(None)
) -> Dict[str, Any]:
    """
    更新环境配置
    
    Args:
        name: 环境名称
        config: 环境配置
        description: 环境描述
        
    Returns:
        Dict[str, Any]: 更新结果
    """
    try:
        env = environment_service.update_environment(name, config, description)
        return {
            "message": "环境配置更新成功",
            "environment": env.to_dict()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{name}")
async def delete_environment(
    *,
    name: str
) -> Dict[str, Any]:
    """
    删除环境配置
    
    Args:
        name: 环境名称
        
    Returns:
        Dict[str, Any]: 删除结果
    """
    try:
        environment_service.delete_environment(name)
        return {
            "message": "环境配置删除成功"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{name}/switch")
async def switch_environment(
    *,
    name: str
) -> Dict[str, Any]:
    """
    切换环境
    
    Args:
        name: 环境名称
        
    Returns:
        Dict[str, Any]: 切换结果
    """
    try:
        environment_service.switch_environment(name)
        return {
            "message": "环境切换成功"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{name}")
async def get_environment(
    *,
    name: str
) -> Dict[str, Any]:
    """
    获取环境配置
    
    Args:
        name: 环境名称
        
    Returns:
        Dict[str, Any]: 环境配置
    """
    try:
        env = environment_service.get_environment(name)
        if not env:
            raise HTTPException(status_code=404, detail=f"环境不存在: {name}")
        return env.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/current")
async def get_current_environment() -> Dict[str, Any]:
    """
    获取当前环境
    
    Returns:
        Dict[str, Any]: 当前环境配置
    """
    try:
        env = environment_service.get_current_environment()
        if not env:
            raise HTTPException(status_code=404, detail="当前环境未设置")
        return env.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def get_all_environments() -> Dict[str, Any]:
    """
    获取所有环境
    
    Returns:
        Dict[str, Any]: 环境配置字典
    """
    try:
        environments = environment_service.get_all_environments()
        return {
            "environments": {
                name: env.to_dict()
                for name, env in environments.items()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/names")
async def get_environment_names() -> List[str]:
    """
    获取所有环境名称
    
    Returns:
        List[str]: 环境名称列表
    """
    try:
        return environment_service.get_environment_names()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{name}/validate")
async def validate_environment(
    *,
    name: str
) -> Dict[str, Any]:
    """
    验证环境配置
    
    Args:
        name: 环境名称
        
    Returns:
        Dict[str, Any]: 验证结果
    """
    try:
        is_valid = environment_service.validate_environment(name)
        return {
            "is_valid": is_valid
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{name}/config")
async def get_environment_config(
    *,
    name: str
) -> Dict[str, Any]:
    """
    获取环境配置
    
    Args:
        name: 环境名称
        
    Returns:
        Dict[str, Any]: 环境配置
    """
    try:
        config = environment_service.get_environment_config(name)
        if not config:
            raise HTTPException(status_code=404, detail=f"环境不存在: {name}")
        return config
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{name}/value/{key}")
async def get_environment_value(
    *,
    name: str,
    key: str,
    default: Any = None
) -> Any:
    """
    获取环境配置值
    
    Args:
        name: 环境名称
        key: 配置键
        default: 默认值
        
    Returns:
        Any: 配置值
    """
    try:
        value = environment_service.get_environment_value(name, key, default)
        if value is None:
            raise HTTPException(status_code=404, detail=f"配置不存在: {key}")
        return value
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{name}/value/{key}")
async def set_environment_value(
    *,
    name: str,
    key: str,
    value: Any = Body(...)
) -> Dict[str, Any]:
    """
    设置环境配置值
    
    Args:
        name: 环境名称
        key: 配置键
        value: 配置值
        
    Returns:
        Dict[str, Any]: 设置结果
    """
    try:
        environment_service.set_environment_value(name, key, value)
        return {
            "message": "配置值设置成功"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 