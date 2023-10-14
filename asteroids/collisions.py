from math import pi
from pymunk import Arbiter
from asteroids.bullet import Bullet
from asteroids.asteroid import Asteroid
from .engine.particle import Particle
from .engine.scene import Scene
from asteroids.explosion import Explosion
from asteroids.maths import diff_angle, vec_polar
from asteroids.missile import Missile
from asteroids.player import Player

def bullet_hits_asteroid(scene: Scene, bullet: Bullet, asteroid: Asteroid, arbiter: Arbiter):
    scene.add(Explosion(bullet.body.position, distance=0, force=bullet.mass))
    bullet.dead = True
    asteroid.on_collision(scene, bullet, 0.5 * asteroid.mass * bullet.body.velocity.get_length_sqrd())

def asteroid_hits_asteroid(scene: Scene, a1: Asteroid, a2: Asteroid, arbiter: Arbiter):
    a1.on_collision(scene, a2, arbiter.total_ke)
    a2.on_collision(scene, a1, arbiter.total_ke)

def missile_hits_asteroid(scene: Scene, missile: Missile, asteroid: Asteroid, arbiter: Arbiter):
    direct_path = -(missile.body.position - asteroid.body.position)
    diff = diff_angle(missile.body.angle, direct_path.angle)
    # print("diff between missle and true direct", diff)

    if abs(diff) < 0.3:
        asteroid.on_collision(scene, missile, 1e7 * asteroid.mass)
        scene.add(Explosion(missile.body.position, distance=150, force=1e13))
        missile.dead = True

def thing_hits_player(scene: Scene, thing: Particle, player: Player, arbiter: Arbiter):
    # thing.hit(engine, player, arbiter)
    player.on_collision(scene, thing, 0.5 * player.mass * thing.body.velocity.get_length_sqrd())
