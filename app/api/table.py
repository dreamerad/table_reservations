from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Path, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.services.table import TableService
from app.schemas.table import Table, TableCreate

router = APIRouter(
    prefix="/tables",
    tags=["tables"],
    responses={
        404: {"description": "Столик не найден"}
    }
)
table_service = TableService()

@router.get(
    "/",
    response_model=List[Table],
    summary="Получить все столики",
    description="Возвращает список всех столиков в ресторане"
)
async def get_tables(db: AsyncSession = Depends(get_db)):
    """
    Получить список всех столиков ресторана
    """
    return await table_service.get_all_tables(db)

@router.post(
    "/",
    response_model=Table,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый столик",
    description="Создает новый столик в ресторане"
)
async def create_table(
    table: TableCreate = Body(..., description="Данные нового столика"),
    db: AsyncSession = Depends(get_db)
):
    """
    Создать новый столик в ресторане
    """
    return await table_service.create_table(db, table)

@router.delete(
    "/{table_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить столик",
    description="Удаляет столик по указанному ID"
)
async def delete_table(
    table_id: int = Path(..., description="ID столика для удаления"),
    db: AsyncSession = Depends(get_db)
):
    """
    Удалить столик по ID
    """
    result = await table_service.delete_table(db, table_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Столик с ID {table_id} не найден"
        )