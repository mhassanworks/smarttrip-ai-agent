from __future__ import annotations
import hashlib
import hmac
import json
import secrets

class HMACSecurity:
    def __init__(self, secret: str | None = None):
        self.secret = (secret or secrets.token_hex(32)).encode("utf-8")

    def sign(self, payload: dict) -> dict:
        message = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return {
            "payload": payload,
            "signature": hmac.new(self.secret, message, hashlib.sha256).hexdigest(),
        }

    def verify(self, envelope: dict) -> bool:
        if not isinstance(envelope, dict) or "payload" not in envelope or "signature" not in envelope:
            return False
        message = json.dumps(envelope["payload"], sort_keys=True, separators=(",", ":")).encode("utf-8")
        expected = hmac.new(self.secret, message, hashlib.sha256).hexdigest()
        return hmac.compare_digest(str(envelope["signature"]), expected)
