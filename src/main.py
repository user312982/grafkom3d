import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

from r2d2_model import *
from day_night_cycle import DayNightCycle
from hud import HUD
from camera import Camera
from object_3d import Object3D


class MainScene:
    def __init__(self):
        pygame.init()
        self.display = (1000, 600)
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        self.init_gl()

        self.hud = HUD(self.display)
        self.day_night = DayNightCycle()

        self.r2d2 = Object3D(
            position=[0.0, 5, 0.0],
            mass=1.0,
            speed=3.0,
            jump_speed=5.0,
            max_speed=3.0,
            run_multiplier=3.0,
        )

        self.circle = Object3D(
            position=[5, 50, 0.0],
            mass=1.0,
            speed=3.0,
            jump_speed=5.0,
            max_speed=3.0,
            run_multiplier=3.0,
        )

        self.gravity_earth = 9.8
        self.gravity_moon = 1.62
        self.gravity = self.gravity_earth
        self.yaw = 0.0

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
                "ctrl": keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL],
            }

            self.r2d2.update(dt, keymap, gravity=self.gravity)
            self.camera.update(keymap, self.r2d2.position, self.r2d2.yaw)

            # Gambar objek langit
            self.draw_ground()
            self.day_night.draw_sky_objects()

            # This means any transformations (like moving or rotating) you do between glPushMatrix() and glPopMatrix() will only affect the drawing of R2-D2, not the rest of the scene.
            glPushMatrix()
            glTranslatef(*self.r2d2.position)
            glRotatef(self.r2d2.yaw, 0, 1, 0)
            draw_r2d2()
            glPopMatrix()

            glPushMatrix()
            glTranslatef(*self.circle.position)
            quad = gluNewQuadric()
            gluSphere(quad, 0.4, 32, 16)
            self.circle.update(dt, {}, gravity=self.gravity)
            gluDeleteQuadric(quad)
            glPopMatrix()

            self.draw_hud()
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
                if event.key == pygame.K_SPACE:
                    self.r2d2.jump()

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

    def draw_hud(self):
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
            f"Speed: {np.linalg.norm(self.r2d2.velocity):.1f} m/s", 20, 120
        )
        self.hud.draw_compass(x=900, y=80, size=50, yaw=self.yaw)


if __name__ == "__main__":
    scene = MainScene()
