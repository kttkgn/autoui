from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Element(Base):
    __tablename__ = "elements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    type = Column(String(50))  # 元素类型：button, text, input 等
    locator = Column(String(200))  # 元素定位器
    locator_type = Column(String(50))  # 定位器类型：id, xpath, css 等
    properties = Column(JSON)  # 元素属性
    device_id = Column(Integer, ForeignKey("devices.id"))
    
    # 关系
    device = relationship("Device", back_populates="elements") 