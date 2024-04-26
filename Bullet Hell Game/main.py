import pygame
from pygame import Rect
from Player import *
from Projectile import Projectile
from Enemy import *
from SETTINGS import *

PI = 3.1415926535897934

pygame.init()
WIDTH = SCREEN_WIDTH
HEIGHT = SCREEN_HEIGHT
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Bullet Hell')

clock = pygame.time.Clock()
deltaTime = 0;

player = Player(WIDTH, HEIGHT, P_SPEED)
enemy = Enemy(WIDTH, HEIGHT, (WIDTH//2, HEIGHT//5), 40, player)

def draw_hp(enem):
  pygame.draw.rect(window, (100,0,0), Rect(20,20,(WIDTH-40), 20))
  w = enem.health/E_HEALTH*(WIDTH-40)
  pygame.draw.rect(window, (200,180,0), Rect(20,20,w,20))

def draw_special():
  alpha = 200 if special_timer == 0 else 100
  s = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
  pygame.draw.rect(s, (100,0,0,alpha), Rect(10, HEIGHT-20, 80,10))
  pygame.draw.rect(s, (200,190,0,alpha), Rect(10, HEIGHT-20, 80*(20-special_timer)/20, 10))
  window.blit(s, (0,0))

special_timer = 20
player_dist = None
prox_multiplier = None
furthest_dist = 500
closest_dist = 200
max_mult = 3

slope = max_mult/(closest_dist-furthest_dist)
intercept = max_mult-(closest_dist*slope)

running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  ##Update sequence

  player_dist = ((player.x-enemy.x)**2 + (player.y-enemy.y)**2)**(1/2)
  prox_multiplier = slope*player_dist + intercept
  if special_timer>0: special_timer -= deltaTime*prox_multiplier
  if special_timer<0:special_timer = 0
  
  keys = pygame.key.get_pressed()

  player.update_movement(keys, deltaTime)
  player.update_timer(deltaTime)
  
  if keys[pygame.K_f] and special_timer <= 0 and player.health > 0:
    special_timer = 20
    for i in range(50):
      ang = ((i/50)*.8) - .4
      Projectile(player, [enemy], -((PI/2)+ang), P_PROJ_SPEED*1.25, size=10, color = (0,0,255), border=0, path=player_spread, damage=2.25)
      
  if keys[pygame.K_SPACE] and player.shoot_timer <= 0 and player.health > 0:
    player.shoot_timer = .2
    for i in [-.4,-.2,0,.2,.4]:
      Projectile(player, [enemy], -((PI/2)+i), P_PROJ_SPEED, border=0, path=player_spread)

  enemy.update_timers(deltaTime)
  enemy.update_pattern()
  enemy.update_movement(deltaTime)
  enemy.update_projectiles(deltaTime)

  player.update_projectiles(deltaTime)

  if player.health <= 0:
    #running = False
    print("You were killed by Evil Purple Circle.")

  ##Render sequence

  window.fill((0,0,0))

  for proj in enemy.projectiles: proj.draw(window)
  for proj in player.projectiles: proj.draw(window)
  enemy.draw(window)
  player.draw(window)

  draw_hp(enemy)
  draw_special()

  pygame.display.flip()
  deltaTime = clock.tick(60)/1000
  
pygame.quit()
