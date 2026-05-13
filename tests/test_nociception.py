import unittest
import numpy as np
from prometheus.nociception import NociceptiveAnalog
from prometheus.hdc import random_hv

class TestNociception(unittest.TestCase):
    def test_anticipatory_signal(self):
        nis = NociceptiveAnalog()
        hv1 = random_hv(1000)

        # Experience damage in state 1
        nis.register_damage("source", 0.5, current_state_hv=hv1)

        # Now we are in a similar state, we should feel fear
        fear = nis.compute_anticipatory_signal(hv1)
        self.assertGreater(fear, 0.0)

        # In a different state, fear should be lower (or 0)
        hv2 = random_hv(1000)
        fear2 = nis.compute_anticipatory_signal(hv2)
        self.assertLess(fear2, fear)

if __name__ == '__main__':
    unittest.main()
