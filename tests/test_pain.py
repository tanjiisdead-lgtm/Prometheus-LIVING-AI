import unittest
from prometheus.pain import NociceptiveInterruptSystem

class TestPain(unittest.TestCase):
    def test_pain_accumulation(self):
        nis = NociceptiveInterruptSystem()
        nis.register_damage("test_source", 0.5)
        self.assertEqual(nis.fast_pain, 0.5)
        self.assertGreater(nis.slow_pain, 0.0)

    def test_pain_interrupt(self):
        nis = NociceptiveInterruptSystem()
        nis.register_damage("heavy_damage", 0.8)
        self.assertTrue(nis.interrupt_active)

    def test_pain_modulation(self):
        nis = NociceptiveInterruptSystem()
        nis.register_damage("test", 0.5)
        modulation = nis.modulate_all_processing()
        self.assertIn('attention_bias', modulation)
        self.assertLess(modulation['attention_bias'], 0.0)
        self.assertGreater(modulation['learning_rate'], 1.0)

if __name__ == '__main__':
    unittest.main()
