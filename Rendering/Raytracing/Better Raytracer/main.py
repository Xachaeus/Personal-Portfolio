from Engine import *

width, height = 320, 200

blue = Material(Vector3(0,0,255))
red = Material(Vector3(255,255,0))

light = Light(Vector3(-5,4,0), Vector3(255,255,255))
ground = Sphere(Vector3(0,-10000.5,0), 10000, blue)
sphere = Sphere(Vector3(0,0,2), 0.5, red)
scene = Scene((320, 200), [sphere, ground], [light])

engine = RenderEngine()
engine.render(scene)
#engine.render_sphere(sphere)
