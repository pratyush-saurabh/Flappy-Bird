import random 
import sys 
import pygame
from pygame.locals import * 
FPS = 32
SCREENWIDTH = 289 
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT)) #To initialize screen/display surface
basey = SCREENHEIGHT * 0.83
GAME_SPRITES = {}
GAME_SOUNDS = {} 
PLAYER = 'gallery/sprites/bird.png' 
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'

def welcomeScreen():
    ''' Shows welcome images on the screen '''
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.02)
    while True:
        for event in pygame.event.get():
            
            SCREEN.blit(GAME_SPRITES['background'], (0, 0))    
            SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))       
            SCREEN.blit(GAME_SPRITES['base'], (0, basey)) 
            SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey ))    
            pygame.display.update() 
            FPSCLOCK.tick(FPS) 

            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return

def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    newPipe1 = getRandomPipe() 
    newPipe2 = getRandomPipe()

    upperPipes = [{'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']}]

    lowerPipes = [{'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']}, 
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']}]
    base=[{'x':0,'y':basey}] #Created list here to append new base again and delete old base after appending.

    playerVelY = 0
    playerFlapV = -8
    playerAcc = 1 
    playerMaxVelY = 8 
    playerFlapped = False
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP): 
                if playery > 0: #Checks that bird is below the screen top.
                    playerVelY = playerFlapV 
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        if playerVelY < playerMaxVelY and not playerFlapped: #That is only when space is not pressed, if space is pressed then move it by -8 (towards x axis) fastly.
            playerVelY += playerAcc 
        playerFlapped = False 
            
        #MOVES BIRD VERTICALLY: (Inc. playerY only when not reached to ground) 
        playerHeight = GAME_SPRITES['player'].get_height()
        playery += min(playerVelY, basey - playery - playerHeight) 
   
        #MOVE PIPES TO THE LEFT: (Moving pipes only, so that it will appear that bird is moving relatively)
        for up,lp in zip(upperPipes, lowerPipes): #Used for loop so that both the two pipes move after by after.
            up['x'] += -4 
            lp['x'] += -4 
 
        #ADD a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x']<5:  #Can also check for 1st lower pipes.
            newpipe = getRandomPipe() #Here comes the need of pipex coordinate as SW+10
            upperPipes.append(newpipe[0]) 
            lowerPipes.append(newpipe[1]) 

        #REMOVING PIPE, If it is out of the screen:
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width(): 
            upperPipes.pop(0) 
            lowerPipes.pop(0)
        
        #MOVES BASE TO THE LEFT:
        for b in base:
            b['x']+=-4
        
        dist= (GAME_SPRITES['base'].get_width()-SCREENWIDTH)
        if -dist-3 < base[0]['x'] <= -dist: #Should add some limiting value so that it wouldn't keep adding new base.
            base.append({'x':SCREENWIDTH-1,'y':basey}) 
         
        if base[0]['x'] <= - GAME_SPRITES['base'].get_width(): #Out of the screen completely so that no blank space left after popping
            base.pop(0) #So that now after popping,new base will come at 1st index and will blit. 
        
        #CHECKING SCORE
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2 
        for pipe in upperPipes: #As the x pos of two upper pipes are diff.(SW and SW+200). So iterate for both.
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
                print(f"Your score is {score}") 
                GAME_SOUNDS['point'].play()
        #SETTING DIFFICULTY
        if score > 10:
            playerMaxVelY == 15
                            
        #BLITING SPRITES NOW:
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for up, lp in zip(upperPipes, lowerPipes): #To extract single dict. i.e one upper/lower pipe at a time to blit. 
            SCREEN.blit(GAME_SPRITES['pipe'][0], (up['x'], up['y'])) 
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lp['x'], lp['y']))
        
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
           
        for b in base:
            SCREEN.blit(GAME_SPRITES['base'],(b['x'],b['y']))
        
        #This list value will always get updated rather than appending, in every while loop,
        myDigits = [int(x) for x in str(score)] 
        twidth = 0 #total width of the score until next updated score.
        for digit in myDigits:
            twidth += GAME_SPRITES['numbers'][digit].get_width() #Using digit as an index to fetch image.
        Xoffset = (SCREENWIDTH - twidth)/2 #To place the score exactly at mid pos.

        for digit in myDigits: #To blit every digit of score.
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12)) 
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest: #i.e if True
            return
  
        pygame.display.update() #To update entire surface.
        FPSCLOCK.tick(FPS) #For every sec., max given frames should pass.

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery + GAME_SPRITES['player'].get_height() == basey  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['player'].get_width()-5:
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['player'].get_width()-5:
            GAME_SOUNDS['hit'].play()
            return True

    return False

def getRandomPipe():
    """Generate random positions of two pipes (one bottom straight and one top rotated) for blitting on the screen"""
    offset = SCREENHEIGHT/4
    pipeHeight = GAME_SPRITES['pipe'][0].get_height() 
    pipeX = SCREENWIDTH + 10
    #'random.randrage': Returns a random no. from the specified range ('random.randint' is used only for integers and inclusive range)
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()  - 1.2 *offset)) #Subtract "length of base" from the Screen Height(Length)
    y1 = pipeHeight - y2 + offset #This will be dependent on the y2
    pipe = [ {'x': pipeX, 'y': -y1}, {'x': pipeX, 'y': y2}]
    return pipe

if __name__ == "__main__":
    #This will be the main point from where our game will start
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by Pratyush Saurabh')
    GAME_SPRITES['numbers'] = (pygame.image.load('gallery/sprites/0.png').convert_alpha(), #For quick blitting(showing image on screen)
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),#for changing alpha also, ie opacity
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),)

    GAME_SPRITES['message'] =pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] =pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180), 
    pygame.image.load(PIPE).convert_alpha())
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert() #Only image and its pixels will change for quick blitting
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    # Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    while True:
        welcomeScreen() # Shows welcome screen to the user until he presses a button
        mainGame() # This is the main game function