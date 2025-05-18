import numpy as np


class Object3D:
    def __init__(
        self,
        position=None,
        velocity=None,
        mass=1.0,
    ):
        self.position = np.array(
            position if position is not None else [0.0, 0.0, 0.0], dtype=float
        )
        self.velocity = np.array(
            velocity if velocity is not None else [0.0, 0.0, 0.0], dtype=float
        )
        self.mass = mass
        self.forces = np.zeros(3, dtype=float)

    def add_force(self, force):
        self.forces += np.array(force, dtype=float)

    def set_position(self, position):
        self.position = np.array(position, dtype=float)

    def set_velocity(self, velocity):
        self.velocity = np.array(velocity, dtype=float)

    def update(self, dt, gravity=9.8, ground_height=0.25, bounce=0.5):
        self.add_force([0, -gravity * self.mass, 0])
        acceleration = self.forces / self.mass
        initial_velocity = self.velocity
        self.velocity += acceleration * dt
        self.position += initial_velocity * dt + 0.5 * acceleration * dt * dt
        self.forces[:] = 0

        if self.position[1] <= ground_height:
            self.position[1] = ground_height
            if self.velocity[1] < 0:
                self.velocity[1] = -self.velocity[1] * bounce
                if abs(self.velocity[1]) < 0.1:
                    self.velocity[1] = 0
                    self.on_ground = True
                else:
                    self.on_ground = False
            else:
                self.on_ground = True
