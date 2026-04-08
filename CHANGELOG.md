# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-04-08

### Added
- `Client` class built on [httpx](https://www.python-httpx.org/) for synchronous HTTP communication with the ScanLyser API
- Resource classes for all API endpoints: `Teams`, `Sites`, `Scans`, `Pages`, `Issues`, and `Reports`
- Frozen dataclass response types (`Team`, `Site`, `Scan`, `ScanPage`, `ScanScores`, `Issue`) for safe, immutable API data
- `StrEnum` enums for all constrained string values: `ScanStatus`, `WcagLevel`, `IssueCategory`, and `IssueSeverity`
- Generic `PaginatedResponse[T]` type for paginated list endpoints
- Typed exception hierarchy: `ScanLyserError` (base), `AuthenticationError` (401), `ForbiddenError` (403), `NotFoundError` (404), `ValidationError` (422), and `RateLimitError` (429)
- Automatic retry on HTTP 429 responses, honouring the `Retry-After` header, with a configurable `max_retries` limit
- `ScanResource.await_completion()` polling helper with configurable `timeout_seconds` and `poll_interval_seconds`
- `verify_webhook_signature()` utility for validating webhook payloads using `hmac.compare_digest`
- Python 3.10, 3.11, 3.12, and 3.13 support
