from typing import Dict, Optional
import asyncio
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from app.core.config import settings

class DeviceManager:
    _devices: Dict[str, webdriver.Remote] = {}
    _lock = asyncio.Lock()

    @classmethod
    async def get_device(cls, device_name: str) -> Optional[webdriver.Remote]:
        """获取设备实例"""
        async with cls._lock:
            if device_name in cls._devices:
                return cls._devices[device_name]

            try:
                # 从配置中获取设备信息
                device_config = settings.DEVICES.get(device_name)
                if not device_config:
                    raise Exception(f"设备 {device_name} 未配置")

                # 创建新的设备实例
                driver = webdriver.Remote(
                    command_executor=settings.APPIUM_SERVER,
                    desired_capabilities=device_config
                )
                cls._devices[device_name] = driver
                return driver
            except Exception as e:
                raise Exception(f"初始化设备失败: {str(e)}")

    @classmethod
    async def release_device(cls, device: webdriver.Remote):
        """释放设备"""
        async with cls._lock:
            for name, dev in cls._devices.items():
                if dev == device:
                    try:
                        await dev.quit()
                    except:
                        pass
                    del cls._devices[name]
                    break

    @classmethod
    async def release_all_devices(cls):
        """释放所有设备"""
        async with cls._lock:
            for device in cls._devices.values():
                try:
                    await device.quit()
                except:
                    pass
            cls._devices.clear() 