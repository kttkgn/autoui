from enum import Enum

class ResourceType(str, Enum):
    """资源类型枚举"""
    DEVICE = "device"
    BROWSER = "browser"
    DATABASE = "database"
    API = "api"
    FILE = "file"
    CACHE = "cache"

class ResourceStatus(str, Enum):
    """资源状态枚举"""
    AVAILABLE = "available"
    IN_USE = "in_use"
    MAINTENANCE = "maintenance"
    ERROR = "error"
    UNKNOWN = "unknown" 