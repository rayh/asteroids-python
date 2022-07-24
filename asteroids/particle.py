from __future__ import annotations
from functools import reduce

from pygame import Rect
import pymunk as pm
from pymunk import Arbiter, Vec2d, pygame_util
import pygame

from asteroids.polygon import move
from asteroids.constants import COLLISION_TYPE_ORDANANCE, COLLISION_TYPE_PLAYER, WHITE

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
        if moment < 0:
            moment = 1 
        self.body = pm.Body(self.mass, moment)
        self.shape = pm.Poly(self.body, vertices)
        self.shape.friction = .9
        self.body.position = position
        self.gravity_vectors = []
        self.gravity = Vec2d(0,0)
        self.age = 0
        self.health = 1.0
        self.dead = False

        # If false, doesnt experience physics
        self.is_physical = True

        self.debug_surf = pygame.Surface( (250,250), pygame.SRCALPHA, 32 )  

    def draw_vector(self, surf, vector: Vec2d, color, width=1):
        if vector.length == 0:
            return 

        size = surf.get_size()
        pygame.draw.line(surf, color, 
            (size[0]/2, size[1]/2), 
            vector + (size[0]/2, size[1]/2), 
        width)

    def draw_polygon(self, surf, points, colour, width=1):
        size = surf.get_size()
        ps = [pos.rotated(self.body.angle) + Vec2d(size[0]/2, size[1]/2)
                for pos in points]
        pygame.draw.polygon(surf, colour, ps, width=width)

    def draw_shape(self, surf, shape, colour, width=1):
        size = surf.get_size()
        ps = [pos.rotated(shape.body.angle) + Vec2d(size[0]/2, size[1]/2)
                for pos in shape.get_vertices()]
        # ps += [ps[0]]
        pygame.draw.polygon(surf, colour, ps, width=width)

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

    def on_update(self, surf: pygame.Surface, time: float):
        self.draw_shape(self.surf, self.shape, self.colour)
        pass

    def tick(self, time, debug=False):
        self.rect.center = self.body.position
        self.age+=time

        empty = pygame.Color(0,0,0,0)
        #The last 0 indicates 0 alpha, a transparent color#Inside the game loop
        self.surf.fill(empty)

        self.on_update(self.surf, time)

        if debug:
            self.draw_debug()

        # Create the collision mask (anything not transparent)
        self.mask = pygame.mask.from_surface( self.surf )  