from typing import Dict, Optional, Any, List
from app.core.logger import logger
from app.core.locator.base import BaseLocator
from app.core.locator.factory import LocatorFactory
from app.core.locator.cache import LocatorCache
from app.core.enums.element import LocatorStrategy

class LocatorManager:
    """定位器管理类"""
    
    def __init__(self, driver: Any, cache_ttl: int = 300):
        """
        初始化定位器管理器
        
        Args:
            driver: WebDriver实例
            cache_ttl: 缓存生存时间（秒）
        """
        self.driver = driver
        self.cache = LocatorCache(ttl=cache_ttl)
        self._locators: Dict[str, BaseLocator] = {}
    
    def create_locator(
        self,
        locator_type: LocatorStrategy,
        locator_value: str,
        **kwargs
    ) -> BaseLocator:
        """
        创建定位器
        
        Args:
            locator_type: 定位类型
            locator_value: 定位值
            **kwargs: 其他参数
            
        Returns:
            BaseLocator: 定位器实例
        """
        locator = LocatorFactory.create_locator(
            self.driver,
            locator_type,
            locator_value,
            **kwargs
        )
        self._locators[f"{locator_type.value}:{locator_value}"] = locator
        return locator
    
    def get_locator(
        self,
        locator_type: LocatorStrategy,
        locator_value: str
    ) -> Optional[BaseLocator]:
        """
        获取定位器
        
        Args:
            locator_type: 定位类型
            locator_value: 定位值
            
        Returns:
            Optional[BaseLocator]: 定位器实例，如果不存在则返回None
        """
        return self._locators.get(f"{locator_type.value}:{locator_value}")
    
    def find_element(
        self,
        locator_type: LocatorStrategy,
        locator_value: str,
        use_cache: bool = True,
        **kwargs
    ) -> Any:
        """
        查找元素
        
        Args:
            locator_type: 定位类型
            locator_value: 定位值
            use_cache: 是否使用缓存
            **kwargs: 其他参数
            
        Returns:
            Any: 找到的元素
        """
        locator = self.get_locator(locator_type, locator_value)
        if not locator:
            locator = self.create_locator(locator_type, locator_value, **kwargs)
        
        if use_cache:
            cached_element = self.cache.get(locator)
            if cached_element:
                return cached_element
        
        element = locator.find_element()
        if use_cache:
            self.cache.set(locator, element)
        
        return element
    
    def wait_for_element(
        self,
        locator_type: LocatorStrategy,
        locator_value: str,
        condition: str = "presence",
        timeout: Optional[int] = None,
        use_cache: bool = True,
        **kwargs
    ) -> Any:
        """
        等待元素满足指定条件
        
        Args:
            locator_type: 定位类型
            locator_value: 定位值
            condition: 等待条件
            timeout: 超时时间
            use_cache: 是否使用缓存
            **kwargs: 其他参数
            
        Returns:
            Any: 满足条件的元素
        """
        locator = self.get_locator(locator_type, locator_value)
        if not locator:
            locator = self.create_locator(locator_type, locator_value, **kwargs)
        
        if use_cache:
            cached_element = self.cache.get(locator)
            if cached_element:
                return cached_element
        
        element = locator.wait_for_element(condition, timeout)
        if use_cache:
            self.cache.set(locator, element)
        
        return element
    
    def clear_cache(self) -> None:
        """清空缓存"""
        self.cache.clear()
    
    def remove_from_cache(
        self,
        locator_type: LocatorStrategy,
        locator_value: str
    ) -> None:
        """
        从缓存中移除元素
        
        Args:
            locator_type: 定位类型
            locator_value: 定位值
        """
        locator = self.get_locator(locator_type, locator_value)
        if locator:
            self.cache.remove(locator)
    
    def get_cache_info(self) -> Dict[str, Any]:
        """
        获取缓存信息
        
        Returns:
            Dict[str, Any]: 缓存信息
        """
        return self.cache.get_cache_info()
    
    def get_all_locators(self) -> List[BaseLocator]:
        """
        获取所有定位器
        
        Returns:
            List[BaseLocator]: 定位器列表
        """
        return list(self._locators.values())
    
    def clear_locators(self) -> None:
        """清空所有定位器"""
        self._locators.clear()
        self.clear_cache() 