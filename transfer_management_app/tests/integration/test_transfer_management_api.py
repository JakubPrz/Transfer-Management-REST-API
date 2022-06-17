import pytest
from fastapi import status

from .conftest import get_transfers_query_params_combinations


@pytest.mark.parametrize('query_params', get_transfers_query_params_combinations())
def test_get_transfers(client, transfer_management_api_root, query_params):
    response = client.get(f"{transfer_management_api_root}?{query_params}")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_get_existing_transfer(client, transfer_management_api_root, db_transfer):
    response = client.get(f"{transfer_management_api_root}{db_transfer.get('id')}")
    assert response.status_code == status.HTTP_200_OK


def test_get_non_existing_transfer(client, transfer_management_api_root):
    response = client.get(f"{transfer_management_api_root}999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_post_transfer_correct_body(client, post_transfer_correct_body_res):
    assert post_transfer_correct_body_res.status_code == status.HTTP_201_CREATED


def test_post_transfer_wrong_body(client, post_transfer_wrong_body_res):
    assert post_transfer_wrong_body_res.status_code == status.HTTP_400_BAD_REQUEST


def test_delete_existing_transfer(client, transfer_management_api_root, db_transfer):
    response = client.delete(f"{transfer_management_api_root}{db_transfer.get('id')}")
    assert response.status_code == status.HTTP_200_OK


def test_delete_non_existing_transfer(client, transfer_management_api_root):
    response = client.delete(f"{transfer_management_api_root}999999")
    assert response.status_code == status.HTTP_200_OK


def test_put_existing_transfer_correct_body(client, transfer_management_api_root, transfer_in, db_transfer):
    response = client.put(f"{transfer_management_api_root}{db_transfer.get('id')}", json=transfer_in)
    assert response.status_code == status.HTTP_200_OK


def test_put_non_existing_transfer_correct_body(client, transfer_management_api_root, transfer_in):
    response = client.put(f"{transfer_management_api_root}99999999", json=transfer_in)
    assert response.status_code == status.HTTP_201_CREATED


def test_put_transfer_wrong_body(client, transfer_management_api_root, db_transfer, base_body):
    response = client.put(f"{transfer_management_api_root}{db_transfer.get('id')}", json=base_body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
