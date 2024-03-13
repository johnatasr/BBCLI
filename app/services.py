from http import HTTPStatus
from typing import Tuple

import requests


class BitbucketService:
    def __init__(self, constants):
        self.c = constants  # c for simplicity
        self.access_token = None
        self.refresh_token = None

    def do_login(self, code: str) -> bool:
        response = requests.post(
            "{}/access_token".format(self.c.get("BITBUCKET_OAUTH2_URL")),
            auth=(self.c.get("CLIENT_ID"), self.c.get("CLIENT_SECRET")),
            data={"grant_type": "authorization_code", "code": code},
        )

        if response.status_code is HTTPStatus.OK.value:
            data = response.json()
            self.access_token = data["access_token"]
            self.refresh_token = data.get("refresh_token")
            return True
        return False

    def refresh_access_token(self) -> Tuple[str, bool]:
        if not self.refresh_token:
            return "No refresh token available.", False

        response = requests.post(
            "{}/access_token".format(self.c.get("BITBUCKET_OAUTH2_URL")),
            auth=(self.c.get("CLIENT_ID"), self.c.get("CLIENT_SECRET")),
            data={"grant_type": "refresh_token", "refresh_token": self.refresh_token},
        )

        if response.status_code == HTTPStatus.OK.value:
            data = response.json()
            self.access_token = data["access_token"]
            return "Token refreshed successfully", True

        return "Failed to refresh token.", False

    def make_authenticated_request(self, method, url, **kwargs) -> requests.Response:
        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {self.access_token}"
        headers["Accept"] = "application/json"
        headers["Content-Type"] = headers["Accept"]
        kwargs["headers"] = headers
        return requests.request(method, url, **kwargs)

    def create_project(self, name, workspace: str) -> bool:
        payload = {"name": name, "key": name.split(" ")[0].upper(), "is_private": True}
        response = self.make_authenticated_request(
            "POST",
            "{}/2.0/workspaces/{}/projects".format(
                self.c.get("BITBUCKET_API_BASE_URL"), workspace
            ),
            json=payload,
        )
        response.raise_for_status()
        return response.status_code is HTTPStatus.CREATED.value

    def create_repository(self, project, repo_name, workspace: str) -> bool:
        payload = {
            "scm": "git",
            "project": {"key": project[:3].upper()},
            "name": repo_name,
            "is_private": True,
        }
        response = self.make_authenticated_request(
            "POST",
            "{}/2.0/repositories/{}/{}".format(
                self.c.get("BITBUCKET_API_BASE_URL"), workspace, repo_name
            ),
            json=payload,
        )
        response.raise_for_status()
        return response.status_code is HTTPStatus.OK.value

    def add_user_to_repository(self, repository, user_email, workspace: str) -> bool:
        response = self.make_authenticated_request(
            "POST",
            "{}/1.0/invitations/{}/{}".format(
                self.c.get("BITBUCKET_API_BASE_URL"), workspace, repository
            ),
            json={"permission": "write", "email": user_email},
        )
        response.raise_for_status()
        return response.status_code is HTTPStatus.OK.value

    def remove_user_from_repository(
        self, repository, user_name, workspace, admin, password: str
    ) -> bool:
        users: list = self.make_authenticated_request(
            "GET",
            "{}/2.0/repositories/{}/{}/permissions-config/users".format(
                self.c.get("BITBUCKET_API_BASE_URL"), workspace, repository
            ),
        ).json()["values"]

        user = next(
            filter(lambda u: user_name in u["user"]["display_name"], users)
        ).get("user")

        if user_uuid := user.get("uuid"):
            response = requests.delete(
                "{}/2.0/repositories/{}/{}/permissions-config/users/{}".format(
                    self.c.get("BITBUCKET_API_BASE_URL"),
                    workspace,
                    repository,
                    user_uuid,
                ),
                auth=(admin, password),
            )
            response.raise_for_status()
            return response.status_code in [
                HTTPStatus.OK.value,
                HTTPStatus.NO_CONTENT.value,
            ]
        return False

    def allow_users_merge_directly(
        self, repository, workspace, branch_name: str
    ) -> bool:
        restriction_type = "restrict_merges"

        url = "{}/2.0/repositories/{}/{}/branch-restrictions".format(
            self.c.get("BITBUCKET_API_BASE_URL"), workspace, repository
        )
        restrictions: list = self.make_authenticated_request("GET", url).json()[
            "values"
        ]

        if next(filter(lambda e: e["kind"] == restriction_type, restrictions)):
            return True

        payload = {"pattern": branch_name, "kind": restriction_type, "users": []}
        response = self.make_authenticated_request("POST", url, json=payload)
        response.raise_for_status()
        return response.status_code in [HTTPStatus.OK.value, HTTPStatus.CREATED.value]
