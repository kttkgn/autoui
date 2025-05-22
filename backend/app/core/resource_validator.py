from typing import Dict, Any, Optional
from app.core.resource_pool import ResourceType
from app.core.exceptions import ResourceConfigError

class ResourceValidator:
    """资源配置验证器"""
    
    @staticmethod
    def validate_device_config(config: Dict[str, Any]) -> None:
        """
        验证设备资源配置
        
        Args:
            config: 设备配置
            
        Raises:
            ResourceConfigError: 配置无效
        """
        required_fields = ["platform", "version", "udid"]
        for field in required_fields:
            if field not in config:
                raise ResourceConfigError(f"设备配置缺少必要字段: {field}")
                
        if config["platform"] not in ["android", "ios"]:
            raise ResourceConfigError(f"不支持的设备平台: {config['platform']}")
            
    @staticmethod
    def validate_browser_config(config: Dict[str, Any]) -> None:
        """
        验证浏览器资源配置
        
        Args:
            config: 浏览器配置
            
        Raises:
            ResourceConfigError: 配置无效
        """
        required_fields = ["browser_type", "version"]
        for field in required_fields:
            if field not in config:
                raise ResourceConfigError(f"浏览器配置缺少必要字段: {field}")
                
        if config["browser_type"] not in ["chrome", "firefox"]:
            raise ResourceConfigError(f"不支持的浏览器类型: {config['browser_type']}")
            
    @staticmethod
    def validate_database_config(config: Dict[str, Any]) -> None:
        """
        验证数据库资源配置
        
        Args:
            config: 数据库配置
            
        Raises:
            ResourceConfigError: 配置无效
        """
        required_fields = ["host", "port", "username", "password", "database"]
        for field in required_fields:
            if field not in config:
                raise ResourceConfigError(f"数据库配置缺少必要字段: {field}")
                
    @staticmethod
    def validate_api_config(config: Dict[str, Any]) -> None:
        """
        验证API资源配置
        
        Args:
            config: API配置
            
        Raises:
            ResourceConfigError: 配置无效
        """
        required_fields = ["base_url", "timeout"]
        for field in required_fields:
            if field not in config:
                raise ResourceConfigError(f"API配置缺少必要字段: {field}")
                
    @classmethod
    def validate_config(cls, type: ResourceType, config: Dict[str, Any]) -> None:
        """
        验证资源配置
        
        Args:
            type: 资源类型
            config: 资源配置
            
        Raises:
            ResourceConfigError: 配置无效
        """
        if not isinstance(config, dict):
            raise ResourceConfigError("配置必须是字典类型")
            
        validators = {
            ResourceType.DEVICE: cls.validate_device_config,
            ResourceType.BROWSER: cls.validate_browser_config,
            ResourceType.DATABASE: cls.validate_database_config,
            ResourceType.API: cls.validate_api_config
        }
        
        validator = validators.get(type)
        if not validator:
            raise ResourceConfigError(f"不支持的资源类型: {type}")
            
        validator(config) 