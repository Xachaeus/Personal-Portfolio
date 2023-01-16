from Vector3 import Vector3
from Triangle import Triangle
from Box import Box
from math import sin, cos
from Draw import draw_wireframe_triangle
import pygame

class Camera:

    def __init__(self, position, yaw, pitch, roll, Vw,Vh,d,Cw,Ch):
        self.position = position
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll
        self.Vw = Vw
        self.Vh = Vh
        self.d = d
        self.Cw = Cw
        self.Ch = Ch
        
    def render_triangle(self, DISPLAY, color, tri):
        Tri = tri.copy()
        WIDTH, HEIGHT, Vw, Vh, d = self.Cw, self.Ch, self.Vw, self.Vh, self.d
        def ViewportToCanvas(x, y):
            return Vector3((x * WIDTH/Vw)+WIDTH//2, -(y * HEIGHT/Vh)+HEIGHT//2, d)
        def ProjectVertex(v):
            Vx, Vy, Vz = v.x, v.y, v.z
            return ViewportToCanvas(Vx*d/Vz, Vy*d/Vz)
        def draw_triangle(triangle):
            p1 = triangle.p1.x, triangle.p1.y
            p2 = triangle.p2.x, triangle.p2.y
            p3 = triangle.p3.x, triangle.p3.y
            draw_wireframe_triangle(DISPLAY, p0, p1, p2)
        def sub_render_triangle(triangle):
            points = [triangle.p1, triangle.p2, triangle.p3]
            new_points = []
            for point in points:
                new_point = ProjectVertex(point)
                new_points.append(new_point)
            new_triangle = Triangle(new_points[0],new_points[1],new_points[2])
            draw_triangle(new_triangle)
        def rotate(point, origin, angle):
            nx = origin.x+cos(angle)*(point.x-origin.x)-sin(angle)*(point.z-origin.z)
            nz = origin.z+sin(angle)*(point.x-origin.x)+cos(angle)*(point.z-origin.z)
            return Vector3(nx,point.y,nz)
        
        #Translate to world space
        Tri.p1 = Tri.p1 + tri.position
        Tri.p2 = Tri.p2 + tri.position
        Tri.p3 = Tri.p3 + tri.position
        
        Tri.p1 = rotate(Tri.p1, self.position, self.yaw)
        Tri.p2 = rotate(Tri.p2, self.position, self.yaw)
        Tri.p3 = rotate(Tri.p3, self.position, self.yaw)
    
        
        
        #Translate to camera space
        Tri.p1 = Tri.p1-self.position
        Tri.p2 = Tri.p2-self.position
        Tri.p3 = Tri.p3-self.position
        
        sub_render_triangle(Tri)

    def render_boxes(self,display,color,boxes):
        for box in boxes:
            self.render_box(display,color,box)

    def render_box(self, display, color, box):
        WIDTH, HEIGHT, Vw, Vh, d = self.Cw, self.Ch, self.Vw, self.Vh, self.d
        def ViewportToCanvas(x, y):
            result = Vector3((x * WIDTH/Vw)+WIDTH//2, -(y * HEIGHT/Vh)+HEIGHT//2, d)
            result = result            
            return result
        def ProjectVertex(v):
            Vx, Vy, Vz = v.x, v.y, v.z
            return ViewportToCanvas(Vx*d/Vz, Vy*d/Vz)
        def rotate_y(point, origin, angle):
            nx = origin.x+cos(angle)*(point.x-origin.x)-sin(angle)*(point.z-origin.z)
            nz = origin.z+sin(angle)*(point.x-origin.x)+cos(angle)*(point.z-origin.z)
            return Vector3(nx,point.y,nz)
        def rotate_p(point,origin,angle):
            nz = origin.z+cos(angle)*(point.z-origin.z)-sin(angle)*(point.y-origin.y)
            ny = origin.y+sin(angle)*(point.z-origin.z)+cos(angle)*(point.y-origin.y)
            return Vector3(point.x,ny,nz)
        def rotate_r(point, origin, angle):
            nx = origin.x+cos(angle)*(point.x-origin.x)-sin(angle)*(point.y-origin.y)
            ny = origin.y+sin(angle)*(point.x-origin.x)+cos(angle)*(point.y-origin.y)
            return Vector3(nx,ny,point.z)
        def translate(point):
            p = point + box.position
            p = rotate_y(p, self.position, self.yaw)
            p = rotate_p(p, self.position, self.pitch)
            p = rotate_r(p, self.position, self.roll)
            p = p - self.position
            if p.z >= 1:
                p = ProjectVertex(p)
                return p
            elif p.z < 1 and p.z >= 0:
                p.z = 1
                p = ProjectVertex(p)
                return p
            else:
                p.z = 1
                p = ProjectVertex(p)
                return p
        
        fpoints = []
        bpoints = []
        tpoints = []
        dpoints = []
        lpoints = []
        rpoints = []
        
        for point in box.front:
            point = translate(point)
            if point: fpoints.append((point.x,point.y))
        for point in box.back:
            point = translate(point)
            if point: bpoints.append((point.x,point.y))
        for point in box.top:
            point = translate(point)
            if point: tpoints.append((point.x,point.y))
        for point in box.bottom:
            point = translate(point)
            if point: dpoints.append((point.x,point.y))
        for point in box.left:
            point = translate(point)
            if point: lpoints.append((point.x,point.y))
        for point in box.right:
            point = translate(point)
            if point: rpoints.append((point.x,point.y))

        if len(fpoints) >= 3: pygame.draw.polygon(display,color,fpoints)
        if len(bpoints) >= 3: pygame.draw.polygon(display,color,bpoints)
        if len(tpoints) >= 3: pygame.draw.polygon(display,color,tpoints)
        if len(dpoints) >= 3: pygame.draw.polygon(display,color,dpoints)
        if len(lpoints) >= 3: pygame.draw.polygon(display,color,lpoints)
        if len(rpoints) >= 3: pygame.draw.polygon(display,color,rpoints)

    def render_scene(self, display, scene):

        order = []
        dist_order = []
        for obj in scene:
            p1 = obj.p1+obj.position
            p2 = obj.p2+obj.position
            p3 = obj.p3+obj.position
            
            dist1 = (self.position - p1)
            dist1 = dist1.magnitude()
            dist2 = (self.position - p2)
            dist2 = dist2.magnitude()
            dist3 = (self.position - p3)
            dist3 = dist3.magnitude()
            dist =(dist1+dist2+dist3)/3
            dist_order.append(dist)
            dist_order.sort(reverse=True, key=float)
            index = dist_order.index(dist)
            order.insert(index, obj)
        
        for obj in order:
            self.render_triangle(display, obj.color, obj)

        

        
        





        
