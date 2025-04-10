from typing import Tuple, Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.reservation import Reservation
from app.repositories.reservation import ReservationRepository
from app.repositories.table import TableRepository
from app.schemas.reservation import ReservationCreate


class ReservationService:
    """
    Сервис для работы с бронированиями
    """

    def __init__(self) -> None:
        self.repository = ReservationRepository()
        self.table_repository = TableRepository()

    async def get_all_reservations(self, db: AsyncSession):
        """
        Получить все брони
        """
        return await self.repository.get_all(db)
    async def create_reservation(
            self, db: AsyncSession, reservation_data: ReservationCreate
    ) -> Union[Reservation, Tuple[bool, str]]:
        """
        Создать новую бронь с проверкой на пересечения

        Args:
            db: Сессия базы данных
            reservation_data: Данные для создания брони

        Returns:
            Объект созданной брони или кортеж (False, сообщение об ошибке)
        """
        table = await self.table_repository.get(db, reservation_data.table_id)
        if not table:
            return False, f"Столик с ID {reservation_data.table_id} не найден"

        # Проверяем, свободен ли столик в указанное время
        overlapping = await self.repository.find_overlapping_reservations(
            db,
            reservation_data.table_id,
            reservation_data.reservation_time,
            reservation_data.duration_minutes
        )

        if overlapping:
            return False, "Столик уже забронирован на это время"

        reservation_dict = reservation_data.model_dump()
        return await self.repository.create(db, reservation_dict)

    async def delete_reservation(self, db: AsyncSession, reservation_id: int) -> bool:
        """
        Удалить бронь по ID
        """
        return await self.repository.delete(db, reservation_id)