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

    def normalize(self):
        return self.normal

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

    def __rmul__(self, other):
        return self.__mul__(other)
