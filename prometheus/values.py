import numpy as np
from dataclasses import dataclass

CONSISTENCY_THRESHOLD = 0.7

@dataclass
class Principle:
    statement: str
    strength: float
    polarity: str

class ExperienceCrystallizedValues:
    def __init__(self):
        self.proto_values = {}     # raw experience associations
        self.crystallized = {}     # stable principles (slow to change)
        self.crystallization_threshold = 10  # experiences before crystallization (reduced for demo)

    def record_experience(self, action_type, context, outcome_valence):
        # Every experience contributes to proto-values
        # Using a simple string representation of context for now
        key = (action_type, str(context))

        if key not in self.proto_values:
            self.proto_values[key] = []
        self.proto_values[key].append(outcome_valence)

        # When enough evidence accumulates, crystallize into a principle
        if len(self.proto_values[key]) >= self.crystallization_threshold:
            self.crystallize(key)

    def crystallize(self, key):
        experiences = self.proto_values[key]
        mean_valence = np.mean(experiences)
        consistency  = 1 - np.std(experiences)  # more consistent = stronger principle

        if consistency > CONSISTENCY_THRESHOLD:
            action_type, context = key
            if mean_valence > 0.3:
                self.crystallized[key] = Principle(
                    statement=f"In context {context}, {action_type} tends to lead to flourishing",
                    strength=mean_valence * consistency,
                    polarity='positive'
                )
                print(f"NEW PRINCIPLE: {self.crystallized[key].statement}")
            elif mean_valence < -0.3:
                self.crystallized[key] = Principle(
                    statement=f"In context {context}, {action_type} leads to suffering — avoid",
                    strength=abs(mean_valence) * consistency,
                    polarity='negative'
                )
                print(f"NEW PRINCIPLE: {self.crystallized[key].statement}")
