# ScanLyser Python SDK

Official Python SDK for the [ScanLyser](https://scanlyser.app) API. Run accessibility, SEO, performance, UX, and security scans programmatically.

## Requirements

- Python 3.10+
- httpx

## Installation

```bash
pip install scanlyser-sdk
```

## Quick Start

```python
from scanlyser import Client

client = Client(api_key="your-api-token")

# List your sites
sites = client.sites(team_id).list()

for site in sites.data:
    print(f"{site.name}: {site.url}")

# Trigger a scan
scan = client.scans(team_id).trigger(site_id, wcag_level="AA")

# Wait for completion
scan = client.scans(team_id).await_completion(scan.id)

# Get issues
issues = client.issues(team_id).list(scan.id, severity="critical")
```

## API Reference

### Client

```python
client = Client(
    api_key="your-api-token",
    max_retries=3,  # optional, retries on 429
)
```

### Teams

```python
teams = client.teams().list()
team = client.teams().get(team_id)
```

### Sites

```python
sites = client.sites(team_id).list(per_page=15)
site = client.sites(team_id).create(name="My Site", url="https://example.com")
site = client.sites(team_id).get(site_id)
client.sites(team_id).delete(site_id)
```

### Scans

```python
scans = client.scans(team_id).list(site_id)
scan = client.scans(team_id).trigger(site_id, wcag_level="AA")
scan = client.scans(team_id).get(scan_id)

# Poll until complete (default: 600s timeout, 10s interval)
scan = client.scans(team_id).await_completion(
    scan_id,
    timeout_seconds=600,
    poll_interval_seconds=10,
)
```

### Pages

```python
pages = client.pages(team_id).list(scan_id)
page = client.pages(team_id).get(scan_id, page_id)
```

### Issues

```python
issues = client.issues(team_id).list(scan_id)
critical = client.issues(team_id).list(scan_id, category="wcag", severity="critical")
```

### Reports

```python
report = client.reports(team_id).json(scan_id)
client.reports(team_id).pdf(scan_id, save_to="/path/to/report.pdf")
```

## Webhook Verification

Verify webhook signatures from scan completion callbacks:

```python
from scanlyser import verify_webhook_signature

is_valid = verify_webhook_signature(
    payload=request.body,
    signature=request.headers["X-Signature"],
    secret=token_hash,
)
```

## Error Handling

The SDK raises typed exceptions for API errors:

```python
from scanlyser import NotFoundError, ValidationError, RateLimitError

try:
    site = client.sites(team_id).get("nonexistent")
except NotFoundError:
    # 404
    pass
except ValidationError as error:
    # 422 — error.errors contains field-level errors
    print(error.errors)
except RateLimitError:
    # 429 — automatic retries exhausted
    pass
```

Rate-limited requests (429) are automatically retried up to 3 times with the `Retry-After` delay.

## License

MIT
