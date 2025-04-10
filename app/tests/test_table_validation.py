from app.config import settings


def test_table_validation_empty_name(client):
    table_data = {
        "name": "",
        "seats": 4,
        "location": "Empty Name Area"
    }

    # Act
    response = client.post(f"{settings.API_PREFIX}/tables/", json=table_data)

    # Assert
    assert response.status_code == 422


def test_table_validation_zero_seats(client):
    table_data = {
        "name": "Zero Seats Table",
        "seats": 0,
        "location": "Zero Seats Area"
    }

    # Act
    response = client.post(f"{settings.API_PREFIX}/tables/", json=table_data)

    # Assert
    assert response.status_code == 422


def test_table_validation_too_many_seats(client):
    table_data = {
        "name": "Too Many Seats Table",
        "seats": 25,  # Больше максимума в 20
        "location": "Too Many Seats Area"
    }

    # Act
    response = client.post(f"{settings.API_PREFIX}/tables/", json=table_data)

    # Assert
    assert response.status_code == 422


def test_table_validation_empty_location(client):
    table_data = {
        "name": "Empty Location Table",
        "seats": 4,
        "location": ""
    }

    # Act
    response = client.post(f"{settings.API_PREFIX}/tables/", json=table_data)

    # Assert
    assert response.status_code == 422