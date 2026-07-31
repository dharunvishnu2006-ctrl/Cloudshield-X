from abc import ABC, abstractmethod
from src.models import Alert, LogEvent
from src.logging_setup import get_logger
from datetime import datetime, timezone

logger = get_logger("detectors")


class BaseDetector(ABC):
    def __init__(self, name: str, threshold: int) -> None:
        self.name = name
        self.threshold = threshold
        self._counts: dict = {}

    @abstractmethod
    def detect(self, events: list[LogEvent]) -> list[Alert]:
        raise NotImplementedError


class BruteForceDetector(BaseDetector):
    def __init__(self, threshold: int = 3) -> None:
        super().__init__("brute_force", threshold)

    def detect(self, events: list[LogEvent]) -> list[Alert]:
        counts: dict = {}
        for e in events:
            if e.status in (401, 403):
                counts[e.ip] = counts.get(e.ip, 0) + 1

        alerts = []
        for ip, count in counts.items():
            if count >= self.threshold:
                severity = "high" if count >= 5 else "medium"
                alerts.append(
                    Alert(
                        ip=ip,
                        reason="brute force login",
                        count=count,
                        severity=severity,
                        at=datetime.now(timezone.utc).isoformat(),
                    )
                )
        return alerts


class RateDetector(BaseDetector):
    def __init__(self, threshold: int = 100) -> None:
        super().__init__("rate_limit", threshold)

    def detect(self, events: list[LogEvent]) -> list[Alert]:
        counts: dict = {}
        for e in events:
            counts[e.ip] = counts.get(e.ip, 0) + 1

        alerts = []
        for ip, count in counts.items():
            if count >= self.threshold:
                alerts.append(
                    Alert(
                        ip=ip,
                        reason="rate limit exceeded",
                        count=count,
                        severity="critical",
                        at=datetime.now(timezone.utc).isoformat(),
                    )
                )
        return alerts


def __repr__(self) -> str:
    return f"alert(ip={self.ip}," f"severity={self.severity}," f"count={self.count})"


def __eq__(self, other: object) -> bool:
    if not isinstance(other, Alert):
        return False
    return self.ip == other.ip and self.reason == other.reason


def __len__(self) -> int:
    return self.count


class DetectorFactory:
    _registry = {
        "brute_force": BruteForceDetector,
        "rate_limit": RateDetector,
    }

    @classmethod
    def from_config(cls, config: dict) -> list[BaseDetector]:
        detectors = []
        for name, settings in config.items():
            if name in cls._registry:
                threshold = settings.get("threshold", 3)
                detectors.append(cls._registry[name](threshold))
            else:
                logger.warning(f"Unknown detector: {name}")
        return detectors
