from __future__ import annotations


class ScanLyserError(Exception):
    def __init__(self, message: str, status: int = 0) -> None:
        super().__init__(message)
        self.status = status


class AuthenticationError(ScanLyserError):
    def __init__(self, message: str = "Authentication failed.") -> None:
        super().__init__(message, 401)


class ForbiddenError(ScanLyserError):
    def __init__(self, message: str = "Access denied.") -> None:
        super().__init__(message, 403)


class NotFoundError(ScanLyserError):
    def __init__(self, message: str = "Resource not found.") -> None:
        super().__init__(message, 404)


class ValidationError(ScanLyserError):
    def __init__(self, message: str = "Validation failed.", errors: dict[str, list[str]] | None = None) -> None:
        super().__init__(message, 422)
        self.errors = errors or {}


class RateLimitError(ScanLyserError):
    def __init__(self, message: str = "Rate limit exceeded.") -> None:
        super().__init__(message, 429)


def map_error(status: int, body: dict) -> ScanLyserError:
    error = body.get("error", {})
    message = error.get("message", f"API request failed with status {status}")
    errors = error.get("errors", {})

    match status:
        case 401:
            return AuthenticationError(message)
        case 403:
            return ForbiddenError(message)
        case 404:
            return NotFoundError(message)
        case 422:
            return ValidationError(message, errors)
        case 429:
            return RateLimitError(message)
        case _:
            return ScanLyserError(message, status)
