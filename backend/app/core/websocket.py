from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List, Optional
import json
import asyncio
from app.core.logger import logger

class ConnectionManager:
    """WebSocket连接管理器"""
    
    def __init__(self):
        # 存储所有活跃连接，按类型分组
        self.active_connections: Dict[str, List[WebSocket]] = {
            "device": [],
            "log": [],
            "screen": []
        }
    
    async def connect(self, websocket: WebSocket, client_type: str):
        """建立连接"""
        await websocket.accept()
        self.active_connections[client_type].append(websocket)
        logger.info(f"WebSocket连接已建立: {client_type}")
    
    def disconnect(self, websocket: WebSocket, client_type: str):
        """断开连接"""
        self.active_connections[client_type].remove(websocket)
        logger.info(f"WebSocket连接已断开: {client_type}")
    
    async def broadcast(self, message: str, client_type: str):
        """广播消息"""
        for connection in self.active_connections[client_type]:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"广播消息失败: {str(e)}")
                self.disconnect(connection, client_type)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """发送个人消息"""
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"发送个人消息失败: {str(e)}")

# 全局连接管理器实例
manager = ConnectionManager()

async def websocket_endpoint(websocket: WebSocket, client_type: str):
    """WebSocket端点处理函数"""
    await manager.connect(websocket, client_type)
    try:
        while True:
            data = await websocket.receive_text()
            # 处理接收到的消息（如需要）
            logger.info(f"收到消息: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_type)
    except Exception as e:
        logger.error(f"WebSocket处理异常: {str(e)}")
        manager.disconnect(websocket, client_type) 