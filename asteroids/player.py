from cmath import pi
import math
from typing import Tuple
from pathlib import Path
import pygame

from asteroids.physics import Particle, Vector
from asteroids.polygon import Polygon, move_poly, scale_poly, rotate_poly 
from .constants import WHITE

# Define the Player sprite
class Player(Particle):
    SHIP_POLYGON = Polygon([(-1, -1), (0, 1), (1, -1), (0, -0.5)]).rotate(-1/2*pi).scale(15)
    THRUST_POLYGON = Polygon([(-0.4, 0.4), (0, 1), (0.4, 0.4), (0, -1)]).move((0,-2)).rotate(-1/2*pi).scale(10)

    def __init__(self, pos=(0,0)):
        """Initialize the player sprite"""
        super(Player, self).__init__()

        self.size = 30
        self.angle = -pi/2
        self.mass = 5000 # 5000kg

        surf_size = (self.size*2, self.size*2)

        # create transparent background image
        self.surf = pygame.Surface( surf_size, pygame.SRCALPHA, 32 )  
        self.rect = self.surf.get_rect()
        self.rect.center = pos

    def handle_keys(self):
        # Handle keyboard
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_UP]:
            print("Up pressed")
            self.impulse = Vector(m=5000, a=self.angle)
        else:
            self.impulse = Vector()

        if keys_pressed[pygame.K_LEFT]:
            self.angle-=pi/20

        if keys_pressed[pygame.K_RIGHT]:
            self.angle+=pi/20

    def on_update(self, surf):
        self.SHIP_POLYGON.rotate(self.angle).draw(surf)

        if self.impulse.m > 0:
            self.THRUST_POLYGON.rotate(self.angle).draw(surf)
