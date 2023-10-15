from math import pi
from typing import List, Tuple
from pathlib import Path
import pygame
from pymunk import Arbiter, ShapeFilter, Vec2d
from asteroids.asteroid import Asteroid
from asteroids.explosion import Explosion

from .engine.particle import Particle
from .engine.scene import Scene
from asteroids.polygon import Polygon, move_poly, scale_poly, rotate_poly
from .constants import COLLISION_TYPE_FRIENDLY, WHITE


# Define the Player sprite
class Bullet(Particle):
    BULLET_POLYGON = (
        Polygon([(-0.1, -1), (-0.1, 1), (0.1, 1), (0.1, -1)])
        .rotate(-1 / 2 * pi)
        .scale(3)
    )

    def __init__(self, position=(0, 0), angle=0, velocity=(0, 0)):
        """Initialize the player sprite"""
        super(Bullet, self).__init__(
            mass=5, vertices=self.BULLET_POLYGON.points, position=position
        )

        # self.angle = -pi/2
        self.body.angle = angle
        self.body.velocity = velocity
        self.body.elasticity = 0
        self.shape.collision_type = COLLISION_TYPE_FRIENDLY
        self.shape.filter = ShapeFilter(
            mask=ShapeFilter.ALL_MASKS() ^ COLLISION_TYPE_FRIENDLY
        )
        self.colour = (255, 0, 0)

        # create transparent background image
        self.surf = pygame.Surface((10, 10), pygame.SRCALPHA, 32)
        self.rect = self.surf.get_rect()

    def on_update(self, scene: Scene, time: float):
        super().on_update(scene, time)
        if self.age > 5:
            self.dead = True
