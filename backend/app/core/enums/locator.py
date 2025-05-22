from enum import Enum

class LocatorType(str, Enum):
    """元素定位方式"""
    ID = "id"  # ID定位
    NAME = "name"  # 名称定位
    CLASS_NAME = "class_name"  # 类名定位
    TAG_NAME = "tag_name"  # 标签名定位
    LINK_TEXT = "link_text"  # 链接文本定位
    PARTIAL_LINK_TEXT = "partial_link_text"  # 部分链接文本定位
    XPATH = "xpath"  # XPath定位
    CSS_SELECTOR = "css_selector"  # CSS选择器定位
    ACCESSIBILITY_ID = "accessibility_id"  # 无障碍ID定位
    ANDROID_UIAUTOMATOR = "android_uiautomator"  # Android UIAutomator定位
    IOS_PREDICATE = "ios_predicate"  # iOS Predicate定位
    IOS_CLASS_CHAIN = "ios_class_chain"  # iOS Class Chain定位 