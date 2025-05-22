import os
from typing import Optional
from datetime import datetime
from appium.webdriver.webdriver import WebDriver
from app.core.config import settings

async def take_screenshot(driver: WebDriver) -> Optional[str]:
    """获取截图并保存
    
    Returns:
        str: 截图文件路径，如果截图失败则返回None
    """
    try:
        # 创建截图目录
        screenshot_dir = os.path.join(settings.MEDIA_ROOT, "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)

        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(screenshot_dir, filename)

        # 获取截图
        driver.get_screenshot_as_file(filepath)

        # 返回相对路径
        return os.path.join("screenshots", filename)
    except Exception as e:
        print(f"截图失败: {str(e)}")
        return None 