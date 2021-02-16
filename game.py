import pygame
import random
import time
pygame.init() #vraća touple

displayWidth = 500
displayHeight = 500

WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,240,0)

gameDisplay=pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Snakey")

img = pygame.image.load('img/snake.jpg')
appleimg = pygame.image.load('img/apple.png')
icon = pygame.image.load('img/icon.png')
direction = "right"

clock = pygame.time.Clock()
FPS = 15
AppleThickness=30

smallfont = pygame.font.SysFont("rockwell", 20) #moramo def font
mediumfont = pygame.font.SysFont("rockwell", 50)
bigfont = pygame.font.SysFont("rockwell", 80)
pygame.display.set_icon(icon) #najbolje 32x32
#funkcije za ispis i da taj ispis bude centriran

def pause():
    paused = True
    display_msg("Paused", BLACK, -100, size="big")
    display_msg("Press C to conitnue or Q to quit", BLACK, 25)
    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False

                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        # gameDisplay.fill(WHITE)

        clock.tick(5)


def score(score):
    text = smallfont.render("Score: "+ str(score),True, WHITE)
    gameDisplay.blit(text,[0,0]) #ovako stavimo taj tekst na ekran


def randAppleGen():
    randAppleX = round(random.randrange(0, displayWidth - AppleThickness - 10))  # / 10.0) * 10.0
    randAppleY = round(random.randrange(0, displayHeight - AppleThickness - 10))

    return randAppleX, randAppleY

def game_intro():

    intro = True

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(BLACK)
        display_msg("Welcome to Snakey", GREEN, -100, size="medium")
        display_msg("Eat as many apples as you can", WHITE, -30, size="small")
        display_msg("Press C to continue, Q to quit or P to pause", RED, 180)

        pygame.display.update()
        clock.tick(15)

def snake(block_size, snakeList):

    if direction == "right":
        head = img
    if direction == "left":
        head = pygame.transform.rotate(img, 180)
    if direction == "up":
        head = pygame.transform.rotate(img, 90)
    if direction == "down":
        head = pygame.transform.rotate(img, 270)

    gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))

    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay, GREEN, [XnY[0], XnY[1], block_size, block_size])



def text_objects(text,color,size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = mediumfont.render(text, True, color)
    elif size == "big":
        textSurface = bigfont.render(text, True, color)

    return textSurface, textSurface.get_rect()
    #ovo nam vraca pozadinu teksta i okvir njegov


def display_msg(msg,color,y_displace=0,size="small"): #y_displace pomice od centra
    textSurface, textRect = text_objects(msg,color,size)
    textRect.center =(displayWidth/2), (displayHeight/2)+y_displace
    gameDisplay.blit(textSurface, textRect)





def game_loop():
    global direction
    gameExit = False
    gameOver = False
    lead_x = displayWidth / 2  # def di ce se nalazit glava
    lead_y = displayHeight / 2

    lead_x_change = 10 #ovako se zmija odma krece
    lead_y_change = 0
    block_size = 15

    randAppleX = round(random.randrange(0, displayWidth - AppleThickness)) #/ 10.0) * 10.0
    randAppleY = round(random.randrange(0, displayHeight - AppleThickness)) #/ 10.0) * 10.0

    snakeList = []
    snakeLength = 1

    while not gameExit:

        if gameOver == True:
            # gameDisplay.fill(WHITE)
            display_msg("GAME OVER", RED, -50, size="medium")
            display_msg("Press Q to QUIT or C to CONTINUE", GREEN, 0, size="small")
            pygame.display.update()

        while gameOver == True:


            for event in pygame.event.get():
                if event.type == pygame.QUIT: #pritisnemo X za izlazak
                    gameOver = False
                    gameExit = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        game_loop()
                    elif event.key == pygame.K_q:
                        gameOver = False
                        gameExit = True


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction ="left"
                    lead_x_change = -block_size
                    lead_y_change = 0
                if event.key == pygame.K_RIGHT:
                    direction = "right"
                    lead_x_change = block_size
                    lead_y_change = 0
                if event.key == pygame.K_UP:
                    direction = "up"
                    lead_x_change = 0
                    lead_y_change = -block_size
                if event.key == pygame.K_DOWN:
                    direction = "down"
                    lead_x_change = 0
                    lead_y_change = block_size
                if event.key == pygame.K_p:
                    pause()


        #kad zmija pride priko
        if lead_x >= displayWidth or lead_x < 0 or lead_y >= displayHeight or lead_y < 0:
            gameOver = True

        lead_x += lead_x_change
        lead_y += lead_y_change


        gameDisplay.fill(BLACK) #pozadina

        gameDisplay.blit(appleimg, (randAppleX,randAppleY)  )

        snakeHead=[]
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        #ali sad se cilo vrime dodaju elementi jer se pomiče zmija, i tako se minja lead x,y
        if len(snakeList) > snakeLength:
            del snakeList[0]
        '''Kako se zmija pomice mi imamo listu,
            prvi lead x,y su na [0] mistu liste,
            a ostali se appendaju. Kako se zmija pomice, taj [0]
            ostaje na istom mistu, i njega gori brišemo,
            da nebi zmija bila duga'''

        if snakeHead in snakeList[:-2]: #ide do -2 jer nam je duljina 2
            gameOver = True #ne smimo se ugrist


        snake(block_size, snakeList)

        score(snakeLength-1) #snakelengts krece od 1 pa moramo oduzet 1

        pygame.display.update()

        if lead_x > randAppleX and lead_x < randAppleX + AppleThickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + AppleThickness:

            if lead_y > randAppleY and lead_y < randAppleY + AppleThickness:
                randAppleX, randAppleY = randAppleGen()
                snakeLength += 1
            elif lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + AppleThickness:
                randAppleX, randAppleY = randAppleGen()
                snakeLength += 1

        clock.tick(FPS)

    pygame.quit() #ovo je obavezno
    quit()

game_intro()
game_loop()