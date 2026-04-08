from __future__ import annotations

import hashlib
import hmac


def verify_webhook_signature(payload: str, signature: str, secret: str) -> bool:
    """Verify a webhook signature against the request payload."""
    expected = "sha256=" + hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()

    return hmac.compare_digest(expected, signature)
