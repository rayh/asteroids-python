from math import pi
from random import uniform
from typing import Tuple
from pathlib import Path
import pygame
from pymunk import Vec2d

from .particle import Particle
from .maths import vec_polar
from asteroids.polygon import Group, Polygon, move_poly, scale_poly, rotate_poly 
from .constants import COLLISION_TYPE_ORDANANCE, WHITE

# Define the Player sprite
class Explosion(Particle):
    def __init__(self, position=(0,0), extra_power=0):
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

        # create transparent background image
        self.surf = pygame.Surface( (100,100), pygame.SRCALPHA, 32 )  
        self.rect = self.surf.get_rect()

    def on_update(self, surf: pygame.Surface, time):
        n = 9
        for i in range(0, 9):        
            angle = 2 * pi/n * i
            start = vec_polar(angle, (self.age / self.max_age) * 15)
            end = start + vec_polar(angle, (self.age / self.max_age) * 30)
            colour =  (255,0,0, int((1-min(self.age / self.max_age, 1)) * 255))
            shape = Polygon.line(start, end)
            shape.draw(surf, colour, 1)

        if self.age > self.max_age:
            self.dead = True
    #     return super().on_update(surf)
