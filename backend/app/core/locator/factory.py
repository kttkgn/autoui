from typing import Dict, Type, Any
from app.core.locator.base import BaseLocator
from app.core.enums.element import LocatorStrategy

class LocatorFactory:
    """定位器工厂类"""
    
    _locators: Dict[LocatorStrategy, Type[BaseLocator]] = {}
    
    @classmethod
    def register_locator(cls, locator_type: LocatorStrategy, locator_class: Type[BaseLocator]) -> None:
        """
        注册定位器类
        
        Args:
            locator_type: 定位类型
            locator_class: 定位器类
        """
        cls._locators[locator_type] = locator_class
    
    @classmethod
    def create_locator(
        cls,
        driver: Any,
        locator_type: LocatorStrategy,
        locator_value: str,
        **kwargs
    ) -> BaseLocator:
        """
        创建定位器实例
        
        Args:
            driver: WebDriver实例
            locator_type: 定位类型
            locator_value: 定位值
            **kwargs: 其他参数
            
        Returns:
            BaseLocator: 定位器实例
            
        Raises:
            ValueError: 不支持的定位类型
        """
        locator_class = cls._locators.get(locator_type)
        if not locator_class:
            # 如果没有注册特定的定位器类，使用基础定位器
            locator_class = BaseLocator
        
        return locator_class(driver, locator_type, locator_value, **kwargs) 