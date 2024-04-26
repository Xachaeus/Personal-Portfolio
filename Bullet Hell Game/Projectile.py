import numpy, pygame
from numpy import sin, cos, arctan2
from SETTINGS import *

def straight(proj, deltaTime):
  proj.x += cos(proj.dir)*proj.speed*deltaTime
  proj.y += sin(proj.dir)*proj.speed*deltaTime

def straight_growth(proj, deltaTime):
  proj.x += cos(proj.dir)*proj.speed*deltaTime
  proj.y += sin(proj.dir)*proj.speed*deltaTime
  dist = proj.timer*proj.speed
  if proj.size < 75: proj.size += dist*proj.timer*deltaTime/(40)

def accelerate(proj, deltaTime):
  proj.x += cos(proj.dir)*proj.speed*deltaTime
  proj.y += sin(proj.dir)*proj.speed*deltaTime
  proj.speed += 20*deltaTime

def spiral(proj, deltaTime):
  dist = proj.timer*proj.speed
  dir = proj.dir - proj.dir_flag*proj.timer*2*PI/(16)
  proj.x = cos(dir)*dist + proj.origin[0]
  proj.y = sin(dir)*dist + proj.origin[1]
  proj.size += 6*proj.timer*deltaTime

def track(proj, deltaTime):
  proj.x += cos(proj.dir)*proj.speed*deltaTime
  proj.y += sin(proj.dir)*proj.speed*deltaTime
  if proj.timer < .75:
    target_x = proj.targets[0].x-proj.x
    target_y = proj.targets[0].y-proj.y
    to_target = proj.dir_flag#arctan2(target_y, target_x)%(2*PI)
    ang_diff = (to_target-proj.dir)%(2*PI)
    turn_speed = 2.5
    if ang_diff < PI: proj.dir += turn_speed*deltaTime
    else: proj.dir -= turn_speed*deltaTime
  

class Projectile:
  
  def __init__(self, parent, targets, dir, speed, size=5, border=E_PROJ_BORDER, path=straight, color=(255,0,0), origin=None, damage=1, dir_flag=1):
    self.parent = parent
    if origin is not None: self.origin = origin
    else: self.origin = (self.parent.x, self.parent.y)
    self.x, self.y = self.origin
    self.parent.projectiles.append(self)
    self.targets = targets
    self.dir = dir
    self.speed = speed
    self.size = size
    self.path = path
    self.color = color
    self.border = border
    self.timer = 0.00000001
    self.damage = damage
    self.dir_flag = dir_flag
    

  def update(self, deltaTime):
    self.timer += deltaTime
    self.path(self,deltaTime)
    if(self.x+self.size/2>self.parent.width+PROJ_BORDER or self.x-self.size/2<-PROJ_BORDER) or (self.y+self.size/2>self.parent.height+PROJ_BORDER or self.y-self.size/2<-PROJ_BORDER):
      self.parent.projectiles.remove(self)
      return
    for target in self.targets:
      if target.touching(self):
        target.damage(self)
        
  def draw(self, surface):
    pygame.draw.circle(surface, (255,255,255), (self.x, self.y), self.size/2+self.border)
    pygame.draw.circle(surface, self.color, (self.x, self.y), self.size/2)
