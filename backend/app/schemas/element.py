from typing import Optional, Dict, Any, List, Union
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class LocatorStrategy(str, Enum):
    """元素定位策略"""
    ID = "id"
    NAME = "name"
    CLASS_NAME = "class_name"
    TAG_NAME = "tag_name"
    LINK_TEXT = "link_text"
    PARTIAL_LINK_TEXT = "partial_link_text"
    CSS_SELECTOR = "css_selector"
    XPATH = "xpath"
    ACCESSIBILITY_ID = "accessibility_id"
    ANDROID_UIAUTOMATOR = "android_uiautomator"
    IOS_PREDICATE = "ios_predicate"
    IOS_CLASS_CHAIN = "ios_class_chain"

class ElementAction(str, Enum):
    """元素操作类型"""
    CLICK = "click"
    DOUBLE_CLICK = "double_click"
    LONG_PRESS = "long_press"
    INPUT = "input"
    CLEAR = "clear"
    SUBMIT = "submit"
    SCROLL = "scroll"
    SWIPE = "swipe"
    TAP = "tap"
    DRAG_AND_DROP = "drag_and_drop"
    HOVER = "hover"
    WAIT = "wait"
    ASSERT = "assert"

class ElementLocateRequest(BaseModel):
    """元素定位请求"""
    device_id: str
    strategy: LocatorStrategy
    selector: str
    timeout: Optional[int] = Field(default=10, description="定位超时时间(秒)")
    parent_element: Optional[str] = Field(default=None, description="父元素ID")
    index: Optional[int] = Field(default=0, description="当有多个匹配元素时的索引")

class ElementActionRequest(BaseModel):
    """元素操作请求"""
    element_id: str
    action: ElementAction
    params: Optional[Dict[str, Any]] = Field(default=None, description="操作参数")
    timeout: Optional[int] = Field(default=10, description="操作超时时间(秒)")

class ElementProperty(BaseModel):
    """元素属性"""
    name: str
    value: str

class ElementLocation(BaseModel):
    """元素位置和大小"""
    x: int = Field(description="左上角X坐标")
    y: int = Field(description="左上角Y坐标")
    width: int = Field(description="元素宽度")
    height: int = Field(description="元素高度")
    center_x: int = Field(description="中心点X坐标")
    center_y: int = Field(description="中心点Y坐标")

class ElementState(BaseModel):
    """元素状态"""
    is_enabled: bool = Field(description="是否可用")
    is_selected: bool = Field(description="是否被选中")
    is_displayed: bool = Field(description="是否可见")
    is_clickable: bool = Field(description="是否可点击")
    is_focused: bool = Field(description="是否获得焦点")
    is_editable: bool = Field(description="是否可编辑")
    is_checkable: bool = Field(description="是否可勾选")
    is_checked: bool = Field(description="是否已勾选")

class ElementLocateResponse(BaseModel):
    """元素定位响应"""
    id: str = Field(description="元素唯一标识")
    tag_name: str = Field(description="元素标签名")
    text: Optional[str] = Field(default=None, description="元素文本内容")
    attributes: Dict[str, str] = Field(default_factory=dict, description="元素属性")
    location: ElementLocation = Field(description="元素位置和大小")
    state: ElementState = Field(description="元素状态")
    screenshot: Optional[bytes] = Field(default=None, description="元素截图")
    timestamp: datetime = Field(default_factory=datetime.now, description="定位时间")

class ElementNode(BaseModel):
    """元素树节点"""
    id: str = Field(description="元素唯一标识")
    tag_name: str = Field(description="元素标签名")
    text: Optional[str] = Field(default=None, description="元素文本内容")
    attributes: Dict[str, str] = Field(default_factory=dict, description="元素属性")
    location: ElementLocation = Field(description="元素位置和大小")
    state: ElementState = Field(description="元素状态")
    children: List['ElementNode'] = Field(default_factory=list, description="子元素列表")

class ElementTreeResponse(BaseModel):
    """元素树响应"""
    root: ElementNode = Field(description="根节点")
    timestamp: datetime = Field(default_factory=datetime.now, description="获取时间")
    device_id: str = Field(description="设备ID")
    page_source: Optional[str] = Field(default=None, description="页面源码")

class ElementScreenshotResponse(BaseModel):
    """元素截图响应"""
    image_data: bytes = Field(description="图片数据")
    format: str = Field(default="png", description="图片格式")
    timestamp: datetime = Field(default_factory=datetime.now, description="截图时间")
    element_id: str = Field(description="元素ID")
    location: ElementLocation = Field(description="元素位置和大小")

class ElementBase(BaseModel):
    name: str
    type: str
    locator: str
    locator_type: str
    properties: Optional[Dict[str, Any]] = None
    device_id: int

class ElementCreate(ElementBase):
    pass

class ElementUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    locator: Optional[str] = None
    locator_type: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None
    device_id: Optional[int] = None

class Element(ElementBase):
    id: int

    class Config:
        from_attributes = True

class ElementActionResponse(BaseModel):
    """元素操作响应"""
    success: bool = Field(description="操作是否成功")
    message: Optional[str] = Field(default=None, description="操作结果消息")
    timestamp: datetime = Field(default_factory=datetime.now, description="操作时间")
    element_id: str = Field(description="元素ID")
    action: ElementAction = Field(description="执行的操作")
    screenshot: Optional[bytes] = Field(default=None, description="操作后的截图") 