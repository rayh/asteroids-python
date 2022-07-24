
from math import cos, sin
from pymunk import Vec2d

def vec_polar(angle: float, scalar: float) -> Vec2d:
    return Vec2d(
        cos(angle) * scalar, 
        sin(angle) * scalar
    )