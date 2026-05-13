import unittest
from prometheus.dopamine import DopaminergicSystem

class TestDopamine(unittest.TestCase):
    def test_rpe_positive(self):
        dpes = DopaminergicSystem()
        initial_dopamine = dpes.dopamine_level
        # Outcome better than predicted
        dpes.compute_dopamine_signal("state1", 1.0, 0.5)
        self.assertGreater(dpes.dopamine_level, initial_dopamine)

    def test_rpe_negative(self):
        dpes = DopaminergicSystem()
        initial_dopamine = dpes.dopamine_level
        # Outcome worse than predicted
        dpes.compute_dopamine_signal("state1", 0.0, 0.5)
        self.assertLess(dpes.dopamine_level, initial_dopamine)

    def test_novelty_bonus(self):
        dpes = DopaminergicSystem()
        bonus = dpes.compute_novelty_bonus(0.2) # similarity 0.2 means high novelty
        self.assertEqual(bonus, 0.8 * 0.5)

    def test_withdrawal(self):
        dpes = DopaminergicSystem()
        dpes.steps_since_last_reward = 150
        craving = dpes.apply_withdrawal()
        self.assertGreater(craving, 0.0)

if __name__ == '__main__':
    unittest.main()
