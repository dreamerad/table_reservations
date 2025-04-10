from typing import List, Optional, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.table import Table
from app.repositories.base import BaseRepository


class TableRepository(BaseRepository[Table]):
    """
    Репозиторий для работы со столиками ресторана
    """

    def __init__(self) -> None:
        super().__init__(Table)

    async def get(self, db: AsyncSession, id: int) -> Optional[Table]:
        """
        Получить столик по ID

        Args:
            db: Сессия базы данных
            id: Идентификатор столика

        Returns:
            Объект столика или None, если столик не найден
        """
        return await super().get(db, id)

    async def get_all(self, db: AsyncSession) -> List[Table]:
        """
        Получить все столики

        Args:
            db: Сессия базы данных

        Returns:
            Список всех столиков
        """
        return await super().get_all(db)

    async def create(self, db: AsyncSession, obj_in: Dict[str, Any]) -> Table:
        """
        Создать новый столик

        Args:
            db: Сессия базы данных
            obj_in: Словарь с данными столика

        Returns:
            Созданный объект столика
        """
        return await super().create(db, obj_in)

    async def delete(self, db: AsyncSession, id: int) -> bool:
        """
        Удалить столик по ID

        Args:
            db: Сессия базы данных
            id: Идентификатор столика

        Returns:
            True, если столик был успешно удален, иначе False
        """
        return await super().delete(db, id)