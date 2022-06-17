from itertools import combinations

import pytest
from fastapi.testclient import TestClient

from ...main import app


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture
def transfer_management_api_root():
    return "/transfers/"


@pytest.fixture
def base_body():
    return {"sender_name": "sender_name", "recipient_name": "recipient_name"}


@pytest.fixture()
def transfer_in(base_body):
    return {**base_body, "transfer_amount": 23}


@pytest.fixture
def post_transfer_wrong_body_res(client, transfer_management_api_root, base_body):
    return client.post(transfer_management_api_root, json=base_body)


@pytest.fixture
def post_transfer_correct_body_res(client, transfer_management_api_root, transfer_in):
    res = client.post(transfer_management_api_root, json=transfer_in)
    yield res
    client.delete(f"{transfer_management_api_root}{res.json().get('id')}")


@pytest.fixture
def db_transfer(client, post_transfer_correct_body_res):
    return post_transfer_correct_body_res.json()


def get_transfers_query_params_combinations():
    params = ["sender_name=sender_name", "recipient_name=recipient_name", "transfer_amount=23"]
    params_combinations = []
    for i in range(1, 4):
        params_combinations += list(combinations(params, i))
    return ['&'.join(combination) for combination in params_combinations]
