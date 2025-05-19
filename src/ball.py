from object_3d import Object3D
import numpy as np


class Ball(Object3D):
    def __init__(self, position=None, velocity=None, mass=1.0, radius=0.4, **kwargs):
        super().__init__(position=position, velocity=velocity, mass=mass, **kwargs)
        self.radius = radius
        self.rotation_axis = [0.0, 0.0, 0.0]
        self.rotation_angle = 0.0
        self.force = 20
        self.yaw = 0.0

    def update(self, dt, keymap, gravity, ground_height=0.4):
        super().update(dt, gravity=gravity, ground_height=ground_height)
        if keymap.get("left", False):
            self.yaw += 90 * dt
        if keymap.get("right", False):
            self.yaw -= 90 * dt
        self.yaw = round(self.yaw)
        forward = np.array(
            [np.sin(np.radians(self.yaw)), 0, np.cos(np.radians(self.yaw))]
        )
        right = np.array(
            [np.cos(np.radians(self.yaw)), 0, -np.sin(np.radians(self.yaw))]
        )
        move_dir = np.array([0.0, 0.0, 0.0])
        print("dir", move_dir)
        print("forward", forward)
        print("right", right)

        if keymap.get("w", False):
            move_dir += forward
            self.add_force(forward * self.force)
        if keymap.get("s", False):
            move_dir -= forward
            self.add_force(-forward * self.force)
        if keymap.get("d", False):
            move_dir -= right
            self.add_force(-right * self.force)
        if keymap.get("a", False):
            move_dir += right
            self.add_force(right * self.force)

        if keymap.get("space", False):
            if self.on_ground:
                self.velocity[1] = 5
                self.on_ground = False

        # Roll
        v = self.velocity.copy()
        v[1] = 0
        speed = np.linalg.norm(v)
        if speed > 1e-6:
            axis = np.cross([0, 1, 0], v)
            axis_norm = np.linalg.norm(axis)
            if axis_norm > 1e-6:
                self.rotation_axis = axis / axis_norm
                angle_delta = (speed * dt) / self.radius
                self.rotation_angle += np.degrees(angle_delta)
