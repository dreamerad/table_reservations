#!/bin/bash
set -e

mkdir -p /app/alembic/versions

# Чтение пароля из файла, если указан путь
if [ -n "$POSTGRES_PASSWORD_FILE" ] && [ -f "$POSTGRES_PASSWORD_FILE" ]; then
    POSTGRES_PASSWORD=$(cat "$POSTGRES_PASSWORD_FILE")
    echo "Password loaded from file: $POSTGRES_PASSWORD_FILE"
fi

echo "Waiting for PostgreSQL..."
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_SERVER" -U "$POSTGRES_USER" -d "postgres" -c '\q' 2>/dev/null; do
  echo "PostgreSQL unavailable - sleeping"
  sleep 1
done
echo "PostgreSQL is up and running!"

echo "Checking if database exists..."
DB_EXISTS=$(PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_SERVER" -U "$POSTGRES_USER" -d "postgres" -t -c "SELECT 1 FROM pg_database WHERE datname='$POSTGRES_DB'")
if [ -z "$DB_EXISTS" ]; then
    echo "Database $POSTGRES_DB does not exist, creating..."
    PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_SERVER" -U "$POSTGRES_USER" -d "postgres" -c "CREATE DATABASE $POSTGRES_DB"
    echo "Database $POSTGRES_DB created successfully!"
else
    echo "Database $POSTGRES_DB already exists!"
fi

echo "Running database migrations..."
cd /app && alembic upgrade head

echo "Starting FastAPI application..."
exec "$@"
