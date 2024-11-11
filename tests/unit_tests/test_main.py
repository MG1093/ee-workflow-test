import pytest
from unittest.mock import patch
import requests
from app.main import app, cache

# Mock the base URL for your app's API
BASE_URL = "http://unittestmock.com"


@pytest.fixture
def client():
    """Fixture to set up the Flask test client."""
    with app.test_client() as client:
        yield client


@patch("requests.get")
def test_get_gists_valid_user(mock_get, client):
    """Test case to check if the app's main endpoint is up and running for a valid user"""
    user = "octocat"
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{"id": 1, "description": "Gist 1"}]

    # Make a request to the app's endpoint
    response = client.get(f"/{user}")

    # Assert that the HTTP status code is 200 OK
    assert response.status_code == 200

    # Check that the response JSON contains a list of gists
    assert isinstance(response.json, list)


@patch("requests.get")
def test_get_gists_invalid_path(mock_get, client):
    """Test case to check the behavior when an invalid path is provided"""
    mock_get.return_value.status_code = 404

    response = client.get(f"/")

    # Assert that the HTTP status code is 404 Not Found
    assert response.status_code == 404

    # Check that the response contains an error message
    response_json = response.json
    assert "error" in response_json
    assert "message" in response_json


@patch("requests.get")
def test_get_gists_with_query_params(mock_get, client):
    """Test case to check if query parameters 'since', 'per_page', and 'page' are handled correctly"""
    user = "octocat"
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{"id": 1, "description": "Gist 1"}]

    response = client.get(f"/{user}?per_page=5&page=1&since=2023-01-01T00:00:00Z")

    # Assert the HTTP status code is 200 OK
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_get_gists_invalid_per_page(client):
    """Test case to check invalid 'per_page' query parameter (non-integer)"""
    user = "octocat"
    response = client.get(f"/{user}?per_page=invalid")

    # Assert that the HTTP status code is 400 Bad Request
    assert response.status_code == 400

    # Check the error message in the response
    response_json = response.json
    assert response_json["message"] == "'page' and 'per_page' query parameters must be numbers"


def test_get_gists_invalid_page(client):
    """Test case to check invalid 'page' query parameter (non-integer)"""
    user = "octocat"
    response = client.get(f"/{user}?page=invalid")

    # Assert that the HTTP status code is 400 Bad Request
    assert response.status_code == 400

    # Check the error message in the response
    response_json = response.json
    assert response_json["message"] == "'page' and 'per_page' query parameters must be numbers"


def test_get_gists_invalid_per_page_value(client):
    """Test case to check 'per_page' greater than 100 (GitHub API limitation)"""
    user = "octocat"
    response = client.get(f"/{user}?per_page=150")

    # Assert that the HTTP status code is 400 Bad Request
    assert response.status_code == 400

    # Check the error message in the response
    response_json = response.json
    assert response_json["message"] == "'per_page' must be between 1 and 100."


def test_get_gists_invalid_page_value(client):
    """Test case to check 'page' less than 1"""
    user = "octocat"
    response = client.get(f"/{user}?page=0")

    # Assert that the HTTP status code is 400 Bad Request
    assert response.status_code == 400

    # Check the error message in the response
    response_json = response.json
    assert response_json["message"] == "'page' must be greater than or equal to 1."


@patch("requests.get")
def test_get_gists_valid_since_timestamp(mock_get, client):
    """Test case to check valid 'since' timestamp query parameter"""
    user = "octocat"
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{"id": 1, "description": "Gist 1"}]

    response = client.get(f"/{user}?since=2023-10-01T00:00:00Z")

    # Assert the HTTP status code is 200 OK
    assert response.status_code == 200
    assert isinstance(response.json, list)


@patch("app.main.fetch_gists_from_github")
def test_get_gists_github_integration_error(mock_fetch_gists, client):
    """Test exception if integration issue happens between webserver and calling api"""
    user = "octocat"

    # Simulate an exception being raised by fetch_gists_from_github
    mock_fetch_gists.side_effect = requests.exceptions.RequestException()

    cache.clear()

    # Make the request to the endpoint
    response = client.get(f"/{user}")

    # Assert that the server returns a 500 error response
    assert response.status_code == 500

    # Assert that the response contains the correct error message
    assert "Github Integration Error" in response.json["error"]


@patch("app.main.fetch_gists_from_github")
def test_get_gists_internal_server_error(mock_fetch_gists, client):
    """Test exception if unexpected error happens in webserver"""
    user = "octocat"

    # Simulate an exception being raised by fetch_gists_from_github
    mock_fetch_gists.side_effect = Exception()

    cache.clear()

    # Make the request to the endpoint
    response = client.get(f"/{user}")

    # Assert that the server returns a 500 error response
    assert response.status_code == 500

    # Assert that the response contains the correct error message
    assert "Internal Server Error" in response.json["error"]
