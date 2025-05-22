from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, Boolean, JSON, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base
from app.core.enums.project import (
    ProjectStatus,
    TestExecutionStatus,
    TestStepStatus,
    TestCaseStatus,
    TestSuiteStatus,
    TestPriority,
    TestType,
    TestEnvironment,
    TestPlatform
)
from typing import Any

class Project(Base):
    """项目模型"""
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.ACTIVE, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联
    test_cases = relationship("TestCase", back_populates="project")
    test_suites = relationship("TestSuite", back_populates="project")
    test_executions = relationship("TestExecution", back_populates="project")

class TestCase(Base):
    def __init__(self, **kw: Any):
        super().__init__(kw)
        self.device_id = None

    """测试用例模型"""
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(Enum(TestCaseStatus), default=TestCaseStatus.DRAFT, nullable=False)
    priority = Column(Enum(TestPriority), default=TestPriority.P2, nullable=False)
    type = Column(Enum(TestType), default=TestType.FUNCTIONAL, nullable=False)
    platform = Column(Enum(TestPlatform), default=TestPlatform.WEB, nullable=False)
    steps = Column(JSON, nullable=False)  # 测试步骤
    data_driven = Column(Boolean, default=False)  # 是否数据驱动
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联
    project = relationship("Project", back_populates="test_cases")
    test_suites = relationship("TestSuite", secondary="test_suite_cases", back_populates="test_cases")
    executions = relationship("TestExecution", back_populates="test_case")

class TestSuite(Base):
    """测试套件模型"""
    __tablename__ = "test_suites"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(Enum(TestSuiteStatus), default=TestSuiteStatus.ACTIVE, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联
    project = relationship("Project", back_populates="test_suites")
    test_cases = relationship("TestCase", secondary="test_suite_cases", back_populates="test_suites")
    executions = relationship("TestExecution", back_populates="test_suite")

class TestExecution(Base):
    """测试执行模型"""
    __tablename__ = "test_executions"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    test_case_id = Column(Integer, ForeignKey("test_cases.id"), nullable=False)
    test_suite_id = Column(Integer, ForeignKey("test_suites.id"))
    device_id = Column(String(100), nullable=False)
    environment = Column(Enum(TestEnvironment), default=TestEnvironment.TEST, nullable=False)
    status = Column(Enum(TestExecutionStatus), default=TestExecutionStatus.PENDING, nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    duration = Column(Integer)  # 执行时长（秒）
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联
    project = relationship("Project", back_populates="test_executions")
    test_case = relationship("TestCase", back_populates="executions")
    test_suite = relationship("TestSuite", back_populates="executions")
    step_results = relationship("TestStepResult", back_populates="execution")

class TestStepResult(Base):
    """测试步骤结果模型"""
    __tablename__ = "test_step_results"

    id = Column(Integer, primary_key=True, index=True)
    execution_id = Column(Integer, ForeignKey("test_executions.id"), nullable=False)
    step_number = Column(Integer, nullable=False)
    action = Column(String(50), nullable=False)
    element = Column(String(200), nullable=False)
    value = Column(String(500))
    status = Column(Enum(TestStepStatus), default=TestStepStatus.PENDING, nullable=False)
    message = Column(Text)
    screenshot = Column(String(500))  # 截图路径
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关联
    execution = relationship("TestExecution", back_populates="step_results")

# 测试套件和测试用例的多对多关系表
test_suite_cases = Table(
    "test_suite_cases",
    Base.metadata,
    Column("test_suite_id", Integer, ForeignKey("test_suites.id"), primary_key=True),
    Column("test_case_id", Integer, ForeignKey("test_cases.id"), primary_key=True)
) 