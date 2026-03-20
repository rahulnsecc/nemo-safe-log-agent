from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import yaml


@dataclass
class PolicyDecision:
    allowed: bool
    reason: str


class PolicyEngine:
    def __init__(self, policy_path: str = "config/policy.yaml") -> None:
        with open(policy_path, "r", encoding="utf-8") as f:
            self.policy: dict[str, Any] = yaml.safe_load(f)
        self.allow_read = [Path(p).resolve() for p in self.policy["filesystem"].get("allow_read", [])]
        self.allow_write = [Path(p).resolve() for p in self.policy["filesystem"].get("allow_write", [])]
        self.deny_read = [Path(p).resolve() for p in self.policy["filesystem"].get("deny_read", [])]
        self.allow_domains = set(self.policy["network"].get("allow_domains", []))
        self.deny_all_other = bool(self.policy["network"].get("deny_all_other", True))

    def _under(self, path: Path, roots: list[Path]) -> bool:
        return any(str(path).startswith(str(root)) for root in roots)

    def can_read(self, path: str) -> PolicyDecision:
        p = Path(path).resolve()
        if self._under(p, self.deny_read):
            return PolicyDecision(False, f"read denied by policy for {p}")
        if self._under(p, self.allow_read):
            return PolicyDecision(True, f"read allowed for {p}")
        return PolicyDecision(False, f"read denied by default for {p}")

    def can_write(self, path: str) -> PolicyDecision:
        p = Path(path).resolve()
        if self._under(p, self.allow_write):
            return PolicyDecision(True, f"write allowed for {p}")
        return PolicyDecision(False, f"write denied by default for {p}")

    def can_call_domain(self, domain: str) -> PolicyDecision:
        if domain in self.allow_domains:
            return PolicyDecision(True, f"network allowed to {domain}")
        if self.deny_all_other:
            return PolicyDecision(False, f"network denied by policy to {domain}")
        return PolicyDecision(True, f"network allowed to {domain}")
