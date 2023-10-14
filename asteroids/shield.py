from math import pi
from random import uniform
from typing import Tuple
from pathlib import Path
import pygame
from pymunk import Vec2d

from .engine.particle import Particle
from .engine.scene import Scene
from .maths import vec_polar
from asteroids.polygon import Group, Polygon, move_poly, scale_poly, rotate_poly
from .constants import WHITE


class Shield(Particle):
    def __init__(self, player: Particle):
        self.player = player
        super(Shield, self).__init__(
            mass=1, vertices=Polygon.circle(40).points, position=player.body.position
        )
        self.colour = (100, 100, 255)
        self.is_physical = True
        self.max_age = 3

        self.surf = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
        self.rect = self.surf.get_rect()

    def on_update(self, scene: Scene, time):
        self.body.position = self.player.body.position
