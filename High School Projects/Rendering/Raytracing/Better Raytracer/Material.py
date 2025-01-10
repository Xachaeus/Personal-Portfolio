from Vector3 import * 

class Material:

    def __init__(self, color, diffuse=1.0, specular=1.0, reflective=0.5,
                 ambient=0.05):

        self.color = color
        self.diffuse = diffuse
        self.reflective = reflective
        self.specular = specular
        self.ambient = ambient
