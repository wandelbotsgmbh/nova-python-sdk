import pytest
from wandelbots import use_nova_api


@pytest.fixture()
def nova_api_client():
    return use_nova_api("172.30.1.202")