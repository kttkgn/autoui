import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
from abc import ABC, abstractmethod
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.test_case import test_case_crud
from app.crud.test_execution import test_execution_crud
from app.core.config import settings
from app.utils.device_manager import DeviceManager
from app.utils.element_locator import ElementLocator
from app.utils.screenshot import take_screenshot
from app.utils.assertions import Assertions
from app.utils.data_driver import DataDriver
from app.models.device import Device
from app.models.project import TestCase, TestExecution, TestStepResult
from app.services.element_locator import create_element_locator
from app.core.logger import logger
from app.core.test_engine import TestEngine
from app.schemas.project import TestExecutionResponse

logger = logging.getLogger(__name__)

class TestExecutor(ABC):
    """测试执行器基类"""
    
    def __init__(self, db: AsyncSession, execution_id: int):
        self.db = db
        self.execution_id = execution_id
        self.device = None
        self.locator = None
        self.assertions = None
        self.test_data = None
        self.current_data_index = 0
        self.execution = None
        self.current_step = None
        self.variables = {}
        self.test_engine = TestEngine()
        self.test_case_id = None
        self.device_id = None
        self.step_results: List[TestStepResult] = []

    async def initialize(self):
        """初始化测试执行环境"""
        try:
            # 获取执行记录
            self.execution = await test_execution_crud.get(self.db, self.execution_id)
            if not self.execution:
                raise Exception("执行记录不存在")

            # 获取测试用例
            self.test_case = await test_case_crud.get(self.db, self.execution.test_case_id)
            if not self.test_case:
                raise Exception("测试用例不存在")

            # 初始化设备
            self.device = await DeviceManager.get_device(self.execution.device_name)
            if not self.device:
                raise Exception(f"设备 {self.execution.device_name} 不可用")

            # 初始化元素定位器
            self.locator = create_element_locator(self.device)
            
            # 初始化断言工具
            self.assertions = Assertions(self.device)

            # 加载测试数据
            if self.test_case.data_driven:
                self.test_data = await DataDriver.load_test_data(self.test_case.data_driven)
                if not self.test_data:
                    raise Exception("加载测试数据失败")

            return True
        except Exception as e:
            await self._handle_error(str(e))
            return False

    async def execute(self):
        """执行测试用例"""
        if not await self.initialize():
            return

        try:
            if self.test_data:
                # 数据驱动执行
                for i, data in enumerate(self.test_data):
                    self.current_data_index = i
                    await self._execute_with_data(data)
            else:
                # 普通执行
                await self._execute_steps(self.test_case.steps)

            # 所有执行成功
            await test_execution_crud.update_execution_status(
                self.db,
                self.execution_id,
                "success"
            )
            self.step_results = self.execution.step_results
            return self.execution
        except Exception as e:
            await self._handle_error(str(e))
        finally:
            await self._cleanup()

    async def _execute_with_data(self, data: Dict[str, Any]):
        """使用测试数据执行测试用例"""
        try:
            # 替换步骤中的变量
            steps = await self._replace_step_variables(self.test_case.steps, data)
            await self._execute_steps(steps)
        except Exception as e:
            raise Exception(f"执行测试数据 {self.current_data_index + 1} 失败: {str(e)}")

    async def _execute_steps(self, steps: List[Dict[str, Any]]):
        """执行测试步骤列表"""
        for step in steps:
            await self._execute_step(step)

    async def _execute_step(self, step: Dict[str, Any]):
        """执行单个测试步骤"""
        try:
            # 查找元素
            element = await self.locator.find_element(step["element"])
            if not element:
                raise Exception(f"未找到元素: {step['element']}")

            # 执行操作
            result = await self._perform_action(element, step)
            
            # 记录步骤结果
            await test_execution_crud.create_step_result(
                self.db,
                self.execution_id,
                step["step_number"],
                step["action"],
                step["element"],
                step.get("value"),
                "success",
                "步骤执行成功",
                await take_screenshot(self.device)
            )
        except Exception as e:
            # 记录失败结果
            await test_execution_crud.create_step_result(
                self.db,
                self.execution_id,
                step["step_number"],
                step["action"],
                step["element"],
                step.get("value"),
                "failed",
                str(e),
                await take_screenshot(self.device)
            )
            raise

    async def _replace_step_variables(self, steps: List[Dict[str, Any]], data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """替换步骤中的变量"""
        result = []
        for step in steps:
            new_step = {}
            for key, value in step.items():
                if isinstance(value, str):
                    # 替换字符串中的变量
                    for var_name, var_value in data.items():
                        value = value.replace(f"${{{var_name}}}", str(var_value))
                new_step[key] = value
            result.append(new_step)
        return result

    async def _perform_action(self, element: Any, step: Dict[str, Any]):
        """执行具体的操作"""
        action = step["action"]
        value = step.get("value")

        if action == "click":
            await element.click()
        elif action == "input":
            await element.clear()
            await element.send_keys(value)
        elif action == "wait":
            await asyncio.sleep(float(value))
        elif action == "assert":
            await self._perform_assertion(step)
        else:
            raise Exception(f"不支持的操作: {action}")

    async def _perform_assertion(self, step: Dict[str, Any]):
        """执行断言操作"""
        assert_type = step.get("assert_type")
        if not assert_type:
            raise Exception("未指定断言类型")

        element = step["element"]
        value = step.get("value")

        if assert_type == "text":
            if not value:
                raise Exception("断言文本内容时未指定预期值")
            result = await self.assertions.assert_element_text(element, value)
        elif assert_type == "attribute":
            attribute = step.get("attribute")
            if not attribute or not value:
                raise Exception("断言属性时未指定属性名或预期值")
            result = await self.assertions.assert_element_attribute(element, attribute, value)
        elif assert_type == "visible":
            result = await self.assertions.assert_element_visible(element)
        elif assert_type == "enabled":
            result = await self.assertions.assert_element_enabled(element)
        elif assert_type == "selected":
            result = await self.assertions.assert_element_selected(element)
        elif assert_type == "count":
            if not value:
                raise Exception("断言元素数量时未指定预期值")
            result = await self.assertions.assert_element_count(element, int(value))
        elif assert_type == "page_source":
            if not value:
                raise Exception("断言页面源码时未指定预期值")
            result = await self.assertions.assert_page_source_contains(value)
        elif assert_type == "url":
            if not value:
                raise Exception("断言URL时未指定预期值")
            result = await self.assertions.assert_current_url(value)
        else:
            raise Exception(f"不支持的断言类型: {assert_type}")

        if not result:
            raise Exception(f"断言失败: {assert_type}")

    async def _handle_error(self, error_message: str):
        """处理执行过程中的错误"""
        await test_execution_crud.update_execution_status(
            self.db,
            self.execution_id,
            "failed",
            error_message
        )

    async def _cleanup(self):
        """清理测试环境"""
        if self.device:
            await DeviceManager.release_device(self.device)

    async def stop(self) -> None:
        """停止测试执行"""
        try:
            self.test_engine.stop_execution(self.execution_id)
        except Exception as e:
            logger.error(f"停止测试执行失败: {str(e)}")
            raise

    def get_status(self) -> str:
        """
        获取执行状态
        
        Returns:
            str: 执行状态
        """
        try:
            return self.test_engine.get_execution_status(self.execution_id)
        except Exception as e:
            logger.error(f"获取执行状态失败: {str(e)}")
            raise

    def get_step_results(self) -> List[TestStepResult]:
        """
        获取步骤执行结果
        
        Returns:
            List[TestStepResult]: 步骤执行结果列表
        """
        try:
            return self.test_engine.get_step_results(self.execution_id)
        except Exception as e:
            logger.error(f"获取步骤执行结果失败: {str(e)}")
            raise

    def retry_step(self, step_number: int) -> TestStepResult:
        """
        重试步骤
        
        Args:
            step_number: 步骤编号
            
        Returns:
            TestStepResult: 步骤执行结果
        """
        try:
            return self.test_engine.retry_step(self.execution_id, step_number)
        except Exception as e:
            logger.error(f"重试步骤失败: {str(e)}")
            raise

    def get_execution_history(self) -> List[TestExecutionResponse]:
        """
        获取执行历史
        
        Returns:
            List[TestExecutionResponse]: 执行历史列表
        """
        try:
            return self.test_engine.get_execution_history(self.test_case_id)
        except Exception as e:
            logger.error(f"获取执行历史失败: {str(e)}")
            raise

    def generate_project_summary(self, project_id: int) -> Dict[str, Any]:
        """
        生成项目执行汇总报告
        
        Args:
            project_id: 项目ID
            
        Returns:
            Dict[str, Any]: 汇总报告
        """
        try:
            return self.test_engine.generate_project_summary(project_id)
        except Exception as e:
            logger.error(f"生成项目执行汇总失败: {str(e)}")
            raise

    def export_project_summary(
        self,
        project_id: int,
        format: str = "pdf"
    ) -> str:
        """
        导出项目执行汇总报告
        
        Args:
            project_id: 项目ID
            format: 导出格式
            
        Returns:
            str: 报告文件路径
        """
        try:
            return self.test_engine.export_project_summary(project_id, format)
        except Exception as e:
            logger.error(f"导出项目执行汇总失败: {str(e)}")
            raise

class AndroidTestExecutor(TestExecutor):
    """Android测试执行器"""
    
    async def _execute_script(self, script: str) -> None:
        """执行Android脚本"""
        # TODO: 实现Android脚本执行
        pass

class IOSTestExecutor(TestExecutor):
    """iOS测试执行器"""
    
    async def _execute_script(self, script: str) -> None:
        """执行iOS脚本"""
        # TODO: 实现iOS脚本执行
        pass

class WebTestExecutor(TestExecutor):
    """Web测试执行器"""
    
    async def _execute_script(self, script: str) -> None:
        """执行Web脚本"""
        # TODO: 实现Web脚本执行
        pass

def create_test_executor(
    test_case_id: Optional[int] = None,
    device_id: Optional[str] = None,
    execution_id: Optional[int] = None
) -> TestExecutor:
    """
    创建测试执行器
    
    Args:
        test_case_id: 测试用例ID
        device_id: 设备ID
        execution_id: 执行记录ID
        
    Returns:
        TestExecutor: 测试执行器实例
    """
    executor = TestExecutor(None, execution_id)
    executor.test_case_id = test_case_id
    executor.device_id = device_id
    return executor

async def execute_test_case(executor: TestExecutor) -> TestExecutionResponse:
    """
    执行测试用例
    
    Args:
        executor: 测试执行器
        
    Returns:
        TestExecutionResponse: 执行结果
    """
    return await executor.execute() 