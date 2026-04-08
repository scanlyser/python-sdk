from __future__ import annotations

from typing import TYPE_CHECKING

from scanlyser.types import PaginatedResponse, Site

if TYPE_CHECKING:
    from scanlyser.client import Client


class SiteResource:
    def __init__(self, client: Client, team_id: str) -> None:
        self._client = client
        self._team_id = team_id

    def list(self, per_page: int = 15) -> PaginatedResponse[Site]:
        response = self._client.get(f"{self._team_id}/sites", params={"per_page": per_page})
        meta = response.get("meta", {})

        return PaginatedResponse(
            data=[Site.from_dict(item) for item in response.get("data", [])],
            current_page=meta.get("current_page", 1),
            per_page=meta.get("per_page", per_page),
            total=meta.get("total", 0),
            last_page=meta.get("last_page", 1),
        )

    def create(self, name: str, url: str) -> Site:
        response = self._client.post(f"{self._team_id}/sites", json={"name": name, "url": url})

        return Site.from_dict(response["data"])

    def get(self, site_id: str) -> Site:
        response = self._client.get(f"{self._team_id}/sites/{site_id}")

        return Site.from_dict(response["data"])

    def delete(self, site_id: str) -> None:
        self._client.delete(f"{self._team_id}/sites/{site_id}")
