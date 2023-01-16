from Raytracing import *

WIDTH = 320
HEIGHT = 200
#DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

ASPECT_RATIO = WIDTH/HEIGHT

RED = Color.from_hex("#FFFFFF")
BLUE = Color.from_hex("#00FF00")

mat = Material(RED, 0.05, 0, 1, 1)
mat2 = Material(BLUE, 0.05, .8, 1)
#mat3 = Material(GREEN, 0.05, 2, 0)

Ground = Sphere( Point(0, 100000.5, 1), 100000.0, CheckeredMaterial())

camera = Vector(.2,-0.35,-1)
objects = [Sphere(Point(1,0,1), 0.5, mat),
           Sphere(Point(-1,-0.5,0.5), 0.5, mat2),
           Ground]
lights = [Light(Point(3, -0.5, -3.0)),
          Light(Point(2, -3, -1))]
scene = Scene(camera, objects, lights, WIDTH, HEIGHT)
engine = RenderEngine()
image = engine.render(scene)

image.write_ppm(open("picture3.ppm", "w"))
