import pygame

def clamp(val, min, max, loop=True):
    if val<min:
        if loop: val = val+max
        else: val = min
    if val>max:
        if loop: val = val-max
        else: val = max
    return val

def to_image(iterable, shape, filename):
    file = open(filename, "w")
    file.write(f"P3 {shape[0]} {shape[1]}\n")
    file.write("255\n")
    x = 0
    y = 0
    for item in iterable:
        file.write(f"{int(item[0])} {int(item[1])} {int(item[2])}    ")
        x += 1
        if x == shape[0]:
            x = 0
            y +=1
            file.write("\n")
    file.close()

def to_pygame_display(iterable, shape, display):
    total = 0
    for y in range(shape[1]):
        for x in range(shape[0]):
            try:
                color = iterable[total]
                x = color.x
                y = color.y
                z = color.z
                color = (x,y,z)
                pygame.draw.polygon(display, color, [(x,y),
                                                               (x,y),
                                                               (x,y)])
                total += 1
            except:
                print(color)

class Image:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = [[Color.from_hex("#000000") for _ in range(width)] for _ in range(height)]

    def set_pixel(self, x, y, col):
        self.pixels[y][x] = col

    def write_ppm(self, img_file):
        def to_byte(c):
            return round(max(min(c * 255, 255), 0))

        img_file.write("P3 {} {}\n255\n".format(self.width, self.height))
        for row in self.pixels:
            for color in row:
                img_file.write(
                    "{} {} {} ".format(
                        to_byte(color.x), to_byte(color.y), to_byte(color.z)
                    )
                )
            img_file.write("\n")


        

class Vector:
    """A three element vector used in 3D graphics for multiple purposes"""

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "({}, {}, {})".format(self.x, self.y, self.z)

    def dot_product(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def magnitude(self):
        return (self.dot_product(self)) ** (1/2)

    def normalize(self):
        return self / self.magnitude()

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        assert not isinstance(other, Vector)
        return Vector(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        assert not isinstance(other, Vector)
        return Vector(self.x / other, self.y / other, self.z / other)

    def __iter__(self):
        return (self.x, self.y, self.z)

class Color(Vector):
    """Stores color as RGB triplets. An alias for Vector"""

    @classmethod
    def from_hex(cls, hexcolor="#000000"):
        x = int(hexcolor[1:3], 16) / 255.0
        y = int(hexcolor[3:5], 16) / 255.0
        z = int(hexcolor[5:7], 16) / 255.0
        return cls(x, y, z)

class Sphere:
    """Sphere is the only 3D shape implemented. Has center, radius and material"""

    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def intersects(self, ray):
        """Checks if ray intersects this sphere. Returns distance to intersection or None if there is no intersection"""
        sphere_to_ray = ray.origin - self.center
        # a = 1
        b = 2 * ray.direction.dot_product(sphere_to_ray)
        c = sphere_to_ray.dot_product(sphere_to_ray) - self.radius * self.radius
        discriminant = b * b - 4 * c

        if discriminant >= 0:
            dist = (-b - (discriminant)**(1/2)) / 2
            if dist > 0:
                return dist
        return None

    def normal(self, surface_point):
        """Returns surface normal to the point on sphere's surface"""
        return (surface_point - self.center).normalize()

class Light:
    """Light represents a point light source of a certain color"""

    def __init__(self, position, color=Color.from_hex("#FFFFFF")):
        self.position = position
        self.color = color

class Material:
    """Material has color and properties which tells us how it reacts to light"""

    def __init__(
        self, color=Color.from_hex("#FFFFFF"), ambient=0.05, diffuse=1.0,
        specular=1.0, reflection=0.5):
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection=reflection

    def color_at(self, position):
        return self.color

class CheckeredMaterial:
    """Material has color and properties which tells us how it reacts to light"""

    def __init__(
        self, color1=Color.from_hex("#FFFFFF"), color2=Color.from_hex("#000000"),
        ambient=0.05, diffuse=1.0, specular=1.0, reflection=0.5):
        self.color1 = color1
        self.color2 = color2
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection

    def color_at(self, position):
        if int((position.x + 5.0) * 3.0) % 2 == int(position.z * 3.0) % 2:
            return self.color2
        else:
            return self.color1 
    

        
class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.normalize()

class Point(Vector):
    pass


class Scene:
    def __init__(self, camera, objects, lights, width, height):
        self.camera = camera
        self.objects = objects
        self.width = width
        self.height = height
        self.lights = lights
    

def Draw_Pixel(display,pixel,color):
    pygame.draw.polygon(display, color, [pixel,pixel,pixel])


class RenderEngine:
    """Renders 3D objects into 2D objects using ray tracing"""

    MAX_DEPTH = 5
    MIN_DISPLACE = 0.0001

    def render(self, scene):
        width = scene.width
        height = scene.height
        aspect_ratio = float(width) / height
        x0 = -1.0
        x1 = +1.0
        xstep = (x1 - x0) / (width - 1)
        y0 = -1.0 / aspect_ratio
        y1 = +1.0 / aspect_ratio
        ystep = (y1 - y0) / (height - 1)

        camera = scene.camera
        pixels = Image(width, height)

        for j in range(height):
            y = y0 + j * ystep
            for i in range(width):
                x = x0 + i * xstep
                ray = Ray(camera, Point(x, y) - camera)
                pixels.set_pixel(i, j, self.ray_trace(ray, scene))
            #print("{:3.0f}%".format(float(j) / float(height) * 100), end="\r")
        
        return pixels

    def ray_trace(self, ray, scene, depth=0):
        color = Color(0, 0, 0)
        # Find the nearest object hit by the ray in the scene
        dist_hit, obj_hit = self.find_nearest(ray, scene)
        if obj_hit is None:
            return color
        hit_pos = ray.origin + ray.direction * dist_hit
        hit_normal = obj_hit.normal(hit_pos)
        color += self.color_at(obj_hit, hit_pos, hit_normal, scene)
        if depth < self.MAX_DEPTH:
            new_ray_pos = hit_pos + hit_normal * self.MIN_DISPLACE
            new_ray_dir = (
                ray.direction - 2 * ray.direction.dot_product(hit_normal) * hit_normal
            )
            new_ray = Ray(new_ray_pos, new_ray_dir)
            # Attenuate the reflected ray by the reflection coefficient
            color += (
                self.ray_trace(new_ray, scene, depth + 1) * obj_hit.material.reflection
            )
        return color

    def find_nearest(self, ray, scene):
        dist_min = None
        obj_hit = None
        for obj in scene.objects:
            dist = obj.intersects(ray)
            if dist is not None and (obj_hit is None or dist < dist_min):
                dist_min = dist
                obj_hit = obj
        return (dist_min, obj_hit)

    def color_at(self, obj_hit, hit_pos, normal, scene):
        material = obj_hit.material
        obj_color = material.color_at(hit_pos)
        to_cam = scene.camera - hit_pos
        specular_k = 50
        color = material.ambient * Color.from_hex("#000000")
        # Light calculations
        for light in scene.lights:
            to_light = Ray(hit_pos, light.position - hit_pos)
            # Diffuse shading (Lambert)
            color += (
                obj_color
                * material.diffuse
                * max(normal.dot_product(to_light.direction), 0)
            )
            # Specular shading (Blinn-Phong)
            half_vector = (to_light.direction + to_cam).normalize()
            color += (
                light.color
                * material.specular
                * max(normal.dot_product(half_vector), 0) ** specular_k
            )
        return color
