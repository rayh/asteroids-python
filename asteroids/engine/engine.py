from __future__ import annotations
from functools import reduce
from math import cos, pi, sin
from random import random
from this import d
from typing import List, Tuple

from pygame import Rect
import pymunk as pm
from pymunk import Arbiter, ShapeFilter, Vec2d, pygame_util
import pygame

from asteroids.engine.scene import Scene

pygame_util.positive_y_is_up = False

# def atan_div(opp, adj) -> float:
#     if (opp != 0 and adj != 0):
#         return atan(opp / adj)
#     elif (opp != 0):
#         if(opp > 0):
#             return 3/2 * pi
#         else:
#             return 1/2 * pi
#     else:
#         if(adj > 0):
#             return pi
#         else:
#             return 0

# class Vector:
#     def __init__(self, m=0, a=0) -> None:
#         self.a = a
#         self.m = m

#     def dot(self, scalar) -> Vector:
#         return Vector(m=self.m * scalar, a=self.a)

#     def to_cart(self) -> Tuple(float, float):
#         y = sin(self.a) * self.m
#         x = cos(self.a) * self.m

#         return (x, y)

#     # def distance(self, v: Vector) -> float:
#     #     return sqrt(self.m**2 + v.m**2 - (2*self.m*v.m * cos(self.a - v.a)))

#     # see https://math.stackexchange.com/questions/1365622/adding-two-polar-vectors
#     def add(self, v: Vector) -> Vector:
#         m = sqrt(self.m**2 + v.m**2 + (2*self.m*v.m * cos(v.a - self.a)))
#         a = self.a + atan2(v.m * sin(v.a - self.a), self.m + v.m * cos(v.a - self.a))
#         return Vector(m, a)

#     def subtract(self, v: Vector) -> Vector:
#         return self.add(v.dot(-1))

#     def from_cartesian(x: float, y: float) -> Vector:
#         a = atan2(y, x)
#         m = sqrt(x**2 + y**2)
#         return Vector(m, a)

#     def __str__(self) -> str:
#         return str(self.to_cart())


class GameEngine:
    def __init__(self, fps=60) -> None:
        self.fps = fps
        self.elapsed_time = 0

        # Initialize the Pygame engine
        pygame.init()

        # modes = pygame.display.list_modes()
        mode = (1200, 800)
        print("Using ", mode)

        # Set up the drawing window
        self.screen = pygame.display.set_mode(size=mode)  # , flags=pygame.FULLSCREEN)
        self.debug_surf = pygame.Surface(mode, pygame.SRCALPHA)
        self.game_surf = pygame.Surface(mode, pygame.SRCALPHA)
        self.background_colour = (0, 0, 0)

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

        # Set up the clock for a decent frame rate
        self.clock = pygame.time.Clock()

        self.tick_time = 1 / fps
        self.scene = None

        self.change_scene(Scene())

    def change_scene(self, scene: Scene):
        if self.scene:
            self.scene.teardown(self)

        self.scene = scene
        self.scene.setup(self)

    def change_rate(self, rate=1):
        self.tick_time = rate / self.fps

    def render(self, debug=False):
        if debug:
            empty = pygame.Color(0, 0, 0, 0)
            self.debug_surf.fill(empty)

        self.game_surf.fill(self.background_colour)

        self.scene.render(self.game_surf, self.debug_surf, debug=debug)

        draw_rect = self.game_surf.get_rect()
        draw_rect.center = self.screen.get_rect().center
        self.screen.blit(self.game_surf, draw_rect)

        if debug:
            draw_rect = self.debug_surf.get_rect()
            draw_rect.center = self.screen.get_rect().center
            self.screen.blit(self.debug_surf, draw_rect)

    def quit(self):
        # Make the mouse visible again
        pygame.mouse.set_visible(True)

        # Quit the game
        pygame.quit()

    def add(self, object):
        self.scene.add(object)

    def remove(self, object):
        self.scene.remove(object)

    def tick(self):
        time = self.tick_time
        self.scene.tick(self, time)
        self.clock.tick(1 / time)
        self.elapsed_time += time
