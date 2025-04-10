from pydantic import BaseModel, Field, field_validator, ConfigDict


class TableBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Название столика")
    seats: int = Field(..., gt=0, le=20, description="Количество мест за столиком (от 1 до 20)")
    location: str = Field(..., min_length=1, max_length=100, description="Расположение столика в ресторане")

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Название столика не может быть пустым')
        return v

    @field_validator('location')
    @classmethod
    def location_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Расположение столика не может быть пустым')
        return v


class TableCreate(TableBase):
    pass


class Table(TableBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Table 1",
                "seats": 4,
                "location": "Main Hall"
            }
        }
    )