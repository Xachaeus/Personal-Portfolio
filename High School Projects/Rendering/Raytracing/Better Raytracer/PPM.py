from Vector3 import *

def to_ppm(iterable, shape, filename):
    file = open(filename, "w")
    file.write(f"P3 {shape[0]} {shape[1]}\n")
    file.write("255\n")
    x = 0
    y = 0
    for item in iterable:
        file.write(f"{int(item.x)} {int(item.y)} {int(item.z)}    ")
        x += 1
        if x == shape[0]:
            x = 0
            y +=1
            file.write("\n")
    file.close()

def open_ppm(filename, scene):
    file = open(filename, 'w')
    file.write(f"P3 {scene.width} {scene.height} \n255\n")
