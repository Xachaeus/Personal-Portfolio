from math import sin, cos, atan, tan
import pygame
import Settings
from PIL import Image

RESOLUTION = Settings.resolution
FOV = Settings.fov
p_speed = Settings.speed
p_sensitivity = Settings.sensitivity

#IMPORTANT SETTING HERE
show_textures = True

if not show_textures:
    p_sensitivity = p_sensitivity/1.5
    p_speed = p_speed/1.5

PI = 3.14159265359
P2 = PI/2
P3 = 3*PI/2
DR = 0.0174533

WIDTH = 512
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

COLORS = [BLACK,RED,BLUE,GREEN,WHITE,GREY]

px, py = 96,96
pdx, pdy, pa = 0,0,P2+0.0001
playerSize = 6

opx,opy = px,py

wood_wall = []
stone_wall = []


def loadTextures():

    wood_wall_image = Image.open("wood_wall.png")
    stone_wall_image = Image.open("stone_wall.png")

    i = 0

    for pixel in wood_wall_image.getdata():

        r,g,b,a = pixel
        new_pixel = (r,g,b)
        
        wood_wall.append(new_pixel)

    for pixel in stone_wall_image.getdata():

        r,g,b,a = pixel
        new_pixel = (r,g,b)
        
        stone_wall.append(new_pixel)

def clamp(val,min,max,range):

    while val < min:
        val = val + range
    while val > max:
        val = val - range
    return(val)

def drawSquare(x, y, width, color=WHITE):
    pygame.draw.polygon(DISPLAY, color, [(x,y),
                                         (x+width,y),
                                         (x+width,y+width),
                                         (x,y+width)])


mapX = 16
mapY = 16
mapS = 64

map = [1,3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
       1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,1,
       1,0,0,0,0,0,1,1,0,1,1,1,1,1,1,1,
       1,0,1,0,1,1,0,1,1,1,0,1,1,1,1,1,
       1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,
       1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
       1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
       1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,
       1,0,0,0,0,0,0,5,2,1,0,0,0,0,0,1,
       1,0,1,1,1,1,1,1,1,1,0,1,1,1,0,1,
       1,0,0,0,0,0,0,0,0,1,0,1,1,1,0,1,
       1,0,1,1,1,1,1,1,0,1,0,1,1,1,0,1,
       1,0,1,1,0,1,0,0,0,1,0,1,1,1,0,1,
       1,0,1,1,0,1,1,1,1,1,0,1,1,1,0,1,
       1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,
       1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

maze2=[4,3,4,4,4,4,4,4,4,4,4,4,4,4,4,4,
       4,0,4,4,0,0,0,0,0,4,0,0,0,0,0,4,
       4,0,4,4,4,0,4,4,0,4,0,4,4,4,0,4,
       4,0,0,0,0,0,4,4,0,0,0,0,0,0,0,4,
       4,0,4,4,4,0,0,0,4,4,4,4,4,4,4,4,
       4,0,4,0,4,0,4,4,4,0,0,0,0,0,0,4,
       4,0,4,0,0,0,4,4,4,0,4,4,4,4,0,4,
       4,0,4,4,4,4,4,4,4,0,4,4,2,4,0,4,
       4,0,0,0,0,0,0,0,0,0,4,4,5,4,0,4,
       4,0,4,4,4,4,4,4,4,4,4,4,0,4,0,4,
       4,0,4,0,0,0,0,0,0,0,0,4,0,0,0,4,
       4,0,4,0,4,4,4,4,4,4,0,4,4,4,0,4,
       4,0,4,0,4,0,0,0,0,0,0,4,0,4,0,4,
       4,0,4,0,4,4,4,4,0,4,0,4,0,4,0,4,
       4,0,0,0,0,0,0,0,0,4,0,4,0,0,0,4,
       4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4]

for j in range(len(maze2)):
    if maze2[j] == 1:
        maze2[j] == 4

        



def dist(ax, ay, bx, by, ang):
    ans = ((bx-ax)*(bx-ax) + (by-ay)*(by-ay))**(1/2)
    return(ans)

def equalsXorY(param, x, y):
    if param == x or param == y:
        return(True)
    else:
        return(False)

def drawRays3D(): #Requires variables FOV, RESOLUTION, px, py, pa, mapX, mapY, mapS
#Requires functions sin, cos, tan, atan, complete pygame library
    FoV = FOV
    if RESOLUTION == "Low": Resolution = 1
    if RESOLUTION == "Normal": Resolution = 2
    if RESOLUTION == "High": Resolution = 4
    if RESOLUTION == "Very high": Resolution = 8

    displayWidth = 8*60
    lineOffset = 8//Resolution

    color = (0,0,0)
    
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
            if(mp > 0 and mp<mapX*mapY and map[mp]>0 and map[mp]!=5):
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
            if(mp > 0 and mp<mapX*mapY and map[mp]>0 and map[mp]!=5):
                vx=rx
                vy=ry
                disV = dist(px,py,vx,vy,ra)
                dof = limit
            else:
                rx = rx + xo
                ry = ry + yo
                dof = dof + 1

        disT = 10000

        DIR = ""
        
        if(disV<disH):
            rx = vx
            ry = vy
            disT = disV
            color = (255,0,0)
            DIR = "Vertical"
        if(disH<disV):
            rx = hx
            ry = hy
            disT = disH
            color = (155,0,0)
            DIR = "Horizontal"
            
        #pygame.draw.line(DISPLAY, color, (px,py), (rx,ry))

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
        lineO = int(HEIGHT/2-lineH/2)
        lineO2 = int(HEIGHT/2+lineH/2)
        if(lineH>320):
            lineH = 320

        mapCoordX, mapCoordY = rx//mapS, ry//mapS
        MP = mapCoordY*mapX+mapCoordX

        #Textures

        textured = False

        if MP < len(map) and MP > 0:

            if map[int(MP)] == 2:
                color = (0,255,0)
            if map[int(MP)] == 3:
                color = (255,255,0)
            if map[int(MP)] == 4:

                if DIR == "Horizontal":
                    x_coord = clamp(rx,0,64,64)
                if DIR == "Vertical":
                    x_coord = clamp(ry,0,64,64)

                textured = True

                texture = stone_wall
                
            if map[int(MP)] == 1:
                
                if DIR == "Horizontal":
                    x_coord = clamp(rx,0,64,64)
                if DIR == "Vertical":
                    x_coord = clamp(ry,0,64,64)

                textured = True

                texture = wood_wall

        else:
            raise Exception("The map is probably the wrong size, bro.")

        if textured and show_textures:
            chunk_height = (lineO2-lineO)/8
            chunk_width = lineOffset
            x_coord = x_coord//8
            #for i in range(64):
                #y_coord = i
                #image_strip = texture.crop((x_coord,0,x_coord+lineOffset,64))
                #str_image = image_strip.tobytes("raw","RGBA")
                #display_image = pygame.image.fromstring(str_image, (lineOffset,64), "RGBA")
                #strip = pygame.transform.scale(display_image, (int(lineOffset),
                                                               #int(lineH)))
                #DISPLAY.blit(strip, (r*lineOffset+18,lineO))
            for i in range(8):
                y_coord = i
                color = texture[int((y_coord*8)+x_coord)]
                point1 = (r*lineOffset+18,lineO+chunk_height*i)
                point2 = (r*lineOffset+18, lineO+chunk_height*(i+1))
                pygame.draw.line(DISPLAY,color,
                                 point1,
                                 point2,
                                 chunk_width)

        else:
            pygame.draw.line(DISPLAY,color, (r*lineOffset+18,lineO),
                          (r*lineOffset+18,lineO2), lineOffset)



def drawCursor():
    x = WIDTH//2
    y = HEIGHT//2

    x1 = x - 2
    x2 = x + 2
    y1 = y - 2
    y2 = y + 2

    pygame.draw.polygon(DISPLAY, WHITE, [(x1,y1),
                                         (x2,y1),
                                         (x2,y2),
                                         (x1,y2)])

def applyShade(color, brightness=50):
    r,g,b = color
    
    r = r-brightness
    g = g-brightness
    b = b-brightness

    if r<0: r=0
    if g<0: g=0
    if b<0: b=0
    
    new_color = (r,g,b)
    return(new_color)

def applyLight(color,brightness=50):
    r,g,b = color
    
    r = r+brightness
    g = g+brightness
    b = b+brightness

    if r>255: r=255
    if g>255: g=255
    if b>255: b=255
    
    new_color = (int(r),int(g),int(b))
    return(new_color)

Clock = pygame.time.Clock()


level = 1
oldLevel = level

loadTextures()


running = True

while running:

    if level == 2 and oldLevel == 1:
        oldLevel = 2
        pass
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    DISPLAY.fill(GREY)

    pdx = cos(pa)*p_speed
    pdy = sin(pa)*p_speed
    
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
        pa = pa - p_sensitivity
        if(pa<0):
            pa = pa + 2*PI
        pdx = cos(pa)*p_speed
        pdy = sin(pa)*p_speed
        
    if keys[pygame.K_d]:
        pa = pa + p_sensitivity
        if(pa>2*PI):
            pa = pa - 2*PI
        pdx = cos(pa)*p_speed
        pdy = sin(pa)*p_speed

    mapCoordX = px//mapS
    mapCoordY = py//mapS
    oMapCoordX = opx//mapS
    oMapCoordY = opy//mapS
    if map[int(mapCoordY*mapX+mapCoordX)] == 5:
        map = maze2
        px,py = 96,96
        pa = P2
        if level==2:
            running = False
        level = level+1
        pass
    if map[int(mapCoordY*mapX+mapCoordX)] > 0:
        #px = opx
        #py = opy
        
        npx = cos(pa)*dist(opx,opy,px,py,pa)
        npy = sin(pa)*dist(opx,opy,px,py,pa)
        nMapCoordX, nMapCoordY = npx//mapS, npy//mapS
        #need to determine if the X coordinates or Y coordinates is in the block
            
        if map[int(mapCoordY*mapX+mapCoordX)] == 2:
            print("You win!")

    drawRays3D()

    drawCursor()

    pygame.display.update()

    Clock.tick(60)


pygame.quit()

