from math import pi
from pymunk import Arbiter
from asteroids.bullet import Bullet
from asteroids.asteroid import Asteroid
from asteroids.engine import GameEngine
from asteroids.explosion import Explosion
from asteroids.maths import diff_angle, vec_polar
from asteroids.missile import Missile

def bullet_hits_asteroid(engine: GameEngine, bullet: Bullet, asteroid: Asteroid, arbiter: Arbiter):
    engine.add(Explosion(bullet.body.position, distance=0, force=bullet.mass))
    bullet.dead = True
    asteroid.hit(engine, bullet, 0.5 * asteroid.mass * bullet.body.velocity.get_length_sqrd())

def asteroid_hits_asteroid(engine: GameEngine, a1: Asteroid, a2: Asteroid, arbiter: Arbiter):
    a1.hit(engine, a2, arbiter.total_ke)
    a2.hit(engine, a1, arbiter.total_ke)

def missile_hits_asteroid(engine: GameEngine, missile: Missile, asteroid: Asteroid, arbiter: Arbiter):
    direct_path = -(missile.body.position - asteroid.body.position)
    diff = diff_angle(missile.body.angle, direct_path.angle)
    # print("diff between missle and true direct", diff)

    if abs(diff) < 0.3:
        asteroid.hit(engine, missile, 1e7 * asteroid.mass)
        engine.add(Explosion(missile.body.position, distance=150, force=1e13))
        missile.dead = True

