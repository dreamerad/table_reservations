from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import table_router, reservation_router
from app.config import settings
from app.utils.logger import setup_logging, get_logger

setup_logging()
logger = get_logger()

app = FastAPI(
    title=settings.APP_NAME,
    description="""
    API для бронирования столиков в ресторане. 
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "tables",
            "description": "Операции со столиками ресторана",
        },
        {
            "name": "reservations",
            "description": "Операции с бронированиями столиков",
        },
    ]
)

# Настройки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(table_router, prefix=settings.API_PREFIX)
app.include_router(reservation_router, prefix=settings.API_PREFIX)


@app.get("/", include_in_schema=False)
async def root():
    """Корневой эндпоинт API"""
    return {
        "message": "Restaurant Reservation API",
        "docs": "/docs"
    }


@app.get("/health", include_in_schema=False)
async def health():
    """Эндпоинт для проверки здоровья API"""
    return {"status": "healthy"}


logger.info("Application started")