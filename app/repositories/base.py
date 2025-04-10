from typing import Generic, TypeVar, Type, List, Optional, Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """
    Базовый репозиторий с общими CRUD методами
    """
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """
        Получить объект по ID асинхронно
        """
        query = select(self.model).where(self.model.id == id)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_all(self, db: AsyncSession) -> List[ModelType]:
        """
        Получить все объекты асинхронно
        """
        query = select(self.model)
        result = await db.execute(query)
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: Dict[str, Any]) -> ModelType:
        """
        Создать новый объект асинхронно
        """
        obj_db = self.model(**obj_in)
        db.add(obj_db)
        await db.commit()
        await db.refresh(obj_db)
        return obj_db

    async def delete(self, db: AsyncSession, id: Any) -> bool:
        """
        Удалить объект по ID
        """
        obj = await self.get(db, id)
        if obj:
            await db.delete(obj)
            await db.commit()
            return True
        return False