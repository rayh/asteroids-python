from cmath import pi
import math
from typing import Tuple
from pathlib import Path
import pygame
from pymunk import Vec2d

from asteroids.physics import Particle
from asteroids.polygon import Polygon, move_poly, scale_poly, rotate_poly 
from .constants import COLLISION_TYPE_ORDANANCE, WHITE

# Define the Player sprite
class Explosion(Particle):
    EXPLOSION_POLYGON = Polygon.circle(5, 10, randomize_radius_factor=0.5)

    def __init__(self, position=(0,0), extra_power=0):
        """Initialize the player sprite"""
        super(Explosion, self).__init__(
            mass=1,
            vertices=self.EXPLOSION_POLYGON.points, 
            position=position)

        # self.angle = -pi/2
        self.body.angle = 0
        self.body.velocity = Vec2d.zero()
        self.colour = (255,0,0)

        # create transparent background image
        self.surf = pygame.Surface( (30,30), pygame.SRCALPHA, 32 )  
        self.rect = self.surf.get_rect()

    def on_update(self, surf: pygame.Surface):
        if self.age > 0.5:
            self.dead = True
        return super().on_update(surf)
