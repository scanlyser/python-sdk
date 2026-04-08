import hashlib
import hmac

from scanlyser.webhooks import verify_webhook_signature


def _sign(payload: str, secret: str) -> str:
    return "sha256=" + hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()


def test_verifies_valid_signature():
    payload = '{"event":"scan.completed","scan":{"id":"scan_01"}}'
    secret = "my-secret-key"
    signature = _sign(payload, secret)

    assert verify_webhook_signature(payload, signature, secret) is True


def test_rejects_invalid_signature():
    assert verify_webhook_signature('{"event":"scan.completed"}', "sha256=invalid", "my-secret-key") is False


def test_rejects_tampered_payload():
    secret = "my-secret-key"
    signature = _sign('{"event":"scan.completed"}', secret)

    assert verify_webhook_signature('{"event":"scan.failed"}', signature, secret) is False
