import pygame
from pygame import Rect
from numpy import sin, cos
from Projectile import Projectile
from SETTINGS import *


def player_spread(proj, deltaTime):
  if proj.timer<0.22:
    proj.x += cos(proj.dir)*proj.speed*deltaTime
    proj.y += sin(proj.dir)*proj.speed*deltaTime
  else:
    proj.y -= proj.speed*deltaTime


class Player:

  def __init__(self, width, height, speed, targets=[]):
    self.width = width;
    self.height = height;
    self.speed = speed;
    self.x = width//2;
    self.y = height//2;
    self.size = P_SIZE
    self.projectiles = []
    self.health = P_HEALTH
    self.shoot_timer = 0
    self.damage_timer = 0
    self.targets = targets

  def update_timer(self, deltaTime):
    if self.shoot_timer > 0: self.shoot_timer -= deltaTime
    if self.damage_timer > 0: self.damage_timer -= deltaTime

  def update_movement(self, keys, deltaTime):
    if keys[pygame.K_w]: 
      self.y-=self.speed*deltaTime; #Access a specific address in memory, subtract the value at that address by the format-adjusted value at another memory address, and multiply that by yet another thingy
      if self.y+self.size/2 > self.height or self.y-self.size/2 < 0: self.y+=self.speed*deltaTime;
    if keys[pygame.K_s]: 
      self.y+=self.speed*deltaTime;
      if self.y+self.size/2 > self.height or self.y-self.size/2 < 0: self.y-=self.speed*deltaTime;
    if keys[pygame.K_a]: 
      self.x-=self.speed*deltaTime;
      if self.x+self.size/2 > self.width or self.x-self.size/2 < 0: self.x+=self.speed*deltaTime;
    if keys[pygame.K_d]: 
      self.x+=self.speed*deltaTime;
      if self.x+self.size/2 > self.width or self.x-self.size/2 < 0: self.x-=self.speed*deltaTime;

  def update_projectiles(self, deltaTime):
    for proj in self.projectiles: proj.update(deltaTime)

  def draw(self, surface):
    s = pygame.Surface((self.width,self.height), pygame.SRCALPHA)

    player_alpha = 255 if self.damage_timer<=0 else 75
    color = (0,255,0, player_alpha)
    pygame.draw.circle(s,color,(self.x,self.y),self.size/2)
    #rect width: 60
    top = self.y+25 if self.y+35 < self.height else self.y-35
    pygame.draw.rect(s, (100,0,0, 100), Rect(self.x-30,top,60,10))
    width = self.health/P_HEALTH*60
    pygame.draw.rect(s, (0,200,0, 100), Rect(self.x-30,top,width,10))
    surface.blit(s, (0,0))
    

  def touching(self, proj):
    dist = ((self.x-proj.x)**2 + (self.y-proj.y)**2)**(1/2)
    return dist <= self.size/2 + proj.size/2

  def damage(self, proj):
    if self.damage_timer <= 0:
      self.health -= proj.damage*E_PROJ_DAMAGE_MULT
      self.damage_timer = .6
      proj.parent.projectiles.remove(proj)
