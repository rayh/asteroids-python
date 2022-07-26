from __future__ import annotations
from math import cos, pi, sin
from pdb import pm
import pygame
import pymunk
from random import random

from asteroids.constants import WHITE

def rotate(origin, point, angle):

    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + cos(angle) * (px - ox) - sin(angle) * (py - oy)
    qy = oy + sin(angle) * (px - ox) + cos(angle) * (py - oy)
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

class Group:
    def __init__(self, shapes = []) -> None:
        self.shapes = shapes

    def rotate(self, angle, origin=(0,0)) -> Group:
        return Group([shape.rotate(angle, origin) for shape in self.shapes])

    def draw(self, surface, colour=WHITE, width=0):
        [shape.draw(surface, colour, width) for shape in self.shapes]

class Polygon:
    def __init__(self, points) -> None:
        self.points = points

    def rotate(self, angle, origin=(0,0)) -> Polygon:
        return Polygon(rotate_poly(origin, self.points, angle))

    def translate(self, amount) -> Polygon:
        return Polygon(move_poly(self.points, amount))

    def scale(self, s) -> Polygon:
        return Polygon(scale_poly(self.points, s))

    def center_in_surface(self, surf) -> Polygon:
        surf_size = surf.get_size()
        return Polygon(move_poly(self.points, (surf_size[0]/2, surf_size[1]/2)))

    def draw(self, surface, colour=WHITE, width=0):
        pygame.draw.polygon( surface, colour, self.points, width=width)

    def circle(radius, segments=10, randomize_radius_factor=0) -> Polygon:
        points = []
        for i in range(0, segments):
            r = (radius * 1-randomize_radius_factor) + (random() * radius * randomize_radius_factor)
            angle = i * 2 * pi / segments
            points.append((cos(angle) * r, sin(angle) * r))

        return Polygon(points)

    def line(a, b) -> Polygon:
        return Polygon([a,b])

    def square(size) -> Polygon:
        return Polygon([
            (-size/2,-size/2),
            (size/2,-size/2),
            (size/2,size/2),
            (-size/2,size/2)
            ])
