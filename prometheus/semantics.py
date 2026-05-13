import numpy as np
from .hdc import random_hv, bind, superpose, unbind, hamming_similarity, encode_scalar

class AffectivelyGroundedSemantics:
    def __init__(self, hdl):
        self.hdl = hdl
        self.D = hdl.D

        # Role hypervectors — immutable random vectors for syntactic roles
        self.ROLE = {
            'AGENT':    random_hv(self.D),
            'PATIENT':  random_hv(self.D),
            'ACTION':   random_hv(self.D),
            'CONTEXT':  random_hv(self.D),
            'PROPERTY': random_hv(self.D),
        }

        self.last_proposition_salience = 0.0

    def build_proposition(self, agent_word, action_word, patient_word, context_word=None, current_affective_state=None):
        """
        Construct a proposition as a single hypervector.
        """
        agent_hv   = bind(self.hdl.get_word_hv(agent_word),   self.ROLE['AGENT'])
        action_hv  = bind(self.hdl.get_word_hv(action_word),  self.ROLE['ACTION'])
        patient_hv = bind(self.hdl.get_word_hv(patient_word), self.ROLE['PATIENT'])

        components = [agent_hv, action_hv, patient_hv]

        if context_word:
            context_hv = bind(self.hdl.get_word_hv(context_word), self.ROLE['CONTEXT'])
            components.append(context_hv)

        proposition = superpose(components)

        # Stamping with affective context
        if current_affective_state:
            pain_hv = encode_scalar(current_affective_state.get('pain', 0.0), self.D)
            dopamine_hv = encode_scalar(current_affective_state.get('dopamine', 0.5), self.D)
            stamped = bind(proposition, superpose([pain_hv, dopamine_hv]))
            return stamped

        return proposition

    def query_proposition(self, proposition_hv, query_role):
        """
        Given a stored proposition, recover what's in a role.
        """
        recovered = unbind(proposition_hv, self.ROLE[query_role])
        word, similarity = self.hdl.nearest_neighbor(recovered)
        return word, similarity

    def compute_survival_relevance(self, proposition_hv, system_state):
        """
        How relevant is this proposition to survival?
        Simplified matching against affective markers.
        """
        # In a real system, we'd match against pain_memory_bundle etc.
        # Here we just check if it contains 'painful' or 'rewarding' words

        # Placeholder for relevance logic
        # For now, let's just say relevance is linked to the proposition's
        # internal similarity to known affective HVs

        pain_hv = encode_scalar(1.0, self.D) # Pure pain marker
        reward_hv = encode_scalar(1.0, self.D) # Pure reward marker (dopamine)

        pain_relevance = hamming_similarity(proposition_hv, pain_hv)
        energy_relevance = hamming_similarity(proposition_hv, reward_hv)

        self.last_proposition_salience = max(pain_relevance, energy_relevance)

        return {
            'pain_relevance': pain_relevance,
            'energy_relevance': energy_relevance,
            'total_salience': self.last_proposition_salience
        }
