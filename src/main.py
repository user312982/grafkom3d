import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

from r2d2_model import *
from day_night_cycle import DayNightCycle
from hud import HUD
from camera import Camera
from ball import Ball
from rigid_body_3d import RigidBody3D
from collision_shape import CollisionShape


class MainScene:
    def __init__(self):
        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
        self.display = (1000, 600)
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        glEnable(GL_MULTISAMPLE)
        self.init_gl()

        self.hud = HUD(self.display)
        self.day_night = DayNightCycle()

        self.ball = Ball(
            position=[5, 5, 0.0],
            radius=0.4,
            mass=0.5,
            bounding_box_size=(-0.35, 0.35, 0.35),
        )

        self.ball1 = Ball(
            position=[5, 10, 0.0],
            radius=0.4,
            mass=0.5,
            bounding_box_size=(-0.35, 0.35, 0.35),
        )

        collision_thickness = 2.0

        self.wall1 = CollisionShape(
            position=[21, 0, 0],
            bounding_box_size=[
                (-collision_thickness / 2, 0, -20),
                (collision_thickness / 2, 20, 20),
            ],
        )

        self.wall2 = CollisionShape(
            position=[-21, 0, 0],
            bounding_box_size=[
                (-collision_thickness / 2, 0, -20),
                (collision_thickness / 2, 20, 20),
            ],
        )

        self.wall3 = CollisionShape(
            position=[0, 0, -21],
            bounding_box_size=[
                (-20, 0, -collision_thickness / 2),
                (20, 20, collision_thickness / 2),
            ],
        )

        self.wall4 = CollisionShape(
            position=[0, 0, 21],
            bounding_box_size=[
                (-20, 0, -collision_thickness / 2),
                (20, 20, collision_thickness / 2),
            ],
        )

        self.gravity_earth = 9.8
        self.gravity_moon = 1.62
        self.gravity = self.gravity_earth

        self.camera = Camera(offset=(0, 2, 6))
        self.clock = pygame.time.Clock()

        self.running = True
        while self.running:
            dt = self.clock.tick(60) / 1000  # detik/frame
            self.handle_events()

            self.day_night.update(dt)
            self.day_night.setup_lighting()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()

            keys = pygame.key.get_pressed()

            keymap = {
                "w": keys[pygame.K_w],
                "a": keys[pygame.K_a],
                "s": keys[pygame.K_s],
                "d": keys[pygame.K_d],
                "left": keys[pygame.K_LEFT],
                "right": keys[pygame.K_RIGHT],
                "shift": keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT],
                "space": keys[pygame.K_SPACE],
                "up": keys[pygame.K_UP],
                "down": keys[pygame.K_DOWN],
                "z": keys[pygame.K_z],
                "x": keys[pygame.K_x],
            }

            self.camera.update(keymap, self.ball.position, self.ball.yaw)
            RigidBody3D.check_all_collisions()
            CollisionShape.check_all_collisions_with_rigidbody()
            self.draw_ground()
            self.draw_walls()
            self.day_night.draw_sky_objects()

            # draw ball
            glPushMatrix()
            glTranslatef(*self.ball.position)
            glRotatef(self.ball.rotation_angle, *self.ball.rotation_axis)
            glColor3f(1.0, 1.0, 0.0)
            quad = gluNewQuadric()
            gluSphere(quad, self.ball.radius, 32, 16)
            gluDeleteQuadric(quad)
            glColor3f(0.2, 0.2, 0.2)
            glLineWidth(2)
            for i in range(0, 360, 45):
                glBegin(GL_LINE_STRIP)
                for theta in np.linspace(0, np.pi, 32):
                    x = self.ball.radius * np.sin(theta) * np.cos(np.radians(i))
                    y = self.ball.radius * np.cos(theta)
                    z = self.ball.radius * np.sin(theta) * np.sin(np.radians(i))
                    glVertex3f(x, y, z)
                glEnd()

            self.ball.update(dt, keymap, gravity=self.gravity)
            glPopMatrix()

            # draw ball1
            glPushMatrix()
            glTranslatef(*self.ball1.position)
            glRotatef(self.ball1.rotation_angle, *self.ball1.rotation_axis)
            glColor3f(1.0, 1.0, 0.0)
            quad = gluNewQuadric()
            gluSphere(quad, self.ball1.radius, 32, 16)
            gluDeleteQuadric(quad)
            # Ball lines
            glColor3f(0.2, 0.2, 0.2)
            glLineWidth(2)
            for i in range(0, 360, 45):
                glBegin(GL_LINE_STRIP)
                for theta in np.linspace(0, np.pi, 32):
                    x = self.ball1.radius * np.sin(theta) * np.cos(np.radians(i))
                    y = self.ball1.radius * np.cos(theta)
                    z = self.ball1.radius * np.sin(theta) * np.sin(np.radians(i))
                    glVertex3f(x, y, z)
                glEnd()

            self.ball1.update(dt, {}, gravity=self.gravity)
            glPopMatrix()

            # self.draw_hud()
            pygame.display.flip()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    self.gravity = (
                        self.gravity_moon
                        if self.gravity == self.gravity_earth
                        else self.gravity_earth
                    )
                    print(
                        f"Gravitasi diganti ke {'Bulan' if self.gravity==self.gravity_moon else 'Bumi'} ({self.gravity:.2f} m/s²)"
                    )

    def init_gl(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.5, 0.7, 1.0, 1.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (self.display[0] / self.display[1]), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def draw_ground(self, size=20, tile_size=1):
        dark_gray = (0.3, 0.3, 0.3)
        light_gray = (0.7, 0.7, 0.7)
        glBegin(GL_QUADS)
        for x in range(-size, size):
            for z in range(-size, size):
                if (x + z) % 2 == 0:
                    glColor3f(*dark_gray)
                else:
                    glColor3f(*light_gray)
                glVertex3f(x * tile_size, 0, z * tile_size)
                glVertex3f(x * tile_size, 0, (z + 1) * tile_size)
                glVertex3f((x + 1) * tile_size, 0, (z + 1) * tile_size)
                glVertex3f((x + 1) * tile_size, 0, z * tile_size)
        glEnd()

    def draw_walls(self, size=20):
        glBegin(GL_QUADS)
        glColor3f(0.5, 0.5, 0.5)
        for x in range(-size, size):
            # wall 1
            glVertex3f(x, 0, -size)
            glVertex3f(x, size, -size)
            glVertex3f(x + 1, size, -size)
            glVertex3f(x + 1, 0, -size)

            # wall 2
            glVertex3f(x, 0, size)
            glVertex3f(x + 1, 0, size)
            glVertex3f(x + 1, size, size)
            glVertex3f(x, size, size)

            # wall 3
            glVertex3f(-size, 0, x)
            glVertex3f(-size, size, x)
            glVertex3f(-size, size, x + 1)
            glVertex3f(-size, 0, x + 1)

            # wall 4
            glVertex3f(size, 0, x)
            glVertex3f(size, 0, x + 1)
            glVertex3f(size, size, x + 1)
            glVertex3f(size, size, x)

        glEnd()

    def draw_hud(self):
        light_gray = (1, 1, 1)
        glColor3f(*light_gray)
        self.hud.draw_text(f"Time: {self.day_night.get_time_text()}", 20, 30)
        self.hud.draw_text(
            f"Position: X:{self.r2d2.position[0]:.1f} Y:{self.r2d2.position[1]:.1f} Z:{self.r2d2.position[2]:.1f}",
            20,
            60,
        )
        self.hud.draw_text(
            f"Gravity: {'Moon' if self.gravity==self.gravity_moon else 'Earth'} mode",
            20,
            90,
        )
        self.hud.draw_text(
            f"Speed: {np.linalg.norm(self.ball.velocity):.1f} m/s", 20, 120
        )
        self.hud.draw_compass(x=900, y=80, size=50, yaw=self.r2d2.yaw)


if __name__ == "__main__":
    scene = MainScene()
