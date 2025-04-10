import pytest

from app.repositories.table import TableRepository


@pytest.mark.asyncio
async def test_create_table(async_db_session):
    repo = TableRepository()
    data = {
        "name": "Test Table",
        "seats": 4,
        "location": "Corner"
    }
    created_table = await repo.create(async_db_session, data)

    assert created_table.id is not None
    assert created_table.name == "Test Table"
    assert created_table.seats == 4
    assert created_table.location == "Corner"

@pytest.mark.asyncio
async def test_get_all_tables_empty(async_db_session):
    repo = TableRepository()
    tables = await repo.get_all(async_db_session)
    assert tables == []

@pytest.mark.asyncio
async def test_delete_table(async_db_session):
    repo = TableRepository()
    data = {
        "name": "Delete Test Table",
        "seats": 4,
        "location": "Delete Area"
    }
    created_table = await repo.create(async_db_session, data)
    table_id = created_table.id

    result = await repo.delete(async_db_session, table_id)
    assert result is True

    found = await repo.get(async_db_session, table_id)
    assert found is None