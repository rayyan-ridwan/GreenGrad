"""Trainer orchestration for sustainability-aware runs."""

from __future__ import annotations

from typing import Callable

from .policy import EnergyBudgetPolicy
from .tracker import ResourceSnapshot, ResourceTracker


class SustainableTrainer:
    """Runs a training loop with optional policy checks."""

    def __init__(self, tracker: ResourceTracker, policy: EnergyBudgetPolicy):
        self._tracker = tracker
        self._policy = policy

    def run(
        self,
        steps: int,
        step_fn: Callable[[int, ResourceSnapshot], object],
        on_budget_exceeded: Callable[[int, ResourceSnapshot], None] | None = None,
    ) -> list[object]:
        if steps <= 0:
            raise ValueError("steps must be greater than zero")

        outputs: list[object] = []
        for step in range(1, steps + 1):
            snapshot = self._tracker.record(step=step)
            if not self._policy.is_within_budget(snapshot) and on_budget_exceeded:
                on_budget_exceeded(step, snapshot)

            outputs.append(step_fn(step, snapshot))

        return outputs
