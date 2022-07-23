from __future__ import annotations
from math import atan, atan2, cos, pi, sin, sqrt
from random import random
from typing import Tuple

from pygame import Rect
import pymunk as pm
import pygame

from asteroids.polygon import move

G = 6.67e-11 

def atan_div(opp, adj) -> float:
    if (opp != 0 and adj != 0):
        return atan(opp / adj)
    elif (opp != 0):
        if(opp > 0):
            return 3/2 * pi
        else:
            return 1/2 * pi
    else:
        if(adj > 0):
            return pi
        else:
            return 0

class Vector:
    def __init__(self, m=0, a=0) -> None:
        self.a = a
        self.m = m

    def dot(self, scalar) -> Vector:
        return Vector(m=self.m * scalar, a=self.a)

    def to_cart(self) -> Tuple(float, float):
        y = sin(self.a) * self.m
        x = cos(self.a) * self.m

        return (x, y)

    # def distance(self, v: Vector) -> float:
    #     return sqrt(self.m**2 + v.m**2 - (2*self.m*v.m * cos(self.a - v.a)))

    # see https://math.stackexchange.com/questions/1365622/adding-two-polar-vectors
    def add(self, v: Vector) -> Vector:
        m = sqrt(self.m**2 + v.m**2 + (2*self.m*v.m * cos(v.a - self.a)))
        a = self.a + atan2(v.m * sin(v.a - self.a), self.m + v.m * cos(v.a - self.a))
        return Vector(m, a)

    def subtract(self, v: Vector) -> Vector:
        return self.add(v.dot(-1))

    def from_cartesian(x: float, y: float) -> Vector:
        a = atan2(y, x)
        m = sqrt(x**2 + y**2)
        return Vector(m, a)

    def __str__(self) -> str:
        return str(self.to_cart())

class Particle(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super(Particle, self).__init__()
        self.angle = -pi/2
        self.mass = 1 # 1kg
        self.gravity = Vector()
        self.position = Vector.from_cartesian(0,0)
        self.impulse = Vector()
        self.velocity = Vector()

        # moment = pm.moment_for_poly(self.mass, vs)
        # self.body = pm.Body(self.mass, moment)
        # self.shape = pm.Poly(self.body, vs)
        # self.shape.friction = .9
        # self.body.position = pos

    def draw_vector(self, surf, vector, color, width=1):
        size = surf.get_size()
        xy = vector.to_cart()
        pygame.draw.line(surf, color, 
            move((0,0), (size[0]/2, size[1]/2)), 
            move(xy, (size[0]/2, size[1]/2)), 
        width)

    def draw_debug(self, screen):
        debug_surf = pygame.Surface( (50,50), pygame.SRCALPHA, 32 )  
        self.draw_vector(debug_surf, self.impulse, (255,0,0))
        self.draw_vector(debug_surf, self.velocity, (0,255,0))
        self.draw_vector(debug_surf, self.gravity, (0,0,255))

        draw_rect = Rect(0,0,50,50)
        draw_rect.center = self.rect.center
        screen.blit(debug_surf, draw_rect)

    def draw_screen(self, screen):
        screen.blit(self.surf, self.rect)

    def on_update(self, surf: pygame.Surface):
        pass

    def update(self):
        empty = pygame.Color(0,0,0,0) #The last 0 indicates 0 alpha, a transparent color#Inside the game loop
        self.surf.fill(empty)

        self.on_update(self.surf)

        # Create the collision mask (anything not transparent)
        self.mask = pygame.mask.from_surface( self.surf )  
        self.rect.center = self.position.to_cart()

class PhysicsEngine:

    def __init__(self, screen_size) -> None:
        self.space = pm.Space()
        self.screen_size = screen_size
        self.particles = []
        pass

    def add(self, object):
        self.particles.append(object)
        self.space.add(object.body, object.shape)

    def calculate_gravitational_impulse(self, p):
        # Calculate gravity
        # F=G{\frac{m_1m_2}{r^2}}
        for p2 in self.particles:
            if p == p2:
                continue
            diff = p.position.subtract(p2.position)
            force = G * ((p.mass * p2.mass) / (diff.m ** 2))
            p.gravity = p.gravity.add(Vector(force*-1000, diff.a))
            # print('Add', p.gravity, 'to', p)

    def wrap_screen_coords(self, p: Particle):
        if p.position.to_cart()[1]>self.screen_size[1]:
            p.position = Vector.from_cartesian(p.position.to_cart()[0], p.position.to_cart()[1] - self.screen_size[1])
        
        if p.position.to_cart()[1]<0:
            p.position = Vector.from_cartesian(p.position.to_cart()[0], self.screen_size[1] - p.position.to_cart()[1])

        if p.position.to_cart()[0]>self.screen_size[0]:
            p.position = Vector.from_cartesian(p.position.to_cart()[0] - self.screen_size[0], p.position.to_cart()[1])
        
        if p.position.to_cart()[0]<0:
            p.position = Vector.from_cartesian(self.screen_size[0] - p.position.to_cart()[0], p.position.to_cart()[1])

    def calculate_collisions(self, p: Particle):
        pass
        # for p2 in self.particles:
        #     if p == p2:
        #         continue

        #     collision = pygame.sprite.collide_mask(p, p2)
        #     if collision:
        #         diff = p.position.subtract(p2.position)


    def tick(self, time=1):
        self.space.step(time)

        for p in self.particles:
            p.gravity = Vector()
            self.calculate_gravitational_impulse(p)

            # Calculate impulse
            p.velocity = p.impulse.add(p.gravity).dot(1/p.mass).add(p.velocity)

            # Update position
            movement = p.velocity.dot(time)
            p.position = p.position.add(movement)

            # Check colisions
            self.calculate_collisions(p)

            self.wrap_screen_coords(p)
            # print('move', p, 'by', movement, 'to', p.position)