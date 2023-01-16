from math import sin, cos, atan, tan
import pygame
import Settings

RESOLUTION = Settings.resolution
FOV = Settings.fov

PI = 3.14159265359
P2 = PI/2
P3 = 3*PI/2
DR = 0.0174533

WIDTH = 1024
HEIGHT = 512
DISPLAY = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Raycaster")

GREY = (100,100,100)
WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)

COLORS = [BLACK,RED,BLUE,GREEN,WHITE]

px, py = HEIGHT/2, HEIGHT/2
pdx, pdy, pa = 0,0,0.0001
playerSize = 6

opx,opy = px,py

def equalsXorY(param, x, y):
    if param == x or param == y:
        return(True)
    else:
        return(False)

def drawSquare(x, y, width, color=WHITE):
    pygame.draw.polygon(DISPLAY, color, [(x,y),
                                         (x+width,y),
                                         (x+width,y+width),
                                         (x,y+width)])

def drawPlayer():
    topLeft = (px - playerSize//2, py - playerSize//2)
    x, y = topLeft
    drawSquare(x,y,playerSize,YELLOW)
    pygame.draw.line(DISPLAY,YELLOW, (px,py), (px+pdx*5, py+pdy*5))


mapX = 8
mapY = 8
mapS = 64

map = [1,1,1,1,1,1,1,1,
       1,0,1,0,0,0,0,1,
       1,0,1,0,1,0,0,1,
       1,0,1,0,0,0,0,1,
       1,0,0,0,0,0,0,1,
       1,0,0,0,0,1,0,1,
       1,0,0,0,0,0,0,1,
       1,1,1,1,1,1,1,1]

def drawMap2D():
    y = 0
    x = 0
    for y in range(mapY):
        for x in range(mapX):
            dX, dY = x*mapS, y*mapS
            dX2,dY2 = x*mapS+mapS, y*mapS+mapS
            mp = y*mapX+x
            if(map[mp]>0):
                color = COLORS[map[mp]]
                pygame.draw.polygon(DISPLAY, WHITE, [(dX + 1,dY + 1),
                                                     (dX2 - 1,dY + 1),
                                                     (dX2 - 1,dY2 - 1),
                                                     (dX + 1,dY2 - 1)])
            else:
                pygame.draw.polygon(DISPLAY, BLACK, [(dX + 1,dY + 1),
                                                     (dX2 - 1,dY + 1),
                                                     (dX2 - 1,dY2 - 1),
                                                     (dX + 1,dY2 - 1)])

def dist(ax, ay, bx, by, ang):
    ans = ((bx-ax)*(bx-ax) + (by-ay)*(by-ay))**(1/2)
    return(ans)

def drawRays3D(): #Requires variables FOV, RESOLUTION, px, py, pa, mapX, mapY, mapS
#Requires functions sin, cos, tan, atan, complete pygame library
    FoV = FOV
    if RESOLUTION == "Low": Resolution = 1
    if RESOLUTION == "Normal": Resolution = 2
    if RESOLUTION == "High": Resolution = 4
    if RESOLUTION == "Very high": Resolution = 8

    Resolution = 2

    displayWidth = 8*60
    lineOffset = 8//Resolution
    
    r,mx,my,mp,dof = 0,0,0,0,0
    rx,ry,ra,xo,yo, disT = 0.0,0.0,0.0,0.0,0.0, 0.0

    ra = pa-DR*(FoV/2)
    if(ra<0):
        ra = ra + 2*PI
    if (ra>2*PI):
        ra = ra - 2*PI
    

    for r in range(FoV*Resolution):#Change number of rays here
        #Check horizontal lines
        dof = 0
        disH = 1000000
        hx = px
        hy = py
        aTan = -1/tan(ra)
        if(ra>PI):#Looking down
            ry = (((int)(py)>>6)<<6)-0.0001
            rx = (py-ry)*aTan+px
            yo = -64
            xo = -yo*aTan
        if(ra<PI):#Looking up
            ry = (((int)(py)>>6)<<6)+64
            rx = (py-ry)*aTan+px
            yo = 64
            xo = -yo*aTan
        if(ra==0 or ra==PI):
            rx=px
            ry=py
            dof=mapX
        limit = [mapX,mapY]
        limit.sort()
        limit = limit[1]
        while(dof<limit):
            mx = (int)(rx)//mapS
            my = (int)(ry)//mapS
            mp=my*mapX+mx
            if(mp > 0 and mp<mapX*mapY and map[mp]>0):
                hx=rx
                hy=ry
                disH = dist(px,py,hx,hy,ra)
                dof = limit
            else:
                rx = rx + xo
                ry = ry + yo
                dof = dof + 1

        #Check vertical lines
        dof = 0
        disV = 1000000
        vx = px
        vy = py
        nTan = -tan(ra)
        if(ra>P2 and ra<P3):#Looking right
            rx = (((int)(px)>>6)<<6)-0.0001
            ry = (px-rx)*nTan+py
            xo = -64
            yo = -xo*nTan
        if(ra<P2 or ra>P3):#Looking left
            rx = (((int)(px)>>6)<<6)+64
            ry = (px-rx)*nTan+py
            xo = 64
            yo = -xo*nTan
        if(ra==0 or ra==PI):
            rx=px
            ry=py
            dof=mapY
        while(dof<limit):
            mx = (int)(rx)//mapS
            my = (int)(ry)//mapS
            mp=my*mapX+mx
            if(mp > 0 and mp<mapX*mapY and map[mp]>0):
                vx=rx
                vy=ry
                disV = dist(px,py,vx,vy,ra)
                dof = limit
            else:
                rx = rx + xo
                ry = ry + yo
                dof = dof + 1

        if(disV<disH):
            rx = vx
            ry = vy
            disT = disV
            color = (255,0,0)
        if(disH<disV):
            rx = hx
            ry = hy
            disT = disH
            color = (155,0,0)
            
        pygame.draw.line(DISPLAY, color, (px,py), (rx,ry))

        ra = ra+DR/Resolution
        if(ra<0):
            ra = ra + 2*PI
        if (ra>2*PI):
            ra = ra - 2*PI

        #Draw 3d walls
        
        ca=pa-ra
        if(ca<0):
            ca = ca + 2*PI
        if (ca>2*PI):
            ca = ca - 2*PI
        disT = disT*cos(ca)
        lineH = (mapS*320)/disT
        lineO = HEIGHT/2-lineH/2
        lineO2 = HEIGHT/2+lineH/2
        if(lineH>320):
            lineH = 320
        
        pygame.draw.line(DISPLAY,color, (r*lineOffset+530,lineO),
                         (r*lineOffset+530,lineO2), lineOffset)

Clock = pygame.time.Clock()




running = True

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    DISPLAY.fill(GREY)

    pdx = cos(pa)*5
    pdy = sin(pa)*5
    
    opx,opy = px,py

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        if equalsXorY(map[int((py + pdy)//mapS*mapX+(px//mapS))],0,5):
            py = py + pdy
        if equalsXorY(map[int((py//mapS)*mapX+(px + pdx)//mapS)],0,5):
            px = px + pdx
    if keys[pygame.K_s]:
        if equalsXorY(map[int((py - pdy)//mapS*mapX+(px//mapS))],0,5):
            py = py - pdy
        if equalsXorY(map[int((py//mapS)*mapX+(px - pdx)//mapS)],0,5):
            px = px - pdx
    if keys[pygame.K_a]:
        pa = pa - 0.1
        if(pa<0):
            pa = pa + 2*PI
        pdx = cos(pa)*5
        pdy = sin(pa)*5
        
    if keys[pygame.K_d]:
        pa = pa + 0.1
        if(pa>2*PI):
            pa = pa - 2*PI
        pdx = cos(pa)*5
        pdy = sin(pa)*5

    mapCoordX = px//mapS
    mapCoordY = py//mapS
    if map[int(mapCoordY*mapX+mapCoordX)] > 0:
        px,py = opx,opy

    drawMap2D()

    drawRays3D()

    drawPlayer()

    pygame.display.update()

    Clock.tick(60)

pygame.quit()
