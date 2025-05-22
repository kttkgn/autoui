from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from app.schemas.project import TestCaseStatus

class TestCase(Base):
    """测试用例模型"""
    __tablename__ = "testcases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    status = Column(Enum(TestCaseStatus), default=TestCaseStatus.DRAFT)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    project = relationship("Project", back_populates="testcases")
    steps = relationship("TestStep", back_populates="testcase", cascade="all, delete-orphan")
    executions = relationship("TestExecution", back_populates="testcase", cascade="all, delete-orphan") 