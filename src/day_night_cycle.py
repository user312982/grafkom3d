import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from math import sin, cos, radians, pi
import random

class DayNightCycle:
    def __init__(self):
        self.time_of_day = 12.0  # Jam mulai pukul 12.00 siang
        self.day_speed = 0.05    # Kecepatan waktu (jam per detik realtime)
        self.is_daytime = True   # Status siang/malam
    
    def update(self, dt):
        self.time_of_day = (self.time_of_day + self.day_speed * dt) % 24
        self.is_daytime = 6 < self.time_of_day < 18
    
    def get_sky_color(self):
        if self.is_daytime:
            progress = (self.time_of_day - 6) / 12
            if self.time_of_day < 12:
                return (0.3 + 0.2 * progress, 0.5 + 0.2 * progress, 0.8 + 0.2 * progress)
            else:
                return (0.5 - 0.2 * (progress-0.5), 0.7 - 0.2 * (progress-0.5), 1.0 - 0.3 * (progress-0.5))
        else:
            progress = (self.time_of_day - 18) / 12 if self.time_of_day > 18 else (self.time_of_day + 6) / 12
            darkness = 0.1 + 0.9 * (1 - abs(progress - 0.5) * 2)
            return (0.05 * darkness, 0.05 * darkness, 0.15 * darkness)
    
    def get_sun_position(self):
        sun_angle = (self.time_of_day / 24) * 2 * pi - pi/2
        sun_distance = 20
        return (
            sun_distance * cos(sun_angle),
            max(0, sun_distance * sin(sun_angle)),
            sun_distance * 0.5
        )
    
    def get_moon_position(self):
        moon_angle = (self.time_of_day / 24) * 2 * pi + pi/2
        moon_distance = 20
        return (
            moon_distance * cos(moon_angle),
            max(0, moon_distance * sin(moon_angle)),
            moon_distance * 0.5
        )
    
    def setup_lighting(self):
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        
        # Matahari
        sun_pos = self.get_sun_position()
        if self.is_daytime:
            sun_intensity = max(0.2, sin(pi * (self.time_of_day - 6)/12))
            glLightfv(GL_LIGHT0, GL_POSITION, [sun_pos[0], sun_pos[1], sun_pos[2], 1.0])
            glLightfv(GL_LIGHT0, GL_DIFFUSE, [sun_intensity, sun_intensity, sun_intensity, 1.0])
            glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
            glEnable(GL_LIGHT0)
        else:
            glDisable(GL_LIGHT0)
        
        # Bulan
        moon_pos = self.get_moon_position()
        if not self.is_daytime:
            moon_intensity = max(0.1, 0.3 * sin(pi * (self.time_of_day - 18)/12))
            glLightfv(GL_LIGHT1, GL_POSITION, [moon_pos[0], moon_pos[1], moon_pos[2], 1.0])
            glLightfv(GL_LIGHT1, GL_DIFFUSE, [moon_intensity*0.7, moon_intensity*0.7, moon_intensity, 1.0])
            glLightfv(GL_LIGHT1, GL_AMBIENT, [0.05, 0.05, 0.1, 1.0])
            glEnable(GL_LIGHT1)
        else:
            glDisable(GL_LIGHT1)
    
    def draw_sky_objects(self):
        sun_pos = self.get_sun_position()
        moon_pos = self.get_moon_position()
        
        glPushMatrix()
        glDisable(GL_LIGHTING)
        
        if sun_pos[1] > 0:
            glTranslatef(*sun_pos)
            glColor3f(1, 0.9, 0)
            glutSolidSphere(1.0, 16, 16)
        
        if moon_pos[1] > 0:
            glTranslatef(moon_pos[0]-sun_pos[0], moon_pos[1]-sun_pos[1], moon_pos[2]-sun_pos[2])
            glColor3f(0.8, 0.8, 0.9)
            glutSolidSphere(0.8, 16, 16)
        
        glEnable(GL_LIGHTING)
        glPopMatrix()
    
    def get_time_text(self):
        return f"{int(self.time_of_day):02d}:{int((self.time_of_day%1)*60):02d} {'AM' if self.time_of_day < 12 else 'PM'}"
    
    def draw_sky_objects(self):
        sun_pos = self.get_sun_position()
        moon_pos = self.get_moon_position()
        
        glPushMatrix()
        glDisable(GL_LIGHTING)
        
        if sun_pos[1] > 0:
            glTranslatef(*sun_pos)
            glColor3f(1, 0.9, 0)
            quadric = gluNewQuadric()
            gluSphere(quadric, 1.0, 16, 16)
            gluDeleteQuadric(quadric)
        
        if moon_pos[1] > 0:
            glTranslatef(moon_pos[0]-sun_pos[0], moon_pos[1]-sun_pos[1], moon_pos[2]-sun_pos[2])
            glColor3f(0.8, 0.8, 0.9)
            quadric = gluNewQuadric()
            gluSphere(quadric, 0.8, 16, 16)
            gluDeleteQuadric(quadric)
        
        glEnable(GL_LIGHTING)
        glPopMatrix()