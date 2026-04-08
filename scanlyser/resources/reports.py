from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from scanlyser.client import Client


class ReportResource:
    def __init__(self, client: Client, team_id: str) -> None:
        self._client = client
        self._team_id = team_id

    def json(self, scan_id: str) -> dict[str, Any]:
        return self._client.get(f"{self._team_id}/scans/{scan_id}/report", params={"format": "json"})

    def pdf(self, scan_id: str, save_to: str | Path) -> None:
        content = self._client.get_raw(f"{self._team_id}/scans/{scan_id}/report")

        Path(save_to).write_bytes(content)
