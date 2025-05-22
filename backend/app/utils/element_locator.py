from typing import Optional, Any
import asyncio
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver

class ElementLocator:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    async def find_element(self, locator: str) -> Optional[Any]:
        """查找元素
        
        Args:
            locator: 元素定位表达式，格式为 "定位方式:定位值"
                    支持的定位方式：
                    - id: 元素ID
                    - xpath: XPath表达式
                    - name: 元素名称
                    - class: 元素类名
                    - accessibility_id: 无障碍ID
                    - android_uiautomator: Android UI Automator表达式
                    - ios_predicate: iOS Predicate表达式
        """
        try:
            locator_type, locator_value = locator.split(":", 1)
            locator_type = locator_type.strip().lower()
            locator_value = locator_value.strip()

            if locator_type == "id":
                return await self.driver.find_element(AppiumBy.ID, locator_value)
            elif locator_type == "xpath":
                return await self.driver.find_element(AppiumBy.XPATH, locator_value)
            elif locator_type == "name":
                return await self.driver.find_element(AppiumBy.NAME, locator_value)
            elif locator_type == "class":
                return await self.driver.find_element(AppiumBy.CLASS_NAME, locator_value)
            elif locator_type == "accessibility_id":
                return await self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, locator_value)
            elif locator_type == "android_uiautomator":
                return await self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, locator_value)
            elif locator_type == "ios_predicate":
                return await self.driver.find_element(AppiumBy.IOS_PREDICATE, locator_value)
            else:
                raise Exception(f"不支持的定位方式: {locator_type}")
        except Exception as e:
            raise Exception(f"查找元素失败: {str(e)}")

    async def wait_for_element(self, locator: str, timeout: int = 10) -> Optional[Any]:
        """等待元素出现"""
        try:
            element = await self.find_element(locator)
            if element:
                return element
            await asyncio.sleep(1)
            timeout -= 1
            if timeout <= 0:
                raise Exception("等待元素超时")
            return await self.wait_for_element(locator, timeout)
        except Exception as e:
            raise Exception(f"等待元素失败: {str(e)}")

    async def is_element_present(self, locator: str) -> bool:
        """检查元素是否存在"""
        try:
            await self.find_element(locator)
            return True
        except:
            return False 