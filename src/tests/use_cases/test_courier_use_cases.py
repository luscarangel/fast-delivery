from unittest.mock import ANY, MagicMock
from uuid import uuid4

import pytest

from src.domain.entities.courier import Courier, CourierStatus
from src.use_cases.create_courier import CreateCourier
from src.use_cases.delete_courier import DeleteCourier
from src.use_cases.get_courier_by_id import GetCourierById
from src.use_cases.list_couriers import ListCouriers
from src.use_cases.update_courier import UpdateCourier


def test_create_courier():
    """
    Teste Unitário: Testa a criação de um entregador
    """
    # Arrange
    mock_courier_repo = MagicMock()
    use_case = CreateCourier(courier_repository=mock_courier_repo)
    courier_data = {"name": "Lucas Rangel", "vehicle": "Kawasaki Ninja"}

    # Act
    use_case.execute(**courier_data)

    # Assert
    mock_courier_repo.save.assert_called_once_with(ANY)


def test_get_courier_by_id():
    """
    Teste Unitário: Testa a busca de um entregador pelo seu ID
    """
    # Arrange
    mock_courier_repo = MagicMock()
    courier_id = uuid4()
    mock_courier_repo.get_by_id.return_value = Courier(
        id=courier_id, name="Teste", vehicle="Teste"
    )
    use_case = GetCourierById(courier_repository=mock_courier_repo)

    # Act
    result = use_case.execute(courier_id=courier_id)

    # Assert
    mock_courier_repo.get_by_id.assert_called_once_with(courier_id)
    assert result is not None
    assert result.id == courier_id


def test_list_couriers():
    """
    Teste Unitário: Testa a listagem de todos os entregadores
    """
    # Arrange
    mock_courier_repo = MagicMock()
    mock_courier_repo.get_all.return_value = [
        Courier(id=uuid4(), name="Teste", vehicle="Teste")
    ]
    use_case = ListCouriers(courier_repository=mock_courier_repo)

    # Act
    result = use_case.execute()

    # Assert
    mock_courier_repo.get_all.assert_called_once()
    assert len(result) == 1


def test_update_courier():
    """
    Teste Unitário: Testa a atualização de um entregador
    """
    # Arrange
    mock_courier_repo = MagicMock()
    courier_id = uuid4()
    existing_courier = Courier(
        id=courier_id, name="Nome Original", vehicle="Veículo Original"
    )
    mock_courier_repo.get_by_id.return_value = existing_courier
    use_case = UpdateCourier(courier_repository=mock_courier_repo)
    update_data = {"name": "Nome Atualizado", "status": CourierStatus.UNAVAILABLE}

    # Act
    use_case.execute(courier_id=courier_id, **update_data)

    # Assert
    mock_courier_repo.get_by_id.assert_called_once_with(courier_id)
    mock_courier_repo.save.assert_called_once()
    saved_courier = mock_courier_repo.save.call_args[0][0]
    assert saved_courier.name == "Nome Atualizado"
    assert saved_courier.status == CourierStatus.UNAVAILABLE


def test_delete_courier_successfully():
    """
    Teste Unitário: Testa a remoção bem-sucedida de um entregador sem pedidos associados
    """
    # Arrange
    mock_courier_repo = MagicMock()
    mock_order_repo = MagicMock()
    courier_id = uuid4()
    mock_courier_repo.get_by_id.return_value = Courier(
        id=courier_id, name="Teste", vehicle="Teste"
    )
    mock_order_repo.get_by_courier_id.return_value = []
    use_case = DeleteCourier(
        courier_repository=mock_courier_repo, order_repository=mock_order_repo
    )

    # Act
    use_case.execute(courier_id=courier_id)

    # Assert
    mock_courier_repo.get_by_id.assert_called_once_with(courier_id)
    mock_order_repo.get_by_courier_id.assert_called_once_with(courier_id)
    mock_courier_repo.delete.assert_called_once_with(courier_id)


def test_delete_courier_with_associated_orders_fails():
    """
    Teste Unitário: Testa que a remoção de um entregador com pedidos associados
    lança um ValueError
    """
    # Arrange
    mock_courier_repo = MagicMock()
    mock_order_repo = MagicMock()
    courier_id = uuid4()
    mock_courier_repo.get_by_id.return_value = Courier(
        id=courier_id, name="Teste", vehicle="Teste"
    )
    mock_order_repo.get_by_courier_id.return_value = [1, 2]
    use_case = DeleteCourier(
        courier_repository=mock_courier_repo, order_repository=mock_order_repo
    )

    # Act & Assert
    with pytest.raises(ValueError) as excinfo:
        use_case.execute(courier_id=courier_id)

    assert "Cannot delete courier, as they have associated orders" in str(excinfo.value)
    mock_courier_repo.delete.assert_not_called()
