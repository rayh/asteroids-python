from math import pi
from typing import Tuple
from pathlib import Path
from asteroids.engine import GameEngine
import pygame
from pymunk import Vec2d
from asteroids.bullet import Bullet

from .maths import vec_polar
from .particle import Particle
from .polygon import Polygon 
from .constants import COLLISION_TYPE_PLAYER, WHITE

# Define the Player sprite
class Player(Particle):
    SHIP_POLYGON = Polygon([(-1, -1), (0, 1), (1, -1), (0, -0.5), (-1, -1)]).rotate(-1/2*pi).scale(15)
    THRUST_POLYGON = Polygon([(-0.4, 0.4), (0, 1), (0.4, 0.4), (0, -1)]).translate((0,-2)).rotate(-1/2*pi).scale(10)

    def __init__(self, pos=(0,0)):
        """Initialize the player sprite"""
        super(Player, self).__init__(
            mass=5000,
            vertices=self.SHIP_POLYGON.points, 
            position=pos)

        # self.angle = -pi/2
        self.body.elasticity = 0.3
        surf_size = (100,100)
        self.thrusting = False
        self.colour = (0,255,0)
        self.shape.collision_type = COLLISION_TYPE_PLAYER

        # create transparent background image
        self.surf = pygame.Surface( surf_size, pygame.SRCALPHA, 32 )  
        self.rect = self.surf.get_rect()

    def handle_keys(self, engine: GameEngine):
        # Handle keyboard
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_UP]:
            self.thrusting = True   
            force_v = vec_polar(self.body.angle, self.mass * 5)
            self.body.apply_impulse_at_world_point(force_v, self.body.position)
        else:
            self.thrusting = False

        if keys_pressed[pygame.K_SPACE]:
            b = Bullet(
                position=self.body.position + vec_polar(self.body.angle, 20), 
                angle=self.body.angle, 
                velocity=Vec2d(0,0))
            engine.add(b)
            velocity_m = self.body.velocity.length + 1e3
            impulse_v = vec_polar(0, velocity_m)
            self.body.apply_impulse_at_local_point(-impulse_v)
            b.body.apply_impulse_at_local_point(impulse_v)

        if keys_pressed[pygame.K_LEFT]:
            self.body.angular_velocity=0
            self.body.angle-=pi/20

        if keys_pressed[pygame.K_RIGHT]:
            self.body.angular_velocity=0
            self.body.angle+=pi/20

    def on_update(self, surf: pygame.Surface, time: float):
        super().on_update(surf, time)
        # self.SHIP_POLYGON.rotate(self.body.angle - pi/2).draw(surf)

        if self.thrusting:
            self.THRUST_POLYGON.rotate(self.body.angle).draw(surf)
