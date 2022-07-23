# Import and initialize the pygame library
import pygame

# To randomize coin placement
from random import randint

# To find your assets
from pathlib import Path

# For type hinting
from typing import Tuple

from .player import Player
from .asteroid import Asteroid
from .physics import PhysicsEngine

def main_loop():
    FPS = 30

    # Set the width and height of the output window, in pixels
    WIDTH = 800
    HEIGHT = 600
   
    physics = PhysicsEngine((WIDTH, HEIGHT)) 

    # Initialize the Pygame engine
    pygame.init()

    # Set up the drawing window
    screen = pygame.display.set_mode(size=[WIDTH, HEIGHT])

    # Hide the mouse cursor
    pygame.mouse.set_visible(False)

    # Set up the clock for a decent frame rate
    clock = pygame.time.Clock()

    # Create a custom event for adding a new coin
    # ADDCOIN = pygame.USEREVENT + 1
    # pygame.time.set_timer(ADDCOIN, coin_countdown)

    # Initialize the score
    score = 0

    # Set up the coin pickup sound
    # coin_pickup_sound = pygame.mixer.Sound(
    #     str(Path.cwd() / "pygame" / "sounds" / "coin_pickup.wav")
    # )

    # Create a player sprite and set its initial position
    player = Player(pos=(WIDTH/2, HEIGHT/2))
    physics.add(player)

    asteroids = pygame.sprite.Group()
    for i in range(1,20):
        asteroid = Asteroid()
        asteroids.add(asteroid)
        physics.add(asteroid)


    # Run until you get to an end condition
    running = True
    while running:
        player.handle_keys(physics)

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Should you add a new coin?
            # elif event.type == ADDCOIN:
            #     # Create a new coin and add it to the coin_list
            #     new_coin = Asteroid()
            #     coin_list.add(new_coin)

            #     # Speed things up if fewer than three coins are on-screen
            #     if len(coin_list) < 3:
            #         coin_countdown -= coin_interval
            #     # Need to have some interval
            #     if coin_countdown < 100:
            #         coin_countdown = 100

            #     # Stop the previous timer by setting the interval to 0
            #     pygame.time.set_timer(ADDCOIN, 0)

                # Start a new timer
                # pygame.time.set_timer(ADDCOIN, coin_countdown)

        # Update the player position
        # player.update(pygame.mouse.get_pos())

        # Check if the player has collided with a coin, removing the coin if so
        # collisions = pygame.sprite.spritecollide(
        #     sprite=player, group=asteroids, dokill=True
        # )
        # for collision in collisions:
        #     # Each coin is worth 10 points
        #     score += 10
        #     # Play the coin collected sound
        #     # coin_pickup_sound.play()
        #     print("Collision!!")

        physics.tick(time=1/FPS)

        # Are there too many coins on the screen?
        if len(asteroids) == 0:
            # This counts as an end condition, so you end your game loop
            running = False

        # To render the screen, first fill the background with pink
        screen.fill((255, 170, 164))
        for p in physics.particles:
            p.draw_screen(screen, debug=True)

        # Finally, draw the score at the bottom left
        score_font = pygame.font.SysFont("any_font", 36)
        score_block = score_font.render(f"Score: {score}", False, (0, 0, 0))
        screen.blit(score_block, (50, HEIGHT - 50))

        # Flip the display to make everything appear
        pygame.display.flip()

        # Ensure you maintain a 30 frames per second rate
        clock.tick(FPS)

    # Done! Print the final score
    print(f"Game over! Final score: {score}")

    # Make the mouse visible again
    pygame.mouse.set_visible(True)

    # Quit the game
    pygame.quit()