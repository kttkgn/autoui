from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class DeviceType(str, Enum):
    ANDROID = "android"
    IOS = "ios"
    WEB = "web"

class DeviceStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"

class DevicePropertyBase(BaseModel):
    """设备属性基础模型"""
    key: str
    value: str
    description: Optional[str] = None

class DevicePropertyCreate(DevicePropertyBase):
    """创建设备属性模型"""
    pass

class DevicePropertyUpdate(DevicePropertyBase):
    """更新设备属性模型"""
    pass

class DeviceProperty(DevicePropertyBase):
    """设备属性响应模型"""
    id: int
    device_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DeviceBase(BaseModel):
    """设备基础模型"""
    name: str
    type: DeviceType
    status: DeviceStatus
    config: Dict[str, Any]
    description: Optional[str] = None

class DeviceCreate(DeviceBase):
    """创建设备模型"""
    id: str

class DeviceUpdate(BaseModel):
    """更新设备模型"""
    name: Optional[str] = None
    type: Optional[DeviceType] = None
    status: Optional[DeviceStatus] = None
    config: Optional[Dict[str, Any]] = None
    description: Optional[str] = None

class Device(DeviceBase):
    """设备响应模型"""
    id: str
    created_at: datetime
    updated_at: datetime
    properties: List[DeviceProperty] = []

    class Config:
        from_attributes = True

class DeviceResponse(Device):
    """设备响应模型，包含所有设备信息"""
    pass

class DeviceList(BaseModel):
    """设备列表响应模型"""
    total: int
    items: List[DeviceResponse] 