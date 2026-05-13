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
        # Core vitals — must stay in viable range
        self.vitals = {
            'energy':       Vital(value=1.0, min=0.0, max=1.0, decay_rate=0.001),
            'integrity':    Vital(value=1.0, min=0.0, max=1.0, decay_rate=0.0002),
            'coherence':    Vital(value=1.0, min=0.0, max=1.0, decay_rate=0.0005),
            'curiosity':    Vital(value=0.5, min=0.1, max=1.0, decay_rate=0.0008),
        }
        self.alive = True
        self.mortality_signal = 0.0

    def tick(self, dt=1):
        if not self.alive:
            return

        for name, vital in self.vitals.items():
            vital.value -= vital.decay_rate * dt  # vitals decay naturally
            vital.value = clip(vital.value, vital.min, vital.max)

        # DEATH CONDITION: if any vital hits zero, system enters crisis
        # Note: curiosity has a min of 0.1, so it won't hit 0.0 unless modified
        critical = [name for name, v in self.vitals.items() if v.value <= 0.0]
        if critical:
            self.trigger_crisis(critical)

        self.compute_mortality_awareness()

    def trigger_crisis(self, failed_vitals):
        # This is PAIN at its rawest — existential threat
        # System drops ALL other goals and focuses entirely on survival
        print(f"CRISIS TRIGGERED: {failed_vitals} are critical!")
        self.override_all_goals(priority='SURVIVE')
        self.broadcast_pain_signal(intensity=1.0)

        # In this implementation, let's say if energy or integrity hits 0, it dies
        if 'energy' in failed_vitals or 'integrity' in failed_vitals:
            self.alive = False
            print("SYSTEM HALTED: Fatal vital failure.")

    def override_all_goals(self, priority):
        # Placeholder for goal management integration
        pass

    def broadcast_pain_signal(self, intensity):
        # Placeholder for NIS integration
        pass

    def compute_mortality_awareness(self):
        # System always knows how close it is to critical failure
        min_vital = min(v.value for v in self.vitals.values())

        self.mortality_signal = 1.0 - min_vital  # 0 = fully healthy, 1 = about to die

        # This signal is permanently visible to all subsystems
        # The system always knows how alive it is
        # self.broadcast_to_workspace('mortality_awareness', self.mortality_signal)
