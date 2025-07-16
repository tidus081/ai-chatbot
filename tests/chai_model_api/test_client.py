import pytest
from unittest.mock import patch
from chai_model_api.client import ChaiModelApiClient
from chai_model_api.response import ChaiModelResponse

@pytest.fixture
def dummy_history():
    return [
        {"sender": "User", "message": "Hello"},
        {"sender": "Bot", "message": "Hi! How can I help you?"},
    ]

@patch("chai_model_api.client.requests.post")
def test_send_chat_success_returns_chai_model_response_instance(mock_post, dummy_history):
    # Arrange
    client = ChaiModelApiClient()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "model_output": "Test response",
        "model_name": "chai-test-model",
    }
    # Act
    response = client.send_chat(chat_history=dummy_history)
    # Assert
    assert isinstance(response, ChaiModelResponse)

@patch("chai_model_api.client.requests.post")
def test_send_chat_success_sets_status_code(mock_post, dummy_history):
    client = ChaiModelApiClient()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "model_output": "Test response",
        "model_name": "chai-test-model",
    }
    response = client.send_chat(chat_history=dummy_history)
    assert response.status_code == 200

@patch("chai_model_api.client.requests.post")
def test_send_chat_success_sets_model_output(mock_post, dummy_history):
    client = ChaiModelApiClient()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "model_output": "Test response",
        "model_name": "chai-test-model",
    }
    response = client.send_chat(chat_history=dummy_history)
    assert response.model_output == "Test response"

@patch("chai_model_api.client.requests.post")
def test_send_chat_success_sets_model_name(mock_post, dummy_history):
    client = ChaiModelApiClient()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "model_output": "Test response",
        "model_name": "chai-test-model",
    }
    response = client.send_chat(chat_history=dummy_history)
    assert response.model_name == "chai-test-model"

@patch("chai_model_api.client.requests.post")
def test_send_chat_failure_sets_status_code(mock_post, dummy_history):
    client = ChaiModelApiClient()
    mock_post.return_value.status_code = 500
    mock_post.return_value.json.return_value = {}
    response = client.send_chat(chat_history=dummy_history)
    assert response.status_code == 500

@patch("chai_model_api.client.requests.post")
def test_send_chat_failure_sets_model_output_none(mock_post, dummy_history):
    client = ChaiModelApiClient()
    mock_post.return_value.status_code = 500
    mock_post.return_value.json.return_value = {}
    response = client.send_chat(chat_history=dummy_history)
    assert response.model_output is None

@patch("chai_model_api.client.requests.post")
def test_send_chat_failure_sets_model_name_none(mock_post, dummy_history):
    client = ChaiModelApiClient()
    mock_post.return_value.status_code = 500
    mock_post.return_value.json.return_value = {}
    response = client.send_chat(chat_history=dummy_history)
    assert response.model_name is None
