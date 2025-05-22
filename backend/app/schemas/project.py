from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from enum import Enum

from app.core.enums.project import TestExecutionStatus, TestStepStatus, TestEnvironment


# 基础项目Schema
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

# 创建项目Schema
class ProjectCreate(ProjectBase):
    pass

# 更新项目Schema
class ProjectUpdate(ProjectBase):
    name: Optional[str] = None

# 项目响应Schema
class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# 测试套件Schema
class TestSuiteBase(BaseModel):
    name: str
    description: Optional[str] = None

class TestSuiteCreate(TestSuiteBase):
    project_id: int

class TestSuiteUpdate(TestSuiteBase):
    name: Optional[str] = None

class TestSuiteResponse(TestSuiteBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# 测试步骤Schema
class TestStep(BaseModel):
    step_number: int
    action: str
    element: str
    value: Optional[str] = None

# 数据驱动配置Schema
class DataDrivenConfig(BaseModel):
    enabled: bool = False
    data_source: Optional[str] = None
    parameters: List[str] = []

# 测试用例Schema
class TestCaseBase(BaseModel):
    name: str
    description: Optional[str] = None
    steps: List[TestStep] = []
    data_driven: DataDrivenConfig = DataDrivenConfig()

class TestCaseCreate(TestCaseBase):
    suite_id: int

class TestCaseUpdate(TestCaseBase):
    name: Optional[str] = None

class TestCaseResponse(TestCaseBase):
    id: int
    suite_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# 测试步骤结果Schema
class TestStepResultBase(BaseModel):
    step_number: int
    action: str
    element: str
    value: Optional[str] = None
    status: TestStepStatus
    message: Optional[str] = None
    screenshot: Optional[str] = None

class TestStepResultCreate(TestStepResultBase):
    execution_id: int

class TestStepResultUpdate(TestStepResultBase):
    pass

class TestStepResultResponse(TestStepResultBase):
    id: int
    execution_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# 测试执行Schema
class TestExecutionBase(BaseModel):
    """测试执行基础模型"""
    test_case_id: int
    device_id: str
    environment: TestEnvironment = TestEnvironment.TEST
    status: TestExecutionStatus = TestExecutionStatus.PENDING
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    error_message: Optional[str] = None

class TestExecutionCreate(TestExecutionBase):
    pass

class TestExecutionUpdate(BaseModel):
    status: Optional[TestExecutionStatus] = None
    error_message: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: Optional[int] = None

class TestExecutionResponse(TestExecutionBase):
    id: int
    project_id: int
    status: TestExecutionStatus
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: Optional[int] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    step_results: List[TestStepResultResponse] = []

    class Config:
        from_attributes = True

class TestExecutionSummary(BaseModel):
    """测试执行汇总报告响应模型"""
    total: int
    success: int
    failed: int
    running: int
    report_url: str
    executions: List[TestExecutionResponse]

    class Config:
        from_attributes = True

class TestCaseStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived" 