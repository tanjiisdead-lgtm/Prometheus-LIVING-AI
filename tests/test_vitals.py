import unittest
from prometheus.vitals import ExistentialDriveEngine, Vital

class TestVitals(unittest.TestCase):
    def test_vital_decay(self):
        ede = ExistentialDriveEngine()
        initial_energy = ede.vitals['energy'].value
        ede.tick(dt=10)
        decayed_energy = ede.vitals['energy'].value
        self.assertLess(decayed_energy, initial_energy)
        self.assertAlmostEqual(decayed_energy, initial_energy - 0.001 * 10)

    def test_death_condition(self):
        ede = ExistentialDriveEngine()
        # Force energy to zero
        ede.vitals['energy'].value = 0.0
        ede.tick(dt=1)
        self.assertFalse(ede.alive)

    def test_mortality_awareness(self):
        ede = ExistentialDriveEngine()
        ede.vitals['energy'].value = 0.5
        ede.tick(dt=0) # Update awareness
        self.assertEqual(ede.mortality_signal, 0.5)

        ede.vitals['energy'].value = 0.1
        ede.tick(dt=0)
        self.assertEqual(ede.mortality_signal, 0.9)

if __name__ == '__main__':
    unittest.main()
