import pygame
from Projectile import *
from SETTINGS import *
from random import random, randint
from numpy import sin, cos, arctan2

#Enemies can be bosses or small enemies; need to be able to define movement behavior and projectile patterns

def proj_spin(proj, deltaTime):
    spin_time = 2
    proj.x += cos(proj.dir)*proj.speed*deltaTime
    proj.y += sin(proj.dir)*proj.speed*deltaTime
    proj.size+=5*proj.timer*deltaTime
    if(proj.timer<spin_time):
        proj.dir += 1.5*deltaTime/proj.timer#/(deltaTime/3+0.000001)
        proj.color = (int(200+(min(55*proj.timer/spin_time,55))), int(255*(spin_time-proj.timer)/spin_time),0)

def standard_movement(enemy, deltaTime):
    enemy.x = (cos(enemy.move_timer/3)*(enemy.width-enemy.size/2-50)/2) + enemy.width/2

def radial_pattern(origin): #Origin can be player or enemy
    if(origin.shoot_timer<=0):
        flag = [-1,1]; flag=flag[randint(0,1)]
        offset = random()*2*PI/21
        speed = (randint(0,40)+RADIAL_SPEED)
        for i in range(RADIAL_COUNT):
            dir = (i/RADIAL_COUNT) * 2 * PI + offset
            Projectile(origin, origin.targets, dir, RADIAL_SPEED, 15, path=spiral, dir_flag=flag)
        origin.shoot_timer = RADIAL_DELAY

def spin_pattern(origin):
    if(origin.shoot_timer<=0):
        offset = random()*2*PI/30
        for i in range(SPIN_COUNT):
            dir = (i/SPIN_COUNT) * 2 * PI + offset
            Projectile(origin, origin.targets, dir, SPIN_SPEED, 12, path=proj_spin)
        origin.shoot_timer = SPIN_DELAY

def random_pattern(origin):
    if(origin.shoot_timer<=0):
        for i in range(RANDOM_COUNT):
            dir = random()*2*PI
            Projectile(origin, origin.targets, dir, randint(-75,75)+RANDOM_SPEED, size=5, path=straight_growth)
        origin.shoot_timer = RANDOM_DELAY

def rain_pattern(origin):
    if(origin.shoot_timer<=0):
        for i in range(RAIN_COUNT):
            speed = randint(-75,75)+RAIN_SPEED
            p = Projectile(origin,origin.targets, (PI/2), speed, 10)
            p.x = randint(0, origin.width)
            p.y = randint(-PROJ_BORDER, 0)
        origin.shoot_timer = RAIN_DELAY

def tracking_pattern(origin):
    if origin.shoot_timer <= 0:
        to_player =  arctan2((origin.targets[0].y-origin.y), (origin.targets[0].x-origin.x))
        for i in range(TRACKING_COUNT):
            dir = ((i/TRACKING_COUNT)*TRACKING_SPAN) - TRACKING_SPAN*.5 + to_player
            while dir<0: dir+= 2*PI
            dir%=(2*PI)
            Projectile(origin, origin.targets, dir, TRACKING_SPEED, size=8, path=track,dir_flag=to_player)
        origin.shoot_timer = TRACKING_DELAY

class Enemy:

    def __init__(self, width, height, origin, size, target, movement=standard_movement, patterns=[tracking_pattern, radial_pattern, spin_pattern, random_pattern, rain_pattern]):

        self.width = width
        self.height = height
        self.x, self.y = origin
        self.size = size
        self.movement = movement
        self.patterns = patterns
        self.pattern = self.patterns[randint(0,len(self.patterns)-1)]
        self.pattern_weights = [0 for x in self.patterns]
        self.move_timer = 0
        self.pattern_timer = -1
        self.shoot_timer = 0
        self.shoot_timer_2 = 0
        self.projectiles = []
        self.health = E_HEALTH
        self.targets = [target]

    def update_pattern(self):
        if self.pattern_timer<=-2:
            self.pattern_timer = 8
            old = self.pattern
            if len(self.patterns)>1:
                while self.pattern == old: self.pattern = self.patterns[randint(0,len(self.patterns)-1)]
            

    def update_movement(self, deltaTime):

        self.movement(self, deltaTime)
        if self.x+self.size/2>self.width or self.x-self.size/2<0 or self.y+self.size/2>self.height or self.y-self.size/2<0:
            self.movement(self, -deltaTime)

    def update_timers(self, deltaTime):
        self.move_timer += deltaTime
        self.pattern_timer -= deltaTime
        if self.shoot_timer > 0: self.shoot_timer -= deltaTime
        if self.shoot_timer_2 > 0: self.shoot_timer_2 -= deltaTime

    def update_projectiles(self, deltatime):
        if self.health >0 and self.pattern_timer>0: self.pattern(self)
        for proj in self.projectiles: proj.update(deltatime)

    def draw(self, surface):
        color = (255,0,255)
        pygame.draw.circle(surface, color, (self.x,self.y), self.size/2)

    def touching(self, proj):
        dist = ((self.x-proj.x)**2 + (self.y-proj.y)**2)**(1/2)
        return dist <= self.size/2 + proj.size/2
    
    def damage(self, proj):
        proj.parent.projectiles.remove(proj)
        self.health-=proj.damage*P_PROJ_DAMAGE_MULT
