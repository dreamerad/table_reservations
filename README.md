# Restaurant Reservation API

## Требования
- Docker
- Docker Compose

## Быстрый старт

1. Клонируйте репозиторий
```bash
git clone https://github.com/your-repo/restaurant-reservation.git
cd restaurant-reservation
```

2. Запустите приложение
```bash
docker-compose up --build
```

## Полезные команды

- Создать миграцию: `docker-compose exec backend ./create_migration.sh "migration_name"`

## Документация API
После запуска документация доступна по адресу:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Структура проекта
- `app/` - Основной код приложения
- `alembic/` - Миграции базы данных
- `docker-compose.yml` - Конфигурация Docker Compose
- `Dockerfile` - Сборка Docker образа
- `start.sh` - Скрипт инициализации

## Разработка
- Код приложения монтируется как том, изменения применяются моментально
