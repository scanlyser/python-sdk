from __future__ import annotations

import time
from typing import TYPE_CHECKING

from scanlyser.errors import ScanLyserError
from scanlyser.types import PaginatedResponse, Scan

if TYPE_CHECKING:
    from scanlyser.client import Client


class ScanResource:
    def __init__(self, client: Client, team_id: str) -> None:
        self._client = client
        self._team_id = team_id

    def list(self, site_id: str, per_page: int = 15) -> PaginatedResponse[Scan]:
        response = self._client.get(f"{self._team_id}/sites/{site_id}/scans", params={"per_page": per_page})
        meta = response.get("meta", {})

        return PaginatedResponse(
            data=[Scan.from_dict(item) for item in response.get("data", [])],
            current_page=meta.get("current_page", 1),
            per_page=meta.get("per_page", per_page),
            total=meta.get("total", 0),
            last_page=meta.get("last_page", 1),
        )

    def trigger(self, site_id: str, wcag_level: str = "AA", webhook_url: str | None = None) -> Scan:
        data: dict = {"wcag_level": wcag_level}

        if webhook_url is not None:
            data["webhook_url"] = webhook_url

        response = self._client.post(f"{self._team_id}/sites/{site_id}/scans", json=data)

        return Scan.from_dict(response["data"])

    def get(self, scan_id: str) -> Scan:
        response = self._client.get(f"{self._team_id}/scans/{scan_id}")

        return Scan.from_dict(response["data"])

    def await_completion(
        self,
        scan_id: str,
        *,
        timeout_seconds: int = 600,
        poll_interval_seconds: int = 10,
    ) -> Scan:
        start = time.time()

        while True:
            scan = self.get(scan_id)

            if scan.is_terminal:
                return scan

            if time.time() - start >= timeout_seconds:
                raise ScanLyserError(
                    f"Scan {scan_id} did not complete within {timeout_seconds} seconds. Last status: {scan.status}",
                )

            time.sleep(poll_interval_seconds)
