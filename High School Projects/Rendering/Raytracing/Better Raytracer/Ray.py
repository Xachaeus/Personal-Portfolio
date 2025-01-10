from Vector3 import *

class Ray:

    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.normal
        self.dir = self.direction
