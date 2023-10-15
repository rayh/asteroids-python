from __future__ import annotations
from functools import reduce
from math import cos, pi, sin
from random import random
from this import d
from typing import List, Tuple

from pygame import Rect
import pymunk as pm
from pymunk import Arbiter, ShapeFilter, Vec2d, pygame_util
from asteroids.engine.particle import Particle
from random import randint, random, uniform
from .polygon import Polygon
from .constants import COLLISION_TYPE_ENEMY, WHITE
import pygame

G = 6.67e-10


class GravityWell(Particle):
    @classmethod
    def randomized(cls, screen_size: Tuple[float, float]) -> "GravityWell":
        width, height = screen_size
        position = (randint(10, width - 10), randint(10, height - 10))
        return GravityWell(mass=1e15, position=position)

    def __init__(self, mass, position):
        self.size = 20
        self.poly = Polygon.circle(
            self.size,
            segments=20,
        )

        super(GravityWell, self).__init__(mass=mass, vertices=self.poly.points)

        # self.body.velocity =
        self.is_physical = True
        self.is_movable = False
        self.shape.elasticity = 0.3

        self.shape.collision_type = COLLISION_TYPE_ENEMY
        self.shape.filter = ShapeFilter(categories=ShapeFilter.ALL_CATEGORIES())
        self.body.body_type = pm.Body.STATIC
        # The starting position is randomly generated
        self.body.position = position

        # create transparent background image
        self.surf = pygame.Surface((150, 150), pygame.SRCALPHA, 32)
        self.rect = self.surf.get_rect(center=self.body.position)

    def on_update(self, scene: "Scene", time: float):
        # Calculate gravity
        # F=G{\frac{m_1m_2}{r^2}}
        for p2 in scene.particles[:]:
            if self == p2:
                continue

            diff_v = self.body.position - p2.body.position

            # Min radius to apply gravity - prevents insane forces
            if diff_v.length < self.size:
                continue

            dist_sq = diff_v.get_length_sqrd()
            angle = diff_v.angle

            force = G * ((self.mass * p2.mass) / dist_sq)
            if force == 0:
                continue

            force_v = Vec2d(cos(angle) * force, sin(angle) * force)
            p2.apply_force(force_v, label="gravity")
