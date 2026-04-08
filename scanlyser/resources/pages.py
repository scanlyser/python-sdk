from __future__ import annotations

from typing import TYPE_CHECKING

from scanlyser.types import PaginatedResponse, ScanPage

if TYPE_CHECKING:
    from scanlyser.client import Client


class PageResource:
    def __init__(self, client: Client, team_id: str) -> None:
        self._client = client
        self._team_id = team_id

    def list(self, scan_id: str, per_page: int = 15) -> PaginatedResponse[ScanPage]:
        response = self._client.get(f"{self._team_id}/scans/{scan_id}/pages", params={"per_page": per_page})
        meta = response.get("meta", {})

        return PaginatedResponse(
            data=[ScanPage.from_dict(item) for item in response.get("data", [])],
            current_page=meta.get("current_page", 1),
            per_page=meta.get("per_page", per_page),
            total=meta.get("total", 0),
            last_page=meta.get("last_page", 1),
        )

    def get(self, scan_id: str, page_id: str) -> ScanPage:
        response = self._client.get(f"{self._team_id}/scans/{scan_id}/pages/{page_id}")

        return ScanPage.from_dict(response["data"])
