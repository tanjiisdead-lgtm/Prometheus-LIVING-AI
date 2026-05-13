import numpy as np

def clip(n, smallest, largest):
    return max(smallest, min(n, largest))

PAIN_INTERRUPT_THRESHOLD = 0.7
PAIN_LEARNING_MULTIPLIER = 10.0

class NociceptiveInterruptSystem:
    def __init__(self):
        self.fast_pain = 0.0    # immediate, decays fast
        self.slow_pain = 0.0    # chronic, decays slow
        self.pain_memory = []   # what caused pain — learned to avoid
        self.interrupt_active = False

    def register_damage(self, source, magnitude):
        # Fast pain: immediate spike
        self.fast_pain = min(1.0, self.fast_pain + magnitude)

        # Slow pain: accumulates from repeated damage
        self.slow_pain = clip(self.slow_pain + 0.1 * magnitude, 0, 1)

        # Store pain source in memory with high salience
        self.pain_memory.append({
            'source': source,
            'magnitude': magnitude,
            'context': self.get_current_context(),
            'salience': magnitude  # painful memories are written strongly
        })

        # MANDATORY INTERRUPT: if fast pain > threshold, override cognition
        if self.fast_pain > PAIN_INTERRUPT_THRESHOLD:
            self.issue_cognitive_interrupt(source)

    def issue_cognitive_interrupt(self, source):
        # This cannot be suppressed by any other system
        # It clears the goal stack and forces pain-source focus
        print(f"PAIN INTERRUPT: {source}")
        self.interrupt_active = True
        # cognitive_bus.send_interrupt(...)

    def modulate_all_processing(self):
        # Slow pain modulates everything — there's no escaping it
        total_pain = self.fast_pain + 0.3 * self.slow_pain

        # Decay pain values
        self.fast_pain *= 0.5  # decays in ~5 steps
        self.slow_pain *= 0.998 # decays in ~500 steps

        if self.fast_pain < 0.1:
            self.interrupt_active = False

        return {
            'attention_bias':   -total_pain,      # harder to focus
            'memory_threshold':  total_pain,       # harder to write new memories
            'action_variance':   total_pain,       # actions become more erratic
            'learning_rate':     1 + total_pain,   # pain sharpens learning (avoid this)
            'creativity_bias':  -total_pain * 0.5  # pain suppresses exploration
        }

    def get_current_context(self):
        # Placeholder for context retrieval
        return "default_context"

    def learn_from_pain(self, state, action, magnitude):
        # Any state-action pair leading to pain gets a very strong
        # negative update — much stronger than normal reward shaping
        pain_gradient = magnitude * PAIN_LEARNING_MULTIPLIER

        print(f"PAIN LEARNING: Avoid {action} in {state}. Gradient: {pain_gradient}")
        # self.update_weights_immediately(state, action, -pain_gradient)
