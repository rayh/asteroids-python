from cmath import pi
import math
from typing import Tuple
from pathlib import Path
import pygame
from pymunk import Vec2d
from asteroids.bullet import Bullet

from asteroids.physics import Particle
from asteroids.polygon import Polygon, move_poly, scale_poly, rotate_poly 
from .constants import WHITE

# Define the Player sprite
class Player(Particle):
    SHIP_POLYGON = Polygon([(-1, -1), (0, 1), (1, -1), (0, -0.5), (-1, -1)]).rotate(-1/2*pi).scale(15)
    THRUST_POLYGON = Polygon([(-0.4, 0.4), (0, 1), (0.4, 0.4), (0, -1)]).move((0,-2)).rotate(-1/2*pi).scale(10)

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

        # create transparent background image
        self.surf = pygame.Surface( surf_size, pygame.SRCALPHA, 32 )  
        self.rect = self.surf.get_rect()

    def handle_keys(self, engine):
        # Handle keyboard
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_UP]:
            self.thrusting = True   
            force_v = (
                math.cos(self.body.angle) * self.mass * 2, 
                math.sin(self.body.angle) * self.mass * 2
            )
            self.body.apply_impulse_at_world_point(force_v, self.body.position)
        else:
            self.thrusting = False

        if keys_pressed[pygame.K_SPACE]:
            velocity_m = self.body.velocity.length + 100
            velocity_v = Vec2d(math.cos(self.body.angle) * velocity_m, math.sin(self.body.angle) * velocity_m)
            engine.add(Bullet(
                position=self.body.position, 
                angle=self.body.angle, 
                velocity=velocity_v))

        if keys_pressed[pygame.K_LEFT]:
            self.body.angular_velocity=0
            self.body.angle-=pi/20

        if keys_pressed[pygame.K_RIGHT]:
            self.body.angular_velocity=0
            self.body.angle+=pi/20

    def on_update(self, surf):
        # self.SHIP_POLYGON.rotate(self.body.angle - pi/2).draw(surf)

        if self.thrusting:
            self.THRUST_POLYGON.rotate(self.body.angle).draw(surf)
