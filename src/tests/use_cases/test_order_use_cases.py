from unittest.mock import ANY, MagicMock
from uuid import uuid4

from src.domain.entities.delivery_status import DeliveryStatus
from src.domain.entities.order import Order
from src.use_cases.create_order import CreateOrder
from src.use_cases.delete_order import DeleteOrder
from src.use_cases.get_order_by_id import GetOrderById
from src.use_cases.list_orders import ListOrders
from src.use_cases.update_order import UpdateOrder


def test_create_order():
    """
    Teste Unitário: Testa a criação de um pedido
    """
    # Arrange
    mock_order_repo = MagicMock()
    use_case = CreateOrder(order_repository=mock_order_repo)
    order_data = {
        "customer_name": "Café Teste",
        "address": "Avenida Teste, 123",
        "value": 25.50,
    }

    # Act
    use_case.execute(**order_data)

    # Assert
    mock_order_repo.save.assert_called_once_with(ANY)


def test_get_order_by_id():
    """
    Teste Unitário: Testa a busca de um pedido pelo ID
    """
    # Arrange
    mock_order_repo = MagicMock()
    order_id = uuid4()
    mock_order_repo.get_by_id.return_value = Order(
        id=order_id, customer_name="Cliente Teste", address="Endereço Teste", value=10
    )
    use_case = GetOrderById(order_repository=mock_order_repo)

    # Act
    result = use_case.execute(order_id=order_id)

    # Assert
    mock_order_repo.get_by_id.assert_called_once_with(order_id)
    assert result is not None
    assert result.id == order_id


def test_list_orders():
    """
    Teste Unitário: Testa a listagem de todos os pedidos
    """
    # Arrange
    mock_order_repo = MagicMock()
    mock_order_repo.get_all.return_value = [
        Order(
            id=uuid4(), customer_name="Pedido Teste", address="Endereço Teste", value=10
        )
    ]
    use_case = ListOrders(order_repository=mock_order_repo)

    # Act
    result = use_case.execute()

    # Assert
    mock_order_repo.get_all.assert_called_once()
    assert len(result) == 1


def test_update_order():
    """
    Teste Unitário: Testa a atualização de um pedido
    """
    # Arrange
    mock_order_repo = MagicMock()
    mock_courier_repo = MagicMock()
    order_id = uuid4()
    existing_order = Order(
        id=order_id,
        customer_name="Cliente Original",
        address="Endereço Original",
        value=50,
    )
    mock_order_repo.get_by_id.return_value = existing_order
    use_case = UpdateOrder(
        order_repository=mock_order_repo, courier_repository=mock_courier_repo
    )
    update_data = {
        "customer_name": "Cliente Atualizado",
        "status": DeliveryStatus.DELIVERED,
    }

    # Act
    use_case.execute(order_id=order_id, **update_data)

    # Assert
    mock_order_repo.get_by_id.assert_called_once_with(order_id)
    mock_order_repo.save.assert_called_once()
    saved_order = mock_order_repo.save.call_args[0][0]
    assert saved_order.customer_name == "Cliente Atualizado"
    assert saved_order.status == DeliveryStatus.DELIVERED


def test_delete_order():
    """
    Teste Unitário: Testa a remoção de um pedido
    """
    # Arrange
    mock_order_repo = MagicMock()
    order_id = uuid4()
    use_case = DeleteOrder(order_repository=mock_order_repo)

    # Act
    use_case.execute(order_id=order_id)

    # Assert
    mock_order_repo.delete.assert_called_once_with(order_id)
