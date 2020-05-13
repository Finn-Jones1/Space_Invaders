import pygame, sys

clock = pygame.time.Clock()
from pygame.locals import *
pygame.init()

playerSpeed = 15
display_width = 1000
display_height = 700

gameDisplay = pygame.display.set_mode((display_width,display_height))

ls = [pygame.image.load("/Users/finnjones/IST/E1.png"), pygame.image.load("/Users/finnjones/IST/E2.png"), pygame.image.load("/Users/finnjones/IST/E3.png")]
pygame.display.set_caption('A bit Racey')

black = (0,0,0)
white = (255,255,255)


crashed = False
playerImg = pygame.image.load('/Users/finnjones/IST/Player.png')
x =  (display_width * 0.45)
y = (display_height * 0.8)
x_change = 0

missileImg = pygame.image.load('/Users/finnjones/IST/Missile.png')

missileX = x + 20
missileY = y
missileY_change = -30
missileFire = "ready"
walkCount = 0


def player(x,y):
    global walkCount
    if walkCount + 1 >= 3:
        walkCount = 0
    gameDisplay.blit(ls[walkCount//3], (x,y))  # We integer divide walkCounr by 3 to ensure each


def fireMisslie(x,y):
    gameDisplay.blit(missileImg, (x,y))


     


while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                x_change -= playerSpeed
            elif event.key == pygame.K_d:
                x_change += playerSpeed
            elif event.key == pygame.K_SPACE:
                if missileFire == "ready":
                    missileX = x + 20
                    missileY = y
                missileFire = "fire"


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

    x += x_change

    player(x,y)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()