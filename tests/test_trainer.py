import unittest

from greengrad import EnergyBudgetPolicy, ResourceTracker, SustainableTrainer


class TestSustainableTrainer(unittest.TestCase):
    def test_run_collects_outputs(self):
        tracker = ResourceTracker(
            metrics_provider=lambda: {
                "cpu_percent": 35,
                "ram_percent": 55,
                "gpu_power_watts": 120,
                "gpu_utilization_percent": 70,
            }
        )
        trainer = SustainableTrainer(
            tracker=tracker,
            policy=EnergyBudgetPolicy(max_power_watts=200),
        )

        outputs = trainer.run(
            steps=3,
            step_fn=lambda step, snapshot: (step, snapshot.cpu_percent),
        )

        self.assertEqual(outputs, [(1, 35.0), (2, 35.0), (3, 35.0)])
        self.assertEqual(len(tracker.snapshots), 3)

    def test_budget_exceeded_callback(self):
        tracker = ResourceTracker(
            metrics_provider=lambda: {
                "cpu_percent": 35,
                "ram_percent": 55,
                "gpu_power_watts": 250,
                "gpu_utilization_percent": 70,
            }
        )
        trainer = SustainableTrainer(
            tracker=tracker,
            policy=EnergyBudgetPolicy(max_power_watts=200),
        )

        exceeded_steps: list[int] = []
        trainer.run(
            steps=2,
            step_fn=lambda step, snapshot: step,
            on_budget_exceeded=lambda step, snapshot: exceeded_steps.append(step),
        )

        self.assertEqual(exceeded_steps, [1, 2])


if __name__ == "__main__":
    unittest.main()
