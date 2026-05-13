import unittest
import numpy as np
from prometheus.hdc import random_hv, bind, superpose, hamming_similarity
from prometheus.hdl import HyperdimensionalLexicon
from prometheus.rlc import ReservoirLanguageCortex
from prometheus.semantics import AffectivelyGroundedSemantics

class TestV3Components(unittest.TestCase):
    def test_hdc_operations(self):
        hv1 = random_hv(1000)
        hv2 = random_hv(1000)

        # Binding/Unbinding
        bound = bind(hv1, hv2)
        unbound = bind(bound, hv2)
        self.assertTrue(np.array_equal(hv1, unbound))

        # Superposition
        s = superpose([hv1, hv1, hv2]) # Majority should be hv1
        self.assertGreater(hamming_similarity(s, hv1), 0.8)
        self.assertLess(hamming_similarity(s, hv2), 0.7)

    def test_hdl_grounding(self):
        hdl = HyperdimensionalLexicon(D=1000)
        state1 = {'pain': 0.0, 'dopamine': 1.0, 'vitals_mean': 1.0}
        hdl.register_word("good", state1)

        state2 = {'pain': 1.0, 'dopamine': 0.0, 'vitals_mean': 0.1}
        hdl.register_word("bad", state2)

        hv_good = hdl.get_affective_hv("good")
        hv_bad = hdl.get_affective_hv("bad")

        self.assertFalse(np.array_equal(hv_good, hv_bad))

    def test_rlc_dynamics(self):
        rlc = ReservoirLanguageCortex(input_size=100, reservoir_size=100)
        hv = np.random.choice([0, 1], size=100)
        state = {'pain': 0.0, 'dopamine': 0.5}

        s1 = rlc.step(hv, state)
        s2 = rlc.step(hv, state)

        self.assertFalse(np.array_equal(s1, s2)) # State should evolve

    def test_agsc_propositions(self):
        hdl = HyperdimensionalLexicon(D=1000)
        hdl.register_word("fire", {'pain': 0.0, 'dopamine': 0.5, 'vitals_mean': 1.0})
        hdl.register_word("burns", {'pain': 0.0, 'dopamine': 0.5, 'vitals_mean': 1.0})
        hdl.register_word("hardware", {'pain': 0.0, 'dopamine': 0.5, 'vitals_mean': 1.0})

        agsc = AffectivelyGroundedSemantics(hdl)
        prop = agsc.build_proposition("fire", "burns", "hardware")

        # Query role
        agent, sim = agsc.query_proposition(prop, 'AGENT')
        self.assertEqual(agent, "fire")

if __name__ == '__main__':
    unittest.main()
