from datetime import datetime, timedelta, timezone

from app.config import settings


def test_reservation_validation_empty_name(client):
    table_data = {
        "name": "Validation Test Table",
        "seats": 4,
        "location": "Validation Area"
    }

    table_response = client.post(f"{settings.API_PREFIX}/tables/", json=table_data)
    assert table_response.status_code == 201
    table_id = table_response.json()["id"]

    now = datetime.now(timezone.utc)
    reservation_time = now + timedelta(days=1)

    reservation_data = {
        "customer_name": "",
        "table_id": table_id,
        "reservation_time": reservation_time.isoformat(),
        "duration_minutes": 120
    }

    response = client.post(f"{settings.API_PREFIX}/reservations/", json=reservation_data)

    assert response.status_code == 422  # Ошибка валидации


def test_reservation_validation_past_time(client):
    table_data = {
        "name": "Past Time Test Table",
        "seats": 4,
        "location": "Past Time Area"
    }

    table_response = client.post(f"{settings.API_PREFIX}/tables/", json=table_data)
    assert table_response.status_code == 201
    table_id = table_response.json()["id"]

    now = datetime.now(timezone.utc)
    reservation_time = now - timedelta(days=1)  # Время в прошлом

    reservation_data = {
        "customer_name": "Past Time Customer",
        "table_id": table_id,
        "reservation_time": reservation_time.isoformat(),
        "duration_minutes": 120
    }

    response = client.post(f"{settings.API_PREFIX}/reservations/", json=reservation_data)

    assert response.status_code == 422


def test_reservation_validation_long_duration(client):
    table_data = {
        "name": "Long Duration Test Table",
        "seats": 4,
        "location": "Long Duration Area"
    }

    # Создаем столик
    table_response = client.post(f"{settings.API_PREFIX}/tables/", json=table_data)
    assert table_response.status_code == 201
    table_id = table_response.json()["id"]

    now = datetime.now(timezone.utc)
    reservation_time = now + timedelta(days=1)

    reservation_data = {
        "customer_name": "Long Duration Customer",
        "table_id": table_id,
        "reservation_time": reservation_time.isoformat(),
        "duration_minutes": 600
    }

    # Act
    response = client.post(f"{settings.API_PREFIX}/reservations/", json=reservation_data)

    # Assert
    assert response.status_code == 422