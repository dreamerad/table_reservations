from app.config import settings


def test_create_table(client):
    table_data = {
        "name": "API Test Table",
        "seats": 6,
        "location": "API Test Area"
    }

    response = client.post(f"{settings.API_PREFIX}/tables/", json=table_data)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == table_data["name"]
    assert data["seats"] == table_data["seats"]
    assert data["location"] == table_data["location"]
    assert "id" in data


def test_get_tables(client):
    table_data1 = {
        "name": "API Get Table 1",
        "seats": 2,
        "location": "API Get Area 1"
    }
    table_data2 = {
        "name": "API Get Table 2",
        "seats": 4,
        "location": "API Get Area 2"
    }

    client.post(f"{settings.API_PREFIX}/tables/", json=table_data1)
    client.post(f"{settings.API_PREFIX}/tables/", json=table_data2)

    response = client.get(f"{settings.API_PREFIX}/tables/")

    assert response.status_code == 200
    data = response.json()

    assert len(data) >= 2

    names = [t["name"] for t in data]
    assert "API Get Table 1" in names
    assert "API Get Table 2" in names


def test_delete_table(client):
    table_data = {
        "name": "API Delete Table",
        "seats": 8,
        "location": "API Delete Area"
    }

    create_response = client.post(f"{settings.API_PREFIX}/tables/", json=table_data)
    assert create_response.status_code == 201
    table_id = create_response.json()["id"]

    delete_response = client.delete(f"{settings.API_PREFIX}/tables/{table_id}")

    assert delete_response.status_code == 204

    get_response = client.get(f"{settings.API_PREFIX}/tables/")
    tables = get_response.json()
    table_still_exists = any(t["id"] == table_id for t in tables)
    assert not table_still_exists


def test_delete_non_existent_table(client, clean_db):
    non_existent_id = 99999

    response = client.delete(f"{settings.API_PREFIX}/tables/{non_existent_id}")

    assert response.status_code == 404
    assert "не найден" in response.json()["detail"]