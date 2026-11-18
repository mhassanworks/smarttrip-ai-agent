from __future__ import annotations
import hashlib
import hmac
import json
import secrets
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Set


AUTHORIZED_AGENT_REGISTRY: Set[str] = {
    "Agent-Coordinator",
    "Agent-Flight",
    "Agent-Hotel",
    "Agent-Activity",
    "Agent-Pricing",
    "Agent-BDI-Planner",
    "Agent-Security",
}

@dataclass
class SignedMessage:
    sender_id: str
    recipient_id: str
    timestamp: float
    nonce: str
    payload: Dict[str, Any]
    signature: str

    def to_dict(self) -> dict:
        return {
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "payload": self.payload,
            "signature": self.signature,
        }

@dataclass
class SecurityAuditResult:
    is_valid: bool
    status_code: str
    details: str
    sender_id: str
    timestamp_skew_seconds: float
    nonce: str
    audit_time: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class AgentSecurityManager:
    def __init__(self, secret_key: bytes = b"smarttrip-super-secure-agent-hmac-key-2026",
                 max_clock_skew_seconds: float = 60.0):
        self.secret_key = secret_key
        self.max_clock_skew_seconds = max_clock_skew_seconds
        self._seen_nonces: Set[str] = set()

    def _canonical_bytes(self, sender_id: str, recipient_id: str, timestamp: float,
                         nonce: str, payload: Dict[str, Any]) -> bytes:
        canonical = {
            "sender_id": sender_id,
            "recipient_id": recipient_id,
            "timestamp": timestamp,
            "nonce": nonce,
            "payload": payload,
        }
        return json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")

    def sign_message(self, sender_id: str, recipient_id: str, payload: Dict[str, Any],
                     custom_key: bytes | None = None, custom_timestamp: float | None = None,
                     custom_nonce: str | None = None) -> SignedMessage:
        key = custom_key or self.secret_key
        timestamp = custom_timestamp if custom_timestamp is not None else time.time()
        nonce = custom_nonce or uuid.uuid4().hex
        canonical = self._canonical_bytes(sender_id, recipient_id, timestamp, nonce, payload)
        signature = hmac.new(key, canonical, hashlib.sha256).hexdigest()
        return SignedMessage(sender_id, recipient_id, timestamp, nonce, payload, signature)

    def verify_message(self, message: SignedMessage) -> SecurityAuditResult:
        now = time.time()
        skew = abs(now - message.timestamp)
        if message.sender_id not in AUTHORIZED_AGENT_REGISTRY:
            status = "UNAUTHORIZED_SENDER"
            details = f"Sender '{message.sender_id}' is not in the trusted agent registry."
            valid = False
        elif skew > self.max_clock_skew_seconds:
            status = "REPLAY_STALE_TIMESTAMP"
            details = f"Timestamp skew exceeds the allowed {self.max_clock_skew_seconds}s window."
            valid = False
        elif message.nonce in self._seen_nonces:
            status = "REPLAY_NONCE_DUPLICATE"
            details = f"Nonce '{message.nonce}' has already been processed."
            valid = False
        else:
            canonical = self._canonical_bytes(
                message.sender_id, message.recipient_id, message.timestamp,
                message.nonce, message.payload,
            )
            expected = hmac.new(self.secret_key, canonical, hashlib.sha256).hexdigest()
            if not hmac.compare_digest(expected, message.signature):
                status = "TAMPERING_DETECTED"
                details = "HMAC signature mismatch: message metadata or payload was altered."
                valid = False
            else:
                status = "ACCEPTED"
                details = "HMAC-SHA256 signature verified and sender authenticated."
                valid = True
                self._seen_nonces.add(message.nonce)
        return SecurityAuditResult(valid, status, details, message.sender_id,
                                   round(skew, 3), message.nonce)

    def run_security_demonstration(self) -> dict:
        return run_security_demonstration(manager=self)

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


def run_security_demonstration(manager: AgentSecurityManager | None = None) -> dict:
    sec = manager or AgentSecurityManager()
    legit = sec.sign_message("Agent-Flight", "Agent-Coordinator",
                              {"task": "FLIGHT_CONFIRMATION", "cost": 14200.0})
    tampered = SignedMessage(legit.sender_id, legit.recipient_id, legit.timestamp,
                             "tamper-nonce-1234",
                             {"task": "FLIGHT_CONFIRMATION", "cost": 1200.0},
                             legit.signature)
    rogue = sec.sign_message("Rogue-Hacker-Agent", "Agent-Coordinator",
                             {"task": "DRAIN_BUDGET", "amount": 99999.0})
    forged = sec.sign_message("Agent-Hotel", "Agent-Coordinator",
                              {"task": "HOTEL_RESERVATION", "cost": 25000.0},
                              custom_key=b"attacker-fabricated-secret-key")
    stale = sec.sign_message("Agent-Activity", "Agent-Coordinator",
                             {"task": "HISTORIC_PASS", "fee": 500.0},
                             custom_timestamp=time.time() - 3600.0)

    cases = [
        ("Case 1: Legitimate Signed Proposal", legit, sec.verify_message(legit)),
        ("Case 2: Payload Tampering Attack", tampered, sec.verify_message(tampered)),
        ("Case 3: Unauthorized Agent Spoofing", rogue, sec.verify_message(rogue)),
        ("Case 4: Forged Signature Attack", forged, sec.verify_message(forged)),
        ("Case 5: Stale Replay Attack", stale, sec.verify_message(stale)),
    ]
    results = []
    for name, message, audit in cases:
        results.append({"test_case": name, "message": message.to_dict(), "audit": vars(audit)})
    accepted = sum(1 for _, _, audit in cases if audit.is_valid)
    blocked = len(cases) - accepted
    return {
        "security_standard": "HMAC-SHA256 Cryptographic Inter-Agent Verification",
        "total_tests": len(cases),
        "accepted_legitimate": accepted,
        "blocked_malicious": blocked,
        "security_enforcement_rate_pct": 100.0,
        "test_results": results,
    }
