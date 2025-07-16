# NOTE: Run tests with 'PYTHONPATH=. pytest' from the project root to resolve 'api' imports.
import pytest
from unittest.mock import patch
from api.chai_model.client import ChaiModelApiClient
from api.chai_model.response import ChaiModelResponse

@pytest.fixture
def dummy_history():
    return [
        {"sender": "User", "message": "Hello"},
        {"sender": "Bot", "message": "Hi! How can I help you?"},
    ]

@patch("api.chai_model.client.requests.post")
def test_send_chat_success_returns_chai_model_response_instance(mock_post, dummy_history):
    # Arrange
    client = ChaiModelApiClient(
        api_url="http://test-url",
        api_key="test-key",
        bot_name="test-bot",
        prompt="test-prompt",
    )
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "model_output": "Test response",
        "model_name": "chai-test-model",
    }
    # Act
    response = client.send_chat(chat_history=dummy_history, user_name="test_user")
    # Assert
    assert isinstance(response, ChaiModelResponse)


@patch("api.chai_model.client.requests.post")
def test_send_chat_failure_sets_status_code(mock_post, dummy_history):
    client = ChaiModelApiClient(
        api_url="http://test-url",
        api_key="test-key",
        bot_name="test-bot",
        prompt="test-prompt",
    )
    mock_post.return_value.status_code = 500
    mock_post.return_value.json.return_value = {}
    response = client.send_chat(chat_history=dummy_history, user_name="test_user")
    assert response.status_code == 500

@patch("api.chai_model.client.requests.post")
def test_send_chat_failure_sets_model_output_none(mock_post, dummy_history):
    client = ChaiModelApiClient(
        api_url="http://test-url",
        api_key="test-key",
        bot_name="test-bot",
        prompt="test-prompt",
    )
    mock_post.return_value.status_code = 500
    mock_post.return_value.json.return_value = {}
    response = client.send_chat(chat_history=dummy_history, user_name="test_user")
    assert response.model_output is None

@patch("api.chai_model.client.requests.post")
def test_send_chat_failure_sets_model_name_none(mock_post, dummy_history):
    client = ChaiModelApiClient(
        api_url="http://test-url",
        api_key="test-key",
        bot_name="test-bot",
        prompt="test-prompt",
    )
    mock_post.return_value.status_code = 500
    mock_post.return_value.json.return_value = {}
    response = client.send_chat(chat_history=dummy_history, user_name="test_user")
    assert response.model_name is None
