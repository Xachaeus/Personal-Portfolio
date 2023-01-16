from Vector3 import *
from Ray import *
from Sphere import *
from Scene import *
from Light import *
from PPM import to_ppm
from Material import *

class RenderEngine:

    def __init__(self):
        pass

    def render_sphere(self, sphere):

        width = 320
        height = 200

        position = Vector3(0,0,-1)

        aspect_ratio = float(width) / height

        x0 = -1.0
        x1 = 1.0
        x_step = (x1-x0) / (width-1)
        y0 = -1.0/aspect_ratio
        y1 = 1.0/aspect_ratio
        y_step = (y1-y0) / (height-1)

        picture = []

        for j in range(height):
          y = y0 + j * y_step
          for i in range(width):
            x = x0 + i * x_step
            ray = Ray(position, Vector3(x,y,0)-position)
            dist = sphere.intersects(ray)
            if dist is not None:
                picture.append(Vector3(0,255,0))
            else:
                picture.append(Vector3(0,0,0))

        print(len(picture) / 320)
    
        to_ppm(picture, (320, 200), "Test.ppm")

    def render(self, scene):

        width = scene.width
        height = scene.height

        position = Vector3(0,0,-1)
        
        aspect_ratio = float(width) / height

        x0 = -1.0
        x1 = 1.0
        xstep = (x1-x0) / (width-1)
        y0 = -1.0/aspect_ratio
        y1 = 1.0/aspect_ratio
        ystep = (y1-y0) / (height-1)

        picture = []

        for sphere in scene.objects:
            sphere.center.y = -sphere.center.y
        for light in scene.lights:
            light.position.y = -light.position.y

        for j in range(height):
            y = y0 + j * ystep
            for i in range(width):
                x = x0 + i * xstep

                ray = Ray(position, Vector3(x,y,0)-position)
                color = self.ray_trace(ray, scene)
                picture.append(color)

        to_ppm(picture, (width, height), "Test.ppm")

    def ray_trace(self, ray, scene):

        dist, sphere = self.find_nearest(ray, scene)
        color = self.color_at(ray, dist, sphere, scene)
        return color

    def find_nearest(self, ray, scene):

        min_dist = None
        obj_hit = None
        dist = None
        for sphere in scene.objects:
            dist = sphere.intersects(ray)
            if dist is not None and (obj_hit is None or dist <= min_dist):
                min_dist = dist
                obj_hit = sphere
        return min_dist, obj_hit

    def color_at(self, ray, dist, sphere, scene):

        if dist is not None:
            hit_pos = dist * ray.direction

            material = sphere.material
            obj_color = material.color
            to_cam = scene.camera - hit_pos
            specular_k = 50
            ambient = material.ambient
            color = ambient * Vector3(1,1,1)
            normal = sphere.normal(hit_pos)
            for light in scene.lights:
                to_light = Ray(hit_pos, light.position - hit_pos)
                color += (
                    obj_color
                    * material.diffuse
                    * max(normal.dot_product(to_light.direction), 0)
                    )
            return color
        else:
            return Vector3(0,0,0)
        
            
                

        
