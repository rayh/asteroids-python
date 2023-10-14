import pygame
from pymunk import Arbiter

from asteroids.collisions import *

from ..engine.particle import Particle
from ..engine.scene import Scene
from ..asteroid import Asteroid
from ..player import Player
from asteroids.behaviours.gravity import GravityBehaviour


def draw_title(surf, text, alpha=1):
    title_font = pygame.font.SysFont("arialblack", 150)
    title_block = title_font.render(text, True, (255, 255, 255, 255))
    title_block.set_alpha(int(255 * alpha))
    title_size = title_block.get_size()
    screen_size = surf.get_size()
    surf.blit(
        title_block,
        (
            screen_size[0] / 2 - title_size[0] / 2,
            screen_size[1] / 2 - title_size[1] / 2,
        ),
    )


def draw_subtitle(surf, text, alpha=1):
    title_font = pygame.font.SysFont("arialblack", 40)
    title_block = title_font.render(text, True, (255, 255, 255, 255))
    title_block.set_alpha(int(255 * alpha))
    title_size = title_block.get_size()
    screen_size = surf.get_size()
    surf.blit(
        title_block,
        (
            screen_size[0] / 2 - title_size[0] / 2,
            screen_size[1] / 2 - title_size[1] / 2 + 100,
        ),
    )


class LevelScene(Scene):
    def __init__(self) -> None:
        super().__init__()

        self.player = None

    def setup(self, engine):
        super().setup(engine)
        screen_size = pygame.display.get_window_size()
        # screen_size = engine.screen.get_size()

        self.player = Player(pos=(screen_size[0] / 2, screen_size[1] / 2))
        self.add(self.player)

        self.behaviours.append(GravityBehaviour())

        # asteroids = pygame.sprite.Group()
        for i in range(0, 5):
            asteroid = Asteroid.randomized(screen_size)
            # asteroids.add(asteroid)
            self.add(asteroid)

    def tick(self, engine, time: float):
        super().tick(engine, time)

        # keys_pressed = pygame.key.get_pressed()
        # if self.player.health <= 0 and keys_pressed[pygame.K_RETURN]:
        #     pygame.event.post()

    def tick_particle(self, p: Particle, time: float):
        super().tick_particle(p, time)
        self.wrap_screen_coords(p)

    def render(self, surf, debug_surf, debug=False):
        super().render(surf, debug_surf, debug)

        screen_size = pygame.display.get_window_size()

        if self.elapsed_time < 3:
            # Finally, draw the score at the bottom left
            alpha = 1 - (self.elapsed_time / 3)
            draw_title(surf, f"Asteroids!", alpha)
            draw_subtitle(surf, "Level 1", alpha)

        if self.player.health <= 0:
            draw_title(surf, "Game Over!", 1)
            draw_subtitle(surf, "Press RETURN to restart", 1)

        # Finally, draw the score at the bottom left
        font = pygame.font.SysFont("arialblack", 36)

        score_block = font.render(
            f"Objects: {len(self.particles)}", True, (255, 255, 255)
        )
        surf.blit(score_block, (50, screen_size[1] - 50))

        health_block = font.render(
            f"Health: {int(self.player.health * 100)}", True, (255, 255, 255)
        )
        surf.blit(health_block, (screen_size[0] - health_block.get_size()[0] - 50, 50))

    def wrap_screen_coords(self, p: Particle):
        size = pygame.display.get_window_size()

        if p.body.position[1] > size[1]:
            p.body.position = (p.body.position[0], p.body.position[1] - size[1])

        if p.body.position[1] < 0:
            p.body.position = (p.body.position[0], size[1] - p.body.position[1])

        if p.body.position[0] > size[0]:
            p.body.position = (p.body.position[0] - size[0], p.body.position[1])

        if p.body.position[0] < 0:
            p.body.position = (size[0] - p.body.position[0], p.body.position[1])

    def on_collision_pair(self, p1: Particle, p2: Particle, arbiter: Arbiter):
        # Avoid repetative processing
        if p1.dead or p2.dead:
            return

        # print('collision', p1, p2)
        # impulse_v = arbiter.total_impulse * -1 * 1e12
        # p.body.apply_impulse_at_world_point(
        #     impulse_v,
        #     p.body.position)
        # print('Apply', self, impulse_v, 'to', p)

        if type(p1) == Asteroid and type(p2) == Bullet:
            bullet_hits_asteroid(self, p2, p1, arbiter)
            return

        if type(p2) == Asteroid and type(p1) == Bullet:
            bullet_hits_asteroid(self, p1, p2, arbiter)
            return

        if type(p1) == Asteroid and type(p2) == Asteroid:
            asteroid_hits_asteroid(self, p1, p2, arbiter)
            return

        if type(p1) == Asteroid and type(p2) == Missile:
            missile_hits_asteroid(self, p2, p1, arbiter)
            return

        if type(p2) == Asteroid and type(p1) == Missile:
            missile_hits_asteroid(self, p1, p2, arbiter)
            return

        if isinstance(p1, Player):
            thing_hits_player(self, p2, p1, arbiter)
            return

        if isinstance(p2, Player):
            thing_hits_player(self, p1, p2, arbiter)
