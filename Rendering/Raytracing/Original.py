import pygame
#from multiproccessing import Process
from math import sin, cos

WIDTH = 200
HEIGHT = 200
DISPLAY = pygame.display.set_mode((WIDTH,HEIGHT))

def rad(val):
    return val * (3.141592/180)

def to_ppm(list):
    with open('tests.ppm', 'w') as file:
        file.write(f"P3 {WIDTH} {HEIGHT} \n255\n")
        for item in list:
            file.write(f"{item[0]} {item[1]} {item[2]}     ")

def draw_pixel(pixel, color):
    pygame.draw.line(DISPLAY, color, pixel, pixel)

class Vector3:

    """Base class for storing and operating with triple values."""
    def __init__(self, x, y=None, z=None):
        if (y is None) and (z is None):
            self.x, self.y, self.z = x
        else:
            self.x, self.y, self.z = x,y,z

    @property
    def magnitude(self):
        return (self.x**2 + self.y**2 + self.z**2)**(1/2)
    @property
    def normal(self):
        if self.magnitude != 0: return self/self.magnitude

    def dot_product(self, other):
        total = 0
        total += self.x * other.x
        total += self.y * other.y
        total += self.z * other.z
        return total

    def __mul__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x*other.x,
                           self.y*other.y,
                           self.z*other.z)
        else:
            return Vector3(self.x*other,
                           self.y*other,
                           self.z*other)
    def __truediv__(self, other):
        assert not isinstance(other, Vector3), "Canot divide by Vector3 object!"
        return Vector3(self.x/other,
                       self.y/other,
                       self.z/other)

    def __add__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x+other.x,
                           self.y+other.y,
                           self.z+other.z)
        else:
            return Vector3(self.x+other,
                           self.y+other,
                           self.z+other)

    def __sub__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x-other.x,
                           self.y-other.y,
                           self.z-other.z)
        else:
            return Vector3(self.x-other,
                           self.y-other,
                           self.z-other)

class Point(Vector3):
    pass


class Ray:

    def __init__(self, origin, direction):
        self.origin = origin
        self.dir = direction.normal

class Sphere:
    def __init__(self, position, radius, color=(255,0,0)):
        self.center = position
        self.radius = radius
        self.color = color

    def intersects(self, ray):
        sphere_to_ray = ray.origin - self.center
        #a = 1
        b = 2 * ray.dir.dot_product(sphere_to_ray)
        print(b)
        c = sphere_to_ray.dot_product(sphere_to_ray) - self.radius**2
        print(c)
        discriminant = b*b - 4*c

        if discriminant >= 0:
            dist = (-b - (discriminant**(1/2))) / 2
            if dist > 0: return dist
        return None

class Camera:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction


class RenderEngine:

    def __init__(self):
        pass

    def render(self, scene):
        width = WIDTH
        height = HEIGHT
        aspect_ratio = width/height
        x0 = -1.0
        x1 = 1.0
        xstep = (x1 - x0) / (width -1)
        y0 = -1.0 / aspect_ratio
        y1 = 1.0 / aspect_ratio
        ystep = (y1 - y0) / (height - 1)

        camera = CAMERA
        pixels = []

        for j in range(height):
            y = y0 + j*ystep
            for i in range(width):
                x = x0 + i*xstep
                ray = Ray(camera.origin, Point(x, y, 0) - camera.origin + camera.direction)
                #pixels.append(self.ray_trace(ray, scene))
                draw_pixel((i,HEIGHT-j),self.ray_trace(ray, scene))

        #to_ppm(pixels)

    def ray_trace(self, ray, scene):
        color = (0,0,0)
        dist_hit, obj_hit = self.find_nearest(ray, scene)
        if obj_hit is None:
            return (0,0,0)
        else:
            return obj_hit.color

    def find_nearest(self, ray, scene):
        dist_min = None
        obj_hit = None
        for obj in scene:
            dist = obj.intersects(ray)
            if dist is not None and (obj_hit is None or dist < dist_min):
                dist_min = dist
                obj_hit = obj
        return (dist_min, obj_hit)

Engine = RenderEngine()
sphere = Sphere(Point(0,0,1),0.5)
ray = Ray(Vector3(0,0,-1), sphere.center)
print("Dist: "+str(sphere.intersects(ray)))
Scene = [sphere]
CAMERA = Camera(Vector3(0,0,-1), Vector3(0,0,0))

DIRX = 0
DIRZ = 0
mag = 0

running = False
while running:
    mag = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    

    

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        DIRX += .1
        DIRZ -= .1
    if keys[pygame.K_d]:
        DIRX -= .1
        DIRZ += .1
    if keys[pygame.K_w]:
        CAMERA.direction.y += .1
        CAMERA.origin.y += .1
        

    #CAMERA.direction.x = (DIRX)
    #CAMERA.direction.z = (DIRZ)

    pygame.display.update()

pygame.quit()



































    





    
