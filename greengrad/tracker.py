"""Resource tracking primitives."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from statistics import mean
from typing import Callable


@dataclass(slots=True)
class ResourceSnapshot:
    """Single training resource snapshot."""

    step: int
    cpu_percent: float
    ram_percent: float
    gpu_power_watts: float | None = None
    gpu_utilization_percent: float | None = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class ResourceTracker:
    """Collects and stores resource snapshots."""

    def __init__(self, metrics_provider: Callable[[], dict[str, float | None]]):
        self._metrics_provider = metrics_provider
        self._snapshots: list[ResourceSnapshot] = []

    @property
    def snapshots(self) -> list[ResourceSnapshot]:
        return list(self._snapshots)

    def record(self, step: int) -> ResourceSnapshot:
        metrics = self._metrics_provider()
        snapshot = ResourceSnapshot(
            step=step,
            cpu_percent=float(metrics["cpu_percent"]),
            ram_percent=float(metrics["ram_percent"]),
            gpu_power_watts=self._optional_float(metrics.get("gpu_power_watts")),
            gpu_utilization_percent=self._optional_float(
                metrics.get("gpu_utilization_percent")
            ),
        )
        self._snapshots.append(snapshot)
        return snapshot

    def rolling_average(self, field_name: str, last_n: int = 5) -> float | None:
        if last_n <= 0:
            raise ValueError("last_n must be greater than zero")

        values = [
            value
            for value in (
                getattr(snapshot, field_name) for snapshot in self._snapshots[-last_n:]
            )
            if value is not None
        ]

        if not values:
            return None

        return float(mean(values))

    @staticmethod
    def _optional_float(value: float | None) -> float | None:
        if value is None:
            return None
        return float(value)
