import numpy as np
from scipy import sparse

class ESN:
    def __init__(self, size, spectral_radius, input_size):
        self.size = size
        self.W_res = self.init_reservoir(size, spectral_radius)
        self.W_in = np.random.randn(size, input_size) * 0.01
        self.x = np.zeros(size)

    def init_reservoir(self, size, spectral_radius):
        density = 0.02
        W = sparse.random(size, size, density=density, format='csr')
        W.data = (W.data - 0.5) * 2
        W = W.multiply(spectral_radius / np.sqrt(size * density))
        return W

    def step(self, u, affective_bias):
        res_influence = self.W_res.dot(self.x)
        in_influence = self.W_in.dot(u)
        self.x = np.tanh(res_influence + in_influence + affective_bias)
        return self.x.copy()

class HierarchicalReservoirStack:
    """
    Three reservoirs at different timescales (fast, medium, slow).
    """
    def __init__(self, input_size=10000):
        self.fast   = ESN(size=1000, spectral_radius=0.5, input_size=input_size)
        self.medium = ESN(size=2000, spectral_radius=0.9, input_size=1000) # takes fast state
        self.slow   = ESN(size=2000, spectral_radius=0.99, input_size=2000) # takes medium state

        self.pain_bias_fast = np.random.randn(1000) * 0.1
        self.pain_bias_med  = np.random.randn(2000) * 0.1
        self.pain_bias_slow = np.random.randn(2000) * 0.1

        self.novelty_bias_fast = np.random.randn(1000) * 0.1
        self.novelty_bias_med  = np.random.randn(2000) * 0.1
        self.novelty_bias_slow = np.random.randn(2000) * 0.1

    def step(self, word_hv, affective_state):
        pain = affective_state.get('pain', 0.0)
        dopamine = affective_state.get('dopamine', 0.5)

        b_fast = pain * self.pain_bias_fast + dopamine * self.novelty_bias_fast
        b_med  = pain * self.pain_bias_med  + dopamine * self.novelty_bias_med
        b_slow = pain * self.pain_bias_slow + dopamine * self.novelty_bias_slow

        fast_state   = self.fast.step(word_hv.astype(float), b_fast)
        medium_state = self.medium.step(fast_state, b_med)
        slow_state   = self.slow.step(medium_state, b_slow)

        # Concatenate all timescales — this is your context window
        return np.concatenate([fast_state, medium_state, slow_state])

    def reset_state(self):
        self.fast.x.fill(0)
        self.medium.x.fill(0)
        self.slow.x.fill(0)
