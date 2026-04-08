from __future__ import annotations

import json

import httpx

from scanlyser.client import Client


def mock_client(*responses: tuple[int, dict | None, dict | None]) -> Client:
    """Create a client with mocked HTTP responses.

    Each response is a tuple of (status_code, body_dict, headers_dict).
    """
    mocked = []

    for status, body, headers in responses:
        mocked.append(
            httpx.Response(
                status_code=status,
                content=json.dumps(body).encode() if body else b"",
                headers=headers or {},
            )
        )

    transport = httpx.MockTransport(lambda request: mocked.pop(0))
    http = httpx.Client(transport=transport, base_url="https://scanlyser.app/api/v1/")

    return Client(api_key="test-token", http_client=http)
