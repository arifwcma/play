import numpy as np

def estimate_pi(n):
    points = np.random.rand(n, 2)
    inside = np.sum(np.linalg.norm(points, axis=1) <= 1.0)
    return (inside / n) * 4

print(estimate_pi(1000000))
