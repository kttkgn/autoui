from typing import Any, Optional
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy as By

class Assertions:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    async def assert_element_text(self, locator: str, expected_text: str) -> bool:
        """断言元素文本内容"""
        try:
            element = await self.driver.find_element(By.XPATH, locator)
            actual_text = await element.text
            return actual_text == expected_text
        except Exception as e:
            raise Exception(f"断言元素文本失败: {str(e)}")

    async def assert_element_attribute(self, locator: str, attribute: str, expected_value: str) -> bool:
        """断言元素属性值"""
        try:
            element = await self.driver.find_element(By.XPATH, locator)
            actual_value = await element.get_attribute(attribute)
            return actual_value == expected_value
        except Exception as e:
            raise Exception(f"断言元素属性失败: {str(e)}")

    async def assert_element_visible(self, locator: str) -> bool:
        """断言元素可见"""
        try:
            element = await self.driver.find_element(By.XPATH, locator)
            return await element.is_displayed()
        except Exception as e:
            raise Exception(f"断言元素可见失败: {str(e)}")

    async def assert_element_enabled(self, locator: str) -> bool:
        """断言元素可用"""
        try:
            element = await self.driver.find_element(By.XPATH, locator)
            return await element.is_enabled()
        except Exception as e:
            raise Exception(f"断言元素可用失败: {str(e)}")

    async def assert_element_selected(self, locator: str) -> bool:
        """断言元素被选中"""
        try:
            element = await self.driver.find_element(By.XPATH, locator)
            return await element.is_selected()
        except Exception as e:
            raise Exception(f"断言元素选中失败: {str(e)}")

    async def assert_page_source_contains(self, text: str) -> bool:
        """断言页面源码包含指定文本"""
        try:
            page_source = await self.driver.page_source
            return text in page_source
        except Exception as e:
            raise Exception(f"断言页面源码失败: {str(e)}")

    async def assert_current_url(self, expected_url: str) -> bool:
        """断言当前URL"""
        try:
            current_url = await self.driver.current_url
            return current_url == expected_url
        except Exception as e:
            raise Exception(f"断言当前URL失败: {str(e)}")

    async def assert_element_count(self, locator: str, expected_count: int) -> bool:
        """断言元素数量"""
        try:
            elements = await self.driver.find_elements(By.XPATH, locator)
            return len(elements) == expected_count
        except Exception as e:
            raise Exception(f"断言元素数量失败: {str(e)}") 