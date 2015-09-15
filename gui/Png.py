import pygame, sys
from pygame.locals import *
import time
SPTruVal = 0 #To be removed 
# Number of frames per second
# Change this value to speed up or slow down your game
FPS = 50
Threshold = 1.0  #this is used to determine whether the paddle is high or low
#Global Variables to be used through our program

pygame.display.init()
disp = pygame.display.Info()
WINDOWWIDTH = disp.current_w - 50
WINDOWHEIGHT = disp.current_h -200
size = [WINDOWWIDTH,WINDOWHEIGHT]
# screen = pygame.display.set_mode(size)
# background = pygame.Surface(screen.get_size())



LINETHICKNESS = 10
PADDLESIZE = (10)
PADDLEOFFSET = 20
pygame.mixer.init()
coin = pygame.mixer.Sound('mariocoin.wav')




# Set up the colours
BLACK     = (0  ,0  ,0  )
WHITE     = (255,255,255)

#Draws the arena the game will be played in. 
def drawArena():
    DISPLAYSURF.fill((0,0,0))
    #Draw outline of arena
    pygame.draw.rect(DISPLAYSURF, WHITE, ((0,0),(WINDOWWIDTH,WINDOWHEIGHT)), LINETHICKNESS*2)
    



#Draws the paddle
def drawPaddle(paddle):
    #Stops paddle moving too low
    if paddle.bottom > WINDOWHEIGHT - LINETHICKNESS:
        paddle.bottom = WINDOWHEIGHT - LINETHICKNESS
    #Stops paddle moving too high
    elif paddle.top < LINETHICKNESS:
        paddle.top = LINETHICKNESS
    #Draws paddle
    pygame.draw.rect(DISPLAYSURF, WHITE, paddle)


def drawSprite(b):  
    if b.rect.bottom > WINDOWHEIGHT - LINETHICKNESS:
        b.rect.bottom = WINDOWHEIGHT - LINETHICKNESS
    #Stops paddle moving too high
    elif b.rect.top < LINETHICKNESS:
        b.rect.top = LINETHICKNESS
 

    DISPLAYSURF.blit(b.image, b.rect)





#Checks to see if a point has been scored returns new score
def checkPointScored(paddle1, score): # paddle1, ball, score, ballDirX):

    if 1 == 2:
        a = true
    else: return score



#Displays the current score on the screen 
def displayScore(score):
    resultSurf = BASICFONT.render('Score = %s' %(score), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 150, 25)
    DISPLAYSURF.blit(resultSurf, resultRect)
	
#Displays the Electrode Value on the screen  for debugging
def displaySPTruVal(SPTruVal):
    resultSurf = BASICFONT.render('SPVal = %s' %(SPTruVal), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 300, 25)
    DISPLAYSURF.blit(resultSurf, resultRect)

#Main function
def main():
    pygame.init()
    global DISPLAYSURF
    ##Font information
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 20
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT)) 
    pygame.display.set_caption('Pong')

    #Initiate variable and set starting positions
    playerOnePosition = (WINDOWHEIGHT - PADDLESIZE) /2
    score = 0



    #Creates Rectangles for ball and paddles also sprite.
    
    paddle1 = pygame.Rect(WINDOWWIDTH/2 - LINETHICKNESS/2, playerOnePosition, LINETHICKNESS,PADDLESIZE)
    
    
    b = pygame.sprite.Sprite() # create sprite
    b.image = pygame.image.load("Glider.png").convert() # load ball image
    b.image.convert_alpha()
    b.rect = b.image.get_rect() # use image extent values
    b.rect.topleft = [WINDOWWIDTH/2, WINDOWHEIGHT/2] # put the image in the top left corner
    print(b.rect.y)
    
    #Draws the starting position of the Arena
    drawArena()
    drawPaddle(paddle1)



    pygame.mouse.set_visible(0) # make cursor invisible

    while True: #main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                print "Good Night!"
                #sys.exit()
        if SPTruVal < Threshold:  
                b.rect.y	=  b.rect.y - 1#(WINDOWHEIGHT - PADDLESIZE)
        elif SPTruVal >= Threshold:
            b.rect.y = b.rect.y + 1
			
			
			
        
        drawArena()
        drawSprite(b)
        #drawPaddle(paddle1)

        score = checkPointScored(paddle1, score)#paddle1, ball, score, ballDirX)
 

        displayScore(score)
        displaySPTruVal(round(SPTruVal,3))

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()
	
