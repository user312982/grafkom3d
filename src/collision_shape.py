from object_3d import Object3D
from rigid_body_3d import RigidBody3D
import numpy as np


class CollisionShape(Object3D):
    instances = []

    def __init__(self, position=None, bounding_box_size=None):
        self.instances.append(self)
        super().__init__(position, bounding_box_size)

    @staticmethod
    def check_all_collisions_with_rigidbody():
        for shape in CollisionShape.instances:
            for rigidbody in RigidBody3D.instances:
                shape.check_collision_with_rigidbody(rigidbody)
            shape.draw_bounding_box()

    def get_aabb(self):
        min_bb = self.position + self.bounding_box_size[0]
        max_bb = self.position + self.bounding_box_size[1]
        return min_bb, max_bb

    def check_collision_with_rigidbody(self, rigidbody):
        min_a, max_a = self.get_aabb()
        min_b, max_b = rigidbody.get_aabb()
        overlap = True
        for i in range(3):
            if max_a[i] < min_b[i] or min_a[i] > max_b[i]:
                overlap = False
        if overlap:
            diffs = [
                min(max_a[i], max_b[i]) - max(min_a[i], min_b[i]) for i in range(3)
            ]
            axis = np.argmin(diffs)
            if rigidbody.position[axis] < self.position[axis]:
                rigidbody.position[axis] = (
                    min_a[axis] - rigidbody.bounding_box_size[1]
                )
            else:
                rigidbody.position[axis] = (
                    max_a[axis] - rigidbody.bounding_box_size[0]
                )

            rigidbody.velocity[axis] = -rigidbody.velocity[axis] * getattr(rigidbody, "bounciness", 0.0)

    def draw_bounding_box(self):
        try:
            from OpenGL.GL import glBegin, glEnd, glVertex3f, glColor3f, GL_LINES
        except ImportError:
            return
        min_bb, max_bb = self.get_aabb()
        corners = [
            [min_bb[0], min_bb[1], min_bb[2]],
            [max_bb[0], min_bb[1], min_bb[2]],
            [max_bb[0], max_bb[1], min_bb[2]],
            [min_bb[0], max_bb[1], min_bb[2]],
            [min_bb[0], min_bb[1], max_bb[2]],
            [max_bb[0], min_bb[1], max_bb[2]],
            [max_bb[0], max_bb[1], max_bb[2]],
            [min_bb[0], max_bb[1], max_bb[2]],
        ]
        edges = [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),
            (4, 5),
            (5, 6),
            (6, 7),
            (7, 4),
            (0, 4),
            (1, 5),
            (2, 6),
            (3, 7),
        ]
        glColor3f(0, 1, 0)  # Green color for static collision shape
        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glVertex3f(*corners[vertex])
        glEnd()
