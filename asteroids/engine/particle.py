from __future__ import annotations
from math import degrees
from this import d
from typing_extensions import Self

from pygame import Rect
import pymunk as pm
from pymunk import Arbiter, Vec2d, pygame_util
import pygame

# from asteroids.engine import GameEngine
from asteroids.polygon import move
from asteroids.constants import WHITE
from functools import reduce


class Particle(pygame.sprite.Sprite):
    def __init__(self, mass, vertices, position=(0, 0)) -> None:
        super(Particle, self).__init__()
        # self.angle = -pi/2
        self.mass = mass  # 1kg
        # self.position = Vector.from_cartesian(0,0)
        # self.impulse = Vector()
        # self.velocity = Vector()
        self.colour = WHITE
        moment = pm.moment_for_poly(self.mass, vertices)
        if moment < 0:
            moment = 1
        self.body = pm.Body(self.mass, moment)
        self.shape = pm.Poly(self.body, vertices)
        self.shape.friction = 0.9
        self.body.position = position
        self.force_vectors = []
        self.age = 0
        self.health = 1.0
        self.dead = False

        # If false, doesnt experience physics
        self.is_physical = True
        self.is_movable = True

    def draw_debug_vector(
        self, surf: pygame.Surface, vector: Vec2d, color, width=1, text=None
    ):
        if vector.length == 0:
            return

        pygame.draw.line(
            surf, color, self.body.position, self.body.position + vector, width
        )

        if text:
            text_surface = pygame.font.SysFont("arial", 10, bold=False).render(
                text, True, color
            )
            text_surface = pygame.transform.rotate(text_surface, -degrees(vector.angle))
            surf.blit(
                text_surface,
                self.body.position
                + vector
                + vector.perpendicular_normal() * 10
                - text_surface.get_rect().center,
            )

    def draw_shape(self, surf, shape, colour, width=1):
        size = surf.get_size()
        ps = [
            pos.rotated(shape.body.angle) + Vec2d(size[0] / 2, size[1] / 2)
            for pos in shape.get_vertices()
        ]
        # ps += [ps[0]]
        pygame.draw.polygon(surf, colour, ps, width=width)

    def draw_debug(self, surf: pygame.Surface):
        # self.draw_vector(debug_surf, self.impulse, (255,0,0))
        self.draw_debug_vector(surf, self.body.velocity, (0, 255, 0), text="VELOCITY")
        self.draw_debug_vector(surf, self.body.force, (255, 0, 0), text="FORCE")
        # self.draw_debug_vector(surf, self.force, (0, 0, 255), text="GRAVITY")

        for v, label in self.force_vectors:
            self.draw_debug_vector(
                surf, v.scale_to_length(100), (0, 0, 128, 128), text=label.upper()
            )

    def draw(self):
        self.rect.center = self.body.position
        empty = pygame.Color(0, 0, 0, 0)
        # The last 0 indicates 0 alpha, a transparent color
        self.surf.fill(empty)

        self.on_draw(self.surf)

        # Create the collision mask (anything not transparent)
        self.mask = pygame.mask.from_surface(self.surf)

    def on_draw(self, surf: pygame.Surface):
        self.draw_shape(self.surf, self.shape, self.colour)
        pass

    def on_collision(self, scene, by: Self, ke: float) -> bool:
        pass

    def on_update(self, scene, time: float):
        pass

    def on_start_tick(self, scene, time: float):
        self.force_vectors = []
        pass

    def apply_force(self, force: Vec2d, label: str):
        if self.is_movable:
            # print("Apply", label, force, "to", self)
            self.force_vectors.append((force, label))

    def tick(self, scene, time):
        self.on_update(scene, time)

        if self.force_vectors:
            # print("Forces for", self, "have", len(self.force_vectors), "forces")
            force = reduce(
                lambda a, b: a + b, [f for f, _ in self.force_vectors], Vec2d.zero()
            )
            self.body.apply_impulse_at_world_point(force, self.body.position)

        self.age += time
