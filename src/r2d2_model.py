from OpenGL.GL import *
from OpenGL.GLU import *
from math import cos, sin, pi

def draw_cylinder(radius=0.5, height=1.0, slices=32):
    quad = gluNewQuadric()
    gluCylinder(quad, radius, radius, height, slices, 1)
    gluDeleteQuadric(quad)

def draw_disk(radius=0.5, slices=32):
    quad = gluNewQuadric()
    gluDisk(quad, 0, radius, slices, 1)
    gluDeleteQuadric(quad)

def draw_partial_disk(inner, outer, slices, rings, start, sweep):
    quad = gluNewQuadric()
    gluPartialDisk(quad, inner, outer, slices, rings, start, sweep)
    gluDeleteQuadric(quad)

def draw_sphere(radius=0.5, slices=32, stacks=16):
    quad = gluNewQuadric()
    gluSphere(quad, radius, slices, stacks)
    gluDeleteQuadric(quad)

def draw_half_sphere(radius=0.4, slices=32, stacks=16):
    quad = gluNewQuadric()
    for i in range(stacks // 2, stacks):
        lat0 = pi * (-0.5 + float(i) / stacks)
        z0 = sin(lat0)
        zr0 = cos(lat0)

        lat1 = pi * (-0.5 + float(i + 1) / stacks)
        z1 = sin(lat1)
        zr1 = cos(lat1)

        glBegin(GL_QUAD_STRIP)
        for j in range(slices + 1):
            lng = 2 * pi * float(j) / slices
            x = cos(lng)
            y = sin(lng)

            glNormal3f(x * zr0, y * zr0, z0)
            glVertex3f(radius * x * zr0, radius * y * zr0, radius * z0)

            glNormal3f(x * zr1, y * zr1, z1)
            glVertex3f(radius * x * zr1, radius * y * zr1, radius * z1)
        glEnd()
    gluDeleteQuadric(quad)


def draw_cube(size=1.0):
    half = size / 2.0
    glBegin(GL_QUADS)
    
    # Front face
    glNormal3f(0, 0, 1)
    glVertex3f(-half, -half, half)
    glVertex3f(half, -half, half)
    glVertex3f(half, half, half)
    glVertex3f(-half, half, half)
    
    # Back face
    glNormal3f(0, 0, -1)
    glVertex3f(-half, -half, -half)
    glVertex3f(-half, half, -half)
    glVertex3f(half, half, -half)
    glVertex3f(half, -half, -half)
    
    # Left face
    glNormal3f(-1, 0, 0)
    glVertex3f(-half, -half, -half)
    glVertex3f(-half, -half, half)
    glVertex3f(-half, half, half)
    glVertex3f(-half, half, -half)
    
    # Right face
    glNormal3f(1, 0, 0)
    glVertex3f(half, -half, -half)
    glVertex3f(half, half, -half)
    glVertex3f(half, half, half)
    glVertex3f(half, -half, half)
    
    # Top face
    glNormal3f(0, 1, 0)
    glVertex3f(-half, half, -half)
    glVertex3f(-half, half, half)
    glVertex3f(half, half, half)
    glVertex3f(half, half, -half)
    
    # Bottom face
    glNormal3f(0, -1, 0)
    glVertex3f(-half, -half, -half)
    glVertex3f(half, -half, -half)
    glVertex3f(half, -half, half)
    glVertex3f(-half, -half, half)
    
    glEnd()

def draw_r2d2():
    glPushMatrix()
    
    # Main body (white cylinder)
    glColor3f(0.95, 0.95, 0.95)
    glRotatef(-90, 1, 0, 0)  # Rotate cylinder to stand vertically
    draw_cylinder(radius=0.5, height=1.2)
    
    # Blue panels on body
    glColor3f(0.1, 0.3, 0.8)
    for i in range(6):
        glPushMatrix()
        glRotatef(i * 60, 0, 0, 1)
        glTranslatef(0.45, 0, 0.2)
        glScalef(0.15, 0.02, 0.8)
        draw_cube()
        glPopMatrix()
    
    # Lower blue ring
    glPushMatrix()
    glTranslatef(0, 0, 0.1)
    draw_disk(radius=0.51)
    glTranslatef(0, 0, -0.01)
    draw_partial_disk(0.45, 0.51, 32, 1, 0, 360)
    glPopMatrix()
    
    # Middle dome (head)
    glTranslatef(0, 0, 1.2)
    glColor3f(0.95, 0.95, 0.95)
    draw_disk(radius=0.5)
    
    # Dome top
    glPushMatrix()
    glTranslatef(0, -0.05, 0.005)
    draw_half_sphere(radius=0.50, slices=32, stacks=16)
    
    # Dome details
    glColor3f(0.1, 0.3, 0.8)
    
    # Main eye
    glPushMatrix()
    glTranslatef(0, 0.35, 0.1)
    glRotatef(90, 1, 0, 0)
    draw_cylinder(radius=0.08, height=0.1)
    glTranslatef(0, 0, 0.1)
    glColor3f(0.7, 0.1, 0.1)  # Red eye
    draw_disk(radius=0.08)
    glPopMatrix()
    
    # Side panels
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(side * 0.2, 0.25, 0.1)
        glScalef(0.15, 0.05, 0.02)
        draw_cube()
        glPopMatrix()
    
    # Front panel
    glPushMatrix()
    glTranslatef(0, 0.2, 0.2)
    glScalef(0.2, 0.05, 0.02)
    draw_cube()
    glPopMatrix()
    
    glPopMatrix()  # End of dome details
    
    # Kaki-kaki (sekarang di bawah)
    glPushMatrix()
    glTranslatef(0, 0, -1.2)  # Pindahkan kaki ke bawah body
    
    # Kaki depan kiri
    glPushMatrix()
    glTranslatef(-0.35, 0, 0)
    glColor3f(0.8, 0.8, 0.8)
    
    # Bagian utama kaki
    glPushMatrix()
    glScalef(0.3, 0.8, 0.3)
    draw_cube()
    glPopMatrix()
    
    # Kaki bawah
    glPushMatrix()
    glTranslatef(0, -0.5, 0)
    glScalef(0.4, 0.1, 0.5)
    draw_cube()
    glPopMatrix()
    
    # Detail pergelangan kaki
    glColor3f(0.1, 0.3, 0.8)
    glPushMatrix()
    glTranslatef(0, -0.2, 0.2)
    glScalef(0.25, 0.1, 0.05)
    draw_cube()
    glPopMatrix()
    
    glPopMatrix()  # End kaki depan kiri
    
    # Kaki depan kanan
    glPushMatrix()
    glTranslatef(0.35, 0, 0)
    glColor3f(0.8, 0.8, 0.8)
    
    # Bagian utama kaki
    glPushMatrix()
    glScalef(0.3, 0.8, 0.3)
    draw_cube()
    glPopMatrix()
    
    # Kaki bawah
    glPushMatrix()
    glTranslatef(0, -0.5, 0)
    glScalef(0.4, 0.1, 0.5)
    draw_cube()
    glPopMatrix()
    
    # Detail pergelangan kaki
    glColor3f(0.1, 0.3, 0.8)
    glPushMatrix()
    glTranslatef(0, -0.2, 0.2)
    glScalef(0.25, 0.1, 0.05)
    draw_cube()
    glPopMatrix()
    
    glPopMatrix()  # End kaki depan kanan
    
    # Kaki belakang
    glPushMatrix()
    glTranslatef(0, 0, 0.3)
    glColor3f(0.8, 0.8, 0.8)
    
    # Bagian utama kaki
    glPushMatrix()
    glScalef(0.25, 0.6, 0.25)
    draw_cube()
    glPopMatrix()
    
    # Kaki bawah
    glPushMatrix()
    glTranslatef(0, -0.4, -0.1)
    glScalef(0.3, 0.1, 0.4)
    draw_cube()
    glPopMatrix()
    
    glPopMatrix()  # End kaki belakang
    
    glPopMatrix()  # End semua kaki
    
    # Arms (di sisi badan dan mengarah ke bawah)
    for side in [-1, 1]:
        glPushMatrix()

        # Tempel di sisi badan dan cukup rendah
        glTranslatef(side * 0.60, 0, -0.5)  # sisi badan (x), tinggi tengah (z)
        glRotatef(180, 1, 0, 0)            # arahkan ke bawah (rotasi ke bawah)

        # Bagian atas lengan (kecil)

        glColor3f(0.8, 0.8, 0.8)
        glPushMatrix()
        glTranslatef(side * -0.05, 0, 0)
        glRotatef(5 * side, 0, 1, 0)
        glRotatef(-5 * -side, 0, 1, 0)
        glScalef(0.1, 0.1, 0.4)  # segmen atas, lebih kecil
        draw_cube()
        glPopMatrix()

        # Bagian bawah lengan (besar)
        glPushMatrix()
        glTranslatef(0, 0, 0.4)  # geser ke ujung segmen atas
        glScalef(0.15, 0.15, 0.4)  # segmen bawah, lebih besar
        draw_cube()
        glPopMatrix()

        # Tool di ujung lengan
        glColor3f(0.3, 0.3, 0.3)
        glPushMatrix()
        glTranslatef(0, 0, 0.6)
        glRotatef(0, 1, 0, 0)
        draw_cylinder(radius=0.05, height=0.2)
        glPopMatrix()

        glPopMatrix()



    
    glPopMatrix()  # End of R2-D2