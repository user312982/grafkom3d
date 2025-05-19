from object_3d import Object3D
import numpy as np


class Ball(Object3D):
    def __init__(self, position=None, velocity=None, mass=1.0, radius=0.4, **kwargs):
        super().__init__(position=position, velocity=velocity, mass=mass, **kwargs)
        self.radius = radius
        self.rotation_axis = [0.0, 0.0, 0.0]
        self.rotation_angle = 0.0

    def update(self, dt, keymap, gravity, ground_height=0.4):
        super().update(dt, gravity=gravity, ground_height=ground_height)
        if keymap.get("z", False):
            self.add_force([-5, 0, 0])
        if keymap.get("x", False):
            self.add_force([5, 0, 0])
 
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
