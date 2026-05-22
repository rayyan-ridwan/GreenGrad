import unittest

from greengrad import ResourceSnapshot, generate_markdown_report


class TestReport(unittest.TestCase):
    def test_generate_markdown_report(self):
        snapshots = [
            ResourceSnapshot(step=1, cpu_percent=30, ram_percent=40, gpu_power_watts=100),
            ResourceSnapshot(step=2, cpu_percent=50, ram_percent=60, gpu_power_watts=140),
        ]

        report = generate_markdown_report(snapshots)

        self.assertIn("Steps recorded: **2**", report)
        self.assertIn("Average CPU usage: **40.00%**", report)
        self.assertIn("Average RAM usage: **50.00%**", report)
        self.assertIn("Average GPU power: **120.00 W**", report)

    def test_generate_empty_report(self):
        report = generate_markdown_report([])
        self.assertIn("No snapshots recorded.", report)


if __name__ == "__main__":
    unittest.main()
