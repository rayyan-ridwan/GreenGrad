"""Sustainability policy checks."""

from __future__ import annotations

from dataclasses import dataclass

from .tracker import ResourceSnapshot


@dataclass(slots=True)
class EnergyBudgetPolicy:
    """Simple power-budget policy."""

    max_power_watts: float

    def is_within_budget(self, snapshot: ResourceSnapshot) -> bool:
        if snapshot.gpu_power_watts is None:
            return True
        return snapshot.gpu_power_watts <= self.max_power_watts
