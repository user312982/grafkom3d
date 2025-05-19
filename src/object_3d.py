import numpy as np


class Object3D:
    def __init__(
        self,
        position=None,
        velocity=None,
        mass=1.0,
        friction=0.2,
    ):
        self.position = np.array(
            position if position is not None else [0.0, 0.0, 0.0], dtype=float
        )
        self.velocity = np.array(
            velocity if velocity is not None else [0.0, 0.0, 0.0], dtype=float
        )
        self.mass = mass
        self.forces = np.zeros(3, dtype=float)
        self.friction = friction
        self.on_ground = False

    def add_force(self, force):
        self.forces += np.array(force, dtype=float)

    def set_position(self, position):
        self.position = np.array(position, dtype=float)

    def set_velocity(self, velocity):
        self.velocity = np.array(velocity, dtype=float)

    def update(self, dt, gravity=9.8, ground_height=0.25, bounce=0.5):
        self.add_force([0, -gravity * self.mass, 0])
        self.apply_friction()

        acceleration = self.forces / self.mass
        initial_velocity = self.velocity
        self.velocity += acceleration * dt
        self.position += initial_velocity * dt + 0.5 * acceleration * dt * dt
        self.forces[:] = 0

        self.apply_bounce(bounce)
        self.check_ground()

    def check_ground(self):
        if self.position[0] <= -19.5 or self.position[0] >= 19.5:
            self.position[0] = min(max(self.position[0], -19.5), 19.5)
            self.velocity[0] = 0

        if self.position[2] <= -19.5 or self.position[2] >= 19.5:
            self.position[2] = min(max(self.position[2], -19.5), 19.5)
            self.velocity[2] = 0

    def apply_friction(self):
        if self.on_ground:
            friction_force = -self.friction * self.velocity
            friction_force[1] = 0
            self.forces += friction_force

    def apply_gravity(self, gravity):
        self.add_force([0, -gravity * self.mass, 0])

    def apply_bounce(self, bounce):
        if self.position[1] <= bounce:
            self.position[1] = bounce
            if self.velocity[1] < 0:
                self.velocity[1] = -self.velocity[1] * bounce / (1 + self.mass)
                if abs(self.velocity[1]) < 0.1:
                    self.velocity[1] = 0
                    self.on_ground = True
                else:
                    self.on_ground = False
            else:
                self.on_ground = True
