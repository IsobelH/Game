import random # For generating random numbers
import sys # We will use sys.exit to exit the program
import pygame # makes all the available pygame modules available
from pygame.locals import * # Basic pygame imports
pygame.init()


# Global Variables for the game
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
HIGHSCORE=int(0)
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
playerNumber = random.randint(0,2)
characters = ['gallery/sprites/papa smurf.png', 'gallery/sprites/smurfette.png', 'gallery/sprites/gargamel.png']
PLAYER = pygame.image.load(characters[playerNumber])
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe1.png'
smurfberry = pygame.image.load('gallery/sprites/smurfberries.png')
smurfberries = []

EXPLOSTION=pygame.image.load('gallery/sprites/explosion.png').convert_alpha()
BACKGROUNDc = pygame.image.load('gallery/sprites/background.png').convert_alpha()
LOGOc=pygame.image.load('gallery/sprites/logo.png').convert_alpha()
BASEc=pygame.image.load('gallery/sprites/base.png').convert_alpha()

def welcomeScreen():
    """
    Shows welcome images on the screen
    """

    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)

    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()  # if user clicks on cross button, close the game

            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return # if  user presses space or up key, start the game for them
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0, 0))    
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))    
                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey ))    
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))    
                pygame.display.update() #if user presses nothing, images are blited onto screen
                FPSCLOCK.tick(FPS)  


def button(screen, position, text):
    font = pygame.font.SysFont("Arial", 20)
    text_render = font.render(text, 1, (255, 255, 255))
    x, y, w , h = text_render.get_rect()
    x, y = position
    pygame.draw.line(screen, (203, 000, 000), (x, y), (x + w , y), 5)
    pygame.draw.line(screen, (203, 000, 000), (x, y - 2), (x, y + h), 5)
    pygame.draw.line(screen, (139, 11, 11), (x, y + h), (x + w , y + h), 5)
    pygame.draw.line(screen, (139, 11, 11), (x + w , y+h), [x + w , y], 5)
    pygame.draw.rect(screen, (139, 11, 11), (x, y, w , h))
    return screen.blit(text_render, (x, y))

def character(): #allows user to select charcater
    
    PapaSmurfIcon=pygame.image.load('gallery/sprites/papasmurfmessage.png').convert_alpha()
    SmurfetteIcon=pygame.image.load('gallery/sprites/smurfettemessage.png').convert_alpha()
    GargamelIcon=pygame.image.load('gallery/sprites/gargamelmessage.png').convert_alpha()

    SCREEN.blit(BACKGROUNDc, (0, 0))
    logox = int((SCREENWIDTH/2)-LOGOc.get_width()/2)
    SCREEN.blit(BASEc, (0, GROUNDY))
    logoy = int(SCREENHEIGHT*0.13)
    SCREEN.blit(LOGOc, (logox,logoy ))


    #creates buttons for characters
    b1 = button(SCREEN, (50,200), "Red Car")
    SCREEN.blit(PapaSmurfIcon, (175,175))
    b2 = button(SCREEN, (50,275), "Smurfette")
    SCREEN.blit(SmurfetteIcon, (175,250))
    b3 = button(SCREEN, (50,350), "Gargamel")
    SCREEN.blit(GargamelIcon, (175,325))
    pygame.display.update()
    FPSCLOCK.tick(FPS)

    #allows user to select a button
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()  # if user clicks on cross button, close the game
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b1.collidepoint(pygame.mouse.get_pos()):
                    PLAYER='gallery/sprites/papa smurf.png'
                    return PLAYER
                    go=True
                    return PLAYER
                elif b2.collidepoint(pygame.mouse.get_pos()):
                    PLAYER='gallery/sprites/smurfette.png'
                    go=True
                    return PLAYER
                elif b3.collidepoint(pygame.mouse.get_pos()):
                    PLAYER='gallery/sprites/gargamel.png'
                    go=True
                    return PLAYER

def hightscore(score):
    print("New highscore")
    HIGHSCORE=int(score)
    return HIGHSCORE

def mainGame(HIGHSCORE):
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    #randomly creates 2 pipes for blitting onto the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    #list of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
    ]
    #list of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200 +(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]

    #velocity of sprites
    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1
    playerFlapAccv = -8 # velocity while flying(flapping)
    playerFlapped = False # It is true only when the smurfs are flying(flapping)


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): #if user presses esc, game closes
                pygame.quit()
                sys.exit() 
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP): #if user presses space or up arrow, sleigh flys(flaps)
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()


        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) #returns true if the player crashes
        if crashTest:
            return HIGHSCORE   

        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2 #checks score
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
                print(f"Your score is {score}") #outputs players score
                GAME_SOUNDS['point'].play() #outputs score sound


        if score>HIGHSCORE:
            HIGHSCORE=hightscore(score)

        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY 

        if playerFlapped:
            playerFlapped = False            
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        #move pipes to the left
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        #adds a new pipe when the first is about to go off the screen
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        #if pipe is out of screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        #blits the sprites
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))

        font = pygame.font.SysFont('microsoftjhengheimicrosoftjhengheiuiligh', 25)
        text=font.render(("Highscore:"+str(HIGHSCORE)), True, (255,255,255))
        SCREEN.blit(text, (10,10))

        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUNDY - 25  or playery<0: #if player collides with ground, game over
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes: #if player collides with top pipe, game over
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            GAME_SOUNDS['song'].stop()
            SCREEN.blit(EXPLOSTION,(playerx, playery))
            pygame.display.update()
    

            return True

    for pipe in lowerPipes: #if player collides with bottom pipe, game over
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            GAME_SOUNDS['song'].stop()
            SCREEN.blit(EXPLOSTION,(playerx, playery))
            pygame.display.update()
            return True

    return False

def getRandomPipe(): #generates positions of two pipes for blitting onto screen
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()  - 1.2 *offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe

if __name__ == "__main__":
    #this is the main point from where the game will start
    pygame.init() #initialise all pygame's modules
    FPSCLOCK = pygame.time.Clock()

    pygame.display.set_caption('Flappy Smurf by Juliana, Katie, and Isobel')
    PLAYER=character()


    GAME_SPRITES['numbers'] = ( 
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] =pygame.image.load('gallery/sprites/messageSmurf1.png').convert_alpha()
    GAME_SPRITES['base'] =pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180), 
    pygame.image.load(PIPE).convert_alpha()
    )

    #game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')
    GAME_SOUNDS['song'] = pygame.mixer.Sound('gallery/audio/SmurfSong.mp3')

    #gmae sprites
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER) .convert_alpha()


    while True: 
 

        GAME_SOUNDS['song'].play()
        welcomeScreen() # Shows welcome screen to the  user until he presses a button
        HIGHSCORE=mainGame(HIGHSCORE) # This is the main game function 


