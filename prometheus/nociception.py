import numpy as np
from .hdc import hamming_similarity

def clip(n, smallest, largest):
    return max(smallest, min(n, largest))

NOCI_INTERRUPT_THRESHOLD = 0.7
NOCI_LEARNING_MULTIPLIER = 10.0
FEAR_SCALE = 0.8

class NociceptiveAnalog:
    def __init__(self):
        self.fast_noci = 0.0    # immediate
        self.slow_noci = 0.0    # chronic
        self.anticipatory_noci = 0.0 # fear analog
        self.noci_memory = []   # (state_hv, magnitude, step)
        self.interrupt_active = False

    def register_damage(self, source, magnitude, current_state_hv=None):
        self.fast_noci = min(1.0, self.fast_noci + magnitude)
        self.slow_noci = clip(self.slow_noci + 0.1 * magnitude, 0, 1)

        if current_state_hv is not None:
            self.noci_memory.append({
                'source': source,
                'magnitude': magnitude,
                'state_hv': current_state_hv.copy() if hasattr(current_state_hv, 'copy') else current_state_hv
            })

        if self.fast_noci > NOCI_INTERRUPT_THRESHOLD:
            self.issue_cognitive_interrupt(source)

    def compute_anticipatory_signal(self, current_state_hv):
        """
        Fear analog: predicts damage from historical preceding states.
        """
        if not self.noci_memory or current_state_hv is None:
            return 0.0

        # Simplified query: find highest similarity to any state that caused damage
        max_sim = 0.0
        for entry in self.noci_memory:
            sim = hamming_similarity(current_state_hv, entry['state_hv'])
            if sim > max_sim:
                max_sim = sim

        # The signal fires BEFORE damage occurs in states historically preceding damage
        self.anticipatory_noci = clip(max_sim * FEAR_SCALE, 0, 1)
        return self.anticipatory_noci

    def issue_cognitive_interrupt(self, source):
        print(f"NOCICEPTIVE INTERRUPT: {source}")
        self.interrupt_active = True

    def modulate_all_processing(self):
        total_noci = self.fast_noci + 0.3 * self.slow_noci + 0.5 * self.anticipatory_noci

        # Decay
        self.fast_noci *= 0.5
        self.slow_noci *= 0.998

        if self.fast_noci < 0.1:
            self.interrupt_active = False

        return {
            'attention_bias':   -total_noci,
            'learning_rate':     1 + total_noci,
            'action_variance':   total_noci
        }
