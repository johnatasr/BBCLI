from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from app.cli import cli

AUTh_CODE = "authorization_code"


@pytest.fixture
def runner():
    return CliRunner()


@patch("app.cli.run_callback_server", MagicMock(return_value=True))
@patch("app.cli.generate_ssl_certificate", MagicMock(return_value=True))
@patch("app.cli.load_constants_from_yaml", MagicMock(return_value={}))
@patch("app.cli.click.prompt", MagicMock(return_value=AUTh_CODE))
def test_create_project(runner):
    with patch("app.cli.BitbucketService") as MockService:
        mock_service = MockService.return_value
        mock_service.do_login.return_value = True
        mock_service.create_project.return_value = True

        result = runner.invoke(
            cli, ["create-project", "-n", "project_name", "-w", "workspace"]
        )

        assert 'Project "project_name" created successfully' in result.output


@patch("app.cli.run_callback_server", MagicMock(return_value=True))
@patch("app.cli.generate_ssl_certificate", MagicMock(return_value=True))
@patch("app.cli.load_constants_from_yaml", MagicMock(return_value={}))
@patch("app.cli.click.prompt", MagicMock(return_value=AUTh_CODE))
def test_create_repository(runner):
    with patch("app.cli.BitbucketService") as MockService:
        mock_service = MockService.return_value
        mock_service.do_login.return_value = True
        mock_service.create_project.return_value = True

        result = runner.invoke(
            cli,
            [
                "create-repository",
                "-p",
                "project",
                "-r",
                "repo_name",
                "-w",
                "workspace",
            ],
        )

        assert 'Repository "repo_name" created successfully' in result.output


@patch("app.cli.run_callback_server", MagicMock(return_value=True))
@patch("app.cli.generate_ssl_certificate", MagicMock(return_value=True))
@patch("app.cli.load_constants_from_yaml", MagicMock(return_value={}))
@patch("app.cli.click.prompt", MagicMock(return_value=AUTh_CODE))
def test_add_user(runner):
    with patch("app.cli.BitbucketService") as MockService:
        mock_service = MockService.return_value
        mock_service.do_login.return_value = True
        mock_service.create_project.return_value = True

        result = runner.invoke(
            cli, ["add-user", "-r", "repository", "-e", "user_email", "-w", "workspace"]
        )

        assert (
            'User "user_email" added to repository "repository" successfully'
            in result.output
        )


@patch("app.cli.run_callback_server", MagicMock(return_value=True))
@patch("app.cli.generate_ssl_certificate", MagicMock(return_value=True))
@patch("app.cli.load_constants_from_yaml", MagicMock(return_value={}))
@patch("app.cli.click.prompt", MagicMock(return_value="authorization_code"))
def test_remove_user(runner):
    with patch("app.cli.BitbucketService") as MockService:
        mock_service = MockService.return_value
        mock_service.do_login.return_value = True
        mock_service.create_project.return_value = True

        result = runner.invoke(
            cli,
            [
                "remove-user",
                "-r",
                "repository",
                "-u",
                "user_name",
                "-w",
                "workspace",
                "-a",
                "admin_username",
                "-p",
                "password",
            ],
        )

        assert (
            'User "user_name" removed from repository "repository" successfully'
            in result.output
        )


@patch("app.cli.run_callback_server", MagicMock(return_value=True))
@patch("app.cli.generate_ssl_certificate", MagicMock(return_value=True))
@patch("app.cli.load_constants_from_yaml", MagicMock(return_value={}))
@patch("app.cli.click.prompt", MagicMock(return_value="authorization_code"))
def test_allow_users_merge(runner):
    with patch("app.cli.BitbucketService") as MockService:
        mock_service = MockService.return_value
        mock_service.do_login.return_value = True
        mock_service.create_project.return_value = True

        result = runner.invoke(
            cli,
            ["allow-users-merge", "-r", "repository", "-w", "workspace", "-b", "main"],
        )

        assert "Users allowed to merge successfully" in result.output
