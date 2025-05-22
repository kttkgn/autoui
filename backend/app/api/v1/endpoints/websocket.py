from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.websocket import manager, websocket_endpoint

router = APIRouter()

@router.websocket("/ws/device/{device_id}")
async def device_websocket(websocket: WebSocket, device_id: str):
    """设备状态实时推送"""
    await websocket_endpoint(websocket, "device")

@router.websocket("/ws/log/{execution_id}")
async def log_websocket(websocket: WebSocket, execution_id: str):
    """执行日志实时推送"""
    await websocket_endpoint(websocket, "log")

@router.websocket("/ws/screen/{device_id}")
async def screen_websocket(websocket: WebSocket, device_id: str):
    """屏幕流实时推送"""
    await websocket_endpoint(websocket, "screen") 