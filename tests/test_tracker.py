import unittest

from greengrad import ResourceTracker


class TestResourceTracker(unittest.TestCase):
    def test_record_creates_snapshot(self):
        tracker = ResourceTracker(
            metrics_provider=lambda: {
                "cpu_percent": 25,
                "ram_percent": 40,
                "gpu_power_watts": 110,
                "gpu_utilization_percent": 60,
            }
        )

        snapshot = tracker.record(step=1)

        self.assertEqual(snapshot.step, 1)
        self.assertEqual(snapshot.cpu_percent, 25.0)
        self.assertEqual(snapshot.ram_percent, 40.0)
        self.assertEqual(snapshot.gpu_power_watts, 110.0)

    def test_rolling_average(self):
        values = iter([10, 20, 30, 40])
        tracker = ResourceTracker(
            metrics_provider=lambda: {
                "cpu_percent": next(values),
                "ram_percent": 50,
                "gpu_power_watts": None,
                "gpu_utilization_percent": None,
            }
        )

        for step in range(1, 5):
            tracker.record(step)

        self.assertEqual(tracker.rolling_average("cpu_percent", last_n=2), 35.0)


if __name__ == "__main__":
    unittest.main()
