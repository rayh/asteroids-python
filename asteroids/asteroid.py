from math import pi
from typing import Tuple
import pygame

# To randomize coin placement
from random import randint, random

# To find your assets
from pathlib import Path

from .physics import Particle
from .polygon import Polygon
from .constants import WHITE

# Define the Coin sprite
class Asteroid(Particle):
    MAX_MASS = 1e11
    def __init__(self):
        mass = self.MAX_MASS/10 + (random() * self.MAX_MASS/10*9)
        self.poly = Polygon.circle(10 + 20 * mass/self.MAX_MASS, segments=15, randomize_radius_factor=1)
        """Initialize the coin sprite"""
        super(Asteroid, self).__init__(
            mass=mass,
            vertices=self.poly.points
        )

        # self.body.velocity = 
        self.body.elasticity = 0.1
        self.body.angular_velocity = (random() * 2 * pi) - pi

        # The starting position is randomly generated
        width, height = pygame.display.get_window_size()
        self.body.position = (
            randint(10, width - 10),
            randint(10, height - 10)
        )

        # create transparent background image
        self.surf = pygame.Surface( (150,150), pygame.SRCALPHA, 32 )  

        self.rect = self.surf.get_rect(
            center=self.body.position
        )

    def on_update(self, surf):
        # self.poly.rotate(self.body.angle).draw(surf, width=1)

        # Create the collision mask (anything not transparent)
        self.mask = pygame.mask.from_surface( surf )  
