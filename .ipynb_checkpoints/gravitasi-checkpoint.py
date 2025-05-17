from vpython import *

# Setup scene
scene.title = "Simulasi Pejalan Gravitasi Bumi vs Bulan"
scene.width = 800
scene.height = 600
scene.center = vector(0,1,0)

# Parameter
g_earth = 9.8
g_moon = 1.62
gravity = g_earth

# Objek pejalan (bola sederhana)
walker = sphere(pos=vector(0,1,0), radius=0.3, color=color.red)
floor = box(pos=vector(0,0,0), size=vector(10,0.2,10), color=color.green)

# Variabel fisika
velocity = vector(0,0,0)
dt = 0.01

# Status gravitasi bumi/ bulan
on_earth = True

def key_input(evt):
    global velocity, gravity, on_earth

    s = evt.key
    if s == 'left':
        velocity.x = -2
    elif s == 'right':
        velocity.x = 2
    elif s == 'up':
        velocity.z = -2
    elif s == 'down':
        velocity.z = 2
    elif s == ' ':
        # lompat hanya kalau pejalan dekat lantai
        if abs(walker.pos.y - (floor.pos.y + floor.size.y/2 + walker.radius)) < 0.01:
            velocity.y = 5
    elif s == 'g':
        # toggle gravitasi
        on_earth = not on_earth
        gravity = g_earth if on_earth else g_moon
        print("Gravitasi: BUMI" if on_earth else "Gravitasi: BULAN")

def key_up(evt):
    # berhentikan gerak saat tombol dilepas
    s = evt.key
    if s in ['left', 'right']:
        velocity.x = 0
    elif s in ['up', 'down']:
        velocity.z = 0

scene.bind('keydown', key_input)
scene.bind('keyup', key_up)

while True:
    rate(100)

    # Update physics
    velocity.y -= gravity * dt

    # Update posisi
    walker.pos += velocity * dt

    # Cek lantai supaya tidak jatuh tembus
    floor_top = floor.pos.y + floor.size.y/2
    if walker.pos.y < floor_top + walker.radius:
        walker.pos.y = floor_top + walker.radius
        velocity.y = 0

    # Kamera mengikuti walker
    scene.center = walker.pos
