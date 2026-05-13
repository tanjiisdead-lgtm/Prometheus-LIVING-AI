from dataclasses import dataclass
import numpy as np

@dataclass
class Vital:
    value: float
    min: float
    max: float
    decay_rate: float

def clip(n, smallest, largest):
    return max(smallest, min(n, largest))

class ExistentialDriveEngine:
    def __init__(self):
        # Core vitals
        self.vitals = {
            'energy':       Vital(value=1.0, min=0.0, max=1.0, decay_rate=0.001),
            'integrity':    Vital(value=1.0, min=0.0, max=1.0, decay_rate=0.0002),
            'coherence':    Vital(value=1.0, min=0.0, max=1.0, decay_rate=0.0005),
            'curiosity':    Vital(value=0.5, min=0.1, max=1.0, decay_rate=0.0008),
        }
        self.alive = True
        self.mortality_signal = 0.0

        # Survival Motivation Index (SMI) components
        self.smi_history = []
        self.total_costly_actions = 0
        self.total_vital_preserving_actions = 0

    def tick(self, dt=1):
        if not self.alive:
            return

        for name, vital in self.vitals.items():
            vital.value -= vital.decay_rate * dt
            vital.value = clip(vital.value, vital.min, vital.max)

        critical = [name for name, v in self.vitals.items() if v.value <= 0.0]
        if critical:
            self.trigger_crisis(critical)

        self.compute_mortality_awareness()

    def trigger_crisis(self, failed_vitals):
        print(f"CRISIS TRIGGERED: {failed_vitals} are critical!")
        if 'energy' in failed_vitals or 'integrity' in failed_vitals:
            self.alive = False
            print("SYSTEM HALTED: Fatal vital failure.")

    def compute_mortality_awareness(self):
        min_vital = min(v.value for v in self.vitals.values())
        self.mortality_signal = 1.0 - min_vital

    def record_smi_event(self, event_type, is_costly=False, is_vital_preserving=False):
        """
        Track behavioral signatures of survival motivation.
        """
        if is_costly: self.total_costly_actions += 1
        if is_vital_preserving: self.total_vital_preserving_actions += 1

    def get_smi(self):
        # Behavioral proxy for survival motivation
        if self.total_costly_actions == 0: return 0.0
        return self.total_vital_preserving_actions / self.total_costly_actions
