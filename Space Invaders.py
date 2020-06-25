import pygame, sys, os, random, time, datetime
from pygame.locals import *

clock = pygame.time.Clock()
pygame.init()

FlexyPath = os.path.dirname(os.path.abspath(__file__))

display_width = 900
display_height = 700

pygame.joystick.init()

screen = pygame.display.set_mode((display_width,display_height))

pygame.display.set_caption('Space Invaders')

black = (0,0,0)
white = (255,255,255)
grey = (128,128,128)
lightGrey = (211,211,211)

f=open(FlexyPath + "/data.txt", "r")
contents = f.read()
f.close()
Scontents = contents.split()

highestLevel = Scontents[0]

highestScore = Scontents[1]



enemySpacing = 50
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
x_change = 0
Score = 0
playerSpeed = 15
hitList = []
doublePoints = False
clusterShot = False
health = 5
numEnemies = 3
levelCounter = 1
eMissileChange = 15
enemySpeed = 5


for i in range(numEnemies):
    enemyImg.append(pygame.image.load(FlexyPath+"/sprites/E1.png"))
    eChangeX.append(enemySpeed)
    eChangeY.append(10)
    Ex.append(100 + enemySpacing * i)
    Ey.append(100)

    eMissile.append(pygame.image.load(FlexyPath+"/sprites/eMissile.png"))
    eMChangeY.append(eMissileChange)
    eMissileFire.append("ready")
    eMX.append(100)
    eMY.append(100)
    


# Sound Effects
hitSound = pygame.mixer.Sound(FlexyPath+"/sound/Hit_Hurt.wav")
click = pygame.mixer.Sound(FlexyPath+"/sound/Blip_Select.wav")
Shoot = pygame.mixer.Sound(FlexyPath+"/sound/Missile_Shoot.wav")
Explosion = pygame.mixer.Sound(FlexyPath+"/sound/Explosion.wav")
hitSound = pygame.mixer.Sound(FlexyPath+"/sound/Hit_Hurt.wav")

# Background
background_image = pygame.image.load(FlexyPath+"/sprites/bg.png")

pygame.mixer.music.load(FlexyPath+'/sound/music.mp3')
pygame.mixer.music.play(-1)

def save():
    global highestScore
    global highestLevel
    f = open(FlexyPath + '/data.txt','w')
    if int(Score) > int(highestScore):
        highestScore = Score
    if int(levelCounter) > int(highestLevel):
        highestLevel = levelCounter

    f.write(str(highestLevel)+ " " + str(highestScore))

def boom(x,y):
    screen.blit(pygame.image.load(FlexyPath+"/sprites/Boom.png"),(x,y))

def player(x,y):
    screen.blit(pygame.image.load(FlexyPath+"/sprites/Player.png"), (x,y))  # We integer divide walkCounr by 3 to ensure each

def bossEn(x,y):
    screen.blit(pygame.image.load(FlexyPath+"/sprites/BossE.png"), (x,y))

def enemy(x,y,i):
    screen.blit((enemyImg[i]), (x,y))

def fireMisslie(x,y):
    screen.blit(pygame.image.load(FlexyPath+'/sprites/Missile.png'), (x,y))

def eFireMisslie(x,y,i):
    screen.blit((eMissile[i]), (x,y))

def textRender(text, font , colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()

def showText(text, fontSize, textloc, colour):
    Font = pygame.font.Font(FlexyPath+'/Quicksand-VariableFont_wght.ttf', fontSize)
    finalText, textLoc = textRender(text, Font , colour)
    screen.blit(finalText, textloc)

def hitDetect(x,y,x1,y1, hitSizeW, hitSizeL):
    if x - hitSizeW < x1 and x + hitSizeW > x1 and y + hitSizeL > y1 and y - hitSizeL < y1:
        return True
    else:
        return False
  
def Intro():
    global joyConnect
    global powerupSelector
    global selection
    joyConnect = "false"
    controllerStatus = "Off"
    powerupSelector = ["Double Points", "Cluster Shot", "Super Speed"]
    selection = 0
    stop = False
    
    screen.blit(background_image, [0, 0])
    
    # Start Game
    pygame.draw.rect(screen,white,(404,500,100,50))
    # Powerup Switcher Button
    pygame.draw.rect(screen,white,(370,400,170,50))
    # Controler On / Off
    pygame.draw.rect(screen,white,(380,600,150,50))

    showText('Start', 30, (420 ,505), black)
    showText('Controller '+ controllerStatus, 20, (396 ,610), black)
    showText('Pew Pew 2D', 50, (100 ,100), white)
    showText('High Score: '+ str(highestScore), 30, (100 ,170), white)
    showText('High Level: '+ str(highestLevel), 30, (100 ,210), white)
    showText('Powerup Selecter: ', 20, (375 ,405), black)
    showText(powerupSelector[selection], 15, (402 ,430), black)

    while not stop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()


            if joyConnect == "true":
                controllerStatus = "On"
            elif joyConnect == "false":
                controllerStatus = "Off"


            
            if pygame.mouse.get_pos()[0] > 405 and pygame.mouse.get_pos()[0] < 505:
                if pygame.mouse.get_pos()[1] > 500 and pygame.mouse.get_pos()[1] < 550:
                    pygame.draw.rect(screen,lightGrey,(404,500,100,50))
                    showText('Start', 30, (420 ,505), black)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        click.play()
                        pygame.draw.rect(screen,grey,(404,500,100,50))
                        showText('Start', 30, (420 ,505), black)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        pygame.draw.rect(screen,white,(404,500,100,50))
                        showText('Start', 30, (420 ,505), black)
                        print("pressed")
                        gameLoop()
                else:
                    pygame.draw.rect(screen,white,(404,500,100,50))
                    showText('Start', 30, (420 ,505), black)


            if pygame.mouse.get_pos()[0] > 380 and pygame.mouse.get_pos()[0] < 529:
                if pygame.mouse.get_pos()[1] > 600 and pygame.mouse.get_pos()[1] < 649:
                    pygame.draw.rect(screen,lightGrey,(380,600,150,50))
                    showText('Controller '+ controllerStatus, 20, (396 ,610), black)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        click.play()
                        print("test")
                        if joyConnect == "true":
                            joyConnect = "false"
                            pygame.draw.rect(screen,grey,(380,600,150,50))

                        elif joyConnect == "false":
                            joyConnect = "true"
                            pygame.draw.rect(screen,grey,(380,600,150,50))
                        showText('Controller '+ controllerStatus, 20, (396 ,610), black)

                            
                    if event.type == pygame.MOUSEBUTTONUP:
                        pygame.draw.rect(screen,white,(380,600,150,50))
                        showText('Controller '+ controllerStatus, 20, (396 ,610), black)
                else:
                    pygame.draw.rect(screen,white,(380,600,150,50))
                    showText('Controller '+ controllerStatus, 20, (396 ,610), black)


            if pygame.mouse.get_pos()[0] > 370 and pygame.mouse.get_pos()[0] < 540:
                if pygame.mouse.get_pos()[1] > 400 and pygame.mouse.get_pos()[1] < 450:
                    pygame.draw.rect(screen,lightGrey,(370,400,170,50))
                    showText('Powerup Selecter: ', 20, (375 ,405), black)
                    showText(powerupSelector[selection], 15, (402 ,430), black)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        selection = selection + 1
                        print(selection)
                        if len(powerupSelector) == selection:
                            selection = 0
                        pygame.draw.rect(screen,grey,(370,400,170,50))
                        showText('Powerup Selecter: ', 20, (375 ,405), black)
                        showText(powerupSelector[selection], 15, (402 ,430), black)
                        
                        print("change")
            
                else:
                    pygame.draw.rect(screen,white,(370,400,170,50))
                    showText('Powerup Selecter: ', 20, (375 ,405), black)
                    showText(powerupSelector[selection], 15, (402 ,430), black)


            pygame.display.update()
            clock.tick(120)

def gameLoop():
    global levelCounter
    global enemySpeed
    global numEnemies
    global x_change
    global Score
    global playerSpeed
    global doublePoints
    global clusterShot
    global hitList
    global health
    BossX = 2000
    BossY = 100
    movementEprevent = 0
    bossChange = -10
    
    x = (display_width * 0.45)
    y = (display_height * 0.8)
    axis = ''
    missileY = 0
    EnemyW = 28
    EnemyL = 78
    missileX = 0
    missileY = 0
    missileY_change = -30
    missileFire = "ready"
    
    connectEndLoop = "false"
    boundaries = 0

    

    if powerupSelector[selection] == "Super Speed":
        playerSpeed = 30
        clusterShot = False
        doublePoints = False

    elif powerupSelector[selection] == "Double Points":
        doublePoints = True
        playerSpeed = 15
        clusterShot = False
    
    elif powerupSelector[selection] == "Cluster Shot":
        clusterShot = True
        playerSpeed = 15
        doublePoints = False


    x_change = 0
    stop = False
    while not stop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save()
                Intro()
            if event.type == pygame.JOYBUTTONDOWN:
                
                    if missileFire == "ready":
                        Shoot.play()
                        missileX = x + 28
                        missileY = y
                    missileFire = "fire"



            if event.type == pygame.KEYDOWN:
                

                if event.key == pygame.K_SPACE:
                    if missileFire == "ready":
                        Shoot.play()
                        missileX = x + 28
                        missileY = y
                    missileFire = "fire"

                elif event.key == pygame.K_a:
                    x_change -= playerSpeed
                    movementEprevent = 1

                elif event.key == pygame.K_d:
                    x_change += playerSpeed
                    movementEprevent = 1
                    
                # elif event.key == pygame.K_ESCAPE:
                #     stop = True


            if event.type == pygame.KEYUP:
                
                if event.key == pygame.K_a:
                    if movementEprevent == 1:
                        x_change += playerSpeed
                    else:
                        x_change = 0
                    
                elif event.key == pygame.K_d:
                    if movementEprevent == 1:
                        x_change -= playerSpeed
                    else:
                        x_change = 0
                    movementEprevent = 0
            # else:
            #     print("ting")
            #     x_change = 0


        if x < 10:
            if x_change < 0:
                x_change = 0
                movementEprevent = 0

        elif x > 821:
            if x_change > 0:
                x_change = 0
                movementEprevent = 0



        screen.blit(background_image, [0, 0])

        joystick_count = pygame.joystick.get_count()

        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            axis = joystick.get_axis(0)

        if joyConnect == "true":

            if axis > 0.5:
                x = x + playerSpeed * axis
            elif axis < -0.01:
                x = x + playerSpeed * axis

        if missileY < -20:
            missileFire = "ready"

        if missileFire == "fire":
            if hitDetect(BossX,BossY, missileX, missileY, 30, 30) is True:
                Explosion.play()
                boom(BossX, BossY)
                if doublePoints is True:
                    Score = Score + 200
                else:
                    Score = Score + 100
                print(Score)
                BossX = 2000
                missileFire = "ready"
            fireMisslie(missileX,missileY)
            missileY += missileY_change
            for i in range(numEnemies):
                print("y crossover")
                if hitDetect(Ex[i],Ey[i], missileX, missileY, 25, 30) is True:
                    if i not in hitList:
                        Explosion.play()
                        boom(Ex[i], Ey[i])
                        hitList.append(i)
                        if clusterShot is True:
                            if i - 1 >= 0 and i - 1 not in hitList:
                                boom(Ex[i - 1], Ey[i - 1])
                                hitList.append(i - 1)
                            if i + 1 < numEnemies and i + 1 not in hitList:
                                boom(Ex[i + 1], Ey[i + 1])
                                hitList.append(i + 1)
                            
                        if doublePoints is True:
                            Score = Score + 20
                        else:
                            Score = Score + 10
                        # Shot = True
                        missileFire = "ready"
                        print("x crossover")




        for i in range(numEnemies):
            if i not in hitList:
                
                
                Ex[i] += eChangeX[i]
                enemy(Ex[i],Ey[i], i)

                shootDelay = random.randint(0,250)

                if shootDelay == 1:
                    if eMissileFire[i] != "fire":
                        eMX[i] = Ex[i]
                        eMY[i] = Ey[i]
                        eMissileFire[i] = "fire"
                if eMY[i] > 670:
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
                if eMY[i] + 50 > y and eMY[i] < y + 50:
                    # print(eMY[i])
                    if eMX[i] < x + 90 and eMX[i] > x:
                        health -= 1
                        hitSound.play()
                        eMissileFire[i] = "ready"
                        boom(eMX[i],eMY[i])
                        
                        print("hit")


            if health == 0 or Ey[i] > 650 and Ex[i] < 0:
                save()
                hitList.clear()
                eChangeX.clear()
                Ex.clear()
                Ey.clear()
                eMissileFire.clear()
                levelCounter = 1
                enemySpeed = 5
                numEnemies = 3
                Score = 0
                enemyImg.clear()
                eMissile.clear()
                eMX.clear()
                eMY.clear()
                health = 5
                for i in range(numEnemies):
                    enemyImg.append(pygame.image.load(FlexyPath+"/sprites/E1.png"))
                    eChangeX.append(enemySpeed)
                    Ex.append(100 + enemySpacing * i)
                    Ey.append(100)
                    eMissile.append(pygame.image.load(FlexyPath+"/sprites/eMissile.png"))
                    eMissileFire.append("ready")
                    eMX.append(100)
                    eMY.append(100)

                gameOverScreen()


        if len(hitList) == numEnemies:
            levelCounter += 1
            save()
            enemySpeed = enemySpeed + int(levelCounter)
            print(numEnemies)
            hitList.clear()
            eChangeX.clear()
            Ex.clear()
            Ey.clear()
            eMissileFire.clear()
            numEnemies = numEnemies + 2
            x_change = 0
            for i in range(numEnemies):
                enemyImg.append(pygame.image.load(FlexyPath+"/sprites/E1.png"))
                eChangeX.append(enemySpeed)
                Ex.append(100 + enemySpacing * i)
                Ey.append(100)
                eMissile.append(pygame.image.load(FlexyPath+"/sprites/eMissile.png"))
                eMissileFire.append("ready")
                eMX.append(100)
                eMY.append(100)

            gameLoop()



        if BossX < -100:
            BossX = 2000

        

        
        
        
        x += x_change
        BossX += bossChange
        player(x,y)
        bossEn(BossX, BossY)

        showText('Level: ' + str(levelCounter), 50, (500,0), white)
        showText('Lives: ' + str(health), 50, (700,0), white)
        showText('Score: ' + str(Score), 50, (10,0), white)

        pygame.display.update()
        clock.tick(100)



def gameOverScreen():
    stop = False
    
    screen.blit(background_image, [0, 0])

    showText('Game Over', 50, (100 ,100), white)
    showText('Click To Play Again', 30, (100 ,150), white)

    

    while not stop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Intro()
            if event.type == pygame.MOUSEBUTTONDOWN:
                Intro()

        pygame.display.update()
        clock.tick(120)

Intro()

# gameOverScreen()
pygame.quit()
quit()