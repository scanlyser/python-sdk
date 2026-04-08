from __future__ import annotations

from typing import TYPE_CHECKING

from scanlyser.types import PaginatedResponse, Team

if TYPE_CHECKING:
    from scanlyser.client import Client


class TeamResource:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(self, per_page: int = 15) -> PaginatedResponse[Team]:
        response = self._client.get("teams", params={"per_page": per_page})
        meta = response.get("meta", {})

        return PaginatedResponse(
            data=[Team.from_dict(item) for item in response.get("data", [])],
            current_page=meta.get("current_page", 1),
            per_page=meta.get("per_page", per_page),
            total=meta.get("total", 0),
            last_page=meta.get("last_page", 1),
        )

    def get(self, team_id: str) -> Team:
        response = self._client.get(f"teams/{team_id}")

        return Team.from_dict(response["data"])
