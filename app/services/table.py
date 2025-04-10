from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.table import TableRepository
from app.schemas.table import TableCreate
from app.models.table import Table


class TableService:
    """
    Сервис для работы со столиками
    """

    def __init__(self) -> None:
        self.repository = TableRepository()

    async def get_table(self, db: AsyncSession, table_id: int) -> Optional[Table]:
        """
        Получить столик по ID

        Args:
            db: Сессия базы данных
            table_id: Идентификатор столика

        Returns:
            Объект столика или None, если столик не найден
        """
        return await self.repository.get(db, table_id)

    async def get_all_tables(self, db: AsyncSession) -> List[Table]:
        """
        Получить все столики

        Args:
            db: Сессия базы данных

        Returns:
            Список всех столиков
        """
        return await self.repository.get_all(db)

    async def create_table(self, db: AsyncSession, table_data: TableCreate) -> Table:
        """
        Создать новый столик

        Args:
            db: Сессия базы данных
            table_data: Данные для создания столика

        Returns:
            Созданный объект столика
        """
        table_dict = table_data.model_dump()
        return await self.repository.create(db, table_dict)

    async def delete_table(self, db: AsyncSession, table_id: int) -> bool:
        """
        Удалить столик по ID

        Args:
            db: Сессия базы данных
            table_id: Идентификатор столика

        Returns:
            True, если столик был успешно удален, иначе False
        """
        return await self.repository.delete(db, table_id)