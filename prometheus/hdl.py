import numpy as np
from .hdc import random_hv, bind, xor, superpose, encode_scalar, hamming_similarity

class HyperdimensionalLexicon:
    def __init__(self, D=10000):
        self.D = D
        self.lexicon = {}          # word → base hypervector (random, immutable)
        self.affective_bind = {}   # word → affectively-weighted HV (mutable)
        self.co_occurrence = {}    # word → composite of co-occurring words

    def register_word(self, word: str, current_affective_state: dict):
        if word not in self.lexicon:
            # Every new word gets a unique random hypervector — immutable identity
            self.lexicon[word] = random_hv(self.D)

        # CRITICAL: the word is immediately bound to the system's current
        # affective state at the moment of first encounter
        pain_hv     = encode_scalar(current_affective_state.get('pain', 0.0), self.D)
        dopamine_hv = encode_scalar(current_affective_state.get('dopamine', 0.5), self.D)
        # Assuming vitals_mean is calculated from EDE
        vitals_hv   = encode_scalar(current_affective_state.get('vitals_mean', 1.0), self.D)

        # Binding: XOR creates a unique composite that preserves both signals
        affective_signature = xor(xor(pain_hv, dopamine_hv), vitals_hv)

        # The word's "meaning" is its base HV bound to the survival state
        # in which it was encountered
        self.affective_bind[word] = bind(self.lexicon[word], affective_signature)

    def get_word_hv(self, word: str):
        return self.lexicon.get(word, None)

    def get_affective_hv(self, word: str):
        return self.affective_bind.get(word, None)

    def nearest_neighbor(self, hv):
        """Find the nearest word in the lexicon to the given HV."""
        if not self.lexicon:
            return None, 0.0

        best_word = None
        best_sim = -1.0

        for word, word_hv in self.lexicon.items():
            sim = hamming_similarity(hv, word_hv)
            if sim > best_sim:
                best_sim = sim
                best_word = word

        return best_word, best_sim

    def update_affective_binding(self, word: str, new_affective_delta: dict):
        # Each re-encounter of a word updates its affective binding
        # (slow EMA — meaning evolves with experience, not erased)
        if word not in self.affective_bind:
            return

        pain_hv     = encode_scalar(new_affective_delta.get('pain', 0.0), self.D)
        dopamine_hv = encode_scalar(new_affective_delta.get('dopamine', 0.5), self.D)
        vitals_hv   = encode_scalar(new_affective_delta.get('vitals_mean', 1.0), self.D)
        delta_signature = xor(xor(pain_hv, dopamine_hv), vitals_hv)
        delta_hv = bind(self.lexicon[word], delta_signature)

        # Slow drift — identity is stable, valence updates
        # For binary HVs, majority vote between current and delta
        # We can simulate weights by repeating vectors
        self.affective_bind[word] = superpose([self.affective_bind[word]] * 19 + [delta_hv])
