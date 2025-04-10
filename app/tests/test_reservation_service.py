from datetime import datetime, timedelta, timezone

import pytest

from app.repositories.table import TableRepository
from app.schemas.reservation import ReservationCreate
from app.services.reservation import ReservationService


class TestReservationService:
    @pytest.fixture
    def service(self):
        return ReservationService()

    @pytest.mark.asyncio
    async def test_get_all_reservations_empty(self, service, async_db_session):
        all_res = await service.get_all_reservations(async_db_session)
        assert len(all_res) == 0

    @pytest.mark.asyncio
    async def test_create_reservation_success(self, service, async_db_session):
        table_repo = TableRepository()
        created_table = await table_repo.create(async_db_session, {
            "name": "Test Table",
            "seats": 4,
            "location": "Main Hall"
        })

        data = ReservationCreate(
            customer_name="Test User",
            table_id=created_table.id,
            reservation_time=datetime.now(tz=timezone.utc) + timedelta(hours=1),
            duration_minutes=60
        )

        result = await service.create_reservation(async_db_session, data)
        assert not isinstance(result, tuple), f"Ожидалась успешная бронь, а не ошибка: {result}"

        all_res = await service.get_all_reservations(async_db_session)
        assert len(all_res) == 1
        assert all_res[0].customer_name == "Test User"

    @pytest.mark.asyncio
    async def test_create_reservation_table_not_found(self, service, async_db_session):
        data = ReservationCreate(
            customer_name="Alice",
            table_id=9999,  # заведомо несуществующий
            reservation_time=datetime.now(tz=timezone.utc) + timedelta(hours=2),
            duration_minutes=60
        )
        result = await service.create_reservation(async_db_session, data)

        assert isinstance(result, tuple)
        assert result[0] is False
        assert "не найден" in result[1]

    @pytest.mark.asyncio
    async def test_create_reservation_overlapping(self, service, async_db_session):
        table_repo = TableRepository()
        created_table = await table_repo.create(async_db_session, {
            "name": "Overlap Table",
            "seats": 4,
            "location": "Test"
        })

        first_data = ReservationCreate(
            customer_name="Bob",
            table_id=created_table.id,
            reservation_time=datetime.now(tz=timezone.utc) + timedelta(hours=1),
            duration_minutes=60
        )
        first_res = await service.create_reservation(async_db_session, first_data)
        assert not isinstance(first_res, tuple)

        second_data = ReservationCreate(
            customer_name="Charlie",
            table_id=created_table.id,
            # Начинается в середине первой
            reservation_time=first_data.reservation_time + timedelta(minutes=30),
            duration_minutes=60
        )
        second_res = await service.create_reservation(async_db_session, second_data)

        assert isinstance(second_res, tuple)
        assert second_res[0] is False
        assert "уже забронирован" in second_res[1]

    @pytest.mark.asyncio
    async def test_delete_reservation_success(self, service, async_db_session):
        table_repo = TableRepository()
        created_table = await table_repo.create(async_db_session, {
            "name": "Table for Delete",
            "seats": 4,
            "location": "Main Hall"
        })

        data = ReservationCreate(
            customer_name="Eve",
            table_id=created_table.id,
            reservation_time=datetime.now(tz=timezone.utc) + timedelta(hours=1),
            duration_minutes=60
        )
        created_res = await service.create_reservation(async_db_session, data)
        assert not isinstance(created_res, tuple)

        success = await service.delete_reservation(async_db_session, created_res.id)
        assert success is True

        all_res = await service.get_all_reservations(async_db_session)
        assert len(all_res) == 0
