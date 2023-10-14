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


G = 6.67e-4


class GravityBehaviour:
    def on_tick(self, scene: "Scene", p: Particle):
        # Calculate gravity
        # F=G{\frac{m_1m_2}{r^2}}
        p.gravity_vectors = []
        for p2 in scene.particles[:]:
            if p == p2:
                continue

            diff_v = p2.body.position - p.body.position

            dist_sq = diff_v.get_length_sqrd()
            if dist_sq < 2:
                continue

            angle = diff_v.angle

            force = G * ((p.mass * p2.mass) / dist_sq)
            if force == 0:
                continue

            force_v = Vec2d(cos(angle) * force, sin(angle) * force)
            p.gravity_vectors.append(force_v)

        p.gravity = reduce(lambda a, b: a + b, p.gravity_vectors, Vec2d.zero())
        p.body.apply_impulse_at_world_point(p.gravity, p.body.position)
