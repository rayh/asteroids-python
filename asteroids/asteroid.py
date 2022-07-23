from math import pi
from typing import Tuple
import pygame

# To randomize coin placement
from random import randint, random

# To find your assets
from pathlib import Path

from asteroids.physics import Particle, Vector

from .constants import WHITE

# Define the Coin sprite
class Asteroid(Particle):
    def __init__(self):
        """Initialize the coin sprite"""
        super(Asteroid, self).__init__()

        self.mass = random() * 10e9
        # The starting position is randomly generated
        width, height = pygame.display.get_window_size()
        self.position = Vector.from_cartesian(
            randint(10, width - 10),
            randint(10, height - 10)
        )
        self.velocity = Vector(a=random() * pi * 2, m=random() * 20)


        # Get the image to draw for the coin
        # coin_image = str(Path.cwd() / "pygame" / "images" / "coin_gold.png")

        # Load the image, preserve alpha channel for transparency
        # self.surf = pygame.image.load(coin_image).convert_alpha()

        total_size = self.mass / 1e8
        size = (total_size, total_size)

        # create transparent background image
        self.surf = pygame.Surface( size, pygame.SRCALPHA, 32 )  

        self.rect = self.surf.get_rect(
            center=self.position.to_cart()
        )

    def on_update(self, surf):
        total_size = self.mass / 1e8
        pygame.draw.circle(surf, WHITE, (total_size/2, total_size/2), total_size/2, 1)  # Position is the center of the circle.

        # Create the collision mask (anything not transparent)
        self.mask = pygame.mask.from_surface( surf )  
