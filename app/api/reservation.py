from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Path, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.services.reservation import ReservationService
from app.schemas.reservation import Reservation, ReservationCreate

router = APIRouter(
    prefix="/reservations",
    tags=["reservations"],
    responses={
        404: {"description": "Бронь не найдена"}
    }
)
reservation_service = ReservationService()


@router.get(
    "/",
    response_model=List[Reservation],
    summary="Получить все брони"
)
async def get_reservations(db: AsyncSession = Depends(get_db)):
    """
    Получить список всех бронирований
    """
    return await reservation_service.get_all_reservations(db)


@router.post(
    "/",
    response_model=Reservation,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую бронь",
    responses={
        400: {"description": "Некорректные данные или столик уже забронирован"},
        404: {"description": "Столик не найден"}
    }
)
async def create_reservation(
        reservation: ReservationCreate = Body(..., description="Данные для бронирования"),
        db: AsyncSession = Depends(get_db)
):
    """
    Создать новую бронь столика
    """
    result = await reservation_service.create_reservation(db, reservation)

    if isinstance(result, tuple) and not result[0]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result[1]
        )

    return result


@router.delete(
    "/{reservation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить бронь",
    description="Удаляет бронь по указанному ID"
)
async def delete_reservation(
        reservation_id: int = Path(..., description="ID брони для удаления"),
        db: AsyncSession = Depends(get_db)
):
    """
    Удалить бронь по ID
    """
    result = await reservation_service.delete_reservation(db, reservation_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Бронь с ID {reservation_id} не найдена"
        )