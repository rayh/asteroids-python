from __future__ import annotations
from math import cos, pi, sin
from typing import List, Tuple
import pygame

# To randomize coin placement
from random import randint, random

# To find your assets
from pathlib import Path

from pymunk import Arbiter, Vec2d

from .physics import Particle, PhysicsEngine, vec_polar
from .polygon import Polygon
from .constants import COLLISION_TYPE_ASTEROID, WHITE

# Define the Coin sprite
class Asteroid(Particle):
    MIN_MASS = 1e11 * 5
    MAX_MASS = 1e13
    MAX_SIZE = 15
    MIN_SIZE = 3
    MIN_SPEED = 10
    MAX_SPEED = 50

    def randomized() -> Asteroid:
        velocity_m = Asteroid.MIN_SPEED + (random() * (Asteroid.MAX_SPEED - Asteroid.MIN_SPEED))
        velocity_v = Vec2d(cos(random() * 2 * pi) * velocity_m, sin(random() * 2 * pi) * velocity_m) 
        mass = Asteroid.MAX_MASS/10 + (random() * Asteroid.MAX_MASS/10*9)

        width, height = pygame.display.get_window_size()
        position = (
            randint(10, width - 10),
            randint(10, height - 10)
        )

        return Asteroid(
            mass=mass,
            velocity=velocity_v,
            position=position
        )

    def size_from_mass(mass: float) -> float:
        return Asteroid.MIN_SIZE + (Asteroid.MAX_SIZE-Asteroid.MIN_SIZE) * mass/Asteroid.MAX_MASS

    def __init__(self, mass, velocity, position):
        self.poly = Polygon.circle(Asteroid.size_from_mass(mass), segments=15, randomize_radius_factor=1)

        super(Asteroid, self).__init__(
            mass=mass,
            vertices=self.poly.points
        )

        # self.body.velocity = 
        self.body.elasticity = 0.4
        self.body.velocity = velocity
        self.body.angular_velocity = (random() * 2 * pi) - pi
        self.shape.collision_type = COLLISION_TYPE_ASTEROID

        # The starting position is randomly generated
        self.body.position = position

        # create transparent background image
        self.surf = pygame.Surface( (150,150), pygame.SRCALPHA, 32 )  

        self.rect = self.surf.get_rect(
            center=self.body.position
        )

    def on_update(self, surf):
        if self.mass < Asteroid.MIN_MASS:
            self.dead = True

        # self.poly.rotate(self.body.angle).draw(surf, width=1)

        # Create the collision mask (anything not transparent)
        self.mask = pygame.mask.from_surface( surf )  

    def spawn_smaller_asteroids(self, engine: PhysicsEngine, ke: float = 0):
        fragments = randint(2,5)
        even_mass = self.mass / fragments
    
        for i in range(0,fragments):
            actual_mass = even_mass/2 + (random() * even_mass/2)
            if actual_mass < Asteroid.MIN_MASS:
                continue

            random_angle = random() * 2 * pi
            random_vector = self.body.position + vec_polar(random_angle, 10)
            velocity_v = vec_polar(random_angle, random() * 1e2) # * ke/fragments)
            a = Asteroid(actual_mass, velocity_v, random_vector)
            engine.add(a)
            # a.body.apply_impulse_at_world_point(impulse_v, a.body.position)

        self.dead = True