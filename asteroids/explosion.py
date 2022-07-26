from math import pi
from random import uniform
from typing import Tuple
from pathlib import Path
import pygame
from pymunk import Vec2d

from .particle import Particle
from .maths import vec_polar
from .engine import GameEngine
from asteroids.polygon import Group, Polygon, move_poly, scale_poly, rotate_poly 
from .constants import WHITE

# Define the Player sprite
class Explosion(Particle):
    def __init__(self, position=(0,0), distance=150, force=1e8):
        """Initialize the player sprite"""
        super(Explosion, self).__init__(
            mass=1,
            vertices=Polygon.square(1).points, 
            position=position)

        # self.angle = -pi/2
        self.body.angle = 0
        self.body.velocity = Vec2d.zero()
        self.colour = (255,0,0)
        self.is_physical = False
        self.max_age = 1
        self.force = force
        self.max_distance = distance
        self.explosion_vectors = []

        # create transparent background image
        self.surf = pygame.Surface( (100,100), pygame.SRCALPHA, 32 )  
        self.rect = self.surf.get_rect()

    def draw_debug(self, surface):
        super().draw_debug(surface)

        for v in self.explosion_vectors:
            self.draw_debug_vector(surface, v, (0,0,255), 1)

    def on_draw(self, surf: pygame.Surface):
        n = 9
        for i in range(0, 9):        
            angle = 2 * pi/n * i
            start = vec_polar(angle, (self.age / self.max_age) * 15)
            end = start + vec_polar(angle, (self.age / self.max_age) * 25)
            colour =  (255,255,0, int((1-min(self.age / self.max_age, 1)) * 255))
            Polygon.line(start, end).center_in_surface(surf).draw(surf, colour, 1)

    def on_update(self, engine: GameEngine, time):

        if self.age > self.max_age:
            self.dead = True
            return

        self.explosion_vectors = []
        for p in engine.particles_near(self.body.position, 100):
            distance_v =  (p.body.position - self.body.position)
            distance_sqrd = distance_v.get_length_sqrd()
            self.explosion_vectors.append(distance_v)

            # print("explode with 1/", distance_sqrd)

            if distance_sqrd <= 0:
                continue

            p.body.apply_impulse_at_local_point(
                vec_polar(distance_v.angle, self.force/distance_sqrd),
            )
    #     return super().on_update(surf)
