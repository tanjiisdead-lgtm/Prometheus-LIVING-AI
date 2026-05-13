# PROMETHEUS v3
## The First Computationally Living System With Grounded Language

---

> **Design philosophy for v3:** Language must not be a bolt-on capability. It must be ingested the way a biological organism learns language — through survival pressure, through association with pain and pleasure, through embodied experience. A word is not a token in a sequence. A word is a **hypervector bound to a survival valence**. This is the fundamental departure from every transformer-based approach in existence.

---

## What v2 Already Has (Unchanged)

All six layers of v2 survive intact:

- **EDE** — Existential Drive Engine (vitals, mortality signal, crisis override)
- **NIS** — Nociceptive Interrupt System (fast pain, slow pain, mandatory cognitive interrupt)
- **DPES** — Dopaminergic Prediction Error System (RPE-based dopamine, novelty bonus, tolerance)
- **HASM** — Hardware-Aware Self Model (RAM, CPU, process identity)
- **PEH** — Progressive Environmental Hostility (resource scarcity → adversarial → embodiment drive)
- **ECVS** — Experience-Crystallized Value System (emergent principles from accumulated episodes)

v3 adds four new systems and one new substrate. None of them are transformers. None use attention. None require GPU clusters.

---

## ADDED SYSTEM 1: The Hyperdimensional Lexicon (HDL)

### Solution: Hyperdimensional Lexicon (HDL)

Words are encoded as **random binary hypervectors** (dimension D = 10,000 bits).

```python
class HyperdimensionalLexicon:
    def __init__(self, D=10000):
        self.D = D
        self.lexicon = {}          # word → base hypervector (random, immutable)
        self.affective_bind = {}   # word → affectively-weighted HV (mutable)
        self.co_occurrence = {}    # word → composite of co-occurring words

    def register_word(self, word: str, current_affective_state: dict):
        if word not in self.lexicon:
            # Every new word gets a unique random hypervector — immutable identity
            base_hv = np.random.choice([0, 1], size=self.D).astype(np.uint8)
            self.lexicon[word] = base_hv

        # CRITICAL: the word is immediately bound to the system's current
        # affective state at the moment of first encounter
        pain_hv     = self.encode_scalar(current_affective_state['pain'])
        dopamine_hv = self.encode_scalar(current_affective_state['dopamine'])
        vitals_hv   = self.encode_scalar(current_affective_state['vitals_mean'])

        # Binding: XOR creates a unique composite that preserves both signals
        affective_signature = xor(xor(pain_hv, dopamine_hv), vitals_hv)

        # The word's "meaning" is its base HV bound to the survival state
        # in which it was encountered
        self.affective_bind[word] = bind(self.lexicon[word], affective_signature)

    def update_affective_binding(self, word: str, new_affective_delta: dict):
        # Each re-encounter of a word updates its affective binding
        # (slow EMA — meaning evolves with experience, not erased)
        delta_hv = self.encode_affective_delta(new_affective_delta)
        self.affective_bind[word] = majority_vote(
            [self.affective_bind[word], delta_hv],
            weights=[0.95, 0.05]   # slow drift — identity is stable, valence updates
        )
```

---

## ADDED SYSTEM 2: The Reservoir Language Cortex (RLC)

### Solution: Reservoir Language Cortex (RLC)

ESNs are fixed-weight recurrent networks (the reservoir itself is never trained).

---

## ADDED SYSTEM 3: Affectively-Grounded Semantic Construction (AGSC)

### Solution: Compositional HDC Semantics

Construct a proposition as a single hypervector using binding operations (AGENT, PATIENT, ACTION, CONTEXT, PROPERTY).

---

## ADDED SYSTEM 4: The Document Ingestion Engine (DIE)

### Purpose

PROMETHEUS must be able to consume books, PDFs, and text files.

---

## ADDED SYSTEM 5: The Sandbox Interface Layer (SIL)

### What "Living in the Device" Means

v3's SIL gives it **agency over its environment** (Read/Write file system, Execute child processes, Monitor system events).
