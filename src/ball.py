from rigid_body_3d import RigidBody3D
import numpy as np
from OpenGL.GL import glPushMatrix, glPopMatrix
from OpenGL.GL import (
    glBegin,
    glEnd,
    glVertex3f,
    glColor3f,
    GL_LINES,
    glTranslatef,
    glRotatef,
    glLineWidth,
)


class Ball(RigidBody3D):
    def __init__(self, position=None, velocity=None, mass=1.0, radius=0.4, force=20, **kwargs):
        super().__init__(position=position, velocity=velocity, mass=mass, **kwargs)
        self.radius = radius
        self.rotation_axis = [0.0, 0.0, 0.0]
        self.rotation_angle = 0.0
        self.force = force
        self.yaw = 0.0

    def update(self, dt, keymap, gravity, ground_height=0.4):
        super().update(dt, gravity=gravity, ground_height=ground_height)

        if keymap.get("left", False):
            self.yaw += 120 * dt
        if keymap.get("right", False):
            self.yaw -= 120 * dt
        self.yaw = round(self.yaw)

        forward = np.array(
            [np.sin(np.radians(self.yaw)), 0, np.cos(np.radians(self.yaw))]
        )
        right = np.array(
            [np.cos(np.radians(self.yaw)), 0, -np.sin(np.radians(self.yaw))]
        )
        move_dir = np.array([0.0, 0.0, 0.0])

        if keymap.get("w", False):
            move_dir += forward
        if keymap.get("s", False):
            move_dir -= forward
        if keymap.get("d", False):
            move_dir -= right
        if keymap.get("a", False):
            move_dir += right

        if keymap.get("space", False):
            if self.on_ground:
                self.velocity = forward * self.force

        # Tambahan: loncat ke atas dengan tombol X
        if keymap.get("x", False):
            if self.on_ground:
                self.velocity[1] = self.force  # Lompatan vertikal

        if keymap.get("z", False):
            self.velocity = np.array([0, 0, 0], dtype=np.float32)

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

    def draw_arrow(self):
        glPushMatrix()
        glTranslatef(
            self.position[0],
            self.position[1],
            self.position[2],
        )
        glRotatef(self.yaw, 0, 1, 0)

        glColor3f(0.0, 0.5, 2.0)
        glLineWidth(3)
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 2)
        glEnd()
        glBegin(GL_LINES)
        glVertex3f(0, 0, 2)
        glVertex3f(0.3, 0, 1.0)
        glVertex3f(0, 0, 2)
        glVertex3f(-0.3, 0, 1.0)
        glEnd()

        glPopMatrix()
