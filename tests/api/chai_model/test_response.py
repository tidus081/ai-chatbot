from api.chai_model.response import ChaiModelResponse

def test_init_sets_fields():
    # Arrange
    resp = ChaiModelResponse(200, "output", "model")
    # Assert
    assert resp.status_code == 200
    assert resp.model_output == "output"
    assert resp.model_name == "model"

def test_repr_contains_fields():
    resp = ChaiModelResponse(200, "output", "model")
    r = repr(resp)
    assert "status_code=200" in r
    assert "model_output='output'" in r
    assert "model_name='model'" in r

def test_optional_fields_are_none():
    resp = ChaiModelResponse(404)
    assert resp.status_code == 404
    assert resp.model_output is None
    assert resp.model_name is None
# moved from tests/chai_model_api/test_response.py
