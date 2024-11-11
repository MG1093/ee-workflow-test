import pytest
import requests

BASE_URL = "http://localhost:8080"  # Localhost where the Flask app is running


@pytest.fixture
def user():
    """Fixture to set up a valid GitHub username."""
    return "octocat"


def test_get_gists_valid_user(user):
    """Test case to check if the app's main endpoint is up and running for a valid user."""
    response = requests.get(f"{BASE_URL}/{user}")

    # Assert that the HTTP status code is 200 OK
    assert response.status_code == 200

    # Check that the response JSON contains a list of gists
    response_json = response.json()
    assert isinstance(response_json, list)


def test_get_gists_invalid_path():
    """Test case to check the behavior when an invalid path is provided."""
    response = requests.get(f"{BASE_URL}/")

    # Assert that the HTTP status code is 404 Not Found
    assert response.status_code == 404

    # Check that the response contains an error message
    response_json = response.json()
    assert "error" in response_json
    assert "message" in response_json


def test_get_gists_with_query_params(user):
    """Test case to check if query parameters 'since', 'per_page', and 'page' are handled correctly."""
    params = {"per_page": 5, "page": 1, "since": "2023-01-01T00:00:00Z"}
    response = requests.get(f"{BASE_URL}/{user}", params=params)

    # Assert that the HTTP status code is 200 OK
    assert response.status_code == 200

    # Check that the response JSON contains a list
    response_json = response.json()
    assert isinstance(response_json, list)


def test_get_gists_invalid_per_page(user):
    """Test case to check invalid 'per_page' query parameter (non-integer)."""
    params = {"per_page": "invalid"}
    response = requests.get(f"{BASE_URL}/{user}", params=params)

    # Assert that the HTTP status code is 400 Bad Request
    assert response.status_code == 400

    # Check the error message in the response
    response_json = response.json()
    assert response_json["message"] == "'page' and 'per_page' query parameters must be numbers"


def test_get_gists_invalid_page(user):
    """Test case to check invalid 'page' query parameter (non-integer)."""
    params = {"page": "invalid"}
    response = requests.get(f"{BASE_URL}/{user}", params=params)

    # Assert that the HTTP status code is 400 Bad Request
    assert response.status_code == 400

    # Check the error message in the response
    response_json = response.json()
    assert response_json["message"] == "'page' and 'per_page' query parameters must be numbers"


def test_get_gists_invalid_per_page_value(user):
    """Test case to check 'per_page' greater than 100 (GitHub API limitation)."""
    params = {"per_page": 150}
    response = requests.get(f"{BASE_URL}/{user}", params=params)

    # Assert that the HTTP status code is 400 Bad Request
    assert response.status_code == 400

    # Check the error message in the response
    response_json = response.json()
    assert response_json["message"] == "'per_page' must be between 1 and 100."


def test_get_gists_invalid_page_value(user):
    """Test case to check 'page' less than 1."""
    params = {"page": 0}
    response = requests.get(f"{BASE_URL}/{user}", params=params)

    # Assert that the HTTP status code is 400 Bad Request
    assert response.status_code == 400

    # Check the error message in the response
    response_json = response.json()
    assert response_json["message"] == "'page' must be greater than or equal to 1."


def test_get_gists_valid_since_timestamp(user):
    """Test case to check valid 'since' timestamp query parameter."""
    params = {"since": "2023-10-01T00:00:00Z"}
    response = requests.get(f"{BASE_URL}/{user}", params=params)

    # Assert that the HTTP status code is 200 OK
    assert response.status_code == 200

    # Check that the response JSON contains a list
    response_json = response.json()
    assert isinstance(response_json, list)
