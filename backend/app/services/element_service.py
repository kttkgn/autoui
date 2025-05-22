from sqlalchemy.ext.asyncio import AsyncSession
from app.models.element import Element
from app.schemas.element import ElementCreate, ElementUpdate
from typing import List, Optional

class ElementService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_elements(
        self,
        skip: int = 0,
        limit: int = 100,
        device_id: Optional[int] = None
    ) -> List[Element]:
        """获取元素列表"""
        query = self.db.query(Element)
        if device_id:
            query = query.filter(Element.device_id == device_id)
        return await query.offset(skip).limit(limit).all()

    async def get_element(self, element_id: int) -> Optional[Element]:
        """获取单个元素"""
        return await self.db.query(Element).filter(Element.id == element_id).first()

    async def create_element(self, element_in: ElementCreate) -> Element:
        """创建元素"""
        element = Element(**element_in.dict())
        self.db.add(element)
        await self.db.commit()
        await self.db.refresh(element)
        return element

    async def update_element(
        self,
        element_id: int,
        element_in: ElementUpdate
    ) -> Optional[Element]:
        """更新元素"""
        element = await self.get_element(element_id)
        if element:
            for field, value in element_in.dict(exclude_unset=True).items():
                setattr(element, field, value)
            await self.db.commit()
            await self.db.refresh(element)
        return element

    async def delete_element(self, element_id: int) -> Optional[Element]:
        """删除元素"""
        element = await self.get_element(element_id)
        if element:
            await self.db.delete(element)
            await self.db.commit()
        return element 