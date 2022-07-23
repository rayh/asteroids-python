from __future__ import annotations
import math
import pygame

from asteroids.constants import WHITE

def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

def move(point, m):
    return point[0] + m[0], point[1] + m[1]

def scale(point, s):
    return point[0] * s, point[1] * s

def rotate_poly(origin, points, angle):
    return [rotate(origin, p, angle) for p in points]

def scale_poly(points, s):
    return [scale(p, s) for p in points]

def move_poly(points, m):
    return [move(p, m) for p in points]

    

class Polygon:
    def __init__(self, points) -> None:
        self.points = points

    def rotate(self, angle, origin=(0,0)) -> Polygon:
        return Polygon(rotate_poly(origin, self.points, angle))

    def move(self, amount) -> Polygon:
        return Polygon(move_poly(self.points, amount))

    def scale(self, s) -> Polygon:
        return Polygon(scale_poly(self.points, s))

    def draw(self, surface, colour=WHITE):
        surf_size = surface.get_size()
        points = move_poly(self.points, (surf_size[0]/2, surf_size[1]/2))
        pygame.draw.polygon( surface, colour, points )
