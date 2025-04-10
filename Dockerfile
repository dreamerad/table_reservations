FROM python:3.9

WORKDIR /app

# Установка PostgreSQL клиента
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Делаем скрипты исполняемыми
RUN chmod +x ./start.sh
RUN chmod +x ./create_migration.sh

# Expose port
EXPOSE 8000

# Run startup script and launch application
CMD ["./start.sh", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]