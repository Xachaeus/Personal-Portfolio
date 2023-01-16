from math import sqrt
import pygame

def interpolate(p0, p1):
    i0, d0 = p0
    i1, d1 = p1

    if i0 == i1:

        return [d0]

    values = []

    a = (d1 - d0)/(i1 - i0)

    d = d0

    i = i0

    while i <= i1:

        values.append(int(d))
        d = d + a
        i += 1

    return values

def line(canvas, p0, p1, color = (0,0,0)):

    x0, y0 = p0
    x1, y1 = p1

    width, height = canvas.get_size()

    if abs(x1 - x0) > abs(y1 - y0):

        if x0 > x1:
            x0, y0 = p1
            x1, y1 = p0

        ys = interpolate((x0, y0), (x1, y1))

        x = x0
        while x <= x1:
            if x <= width and ys[x - x0] <= height:
                canvas.set_at((x, ys[x - x0]), color)
            x += 1

    else:

        if y0 > y1:
            x0, y0 = p1
            x1, y1 = p0

        xs = interpolate((y0, x0), (y1, x1))

        y = y0
        while y <= y1:
            if xs[y - y0] <= width and y <= height:
                canvas.set_at((xs[y - y0], y), color)
            y += 1

def draw_wireframe_triangle(canvas, p0, p1, p2, color=(0,0,0)):

    line(canvas, p0, p1, color)
    line(canvas, p1, p2, color)
    line(canvas, p2, p0, color)

def draw_triangle(canvas, p0, p1, p2, color=(0,0,0)):

    x0, y0 = p0
    x1, y1 = p1
    x2, y2 = p2

    if y1 < y0:
        x0, y0 = p1
        x1, y1 = p0
    if y2 < y0:
        x0, y0 = p2
        x2, y2 = p0
    if y2 < y1:
        x1, y1 = p2
        x2, y2 = p1
        
    


canvas = pygame.display.set_mode((400, 400))
canvas.fill((255,255,255))

draw_wireframe_triangle(canvas, (200,60), (25, 350), (350, 250))

pygame.display.flip()


























            
