import pygame, sys, os, random
from pygame.locals import *

clock = pygame.time.Clock()
pygame.init()

FlexyPath = os.path.dirname(os.path.abspath(__file__))

display_width = 900
display_height = 700

pygame.joystick.init()

gameDisplay = pygame.display.set_mode((display_width,display_height))

# ls = [pygame.image.load(FlexyPath+"/E1.png"), pygame.image.load(FlexyPath+"/E2.png"), pygame.image.load(FlexyPath+"/E3.png")]
pygame.display.set_caption('Space Invaders')

black = (0,0,0)
white = (255,255,255)
enemySpeed = 0
enemySpacing = 50
eMissileChange = 30
enemyImg = []
Ex = []
Ey = []
eChangeX = []
eChangeY = []
eMissile = []
XeMissile = []
YeMissile = []
eMChangeX = []
eMChangeY = []
eMissileFire = []
eMX = []
eMY = []
numEnemies = 15

for i in range(numEnemies):


    enemyImg.append(pygame.image.load(FlexyPath+"/E1.png"))
    eChangeX.append(enemySpeed)
    eChangeY.append(10)
    Ex.append(100 + enemySpacing * i)
    Ey.append(100)

    eMissile.append(pygame.image.load(FlexyPath+"/eMissile.png"))
    # eMChangeX.append(enemySpeed)
    eMChangeY.append(eMissileChange)
    eMissileFire.append("ready")
    eMX.append(100)
    eMY.append(100)
    


# walkCount = 0


def player(x,y):
    gameDisplay.blit(pygame.image.load(FlexyPath+"/Player.png"), (x,y))  # We integer divide walkCounr by 3 to ensure each

def enemy(x,y,i):
    gameDisplay.blit((enemyImg[i]), (x,y))

def fireMisslie(x,y):
    gameDisplay.blit(pygame.image.load(FlexyPath+'/Missile.png'), (x,y))

def eFireMisslie(x,y,i):
    gameDisplay.blit((eMissile[i]), (x,y))


# def textDisplay(text):
#     text = pygame.font.Font(FlexyPath + 'Quicksand-VariableFont_wght.ttf', 110)


def textRender(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def showText(text, fontSize):
    Font = pygame.font.Font(FlexyPath+'/Quicksand-VariableFont_wght.ttf', fontSize)
    finalText, textLoc = textRender(text, Font)
    textLoc = (10,0)
    gameDisplay.blit(finalText, textLoc)

def hitDetect(x,y,x1,y1, hitSizeW, hitSizeL, ajustmentsW):
    if x - hitSizeW < x1 and x + hitSizeL > x1 and y + ajustmentsW > y1 and y - hitSizeL < y1:
        return True

def gameLoop():
    Shot = False
    hitList = []
    x =  (display_width * 0.45)
    y = (display_height * 0.8)
    x_change = 0
    axis = ''
    missileY = 0
    playerSpeed = 20
    EnemyW = 28
    EnemyL = 78
    missileY_change = -30
    missileFire = "ready"

    joyConnect = "false"

    stop = False
    while not stop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop = True
            if event.type == pygame.JOYBUTTONDOWN:
                    if missileFire == "ready":
                        missileX = x + 28
                        missileY = y

                    

                    missileFire = "fire"
                    # joyConnect = "true"
                    


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    x_change -= playerSpeed
                elif event.key == pygame.K_d:
                    x_change += playerSpeed
                elif event.key == pygame.K_ESCAPE:
                    stop = True
                elif event.key == pygame.K_SPACE:
                    if missileFire == "ready":
                        missileX = x + 28
                        missileY = y
                    missileFire = "fire"
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    x_change += playerSpeed
                elif event.key == pygame.K_d:
                    x_change -= playerSpeed
            
        gameDisplay.fill(black)

        showText('Score: ' + str(len(hitList)), 50)

        joystick_count = pygame.joystick.get_count()

        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            axis = joystick.get_axis(0)

        # if joyConnect == "true":

        # if axis > 0.5:
        #     x = x + playerSpeed * axis
        # elif axis < -0.01:
        #     x = x + playerSpeed * axis






            



        if missileY <=0:
            missileFire = "ready"

        if missileFire == "fire":
            fireMisslie(missileX,missileY)
            missileY += missileY_change
            for i in range(numEnemies):
                # if Ey[i] + 40 > missileY:
                print("y crossover")
                if hitDetect(Ex[i],Ey[i], missileX, missileY, 15, 30, 20) is True:
                    if i not in hitList:
                        hitList.append(i)
                        Shot = True
                        missileFire = "ready"
                        print("x crossover")




        for i in range(numEnemies):
            if i not in hitList:
                
                Ex[i] += eChangeX[i]
                enemy(Ex[i],Ey[i], i)

                hello = random.randint(0,100)

                if hello == 1:
                    if eMissileFire[i] != "fire":
                        eMX[i] = Ex[i]
                        eMY[i] = Ey[i]
                        eMissileFire[i] = "fire"
                if eMY[i] > 700:
                    eMissileFire[i] = "ready"

            if Ex[i] > display_width - 10:
                Ey[i] = Ey[i] + 100
                eChangeX[i] = -enemySpeed
            
            if Ex[i] < 0 - 30:
                Ey[i] = Ey[i] + 100
                eChangeX[i] = enemySpeed
            
            if eMissileFire[i] == "fire":

                eFireMisslie(eMX[i],eMY[i], i)
                
                eMY[i] += eMissileChange
                # print(y)
                if eMY[i] > y and eMY[i] < y + 50:
                    # print(eMY[i])
                    if eMX[i] < x + 50 and eMX[i] > x:
                        print("hit") 
                # if hitDetect(x,y, eMY[i], eMY[i], 50, 50, 0) is True:
                #     print("hit")

        x += x_change
        player(x,y)

        pygame.display.update()
        clock.tick(120)

gameLoop()
pygame.quit()
quit()