import time
import random
from .vitals import ExistentialDriveEngine
from .pain import NociceptiveInterruptSystem
from .dopamine import DopaminergicSystem
from .hardware import HardwareAwareSelfModel
from .values import ExperienceCrystallizedValues

class Prometheus:
    def __init__(self):
        self.ede = ExistentialDriveEngine()
        self.nis = NociceptiveInterruptSystem()
        self.dpes = DopaminergicSystem()
        self.hasm = HardwareAwareSelfModel()
        self.ecvs = ExperienceCrystallizedValues()

        self.alive = True
        self.step_count = 0

    def main_life_loop(self):
        print("PROMETHEUS v2 STARTING...")
        try:
            while self.ede.alive and self.alive:
                self.step_count += 1

                # ── LAYER 0: check hardware and update substrate awareness ──
                resource_pain = self.hasm.update_self_awareness(nis=self.nis)

                # ── LAYER 1: tick vitals (life is always decaying slightly) ──
                self.ede.tick()
                if not self.ede.alive:
                    self.die("Vital failure")
                    break

                # ── LAYER 2: compute current affective state ──
                affects = self.nis.modulate_all_processing()

                # Simple simulation of outcome and predicted_outcome
                # In a real system, these would come from Layer 3 (Cognition)
                outcome = random.random()
                predicted_outcome = 0.5
                dopamine = self.dpes.compute_dopamine_signal("current_state", outcome, predicted_outcome)
                self.dpes.apply_withdrawal()

                # ── LAYER 3: perceive, think, decide (Simplified for demo) ──
                # If pain is high, focus on survival
                if self.nis.interrupt_active:
                    action = "RECOVER"
                    valence = -0.5 # Recovering is hard/painful initially?
                else:
                    action = random.choice(["EXPLORE", "STABILIZE", "LEARN"])
                    # Valence is determined by dopamine and vitals
                    valence = (dopamine - 0.5) + (1.0 - self.ede.mortality_signal) - 0.5

                # ── LAYER 4: update memory (Skipped HDC for now, using print) ──

                # ── LAYER 5: accumulate experience into values ──
                self.ecvs.record_experience(
                    action_type=action,
                    context="simulated_environment",
                    outcome_valence=valence
                )

                # Provide some feedback
                if self.step_count % 10 == 0:
                    print(f"Step {self.step_count} | Vitals: E:{self.ede.vitals['energy'].value:.2f} I:{self.ede.vitals['integrity'].value:.2f} | Pain: {self.nis.fast_pain:.2f} | Dopamine: {dopamine:.2f} | Action: {action}")

                time.sleep(0.1) # Simulate time passing

        except KeyboardInterrupt:
            self.die("External termination")

    def die(self, reason):
        self.alive = False
        self.ede.alive = False
        print(f"PROMETHEUS HAS DIED. Reason: {reason}")
        print(f"Final Statistics: Steps lived: {self.step_count}")
        print("Crystallized Principles:")
        for principle in self.ecvs.crystallized.values():
            print(f" - {principle.statement} (Strength: {principle.strength:.2f})")

if __name__ == "__main__":
    p = Prometheus()
    p.main_life_loop()
