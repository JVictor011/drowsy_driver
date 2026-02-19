import math

def euclid(p1, p2): return math.hypot(p1[0]-p2[0], p1[1]-p2[1])

def eye_aspect_ratio(pts):
    A = euclid(pts[1], pts[4])
    B = euclid(pts[2], pts[5])
    C = euclid(pts[0], pts[3]) + 1e-8
    return (A + B) / (2.0 * C)

def smooth(series, maxlen):
    if not series: return 0.0
    return sum(series) / len(series)
