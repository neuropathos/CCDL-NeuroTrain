import pygame, sys
from pygame.locals import *
import time
from random import randrange #for starfield
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
stdev = .5

 
MAX_STARS  = 100
STAR_SPEED = 1
 
def init_stars(DISPLAYSURF):
  """ Create the starfield """
  global stars
  stars = []
  for i in range(MAX_STARS):
    # A star is represented as a list with this format: [X,Y]
    star = [randrange(0,WINDOWWIDTH-500),
            randrange(0,WINDOWHEIGHT - 1)]
    stars.append(star)

    

def move_and_draw_stars(DISPLAYSURF):
  """ Move and draw the stars in the given screen """
  global stars
  for star in stars:
    star[0] -= STAR_SPEED
    # If the star hit the bottom border then we reposition
    # it in the top of the screen with a random X coordinate.
    if star[0] <= 1:
      star[0] = WINDOWWIDTH-500
      star[1] = randrange(0,WINDOWHEIGHT)
    #pygame.draw.rect(DISPLAYSURF, WHITE,(star,(2,2)) )
    DISPLAYSURF.set_at(star,(255,255,255))


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
YELLOW    = (255,255,0)
ORANGE    = (255,165,0)
RED       = (255,0,0)

#Draws the arena the game will be played in. 
def drawArena():
    DISPLAYSURF.fill((0,0,0))
    #Draw outline of arena
    pygame.draw.rect(DISPLAYSURF, WHITE, ((0,0),(WINDOWWIDTH,WINDOWHEIGHT)), LINETHICKNESS*2)
    pygame.draw.line(DISPLAYSURF, WHITE, ((WINDOWWIDTH-500),0),((WINDOWWIDTH-500),WINDOWHEIGHT), (LINETHICKNESS*2))
    
#Draws the bar for high frequency noise
def drawHighFreq():
    pygame.draw.rect(DISPLAYSURF, ORANGE,((WINDOWWIDTH-325,400),(150,-200)) )
    pygame.draw.rect(DISPLAYSURF, WHITE, ((WINDOWWIDTH-325,100),(150,300)), int(LINETHICKNESS*.5))

    
def drawLoFreq():
    pygame.draw.rect(DISPLAYSURF, RED,((WINDOWWIDTH-325,800),(150,-200)) )
    pygame.draw.rect(DISPLAYSURF, WHITE, ((WINDOWWIDTH-325,500),(150,300)), int(LINETHICKNESS*.5))


    
def drawcircle(): #this is the outline of the threshold.
    pygame.draw.circle(DISPLAYSURF, YELLOW, [WINDOWWIDTH/2-200, WINDOWHEIGHT/2], WINDOWHEIGHT/8, 5)

def drawpowercircle(): #this reflects actual NFT correlates; The fourth index in circle is the radius.  
    multiplier = (SPTruVal-Threshold)/stdev         #This means, look at the current number of standard deviations from baseline
    if multiplier > 2:  #no more than 2 standard deviations allowed.
        multiplier = 2
    if multiplier < -2:
        multiplier = -2
    multiplier = (2.5+multiplier)/2.5
    
    circlerad = int(round((WINDOWHEIGHT/8)*multiplier))
    pygame.draw.circle(DISPLAYSURF, WHITE, [WINDOWWIDTH/2-200, WINDOWHEIGHT/2], circlerad)
#Let's make the minimum circle size WINDOWHEIGHT/16 and the maximum WINDOWHEIGHT/4

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

#draws a sprite
def drawSprite(b):  
    if b.rect.bottom > WINDOWHEIGHT - LINETHICKNESS:
        b.rect.bottom = WINDOWHEIGHT - LINETHICKNESS
    #Stops paddle moving too high
    elif b.rect.top < LINETHICKNESS:
        b.rect.top = LINETHICKNESS
    DISPLAYSURF.blit(b.image, b.rect)





#Checks to see if a point has been scored returns new score
def checkPointScored(score): # paddle1, ball, score, ballDirX):

    if 1 == 2:
        a = true
    else: return score



#Displays the current score on the screen 
def displayScore(score):
    resultSurf = SCOREFONT.render('Score = %s' %(score), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (650, 40)
    DISPLAYSURF.blit(resultSurf, resultRect)
	
#Displays the Electrode Value on the screen  for debugging
def displaySPTruVal(SPTruVal):
    resultSurf = BASICFONT.render('TBR = %s' %(SPTruVal), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 300, 25)
    DISPLAYSURF.blit(resultSurf, resultRect)

#Main function
def main():
    pygame.init()
    global DISPLAYSURF
    ##Font information
    global BASICFONT, BASICFONTSIZE
    global SCOREFONTSIZE, SCOREFONT
    BASICFONTSIZE = 20
    SCOREFONTSIZE = 40 
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    SCOREFONT = pygame.font.Font('freesansbold.ttf', SCOREFONTSIZE)
    quittingtime = False

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT)) 
    pygame.display.set_caption('Pong')
    init_stars(DISPLAYSURF)      #STARS
    
    
    #Initiate variable and set starting positions
    
    score = 0
    print(Threshold)
    print(stdev)
    


    #Creates sprite.
    
    b = pygame.sprite.Sprite() # create sprite
    b.image = pygame.image.load("Glider.png").convert_alpha() # load ball image
    #b.image.convert_alpha()
    b.rect = b.image.get_rect() # use image extent values
    b.rect.topleft = [WINDOWWIDTH/2-300, WINDOWHEIGHT/2] # put the image in the top left corner
    print(b.rect.y)
    
    #Draws the starting position of the Arena
    drawArena()
    drawcircle()
    drawHighFreq()
    drawLoFreq()
    
    pygame.mouse.set_visible(0) # make cursor invisible

    while True: #main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quittingtime = True
                break
        if SPTruVal < Threshold:  
                b.rect.y	=  b.rect.y - 1#(WINDOWHEIGHT - PADDLESIZE)
        elif SPTruVal >= Threshold:
            b.rect.y = b.rect.y + 1
        if quittingtime == True:
            break
            
        
        
        drawArena()
        

        drawHighFreq()
        drawLoFreq()
        
        score = checkPointScored(score)#paddle1, ball, score, ballDirX)
 

        displayScore(score)
        displaySPTruVal(round(SPTruVal,3))
        
        
        
        move_and_draw_stars(DISPLAYSURF)
        #drawcircle()
        #drawpowercircle()
        drawSprite(b)
        pygame.display.flip() #STARS

        pygame.display.update()
        
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()
	
