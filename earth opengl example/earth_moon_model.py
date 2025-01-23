import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import sin, cos, pi
import random

def draw_earth(angle_earth):
    glPushMatrix()
    glColor3f(0.0, 0.0, 0.5)  # Set the color to a darker blue
    glRotatef(angle_earth * 2, 0, 0, 1)  # Rotate the earth on its own axis
    earth_emission = [0.02, 0.02, 0.1, 1.0]  # Emissive color for the earth
    glMaterialfv(GL_FRONT, GL_EMISSION, earth_emission)  # Apply the emissive color
    quad = gluNewQuadric()
    gluSphere(quad, 2.0, 32, 32)  # Draw the earth
    gluDeleteQuadric(quad)
    glMaterialfv(GL_FRONT, GL_EMISSION, [0, 0, 0, 1])  # Reset the emissive color
    glPopMatrix()

def draw_moon(angle_moon, distance_moon_earth):
    glPushMatrix()
    if 90 <= angle_moon <= 270:  # The earth is between the moon and the light source
        glColor3f(0.3, 0.3, 0.3)  # Set the color to dark gray
    else:
        glColor3f(0.7, 0.7, 0.7)  # Set the color to gray
    glRotatef(angle_moon, 0, 1, 0)  # Rotate the moon around the earth
    glTranslatef(distance_moon_earth * cos(angle_moon), 0, distance_moon_earth * sin(angle_moon))  # Move the moon away from the earth
    glRotatef(angle_moon * 2, 0, 0, 1)  # Rotate the moon on its own axis
    quad = gluNewQuadric()
    gluSphere(quad, 0.5, 32, 32)  # Draw the moon
    gluDeleteQuadric(quad)
    glPopMatrix()

def drawOrbit(distance_moon_earth):
    glBegin(GL_LINE_LOOP)
    glColor3f(1.0, 1.0, 1.0)  # Set the color to white
    for i in range(100):
        angle = 2 * pi * i / 100
        glVertex3f(distance_moon_earth * cos(angle), 0, distance_moon_earth * sin(angle))
    glEnd()

def drawStars():
    glColor3f(1.0, 1.0, 1.0)
    glPointSize(2.0)
    glBegin(GL_POINTS)
    for _ in range(1000):
        x = random.uniform(-50, 50)
        y = random.uniform(-50, 50)
        z = random.uniform(-50, 50)
        glVertex3f(x, y, z)
    glEnd()

def main():
    pg.mixer.pre_init(44100,16,2,4096)
    pg.init()
    display = (1200, 800)
    pg.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -25)
    glRotatef(-60, 1, 0, 0)  # Lower the viewing angle
    light_ambient = [0.1, 0.1, 0.1, 1.0]
    light_diffuse = [5.0, 5.0, 5.0, 1.0]  # Increase the intensity of the diffuse light
    light_specular = [4.0, 4.0, 4.0, 1.0]
    light_position = [4.0, 4.0, 4.0, 0.0]
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    glEnable(GL_LIGHT1)  # Enable the second light source
    glLightfv(GL_LIGHT1, GL_POSITION, [-5.0, -5.0, -5.0, 0.0])  # Set position of the second light source
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [1.0, 0.5, 0.0, 1.0])  # Solar color for the second light source
    glLightfv(GL_LIGHT1, GL_SPECULAR, [1.0, 0.5, 0.0, 1.0])
    angle_earth = 0
    angle_moon = 0
    distance_moon_earth = 8.0  # Increase the distance between the moon and the earth

    # #play background music
    # pg.mixer.music.load("space.mp3")
    # pg.mixer.music.set_volume(.6)
    # pg.mixer.music.play(-1)

    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                quit()
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        drawStars()
        draw_earth(angle_earth)  # Draw the earth
        draw_moon(angle_moon, distance_moon_earth)  # Draw the moon
        glColor4f(1.0, 1.0, 1.0, 1.0)  # Set the color to white
        drawOrbit(distance_moon_earth)  # Draw the orbit at the moon's distance
        angle_earth += 0.1
        angle_moon += 0.01  # The moon moves faster than the earth
        pg.display.flip()
        pg.time.wait(10)

if __name__ == "__main__":
    main()