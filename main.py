import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

from r2d2_model import *  # import fungsi draw_r2d2 dari file lain

from day_night_cycle import DayNightCycle

from hud import HUD

def draw_ground(size=20, tile_size=1):
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



def main():
    pygame.init()
    display = (1000,600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # Inisialisasi HUD
    hud = HUD(display)
    
    # Inisialisasi sistem waktu
    day_night = DayNightCycle()

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.5, 0.7, 1.0, 1.0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

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

    yaw = 0.0  # sudut rotasi horizontal (derajat)

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
                    gravity = gravity_moon if gravity == gravity_earth else gravity_earth
                    print(f"Gravitasi diganti ke {'Bulan' if gravity==gravity_moon else 'Bumi'} ({gravity:.2f} m/s²)")
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
        forward = np.array([
            np.sin(np.radians(yaw)),
            0,
            np.cos(np.radians(yaw))
        ])

        # Arah samping (strafe) adalah vektor tegak lurus forward di bidang horizontal
        right = np.array([
            np.cos(np.radians(yaw)),
            0,
            -np.sin(np.radians(yaw))
        ])

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

        velocity[0] = move_dir[0] * speed
        velocity[2] = move_dir[2] * speed

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

        # Kamera third person di belakang dan sedikit di atas posisi r2d2
        cam_offset = np.array([0, 2, 6])

        # Putar offset kamera sesuai yaw agar kamera ikut berputar mengikuti objek
        cos_yaw = np.cos(np.radians(yaw))
        sin_yaw = np.sin(np.radians(yaw))
        cam_x = pos[0] - cam_offset[2] * sin_yaw
        cam_y = pos[1] + cam_offset[1]
        cam_z = pos[2] - cam_offset[2] * cos_yaw

        # Kamera menghadap ke posisi r2d2
        gluLookAt(cam_x, cam_y, cam_z, pos[0], pos[1], pos[2], 0,1,0)

        draw_ground()

        glPushMatrix()
        glTranslatef(*pos)
        glRotatef(yaw, 0, 1, 0)  # putar r2d2 sesuai yaw (hadap ke arah yang sama)
        draw_r2d2()
        glPopMatrix()

        # Gambar objek langit
        day_night.draw_sky_objects()
        
        # Gambar ground dan R2-D2
        draw_ground()
        glPushMatrix()
        glTranslatef(*pos)
        glRotatef(yaw, 0, 1, 0)
        draw_r2d2()
        glPopMatrix()
        

        # HUD elements
        hud.draw_text(f"Time: {day_night.get_time_text()}", 20, 30)
        hud.draw_text(f"Position: X:{pos[0]:.1f} Y:{pos[1]:.1f} Z:{pos[2]:.1f}", 20, 60)
        hud.draw_text(f"Gravity: {'Moon' if gravity==gravity_moon else 'Earth'} mode", 20, 90)
        hud.draw_text(f"Speed: {np.linalg.norm(velocity):.1f} m/s", 20, 120)
        hud.draw_compass(x=900, y=80, size=50, yaw=yaw)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
