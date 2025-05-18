import numpy as np
from OpenGL.GLU import gluLookAt


class Camera:
    def __init__(self, offset=(0, 2, 6)):
        self.offset = np.array(offset, dtype=float)
        self.yaw = 0.0
        self.position = np.array([0.0, 0.5, 0.0], dtype=float)

    def update(self, keymap, position, yaw):
        if keymap.get("up", False):
            self.offset[1] += 0.1
        if keymap.get("down", False):
            self.offset[1] -= 0.1

        self.position = np.array(position, dtype=float)
        self.yaw = yaw
        cos_yaw = np.cos(np.radians(self.yaw))
        sin_yaw = np.sin(np.radians(self.yaw))
        cam_x = self.position[0] - self.offset[2] * sin_yaw
        cam_y = self.position[1] + self.offset[1]
        cam_z = self.position[2] - self.offset[2] * cos_yaw

        gluLookAt(
            cam_x,
            cam_y,
            cam_z,
            self.position[0],
            self.position[1],
            self.position[2],
            0,
            1,
            0,
        )
