from __future__ import annotations
from math import cos, pi, sin, sqrt
from typing import List, Tuple
import pygame

# To randomize coin placement
from random import randint, random, uniform

# To find your assets
from pathlib import Path

from pymunk import ShapeFilter, Vec2d

from .particle import Particle
from .explosion import Explosion
from .engine import GameEngine
from .maths import vec_polar
from .polygon import Polygon
from .constants import COLLISION_TYPE_ASTEROID, WHITE

# Define the Coin sprite
class Asteroid(Particle):
    MIN_MASS = 1e6
    MAX_MASS = 2e7
    MAX_SIZE = 50
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
            randomize_radius_factor=0.5)

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
        self.shape.filter = ShapeFilter(categories=COLLISION_TYPE_ASTEROID)

        # The starting position is randomly generated
        self.body.position = position

        # create transparent background image
        self.surf = pygame.Surface( (150,150), pygame.SRCALPHA, 32 )  

        self.rect = self.surf.get_rect(
            center=self.body.position
        )

    def hit(self, engine: GameEngine, by: Particle, ke: float) -> bool:            
        health_impact = sqrt(ke / self.mass)/1000
        self.health -= health_impact
        # print('health', self, self.health, "{:.2e}".format(self.mass), "{:.2e}".format(ke), "{:.2e}".format(health_impact))

        max_min_colour = int(max(min(self.health * 255, 255), 0))
        self.colour = (255, max_min_colour, max_min_colour, 255)

        if self.health > 0:
            return False

        self.dead = True

        engine.add(Explosion(self.body.position))

        if self.mass < Asteroid.MIN_MASS:
            return False

        self.spawn_smaller_asteroids(engine, ke=ke)
 
        return True

    def spawn_smaller_asteroids(self, engine: GameEngine, ke: float = 0):
        fragments = randint(2,4)
        even_mass = self.mass / fragments
    
        for i in range(0,fragments):
            actual_mass = even_mass/2 + (random() * even_mass/2)
            random_angle = random() * 2 * pi 
            random_vector = self.body.position + vec_polar(random_angle, 15)
            velocity_v = vec_polar(random_angle, random() * 2e2) # * ke/fragments)
            a = Asteroid(actual_mass, velocity_v + self.body.velocity, random_vector)
            engine.add(a)

        self.dead = True