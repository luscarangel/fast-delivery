from fastapi import status
from fastapi.testclient import TestClient


def test_create_order(client: TestClient):
    """
    Testa a criação bem-sucedida de um novo pedido.
    """
    # Arrange
    order_data = {
        "customer_name": "Restaurante Saboroso",
        "address": "Rua Principal, 123, Cidade",
        "value": 150.50,
    }

    # Act
    response = client.post("/api/v1/orders/", json=order_data)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["customer_name"] == order_data["customer_name"]
    assert data["address"] == order_data["address"]
    assert data["value"] == order_data["value"]
    assert "id" in data
    assert "status" in data
    assert data["status"] == "in_progress"
    assert data["courier_id"] is None


def test_get_order_not_found(client: TestClient):
    """
    Testa a obtenção de um pedido que não existe
    """
    # Arrange
    non_existent_id = "a1b2c3d4-e5f6-7890-1234-567890abcdef"

    # Act
    response = client.get(f"/api/v1/orders/{non_existent_id}")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Order not found"


def test_create_and_get_order(client: TestClient):
    """
    Testa a criação e a subsequente obtenção de um pedido.
    """
    # Arrange
    order_data = {
        "customer_name": "Hamburgueria Veloz",
        "address": "Avenida Secundária, 456, Cidade",
        "value": 35.00,
    }
    response_create = client.post("/api/v1/orders/", json=order_data)
    created_id = response_create.json()["id"]

    # Act
    response_get = client.get(f"/api/v1/orders/{created_id}")

    # Assert
    assert response_get.status_code == status.HTTP_200_OK
    data = response_get.json()
    assert data["id"] == created_id
    assert data["customer_name"] == order_data["customer_name"]


def test_list_orders(client: TestClient):
    """
    Testa a listagem de pedidos
    """
    # Arrange
    client.post(
        "/api/v1/orders/",
        json={"customer_name": "Pedido A", "address": "Endereço A", "value": 1},
    )
    client.post(
        "/api/v1/orders/",
        json={"customer_name": "Pedido B", "address": "Endereço B", "value": 2},
    )

    # Act
    response = client.get("/api/v1/orders/")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    assert "Pedido A" in [o["customer_name"] for o in data]
    assert "Pedido B" in [o["customer_name"] for o in data]


def test_update_order(client: TestClient):
    """
    Testa a atualização de um pedido existente
    """
    # Arrange
    order_data = {
        "customer_name": "Cliente Inicial",
        "address": "Endereço Inicial",
        "value": 100,
    }
    response_create = client.post("/api/v1/orders/", json=order_data)
    created_id = response_create.json()["id"]

    # Arrange
    courier_response = client.post(
        "/api/v1/couriers/", json={"name": "Lucas Rangel", "vehicle": "Kawasaki Ninja"}
    )
    courier_id = courier_response.json()["id"]

    update_data = {
        "customer_name": "Cliente Atualizado",
        "status": "delivered",
        "courier_id": courier_id,
    }

    # Act
    response_update = client.put(f"/api/v1/orders/{created_id}", json=update_data)

    # Assert
    assert response_update.status_code == status.HTTP_200_OK
    data = response_update.json()
    assert data["customer_name"] == "Cliente Atualizado"
    assert data["status"] == "delivered"
    assert data["courier_id"] == courier_id


def test_assign_unavailable_courier_to_order_fails(client: TestClient):
    """
    Testa que um pedido não pode ser associado a um entregador que não está disponível
    """
    # Arrange
    courier_res = client.post(
        "/api/v1/couriers/", json={"name": "Lucas Rangel", "vehicle": "Kawasaki Ninja"}
    )
    courier_id = courier_res.json()["id"]
    client.put(f"/api/v1/couriers/{courier_id}", json={"status": "delivering"})

    # Arrange
    order_res = client.post(
        "/api/v1/orders/",
        json={
            "customer_name": "Cliente de Teste",
            "address": "Endereço de Teste",
            "value": 50,
        },
    )
    order_id = order_res.json()["id"]

    # Act
    response_update = client.put(
        f"/api/v1/orders/{order_id}", json={"courier_id": courier_id}
    )

    # Assert
    assert response_update.status_code == status.HTTP_409_CONFLICT
    error_detail = response_update.json()["detail"]
    assert "not available" in error_detail


def test_delete_order(client: TestClient):
    """
    Testa a remoção de um pedido
    """
    # Arrange
    order_data = {
        "customer_name": "Pedido Temporário",
        "address": "Endereço Temp",
        "value": 10,
    }
    response_create = client.post("/api/v1/orders/", json=order_data)
    created_id = response_create.json()["id"]

    # Act
    response_delete = client.delete(f"/api/v1/orders/{created_id}")

    # Assert
    assert response_delete.status_code == status.HTTP_204_NO_CONTENT

    # Assert
    response_get = client.get(f"/api/v1/orders/{created_id}")
    assert response_get.status_code == status.HTTP_404_NOT_FOUND
