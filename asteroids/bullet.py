from cmath import pi
import math
from typing import Tuple
from pathlib import Path
import pygame
from pymunk import Vec2d

from asteroids.physics import Particle
from asteroids.polygon import Polygon, move_poly, scale_poly, rotate_poly 
from .constants import WHITE

# Define the Player sprite
class Bullet(Particle):
    BULLET_POLYGON = Polygon([(-0.2, -1), (-0.2, 1), (0.2, 1), (0.2, -1)]).rotate(-1/2*pi).scale(5)

    def __init__(self, position=(0,0), angle=0, velocity=(0,0)):
        """Initialize the player sprite"""
        super(Bullet, self).__init__(
            mass=1e12,
            vertices=self.BULLET_POLYGON.points, 
            position=position)

        # self.angle = -pi/2
        self.body.angle = angle
        self.body.velocity = velocity
        self.body.elasticity = 0

        # create transparent background image
        self.surf = pygame.Surface( (10,10), pygame.SRCALPHA, 32 )  
        self.rect = self.surf.get_rect()
