from pymunk import Arbiter
from asteroids.bullet import Bullet
from asteroids.asteroid import Asteroid
from asteroids.engine import GameEngine
from asteroids.explosion import Explosion

def bullet_hits_asteroid(engine: GameEngine, bullet: Bullet, asteroid: Asteroid, arbiter: Arbiter):
    engine.remove(bullet)

    asteroid.hit(engine, bullet, 0.5 * asteroid.mass * bullet.body.velocity.get_length_sqrd())

def asteroid_hits_asteroid(engine: GameEngine, a1: Asteroid, a2: Asteroid, arbiter: Arbiter):
    a1.hit(engine, a2, arbiter.total_ke)
    a2.hit(engine, a1, arbiter.total_ke)

