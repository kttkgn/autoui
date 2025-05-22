from typing import Dict, List, Optional, Any
from datetime import datetime
from app.core.logger import logger
from app.core.enums.resource import ResourceType, ResourceStatus

class Resource:
    """资源基类"""
    
    def __init__(
        self,
        resource_id: str,
        resource_type: ResourceType,
        name: str,
        status: ResourceStatus = ResourceStatus.AVAILABLE,
        properties: Optional[Dict[str, Any]] = None
    ):
        """
        初始化资源
        
        Args:
            resource_id: 资源ID
            resource_type: 资源类型
            name: 资源名称
            status: 资源状态
            properties: 资源属性
        """
        self.resource_id = resource_id
        self.resource_type = resource_type
        self.name = name
        self.status = status
        self.properties = properties or {}
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.last_used_at: Optional[datetime] = None
        self.usage_count = 0
        self.error_count = 0
        self.error_message: Optional[str] = None
    
    def update_status(self, status: ResourceStatus, error_message: Optional[str] = None) -> None:
        """
        更新资源状态
        
        Args:
            status: 新状态
            error_message: 错误信息
        """
        self.status = status
        self.error_message = error_message
        self.updated_at = datetime.now()
    
    def mark_as_used(self) -> None:
        """标记资源为已使用"""
        self.status = ResourceStatus.IN_USE
        self.last_used_at = datetime.now()
        self.usage_count += 1
        self.updated_at = datetime.now()
    
    def mark_as_available(self) -> None:
        """标记资源为可用"""
        self.status = ResourceStatus.AVAILABLE
        self.updated_at = datetime.now()
    
    def mark_as_error(self, error_message: str) -> None:
        """
        标记资源为错误状态
        
        Args:
            error_message: 错误信息
        """
        self.status = ResourceStatus.ERROR
        self.error_message = error_message
        self.error_count += 1
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典
        
        Returns:
            Dict[str, Any]: 资源信息字典
        """
        return {
            "resource_id": self.resource_id,
            "resource_type": self.resource_type.value,
            "name": self.name,
            "status": self.status.value,
            "properties": self.properties,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "last_used_at": self.last_used_at.isoformat() if self.last_used_at else None,
            "usage_count": self.usage_count,
            "error_count": self.error_count,
            "error_message": self.error_message
        }


class ResourcePool:
    """资源池管理类"""
    
    def __init__(self):
        """初始化资源池"""
        self._resources: Dict[str, Resource] = {}
        self._type_resources: Dict[ResourceType, List[str]] = {
            resource_type: [] for resource_type in ResourceType
        }
    
    def add_resource(self, resource: Resource) -> None:
        """
        添加资源
        
        Args:
            resource: 资源对象
        """
        self._resources[resource.resource_id] = resource
        self._type_resources[resource.resource_type].append(resource.resource_id)
        logger.info(f"添加资源: {resource.resource_id} ({resource.resource_type.value})")
    
    def remove_resource(self, resource_id: str) -> None:
        """
        移除资源
        
        Args:
            resource_id: 资源ID
        """
        if resource_id in self._resources:
            resource = self._resources[resource_id]
            self._type_resources[resource.resource_type].remove(resource_id)
            del self._resources[resource_id]
            logger.info(f"移除资源: {resource_id}")
    
    def get_resource(self, resource_id: str) -> Optional[Resource]:
        """
        获取资源
        
        Args:
            resource_id: 资源ID
            
        Returns:
            Optional[Resource]: 资源对象，如果不存在则返回None
        """
        return self._resources.get(resource_id)
    
    def get_available_resource(self, resource_type: ResourceType) -> Optional[Resource]:
        """
        获取可用的资源
        
        Args:
            resource_type: 资源类型
            
        Returns:
            Optional[Resource]: 可用的资源对象，如果没有则返回None
        """
        for resource_id in self._type_resources[resource_type]:
            resource = self._resources[resource_id]
            if resource.status == ResourceStatus.AVAILABLE:
                return resource
        return None
    
    def get_resources_by_type(self, resource_type: ResourceType) -> List[Resource]:
        """
        获取指定类型的所有资源
        
        Args:
            resource_type: 资源类型
            
        Returns:
            List[Resource]: 资源对象列表
        """
        return [
            self._resources[resource_id]
            for resource_id in self._type_resources[resource_type]
        ]
    
    def get_all_resources(self) -> Dict[str, Resource]:
        """
        获取所有资源
        
        Returns:
            Dict[str, Resource]: 资源对象字典
        """
        return self._resources
    
    def get_resource_count(self, resource_type: Optional[ResourceType] = None) -> int:
        """
        获取资源数量
        
        Args:
            resource_type: 资源类型，如果为None则返回所有类型的资源数量
            
        Returns:
            int: 资源数量
        """
        if resource_type:
            return len(self._type_resources[resource_type])
        return len(self._resources)
    
    def get_available_resource_count(self, resource_type: Optional[ResourceType] = None) -> int:
        """
        获取可用资源数量
        
        Args:
            resource_type: 资源类型，如果为None则返回所有类型的可用资源数量
            
        Returns:
            int: 可用资源数量
        """
        count = 0
        for resource in self.get_all_resources().values():
            if resource.status == ResourceStatus.AVAILABLE:
                if resource_type is None or resource.resource_type == resource_type:
                    count += 1
        return count
    
    def clear(self) -> None:
        """清空资源池"""
        self._resources.clear()
        for resource_type in ResourceType:
            self._type_resources[resource_type].clear()
        logger.info("清空资源池")
    
    def update_resource_status(self, resource_id: str, status: ResourceStatus) -> None:
        """
        更新资源状态
        
        Args:
            resource_id: 资源ID
            status: 新状态
        """
        resource = self.get_resource(resource_id)
        if resource:
            resource.update_status(status)
    
    def get_resource_status(self, resource_id: str) -> Optional[ResourceStatus]:
        """
        获取资源状态
        
        Args:
            resource_id: 资源ID
            
        Returns:
            Optional[ResourceStatus]: 资源状态
        """
        resource = self.get_resource(resource_id)
        return resource.status if resource else None
    
    def get_resources_by_status(self, status: ResourceStatus) -> List[Resource]:
        """
        获取指定状态的资源
        
        Args:
            status: 资源状态
            
        Returns:
            List[Resource]: 资源列表
        """
        return [
            resource for resource in self._resources.values()
            if resource.status == status
        ]
    
    def allocate_resource(self, resource_type: ResourceType, user: str) -> Optional[Resource]:
        """
        分配资源
        
        Args:
            resource_type: 资源类型
            user: 用户标识
            
        Returns:
            Optional[Resource]: 分配的资源
        """
        resource = self.get_available_resource(resource_type)
        if resource:
            resource.mark_as_used()
            resource.properties["allocated_to"] = user
        return resource
    
    def release_resource(self, resource_id: str) -> None:
        """
        释放资源
        
        Args:
            resource_id: 资源ID
        """
        resource = self.get_resource(resource_id)
        if resource:
            resource.mark_as_available()
            resource.properties.pop("allocated_to", None)


# 创建全局资源池实例
resource_pool = ResourcePool() 