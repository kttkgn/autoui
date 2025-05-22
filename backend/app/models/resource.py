from sqlalchemy import Column, String, JSON, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base
from app.core.resource import ResourceType, ResourceStatus

class Resource(Base):
    """资源模型"""
    __tablename__ = "resources"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    type = Column(Enum(ResourceType), nullable=False)
    status = Column(Enum(ResourceStatus), default=ResourceStatus.AVAILABLE, nullable=False)
    config = Column(JSON, nullable=False)  # 资源配置信息
    description = Column(String(200))
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联关系
    project = relationship("Project", back_populates="resources")
    resource_usage = relationship("ResourceUsage", back_populates="resource")

    def __repr__(self):
        return f"<Resource {self.name}>"

class ResourceUsage(Base):
    """资源使用记录模型"""
    __tablename__ = "resource_usage"

    id = Column(String(36), primary_key=True, index=True)
    resource_id = Column(String(36), ForeignKey("resources.id"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    test_execution_id = Column(String(36), ForeignKey("test_executions.id"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    status = Column(String(50), nullable=False)  # 使用状态: allocated, released, error
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联关系
    resource = relationship("Resource", back_populates="resource_usage")
    user = relationship("User", back_populates="resource_usage")
    test_execution = relationship("TestExecution", back_populates="resource_usage")

    def __repr__(self):
        return f"<ResourceUsage {self.resource_id}:{self.user_id}>" 