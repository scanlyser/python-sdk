from scanlyser.types import PaginatedResponse, Site

from tests.helpers import mock_client


def test_lists_sites():
    client = mock_client((200, {
        "data": [{"id": "site_01", "name": "Example", "url": "https://example.com", "scans_count": 3, "created_at": "2026-01-01T00:00:00Z", "updated_at": "2026-01-02T00:00:00Z"}],
        "meta": {"status": 200, "current_page": 1, "per_page": 15, "total": 1, "last_page": 1},
    }, None))

    result = client.sites("team_01").list()

    assert isinstance(result, PaginatedResponse)
    assert len(result.data) == 1
    assert result.data[0].name == "Example"
    assert result.data[0].url == "https://example.com"


def test_creates_site():
    client = mock_client((201, {
        "data": {"id": "site_new", "name": "New Site", "url": "https://new.com", "created_at": "2026-04-08T00:00:00Z", "updated_at": "2026-04-08T00:00:00Z"},
        "meta": {"status": 201},
    }, None))

    site = client.sites("team_01").create(name="New Site", url="https://new.com")

    assert isinstance(site, Site)
    assert site.id == "site_new"
    assert site.name == "New Site"


def test_gets_site_with_latest_scan():
    client = mock_client((200, {
        "data": {
            "id": "site_01", "name": "Example", "url": "https://example.com",
            "latest_scan": {"id": "scan_01", "site_id": "site_01", "status": "completed", "wcag_level": "AA", "pages_crawled": 10, "pages_total": 10, "issues_count": 5, "scores": {"overall": 85, "wcag": 80, "seo": 90, "performance": 85, "ux": 88, "sitewide": 75, "other": 80}, "created_at": "2026-01-01T00:00:00Z", "completed_at": "2026-01-01T01:00:00Z"},
            "scans_count": 5, "created_at": "2026-01-01T00:00:00Z", "updated_at": "2026-01-02T00:00:00Z",
        },
        "meta": {"status": 200},
    }, None))

    site = client.sites("team_01").get("site_01")

    assert site.latest_scan is not None
    assert site.latest_scan.scores.overall == 85.0
