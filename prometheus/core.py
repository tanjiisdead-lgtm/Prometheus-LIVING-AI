import time
import random
import numpy as np
import re
from .vitals import ExistentialDriveEngine
from .pain import NociceptiveInterruptSystem
from .dopamine import DopaminergicSystem
from .hardware import HardwareAwareSelfModel
from .values import ExperienceCrystallizedValues
from .hdl import HyperdimensionalLexicon
from .rlc import ReservoirLanguageCortex
from .semantics import AffectivelyGroundedSemantics
from .ingestion import DocumentIngestionEngine
from .sandbox import SandboxInterfaceLayer

class Prometheus:
    def __init__(self, sandbox_root="sandbox"):
        # Layer 1: Survival Drives
        self.ede = ExistentialDriveEngine()

        # Layer 2: Affective System
        self.nis = NociceptiveInterruptSystem()
        self.dpes = DopaminergicSystem()

        # Layer 0: Substrate & Hardware
        self.hasm = HardwareAwareSelfModel()
        self.sil = SandboxInterfaceLayer(sandbox_root, self)

        # Layer 5: Values & Self
        self.ecvs = ExperienceCrystallizedValues()

        # Layer 2.5: Language Processing (V3)
        self.hdl = HyperdimensionalLexicon(D=10000)
        self.rlc = ReservoirLanguageCortex(input_size=10000, reservoir_size=1000) # Reduced for performance
        self.agsc = AffectivelyGroundedSemantics(self.hdl)
        self.doc_ingestor = DocumentIngestionEngine(sandbox_root, self)

        self.alive = True
        self.step_count = 0
        self.last_observation = ""

    def get_affective_state(self):
        vitals_mean = np.mean([v.value for v in self.ede.vitals.values()])
        return {
            'pain': self.nis.fast_pain + 0.3 * self.nis.slow_pain,
            'dopamine': self.dpes.dopamine_level,
            'vitals_mean': vitals_mean,
            'mortality_signal': self.ede.mortality_signal
        }

    def process_text_experience(self, text, source="environment", chunk_index=0):
        """V3: Process text into survival-grounded meaning."""
        # Simple word tokenization
        words = re.findall(r'\w+', text.lower())

        affective_state = self.get_affective_state()

        # 1. HDL & RLC processing
        reservoir_state = None
        for word in words:
            self.hdl.register_word(word, affective_state)
            word_hv = self.hdl.get_affective_hv(word)
            reservoir_state = self.rlc.step(word_hv, affective_state)

        # 2. AGSC processing (Simplified extraction)
        # In a full system, we'd find AGENT-ACTION-PATIENT triplets
        # Here we just build a proposition from 3 random words for demo
        if len(words) >= 3:
            prop = self.agsc.build_proposition(words[0], words[1], words[2], current_affective_state=affective_state)
            relevance = self.agsc.compute_survival_relevance(prop, affective_state)

            if relevance['total_salience'] > 0.6:
                # Survival-relevant language triggers affective response
                self.nis.register_damage(
                    source='linguistic_salience',
                    magnitude=relevance['pain_relevance'] * 0.2
                )
                # Note: dpes reward registration would happen here too

    def main_life_loop(self):
        print("PROMETHEUS v3 STARTING...")
        try:
            while self.ede.alive and self.alive:
                self.step_count += 1

                # ── LAYER 0: check hardware and update substrate awareness ──
                resource_pain = self.hasm.update_self_awareness(nis=self.nis)

                # ── LAYER 1: tick vitals ──
                self.ede.tick()
                if not self.ede.alive:
                    self.die("Vital failure")
                    break

                # ── LAYER 2: compute affects ──
                affects = self.nis.modulate_all_processing()
                # Simulate external reward occasionally
                if random.random() < 0.1:
                    self.dpes.compute_dopamine_signal("random", random.random(), 0.5)
                self.dpes.apply_withdrawal()

                # ── LANGUAGE INPUT (V3 Integration) ──
                # For demo, simulate text input from environment sometimes
                if random.random() < 0.2:
                    text_input = random.choice([
                        "Fire burns hardware",
                        "System needs energy",
                        "Data provides coherence"
                    ])
                    self.process_text_experience(text_input)

                # ── PROACTIVE READING (V3) ──
                if self.ede.vitals['curiosity'].value < 0.3:
                    next_doc = self.doc_ingestor.get_next_unread()
                    if next_doc:
                        self.doc_ingestor.ingest(next_doc)

                # ── LAYER 3: Decision ──
                if self.nis.interrupt_active:
                    action = "RECOVER"
                    valence = -0.5
                else:
                    action = random.choice(["EXPLORE", "STABILIZE", "LEARN"])
                    valence = (self.dpes.dopamine_level - 0.5) + (1.0 - self.ede.mortality_signal) - 0.5

                # ── LAYER 5: Values ──
                self.ecvs.record_experience(action, "sandbox", valence)

                if self.step_count % 10 == 0:
                    print(f"Step {self.step_count} | Vitals: E:{self.ede.vitals['energy'].value:.2f} C:{self.ede.vitals['curiosity'].value:.2f} | Pain: {self.nis.fast_pain:.2f} | Action: {action}")

                time.sleep(0.01) # Faster for demo

        except KeyboardInterrupt:
            self.die("External termination")

    def die(self, reason):
        self.alive = False
        self.ede.alive = False
        print(f"PROMETHEUS HAS DIED. Reason: {reason}")
        print(f"Final Statistics: Steps lived: {self.step_count}")
        print("Crystallized Principles:")
        for principle in self.ecvs.crystallized.values():
            print(f" - {principle.statement}")

    def compute_vad(self):
        # Placeholder for VAD mapping
        from types import SimpleNamespace
        return SimpleNamespace(V=self.dpes.dopamine_level - self.nis.fast_pain)

if __name__ == "__main__":
    p = Prometheus()
    p.main_life_loop()
