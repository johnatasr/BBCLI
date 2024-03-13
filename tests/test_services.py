from http import HTTPStatus
from unittest.mock import Mock, patch

import pytest

from app.services import BitbucketService


@pytest.fixture
def bitbucket_service():
    constants = {
        "BITBUCKET_OAUTH2_URL": "https://bitbucket.org/site/oauth2",
        "CLIENT_ID": "client_id",
        "CLIENT_SECRET": "client_secret",
        "BITBUCKET_API_BASE_URL": "https://api.bitbucket.org",
    }
    return BitbucketService(constants)


def test_do_login(bitbucket_service):
    with patch("requests.post") as mock_post:
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK.value
        mock_response.json.return_value = {
            "access_token": "access_token",
            "refresh_token": "refresh_token",
        }
        mock_post.return_value = mock_response

        assert bitbucket_service.do_login("code") == True
        assert bitbucket_service.access_token == "access_token"
        assert bitbucket_service.refresh_token == "refresh_token"


def test_refresh_access_token(bitbucket_service):
    with patch("requests.post") as mock_post:
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK.value
        mock_response.json.return_value = {"access_token": "new_access_token"}
        mock_post.return_value = mock_response

        bitbucket_service.refresh_token = "refresh_token"
        message, status = bitbucket_service.refresh_access_token()

        assert status == True
        assert message == "Token refreshed successfully"
        assert bitbucket_service.access_token == "new_access_token"


def test_make_authenticated_request(bitbucket_service):
    with patch("requests.request") as mock_request:
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK.value
        mock_request.return_value = mock_response

        bitbucket_service.access_token = "access_token"
        response = bitbucket_service.make_authenticated_request(
            "GET", "https://api.bitbucket.org/2.0/repositories"
        )

        assert response.status_code == HTTPStatus.OK.value
        mock_request.assert_called_once_with(
            "GET",
            "https://api.bitbucket.org/2.0/repositories",
            headers={
                "Authorization": "Bearer access_token",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )
