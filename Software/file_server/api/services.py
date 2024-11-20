from fastapi import HTTPException, Depends
from sqlmodel import Session, select
from typing import List, Optional

from db.models import Item
from db.db_utils import get_session

class ItemService:
    def __init__(self, session: Session):
        self.session = session

    async def read_all_items(self) -> List[Item]:
        statement = select(Item)
        results = self.session.exec(statement).all()
        return results

    async def read_all_items_in_cubby(self) -> List[Item]:
        statement = select(Item).where(Item.in_cubby.isnot(None))
        results = self.session.exec(statement).all()
        return results

    async def read_all_items_not_in_cubby(self) -> List[Item]:
        statement = select(Item).where(Item.in_cubby == False)
        results = self.session.exec(statement).all()
        return results

    async def create_item(self, name: str, cubby_number: Optional[int] = None) -> Item:
        item = Item(name=name, in_cubby=cubby_number)
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    async def delete_item(self, item_id: int) -> None:
        item = self.session.get(Item, item_id)
        if not item:
            return False
        self.session.delete(item)
        self.session.commit()
    
    async def delete_item_by_name(self, name: str) -> None:
        statement = select(Item).where(Item.name == name)
        item = self.session.exec(statement).first()
        if not item:
            return False
        self.session.delete(item)
        self.session.commit()

    async def update_item_status(self, item_id: int, in_cubby: bool) -> Item:
        item = self.session.get(Item, item_id)
        if not item:
            return
        item.in_cubby = in_cubby
        self.session.add(item)
        self.session.commit()
        return item

# Dependency for ItemService
def get_item_service(session: Session = Depends(get_session)) -> ItemService:
    return ItemService(session=session)