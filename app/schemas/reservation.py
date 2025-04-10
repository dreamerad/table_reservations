from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field, field_validator, ConfigDict


class ReservationBase(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=100, description="Имя клиента")
    table_id: int = Field(..., gt=0, description="ID столика")
    reservation_time: datetime = Field(..., description="Время начала брони")
    duration_minutes: int = Field(..., gt=0, le=480, description="Продолжительность брони в минутах (не более 8 часов)")

    @field_validator('customer_name')
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Имя клиента не может быть пустым')
        return v

    @field_validator('reservation_time', mode='before')
    @classmethod
    def validate_reservation_time(cls, v):
        # Определяем локальный часовой пояс (используем Moscow по умолчанию)
        local_tz = ZoneInfo('Europe/Moscow')

        # Если передана строка, преобразуем в datetime
        if isinstance(v, str):
            v = datetime.fromisoformat(v)

        # Устанавливаем локальный часовой пояс
        if v.tzinfo is None:
            v = v.replace(tzinfo=local_tz)

        return v

    @field_validator('reservation_time')
    @classmethod
    def time_must_be_future(cls, v):
        # Используем локальный часовой пояс для текущего времени
        local_tz = ZoneInfo('Europe/Moscow')
        now = datetime.now(local_tz)

        # Проверяем, что бронь не в прошлом
        if v < now - timedelta(minutes=10):
            raise ValueError('Время бронирования должно быть в будущем')

        return v

    @field_validator('reservation_time', mode='before')
    @classmethod
    def ensure_timezone(cls, v):
        """Гарантируем, что время имеет часовой пояс"""
        local_tz = ZoneInfo('Europe/Moscow')

        # Если передана строка, преобразуем в datetime
        if isinstance(v, str):
            v = datetime.fromisoformat(v)

        # Устанавливаем локальный часовой пояс, если не установлен
        if v.tzinfo is None:
            v = v.replace(tzinfo=local_tz)

        return v


class ReservationCreate(ReservationBase):
    pass


class Reservation(ReservationBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "customer_name": "John Doe",
                "table_id": 1,
                "reservation_time": "2025-04-15T19:00:00",
                "duration_minutes": 120
            }
        }
    )