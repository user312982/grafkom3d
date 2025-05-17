import numpy as np

class Object3D:
    def __init__(self, position=None, velocity=None, mass=1.0, speed=3.0, jump_speed=5.0, max_speed=3.0, run_multiplier=3.0):
        self.position = np.array(position if position is not None else [0.0, 0.0, 0.0], dtype=float)
        self.velocity = np.array(velocity if velocity is not None else [0.0, 0.0, 0.0], dtype=float)
        self.mass = mass
        self.forces = np.zeros(3, dtype=float)
        self.speed = speed
        self.jump_speed = jump_speed
        self.max_speed = max_speed
        self.run_multiplier = run_multiplier
        self.on_ground = False
        self.yaw = 0.0

    def add_force(self, force):
        self.forces += np.array(force, dtype=float)

    def set_position(self, position):
        self.position = np.array(position, dtype=float)

    def set_velocity(self, velocity):
        self.velocity = np.array(velocity, dtype=float)

    def walk(self, keys, dt):
        if keys.get('left', False):
            self.yaw += 90 * dt
        if keys.get('right', False):
            self.yaw -= 90 * dt

        forward = np.array([np.sin(np.radians(self.yaw)), 0, np.cos(np.radians(self.yaw))])
        right = np.array([np.cos(np.radians(self.yaw)), 0, -np.sin(np.radians(self.yaw))])
        move_dir = np.array([0.0, 0.0, 0.0])
        if keys.get('w', False):
            move_dir += forward
        if keys.get('s', False):
            move_dir -= forward
        if keys.get('d', False):
            move_dir -= right
        if keys.get('a', False):
            move_dir += right
        if np.linalg.norm(move_dir) > 0:
            move_dir = move_dir / np.linalg.norm(move_dir)

        target_speed = self.max_speed
        if keys.get('shift', False):
            target_speed *= self.run_multiplier
        self.velocity[0] = move_dir[0] * self.speed
        self.velocity[2] = move_dir[2] * self.speed

    def jump(self):
        if self.on_ground:
            self.velocity[1] = self.jump_speed
            self.on_ground = False

    def update(self, dt, gravity=9.8, ground_height=0.5):
        self.add_force([0, -gravity * self.mass, 0])
        acceleration = self.forces / self.mass
        self.velocity += acceleration * dt
        self.position += self.velocity * dt
        self.forces[:] = 0

        if self.position[1] <= ground_height:
            self.position[1] = ground_height
            self.velocity[1] = 0
            self.on_ground = True
