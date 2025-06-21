import pytest
from monitor import utils
from unittest.mock import patch

@pytest.mark.django_db
@patch("monitor.utils.requests.get")
def test_verificar_status_online(mock_get):
    mock_get.return_value.status_code = 200
    resultado = utils.verificar_status("http://exemplo.com")
    assert resultado == "online"

@patch("monitor.utils.requests.get")
def test_verificar_status_offline(mock_get):
    mock_get.return_value.status_code = 500
    resultado = utils.verificar_status("http://exemplo.com")
    assert resultado == "offline"

@patch("monitor.utils.requests.get", side_effect=Exception("Erro"))
def test_verificar_status_erro(mock_get):
    resultado = utils.verificar_status("http://exemplo.com")
    assert resultado == "offline"
