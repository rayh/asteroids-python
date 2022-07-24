from __future__ import annotations
from functools import reduce
from math import atan, atan2, cos, pi, sin, sqrt
from random import random
from this import d
from typing import List, Tuple

from pygame import Rect
import pymunk as pm
from pymunk import Arbiter, Vec2d, pygame_util
import pygame

from asteroids.polygon import move
from asteroids.constants import COLLISION_TYPE_ORDANANCE, COLLISION_TYPE_PLAYER, WHITE

G = 6.67e-11 

pygame_util.positive_y_is_up = False

def vec_polar(angle: float, scalar: float) -> Vec2d:
    return Vec2d(
        cos(angle) * scalar, 
        sin(angle) * scalar
    )

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

class Particle(pygame.sprite.Sprite):
    def __init__(self, mass, vertices, position=(0,0)) -> None:
        super(Particle, self).__init__()
        # self.angle = -pi/2
        self.mass = mass # 1kg
        # self.position = Vector.from_cartesian(0,0)
        # self.impulse = Vector()
        # self.velocity = Vector()
        self.colour = WHITE
        moment = pm.moment_for_poly(self.mass, vertices)
        self.body = pm.Body(self.mass, moment)
        self.shape = pm.Poly(self.body, vertices)
        self.shape.friction = .9
        self.body.position = position
        self.gravity_vectors = []
        self.gravity = Vec2d(0,0)
        self.age = 0
        self.dead = False

        self.debug_surf = pygame.Surface( (250,250), pygame.SRCALPHA, 32 )  

    def draw_vector(self, surf, vector: Vec2d, color, width=1):
        if vector.length == 0:
            return 

        size = surf.get_size()
        pygame.draw.line(surf, color, 
            (size[0]/2, size[1]/2), 
            vector + (size[0]/2, size[1]/2), 
        width)

    def draw_shape(self, surf):
        shape = self.shape
        size = surf.get_size()
        ps = [pos.rotated(shape.body.angle) + Vec2d(size[0]/2, size[1]/2)
                for pos in shape.get_vertices()]
        # ps += [ps[0]]
        pygame.draw.polygon(surf, self.colour, ps, width=1)

    def draw_debug(self):
        empty = pygame.Color(0,0,0,0)
        self.debug_surf.fill(empty)

        # self.draw_vector(debug_surf, self.impulse, (255,0,0))
        self.draw_vector(self.debug_surf, self.body.velocity, (0,255,0))
        self.draw_vector(self.debug_surf, self.body.force, (255,0,0))
        self.draw_vector(self.debug_surf, self.gravity, (0,0,255))

        for v in self.gravity_vectors:
            self.draw_vector(self.debug_surf, v.scale_to_length(100), (0,0,128,128))


    def draw_screen(self, screen, debug=False):
        screen.blit(self.surf, self.rect)
        if debug:
            draw_rect = self.debug_surf.get_rect()
            draw_rect.center = self.rect.center
            screen.blit(self.debug_surf, draw_rect)

    def on_update(self, surf: pygame.Surface):
        pass

    def on_collision(self, engine: PhysicsEngine, arbiter: Arbiter, particles: List[Particle]):
        pass

    def update(self, time, debug=False):
        self.rect.center = self.body.position
        self.age+=time

        empty = pygame.Color(0,0,0,0)
        #The last 0 indicates 0 alpha, a transparent color#Inside the game loop
        self.surf.fill(empty)

        self.on_update(self.surf)

        self.draw_shape(self.surf)

        if debug:
            self.draw_debug()

        # Create the collision mask (anything not transparent)
        self.mask = pygame.mask.from_surface( self.surf )  

class PhysicsEngine:

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

    def add(self, object):
        self.particles.append(object)
        self.particle_lookup[object.shape] = object
        self.space.add(object.body, object.shape)

    def remove(self, object):
        if object not in self.particles:
            return 
            
        self.particles.remove(object)
        del self.particle_lookup[object.shape]
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

            self.calculate_gravitational_impulse(p)

            self.wrap_screen_coords(p)

            p.update(time, debug=True)

        self.space.step(time)