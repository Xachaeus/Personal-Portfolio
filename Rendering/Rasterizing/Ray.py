from Vector3 import Vector3

class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.normalize()
