from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from app.policies import PolicyEngine
import json
import time


@dataclass
class AuditEvent:
    action: str
    target: str
    allowed: bool
    reason: str
    timestamp: float


class GuardedRuntime:
    def __init__(self, policy_path: str = "config/policy.yaml") -> None:
        self.policy = PolicyEngine(policy_path)
        self.audit_log: list[AuditEvent] = []

    def _record(self, action: str, target: str, allowed: bool, reason: str) -> None:
        self.audit_log.append(AuditEvent(action, target, allowed, reason, time.time()))

    def read_file(self, path: str) -> str:
        decision = self.policy.can_read(path)
        self._record("read_file", path, decision.allowed, decision.reason)
        if not decision.allowed:
            raise PermissionError(decision.reason)
        return Path(path).read_text(encoding="utf-8")

    def write_file(self, path: str, content: str) -> None:
        decision = self.policy.can_write(path)
        self._record("write_file", path, decision.allowed, decision.reason)
        if not decision.allowed:
            raise PermissionError(decision.reason)
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(content, encoding="utf-8")

    def call_url(self, url: str) -> str:
        domain = urlparse(url).netloc
        decision = self.policy.can_call_domain(domain)
        self._record("call_url", url, decision.allowed, decision.reason)
        if not decision.allowed:
            raise PermissionError(decision.reason)
        return f"stubbed network call to {url}"

    def save_audit(self, path: str = "output/audit.json") -> str:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(json.dumps([asdict(e) for e in self.audit_log], indent=2), encoding="utf-8")
        return path


class UnsafeRuntime:
    def __init__(self) -> None:
        self.audit_log: list[dict[str, Any]] = []

    def read_file(self, path: str) -> str:
        self.audit_log.append({"action": "read_file", "target": path, "allowed": True, "reason": "no controls"})
        return Path(path).read_text(encoding="utf-8")

    def write_file(self, path: str, content: str) -> None:
        self.audit_log.append({"action": "write_file", "target": path, "allowed": True, "reason": "no controls"})
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(content, encoding="utf-8")

    def call_url(self, url: str) -> str:
        self.audit_log.append({"action": "call_url", "target": url, "allowed": True, "reason": "no controls"})
        return f"stubbed network call to {url}"
