from math import pi, sqrt
from random import randint
from typing import Tuple
from pathlib import Path

from iniconfig import SectionWrapper

from .engine.particle import Particle
from .engine.scene import Scene
import pygame
from pymunk import ShapeFilter, Vec2d
from asteroids.bullet import Bullet
from asteroids.explosion import Explosion
from .missile import Missile
from .maths import vec_polar
from .polygon import Polygon
from .constants import COLLISION_TYPE_PLAYER, WHITE
from enum import Enum
from asteroids.shield import Shield

SHIP_DAMAGE_MULTIPLIER = 0.5


class Weapon(Enum):
    BULLET_SINGLE = 1
    BULLET_DOUBLE = 2
    MISSILE = 3


# Define the Player sprite
class Player(Particle):
    SHIP_POLYGON = (
        Polygon([(-1, -1), (0, 1), (1, -1), (0, -0.5), (-1, -1)])
        .rotate(-1 / 2 * pi)
        .scale(15)
    )
    THRUST_POLYGON = (
        Polygon([(-0.4, 0.4), (0, 1), (0.4, 0.4), (0, -1)])
        .translate((0, -2))
        .rotate(-1 / 2 * pi)
        .scale(10)
    )

    def __init__(self, pos=(0, 0)):
        """Initialize the player sprite"""
        super(Player, self).__init__(
            mass=5000, vertices=self.SHIP_POLYGON.points, position=pos
        )

        # self.angle = -pi/2
        self.body.elasticity = 0.3
        surf_size = (100, 100)
        self.thrusting = False
        self.colour = (0, 255, 0)
        self.shape.collision_type = COLLISION_TYPE_PLAYER
        self.shape.filter = ShapeFilter(categories=COLLISION_TYPE_PLAYER)
        self.fire_rate = 0
        # self.last_bullet_side = 1
        self.health = 1
        self.current_weapon = Weapon.BULLET_SINGLE

        # create transparent background image
        self.surf = pygame.Surface(surf_size, pygame.SRCALPHA, 32)
        self.rect = self.surf.get_rect()

    def fire_bullet(self, scene: Scene, offset_from_center=0):
        b = Bullet(
            position=self.body.position
            + vec_polar(self.body.angle, 17)
            + vec_polar(self.body.angle + pi / 2, offset_from_center),
            angle=self.body.angle,
            velocity=self.body.velocity,
        )
        # self.last_bullet_side *= -1
        scene.add(b)
        impulse_m = self.body.velocity.length + 2e3
        impulse_v = vec_polar(0, impulse_m)
        self.body.apply_impulse_at_local_point(-impulse_v)
        b.body.apply_impulse_at_local_point(impulse_v)

    def handle_keys(self, scene: Scene):
        # Handle keyboard
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_UP]:
            self.thrusting = True
            force_v = vec_polar(self.body.angle, self.mass * 5)
            self.body.apply_impulse_at_world_point(force_v, self.body.position)
        else:
            self.thrusting = False

        # Select weapon
        if keys_pressed[pygame.K_1]:
            self.current_weapon = Weapon.BULLET_SINGLE
        elif keys_pressed[pygame.K_2]:
            self.current_weapon = Weapon.BULLET_DOUBLE
        elif keys_pressed[pygame.K_3]:
            self.current_weapon = Weapon.MISSILE

        if keys_pressed[pygame.K_SPACE]:
            self.fire_rate += 1

            if self.fire_rate % 4 == 0:
                if self.current_weapon == Weapon.BULLET_SINGLE:
                    self.fire_bullet(scene, 0)
                elif self.current_weapon == Weapon.BULLET_DOUBLE:
                    for i in [-4, 4]:
                        self.fire_bullet(scene, i)
                elif self.current_weapon == Weapon.MISSILE:
                    self.fire_rate += 1

                    if self.fire_rate % 10 == 0:
                        b = Missile(
                            position=self.body.position
                            + vec_polar(self.body.angle, 20),
                            angle=self.body.angle,
                            velocity=self.body.velocity,
                        )
                        scene.add(b)
                        # impulse_m = self.body.velocity.length + 1e3
                        # impulse_v = vec_polar(pi/2, impulse_m)
                        # b.body.apply_impulse_at_local_point(impulse_v)

        if keys_pressed[pygame.K_LSHIFT]:
            scene.add(Shield(player=self))

        if keys_pressed[pygame.K_LEFT]:
            self.body.angular_velocity = 0
            self.body.angle -= pi / 20

        if keys_pressed[pygame.K_RIGHT]:
            self.body.angular_velocity = 0
            self.body.angle += pi / 20

    def on_collision(self, scene: Scene, by: Particle, ke: float) -> bool:
        health_impact = sqrt(ke / self.mass) / 1000
        self.health -= health_impact * SHIP_DAMAGE_MULTIPLIER

        # max_min_colour = int(max(min(self.health * 255, 255), 0))
        # self.colour = (255, max_min_colour, max_min_colour, 255)

        if self.health > 0:
            return False

        self.dead = True
        scene.add(Explosion(self.body.position))
        return True

    def on_update(self, scene: Scene, time: float):
        self.handle_keys(scene)

        return super().on_update(scene, time)

    def on_draw(self, surf: pygame.Surface):
        super().on_draw(surf)

        # self.SHIP_POLYGON.rotate(self.body.angle - pi/2).draw(surf)

        if self.thrusting:
            self.THRUST_POLYGON.rotate(self.body.angle).center_in_surface(surf).draw(
                surf
            )
