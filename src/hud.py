import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import cos, sin, radians


class HUD:
    def __init__(self, display_size,):
        self.display_size = display_size
        self.textures = {}
        self.font_cache = {}
        
    def get_font(self, size):
        if size not in self.font_cache:
            self.font_cache[size] = pygame.font.SysFont('Arial', size)
        return self.font_cache[size]

        
    def draw_text(self, text, x, y, size=24, color=(255, 255, 255)):
        key = (text, size, color)
        if key not in self.textures:
            font = self.get_font(size)
            text_surface = font.render(text, True, color)
            text_data = pygame.image.tostring(text_surface, "RGBA", True)
            width, height = text_surface.get_size()

            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

            self.textures[key] = (texture_id, width, height)
        else:
            texture_id, width, height = self.textures[key]
            font = self.get_font(size)
            text_surface = font.render(text, True, color)
            text_data = pygame.image.tostring(text_surface, "RGBA", True)
            width, height = text_surface.get_size()

        glDisable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Generate texture
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # Setup ortho 2D
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, self.display_size[0], 0, self.display_size[1])

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # Draw quad with texture
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(x, y)
        glTexCoord2f(1, 0); glVertex2f(x + width, y)
        glTexCoord2f(1, 1); glVertex2f(x + width, y + height)
        glTexCoord2f(0, 1); glVertex2f(x, y + height)
        glEnd()

        # Clean up
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        glDeleteTextures([texture_id])
        glDisable(GL_BLEND)
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_LIGHTING)

    def draw_compass(self, x, y, size, yaw):
        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)
        
        # Setup 2D orthographic projection
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, self.display_size[0], 0, self.display_size[1])  # Bawah ke atas
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # Pindahkan ke posisi (x, y) pada layar
        glTranslatef(x, y, 0)

        # Gambar lingkaran kompas
        glColor3f(0.2, 0.2, 0.5)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(0, 0)  # Pusat
        for angle in range(0, 361, 10):
            rad = radians(angle)
            glVertex2f(cos(rad) * size, sin(rad) * size)
        glEnd()

        # Gambar jarum arah utara
        glPushMatrix()
        glRotatef(-yaw, 0, 0, 1)  # Rotasi terhadap pusat kompas
        glColor3f(1, 0, 0)  # Merah untuk utara
        glBegin(GL_TRIANGLES)
        glVertex2f(0, size * 0.9)
        glVertex2f(-size * 0.1, 0)
        glVertex2f(size * 0.1, 0)
        glEnd()
        glPopMatrix()

        # Kembalikan matrix
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
