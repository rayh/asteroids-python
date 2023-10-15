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


class Scene:
    def __init__(self) -> None:
        self.particles = []
        self.behaviours = []
        self.particle_lookup = {}
        self.elapsed_time = 0
        self.space = pm.Space(threaded=True)
        self.space.threads = 4
        self.default_collision_handler = None

    def setup(self, engine):
        def post_solve_collision(arbiter, space, data):
            if not arbiter.is_first_contact:
                return

            if not self.on_collision_pair:
                return

            # first_point = arbiter.contact_point_set.points[0]
            # shapes = [s for s in arbiter.shapes if s.collision_type == COLLISION_TYPE_PLAYER]
            particles = [
                self.particle_lookup[s]
                for s in arbiter.shapes
                if s in self.particle_lookup
            ]
            for p in particles:
                for p2 in particles:
                    if p2 == p:
                        continue

                    self.on_collision_pair(p, p2, arbiter)

        self.default_collision_handler = self.space.add_default_collision_handler()
        self.default_collision_handler.post_solve = post_solve_collision
        pass

    def on_collision_pair(self, p1: Particle, p2: Particle, arbiter: Arbiter):
        pass

    def teardown(self, engine):
        pass

    def tick(self, engine, time: float):
        for p in self.particles[:]:
            p.on_start_tick(self, time)

        for p in self.particles[:]:
            if p.dead:
                self.remove(p)

            self.tick_particle(p, time)

            # Trigger behaviours
            # [b.on_tick(self, p) for b in self.behaviours]

        self.space.step(time)
        self.elapsed_time += time

    def tick_particle(self, p, time: float):
        p.tick(self, time)

    def render(self, surf, debug_surf, debug=False):
        for p in self.particles:
            p.draw()
            surf.blit(p.surf, p.rect)

            if debug:
                p.draw_debug(debug_surf)

    def add(self, object):
        self.particles.append(object)
        self.particle_lookup[object.shape] = object

        if object.is_physical:
            self.space.add(object.body, object.shape)

    def remove(self, object):
        if object not in self.particles:
            return

        self.particles.remove(object)

        if object.shape in self.particle_lookup:
            del self.particle_lookup[object.shape]

        object.dead = True

        if object.is_physical:
            self.space.remove(object.body, object.shape)

    def particles_near(self, position: Vec2d, max_distance: float, mask=0x0):
        points = self.space.point_query(
            position, max_distance=max_distance, shape_filter=ShapeFilter(mask=mask)
        )
        return [self.particle_lookup[point.shape] for point in points]
