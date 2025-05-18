from object_3d import Object3D
import numpy as np


class Player(Object3D):
    def __init__(
        self,
        position=None,
        velocity=None,
        mass=1.0,
        speed=3.0,
        jump_force=5.0,
        max_speed=3.0,
        run_multiplier=3.0,
    ):
        super().__init__(
            position=position,
            velocity=velocity,
            mass=mass,
        )

        self.speed = speed
        self.jump_force = jump_force
        self.max_speed = max_speed
        self.run_multiplier = run_multiplier
        self.on_ground = False
        self.yaw = 0.0

    def walk(self, keys, dt):
        if keys.get("left", False):
            self.yaw += 90 * dt
        if keys.get("right", False):
            self.yaw -= 90 * dt

        self.yaw = round(self.yaw)
        forward = np.array(
            [np.sin(np.radians(self.yaw)), 0, np.cos(np.radians(self.yaw))]
        )
        right = np.array(
            [np.cos(np.radians(self.yaw)), 0, -np.sin(np.radians(self.yaw))]
        )
        move_dir = np.array([0.0, 0.0, 0.0])
        if keys.get("w", False):
            move_dir += forward
        if keys.get("s", False):
            move_dir -= forward
        if keys.get("d", False):
            move_dir -= right
        if keys.get("a", False):
            move_dir += right

        if np.linalg.norm(move_dir) > 0:
            move_dir = move_dir / np.linalg.norm(move_dir)
            move_dir[np.abs(move_dir) < 0.01] = 0

        target_speed = self.speed
        if keys.get("shift", False):
            target_speed *= self.run_multiplier

        accel = 5

        for i in [0, 2]:
            desired = move_dir[i] * target_speed
            delta = desired - self.velocity[i]
            max_delta = accel * dt
            if abs(delta) > max_delta:
                delta = np.sign(delta) * max_delta
            self.velocity[i] += delta

        if np.linalg.norm(move_dir) == 0:
            friction = 0.85
            self.velocity[0] *= friction
            self.velocity[2] *= friction
            if abs(self.velocity[0]) < 0.01:
                self.velocity[0] = 0
            if abs(self.velocity[2]) < 0.01:
                self.velocity[2] = 0

    def jump(self):
        if self.on_ground:
            self.velocity[1] = self.jump_force
            self.on_ground = False

    def update(self, dt, keymap, gravity=9.8):
        super().update(dt, gravity=gravity)
        self.walk(keymap, dt)
