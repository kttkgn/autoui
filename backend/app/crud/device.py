from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from app.crud.base import CRUDBase
from app.models.device import Device, DeviceProperty
from app.schemas.device import DeviceCreate, DeviceUpdate, DevicePropertyCreate, DevicePropertyUpdate

class CRUDDevice(CRUDBase[Device, DeviceCreate, DeviceUpdate]):
    """设备CRUD操作类"""
    
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Device]:
        """根据名称获取设备"""
        result = await db.execute(
            select(Device)
            .where(Device.name == name)
            .options(selectinload(Device.properties))
        )
        return result.scalar_one_or_none()

    async def get_multi_by_type(
        self, db: AsyncSession, *, type: str, skip: int = 0, limit: int = 100
    ) -> List[Device]:
        """根据类型获取设备列表"""
        result = await db.execute(
            select(Device)
            .where(Device.type == type)
            .offset(skip)
            .limit(limit)
            .options(selectinload(Device.properties))
        )
        return result.scalars().all()

    async def get_available_devices(
        self, db: AsyncSession, *, type: str, skip: int = 0, limit: int = 100
    ) -> List[Device]:
        """获取可用设备列表"""
        result = await db.execute(
            select(Device)
            .where(Device.type == type, Device.status == "online")
            .offset(skip)
            .limit(limit)
            .options(selectinload(Device.properties))
        )
        return result.scalars().all()

    async def update_status(
        self, db: AsyncSession, *, device_id: int, status: str
    ) -> Optional[Device]:
        """更新设备状态"""
        await db.execute(
            update(Device)
            .where(Device.id == device_id)
            .values(status=status)
        )
        await db.commit()
        return await self.get(db, id=device_id)

    async def add_property(
        self, db: AsyncSession, *, device_id: int, property_data: DevicePropertyCreate
    ) -> DeviceProperty:
        """添加设备属性"""
        db_property = DeviceProperty(
            device_id=device_id,
            key=property_data.key,
            value=property_data.value
        )
        db.add(db_property)
        await db.commit()
        await db.refresh(db_property)
        return db_property

    async def update_property(
        self, db: AsyncSession, *, property_id: int, property_data: DevicePropertyUpdate
    ) -> Optional[DeviceProperty]:
        """更新设备属性"""
        await db.execute(
            update(DeviceProperty)
            .where(DeviceProperty.id == property_id)
            .values(**property_data.dict(exclude_unset=True))
        )
        await db.commit()
        return await db.get(DeviceProperty, property_id)

    async def delete_property(
        self, db: AsyncSession, *, property_id: int
    ) -> Optional[DeviceProperty]:
        """删除设备属性"""
        property = await db.get(DeviceProperty, property_id)
        if property:
            await db.delete(property)
            await db.commit()
        return property

device = CRUDDevice(Device) 