# Import and initialize the pygame library
import pygame

# To randomize coin placement
from random import randint

# To find your assets
from pathlib import Path

# For type hinting
from typing import Tuple

from pymunk import Arbiter

from asteroids.bullet import Bullet
from asteroids.collisions import (
    asteroid_hits_asteroid,
    bullet_hits_asteroid,
    missile_hits_asteroid,
    thing_hits_player,
)
from asteroids.engine.particle import Particle
from asteroids.missile import Missile
from asteroids.scenes.level import LevelScene

from .player import Player
from .asteroid import Asteroid
from .engine.engine import GameEngine


def main_loop():
    engine = GameEngine(fps=30)
    engine.background_colour = (0, 0, 40)

    # Initialize the score
    score = 0

    def setup_level() -> LevelScene():
        scene = LevelScene()
        engine.change_scene(scene)
        return scene

    # Run until you get to an end condition
    scene = setup_level()
    running = True
    debug = False
    while running:
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_TAB]:
            engine.change_rate(0.01)
        else:
            engine.change_rate(1)

        if keys_pressed[pygame.K_d]:
            debug = True
        else:
            debug = False

        keys_pressed = pygame.key.get_pressed()
        if scene.player.health <= 0 and keys_pressed[pygame.K_RETURN]:
            scene = setup_level()

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        engine.tick()

        engine.render(debug=debug)

        # Flip the display to make everything appear
        pygame.display.flip()

    # Done! Print the final score
    print(f"Game over! Final score: {score}")

    # Make the mouse visible again
    engine.quit()
