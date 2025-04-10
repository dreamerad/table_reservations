# Restaurant Reservation API

## Требования
- Docker
- Docker Compose

## Быстрый старт

1. Клонируйте репозиторий
```bash
git clone https://github.com/dreamerad/table_reservations.git
cd restaurant-reservation
```

2. Запустите приложение
```bash
docker-compose up --build
```

## Документация API
После запуска документация доступна по адресу:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Unit тесты
Для тестирования продукта необходимо заустить тесты в окружении:
docker exec -it backend bash
python3 -m pytest app/tests

## Структура проекта
- `app/` - Основной код приложения
- `alembic/` - Миграции базы данных
- `docker-compose.yml` - Конфигурация Docker Compose
- `Dockerfile` - Сборка Docker образа
- `start.sh` - Скрипт инициализации

## Разработка
- Код приложения монтируется как том, изменения применяются моментально

## Справка
- Многослойная архитектура с четким разделением ответственности
- Асинхронное программирование на базе FastAPI и SQLAlchemy
- Гибкая система валидации данных с Pydantic
- Dependency Injection для управления зависимостями
- Репозиторный паттерн для абстракции доступа к данным
- Поддержка конкурентности и неблокирующих операций
- Абстракция доступа к данным и изоляция логики работы с базой данных
