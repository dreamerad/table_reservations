from datetime import datetime, timedelta, timezone

import pytest

from app.repositories.reservation import ReservationRepository
from app.repositories.table import TableRepository


@pytest.mark.asyncio
async def test_create_reservation(async_db_session):
    table_repo = TableRepository()
    table = await table_repo.create(async_db_session, {
        "name": "Test Table",
        "seats": 4,
        "location": "Main Hall"
    })

    repo = ReservationRepository()

    reservation_data = {
        "customer_name": "John Doe",
        "table_id": table.id,
        "reservation_time": datetime.now(tz=timezone.utc) + timedelta(hours=1),
        "duration_minutes": 120
    }
    created_res = await repo.create(async_db_session, reservation_data)

    assert created_res.id is not None
    assert created_res.customer_name == "John Doe"
    assert created_res.table_id == table.id

@pytest.mark.asyncio
async def test_find_overlapping_reservations(async_db_session):
    """
    Проверяем логику пересечения бронирований.
    """
    table_repo = TableRepository()
    table = await table_repo.create(async_db_session, {
        "name": "Overlap Test Table",
        "seats": 4,
        "location": "Test"
    })

    repo = ReservationRepository()
    start_time = datetime.now(tz=timezone.utc) + timedelta(hours=1)

    res1 = await repo.create(async_db_session, {
        "customer_name": "User1",
        "table_id": table.id,
        "reservation_time": start_time,
        "duration_minutes": 60
    })

    overlapping_start = start_time + timedelta(minutes=30)
    overlapping = await repo.find_overlapping_reservations(
        async_db_session,
        table_id=table.id,
        reservation_time=overlapping_start,
        duration_minutes=60
    )
    assert len(overlapping) == 1
    assert overlapping[0].id == res1.id