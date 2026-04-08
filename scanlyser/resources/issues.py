from __future__ import annotations

from typing import TYPE_CHECKING

from scanlyser.types import Issue, PaginatedResponse

if TYPE_CHECKING:
    from scanlyser.client import Client


class IssueResource:
    def __init__(self, client: Client, team_id: str) -> None:
        self._client = client
        self._team_id = team_id

    def list(
        self,
        scan_id: str,
        *,
        category: str | None = None,
        severity: str | None = None,
        per_page: int = 50,
    ) -> PaginatedResponse[Issue]:
        params: dict = {"per_page": per_page}

        if category is not None:
            params["category"] = category

        if severity is not None:
            params["severity"] = severity

        response = self._client.get(f"{self._team_id}/scans/{scan_id}/issues", params=params)
        meta = response.get("meta", {})

        return PaginatedResponse(
            data=[Issue.from_dict(item) for item in response.get("data", [])],
            current_page=meta.get("current_page", 1),
            per_page=meta.get("per_page", per_page),
            total=meta.get("total", 0),
            last_page=meta.get("last_page", 1),
        )
