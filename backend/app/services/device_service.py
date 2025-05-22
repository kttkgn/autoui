import asyncio
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from app.crud.device import device
from app.models.device import Device, DeviceType, DeviceStatus
from app.schemas.device import DeviceCreate, DevicePropertyCreate, DeviceUpdate, DeviceResponse
from app.core.logger import logger
from app.core.enums.device import DeviceType, DeviceStatus


logger = logging.getLogger(__name__)

class DeviceService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self._device_monitors = {}  # 设备监控任务字典

    async def get_devices(
        self,
        skip: int = 0,
        limit: int = 100,
        type: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Device]:
        """获取设备列表
        
        Args:
            skip: 跳过的记录数
            limit: 返回的最大记录数
            type: 设备类型过滤
            status: 设备状态过滤
            
        Returns:
            List[Device]: 设备列表
        """
        query = select(Device).options(selectinload(Device.properties))
        
        if type:
            query = query.where(Device.type == type)
        if status:
            query = query.where(Device.status == status)
            
        query = query.offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        return result.scalars().all()

    async def detect_devices(self) -> List[Device]:
        """检测所有可用设备"""
        detected_devices = []
        
        # 检测Android设备
        android_devices = await self._detect_android_devices()
        detected_devices.extend(android_devices)
        
        # 检测iOS设备
        ios_devices = await self._detect_ios_devices()
        detected_devices.extend(ios_devices)
        
        # 检测Web浏览器
        web_browsers = await self._detect_web_browsers()
        detected_devices.extend(web_browsers)
        
        return detected_devices

    async def _detect_android_devices(self) -> List[Device]:
        """检测Android设备"""
        try:
            # 使用adb命令检测设备
            proc = await asyncio.create_subprocess_shell(
                "adb devices",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            
            if stderr:
                logger.error(f"Android设备检测错误: {stderr.decode()}")
                return []
            
            devices = []
            for line in stdout.decode().splitlines()[1:]:  # 跳过第一行
                if line.strip():
                    serial = line.split()[0]
                    if serial != "List":
                        # 获取设备详细信息
                        device_info = await self._get_android_device_info(serial)
                        if device_info:
                            # 创建设备
                            device_create = DeviceCreate(
                                name=device_info["model"],
                                type=DeviceType.ANDROID,
                                status=DeviceStatus.ONLINE,
                                config={
                                    "serial": serial,
                                    "model": device_info["model"],
                                    "version": device_info["version"],
                                    "resolution": device_info["resolution"]
                                }
                            )
                            devices.append(device_create)
            
            return devices
        except Exception as e:
            logger.error(f"Android设备检测异常: {str(e)}")
            return []

    async def _get_android_device_info(self, serial: str) -> Optional[Dict]:
        """获取Android设备详细信息"""
        try:
            # 获取设备型号
            model_proc = await asyncio.create_subprocess_shell(
                f"adb -s {serial} shell getprop ro.product.model",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            model_stdout, _ = await model_proc.communicate()
            model = model_stdout.decode().strip()
            
            # 获取Android版本
            version_proc = await asyncio.create_subprocess_shell(
                f"adb -s {serial} shell getprop ro.build.version.release",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            version_stdout, _ = await version_proc.communicate()
            version = version_stdout.decode().strip()
            
            # 获取屏幕分辨率
            resolution_proc = await asyncio.create_subprocess_shell(
                f"adb -s {serial} shell wm size",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            resolution_stdout, _ = await resolution_proc.communicate()
            resolution = resolution_stdout.decode().strip()
            
            return {
                "model": model,
                "version": version,
                "resolution": resolution
            }
        except Exception as e:
            logger.error(f"获取Android设备信息异常: {str(e)}")
            return None

    async def _detect_ios_devices(self) -> List[Device]:
        """检测iOS设备"""
        try:
            # 使用libimobiledevice检测设备
            proc = await asyncio.create_subprocess_shell(
                "idevice_id -l",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            
            if stderr:
                logger.error(f"iOS设备检测错误: {stderr.decode()}")
                return []
            
            devices = []
            for udid in stdout.decode().splitlines():
                if udid.strip():
                    # 获取设备详细信息
                    device_info = await self._get_ios_device_info(udid)
                    if device_info:
                        # 创建设备
                        device_create = DeviceCreate(
                            name=device_info["name"],
                            type=DeviceType.IOS,
                            status=DeviceStatus.ONLINE,
                            config={
                                "udid": udid,
                                "name": device_info["name"],
                                "version": device_info["version"],
                                "resolution": device_info["resolution"]
                            }
                        )
                        devices.append(device_create)
            
            return devices
        except Exception as e:
            logger.error(f"iOS设备检测异常: {str(e)}")
            return []

    async def _get_ios_device_info(self, udid: str) -> Optional[Dict]:
        """获取iOS设备详细信息"""
        try:
            # 获取设备名称
            name_proc = await asyncio.create_subprocess_shell(
                f"ideviceinfo -u {udid} -s DeviceName",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            name_stdout, _ = await name_proc.communicate()
            name = name_stdout.decode().strip()
            
            # 获取iOS版本
            version_proc = await asyncio.create_subprocess_shell(
                f"ideviceinfo -u {udid} -s ProductVersion",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            version_stdout, _ = await version_proc.communicate()
            version = version_stdout.decode().strip()
            
            # 获取屏幕分辨率
            resolution_proc = await asyncio.create_subprocess_shell(
                f"ideviceinfo -u {udid} -s ScreenResolution",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            resolution_stdout, _ = await resolution_proc.communicate()
            resolution = resolution_stdout.decode().strip()
            
            return {
                "name": name,
                "version": version,
                "resolution": resolution
            }
        except Exception as e:
            logger.error(f"获取iOS设备信息异常: {str(e)}")
            return None

    async def _detect_web_browsers(self) -> List[Device]:
        """检测Web浏览器"""
        browsers = [
            {
                "name": "Chrome",
                "type": DeviceType.WEB,
                "status": DeviceStatus.ONLINE,
                "config": {
                    "browser": "Chrome",
                    "version": "latest"
                }
            },
            {
                "name": "Firefox",
                "type": DeviceType.WEB,
                "status": DeviceStatus.ONLINE,
                "config": {
                    "browser": "Firefox",
                    "version": "latest"
                }
            }
        ]
        return [DeviceCreate(**browser) for browser in browsers]

    async def start_device_monitor(self, device_id: int):
        """启动设备监控"""
        if device_id in self._device_monitors:
            return
        
        device_obj = await device.get(self.db, id=device_id)
        if not device_obj:
            raise ValueError("设备不存在")
        
        monitor_task = asyncio.create_task(self._monitor_device(device_id))
        self._device_monitors[device_id] = monitor_task

    async def stop_device_monitor(self, device_id: int):
        """停止设备监控"""
        if device_id in self._device_monitors:
            self._device_monitors[device_id].cancel()
            del self._device_monitors[device_id]

    async def _monitor_device(self, device_id: int):
        """监控设备状态"""
        try:
            while True:
                device_obj = await device.get(self.db, id=device_id)
                if not device_obj:
                    break
                
                # 检查设备状态
                is_online = await self._check_device_status(device_obj)
                if not is_online and device_obj.status != DeviceStatus.OFFLINE:
                    await device.update_status(
                        self.db,
                        device_id=device_id,
                        status=DeviceStatus.OFFLINE
                    )
                elif is_online and device_obj.status == DeviceStatus.OFFLINE:
                    await device.update_status(
                        self.db,
                        device_id=device_id,
                        status=DeviceStatus.ONLINE
                    )
                
                await asyncio.sleep(30)  # 每30秒检查一次
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"设备监控异常: {str(e)}")

    async def _check_device_status(self, device_obj: Device) -> bool:
        """检查设备状态"""
        try:
            if device_obj.type == DeviceType.ANDROID:
                # 检查Android设备
                serial = next(
                    (p.value for p in device_obj.properties if p.key == "serial"),
                    None
                )
                if serial:
                    proc = await asyncio.create_subprocess_shell(
                        f"adb -s {serial} get-state",
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE
                    )
                    stdout, _ = await proc.communicate()
                    return stdout.decode().strip() == "device"
            
            elif device_obj.type == DeviceType.IOS:
                # 检查iOS设备
                udid = next(
                    (p.value for p in device_obj.properties if p.key == "udid"),
                    None
                )
                if udid:
                    proc = await asyncio.create_subprocess_shell(
                        f"ideviceinfo -u {udid} -s DeviceName",
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE
                    )
                    stdout, _ = await proc.communicate()
                    return bool(stdout.decode().strip())
            
            elif device_obj.type == DeviceType.WEB:
                # Web浏览器始终在线
                return True
            
            return False
        except Exception as e:
            logger.error(f"检查设备状态异常: {str(e)}")
            return False

    async def add_device(
        self,
        id: str,
        type: DeviceType,
        config: Dict[str, Any],
        description: Optional[str] = None
    ) -> Device:
        """添加设备
        
        Args:
            id: 设备ID
            type: 设备类型
            config: 设备配置
            description: 设备描述
            
        Returns:
            Device: 添加的设备对象
        """
        # 检查设备是否已存在
        existing_device = await device.get(self.db, id=id)
        if existing_device:
            raise ValueError(f"设备已存在: {id}")
        
        # 创建设备
        device_in = DeviceCreate(
            id=id,
            name=config.get("name", f"Device-{id}"),
            type=type,
            status=DeviceStatus.OFFLINE,
            config=config,
            description=description
        )
        
        return await device.create(self.db, obj_in=device_in)

    async def remove_device(self, device_id: str) -> None:
        """移除设备
        
        Args:
            device_id: 设备ID
            
        Raises:
            ValueError: 设备不存在
        """
        # 检查设备是否存在
        device_obj = await device.get(self.db, id=device_id)
        if not device_obj:
            raise ValueError(f"设备不存在: {device_id}")
        
        # 停止设备监控
        if device_id in self._device_monitors:
            await self.stop_device_monitor(device_id)
        
        # 删除设备
        await device.remove(self.db, id=device_id)

    async def get_device(self, device_id: str) -> Optional[DeviceResponse]:
        """
        获取设备信息
        
        Args:
            device_id: 设备ID
            
        Returns:
            Optional[DeviceResponse]: 设备信息
        """
        try:
            stmt = select(Device).where(Device.device_id == device_id)
            result = await self.db.execute(stmt)
            device = result.scalar_one_or_none()
            
            if not device:
                logger.warning(f"设备不存在: {device_id}")
                return None
            
            return DeviceResponse.model_validate(device)
            
        except Exception as e:
            logger.error(f"获取设备信息失败: {str(e)}")
            raise

    async def get_all_devices(
        self,
        device_type: Optional[DeviceType] = None,
        status: Optional[DeviceStatus] = None
    ) -> List[DeviceResponse]:
        """
        获取所有设备
        
        Args:
            device_type: 设备类型
            status: 设备状态
            
        Returns:
            List[DeviceResponse]: 设备列表
        """
        try:
            stmt = select(Device)
            
            if device_type:
                stmt = stmt.where(Device.type == device_type)
            if status:
                stmt = stmt.where(Device.status == status)
                
            result = await self.db.execute(stmt)
            devices = result.scalars().all()
            
            return [DeviceResponse.model_validate(device) for device in devices]
            
        except Exception as e:
            logger.error(f"获取设备列表失败: {str(e)}")
            raise

    async def update_device(
        self,
        device_id: str,
        device_data: DeviceUpdate
    ) -> Optional[DeviceResponse]:
        """
        更新设备信息
        
        Args:
            device_id: 设备ID
            device_data: 设备数据
            
        Returns:
            Optional[DeviceResponse]: 更新后的设备信息
        """
        try:
            # 检查设备是否存在
            stmt = select(Device).where(Device.device_id == device_id)
            result = await self.db.execute(stmt)
            device = result.scalar_one_or_none()
            
            if not device:
                logger.warning(f"设备不存在: {device_id}")
                return None
            
            # 更新设备信息
            update_data = device_data.model_dump(exclude_unset=True)
            stmt = (
                update(Device)
                .where(Device.device_id == device_id)
                .values(**update_data)
            )
            await self.db.execute(stmt)
            await self.db.commit()
            
            # 刷新设备信息
            await self.db.refresh(device)
            
            logger.info(f"设备信息更新成功: {device_id}")
            return DeviceResponse.model_validate(device)
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"更新设备信息失败: {str(e)}")
            raise

    async def get_device_status(self, device_id: str) -> Optional[DeviceStatus]:
        """
        获取设备状态
        
        Args:
            device_id: 设备ID
            
        Returns:
            Optional[DeviceStatus]: 设备状态
        """
        try:
            stmt = select(Device).where(Device.device_id == device_id)
            result = await self.db.execute(stmt)
            device = result.scalar_one_or_none()
            
            if not device:
                logger.warning(f"设备不存在: {device_id}")
                return None
            
            return device.status
            
        except Exception as e:
            logger.error(f"获取设备状态失败: {str(e)}")
            raise

    async def update_device_status(
        self,
        device_id: str,
        status: DeviceStatus
    ) -> Optional[DeviceResponse]:
        """
        更新设备状态
        
        Args:
            device_id: 设备ID
            status: 新状态
            
        Returns:
            Optional[DeviceResponse]: 更新后的设备信息
        """
        try:
            # 检查设备是否存在
            stmt = select(Device).where(Device.device_id == device_id)
            result = await self.db.execute(stmt)
            device = result.scalar_one_or_none()
            
            if not device:
                logger.warning(f"设备不存在: {device_id}")
                return None
            
            # 更新状态
            stmt = (
                update(Device)
                .where(Device.device_id == device_id)
                .values(status=status)
            )
            await self.db.execute(stmt)
            await self.db.commit()
            
            # 刷新设备信息
            await self.db.refresh(device)
            
            logger.info(f"设备状态更新成功: {device_id} -> {status}")
            return DeviceResponse.model_validate(device)
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"更新设备状态失败: {str(e)}")
            raise

    async def get_device_config(
        self,
        device_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        获取设备配置
        
        Args:
            device_id: 设备ID
            
        Returns:
            Optional[Dict[str, Any]]: 设备配置
        """
        try:
            stmt = select(Device).where(Device.device_id == device_id)
            result = await self.db.execute(stmt)
            device = result.scalar_one_or_none()
            
            if not device:
                logger.warning(f"设备不存在: {device_id}")
                return None
            
            return device.config
            
        except Exception as e:
            logger.error(f"获取设备配置失败: {str(e)}")
            raise

    async def update_device_config(
        self,
        device_id: str,
        config: Dict[str, Any]
    ) -> Optional[DeviceResponse]:
        """
        更新设备配置
        
        Args:
            device_id: 设备ID
            config: 新配置
            
        Returns:
            Optional[DeviceResponse]: 更新后的设备信息
        """
        try:
            # 检查设备是否存在
            stmt = select(Device).where(Device.device_id == device_id)
            result = await self.db.execute(stmt)
            device = result.scalar_one_or_none()
            
            if not device:
                logger.warning(f"设备不存在: {device_id}")
                return None
            
            # 更新配置
            stmt = (
                update(Device)
                .where(Device.device_id == device_id)
                .values(config=config)
            )
            await self.db.execute(stmt)
            await self.db.commit()
            
            # 刷新设备信息
            await self.db.refresh(device)
            
            logger.info(f"设备配置更新成功: {device_id}")
            return DeviceResponse.model_validate(device)
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"更新设备配置失败: {str(e)}")
            raise

    async def get_devices_by_type(
        self,
        device_type: DeviceType
    ) -> List[DeviceResponse]:
        """
        获取指定类型的设备
        
        Args:
            device_type: 设备类型
            
        Returns:
            List[DeviceResponse]: 设备列表
        """
        try:
            stmt = select(Device).where(Device.type == device_type)
            result = await self.db.execute(stmt)
            devices = result.scalars().all()
            
            return [DeviceResponse.model_validate(device) for device in devices]
            
        except Exception as e:
            logger.error(f"获取设备列表失败: {str(e)}")
            raise

    async def get_devices_by_status(
        self,
        status: DeviceStatus
    ) -> List[DeviceResponse]:
        """
        获取指定状态的设备
        
        Args:
            status: 设备状态
            
        Returns:
            List[DeviceResponse]: 设备列表
        """
        try:
            stmt = select(Device).where(Device.status == status)
            result = await self.db.execute(stmt)
            devices = result.scalars().all()
            
            return [DeviceResponse.model_validate(device) for device in devices]
            
        except Exception as e:
            logger.error(f"获取设备列表失败: {str(e)}")
            raise 