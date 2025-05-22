import asyncio
import logging
from typing import Dict, List, Optional, Tuple, Any
from abc import ABC, abstractmethod
from app.models.device import Device, DeviceType
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementNotInteractableException,
    StaleElementReferenceException
)
from app.core.logger import logger
from app.core.enums.locator import LocatorType


logger = logging.getLogger(__name__)

class ElementLocator(ABC):
    """元素定位器基类"""
    
    def __init__(self, device: Device):
        self.device = device
        self._screen_stream = None
        self._element_tree = None
    
    @abstractmethod
    async def connect(self) -> bool:
        """连接设备"""
        pass
    
    @abstractmethod
    async def disconnect(self):
        """断开连接"""
        pass
    
    @abstractmethod
    async def get_screen_size(self) -> Tuple[int, int]:
        """获取屏幕尺寸"""
        pass
    
    @abstractmethod
    async def take_screenshot(self) -> bytes:
        """获取屏幕截图"""
        pass
    
    @abstractmethod
    async def get_element_tree(self) -> Dict:
        """获取元素树"""
        pass
    
    @abstractmethod
    async def find_element(self, locator: Dict[str, Any]) -> Optional[Dict]:
        """查找元素"""
        pass
    
    @abstractmethod
    async def find_elements(self, locator: Dict[str, Any]) -> List[Dict]:
        """查找多个元素"""
        pass
    
    @abstractmethod
    async def get_element_attributes(self, element_id: str) -> Dict[str, Any]:
        """获取元素属性"""
        pass
    
    @abstractmethod
    async def click_element(self, element_id: str) -> bool:
        """点击元素"""
        pass
    
    @abstractmethod
    async def input_text(self, element_id: str, text: str) -> bool:
        """输入文本"""
        pass
    
    @abstractmethod
    async def clear_text(self, element_id: str) -> bool:
        """清除文本"""
        pass
    
    @abstractmethod
    async def get_text(self, element_id: str) -> str:
        """获取文本"""
        pass
    
    @abstractmethod
    async def is_element_displayed(self, element_id: str) -> bool:
        """检查元素是否可见"""
        pass
    
    @abstractmethod
    async def is_element_enabled(self, element_id: str) -> bool:
        """检查元素是否可用"""
        pass
    
    @abstractmethod
    async def get_element_location(self, element_id: str) -> Dict[str, int]:
        """获取元素位置"""
        pass
    
    @abstractmethod
    async def get_element_size(self, element_id: str) -> Dict[str, int]:
        """获取元素大小"""
        pass
    
    @abstractmethod
    async def scroll_to_element(self, element_id: str) -> bool:
        """滚动到元素位置"""
        pass
    
    @abstractmethod
    async def wait_for_element(self, locator: Dict[str, Any], timeout: int = 10) -> Optional[Dict]:
        """等待元素出现"""
        pass
    
    @abstractmethod
    async def wait_for_element_disappear(self, locator: Dict[str, Any], timeout: int = 10) -> bool:
        """等待元素消失"""
        pass

class AndroidElementLocator(ElementLocator):
    """Android元素定位器"""
    
    def __init__(self, device: Device):
        super().__init__(device)
        self._adb = None
        self._uiautomator = None
    
    async def connect(self) -> bool:
        try:
            # 获取设备序列号
            serial = next(
                (p.value for p in self.device.properties if p.key == "serial"),
                None
            )
            if not serial:
                return False
            
            # 初始化ADB连接
            self._adb = await self._init_adb(serial)
            
            # 初始化UIAutomator2
            self._uiautomator = await self._init_uiautomator(serial)
            
            return True
        except Exception as e:
            logger.error(f"Android设备连接失败: {str(e)}")
            return False
    
    async def disconnect(self):
        if self._uiautomator:
            await self._uiautomator.quit()
        if self._adb:
            await self._adb.close()
    
    async def get_screen_size(self) -> Tuple[int, int]:
        try:
            size = await self._uiautomator.window_size()
            return size["width"], size["height"]
        except Exception as e:
            logger.error(f"获取屏幕尺寸失败: {str(e)}")
            return 0, 0
    
    async def take_screenshot(self) -> bytes:
        try:
            return await self._uiautomator.screenshot()
        except Exception as e:
            logger.error(f"获取屏幕截图失败: {str(e)}")
            return b""
    
    async def get_element_tree(self) -> Dict:
        try:
            return await self._uiautomator.dump_hierarchy()
        except Exception as e:
            logger.error(f"获取元素树失败: {str(e)}")
            return {}
    
    async def find_element(self, locator: Dict[str, Any]) -> Optional[Dict]:
        try:
            return await self._uiautomator.find_element(**locator)
        except Exception as e:
            logger.error(f"查找元素失败: {str(e)}")
            return None
    
    async def find_elements(self, locator: Dict[str, Any]) -> List[Dict]:
        try:
            return await self._uiautomator.find_elements(**locator)
        except Exception as e:
            logger.error(f"查找多个元素失败: {str(e)}")
            return []
    
    async def get_element_attributes(self, element_id: str) -> Dict[str, Any]:
        try:
            element = await self._uiautomator.element(element_id)
            return await element.attributes()
        except Exception as e:
            logger.error(f"获取元素属性失败: {str(e)}")
            return {}
    
    async def click_element(self, element_id: str) -> bool:
        try:
            element = await self._uiautomator.element(element_id)
            await element.click()
            return True
        except Exception as e:
            logger.error(f"点击元素失败: {str(e)}")
            return False
    
    async def input_text(self, element_id: str, text: str) -> bool:
        try:
            element = await self._uiautomator.element(element_id)
            await element.set_text(text)
            return True
        except Exception as e:
            logger.error(f"输入文本失败: {str(e)}")
            return False
    
    async def clear_text(self, element_id: str) -> bool:
        try:
            element = await self._uiautomator.element(element_id)
            await element.clear_text()
            return True
        except Exception as e:
            logger.error(f"清除文本失败: {str(e)}")
            return False
    
    async def get_text(self, element_id: str) -> str:
        try:
            element = await self._uiautomator.element(element_id)
            return await element.text()
        except Exception as e:
            logger.error(f"获取文本失败: {str(e)}")
            return ""
    
    async def is_element_displayed(self, element_id: str) -> bool:
        try:
            element = await self._uiautomator.element(element_id)
            return await element.is_displayed()
        except Exception as e:
            logger.error(f"检查元素可见性失败: {str(e)}")
            return False
    
    async def is_element_enabled(self, element_id: str) -> bool:
        try:
            element = await self._uiautomator.element(element_id)
            return await element.is_enabled()
        except Exception as e:
            logger.error(f"检查元素可用性失败: {str(e)}")
            return False
    
    async def get_element_location(self, element_id: str) -> Dict[str, int]:
        try:
            element = await self._uiautomator.element(element_id)
            location = await element.location()
            return {
                "x": location["x"],
                "y": location["y"]
            }
        except Exception as e:
            logger.error(f"获取元素位置失败: {str(e)}")
            return {"x": 0, "y": 0}
    
    async def get_element_size(self, element_id: str) -> Dict[str, int]:
        try:
            element = await self._uiautomator.element(element_id)
            size = await element.size()
            return {
                "width": size["width"],
                "height": size["height"]
            }
        except Exception as e:
            logger.error(f"获取元素大小失败: {str(e)}")
            return {"width": 0, "height": 0}
    
    async def scroll_to_element(self, element_id: str) -> bool:
        try:
            element = await self._uiautomator.element(element_id)
            await element.scroll_into_view()
            return True
        except Exception as e:
            logger.error(f"滚动到元素位置失败: {str(e)}")
            return False
    
    async def wait_for_element(self, locator: Dict[str, Any], timeout: int = 10) -> Optional[Dict]:
        try:
            return await self._uiautomator.wait_for_element(**locator, timeout=timeout)
        except Exception as e:
            logger.error(f"等待元素出现失败: {str(e)}")
            return None
    
    async def wait_for_element_disappear(self, locator: Dict[str, Any], timeout: int = 10) -> bool:
        try:
            await self._uiautomator.wait_for_element_disappear(**locator, timeout=timeout)
            return True
        except Exception as e:
            logger.error(f"等待元素消失失败: {str(e)}")
            return False
    
    async def _init_adb(self, serial: str):
        """初始化ADB连接"""
        # TODO: 实现ADB连接初始化
        pass
    
    async def _init_uiautomator(self, serial: str):
        """初始化UIAutomator2"""
        # TODO: 实现UIAutomator2初始化
        pass

class IOSElementLocator(ElementLocator):
    """iOS元素定位器"""
    
    def __init__(self, device: Device):
        super().__init__(device)
        self._wda = None
    
    async def connect(self) -> bool:
        try:
            # 获取设备UDID
            udid = next(
                (p.value for p in self.device.properties if p.key == "udid"),
                None
            )
            if not udid:
                return False
            
            # 初始化WebDriverAgent
            self._wda = await self._init_wda(udid)
            
            return True
        except Exception as e:
            logger.error(f"iOS设备连接失败: {str(e)}")
            return False
    
    async def disconnect(self):
        if self._wda:
            await self._wda.quit()
    
    # TODO: 实现iOS元素定位器的其他方法

class WebElementLocator(ElementLocator):
    """Web元素定位器"""
    
    def __init__(self, device: Device):
        super().__init__(device)
        self._driver = None
    
    async def connect(self) -> bool:
        try:
            # 获取浏览器类型
            browser = next(
                (p.value for p in self.device.properties if p.key == "browser"),
                None
            )
            if not browser:
                return False
            
            # 初始化WebDriver
            self._driver = await self._init_webdriver(browser)
            
            return True
        except Exception as e:
            logger.error(f"Web浏览器连接失败: {str(e)}")
            return False
    
    async def disconnect(self):
        if self._driver:
            await self._driver.quit()
    
    # TODO: 实现Web元素定位器的其他方法

def create_element_locator(device: Device) -> Optional[ElementLocator]:
    """创建元素定位器"""
    if device.type == DeviceType.ANDROID:
        return AndroidElementLocator(device)
    elif device.type == DeviceType.IOS:
        return IOSElementLocator(device)
    elif device.type == DeviceType.WEB:
        return WebElementLocator(device)
    return None

class ElementLocator:
    """元素定位器"""
    
    def __init__(
        self,
        driver,
        locator_type: LocatorType,
        locator_value: str,
        timeout: int = 10,
        poll_frequency: float = 0.5
    ):
        """
        初始化元素定位器
        
        Args:
            driver: WebDriver实例
            locator_type: 定位方式
            locator_value: 定位值
            timeout: 超时时间(秒)
            poll_frequency: 轮询频率(秒)
        """
        self.driver = driver
        self.locator_type = locator_type
        self.locator_value = locator_value
        self.timeout = timeout
        self.poll_frequency = poll_frequency
        self.wait = WebDriverWait(
            driver,
            timeout,
            poll_frequency=poll_frequency
        )
    
    def find_element(self):
        """
        查找元素
        
        Returns:
            WebElement: 找到的元素
            
        Raises:
            NoSuchElementException: 元素未找到
        """
        try:
            return self.driver.find_element(
                self._get_by(),
                self.locator_value
            )
        except NoSuchElementException as e:
            logger.error(f"元素未找到: {self.locator_value}")
            raise
    
    def wait_for_element(
        self,
        condition: str = "presence",
        timeout: Optional[int] = None
    ):
        """
        等待元素
        
        Args:
            condition: 等待条件
            timeout: 超时时间(秒)
            
        Returns:
            WebElement: 找到的元素
            
        Raises:
            TimeoutException: 等待超时
        """
        try:
            if timeout:
                self.wait = WebDriverWait(
                    self.driver,
                    timeout,
                    poll_frequency=self.poll_frequency
                )
            
            if condition == "presence":
                return self.wait.until(
                    EC.presence_of_element_located((
                        self._get_by(),
                        self.locator_value
                    ))
                )
            elif condition == "visibility":
                return self.wait.until(
                    EC.visibility_of_element_located((
                        self._get_by(),
                        self.locator_value
                    ))
                )
            elif condition == "clickable":
                return self.wait.until(
                    EC.element_to_be_clickable((
                        self._get_by(),
                        self.locator_value
                    ))
                )
            elif condition == "selected":
                return self.wait.until(
                    EC.element_located_to_be_selected((
                        self._get_by(),
                        self.locator_value
                    ))
                )
            else:
                raise ValueError(f"不支持的等待条件: {condition}")
                
        except TimeoutException as e:
            logger.error(f"等待元素超时: {self.locator_value}")
            raise
    
    def is_present(self) -> bool:
        """
        检查元素是否存在
        
        Returns:
            bool: 是否存在
        """
        try:
            self.find_element()
            return True
        except NoSuchElementException:
            return False
    
    def is_visible(self) -> bool:
        """
        检查元素是否可见
        
        Returns:
            bool: 是否可见
        """
        try:
            element = self.find_element()
            return element.is_displayed()
        except (NoSuchElementException, StaleElementReferenceException):
            return False
    
    def is_enabled(self) -> bool:
        """
        检查元素是否可用
        
        Returns:
            bool: 是否可用
        """
        try:
            element = self.find_element()
            return element.is_enabled()
        except (NoSuchElementException, StaleElementReferenceException):
            return False
    
    def is_selected(self) -> bool:
        """
        检查元素是否被选中
        
        Returns:
            bool: 是否被选中
        """
        try:
            element = self.find_element()
            return element.is_selected()
        except (NoSuchElementException, StaleElementReferenceException):
            return False
    
    def click(self):
        """
        点击元素
        
        Raises:
            ElementNotInteractableException: 元素不可交互
        """
        try:
            element = self.wait_for_element(condition="clickable")
            element.click()
        except ElementNotInteractableException as e:
            logger.error(f"元素不可点击: {self.locator_value}")
            raise
    
    def input_text(self, text: str):
        """
        输入文本
        
        Args:
            text: 要输入的文本
            
        Raises:
            ElementNotInteractableException: 元素不可交互
        """
        try:
            element = self.wait_for_element(condition="visibility")
            element.clear()
            element.send_keys(text)
        except ElementNotInteractableException as e:
            logger.error(f"元素不可输入: {self.locator_value}")
            raise
    
    def clear(self):
        """
        清除文本
        
        Raises:
            ElementNotInteractableException: 元素不可交互
        """
        try:
            element = self.wait_for_element(condition="visibility")
            element.clear()
        except ElementNotInteractableException as e:
            logger.error(f"元素不可清除: {self.locator_value}")
            raise
    
    def submit(self):
        """
        提交表单
        
        Raises:
            ElementNotInteractableException: 元素不可交互
        """
        try:
            element = self.wait_for_element(condition="clickable")
            element.submit()
        except ElementNotInteractableException as e:
            logger.error(f"元素不可提交: {self.locator_value}")
            raise
    
    def get_text(self) -> str:
        """
        获取文本
        
        Returns:
            str: 元素文本
        """
        try:
            element = self.wait_for_element(condition="visibility")
            return element.text
        except Exception as e:
            logger.error(f"获取文本失败: {self.locator_value}")
            raise
    
    def get_attribute(self, name: str) -> Optional[str]:
        """
        获取属性值
        
        Args:
            name: 属性名
            
        Returns:
            Optional[str]: 属性值
        """
        try:
            element = self.wait_for_element(condition="presence")
            return element.get_attribute(name)
        except Exception as e:
            logger.error(f"获取属性失败: {self.locator_value} -> {name}")
            raise
    
    def get_css_value(self, name: str) -> str:
        """
        获取CSS属性值
        
        Args:
            name: CSS属性名
            
        Returns:
            str: CSS属性值
        """
        try:
            element = self.wait_for_element(condition="presence")
            return element.value_of_css_property(name)
        except Exception as e:
            logger.error(f"获取CSS属性失败: {self.locator_value} -> {name}")
            raise
    
    def get_size(self) -> Dict[str, int]:
        """
        获取元素大小
        
        Returns:
            Dict[str, int]: 元素大小
        """
        try:
            element = self.wait_for_element(condition="presence")
            size = element.size
            return {
                "width": size["width"],
                "height": size["height"]
            }
        except Exception as e:
            logger.error(f"获取元素大小失败: {self.locator_value}")
            raise
    
    def get_location(self) -> Dict[str, int]:
        """
        获取元素位置
        
        Returns:
            Dict[str, int]: 元素位置
        """
        try:
            element = self.wait_for_element(condition="presence")
            location = element.location
            return {
                "x": location["x"],
                "y": location["y"]
            }
        except Exception as e:
            logger.error(f"获取元素位置失败: {self.locator_value}")
            raise
    
    def scroll_into_view(self):
        """
        滚动到元素位置
        """
        try:
            element = self.wait_for_element(condition="presence")
            self.driver.execute_script(
                "arguments[0].scrollIntoView(true);",
                element
            )
        except Exception as e:
            logger.error(f"滚动到元素位置失败: {self.locator_value}")
            raise
    
    def take_screenshot(self) -> str:
        """
        获取元素截图
        
        Returns:
            str: 截图文件路径
        """
        try:
            element = self.wait_for_element(condition="presence")
            return element.screenshot_as_png
        except Exception as e:
            logger.error(f"获取元素截图失败: {self.locator_value}")
            raise
    
    def get_rect(self) -> Dict[str, int]:
        """
        获取元素矩形区域
        
        Returns:
            Dict[str, int]: 矩形区域
        """
        try:
            element = self.wait_for_element(condition="presence")
            rect = element.rect
            return {
                "x": rect["x"],
                "y": rect["y"],
                "width": rect["width"],
                "height": rect["height"]
            }
        except Exception as e:
            logger.error(f"获取元素矩形区域失败: {self.locator_value}")
            raise
    
    def _get_by(self):
        """
        获取定位方式
        
        Returns:
            By: 定位方式
        """
        if self.locator_type == LocatorType.ID:
            return AppiumBy.ID
        elif self.locator_type == LocatorType.NAME:
            return AppiumBy.NAME
        elif self.locator_type == LocatorType.CLASS_NAME:
            return AppiumBy.CLASS_NAME
        elif self.locator_type == LocatorType.TAG_NAME:
            return AppiumBy.TAG_NAME
        elif self.locator_type == LocatorType.LINK_TEXT:
            return AppiumBy.LINK_TEXT
        elif self.locator_type == LocatorType.PARTIAL_LINK_TEXT:
            return AppiumBy.PARTIAL_LINK_TEXT
        elif self.locator_type == LocatorType.XPATH:
            return AppiumBy.XPATH
        elif self.locator_type == LocatorType.CSS_SELECTOR:
            return AppiumBy.CSS_SELECTOR
        elif self.locator_type == LocatorType.ACCESSIBILITY_ID:
            return AppiumBy.ACCESSIBILITY_ID
        elif self.locator_type == LocatorType.ANDROID_UIAUTOMATOR:
            return AppiumBy.ANDROID_UIAUTOMATOR
        elif self.locator_type == LocatorType.IOS_PREDICATE:
            return AppiumBy.IOS_PREDICATE
        elif self.locator_type == LocatorType.IOS_CLASS_CHAIN:
            return AppiumBy.IOS_CLASS_CHAIN
        else:
            raise ValueError(f"不支持的定位方式: {self.locator_type}")


def create_element_locator(
    driver,
    locator_type: LocatorType,
    locator_value: str,
    timeout: int = 10,
    poll_frequency: float = 0.5
) -> ElementLocator:
    """
    创建元素定位器
    
    Args:
        driver: WebDriver实例
        locator_type: 定位方式
        locator_value: 定位值
        timeout: 超时时间(秒)
        poll_frequency: 轮询频率(秒)
        
    Returns:
        ElementLocator: 元素定位器实例
    """
    return ElementLocator(
        driver,
        locator_type,
        locator_value,
        timeout,
        poll_frequency
    ) 