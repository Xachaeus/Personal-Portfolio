from Vector3 import Vector3
class Triangle:
    def __init__(self, p1, p2, p3, position=Vector3(), color=(255,255,255)):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.position = position
        self.color = color
    def __str__(self):
        return(f"{self.p1}, {self.p2}, {self.p3})")
    def copy(self):
        return Triangle(self.p1,self.p2,self.p3, self.position, self.color)
