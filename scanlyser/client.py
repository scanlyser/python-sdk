from __future__ import annotations

import time
from typing import Any

import httpx

from scanlyser.errors import map_error
from scanlyser.resources.issues import IssueResource
from scanlyser.resources.pages import PageResource
from scanlyser.resources.reports import ReportResource
from scanlyser.resources.scans import ScanResource
from scanlyser.resources.sites import SiteResource
from scanlyser.resources.teams import TeamResource


class Client:
    """ScanLyser API client."""

    def __init__(
        self,
        api_key: str,
        *,
        max_retries: int = 3,
        http_client: httpx.Client | None = None,
    ) -> None:
        self._max_retries = max_retries
        self._http = http_client or httpx.Client(
            base_url="https://scanlyser.app/api/v1/",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )

    def teams(self) -> TeamResource:
        return TeamResource(self)

    def sites(self, team_id: str) -> SiteResource:
        return SiteResource(self, team_id)

    def scans(self, team_id: str) -> ScanResource:
        return ScanResource(self, team_id)

    def pages(self, team_id: str) -> PageResource:
        return PageResource(self, team_id)

    def issues(self, team_id: str) -> IssueResource:
        return IssueResource(self, team_id)

    def reports(self, team_id: str) -> ReportResource:
        return ReportResource(self, team_id)

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._request("GET", path, params=params)

    def post(self, path: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._request("POST", path, json=json)

    def delete(self, path: str) -> None:
        self._request("DELETE", path)

    def get_raw(self, path: str, params: dict[str, Any] | None = None) -> bytes:
        return self._request_raw("GET", path, params=params)

    def _request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        raw = self._request_raw(method, path, **kwargs)

        if not raw:
            return {}

        import json

        return json.loads(raw)

    def _request_raw(self, method: str, path: str, **kwargs: Any) -> bytes:
        attempts = 0

        while True:
            response = self._http.request(method, path, **kwargs)

            if response.is_success:
                return response.content

            if response.status_code == 429 and attempts < self._max_retries:
                retry_after = int(response.headers.get("Retry-After", "1"))
                time.sleep(retry_after)
                attempts += 1
                continue

            body = response.json() if response.content else {}
            raise map_error(response.status_code, body)
