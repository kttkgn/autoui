from typing import Optional, List
from datetime import datetime
from app.core.test_engine import TestEngine
from app.core.logger import logger
from app.models.test_case import TestCase
from app.models.test_execution import TestExecution, TestStepResult
from app.crud.test_execution import test_execution
from app.crud.test_case import test_case
from app.core.exceptions import TestExecutionError
from app.core.device_manager import DeviceManager

class TestEngineService:
    """测试执行引擎服务"""
    
    def __init__(self):
        """初始化测试执行引擎服务"""
        self.device_manager = DeviceManager()
        self.current_engine: Optional[TestEngine] = None
        
    async def start_execution(self, test_case_id: int, device_id: int) -> TestExecution:
        """
        开始执行测试用例
        
        Args:
            test_case_id: 测试用例ID
            device_id: 设备ID
            
        Returns:
            TestExecution: 测试执行记录
        """
        try:
            # 获取测试用例
            test_case = await test_case.get(test_case_id)
            if not test_case:
                raise TestExecutionError(f"测试用例不存在: {test_case_id}")
                
            # 获取设备
            device = await self.device_manager.get_device(device_id)
            if not device:
                raise TestExecutionError(f"设备不存在: {device_id}")
                
            # 创建测试执行记录
            execution = await test_execution.create({
                "test_case_id": test_case_id,
                "device_id": device_id,
                "status": "running",
                "start_time": datetime.now()
            })
            
            # 创建测试执行引擎
            self.current_engine = TestEngine(device.driver)
            
            # 执行测试用例
            result = await self.current_engine.execute_test_case(test_case)
            
            # 更新执行记录
            await test_execution.update(execution.id, {
                "status": result.status,
                "end_time": result.end_time,
                "error_message": result.error_message
            })
            
            return result
            
        except Exception as e:
            logger.error(f"测试执行失败: {str(e)}")
            if execution:
                await test_execution.update(execution.id, {
                    "status": "failed",
                    "end_time": datetime.now(),
                    "error_message": str(e)
                })
            raise TestExecutionError(f"测试执行失败: {str(e)}")
            
    async def stop_execution(self, execution_id: int) -> None:
        """
        停止测试执行
        
        Args:
            execution_id: 测试执行ID
        """
        try:
            # 获取执行记录
            execution = await test_execution.get(execution_id)
            if not execution:
                raise TestExecutionError(f"执行记录不存在: {execution_id}")
                
            # 停止执行
            if self.current_engine:
                self.current_engine.cleanup()
                self.current_engine = None
                
            # 更新执行状态
            await test_execution.update(execution_id, {
                "status": "stopped",
                "end_time": datetime.now()
            })
            
        except Exception as e:
            logger.error(f"停止测试执行失败: {str(e)}")
            raise TestExecutionError(f"停止测试执行失败: {str(e)}")
            
    async def get_execution_status(self, execution_id: int) -> str:
        """
        获取执行状态
        
        Args:
            execution_id: 测试执行ID
            
        Returns:
            str: 执行状态
        """
        try:
            execution = await test_execution.get(execution_id)
            if not execution:
                raise TestExecutionError(f"执行记录不存在: {execution_id}")
            return execution.status
        except Exception as e:
            logger.error(f"获取执行状态失败: {str(e)}")
            raise TestExecutionError(f"获取执行状态失败: {str(e)}")
            
    async def get_step_results(self, execution_id: int) -> List[TestStepResult]:
        """
        获取步骤执行结果
        
        Args:
            execution_id: 测试执行ID
            
        Returns:
            List[TestStepResult]: 步骤执行结果列表
        """
        try:
            return await test_execution.get_step_results(execution_id)
        except Exception as e:
            logger.error(f"获取步骤执行结果失败: {str(e)}")
            raise TestExecutionError(f"获取步骤执行结果失败: {str(e)}")
            
    async def retry_step(self, execution_id: int, step_id: int) -> TestStepResult:
        """
        重试步骤
        
        Args:
            execution_id: 测试执行ID
            step_id: 步骤ID
            
        Returns:
            TestStepResult: 步骤执行结果
        """
        try:
            # 获取执行记录
            execution = await test_execution.get(execution_id)
            if not execution:
                raise TestExecutionError(f"执行记录不存在: {execution_id}")
                
            # 获取测试用例
            test_case = await test_case.get(execution.test_case_id)
            if not test_case:
                raise TestExecutionError(f"测试用例不存在: {execution.test_case_id}")
                
            # 获取步骤
            step = next((s for s in test_case.steps if s.id == step_id), None)
            if not step:
                raise TestExecutionError(f"步骤不存在: {step_id}")
                
            # 重试步骤
            if self.current_engine:
                result = await self.current_engine.execute_step(step)
                return result
            else:
                raise TestExecutionError("测试执行引擎未初始化")
                
        except Exception as e:
            logger.error(f"重试步骤失败: {str(e)}")
            raise TestExecutionError(f"重试步骤失败: {str(e)}")
            
    async def cleanup(self) -> None:
        """清理资源"""
        if self.current_engine:
            self.current_engine.cleanup()
            self.current_engine = None 