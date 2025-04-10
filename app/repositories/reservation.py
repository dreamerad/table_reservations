# app/repositories/reservation.py
from typing import List, Optional
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.repositories.base import BaseRepository
from app.models.reservation import Reservation


class ReservationRepository(BaseRepository[Reservation]):
    """
    Репозиторий для работы с бронированиями столиков
    """

    def __init__(self) -> None:
        super().__init__(Reservation)

    async def find_overlapping_reservations(
            self,
            db: AsyncSession,
            table_id: int,
            reservation_time: datetime,
            duration_minutes: int,
            exclude_id: Optional[int] = None
    ) -> List[Reservation]:
        """
        Поиск пересекающихся броней для указанного столика и времени
        """
        # Преобразуем время в UTC для корректного сравнения
        if reservation_time.tzinfo is None:
            reservation_time = reservation_time.replace(tzinfo=timezone.utc)
        else:
            reservation_time = reservation_time.astimezone(timezone.utc)

        new_end_time = reservation_time + timedelta(minutes=duration_minutes)

        query = select(Reservation).where(Reservation.table_id == table_id)

        if exclude_id is not None:
            query = query.where(Reservation.id != exclude_id)

        result = await db.execute(query)
        reservations = result.scalars().all()

        # Проверяем пересечения
        overlapping = []
        for r in reservations:
            r_time = r.reservation_time
            if r_time.tzinfo is None:
                r_time = r_time.replace(tzinfo=timezone.utc)
            else:
                r_time = r_time.astimezone(timezone.utc)

            # Рассчитываем время окончания существующей брони
            existing_end_time = r_time + timedelta(minutes=r.duration_minutes)

            # Проверяем пересечение интервалов
            if (r_time < new_end_time and reservation_time < existing_end_time):
                overlapping.append(r)

        return overlapping