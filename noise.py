import numpy as np

# noise pattern option math

# random
def uniform_pattern(height, pattern_width, **kwargs):
    return np.random.randint(0, 256, (height, pattern_width), dtype=np.uint8)

#gaussian distribution (bell curve of values) ***have to clip in order to prevent wraparound artifact
def gauss_pattern(height, pattern_width, gauss_mean=127, gauss_std=50, **kwargs):
    return np.random.normal(gauss_mean, gauss_std, (height, pattern_width)).clip(0, 255).astype(np.uint8)

# black/white only, random
def binary_pattern(height, pattern_width, **kwargs):
    return np.random.choice([0, 255], size=(height, pattern_width)).astype(np.uint8)

# pattern registry
available_patterns = {
    "Uniform Noise": uniform_pattern,
    "Gaussian Noise": gauss_pattern,
    "Binary Noise": binary_pattern
}


