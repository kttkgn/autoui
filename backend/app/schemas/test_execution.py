from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from app.core.enums.project import TestExecutionStatus, TestStepStatus

# 测试步骤结果
class TestStepResultBase(BaseModel):
    """测试步骤结果基类"""
    step_number: int = Field(..., description="步骤编号")
    step_name: str = Field(..., description="步骤名称")
    status: TestStepStatus = Field(..., description="执行状态")
    start_time: datetime = Field(..., description="开始时间")
    end_time: Optional[datetime] = Field(None, description="结束时间")
    error_message: Optional[str] = Field(None, description="错误信息")
    screenshot_path: Optional[str] = Field(None, description="截图路径")
    logs: Optional[List[str]] = Field(None, description="日志列表")

class TestStepResultCreate(TestStepResultBase):
    """创建测试步骤结果"""
    pass

class TestStepResultUpdate(TestStepResultBase):
    pass

class TestStepResult(TestStepResultBase):
    """测试步骤结果"""
    id: int = Field(..., description="步骤结果ID")
    execution_id: int = Field(..., description="执行记录ID")
    
    class Config:
        from_attributes = True

# 测试执行记录
class TestExecutionBase(BaseModel):
    """测试执行基类"""
    test_case_id: int = Field(..., description="测试用例ID")
    device_id: str = Field(..., description="设备ID")
    status: TestExecutionStatus = Field(..., description="执行状态")
    start_time: datetime = Field(..., description="开始时间")
    end_time: Optional[datetime] = Field(None, description="结束时间")
    error_message: Optional[str] = Field(None, description="错误信息")
    environment: str = Field(..., description="执行环境")
    variables: Optional[Dict[str, Any]] = Field(None, description="变量数据")

class TestExecutionCreate(TestExecutionBase):
    """创建测试执行记录"""
    pass

class TestExecutionUpdate(TestExecutionBase):
    pass

class TestExecution(TestExecutionBase):
    """测试执行记录"""
    id: int = Field(..., description="执行记录ID")
    step_results: List[TestStepResult] = Field(..., description="步骤执行结果")
    
    class Config:
        from_attributes = True 