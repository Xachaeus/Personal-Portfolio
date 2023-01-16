import pygame
from Triangle import Triangle
from Vector3 import Vector3
from Camera import Camera
from Box import Box
from math import sin, cos

def radians(val):
    return val * 3.141592653589793432/180

WHITE = (255,255,255)
GREY = (150,150,150)
BLACK = (0,0,0)
BLUE = (0,150,200)

SPEED = 10

Cw = 600
Ch = 600
Vw = 1.0
Vh = 1.0
d = 1
canvas = pygame.display.set_mode((Cw,Ch))
pygame.display.set_caption("3D Engine Test")
CLOCK = pygame.time.Clock()

camera = Camera(Vector3(0,0,0),0,0,0,Vw,Vh,d,Cw,Ch)

ground = Box(Vector3(0,-1,0),50,1,50)

boxes = [Box(Vector3(0,0,3),3,3,3)]

px = 0
pz = -30
py = 0

dir = 0
pitch = 0

deltaTime = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        pz += cos(dir)*SPEED*deltaTime
        px += sin(dir)*SPEED*deltaTime
    if keys[pygame.K_s]:
        pz -= cos(dir)*SPEED*deltaTime
        px -= sin(dir)*SPEED*deltaTime
    if keys[pygame.K_a]:
        px += sin(dir-radians(90))*SPEED*deltaTime
        pz += cos(dir-radians(90))*SPEED*deltaTime
    if keys[pygame.K_d]:
        px += sin(dir+radians(90))*SPEED*deltaTime
        pz += cos(dir+radians(90))*SPEED*deltaTime
    if keys[pygame.K_LEFT]:
        dir -= radians(SPEED*10)*deltaTime
    if keys[pygame.K_RIGHT]:
        dir += radians(SPEED*10)*deltaTime
    if keys[pygame.K_SPACE]:
        py += SPEED*deltaTime
    if keys[pygame.K_LSHIFT]:
        py -= SPEED*deltaTime
    if keys[pygame.K_UP]:
        pitch -= radians(SPEED*10)*deltaTime
    if keys[pygame.K_DOWN]:
        pitch += radians(SPEED*10)*deltaTime

    if pitch < -radians(90):
        pitch = -radians(90)
    if pitch > radians(90):
        pitch = radians(90)
    
    
    camera.position = Vector3(px,py,pz)
    camera.yaw = dir
    camera.pitch = pitch

    canvas.fill(BLUE)
    camera.render_box(canvas,(0,255,0),ground)
    camera.render_boxes(canvas, GREY, boxes)
    

    pygame.display.flip()
    deltaTime = CLOCK.tick(60)/1000
pygame.quit()
