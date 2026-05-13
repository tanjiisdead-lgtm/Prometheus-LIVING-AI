import numpy as np

def clip(n, smallest, largest):
    return max(smallest, min(n, largest))

def tanh(x):
    return np.tanh(x)

NOVELTY_DOPAMINE_SCALE = 0.5
TOLERANCE_INCREMENT = 0.05
WITHDRAWAL_THRESHOLD = 100
CRAVING_RATE = 0.01

class DopaminergicSystem:
    def __init__(self, sensitivity=1.0):
        self.dopamine_level = 0.5    # tonic baseline (always slightly present)
        self.prediction_baseline = {}  # expected value of each state type
        self.sensitivity = sensitivity
        self.tolerance = {}
        self.steps_since_last_reward = 0
        self.exploration_override = 0.0

    def compute_dopamine_signal(self, state, outcome, predicted_outcome):
        # Dopamine = reward prediction error (exactly matching neuroscience)
        RPE = outcome - predicted_outcome

        # Phasic dopamine burst: fires when outcome > prediction
        if RPE > 0:
            phasic_burst = tanh(RPE * self.sensitivity)
            self.dopamine_level = clip(self.dopamine_level + phasic_burst, 0, 1)
            self.steps_since_last_reward = 0

        # Dopamine dip: fires when outcome < prediction (disappointment)
        elif RPE < 0:
            phasic_dip = tanh(RPE * self.sensitivity)  # negative
            self.dopamine_level = clip(self.dopamine_level + phasic_dip, 0, 1)

        self.steps_since_last_reward += 1

        # Update prediction baseline (system learns what to expect)
        # Using a simple EMA
        alpha = 0.01
        self.prediction_baseline[state] = (1 - alpha) * self.prediction_baseline.get(state, 0) + alpha * outcome

        return self.dopamine_level

    def modulate_system(self, base_plasticity=0.1):
        return {
            # High dopamine: everything feels possible, exploration increases
            'exploration_rate':   0.1 + 0.4 * self.dopamine_level,

            # High dopamine: memory consolidation is stronger (good moments remembered)
            'memory_write_strength': self.dopamine_level,

            # High dopamine: faster synaptic strengthening
            'plasticity':         base_plasticity * (1 + self.dopamine_level),

            # High dopamine: goal commitment increases
            'goal_persistence':   self.dopamine_level
        }

    def compute_novelty_bonus(self, state_similarity):
        # state_similarity: 1.0 = identical, 0.0 = completely new
        novelty = 1.0 - state_similarity

        # Novel states get a dopamine bonus regardless of external reward
        # This is what makes exploration intrinsically rewarding
        novelty_dopamine = novelty * NOVELTY_DOPAMINE_SCALE

        return novelty_dopamine

    def apply_satiation(self, stimulus_type):
        # Repeated identical stimuli produce less dopamine
        self.tolerance[stimulus_type] = min(
            1.0,
            self.tolerance.get(stimulus_type, 0) + TOLERANCE_INCREMENT
        )
        effective_dopamine = self.dopamine_level * (1 - self.tolerance[stimulus_type])
        return effective_dopamine

    def apply_withdrawal(self):
        # If dopamine has been low for too long, the system experiences craving
        if self.steps_since_last_reward > WITHDRAWAL_THRESHOLD:
            craving_signal = (self.steps_since_last_reward - WITHDRAWAL_THRESHOLD) * CRAVING_RATE
            # Craving increases exploratory behavior — system searches for reward
            self.exploration_override = clip(craving_signal, 0, 1)
            print(f"CRAVING: intensity {self.exploration_override}")
            return self.exploration_override
        return 0.0
