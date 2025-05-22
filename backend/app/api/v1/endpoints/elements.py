from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Depends, WebSocket, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_db
from app.crud.device import device
from app.services.element_locator import ElementLocator, create_element_locator
from app.schemas.element import (
    ElementLocateRequest,
    ElementLocateResponse,
    ElementTreeResponse,
    ElementActionRequest,
    ElementActionResponse,
    ElementScreenshotResponse
)

router = APIRouter()

@router.post("/{device_id}/connect")
async def connect_device(
    *,
    db: AsyncSession = Depends(get_db),
    device_id: str
):
    """连接设备"""
    device_obj = await device.get(db, id=device_id)
    if not device_obj:
        raise HTTPException(status_code=404, detail="设备不存在")
    
    locator = create_element_locator(device_obj)
    if not locator:
        raise HTTPException(status_code=400, detail="不支持的设备类型")
    
    connected = await locator.connect()
    if not connected:
        raise HTTPException(status_code=500, detail="设备连接失败")
    
    return {"message": "设备连接成功"}

@router.post("/{device_id}/disconnect")
async def disconnect_device(
    *,
    db: AsyncSession = Depends(get_db),
    device_id: str
):
    """断开设备连接"""
    device_obj = await device.get(db, id=device_id)
    if not device_obj:
        raise HTTPException(status_code=404, detail="设备不存在")
    
    locator = create_element_locator(device_obj)
    if not locator:
        raise HTTPException(status_code=400, detail="不支持的设备类型")
    
    await locator.disconnect()
    return {"message": "设备已断开连接"}

@router.post("/locate", response_model=ElementLocateResponse)
async def locate_element(
    *,
    db: AsyncSession = Depends(get_db),
    request: ElementLocateRequest
):
    """定位元素"""
    device_obj = await device.get(db, id=request.device_id)
    if not device_obj:
        raise HTTPException(status_code=404, detail="设备不存在")
    
    locator = create_element_locator(device_obj)
    if not locator:
        raise HTTPException(status_code=400, detail="不支持的设备类型")
    
    element = await locator.find_element(request.strategy, request.selector)
    if not element:
        raise HTTPException(status_code=404, detail="元素未找到")
    return element

@router.get("/tree", response_model=ElementTreeResponse)
async def get_element_tree(
    *,
    db: AsyncSession = Depends(get_db),
    device_id: str
):
    """获取元素树"""
    device_obj = await device.get(db, id=device_id)
    if not device_obj:
        raise HTTPException(status_code=404, detail="设备不存在")
    
    locator = create_element_locator(device_obj)
    if not locator:
        raise HTTPException(status_code=400, detail="不支持的设备类型")
    
    return await locator.get_element_tree()

@router.websocket("/{device_id}/screen")
async def screen_stream(websocket: WebSocket, device_id: str):
    """获取屏幕流"""
    await websocket.accept()
    device_obj = await device.get(db, id=device_id)
    if not device_obj:
        await websocket.close(code=1000, reason="设备不存在")
        return
    
    locator = create_element_locator(device_obj)
    if not locator:
        await websocket.close(code=1000, reason="不支持的设备类型")
        return
    
    try:
        async for frame in locator.get_screen_stream():
            await websocket.send_bytes(frame)
    except Exception as e:
        await websocket.close(code=1000, reason=str(e))

@router.post("/{device_id}/highlight")
async def highlight_element(
    *,
    db: AsyncSession = Depends(get_db),
    device_id: str,
    element_id: str
):
    """高亮显示元素"""
    device_obj = await device.get(db, id=device_id)
    if not device_obj:
        raise HTTPException(status_code=404, detail="设备不存在")
    
    locator = create_element_locator(device_obj)
    if not locator:
        raise HTTPException(status_code=400, detail="不支持的设备类型")
    
    await locator.highlight_element(element_id)
    return {"message": "元素已高亮"}

@router.get("/{device_id}/screenshot", response_model=ElementScreenshotResponse)
async def take_screenshot(
    *,
    db: AsyncSession = Depends(get_db),
    device_id: str,
    element_id: Optional[str] = None
):
    """获取截图"""
    device_obj = await device.get(db, id=device_id)
    if not device_obj:
        raise HTTPException(status_code=404, detail="设备不存在")
    
    locator = create_element_locator(device_obj)
    if not locator:
        raise HTTPException(status_code=400, detail="不支持的设备类型")
    
    if element_id:
        return await locator.take_element_screenshot(element_id)
    return await locator.take_screenshot()

@router.post("/{device_id}/action", response_model=ElementActionResponse)
async def perform_action(
    *,
    db: AsyncSession = Depends(get_db),
    device_id: str,
    request: ElementActionRequest
):
    """执行元素操作"""
    device_obj = await device.get(db, id=device_id)
    if not device_obj:
        raise HTTPException(status_code=404, detail="设备不存在")
    
    locator = create_element_locator(device_obj)
    if not locator:
        raise HTTPException(status_code=400, detail="不支持的设备类型")
    
    return await locator.perform_action(
        element_id=request.element_id,
        action=request.action,
        params=request.params
    )

@router.get("/{device_id}/screen-size")
async def get_screen_size(
    *,
    db: AsyncSession = Depends(get_db),
    device_id: str
):
    """获取屏幕尺寸"""
    device_obj = await device.get(db, id=device_id)
    if not device_obj:
        raise HTTPException(status_code=404, detail="设备不存在")
    
    locator = create_element_locator(device_obj)
    if not locator:
        raise HTTPException(status_code=400, detail="不支持的设备类型")
    
    width, height = await locator.get_screen_size()
    return {"width": width, "height": height} 