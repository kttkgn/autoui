from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Query, BackgroundTasks, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.device import device
from app.schemas.device import (
    Device, DeviceCreate, DeviceUpdate,
    DeviceProperty, DevicePropertyCreate, DevicePropertyUpdate,
    DeviceList, DeviceResponse, DeviceStatus, DeviceType
)
from app.services.device_service import DeviceService
from app.core.enums.device import DeviceType, DeviceStatus
from app.core.exceptions import DeviceError
from app.core.deps import get_db

router = APIRouter()

@router.get("", response_model=List[DeviceResponse])
async def get_devices(
    *,
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    type: Optional[DeviceType] = None,
    status: Optional[DeviceStatus] = None
):
    """获取设备列表，支持分页和过滤"""
    device_service = DeviceService(db)
    return await device_service.get_devices(skip=skip, limit=limit, type=type, status=status)

@router.post("", response_model=DeviceResponse)
async def create_device(
    *,
    db: AsyncSession = Depends(get_db),
    device_in: DeviceCreate
):
    """创建设备"""
    device_service = DeviceService(db)
    return await device_service.add_device(
        id=device_in.id,
        type=device_in.type,
        config=device_in.config,
        description=device_in.description
    )

@router.get("/{device_id}", response_model=DeviceResponse)
async def get_device(
    *,
    db: AsyncSession = Depends(get_db),
    device_id: str
):
    """获取设备详情，包含所有属性信息"""
    device_service = DeviceService(db)
    device = await device_service.get_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="设备不存在")
    return device

@router.put("/{device_id}", response_model=DeviceResponse)
async def update_device(
    *,
    db: AsyncSession = Depends(get_db),
    device_id: str,
    device_in: DeviceUpdate
):
    """更新设备信息"""
    device_service = DeviceService(db)
    device = await device_service.update_device(device_id, device_in)
    if not device:
        raise HTTPException(status_code=404, detail="设备不存在")
    return device

@router.delete("/{device_id}")
async def delete_device(
    *,
    db: AsyncSession = Depends(get_db),
    device_id: str
):
    """删除设备"""
    device_service = DeviceService(db)
    await device_service.remove_device(device_id)
    return {"message": "设备已删除"}

@router.post("/detect", response_model=List[DeviceResponse])
async def detect_devices(
    *,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """检测并添加新设备"""
    device_service = DeviceService(db)
    return await device_service.detect_devices()

@router.post("/{device_id}/monitor/start")
async def start_device_monitor(
    *,
    db: AsyncSession = Depends(get_db),
    device_id: str
):
    """启动设备监控"""
    device_service = DeviceService(db)
    await device_service.start_device_monitor(device_id)
    return {"message": "设备监控已启动"}

@router.post("/{device_id}/monitor/stop")
async def stop_device_monitor(
    *,
    db: AsyncSession = Depends(get_db),
    device_id: str
):
    """停止设备监控"""
    device_service = DeviceService(db)
    await device_service.stop_device_monitor(device_id)
    return {"message": "设备监控已停止"}

@router.get("/{device_id}/screen")
async def get_screen_stream(
    *,
    db: AsyncSession = Depends(get_db),
    device_id: str
):
    """获取设备屏幕流（WebSocket）"""
    device_service = DeviceService(db)
    return await device_service.get_screen_stream(device_id)

@router.get("/{device_id}/status")
async def get_device_status(
    *,
    db: AsyncSession = Depends(get_db),
    device_id: str
) -> Dict[str, Any]:
    """
    获取设备状态
    
    Args:
        device_id: 设备ID
        
    Returns:
        Dict[str, Any]: 设备状态
    """
    try:
        device_service = DeviceService(db)
        status = device_service.get_device_status(device_id)
        if not status:
            raise HTTPException(status_code=404, detail=f"设备不存在: {device_id}")
        return {
            "status": status.value
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{device_id}/status")
async def update_device_status(
    *,
    db: AsyncSession = Depends(get_db),
    device_id: str,
    status: DeviceStatus = Body(...)
) -> Dict[str, Any]:
    """
    更新设备状态
    
    Args:
        device_id: 设备ID
        status: 设备状态
        
    Returns:
        Dict[str, Any]: 更新结果
    """
    try:
        device_service = DeviceService(db)
        device_service.update_device_status(device_id, status)
        return {
            "message": "设备状态更新成功"
        }
    except DeviceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def get_all_devices(
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取所有设备
    
    Returns:
        Dict[str, Any]: 设备列表
    """
    try:
        device_service = DeviceService(db)
        devices = device_service.get_all_devices()
        return {
            "devices": {
                id: device.to_dict()
                for id, device in devices.items()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/type/{type}")
async def get_devices_by_type(
    *,
    db: AsyncSession = Depends(get_db),
    type: DeviceType
) -> Dict[str, Any]:
    """
    获取指定类型的设备
    
    Args:
        type: 设备类型
        
    Returns:
        Dict[str, Any]: 设备列表
    """
    try:
        device_service = DeviceService(db)
        devices = device_service.get_devices_by_type(type)
        return {
            "devices": {
                id: device.to_dict()
                for id, device in devices.items()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{status}")
async def get_devices_by_status(
    *,
    db: AsyncSession = Depends(get_db),
    status: DeviceStatus
) -> Dict[str, Any]:
    """
    获取指定状态的设备
    
    Args:
        status: 设备状态
        
    Returns:
        Dict[str, Any]: 设备列表
    """
    try:
        device_service = DeviceService(db)
        devices = device_service.get_devices_by_status(status)
        return {
            "devices": {
                id: device.to_dict()
                for id, device in devices.items()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/available")
async def get_available_devices(
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取可用设备
    
    Returns:
        Dict[str, Any]: 设备列表
    """
    try:
        device_service = DeviceService(db)
        devices = device_service.get_available_devices()
        return {
            "devices": {
                id: device.to_dict()
                for id, device in devices.items()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{device_id}/properties", response_model=DeviceProperty)
async def add_device_property(
    *,
    db: AsyncSession = Depends(get_db),
    device_id: str,
    property_in: DevicePropertyCreate
):
    """添加设备属性"""
    device_service = DeviceService(db)
    return await device_service.add_device_property(device_id, property_in)

@router.put("/properties/{property_id}", response_model=DeviceProperty)
async def update_device_property(
    *,
    db: AsyncSession = Depends(get_db),
    property_id: int,
    property_in: DevicePropertyUpdate
):
    """更新设备属性"""
    device_service = DeviceService(db)
    return await device_service.update_device_property(property_id, property_in)

@router.delete("/properties/{property_id}", response_model=DeviceProperty)
async def delete_device_property(
    *,
    db: AsyncSession = Depends(get_db),
    property_id: int
):
    """删除设备属性"""
    device_service = DeviceService(db)
    return await device_service.delete_device_property(property_id) 