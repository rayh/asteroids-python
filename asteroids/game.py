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
from asteroids.collisions import asteroid_hits_asteroid, bullet_hits_asteroid, missile_hits_asteroid
from asteroids.missile import Missile

from .player import Player
from .asteroid import Asteroid
from .engine import GameEngine
from .particle import Particle

def main_loop():

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

        if type(p1) == Asteroid and type(p2) == Missile:
            missile_hits_asteroid(engine, p2, p1, arbiter)
            return

        if type(p2) == Asteroid and type(p1) == Missile:
            missile_hits_asteroid(engine, p1, p2, arbiter)
            return
   
    engine = GameEngine(fps=30) 
    engine.on_collision_pair = handle_collision_pair

    # Initialize the score
    score = 0

    # Set up the coin pickup sound
    # coin_pickup_sound = pygame.mixer.Sound(
    #     str(Path.cwd() / "pygame" / "sounds" / "coin_pickup.wav")
    # )

    # Create a player sprite and set its initial position
    screen_size = engine.screen.get_size()
    player = Player(pos=(screen_size[0]/2, screen_size[1]/2))
    engine.add(player)

    asteroids = pygame.sprite.Group()
    for i in range(0,5):
        asteroid = Asteroid.randomized()
        asteroids.add(asteroid)
        engine.add(asteroid)


    # Run until you get to an end condition
    running = True
    debug = False
    while running:
        player.handle_keys(engine)

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_TAB]:
            engine.change_rate(0.01)
        else:
            engine.change_rate(1)

        if keys_pressed[pygame.K_d]:
            debug = True
        else:
            debug = False

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        engine.tick()

        # To render the screen, first fill the background with pink
        engine.screen.fill((0, 0, 40))

        if engine.elapsed_time < 3:
            # Finally, draw the score at the bottom left
            title_font = pygame.font.SysFont("arialblack", 150)
            alpha = int(255 * (1 - (engine.elapsed_time/3)))
            title_block = title_font.render(f"Asteroids!", True, (255,255,255,255))
            title_block.set_alpha(alpha)
            title_size = title_block.get_size()
            engine.screen.blit(title_block, (screen_size[0]/2 - title_size[0]/2 , screen_size[1]/2 - title_size[1]/2))

        engine.render(debug=debug)

        # Finally, draw the score at the bottom left
        score_font = pygame.font.SysFont("arialblack", 36)
        score_block = score_font.render(f"Objects: {len(engine.particles)}", True, (255,255,255))
        engine.screen.blit(score_block, (50, screen_size[1] - 50))

        # Flip the display to make everything appear
        pygame.display.flip()

    # Done! Print the final score
    print(f"Game over! Final score: {score}")

    # Make the mouse visible again
    pygame.mouse.set_visible(True)

    # Quit the game
    pygame.quit()