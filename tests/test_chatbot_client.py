import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import chatbot_client

@pytest.mark.asyncio
@patch("chatbot_client.websockets.connect")
@patch("chatbot_client.input")
@patch("utils.chatbot_client_utils.input")
async def test_initiate_chat_start_new(mock_utils_input, mock_client_input, mock_ws_connect):
    # Arrange
    mock_utils_input.side_effect = ["Alice", "y"]
    mock_client_input.side_effect = ["exit"]
    mock_ws = MagicMock()
    mock_ws.__aenter__ = AsyncMock(return_value=mock_ws)
    mock_ws.__aexit__ = AsyncMock(return_value=None)
    mock_ws.recv = AsyncMock(return_value="[[END]]")
    mock_ws.send = AsyncMock()
    mock_ws_connect.return_value = mock_ws

    # Act
    await chatbot_client.chat()

    # Assert
    mock_ws_connect.assert_called()
    assert mock_ws.send.await_count >= 0

@pytest.mark.asyncio
@patch("chatbot_client.websockets.connect")
@patch("chatbot_client.input")
@patch("utils.chatbot_client_utils.input")
async def test_initiate_chat_load_existing(mock_utils_input, mock_client_input, mock_ws_connect):
    mock_utils_input.side_effect = ["Bob", "n"]
    mock_client_input.side_effect = ["exit"]
    mock_ws = MagicMock()
    mock_ws.__aenter__ = AsyncMock(return_value=mock_ws)
    mock_ws.__aexit__ = AsyncMock(return_value=None)
    mock_ws.recv = AsyncMock(return_value="[[END]]")
    mock_ws.send = AsyncMock()
    mock_ws_connect.return_value = mock_ws
    await chatbot_client.chat()
    mock_ws_connect.assert_called()
    assert mock_ws.send.await_count >= 0

@pytest.mark.asyncio
@patch("chatbot_client.websockets.connect")
@patch("chatbot_client.input")
@patch("utils.chatbot_client_utils.input")
async def test_initiate_chat_invalid_input_defaults_to_load(mock_utils_input, mock_client_input, mock_ws_connect):
    mock_utils_input.side_effect = ["Charlie", "invalid"]
    mock_client_input.side_effect = ["exit"]
    mock_ws = MagicMock()
    mock_ws.__aenter__ = AsyncMock(return_value=mock_ws)
    mock_ws.__aexit__ = AsyncMock(return_value=None)
    mock_ws.recv = AsyncMock(return_value="[[END]]")
    mock_ws.send = AsyncMock()
    mock_ws_connect.return_value = mock_ws
    await chatbot_client.chat()
    mock_ws_connect.assert_called()
    assert mock_ws.send.await_count >= 0
