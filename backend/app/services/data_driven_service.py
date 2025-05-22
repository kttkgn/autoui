from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from app.core.data_driven import DataDrivenTest
from app.core.test_engine import TestEngine
from app.core.logger import logger

from app.core.exceptions import (
    DataSourceError,
    DataValidationError,
    DataParameterError,
    TestExecutionError
)
from app.models.project import TestExecution, TestCase
from app.schemas.project import TestStep


class DataDrivenService:
    """数据驱动测试服务"""
    
    def __init__(self, test_engine: TestEngine):
        """
        初始化数据驱动测试服务
        
        Args:
            test_engine: 测试执行引擎
        """
        self.test_engine = test_engine
        self.data_driven: Optional[DataDrivenTest] = None
        
    async def execute_data_driven_test(
        self,
        test_case: TestCase,
        data_source_path: str,
        data_schema: Dict[str, Any]
    ) -> List[TestExecution]:
        """
        执行数据驱动测试
        
        Args:
            test_case: 测试用例
            data_source_path: 数据源文件路径
            data_schema: 数据模式
            
        Returns:
            List[TestExecution]: 测试执行记录列表
        """
        try:
            # 创建数据驱动测试实例
            self.data_driven = DataDrivenTest(data_source_path)
            
            # 加载测试数据
            self.data_driven.load_data()
            
            # 验证测试数据
            self.data_driven.validate_data(data_schema)
            
            # 执行测试
            executions = []
            
            def execute_test(data: Dict[str, Any]) -> None:
                # 参数化测试用例
                parameterized_case = self.parameterize_test_case(test_case, data)
                
                # 执行测试用例
                execution = self.test_engine.execute_test_case(parameterized_case)
                executions.append(execution)
                
            # 遍历测试数据
            self.data_driven.iterate_data(execute_test)
            
            return executions
            
        except Exception as e:
            logger.error(f"执行数据驱动测试失败: {str(e)}")
            raise TestExecutionError(f"执行数据驱动测试失败: {str(e)}")
            
        finally:
            # 清理资源
            if self.data_driven:
                self.data_driven.cleanup_data()
                
    def parameterize_test_case(self, test_case: TestCase, data: Dict[str, Any]) -> TestCase:
        """
        参数化测试用例
        
        Args:
            test_case: 测试用例
            data: 测试数据
            
        Returns:
            TestCase: 参数化后的测试用例
        """
        try:
            # 创建测试用例副本
            parameterized_case = TestCase(
                id=test_case.id,
                name=test_case.name,
                description=test_case.description,
                device_id=test_case.device_id,
                steps=[]
            )
            
            # 参数化测试步骤
            for step in test_case.steps:
                parameterized_step = self.parameterize_test_step(step, data)
                parameterized_case.steps.append(parameterized_step)
                
            return parameterized_case
            
        except Exception as e:
            raise DataParameterError(f"参数化测试用例失败: {str(e)}")
            
    def parameterize_test_step(self, step: TestStep, data: Dict[str, Any]) -> TestStep:
        """
        参数化测试步骤
        
        Args:
            step: 测试步骤
            data: 测试数据
            
        Returns:
            TestStep: 参数化后的测试步骤
        """
        try:
            # 创建测试步骤副本
            parameterized_step = TestStep(
                action=step.action,
                value=self.data_driven.parameterize(step.value) if step.value else None
            )
            
            return parameterized_step
            
        except Exception as e:
            raise DataParameterError(f"参数化测试步骤失败: {str(e)}")
            
    def get_current_data(self) -> Optional[Dict[str, Any]]:
        """
        获取当前测试数据
        
        Returns:
            Optional[Dict[str, Any]]: 当前测试数据
        """
        if self.data_driven:
            return self.data_driven.get_current_data()
        return None
        
    def get_test_data(self) -> List[Dict[str, Any]]:
        """
        获取所有测试数据
        
        Returns:
            List[Dict[str, Any]]: 测试数据列表
        """
        if self.data_driven:
            return self.data_driven.get_test_data()
        return []
        
    def add_test_data(self, data: Dict[str, Any]) -> None:
        """
        添加测试数据
        
        Args:
            data: 测试数据
        """
        if self.data_driven:
            self.data_driven.add_test_data(data)
            
    def remove_test_data(self, index: int) -> None:
        """
        删除测试数据
        
        Args:
            index: 数据索引
        """
        if self.data_driven:
            self.data_driven.remove_test_data(index)
            
    def update_test_data(self, index: int, data: Dict[str, Any]) -> None:
        """
        更新测试数据
        
        Args:
            index: 数据索引
            data: 测试数据
        """
        if self.data_driven:
            self.data_driven.update_test_data(index, data)
            
    def save_data(self) -> None:
        """保存测试数据"""
        if self.data_driven:
            self.data_driven.save_data() 