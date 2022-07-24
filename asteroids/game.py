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
from asteroids.collisions import asteroid_hits_asteroid, bullet_hits_asteroid

from .player import Player
from .asteroid import Asteroid
from .engine import GameEngine
from .particle import Particle

def main_loop():
    FPS = 30

    # Set the width and height of the output window, in pixels
    WIDTH = 800
    HEIGHT = 600

    def handle_collision_pair(engine: GameEngine, p1: Particle, p2: Particle, arbiter: Arbiter):
        # impulse_v = arbiter.total_impulse * -1 * 1e12
        # p.body.apply_impulse_at_world_point(
        #     impulse_v, 
        #     p.body.position)
        # print('Apply', self, impulse_v, 'to', p)

        if type(p1) == Asteroid and type(p2) == Bullet:
            bullet_hits_asteroid(engine, p2, p1, arbiter)
            return

        if type(p2) == Asteroid and type(p1) == Bullet:
            bullet_hits_asteroid(engine, p1, p2, arbiter)
            return

        if type(p1) == Asteroid and type(p2) == Asteroid:
            asteroid_hits_asteroid(engine, p1, p2, arbiter)
            return 
   
    engine = GameEngine((WIDTH, HEIGHT)) 
    engine.on_collision_pair = handle_collision_pair

    # Initialize the score
    score = 0

    # Set up the coin pickup sound
    # coin_pickup_sound = pygame.mixer.Sound(
    #     str(Path.cwd() / "pygame" / "sounds" / "coin_pickup.wav")
    # )

    # Create a player sprite and set its initial position
    player = Player(pos=(WIDTH/2, HEIGHT/2))
    engine.add(player)

    asteroids = pygame.sprite.Group()
    for i in range(0,20):
        asteroid = Asteroid.randomized()
        asteroids.add(asteroid)
        engine.add(asteroid)


    # Run until you get to an end condition
    running = True
    while running:
        player.handle_keys(engine)

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        engine.tick(time=1/FPS)

        # To render the screen, first fill the background with pink
        engine.screen.fill((0, 0, 40))
        engine.render(debug=False)

        # Finally, draw the score at the bottom left
        score_font = pygame.font.SysFont("any_font", 36)
        score_block = score_font.render(f"Objects: {len(engine.particles)}", False, (255,255,255))
        engine.screen.blit(score_block, (50, HEIGHT - 50))

        # Flip the display to make everything appear
        pygame.display.flip()

    # Done! Print the final score
    print(f"Game over! Final score: {score}")

    # Make the mouse visible again
    pygame.mouse.set_visible(True)

    # Quit the game
    pygame.quit()