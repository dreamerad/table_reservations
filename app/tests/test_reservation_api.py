from datetime import datetime, timedelta, timezone

from app.config import settings


def test_create_reservation(client):
    table_data = {
        "name": "API Reservation Test Table",
        "seats": 4,
        "location": "API Reservation Area"
    }

    table_response = client.post(f"{settings.API_PREFIX}/tables/", json=table_data)
    assert table_response.status_code == 201
    table_id = table_response.json()["id"]

    now = datetime.now(timezone.utc)
    reservation_time = now + timedelta(days=1)

    reservation_data = {
        "customer_name": "API Test Customer",
        "table_id": table_id,
        "reservation_time": reservation_time.isoformat(),
        "duration_minutes": 120
    }

    response = client.post(f"{settings.API_PREFIX}/reservations/", json=reservation_data)

    # Assert - проверяем успешное создание бронирования
    assert response.status_code == 201, f"Ожидался код 201, получен {response.status_code}. Ответ: {response.text}"
    data = response.json()
    assert data["customer_name"] == reservation_data["customer_name"]
    assert data["table_id"] == table_id
    assert data["duration_minutes"] == 120
    assert "id" in data


def test_create_reservation_invalid_table(client):
    non_existent_table_id = 99999

    now = datetime.now(timezone.utc)
    reservation_time = now + timedelta(days=1)

    reservation_data = {
        "customer_name": "API Invalid Table Customer",
        "table_id": non_existent_table_id,
        "reservation_time": reservation_time.isoformat(),
        "duration_minutes": 120
    }

    response = client.post(f"{settings.API_PREFIX}/reservations/", json=reservation_data)

    assert response.status_code == 400
    assert "не найден" in response.json()["detail"]


def test_create_reservation_overlap(client):
    table_data = {
        "name": "API Overlap Test Table",
        "seats": 6,
        "location": "API Overlap Area"
    }

    table_response = client.post(f"{settings.API_PREFIX}/tables/", json=table_data)
    assert table_response.status_code == 201
    table_id = table_response.json()["id"]

    now = datetime.now(timezone.utc)
    base_time = now + timedelta(days=1)
    reservation_time1 = base_time.replace(hour=18, minute=0, second=0, microsecond=0)

    reservation_data1 = {
        "customer_name": "API First Customer",
        "table_id": table_id,
        "reservation_time": reservation_time1.isoformat(),
        "duration_minutes": 120
    }

    first_response = client.post(f"{settings.API_PREFIX}/reservations/", json=reservation_data1)
    assert first_response.status_code == 201, f"Не удалось создать первое бронирование: {first_response.text}"

    reservation_time2 = base_time.replace(hour=19, minute=0, second=0, microsecond=0)
    reservation_data2 = {
        "customer_name": "API Second Customer",
        "table_id": table_id,
        "reservation_time": reservation_time2.isoformat(),
        "duration_minutes": 120
    }

    second_response = client.post(f"{settings.API_PREFIX}/reservations/", json=reservation_data2)

    assert second_response.status_code == 400, f"Должна быть ошибка перекрытия. Получено: {second_response.text}"
    assert "уже забронирован" in second_response.json()["detail"]


def test_get_reservations(client):
    table_data = {
        "name": "API Get Reservations Table",
        "seats": 4,
        "location": "API Get Area"
    }

    table_response = client.post(f"{settings.API_PREFIX}/tables/", json=table_data)
    assert table_response.status_code == 201
    table_id = table_response.json()["id"]

    now = datetime.now(timezone.utc)
    created_reservations = []

    for i in range(3):
        reservation_data = {
            "customer_name": f"API Get Customer {i}",
            "table_id": table_id,
            "reservation_time": (now + timedelta(days=1, hours=i * 3)).isoformat(),
            "duration_minutes": 60
        }
        response = client.post(f"{settings.API_PREFIX}/reservations/", json=reservation_data)
        assert response.status_code == 201, f"Не удалось создать бронирование {i}: {response.text}"
        created_reservations.append(response.json())

    response = client.get(f"{settings.API_PREFIX}/reservations/")

    assert response.status_code == 200
    data = response.json()

    # Проверяем, что созданные бронирования присутствуют в ответе
    for reservation in created_reservations:
        assert any(r["id"] == reservation["id"] for r in data), f"Бронирование {reservation['id']} не найдено в ответе"

    # Проверяем количество созданных бронирований с нужными именами
    test_reservations = [r for r in data if r["customer_name"].startswith("API Get Customer")]
    assert len(test_reservations) == 3


def test_delete_reservation(client):
    table_data = {
        "name": "API Delete Reservation Table",
        "seats": 4,
        "location": "API Delete Area"
    }

    table_response = client.post(f"{settings.API_PREFIX}/tables/", json=table_data)
    assert table_response.status_code == 201
    table_id = table_response.json()["id"]

    now = datetime.now(timezone.utc)
    reservation_data = {
        "customer_name": "API Delete Customer",
        "table_id": table_id,
        "reservation_time": (now + timedelta(days=1)).isoformat(),
        "duration_minutes": 120
    }

    create_response = client.post(f"{settings.API_PREFIX}/reservations/", json=reservation_data)
    assert create_response.status_code == 201
    reservation_id = create_response.json()["id"]

    delete_response = client.delete(f"{settings.API_PREFIX}/reservations/{reservation_id}")

    assert delete_response.status_code == 204

    get_response = client.get(f"{settings.API_PREFIX}/reservations/")
    reservations = get_response.json()
    reservation_still_exists = any(r["id"] == reservation_id for r in reservations)
    assert not reservation_still_exists


def test_delete_non_existent_reservation(client, clean_db):
    # Тестируем удаление несуществующего бронирования
    table_data = {
        "name": "Nonexistent Res Table",
        "seats": 4,
        "location": "Test Area"
    }
    client.post(f"{settings.API_PREFIX}/tables/", json=table_data)

    non_existent_id = 99999
    response = client.delete(f"{settings.API_PREFIX}/reservations/{non_existent_id}")

    assert response.status_code == 404
    assert "не найдена" in response.json()["detail"]