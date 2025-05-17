import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

from r2d2_model import *  # import fungsi draw_r2d2 dari file lain
from day_night_cycle import DayNightCycle
from hud import HUD
from camera import Camera


class MainScene:
    def __init__(self):
        pygame.init()
        display = (1000, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

        # Inisialisasi HUD
        hud = HUD(display)

        # Inisialisasi sistem waktu
        day_night = DayNightCycle()

        glEnable(GL_DEPTH_TEST)
        glClearColor(0.5, 0.7, 1.0, 1.0)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        pos = np.array([0.0, 0.5, 0.0])
        velocity = np.array([0.0, 0.0, 0.0])
        speed = 3.0
        jump_speed = 5.0
        gravity_earth = 9.8
        gravity_moon = 1.62
        gravity = gravity_earth
        on_ground = False
        acceleration = 10.0  # m/s²
        deceleration = 12.0  # m/s²
        max_speed = 3.0
        run_multiplier = 3.0

        yaw = 0.0  # sudut rotasi horizontal (derajat)

        camera = Camera(offset=(0, 2, 6))

        clock = pygame.time.Clock()
        gravity_toggle_key = pygame.K_h

        running = True
        while running:
            dt = clock.tick(60) / 1000  # detik/frame

            # Update waktu
            day_night.update(dt)

            # Set background color
            sky_color = day_night.get_sky_color()
            glClearColor(*sky_color, 1.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # Setup pencahayaan
            day_night.setup_lighting()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == gravity_toggle_key:
                        gravity = (
                            gravity_moon if gravity == gravity_earth else gravity_earth
                        )
                        print(
                            f"Gravitasi diganti ke {'Bulan' if gravity==gravity_moon else 'Bumi'} ({gravity:.2f} m/s²)"
                        )
                    if event.key == pygame.K_SPACE and on_ground:
                        velocity[1] = jump_speed
                        on_ground = False

            keys = pygame.key.get_pressed()

            # Rotasi dengan arrow kiri dan kanan
            if keys[pygame.K_LEFT]:
                yaw += 90 * dt  # putar ke kiri 90 derajat per detik
            if keys[pygame.K_RIGHT]:
                yaw -= 90 * dt  # putar ke kanan 90 derajat per detik

            # Hitung arah maju berdasarkan yaw (rotasi)
            forward = np.array([np.sin(np.radians(yaw)), 0, np.cos(np.radians(yaw))])

            # Arah samping (strafe) adalah vektor tegak lurus forward di bidang horizontal
            right = np.array([np.cos(np.radians(yaw)), 0, -np.sin(np.radians(yaw))])

            move_dir = np.array([0.0, 0.0, 0.0])
            # WASD untuk maju mundur dan strafing
            if keys[pygame.K_w]:
                move_dir += forward
            if keys[pygame.K_s]:
                move_dir -= forward
            if keys[pygame.K_d]:
                move_dir -= right
            if keys[pygame.K_a]:
                move_dir += right

            if np.linalg.norm(move_dir) > 0:
                move_dir = move_dir / np.linalg.norm(move_dir)

            # Tentukan target speed (jalan atau lari)
            target_speed = max_speed

            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                target_speed *= run_multiplier

            # GLBB: percepat atau perlambat velocity horizontal
            for i in [0, 2]:  # hanya sumbu X dan Z
                if np.abs(move_dir[i]) > 0:
                    # percepatan ke arah target
                    desired_velocity = move_dir[i] * target_speed
                    delta_v = desired_velocity - velocity[i]
                    step = acceleration * dt

                    if np.abs(delta_v) < step:
                        velocity[i] = desired_velocity
                    else:
                        velocity[i] += step * np.sign(delta_v)
                else:
                    if np.abs(velocity[i]) > 0:
                        step = deceleration * dt
                        if np.abs(velocity[i]) < step:
                            velocity[i] = 0
                        else:
                            velocity[i] -= step * np.sign(velocity[i])

            # Update vertikal velocity dengan gravitasi
            velocity[1] -= gravity * dt
            pos += velocity * dt

            # Collision dengan lantai
            if pos[1] <= 0.5:
                pos[1] = 0.5
                velocity[1] = 0
                on_ground = True

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()

            camera.update(pos, yaw)
            camera.apply()

            # Gambar objek langit
            # Gambar ground dan R2-D2
            self.draw_ground()
            day_night.draw_sky_objects()
            glPushMatrix()
            glTranslatef(*pos)
            glRotatef(yaw, 0, 1, 0)
            draw_r2d2()
            glPopMatrix()

            hud.draw_text(f"Time: {day_night.get_time_text()}", 20, 30)
            hud.draw_text(
                f"Position: X:{pos[0]:.1f} Y:{pos[1]:.1f} Z:{pos[2]:.1f}", 20, 60
            )
            hud.draw_text(
                f"Gravity: {'Moon' if gravity==gravity_moon else 'Earth'} mode", 20, 90
            )
            hud.draw_text(f"Speed: {np.linalg.norm(velocity):.1f} m/s", 20, 120)
            hud.draw_compass(x=900, y=80, size=50, yaw=yaw)

            pygame.display.flip()

        pygame.quit()

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


if __name__ == "__main__":
    scene = MainScene()
