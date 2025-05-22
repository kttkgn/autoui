from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from selenium.webdriver.remote.webdriver import WebDriver
from abc import ABC, abstractmethod

from app.core.locator.manager import LocatorManager
from app.core.logger import logger
from app.models.project import TestExecution, TestStepResult, TestCase
from app.schemas.project import TestStep

from app.schemas.test_execution import TestStepResultCreate
from app.core.exceptions import TestExecutionError, TestStepError

class TestEngine(ABC):
    """测试引擎基类"""
    
    @abstractmethod
    def execute(self, test_case: Dict[str, Any], data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """执行测试用例"""
        pass

class DataDrivenTestEngine(TestEngine):
    """数据驱动测试引擎"""
    
    def execute(self, test_case: Dict[str, Any], data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        执行数据驱动测试用例
        
        Args:
            test_case: 测试用例数据
            data: 数据驱动参数
        
        Returns:
            执行结果
        """
        if not data:
            data = {}
        
        # 替换测试用例中的变量
        steps = test_case.get("steps", [])
        for step in steps:
            for key, value in data.items():
                if isinstance(step, dict) and key in step:
                    step[key] = value
        
        # 执行测试步骤
        results = []
        for step in steps:
            try:
                # 执行步骤逻辑（示例）
                result = {"step": step, "status": "passed", "message": "步骤执行成功"}
            except Exception as e:
                result = {"step": step, "status": "failed", "message": str(e)}
            results.append(result)
        
        return {"test_case": test_case, "results": results}

class KeywordDrivenTestEngine(TestEngine):
    """关键字驱动测试引擎"""
    
    def execute(self, test_case: Dict[str, Any], data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        执行关键字驱动测试用例
        
        Args:
            test_case: 测试用例数据
            data: 关键字参数
        
        Returns:
            执行结果
        """
        if not data:
            data = {}
        
        # 解析关键字
        keywords = test_case.get("keywords", [])
        results = []
        for keyword in keywords:
            try:
                # 执行关键字逻辑（示例）
                result = {"keyword": keyword, "status": "passed", "message": "关键字执行成功"}
            except Exception as e:
                result = {"keyword": keyword, "status": "failed", "message": str(e)}
            results.append(result)
        
        return {"test_case": test_case, "results": results}

class TestEngine:
    """测试执行引擎"""
    
    def __init__(self, driver: WebDriver):
        """
        初始化测试执行引擎
        
        Args:
            driver: WebDriver实例
        """
        self.driver = driver
        self.locator_manager = LocatorManager()
        self.locator_manager.set_driver(driver)
        self.current_execution: Optional[TestExecution] = None
        self.current_step: Optional[TestStep] = None
        self.step_results: List[TestStepResult] = []
        
    async def execute_test_case(self, test_case: TestCase) -> TestExecution:
        """
        执行测试用例
        
        Args:
            test_case: 测试用例对象
            
        Returns:
            TestExecution: 测试执行记录
        """
        try:
            # 创建测试执行记录
            self.current_execution = TestExecution(
                test_case_id=test_case.id,
                device_id=test_case.device_id,
                status="running",
                start_time=datetime.now()
            )
            
            # 执行测试步骤
            for step in test_case.steps:
                await self.execute_step(step)
                
            # 更新执行状态
            self.current_execution.status = "completed"
            self.current_execution.end_time = datetime.now()
            
            return self.current_execution
            
        except Exception as e:
            logger.error(f"测试用例执行失败: {str(e)}")
            if self.current_execution:
                self.current_execution.status = "failed"
                self.current_execution.error_message = str(e)
                self.current_execution.end_time = datetime.now()
            raise TestExecutionError(f"测试用例执行失败: {str(e)}")
            
    async def execute_step(self, step: TestStep) -> TestStepResult:
        """
        执行测试步骤
        
        Args:
            step: 测试步骤对象
            
        Returns:
            TestStepResult: 步骤执行结果
        """
        try:
            self.current_step = step
            logger.info(f"开始执行步骤: {step.name}")
            
            # 创建步骤结果记录
            step_result = TestStepResult(
                test_execution_id=self.current_execution.id,
                test_step_id=step.id,
                status="running",
                start_time=datetime.now()
            )
            
            # 执行步骤操作
            await self.execute_step_action(step)
            
            # 执行断言
            if step.assertions:
                await self.execute_assertions(step.assertions)
                
            # 更新步骤状态
            step_result.status = "passed"
            step_result.end_time = datetime.now()
            
            self.step_results.append(step_result)
            return step_result
            
        except Exception as e:
            logger.error(f"步骤执行失败: {str(e)}")
            if step_result:
                step_result.status = "failed"
                step_result.error_message = str(e)
                step_result.end_time = datetime.now()
            raise TestStepError(f"步骤执行失败: {str(e)}")
            
    async def execute_step_action(self, step: TestStep) -> None:
        """
        执行步骤操作
        
        Args:
            step: 测试步骤对象
        """
        try:
            # 获取元素定位器
            locator = self.locator_manager.create_locator_from_dict(step.locator)
            
            # 执行操作
            if step.action == "click":
                locator.click()
            elif step.action == "input":
                locator.input_text(step.value)
            elif step.action == "clear":
                locator.clear()
            elif step.action == "submit":
                locator.submit()
            elif step.action == "scroll":
                locator.scroll_to()
            elif step.action == "hover":
                locator.hover()
            elif step.action == "double_click":
                locator.double_click()
            elif step.action == "right_click":
                locator.right_click()
            elif step.action == "drag_and_drop":
                locator.drag_and_drop(step.target_locator)
            else:
                raise ValueError(f"不支持的操作类型: {step.action}")
                
        except Exception as e:
            raise TestStepError(f"步骤操作执行失败: {str(e)}")
            
    async def execute_assertions(self, assertions: List[Dict[str, Any]]) -> None:
        """
        执行断言
        
        Args:
            assertions: 断言列表
        """
        for assertion in assertions:
            try:
                # 获取元素定位器
                locator = self.locator_manager.create_locator_from_dict(assertion["locator"])
                
                # 执行断言
                if assertion["type"] == "present":
                    if not locator.is_present():
                        raise AssertionError("元素不存在")
                elif assertion["type"] == "visible":
                    if not locator.is_visible():
                        raise AssertionError("元素不可见")
                elif assertion["type"] == "enabled":
                    if not locator.is_enabled():
                        raise AssertionError("元素不可用")
                elif assertion["type"] == "selected":
                    if not locator.is_selected():
                        raise AssertionError("元素未选中")
                elif assertion["type"] == "text":
                    if locator.get_text() != assertion["value"]:
                        raise AssertionError(f"文本不匹配: 期望 {assertion['value']}, 实际 {locator.get_text()}")
                elif assertion["type"] == "attribute":
                    if locator.get_attribute(assertion["attribute"]) != assertion["value"]:
                        raise AssertionError(f"属性不匹配: {assertion['attribute']}")
                elif assertion["type"] == "css_property":
                    if locator.get_css_property(assertion["property"]) != assertion["value"]:
                        raise AssertionError(f"CSS属性不匹配: {assertion['property']}")
                elif assertion["type"] == "count":
                    if locator.get_count() != assertion["value"]:
                        raise AssertionError(f"元素数量不匹配: 期望 {assertion['value']}, 实际 {locator.get_count()}")
                elif assertion["type"] == "contains_text":
                    if assertion["value"] not in locator.get_text():
                        raise AssertionError(f"文本不包含: {assertion['value']}")
                elif assertion["type"] == "contains_attribute":
                    if assertion["value"] not in locator.get_attribute(assertion["attribute"]):
                        raise AssertionError(f"属性不包含: {assertion['attribute']}")
                else:
                    raise ValueError(f"不支持的断言类型: {assertion['type']}")
                    
            except Exception as e:
                raise TestStepError(f"断言执行失败: {str(e)}")
                
    def take_screenshot(self, step_result: TestStepResult) -> None:
        """
        截图
        
        Args:
            step_result: 步骤执行结果
        """
        try:
            if self.current_step and self.current_step.locator:
                locator = self.locator_manager.create_locator_from_dict(self.current_step.locator)
                screenshot_path = locator.take_screenshot()
                step_result.screenshot = screenshot_path
        except Exception as e:
            logger.error(f"截图失败: {str(e)}")
            
    def cleanup(self) -> None:
        """清理资源"""
        self.current_execution = None
        self.current_step = None
        self.step_results = []
        self.locator_manager.clear_locators() 