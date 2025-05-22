from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import Column, Integer, String, Enum, JSON, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from app.core.enums.device import DeviceType, DeviceStatus

class Device(Base):
    """设备模型"""
    __tablename__ = "devices"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    type = Column(Enum(DeviceType), nullable=False)
    status = Column(Enum(DeviceStatus), default=DeviceStatus.OFFLINE, nullable=False)
    config = Column(JSON, nullable=False)  # 设备配置信息
    description = Column(String(200))
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联关系
    project = relationship("Project", back_populates="devices")
    test_executions = relationship("TestExecution", back_populates="device")
    device_properties = relationship("DeviceProperty", back_populates="device")

    def __repr__(self):
        return f"<Device {self.name}>"

class DeviceProperty(Base):
    """设备属性模型"""
    __tablename__ = "device_properties"

    id = Column(String(36), primary_key=True, index=True)
    device_id = Column(String(36), ForeignKey("devices.id"), nullable=False)
    name = Column(String(50), nullable=False)
    value = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联关系
    device = relationship("Device", back_populates="device_properties")

    def __repr__(self):
        return f"<DeviceProperty {self.device_id}:{self.name}>" 