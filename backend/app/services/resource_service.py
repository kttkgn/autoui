from typing import Dict, Any, List, Optional
from app.core.resource_pool import (
    Resource,
    ResourceType,
    ResourceStatus,
    resource_pool
)
from app.core.resource_validator import ResourceValidator
from app.core.resource_health import health_checker
from app.core.exceptions import ResourceConfigError, ResourceHealthCheckError
from app.core.logger import logger

class ResourceService:
    """资源池服务"""
    
    def add_resource(
        self,
        id: str,
        type: ResourceType,
        config: Dict[str, Any],
        description: Optional[str] = None
    ) -> Resource:
        """
        添加资源
        
        Args:
            id: 资源ID
            type: 资源类型
            config: 资源配置
            description: 资源描述
            
        Returns:
            Resource: 资源
            
        Raises:
            ResourceConfigError: 配置无效
        """
        # 验证资源配置
        ResourceValidator.validate_config(type, config)
        
        resource = Resource(id, type, config, description=description)
        resource_pool.add_resource(resource)
        return resource
        
    def remove_resource(self, resource_id: str) -> None:
        """
        移除资源
        
        Args:
            resource_id: 资源ID
        """
        resource_pool.remove_resource(resource_id)
        
    def get_resource(self, resource_id: str) -> Optional[Resource]:
        """
        获取资源
        
        Args:
            resource_id: 资源ID
            
        Returns:
            Optional[Resource]: 资源
        """
        return resource_pool.get_resource(resource_id)
        
    async def check_resource_health(self, resource_id: str) -> bool:
        """
        检查资源健康状态
        
        Args:
            resource_id: 资源ID
            
        Returns:
            bool: 是否健康
        """
        resource = self.get_resource(resource_id)
        if not resource:
            raise ResourceHealthCheckError(f"资源不存在: {resource_id}")
            
        is_healthy = await health_checker.check_health(resource.type, resource.config)
        if not is_healthy:
            resource_pool.update_resource_status(resource_id, ResourceStatus.ERROR)
        return is_healthy
        
    async def check_all_resources_health(self) -> Dict[str, bool]:
        """
        检查所有资源健康状态
        
        Returns:
            Dict[str, bool]: 资源健康状态
        """
        resources = resource_pool.get_all_resources()
        results = {}
        
        for resource_id, resource in resources.items():
            try:
                is_healthy = await health_checker.check_health(resource.type, resource.config)
                if not is_healthy:
                    resource_pool.update_resource_status(resource_id, ResourceStatus.ERROR)
                results[resource_id] = is_healthy
            except Exception as e:
                logger.error(f"资源健康检查失败: {resource_id} - {str(e)}")
                results[resource_id] = False
                
        return results
        
    def allocate_resource(
        self,
        type: ResourceType,
        user: str
    ) -> Optional[Resource]:
        """
        分配资源
        
        Args:
            type: 资源类型
            user: 用户标识
            
        Returns:
            Optional[Resource]: 分配的资源
        """
        resource = resource_pool.allocate_resource(type, user)
        if not resource:
            logger.warning(f"没有可用的{type.value}资源")
        return resource
        
    def release_resource(self, resource_id: str) -> None:
        """
        释放资源
        
        Args:
            resource_id: 资源ID
        """
        resource_pool.release_resource(resource_id)
        
    def update_resource_status(
        self,
        resource_id: str,
        status: ResourceStatus
    ) -> None:
        """
        更新资源状态
        
        Args:
            resource_id: 资源ID
            status: 资源状态
        """
        resource_pool.update_resource_status(resource_id, status)
        
    def get_resource_status(self, resource_id: str) -> Optional[ResourceStatus]:
        """
        获取资源状态
        
        Args:
            resource_id: 资源ID
            
        Returns:
            Optional[ResourceStatus]: 资源状态
        """
        return resource_pool.get_resource_status(resource_id)
        
    def get_all_resources(self) -> Dict[str, Resource]:
        """
        获取所有资源
        
        Returns:
            Dict[str, Resource]: 资源字典
        """
        return resource_pool.get_all_resources()
        
    def get_resources_by_type(self, type: ResourceType) -> List[Resource]:
        """
        获取指定类型的资源
        
        Args:
            type: 资源类型
            
        Returns:
            List[Resource]: 资源列表
        """
        return resource_pool.get_resources_by_type(type)
        
    def get_resources_by_status(self, status: ResourceStatus) -> List[Resource]:
        """
        获取指定状态的资源
        
        Args:
            status: 资源状态
            
        Returns:
            List[Resource]: 资源列表
        """
        return resource_pool.get_resources_by_status(status)
        
    def get_resource_usage(self) -> Dict[str, int]:
        """
        获取资源使用情况
        
        Returns:
            Dict[str, int]: 使用情况统计
        """
        return resource_pool.get_resource_usage()
        
    def get_available_resources(
        self,
        type: Optional[ResourceType] = None
    ) -> List[Resource]:
        """
        获取可用资源
        
        Args:
            type: 资源类型
            
        Returns:
            List[Resource]: 可用资源列表
        """
        return resource_pool.get_available_resources(type)
        
    def validate_resource_config(
        self,
        type: ResourceType,
        config: Dict[str, Any]
    ) -> bool:
        """
        验证资源配置
        
        Args:
            type: 资源类型
            config: 资源配置
            
        Returns:
            bool: 是否有效
        """
        try:
            ResourceValidator.validate_config(type, config)
            return True
        except ResourceConfigError:
            return False 