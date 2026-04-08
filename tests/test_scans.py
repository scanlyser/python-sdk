from scanlyser.types import Scan, ScanStatus, WcagLevel

from tests.helpers import mock_client


def test_triggers_scan():
    client = mock_client((202, {
        "data": {"id": "scan_new", "site_id": "site_01", "status": "pending", "wcag_level": "AA", "pages_crawled": 0, "pages_total": 0, "issues_count": 0, "created_at": "2026-04-08T00:00:00Z"},
        "meta": {"status": 202},
    }, None))

    scan = client.scans("team_01").trigger("site_01", wcag_level="AA")

    assert scan.id == "scan_new"
    assert scan.status == ScanStatus.PENDING
    assert scan.wcag_level == WcagLevel.AA


def test_gets_completed_scan_with_scores():
    client = mock_client((200, {
        "data": {"id": "scan_01", "site_id": "site_01", "status": "completed", "wcag_level": "AAA", "pages_crawled": 50, "pages_total": 50, "issues_count": 120, "scores": {"overall": 72, "wcag": 65, "seo": 80, "performance": 85, "ux": 70, "sitewide": 60, "other": 75}, "created_at": "2026-01-01T00:00:00Z", "completed_at": "2026-01-01T02:00:00Z"},
        "meta": {"status": 200},
    }, None))

    scan = client.scans("team_01").get("scan_01")

    assert scan.status == ScanStatus.COMPLETED
    assert scan.is_terminal
    assert scan.scores is not None
    assert scan.scores.overall == 72.0


def test_terminal_states():
    completed = Scan.from_dict({"id": "s1", "site_id": "x", "status": "completed", "wcag_level": "AA", "pages_crawled": 1, "pages_total": 1, "issues_count": 0, "created_at": "2026-01-01T00:00:00Z"})
    failed = Scan.from_dict({"id": "s2", "site_id": "x", "status": "failed", "wcag_level": "AA", "pages_crawled": 0, "pages_total": 0, "issues_count": 0, "created_at": "2026-01-01T00:00:00Z", "failure_reason": "Bot protection"})
    pending = Scan.from_dict({"id": "s3", "site_id": "x", "status": "pending", "wcag_level": "AA", "pages_crawled": 0, "pages_total": 0, "issues_count": 0, "created_at": "2026-01-01T00:00:00Z"})

    assert completed.is_terminal is True
    assert failed.is_terminal is True
    assert pending.is_terminal is False
