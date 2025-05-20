from object_3d import Object3D
import numpy as np
from OpenGL.GL import glBegin, glEnd, glVertex3f, glColor3f, GL_LINES


class RigidBody3D(Object3D):
    instances = []

    def __init__(
        self,
        position=None,
        velocity=None,
        mass=1.0,
        friction=0.2,
        bounding_box_size=None,
    ):
        RigidBody3D.instances.append(self)

        super().__init__(position, bounding_box_size)
        self.velocity = np.array(
            velocity if velocity is not None else [0.0, 0.0, 0.0], dtype=float
        )
        self.mass = mass
        self.forces = np.zeros(3, dtype=float)
        self.friction = friction
        self.on_ground = False

    def add_force(self, force):
        self.forces += np.array(force, dtype=float)

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

        self.check_ground()
        # self.check_wall()

    def check_wall(self):
        if self.position[0] <= -19.5 or self.position[0] >= 19.5:
            self.position[0] = min(max(self.position[0], -19.5), 19.5)
            self.velocity[0] = 0

        if self.position[2] <= -19.5 or self.position[2] >= 19.5:
            self.position[2] = min(max(self.position[2], -19.5), 19.5)
            self.velocity[2] = 0

    def check_ground(self):
        if self.position[1] <= 0.4:
            self.position[1] = 0.4
            if self.velocity[1] < 0:
                self.velocity[1] = -self.velocity[1] * self.friction
                if abs(self.velocity[1]) < 0.1:
                    self.velocity[1] = 0
                    self.on_ground = True
                else:
                    self.on_ground = False
            else:
                self.on_ground = True

    def apply_friction(self):
        if self.on_ground:
            friction_force = -self.friction * self.velocity
            friction_force[1] = 0
            self.forces += friction_force

    def apply_gravity(self, gravity):
        self.add_force([0, -gravity * self.mass, 0])

    @staticmethod
    def check_all_collisions():
        for i, obj_a in enumerate(RigidBody3D.instances):
            for obj_b in RigidBody3D.instances[i + 1 :]:
                obj_a.check_object_collision(obj_b)
            obj_a.draw_bounding_box()

    def get_aabb(self):
        # Returns world-space min and max of the bounding box
        min_bb = self.position + self.bounding_box_size[0]
        max_bb = self.position + self.bounding_box_size[1]
        return min_bb, max_bb

    def check_wall_collision(self, min_bound, max_bound):
        # Clamp the AABB to the world bounds and zero velocity if colliding
        min_bb, max_bb = self.get_aabb()
        for i in [0, 1, 2]:
            if min_bb[i] < min_bound[i]:
                self.position[i] += min_bound[i] - min_bb[i]
                self.velocity[i] = 0
            if max_bb[i] > max_bound[i]:
                self.position[i] -= max_bb[i] - max_bound[i]
                self.velocity[i] = 0

    def check_object_collision(self, other):
        # AABB vs AABB collision
        min_a, max_a = self.get_aabb()
        min_b, max_b = other.get_aabb()
        overlap = True
        for i in range(3):
            if max_a[i] < min_b[i] or min_a[i] > max_b[i]:
                overlap = False
        if overlap:
            # Simple collision response: separate along the axis of greatest overlap
            diffs = [
                min(max_a[i], max_b[i]) - max(min_a[i], min_b[i]) for i in range(3)
            ]
            axis = np.argmin(diffs)
            if self.position[axis] < other.position[axis]:
                self.position[axis] -= diffs[axis] / 2
                other.position[axis] += diffs[axis] / 2
            else:
                self.position[axis] += diffs[axis] / 2
                other.position[axis] -= diffs[axis] / 2
            # Swap velocities (simple elastic response)
            self.velocity, other.velocity = other.velocity.copy(), self.velocity.copy()

    def draw_bounding_box(self):
        min_bb, max_bb = self.get_aabb()
        # 8 corners of the box
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

        glColor3f(1, 0, 0)  # Red color for bounding box
        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glVertex3f(*corners[vertex])
        glEnd()
