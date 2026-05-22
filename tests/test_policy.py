import unittest

from greengrad import EnergyBudgetPolicy, ResourceSnapshot


class TestEnergyBudgetPolicy(unittest.TestCase):
    def test_is_within_budget_true(self):
        policy = EnergyBudgetPolicy(max_power_watts=200)
        snapshot = ResourceSnapshot(step=1, cpu_percent=30, ram_percent=40, gpu_power_watts=180)
        self.assertTrue(policy.is_within_budget(snapshot))

    def test_is_within_budget_false(self):
        policy = EnergyBudgetPolicy(max_power_watts=150)
        snapshot = ResourceSnapshot(step=1, cpu_percent=30, ram_percent=40, gpu_power_watts=180)
        self.assertFalse(policy.is_within_budget(snapshot))


if __name__ == "__main__":
    unittest.main()
