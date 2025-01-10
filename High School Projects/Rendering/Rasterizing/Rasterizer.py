import pygame
from math import sin, cos
from numpy import arctan
from Vector3 import Vector3
from Ray import Ray
from Triangle import Triangle

WIDTH = 500
HEIGHT = 500
Vw = 1.0
Vh = 1.0
d = 1
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
DISPLAY.fill((0,0,0))
CLOCK = pygame.time.Clock()

WHITE = (255,255,255)
BLACK = (0,0,0)

SIZE = 100

CAMERA_X = 0
CAMERA_Y = 0
CAMERA_Z = 0

x0, x1 = -1.0, 1.0
y0, y1 = -1.0, 1.0

def rad(num):
    return num * (3.14159265358979/180)

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2


CAMERA = Vector3(CAMERA_X, CAMERA_Y, CAMERA_Z)

def ViewportToCanvas(x, y):
    return Vector3((x * WIDTH/Vw)+WIDTH//2, -(y * HEIGHT/Vh)+HEIGHT//2, d)

def ProjectVertex(v):
    Vx, Vy, Vz = v.x, v.y, v.z
    return ViewportToCanvas(Vx*d/Vz, Vy*d/Vz)

def move(triangle, movement):
    p1, p2, p3 = triangle.p1, triangle.p2, triangle.p3
    return Triangle(p1+movement, p2+movement, p3+movement)
    
    
def draw_triangle(triangle):
    p1 = triangle.p1.x, triangle.p1.y
    p2 = triangle.p2.x, triangle.p2.y
    p3 = triangle.p3.x, triangle.p3.y
    pygame.draw.polygon(DISPLAY, WHITE, [p1,p2,p3])

def render_triangle(triangle):
    points = [triangle.p1, triangle.p2, triangle.p3]
    new_points = []
    for point in points:
        new_point = ProjectVertex(point)
        new_points.append(new_point)
    new_triangle = Triangle(new_points[0],new_points[1],new_points[2])
    draw_triangle(new_triangle)

tri1 = Triangle(Vector3(-1,-1,3),Vector3(1,0,4), Vector3(1,1,3))

running = True
while running:
    movement = Vector3()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        movement.x = .1
    if keys[pygame.K_RIGHT]:
        movement.x = -.1
    if keys[pygame.K_UP]:
        movement.z = -.1
    if keys[pygame.K_DOWN]:
        movement.z = .1

    DISPLAY.fill(BLACK)
    tri1 = move(tri1, movement)
    render_triangle(tri1)
    pygame.display.flip()
    CLOCK.tick(60)
pygame.quit()
    
