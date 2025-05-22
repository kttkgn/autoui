from typing import Optional, Union, Dict, Any
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    ElementNotInteractableException
)
from app.core.logger import logger
from app.core.enums.element import LocatorStrategy

class BaseLocator:
    """元素定位器基类"""
    
    def __init__(
        self,
        driver: Any,
        locator_type: Union[str, LocatorStrategy],
        locator_value: str,
        timeout: int = 10,
        poll_frequency: float = 0.5
    ):
        """
        初始化元素定位器
        
        Args:
            driver: WebDriver实例
            locator_type: 定位类型
            locator_value: 定位值
            timeout: 等待超时时间（秒）
            poll_frequency: 轮询频率（秒）
        """
        self.driver = driver
        self.locator_type = LocatorStrategy(locator_type) if isinstance(locator_type, str) else locator_type
        self.locator_value = locator_value
        self.timeout = timeout
        self.poll_frequency = poll_frequency
        self._element = None
        
    @property
    def by(self) -> By:
        """获取Selenium的定位方式"""
        mapping = {
            LocatorStrategy.ID: By.ID,
            LocatorStrategy.NAME: By.NAME,
            LocatorStrategy.CLASS_NAME: By.CLASS_NAME,
            LocatorStrategy.TAG_NAME: By.TAG_NAME,
            LocatorStrategy.LINK_TEXT: By.LINK_TEXT,
            LocatorStrategy.PARTIAL_LINK_TEXT: By.PARTIAL_LINK_TEXT,
            LocatorStrategy.CSS_SELECTOR: By.CSS_SELECTOR,
            LocatorStrategy.XPATH: By.XPATH
        }
        return mapping.get(self.locator_type)
    
    def find_element(self) -> Any:
        """
        查找元素
        
        Returns:
            WebElement: 找到的元素
            
        Raises:
            NoSuchElementException: 元素未找到
        """
        try:
            if self.by:
                element = self.driver.find_element(self.by, self.locator_value)
            else:
                # 移动端特定的定位方式
                element = self.driver.find_element(self.locator_type.value, self.locator_value)
            self._element = element
            return element
        except NoSuchElementException as e:
            logger.error(f"元素未找到: {self.locator_type.value}={self.locator_value}")
            raise
    
    def wait_for_element(
        self,
        condition: str = "presence",
        timeout: Optional[int] = None
    ) -> Any:
        """
        等待元素满足指定条件
        
        Args:
            condition: 等待条件，可选值：
                - presence: 元素存在
                - visible: 元素可见
                - clickable: 元素可点击
                - selected: 元素被选中
            timeout: 超时时间，默认使用初始化时的timeout
            
        Returns:
            WebElement: 满足条件的元素
            
        Raises:
            TimeoutException: 等待超时
        """
        timeout = timeout or self.timeout
        wait = WebDriverWait(
            self.driver,
            timeout,
            poll_frequency=self.poll_frequency,
            ignored_exceptions=(StaleElementReferenceException,)
        )
        
        conditions = {
            "presence": EC.presence_of_element_located((self.by, self.locator_value)),
            "visible": EC.visibility_of_element_located((self.by, self.locator_value)),
            "clickable": EC.element_to_be_clickable((self.by, self.locator_value)),
            "selected": EC.element_located_to_be_selected((self.by, self.locator_value))
        }
        
        try:
            element = wait.until(conditions.get(condition, conditions["presence"]))
            self._element = element
            return element
        except TimeoutException as e:
            logger.error(f"等待元素超时: {self.locator_type.value}={self.locator_value}, condition={condition}")
            raise
    
    def is_present(self) -> bool:
        """
        检查元素是否存在
        
        Returns:
            bool: 元素是否存在
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
            bool: 元素是否可见
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
            bool: 元素是否可用
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
            bool: 元素是否被选中
        """
        try:
            element = self.find_element()
            return element.is_selected()
        except (NoSuchElementException, StaleElementReferenceException):
            return False
    
    def get_attribute(self, name: str) -> Optional[str]:
        """
        获取元素属性值
        
        Args:
            name: 属性名
            
        Returns:
            str: 属性值，如果属性不存在则返回None
        """
        try:
            element = self.find_element()
            return element.get_attribute(name)
        except (NoSuchElementException, StaleElementReferenceException):
            return None
    
    def get_text(self) -> str:
        """
        获取元素文本
        
        Returns:
            str: 元素文本
        """
        try:
            element = self.find_element()
            return element.text
        except (NoSuchElementException, StaleElementReferenceException):
            return ""
    
    def click(self) -> None:
        """
        点击元素
        
        Raises:
            ElementNotInteractableException: 元素不可交互
        """
        try:
            element = self.wait_for_element(condition="clickable")
            element.click()
        except (ElementNotInteractableException, StaleElementReferenceException) as e:
            logger.error(f"点击元素失败: {self.locator_type.value}={self.locator_value}")
            raise
    
    def input_text(self, text: str) -> None:
        """
        输入文本
        
        Args:
            text: 要输入的文本
            
        Raises:
            ElementNotInteractableException: 元素不可交互
        """
        try:
            element = self.wait_for_element(condition="visible")
            element.clear()
            element.send_keys(text)
        except (ElementNotInteractableException, StaleElementReferenceException) as e:
            logger.error(f"输入文本失败: {self.locator_type.value}={self.locator_value}, text={text}")
            raise
    
    def clear(self) -> None:
        """
        清除元素文本
        
        Raises:
            ElementNotInteractableException: 元素不可交互
        """
        try:
            element = self.wait_for_element(condition="visible")
            element.clear()
        except (ElementNotInteractableException, StaleElementReferenceException) as e:
            logger.error(f"清除文本失败: {self.locator_type.value}={self.locator_value}")
            raise
    
    def submit(self) -> None:
        """
        提交表单
        
        Raises:
            ElementNotInteractableException: 元素不可交互
        """
        try:
            element = self.wait_for_element(condition="visible")
            element.submit()
        except (ElementNotInteractableException, StaleElementReferenceException) as e:
            logger.error(f"提交表单失败: {self.locator_type.value}={self.locator_value}")
            raise
    
    def get_rect(self) -> Dict[str, int]:
        """
        获取元素位置和大小
        
        Returns:
            Dict[str, int]: 包含x、y、width、height的字典
        """
        try:
            element = self.find_element()
            rect = element.rect
            return {
                "x": rect["x"],
                "y": rect["y"],
                "width": rect["width"],
                "height": rect["height"]
            }
        except (NoSuchElementException, StaleElementReferenceException):
            return {"x": 0, "y": 0, "width": 0, "height": 0}
    
    def scroll_into_view(self) -> None:
        """
        将元素滚动到可见区域
        """
        try:
            element = self.find_element()
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        except (NoSuchElementException, StaleElementReferenceException) as e:
            logger.error(f"滚动到元素失败: {self.locator_type.value}={self.locator_value}")
            raise
    
    def take_screenshot(self, filename: str) -> bool:
        """
        对元素进行截图
        
        Args:
            filename: 截图文件名
            
        Returns:
            bool: 截图是否成功
        """
        try:
            element = self.wait_for_element(condition="visible")
            element.screenshot(filename)
            return True
        except Exception as e:
            logger.error(f"元素截图失败: {self.locator_type.value}={self.locator_value}, filename={filename}")
            return False 