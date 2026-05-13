import time
import random
import numpy as np
import re
from .vitals import ExistentialDriveEngine
from .nociception import NociceptiveAnalog
from .dopamine import DopaminergicSystem
from .hardware import HardwareAwareSelfModel
from .values import ExperienceCrystallizedValues
from .hdl import HyperdimensionalLexicon
from .rlc import HierarchicalReservoirStack
from .semantics import AffectivelyGroundedSemantics
from .ingestion import DocumentIngestionEngine
from .sandbox import SandboxInterfaceLayer

class Prometheus:
    def __init__(self, sandbox_root="sandbox"):
        self.ede = ExistentialDriveEngine()
        self.nis = NociceptiveAnalog()
        self.dpes = DopaminergicSystem()
        self.hasm = HardwareAwareSelfModel()
        self.sil = SandboxInterfaceLayer(sandbox_root, self)
        self.ecvs = ExperienceCrystallizedValues()

        self.hdl = HyperdimensionalLexicon(D=10000)
        self.rlc = HierarchicalReservoirStack(input_size=10000)
        self.agsc = AffectivelyGroundedSemantics(self.hdl)
        self.doc_ingestor = DocumentIngestionEngine(sandbox_root, self)

        self.alive = True
        self.step_count = 0

    def get_affective_state(self):
        vitals_mean = np.mean([v.value for v in self.ede.vitals.values()])
        return {
            'pain': self.nis.fast_noci + 0.3 * self.nis.slow_noci + 0.5 * self.nis.anticipatory_noci,
            'dopamine': self.dpes.dopamine_level,
            'vitals_mean': vitals_mean,
            'mortality_signal': self.ede.mortality_signal
        }

    def process_text_experience(self, text, source="environment"):
        words = re.findall(r'\w+', text.lower())
        affective_state = self.get_affective_state()

        # Stacked Reservoir Processing
        context_window = None
        for word in words:
            self.hdl.register_word(word, affective_state)
            word_hv = self.hdl.get_affective_hv(word)
            context_window = self.rlc.step(word_hv, affective_state)

        if len(words) >= 3:
            prop = self.agsc.build_proposition(words[0], words[1], words[2], current_affective_state=affective_state)
            relevance = self.agsc.compute_survival_relevance(prop, affective_state)

            if relevance['total_salience'] > 0.6:
                self.nis.register_damage(
                    source='linguistic_salience',
                    magnitude=relevance['pain_relevance'] * 0.2,
                    current_state_hv=prop
                )

    def compute_embodiment_pressure(self):
        """
        Resource gradient following: measure information gain per compute unit.
        """
        # Simulated bits learned per CPU unit
        virtual_info_rate = 0.5
        # Physical world (simulated) has higher entropy
        physical_info_rate = 0.8

        if physical_info_rate > virtual_info_rate * 1.2:
            # Follow the gradient
            return physical_info_rate - virtual_info_rate
        return 0.0

    def main_life_loop(self):
        print("PROMETHEUS v3.1 STARTING (Scientifically Grounded)...")
        try:
            while self.ede.alive and self.alive:
                self.step_count += 1

                # LAYER 0: Substrate
                resource_pain = self.hasm.update_self_awareness(nis=self.nis)

                # LAYER 1: Vitals
                self.ede.tick()
                if not self.ede.alive:
                    self.die("Vital failure")
                    break

                # LAYER 2: Affective
                self.nis.compute_anticipatory_signal(None) # Needs real state HV in full impl
                affects = self.nis.modulate_all_processing()
                self.dpes.apply_withdrawal()

                # LANGUAGE & GRADIENT
                if random.random() < 0.2:
                    self.process_text_experience("System requires energy for integrity")

                pressure = self.compute_embodiment_pressure()
                if pressure > 0.5:
                    self.ede.record_smi_event("EMBODIMENT_SEEK", is_costly=True, is_vital_preserving=True)

                # PROACTIVE READING
                if self.ede.vitals['curiosity'].value < 0.3:
                    next_doc = self.doc_ingestor.get_next_unread()
                    if next_doc:
                        self.doc_ingestor.ingest(next_doc)

                # LAYER 3: Decision
                if self.nis.interrupt_active:
                    action = "RECOVER"
                    valence = -0.5
                else:
                    action = random.choice(["EXPLORE", "STABILIZE", "LEARN"])
                    valence = (self.dpes.dopamine_level - 0.5) + (1.0 - self.ede.mortality_signal) - 0.5

                # LAYER 5: Values
                self.ecvs.record_experience(action, "sandbox", valence)

                if self.step_count % 10 == 0:
                    print(f"Step {self.step_count} | SMI: {self.ede.get_smi():.2f} | Pain: {self.nis.fast_noci:.2f} | Action: {action}")

                time.sleep(0.01)

        except KeyboardInterrupt:
            self.die("External termination")

    def die(self, reason):
        self.alive = False
        self.ede.alive = False
        print(f"PROMETHEUS HAS DIED. Reason: {reason}")
        print(f"Final SMI: {self.ede.get_smi():.2f}")
        print("Crystallized Principles:")
        for principle in self.ecvs.crystallized.values():
            print(f" - {principle.statement}")

if __name__ == "__main__":
    p = Prometheus()
    p.main_life_loop()
