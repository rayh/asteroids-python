from __future__ import annotations
from functools import reduce
from math import cos, pi, sin
from random import random
from this import d
from typing import List, Tuple

from pygame import Rect
import pymunk as pm
from pymunk import Arbiter, Vec2d, pygame_util
import pygame

from .particle import Particle
from asteroids.constants import COLLISION_TYPE_ORDANANCE, COLLISION_TYPE_PLAYER, G, WHITE

pygame_util.positive_y_is_up = False

# def atan_div(opp, adj) -> float:
#     if (opp != 0 and adj != 0):
#         return atan(opp / adj)
#     elif (opp != 0):
#         if(opp > 0):
#             return 3/2 * pi
#         else:
#             return 1/2 * pi
#     else:
#         if(adj > 0):
#             return pi
#         else:
#             return 0

# class Vector:
#     def __init__(self, m=0, a=0) -> None:
#         self.a = a
#         self.m = m

#     def dot(self, scalar) -> Vector:
#         return Vector(m=self.m * scalar, a=self.a)

#     def to_cart(self) -> Tuple(float, float):
#         y = sin(self.a) * self.m
#         x = cos(self.a) * self.m

#         return (x, y)

#     # def distance(self, v: Vector) -> float:
#     #     return sqrt(self.m**2 + v.m**2 - (2*self.m*v.m * cos(self.a - v.a)))

#     # see https://math.stackexchange.com/questions/1365622/adding-two-polar-vectors
#     def add(self, v: Vector) -> Vector:
#         m = sqrt(self.m**2 + v.m**2 + (2*self.m*v.m * cos(v.a - self.a)))
#         a = self.a + atan2(v.m * sin(v.a - self.a), self.m + v.m * cos(v.a - self.a))
#         return Vector(m, a)

#     def subtract(self, v: Vector) -> Vector:
#         return self.add(v.dot(-1))

#     def from_cartesian(x: float, y: float) -> Vector:
#         a = atan2(y, x)
#         m = sqrt(x**2 + y**2)
#         return Vector(m, a)

#     def __str__(self) -> str:
#         return str(self.to_cart())


class GameEngine:

    def __init__(self, screen_size) -> None:
        self.space = pm.Space()
        self.screen_size = screen_size
        self.particles = []
        self.particle_lookup = {}
        self.on_collision_pair = None

        def post_solve_collision(arbiter, space, data):
            if not arbiter.is_first_contact:
                return

            if not self.on_collision_pair:
                return

            # first_point = arbiter.contact_point_set.points[0]
            # shapes = [s for s in arbiter.shapes if s.collision_type == COLLISION_TYPE_PLAYER]
            particles = [self.particle_lookup[s] for s in arbiter.shapes if s in self.particle_lookup]
            for p in particles:
                for p2 in particles:
                    if p2 == p:
                        continue

                    self.on_collision_pair(self, p, p2, arbiter)

        self.default_collision_handler = self.space.add_default_collision_handler()
        self.default_collision_handler.post_solve = post_solve_collision

        # Initialize the Pygame engine
        pygame.init()

        # Set up the drawing window
        self.screen = pygame.display.set_mode(size=screen_size)

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

        # Set up the clock for a decent frame rate
        self.clock = pygame.time.Clock()

    def render(self, debug=False):
        for p in self.particles:
            p.draw_screen(self.screen, debug=debug)


    def quit(self):
        # Make the mouse visible again
        pygame.mouse.set_visible(True)

        # Quit the game
        pygame.quit()

    def add(self, object):
        self.particles.append(object)
        self.particle_lookup[object.shape] = object

        if object.is_physical:
            self.space.add(object.body, object.shape)

    def remove(self, object):
        if object not in self.particles:
            return 
            
        self.particles.remove(object)
        del self.particle_lookup[object.shape]

        if object.is_physical:
            self.space.remove(object.body, object.shape)

    def calculate_gravitational_impulse(self, p):
        # Calculate gravity
        # F=G{\frac{m_1m_2}{r^2}}
        p.gravity_vectors = []
        for p2 in self.particles[:]:
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

    def wrap_screen_coords(self, p: Particle):
        if p.body.position[1]>self.screen_size[1]:
            p.body.position = (p.body.position[0], p.body.position[1] - self.screen_size[1])
        
        if p.body.position[1]<0:
            p.body.position = (p.body.position[0], self.screen_size[1] - p.body.position[1])

        if p.body.position[0]>self.screen_size[0]:
            p.body.position = (p.body.position[0] - self.screen_size[0], p.body.position[1])
        
        if p.body.position[0]<0:
            p.body.position = (self.screen_size[0] - p.body.position[0], p.body.position[1])

    def calculate_collisions(self, p: Particle):
        pass
        # for p2 in self.particles:
        #     if p == p2:
        #         continue

        #     collision = pygame.sprite.collide_mask(p, p2)
        #     if collision:
        #         diff = p.position.subtract(p2.position)


    def tick(self, time=1):

        for p in self.particles[:]:
            if p.dead:
                self.remove(p)

            # self.calculate_gravitational_impulse(p)

            self.wrap_screen_coords(p)

            p.tick(time, debug=True)

        self.space.step(time)
        self.clock.tick(1/time)
