from enum import Enum

class DeviceType(str, Enum):
    """设备类型枚举"""
    ANDROID = "android"
    IOS = "ios"
    WINDOWS = "windows"
    MAC = "mac"
    OTHER = "other"

class DeviceStatus(str, Enum):
    """设备状态枚举"""
    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"
    MAINTENANCE = "maintenance"
    UNKNOWN = "unknown" 