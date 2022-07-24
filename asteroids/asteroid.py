from __future__ import annotations
from math import cos, pi, sin, sqrt
from typing import List, Tuple
import pygame

# To randomize coin placement
from random import randint, random, uniform

# To find your assets
from pathlib import Path

from pymunk import Vec2d

from .particle import Particle
from .explosion import Explosion
from .engine import GameEngine
from .maths import vec_polar
from .polygon import Polygon
from .constants import COLLISION_TYPE_ASTEROID, WHITE

# Define the Coin sprite
class Asteroid(Particle):
    MIN_MASS = 1e11 * 5
    MAX_MASS = 1e13
    MAX_SIZE = 20
    MIN_SIZE = 2
    MIN_SPEED = 20
    MAX_SPEED = 200

    def randomized() -> Asteroid:
        velocity_m = Asteroid.MIN_SPEED + (random() * (Asteroid.MAX_SPEED - Asteroid.MIN_SPEED))
        velocity_v = Vec2d(cos(random() * 2 * pi) * velocity_m, sin(random() * 2 * pi) * velocity_m) 
        mass = uniform(Asteroid.MIN_SIZE, Asteroid.MAX_MASS)
    
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
        return Asteroid.MIN_SIZE + (Asteroid.MAX_SIZE * sqrt(mass/Asteroid.MAX_MASS))

    def __init__(self, mass, velocity, position):
        size = Asteroid.size_from_mass(mass)
        self.poly = Polygon.circle(size, 
            segments=int(8 + (size/Asteroid.MAX_SIZE * 8)), 
            randomize_radius_factor=0.9)

        super(Asteroid, self).__init__(
            mass=mass,
            vertices=self.poly.points
        )

        # self.body.velocity = 
        self.shape.elasticity = 0.8
        self.shape.friction = 0.2
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

    def hit(self, engine: GameEngine, by: Particle, ke: float):            
        health_impact = sqrt(ke / self.mass)/1000
        self.health -= health_impact
        # print('health', self, self.health, "{:.2e}".format(self.mass), "{:.2e}".format(ke), "{:.2e}".format(health_impact))

        max_min_colour = int(max(min(self.health * 255, 255), 0))
        self.colour = (255, max_min_colour, max_min_colour, 255)

        if self.health > 0:
            return

        self.dead = True
        engine.add(Explosion(self.body.position))

        if self.mass < Asteroid.MIN_MASS:
            return

        self.spawn_smaller_asteroids(engine, ke=ke)


    def on_update(self, surf: pygame.Surface, time: float):
        super().on_update(surf, time)

        # self.poly.rotate(self.body.angle).draw(surf, width=1)

        # Create the collision mask (anything not transparent)
        self.mask = pygame.mask.from_surface( surf )  

    def spawn_smaller_asteroids(self, engine: GameEngine, ke: float = 0):
        fragments = randint(2,4)
        even_mass = self.mass / fragments
    
        for i in range(0,fragments):
            actual_mass = even_mass/2 + (random() * even_mass/2)
            random_angle = random() * 2 * pi
            random_vector = self.body.position + vec_polar(random_angle, 15)
            velocity_v = vec_polar(random_angle, random() * 2e2) # * ke/fragments)
            a = Asteroid(actual_mass, velocity_v, random_vector)
            engine.add(a)
            # a.body.apply_impulse_at_world_point(impulse_v, a.body.position)

        self.dead = True