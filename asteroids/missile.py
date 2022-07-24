from math import pi
from typing import Tuple
from pathlib import Path
import pygame
from pymunk import Vec2d

from .particle import Particle
from asteroids.polygon import Polygon, move_poly, scale_poly, rotate_poly 
from .constants import COLLISION_TYPE_ORDANANCE, WHITE

# Define the Player sprite
class Missile(Particle):
    BULLET_POLYGON = Polygon([(-0.2, -1), (-0.2, 1), (0.2, 1), (0.2, -1)]).rotate(-1/2*pi).scale(5)

    def __init__(self, position=(0,0), angle=0, velocity=(0,0)):
        """Initialize the player sprite"""
        super(Missile, self).__init__(
            mass=1e12,
            vertices=self.BULLET_POLYGON.points, 
            position=position)

        # self.angle = -pi/2
        self.body.angle = angle
        self.body.velocity = velocity
        self.body.elasticity = 0
        self.shape.collision_type = COLLISION_TYPE_ORDANANCE
        self.shape.particle = self
        self.colour = (200,100,0)

        # create transparent background image
        self.surf = pygame.Surface( (10,10), pygame.SRCALPHA, 32 )  
        self.rect = self.surf.get_rect()
