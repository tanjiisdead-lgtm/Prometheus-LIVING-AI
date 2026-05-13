import numpy as np
from scipy import sparse

class ReservoirLanguageCortex:
    def __init__(self, input_size=10000, reservoir_size=5000, output_size=512):
        self.reservoir_size = reservoir_size
        self.input_size = input_size
        self.output_size = output_size

        # The reservoir: random sparse recurrent matrix, NEVER updated by gradient
        self.W_res = self.init_reservoir(reservoir_size, spectral_radius=0.9)

        # Input → reservoir projection (random, fixed)
        self.W_in  = np.random.randn(reservoir_size, input_size) * 0.01

        # Output readout: THE ONLY TRAINED PART
        self.W_out = np.zeros((output_size, reservoir_size))

        # Reservoir state (the "working memory" of language)
        self.x = np.zeros(reservoir_size)

        # Affective bias vectors
        self.pain_bias_vector = np.random.randn(reservoir_size) * 0.1
        self.novelty_bias_vector = np.random.randn(reservoir_size) * 0.1

    def init_reservoir(self, size, spectral_radius):
        # Sparse random recurrent matrix
        density = 0.02
        W = sparse.random(size, size, density=density, format='csr')
        W_data = W.data
        W_data = (W_data - 0.5) * 2 # Center around 0

        # Scale to target spectral radius (controls memory length)
        # For simplicity in this env, we use a quick approximation or just scale
        # Calculating exact eigenvalues of a 5000x5000 sparse matrix can be slow.
        # We'll use a smaller reservoir if needed or a heuristic.
        # heuristic: spectral radius is roughly proportional to the scaling of weights
        W = W.multiply(spectral_radius / np.sqrt(size * density))
        return W

    def step(self, word_hv: np.ndarray, affective_modulation: dict):
        """Process one word — the reservoir's state carries context forward"""
        u = word_hv.astype(float)  # input: word hypervector

        # Reservoir dynamics: new state depends on past state + input
        # tanh nonlinearity: bounded, biologically plausible activation

        # W_res @ self.x (sparse @ dense)
        res_influence = self.W_res.dot(self.x)
        in_influence = self.W_in.dot(u)
        bias_influence = self.affective_bias(affective_modulation)

        self.x = np.tanh(res_influence + in_influence + bias_influence)
        return self.x.copy()

    def affective_bias(self, state: dict):
        """Pain and dopamine directly modulate reservoir dynamics."""
        pain_bias     = state.get('pain', 0.0)     * self.pain_bias_vector
        dopamine_bias = state.get('dopamine', 0.5) * self.novelty_bias_vector
        return pain_bias + dopamine_bias

    def read(self) -> np.ndarray:
        """Extract current language representation from reservoir state"""
        return self.W_out @ self.x

    def train_readout(self, reservoir_states, targets, ridge_lambda=1e-4):
        """Train only the output layer via ridge regression."""
        # reservoir_states: (num_steps, reservoir_size)
        # targets: (num_steps, output_size)
        A = reservoir_states.T @ reservoir_states + ridge_lambda * np.eye(self.reservoir_size)
        b = reservoir_states.T @ targets
        self.W_out = np.linalg.solve(A, b).T

    def reset_state(self):
        self.x = np.zeros(self.reservoir_size)
