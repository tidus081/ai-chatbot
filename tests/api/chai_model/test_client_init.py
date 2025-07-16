import pytest
from unittest.mock import patch
from api.chai_model.client import ChaiModelApiClient

def test_missing_config_raises():
    with patch("os.getenv", side_effect=lambda k, d=None: None):
        with pytest.raises(Exception) as cm:
            ChaiModelApiClient()
        assert "Missing required configuration" in str(cm.value)


def test_partial_config():
    with patch(
        "os.getenv", side_effect=lambda k, d=None: "x" if k == "API_URL" else None
    ):
        with pytest.raises(Exception):
            ChaiModelApiClient()


def test_valid_config():
    with patch("os.getenv", side_effect=lambda k, d=None: "x"):
        client = ChaiModelApiClient()
        assert isinstance(client, ChaiModelApiClient)
