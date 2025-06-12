from fastapi import status
from fastapi.testclient import TestClient


def test_create_courier(client: TestClient):
    """
    Testa a criação bem-sucedida de um novo entregador
    """
    # Arrange
    courier_data = {"name": "Lucas Rangel", "vehicle": "Kawasaki Ninja"}

    # Act
    response = client.post("/api/v1/couriers/", json=courier_data)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == courier_data["name"]
    assert data["vehicle"] == courier_data["vehicle"]
    assert "id" in data
    assert "status" in data
    assert data["status"] == "available"


def test_get_courier_not_found(client: TestClient):
    """
    Testa a obtenção de um entregador que não existe
    """
    # Arrange
    non_existent_id = "a1b2c3d4-e5f6-7890-1234-567890abcdef"

    # Act
    response = client.get(f"/api/v1/couriers/{non_existent_id}")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Courier not found"


def test_create_and_get_courier(client: TestClient):
    """
    Testa a criação e a subsequente obtenção de um entregador
    """
    # Arrange
    courier_data = {"name": "Lucas Rangel", "vehicle": "Kawasaki Ninja"}
    response_create = client.post("/api/v1/couriers/", json=courier_data)
    created_id = response_create.json()["id"]

    # Act
    response_get = client.get(f"/api/v1/couriers/{created_id}")

    # Assert
    assert response_get.status_code == status.HTTP_200_OK
    data = response_get.json()
    assert data["id"] == created_id
    assert data["name"] == courier_data["name"]


def test_list_couriers(client: TestClient):
    """
    Testa a listagem de entregadores
    """
    # Arrange
    client.post(
        "/api/v1/couriers/", json={"name": "Lucas Rangel", "vehicle": "Kawasaki Ninja"}
    )
    client.post(
        "/api/v1/couriers/", json={"name": "Outro Entregador", "vehicle": "Moto"}
    )

    # Act
    response = client.get("/api/v1/couriers/")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    assert "Lucas Rangel" in [c["name"] for c in data]
    assert "Outro Entregador" in [c["name"] for c in data]


def test_update_courier(client: TestClient):
    """
    Testa a atualização de um entregador existente
    """
    # Arrange
    courier_data = {"name": "Nome Original", "vehicle": "Van"}
    response_create = client.post("/api/v1/couriers/", json=courier_data)
    created_id = response_create.json()["id"]
    update_data = {"name": "Lucas Rangel Atualizado", "status": "unavailable"}

    # Act
    response_update = client.put(f"/api/v1/couriers/{created_id}", json=update_data)

    # Assert
    assert response_update.status_code == status.HTTP_200_OK
    data = response_update.json()
    assert data["name"] == "Lucas Rangel Atualizado"
    assert data["status"] == "unavailable"


def test_delete_courier(client: TestClient):
    """
    Testa a remoção de um entregador
    """
    # Arrange
    courier_data = {"name": "Entregador Temporário", "vehicle": "Patinete"}
    response_create = client.post("/api/v1/couriers/", json=courier_data)
    created_id = response_create.json()["id"]

    # Act
    response_delete = client.delete(f"/api/v1/couriers/{created_id}")

    # Assert
    assert response_delete.status_code == status.HTTP_204_NO_CONTENT

    # Assert
    response_get = client.get(f"/api/v1/couriers/{created_id}")
    assert response_get.status_code == status.HTTP_404_NOT_FOUND


def test_delete_courier_with_associated_order(client: TestClient):
    """
    Testa que um entregador com um pedido associado não pode ser removido
    """
    # Arrange
    courier_response = client.post(
        "/api/v1/couriers/", json={"name": "Lucas Rangel", "vehicle": "Kawasaki Ninja"}
    )
    courier_id = courier_response.json()["id"]

    # Arrange
    order_response = client.post(
        "/api/v1/orders/",
        json={
            "customer_name": "Cliente de Teste",
            "address": "Rua Teste, 123",
            "value": 10.50,
        },
    )
    order_id = order_response.json()["id"]

    # Arrange
    client.put(f"/api/v1/orders/{order_id}", json={"courier_id": courier_id})

    # Act
    response_delete = client.delete(f"/api/v1/couriers/{courier_id}")

    # Assert
    assert response_delete.status_code == status.HTTP_409_CONFLICT
    data = response_delete.json()
    assert data["detail"] == "Cannot delete courier, as they have associated orders"
