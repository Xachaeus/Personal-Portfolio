from Vector3 import *
from Ray import *

class Sphere:
    def __init__(self, position, radius, material):
        self.center = position
        self.radius = radius
        self.material = material

    def intersects(self, ray):
        sphere_to_ray = ray.origin - self.center
        #a = 1
        b = 2 * ray.dir.dot_product(sphere_to_ray)
        c = sphere_to_ray.dot_product(sphere_to_ray) - self.radius**2
        discriminant = b*b - 4*c

        if discriminant >= 0:
            dist = (-b - (discriminant**(1/2))) / 2
            if dist > 0: return dist
            else: return None
        return None

    def normal(self, point):

        return (point - self.center).normalize()
