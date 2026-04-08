import pytest

from scanlyser.errors import AuthenticationError, ForbiddenError, NotFoundError, RateLimitError, ValidationError

from tests.helpers import mock_client


def test_raises_authentication_error_on_401():
    client = mock_client((401, {"error": {"status": 401, "message": "Unauthenticated."}}, None))

    with pytest.raises(AuthenticationError, match="Unauthenticated."):
        client.sites("t").list()


def test_raises_forbidden_error_on_403():
    client = mock_client((403, {"error": {"status": 403, "message": "API access requires Agency plan."}}, None))

    with pytest.raises(ForbiddenError, match="API access requires Agency plan."):
        client.sites("t").list()


def test_raises_not_found_error_on_404():
    client = mock_client((404, {"error": {"status": 404, "message": "Site not found."}}, None))

    with pytest.raises(NotFoundError, match="Site not found."):
        client.sites("t").get("x")


def test_raises_validation_error_on_422_with_errors():
    client = mock_client((422, {"error": {"status": 422, "message": "The given data was invalid.", "errors": {"url": ["The url field is required."]}}}, None))

    with pytest.raises(ValidationError) as exc_info:
        client.sites("t").create(name="Test", url="")

    assert exc_info.value.errors["url"][0] == "The url field is required."


def test_retries_on_429_then_succeeds():
    client = mock_client(
        (429, {"error": {"message": "Too many requests."}}, {"Retry-After": "0"}),
        (200, {"data": [], "meta": {"status": 200, "current_page": 1, "per_page": 15, "total": 0, "last_page": 1}}, None),
    )

    result = client.sites("t").list()

    assert result.data == []


def test_raises_rate_limit_error_after_max_retries():
    responses = [(429, {"error": {"message": "Too many requests."}}, {"Retry-After": "0"})] * 4
    client = mock_client(*responses)

    with pytest.raises(RateLimitError):
        client.sites("t").list()
