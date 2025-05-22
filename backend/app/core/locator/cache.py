from typing import Dict, Optional, Any
from datetime import datetime, timedelta
from app.core.logger import logger
from app.core.locator.base import BaseLocator

class LocatorCache:
    """定位器缓存类"""
    
    def __init__(self, ttl: int = 300):
        """
        初始化定位器缓存
        
        Args:
            ttl: 缓存生存时间（秒）
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._ttl = ttl
    
    def _get_cache_key(self, locator: BaseLocator) -> str:
        """
        获取缓存键
        
        Args:
            locator: 定位器实例
            
        Returns:
            str: 缓存键
        """
        return f"{locator.locator_type.value}:{locator.locator_value}"
    
    def get(self, locator: BaseLocator) -> Optional[Any]:
        """
        获取缓存的元素
        
        Args:
            locator: 定位器实例
            
        Returns:
            Optional[Any]: 缓存的元素，如果不存在或已过期则返回None
        """
        cache_key = self._get_cache_key(locator)
        cache_data = self._cache.get(cache_key)
        
        if not cache_data:
            return None
        
        # 检查缓存是否过期
        if datetime.now() - cache_data["timestamp"] > timedelta(seconds=self._ttl):
            del self._cache[cache_key]
            return None
        
        try:
            # 检查元素是否仍然有效
            element = cache_data["element"]
            element.is_enabled()  # 尝试访问元素属性
            return element
        except Exception:
            # 如果元素无效，删除缓存
            del self._cache[cache_key]
            return None
    
    def set(self, locator: BaseLocator, element: Any) -> None:
        """
        缓存元素
        
        Args:
            locator: 定位器实例
            element: 要缓存的元素
        """
        cache_key = self._get_cache_key(locator)
        self._cache[cache_key] = {
            "element": element,
            "timestamp": datetime.now()
        }
        logger.debug(f"缓存元素: {cache_key}")
    
    def clear(self) -> None:
        """清空缓存"""
        self._cache.clear()
        logger.debug("清空元素缓存")
    
    def remove(self, locator: BaseLocator) -> None:
        """
        移除缓存的元素
        
        Args:
            locator: 定位器实例
        """
        cache_key = self._get_cache_key(locator)
        if cache_key in self._cache:
            del self._cache[cache_key]
            logger.debug(f"移除缓存元素: {cache_key}")
    
    def get_cache_size(self) -> int:
        """
        获取缓存大小
        
        Returns:
            int: 缓存中的元素数量
        """
        return len(self._cache)
    
    def get_cache_info(self) -> Dict[str, Any]:
        """
        获取缓存信息
        
        Returns:
            Dict[str, Any]: 缓存信息
        """
        return {
            "size": len(self._cache),
            "ttl": self._ttl,
            "keys": list(self._cache.keys())
        } 