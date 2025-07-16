from api.chai_model.client import ChaiModelApiClient

def test_valid_config():
    client = ChaiModelApiClient(
        api_url="http://test-url",
        api_key="test-key",
        bot_name="test-bot",
        prompt="test-prompt",
    )
    assert isinstance(client, ChaiModelApiClient)
