from Vector3 import Vector3
from Triangle import Triangle

GREY = (150,150,150)

class Box:
    def __init__(self, position, width=1, height=1, depth=1):
        self.position = position
        self.width = width
        self.depth = depth
        self.height = height
        self.set_surfaces()
        
    def set_surfaces(self):
        
        width, height, depth = self.width, self.height, self.depth
        
        fbl = self.position - Vector3(width/2, height/2, depth/2)
        fbr = fbl + Vector3(width,0,0)
        bbl = fbl + Vector3(0,0,depth)
        bbr = fbl + Vector3(width,0,depth)

        ftl = fbl + Vector3(0, height, 0)
        ftr = fbl + Vector3(width, height, 0)
        btl = fbl + Vector3(0, height, depth)
        btr = fbl + Vector3(width, height, depth)
        
        self.front = [fbl,fbr,ftr,ftl]
        self.back = [btl,btr,bbr,bbl]
        self.top = [ftl,ftr,btr,btl]
        self.bottom = [fbl,fbr,bbr,bbl]
        self.left = [ftl,fbl,bbl,btl]
        self.right = [ftr,fbr,bbr,btr]
        
