import numpy as np

def random_hv(D=10000, rng=None):
    if rng is None:
        rng = np.random.default_rng()
    return rng.choice([0, 1], size=D).astype(np.uint8)

def xor(hv1, hv2):
    return np.bitwise_xor(hv1, hv2)

def bind(hv1, hv2):
    # For binary HDC, XOR is the standard binding operator
    return xor(hv1, hv2)

def unbind(hv1, hv2):
    # XOR is its own inverse
    return xor(hv1, hv2)

def superpose(hvs, rng=None):
    """Majority vote for binary vectors."""
    if rng is None:
        rng = np.random.default_rng()

    hvs = np.array(hvs)
    if hvs.ndim == 1:
        return hvs
    count = hvs.shape[0]
    summed = np.sum(hvs, axis=0)

    result = (summed > (count / 2)).astype(np.uint8)

    # Handle ties
    if count % 2 == 0:
        ties = (summed == (count / 2))
        if np.any(ties):
            result[ties] = rng.choice([0, 1], size=np.sum(ties)).astype(np.uint8)

    return result

def hamming_similarity(hv1, hv2):
    """Normalized Hamming similarity: 1.0 = identical, 0.0 = completely different."""
    hamming_dist = np.sum(hv1 != hv2)
    return 1.0 - (hamming_dist / len(hv1))

def encode_scalar(value, D=10000, resolution=100):
    """
    Encode a scalar value [0, 1] into a hypervector.
    """
    # Use a seeded local RNG for deterministic but non-global mapping
    seed = int(value * resolution)
    rng = np.random.default_rng(seed)
    hv = rng.choice([0, 1], size=D).astype(np.uint8)
    return hv
