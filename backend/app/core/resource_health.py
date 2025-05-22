from typing import Dict, Any, Optional
import asyncio
import aiohttp
import subprocess
from app.core.resource_pool import ResourceType, ResourceStatus
from app.core.exceptions import ResourceHealthCheckError
from app.core.logger import logger

class ResourceHealthChecker:
    """资源健康检查器"""
    
    @staticmethod
    async def check_device_health(config: Dict[str, Any]) -> bool:
        """
        检查设备健康状态
        
        Args:
            config: 设备配置
            
        Returns:
            bool: 是否健康
        """
        try:
            if config["platform"] == "android":
                # 检查Android设备连接状态
                result = subprocess.run(
                    ["adb", "devices"],
                    capture_output=True,
                    text=True
                )
                return config["udid"] in result.stdout
            elif config["platform"] == "ios":
                # 检查iOS设备连接状态
                result = subprocess.run(
                    ["idevice_id", "-l"],
                    capture_output=True,
                    text=True
                )
                return config["udid"] in result.stdout
            return False
        except Exception as e:
            logger.error(f"设备健康检查失败: {str(e)}")
            return False
            
    @staticmethod
    async def check_browser_health(config: Dict[str, Any]) -> bool:
        """
        检查浏览器健康状态
        
        Args:
            config: 浏览器配置
            
        Returns:
            bool: 是否健康
        """
        try:
            if config["browser_type"] == "chrome":
                # 检查Chrome版本
                result = subprocess.run(
                    ["google-chrome", "--version"],
                    capture_output=True,
                    text=True
                )
                return config["version"] in result.stdout
            elif config["browser_type"] == "firefox":
                # 检查Firefox版本
                result = subprocess.run(
                    ["firefox", "--version"],
                    capture_output=True,
                    text=True
                )
                return config["version"] in result.stdout
            return False
        except Exception as e:
            logger.error(f"浏览器健康检查失败: {str(e)}")
            return False
            
    @staticmethod
    async def check_database_health(config: Dict[str, Any]) -> bool:
        """
        检查数据库健康状态
        
        Args:
            config: 数据库配置
            
        Returns:
            bool: 是否健康
        """
        try:
            # 尝试连接数据库
            import mysql.connector
            conn = mysql.connector.connect(
                host=config["host"],
                port=config["port"],
                user=config["username"],
                password=config["password"],
                database=config["database"]
            )
            conn.close()
            return True
        except Exception as e:
            logger.error(f"数据库健康检查失败: {str(e)}")
            return False
            
    @staticmethod
    async def check_api_health(config: Dict[str, Any]) -> bool:
        """
        检查API健康状态
        
        Args:
            config: API配置
            
        Returns:
            bool: 是否健康
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{config['base_url']}/health",
                    timeout=config["timeout"]
                ) as response:
                    return response.status == 200
        except Exception as e:
            logger.error(f"API健康检查失败: {str(e)}")
            return False
            
    @classmethod
    async def check_health(cls, type: ResourceType, config: Dict[str, Any]) -> bool:
        """
        检查资源健康状态
        
        Args:
            type: 资源类型
            config: 资源配置
            
        Returns:
            bool: 是否健康
        """
        checkers = {
            ResourceType.DEVICE: cls.check_device_health,
            ResourceType.BROWSER: cls.check_browser_health,
            ResourceType.DATABASE: cls.check_database_health,
            ResourceType.API: cls.check_api_health
        }
        
        checker = checkers.get(type)
        if not checker:
            raise ResourceHealthCheckError(f"不支持的资源类型: {type}")
            
        return await checker(config)

# 创建全局健康检查器实例
health_checker = ResourceHealthChecker() 