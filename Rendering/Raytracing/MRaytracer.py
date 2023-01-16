import pygame, random
from math import sin, cos, asin, acos, atan2
PI = 3.14159265

WIDTH = 500
HEIGHT = 500
DISPLAY = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Raytracer")
CLOCK = pygame.time.Clock()

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)

def line(point1, point2, color=WHITE):
    pygame.draw.line(DISPLAY, color, point1, point2)

def deg(val):
    return val*(180/PI)
def rad(val):
    return val*(PI/180)

def angle(point1, point2):
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    angle = atan2(dx, dy)

    if angle<0: angle = 2*PI - abs(angle)

    angle = angle-rad(90)
    return(angle)

def dist(point1, point2):
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    return ((dx*dx)+(dy*dy))**(1/2)


RUNNING = True
while RUNNING:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: RUNNING = False

    mouse = pygame.mouse.get_pos()

    #mouse = (random.randint(0,WIDTH), random.randint(0,HEIGHT))

    DISPLAY.fill(BLACK)

    line((250,250), mouse)

    Angle = angle((250,250), mouse)

    print(deg(Angle))

    length = dist((250,250), mouse)
    Dy = -(sin(Angle)*length)
    Dx = cos(Angle)*length

    x = 250+Dx
    y = 250+Dy

    line((250,250), (x,y), RED)

    

    pygame.display.update()

    CLOCK.tick(60)

pygame.quit()

    
