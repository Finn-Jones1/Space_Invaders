import pygame, sys, os, random

clock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
FlexyPath = os.path.dirname(os.path.abspath(__file__))
missileY = 0
playerSpeed = 15
display_width = 1000
display_height = 700
Shot = False

pygame.joystick.init()

gameDisplay = pygame.display.set_mode((display_width,display_height))

# ls = [pygame.image.load(FlexyPath+"/E1.png"), pygame.image.load(FlexyPath+"/E2.png"), pygame.image.load(FlexyPath+"/E3.png")]
pygame.display.set_caption('Space Invaders')

black = (0,0,0)
white = (255,255,255)
enemySpeed = 0
enemySpacing = 50
stop = False
enemyImg = []
Ex = []
Ey = []
eChangeX = []
eChangeY = []
numEnemies = 15
for i in range(numEnemies):
    enemyImg.append(pygame.image.load(FlexyPath+"/E1.png"))
    eChangeX.append(enemySpeed)
    eChangeY.append(10)
    Ex.append(100 + enemySpacing * i)
    Ey.append(100)
EnemyW = 28
EnemyL = 78

x =  (display_width * 0.45)
y = (display_height * 0.8)
x_change = 0

# missileX = x + 20
# missileY = y
missileY_change = -30
missileFire = "ready"
# walkCount = 0


hitList = []

def player(x,y):
    gameDisplay.blit(pygame.image.load(FlexyPath+"/Player.png"), (x,y))  # We integer divide walkCounr by 3 to ensure each

def enemy(x,y,i):
    gameDisplay.blit((enemyImg[i]), (x,y))

def fireMisslie(x,y):
    gameDisplay.blit(pygame.image.load(FlexyPath+'/Missile.png'), (x,y))


     

while not stop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                x_change -= playerSpeed
            elif event.key == pygame.K_d:
                x_change += playerSpeed
            elif event.key == pygame.K_ESCAPE:
                stop = True
            elif event.key == pygame.K_SPACE:
                if missileFire == "ready":
                    missileX = x + 20
                    missileY = y
                missileFire = "fire"
            elif event.type == pygame.JOYBUTTONDOWN:
                print("Joystick button pressed.")
            elif event.type == pygame.JOYBUTTONUP:
                print("Joystick button released.")


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                x_change += playerSpeed
            elif event.key == pygame.K_d:
                x_change -= playerSpeed

    gameDisplay.fill(black)





    if missileY <=0:
        missileFire = "ready"

    if missileFire == "fire":
        fireMisslie(missileX,missileY)
        missileY += missileY_change
        for i in range(numEnemies):
            if Ey[i] > missileY:
                print("y crossover")
                if Ex[i] < missileX and Ex[i] > missileX - 28:
                    if str(i) not in hitList:

                        hitList.append(str(i))
                        print(hitList)
                        Shot = True
                        missileFire = "ready"
                        print("x crossover")


    x += x_change


    # if Shot == False:
    for i in range(numEnemies):
        if str(i) not in str(hitList):
            Ex[i] += eChangeX[i]
            enemy(Ex[i],Ey[i], i)

        if Ex[i] > display_width - 65:
            Ey[i] = Ey[i] + 100
            eChangeX[i] = -enemySpeed
        
        if Ex[i] < 0 - 20:
            Ey[i] = Ey[i] + 100
            eChangeX[i] = enemySpeed


    player(x,y)



    pygame.display.update()
    clock.tick(120)

pygame.quit()
quit()