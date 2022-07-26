
from math import cos, modf, pi, sin
from pymunk import Vec2d

def vec_polar(angle: float, scalar: float) -> Vec2d:
    return Vec2d(
        cos(angle) * scalar, 
        sin(angle) * scalar
    )

def diff_angle(a1: float, a2: float) -> float:
    diff = (a1 - a2) % (2*pi)
    if diff > pi:
        return -1 * (2*pi - diff)
    else:
        return diff