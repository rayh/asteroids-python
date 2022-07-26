from math import pi
from typing import Tuple
from pathlib import Path
import pygame
from pymunk import ShapeFilter, Vec2d

from .engine import GameEngine
from .particle import Particle
from asteroids.polygon import Polygon, move_poly, scale_poly, rotate_poly 
from .constants import COLLISION_TYPE_ASTEROID, COLLISION_TYPE_BULLET, COLLISION_TYPE_MISSILE, COLLISION_TYPE_PLAYER, WHITE
from .maths import diff_angle, vec_polar
from .explosion import Explosion

# Define the Player sprite
class Missile(Particle):
    MAX_SPEED = 300
    BULLET_POLYGON = Polygon([(-0.3, -1), (-0.2, -0.7), (-0.2, 0.7), (0, 1), (0.2, 0.7), (0.2, -0.7), (0.3, -1)]).rotate(-1/2*pi).scale(15)
    THRUST_POLYGON = Polygon([(-0.2, -1), (0.2, -1), (0, -1.4)]).rotate(-1/2*pi).scale(15)

    def __init__(self, position=(0,0), angle=0, velocity=(0,0)):
        """Initialize the player sprite"""
        super(Missile, self).__init__(
            mass=1000,
            vertices=self.BULLET_POLYGON.points, 
            position=position)

        # self.angle = -pi/2
        self.body.angle = angle
        self.body.velocity = velocity
        self.body.elasticity = 0
        self.shape.collision_type = COLLISION_TYPE_MISSILE
        self.shape.filter = ShapeFilter(categories=COLLISION_TYPE_MISSILE)
        self.shape.particle = self
        self.colour = (200,100,0)

        self.target = None
        self.thrust_vector = None
        self.target_vector = None
        self.corrective_thrust_vector = None
        self.thrust_factor = 0

        # create transparent background image
        self.surf = pygame.Surface( (40,40), pygame.SRCALPHA, 32 )  
        self.rect = self.surf.get_rect()

    def draw_debug(self, surface):
        super().draw_debug(surface)

        if self.thrust_vector:
            self.draw_debug_vector(surface, self.thrust_vector, (255,255,0), 1, text="THRUST")

        if self.target_vector:
            self.draw_debug_vector(surface, self.target_vector, (255,255,0,128), 1, text="TARGET")

        if self.corrective_thrust_vector:
            self.draw_debug_vector(surface, self.corrective_thrust_vector, (128,255,0,128), 1, text="CORRECTIVE")

        if self.target:
            target_colour = (255,255,0,128)
            Polygon.circle(50, 10).translate(self.body.position + self.target_vector).draw(surface, target_colour, width=1)
            Polygon.line(self.target.body.position, self.body.position + self.target_vector).draw(surface, target_colour, width=1)
            Polygon.circle(10, 10).translate(self.target.body.position).draw(surface, target_colour, width=0)

    def on_draw(self, surf: pygame.Surface):
        super().on_draw(surf)

        alpha = 255 * self.thrust_factor
        self.THRUST_POLYGON.rotate(self.body.angle).center_in_surface(surf).draw(surf, colour=(255,255,255,alpha), width=0)


    def on_update(self, engine: GameEngine, time: float):
        max_thrust_for_time = self.mass * 100 * time

        # Require target
        if not self.target or self.target.dead == True:
            self.target = None
            particles = engine.particles_near(self.body.position, max_distance=500, mask=COLLISION_TYPE_ASTEROID)
            if len(particles) > 0:
                sorted_by_mass = sorted(particles, key=lambda p: p.mass)
                self.target = sorted_by_mass[-1]

        if self.target:
            self.target_vector = self.target.body.position - self.body.position

            target_vector_velocity_m = self.body.velocity.dot(self.target_vector)/abs(self.target_vector)

            # print("target_vector_velocity_m", target_vector_velocity_m)

            # No point calculating this for tiny velocities
            # if target_vector_velocity_m > 0:
            #     ### We need to track for where the asteroid WILL be by the time we get there
            #     # 1. at our current speed, how long would we take to get there?
            #     # NB this is approx, and doesnt take into account the direction!
            #     seconds_until_impact = self.target_vector.length / target_vector_velocity_m

            #     # 2. Where will the asteroid be in this many seconds
            #     target_future_position = self.target.body.position + (self.target.body.velocity * seconds_until_impact)

            #     # 3. Set this as the target vector
            #     self.target_vector = target_future_position - self.body.position


            ### Now we know where to go, we need to work out how to get there

            # 1. How far apart is target vector from current velocity
            target_angle_offset = diff_angle(self.target_vector.angle, self.body.velocity.angle)
            gimble_angle = 0

            # 2. Adjust desired gimble angle based on how far off the desired angle we are
            if abs(target_angle_offset) > pi/2:
            
                # We're quite far off, so cancel our current velocity 
                self.corrective_thrust_vector = self.target_vector - self.body.velocity

                # But to do this, we need to rotate to this ideal vector
                gimble_angle = diff_angle(self.corrective_thrust_vector.angle, self.body.angle)
            else:
                # Reflect through normal 
                # normal = self.target_vector.perpendicular_normal()
                # self.corrective_thrust_vector = self.corrective_thrust_vector - 2(self.corrective_thrust_vector.dot(normal)) * normal
                self.corrective_thrust_vector = None

                # Just rotate to the target vector
                gimble_angle = diff_angle(self.target_vector.angle, self.body.angle)

            # 3. Adjust angular velocity to be proportional to the size of the desired angle from current angle
            how_far_off_factor = (gimble_angle/pi)
            self.body.angular_velocity = how_far_off_factor * 10
            thrust_m = max_thrust_for_time/2 + (max_thrust_for_time/2 * (abs(how_far_off_factor)))

            # print('gimble angle', gimble_angle, 'body angle', self.body.angle, 'torque', self.body.torque, 'f', how_far_off_factor)
            self.thrust_vector = vec_polar(self.body.angle, max_thrust_for_time)

        elif self.body.velocity.length < self.MAX_SPEED:
            self.corrective_thrust_vector = None
            self.target_vector = None
            self.thrust_vector = vec_polar(self.body.angle, max_thrust_for_time/10)
        else:
            self.corrective_thrust_vector = None
            self.target_vector = None
            self.thrust_vector = None

 
        super().on_update(engine, time)

        if self.thrust_vector:
            self.body.apply_impulse_at_world_point(self.thrust_vector, self.body.position)
            self.thrust_factor = (self.thrust_vector.length / max_thrust_for_time)
        else:
            self.thrust_factor = 0

        # if self.age > 20:
        #     engine.add(Explosion(self.body.position, force=1e5))
        #     self.dead = True

