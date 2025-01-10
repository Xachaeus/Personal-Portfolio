from Sphere import *
from Vector3 import *
from Light import *

class Scene:
    """Base object for storing scene data such as width, height, and objects."""
    def __init__(self, dimensions, spheres, lights, camera=Vector3(0,0,-1)):

        self.width, self.height = dimensions
        self.objects = spheres
        self.lights = lights
        self.camera = camera
