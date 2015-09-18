import pygame, sys
from pygame.locals import *
import numpy as np
import time
from random import randrange #for starfield, random number generator



# Number of frames per second
# Change this value to speed up or slow down your game
FPS = 50


initialization = time.time() + 15 #5 seconds are needed for the data stream to connect properly.

pygame.display.init()      
disp = pygame.display.Info()
WINDOWWIDTH = disp.current_w - 50   #I like the screen slightly smaller than window size for ease of portability
WINDOWHEIGHT = disp.current_h -100
size = [WINDOWWIDTH,WINDOWHEIGHT]

#DEBUG Defaults  (These generally are fed to Png.py from NeuroTrainer.py; if you run Png.py alone, these values are used.

stdev = 0.5         #DEBUG default for stdev of target Hz baseline data
HiDev = 0.5         #DEBUG default for stdev of Hi noise freq baseline data
LoDev = 0.5         #DEBUG default for stdev of Lo noise freq baseline data
Threshold = 1.0     #EEG threshold for changing NFT parameter
HiNoise = 1.0       #High amplitude noise amplitude; Dummy value for the electrode
LoNoise = 1.0       #Low amplitude noise; Dummy value for the electrode
SPTruVal = 0        #Signal amplitude; Dummy value for the electrode

#The number of pixels the line functions used in this game is, by default
LINETHICKNESS = 10  

#Initialize the sound engine then load a sound
pygame.mixer.init()
coin = pygame.mixer.Sound('mariocoin.wav')

#Stars Parameters
MAX_STARS  = 100
STAR_SPEED = 1
stage = 0;

# Set up the colours (RGB values)
BLACK     = (0  ,0  ,0  )
WHITE     = (255,255,255)
YELLOW    = (255,255,0)
ORANGE    = (255,165,0)
RED       = (255,0,0)

#Baselining variable declarations; dummy values
output = 0
HiOutput = 0
LoOutput = 0
consolidatedoutput = []
consolidatedhi = []
consolidatedlo = []


#This is both the initial prompt and the breaks between blocks 
def Pausepoint(stage, score):

    #Black out everything on the screen
    DISPLAYSURF.fill(BLACK)
    
    # I kind of did a hack job here, but basically this sets up the screen display for each stage.
    if stage == 0:
        if time.time() < initialization: #if I don't make a 5 scond delay, things go funny
            resultSurf = SCOREFONT.render('PLEASE WAIT WHILE INITIALIZING', True, WHITE)
        else:
            resultSurf = SCOREFONT.render('PRESS SPACE TO BEGIN BASELINE', True, WHITE)
    if stage == 1:
        resultSurf = SCOREFONT.render('PRESS SPACE TO BEGIN STAGE 1', True, WHITE)
    if stage == 2:
        resultSurf = SCOREFONT.render('PRESS SPACE TO BEGIN STAGE 2', True, WHITE)
    if stage == 3:
        resultSurf = SCOREFONT.render('PRESS SPACE TO BEGIN STAGE 3', True, WHITE)
    if stage == 4:
        resultSurf = SCOREFONT.render('PRESS SPACE TO BEGIN STAGE 4', True, WHITE)
    if stage == 5:
        resultSurf = SCOREFONT.render('Five stages have been completed. FINAL BASELINE!', True, WHITE)
    if stage == 6:
        resultSurf = SCOREFONT.render('All Done!', True, WHITE)
        
    resultRect = resultSurf.get_rect()
    resultRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2-300)
    DISPLAYSURF.blit(resultSurf, resultRect)

    
#BASELINE MODULE
def fixation(recordtick):

    #declare some variables as global here
    # global output   #Threshold for signal data
    # global HiOutput #High Frequency noise threshold
    # global LoOutput #Low Frequency noise threshold
    # global deviance #Standard deviation of signal data; probably not needed
    # global HiDev    #Standard deviation of hi freq noise;
    # global LoDev    #Standard deviation of lo freq noise;
    print(HiNoise, LoNoise, SPTruVal)
    #Clear the screen
    DISPLAYSURF.fill(BLACK)
    
    #Draw the reticle
    pygame.draw.line(DISPLAYSURF, WHITE, ((WINDOWWIDTH/2), 10+WINDOWHEIGHT/2),((WINDOWWIDTH/2),WINDOWHEIGHT/2-10), (LINETHICKNESS/2))
    pygame.draw.line(DISPLAYSURF, WHITE, ((10+WINDOWWIDTH/2),WINDOWHEIGHT/2),((WINDOWWIDTH/2 - 10),WINDOWHEIGHT/2), (LINETHICKNESS/2))
    
    #Fill up the baselining array until time runs out
    if time.time() >= recordtick: 
        recordtick = time.time()+.25  #This collects data every 250 ms.  Lower this number for higher resolution
        consolidatedoutput.append(SPTruVal)
        output = sum(consolidatedoutput)/len(consolidatedoutput)
        deviance = np.std(consolidatedoutput)
        
        #Calculate high freq noise and deviation
        consolidatedhi.append(HiNoise)
        HiOutput = sum(consolidatedhi)/len(consolidatedhi)
        HiDev = np.std(consolidatedhi)
        
        #Calculate low freq noise and deviation
        consolidatedlo.append(LoNoise)
        HiOutput = sum(consolidatedlo)/len(consolidatedlo)
        LoDev = np.std(consolidatedlo)
 
 
#Draws the bar for high frequency noise
def drawHighFreq():

    #We create a scale where the ceiling is +2 stdev, and the floor is -2 stdev
    highmark = HiOutput + HiDev*2
    lowmark = HiOutput - HiDev*2
    
    #We scale the current frame's Hi Freq noise value by subtracting the lowmark baseline
    scaledHi = HiNoise - lowmark
    
    #We must not exceed the ceiling or the floor; and if we don't, we scale the value as a value between 1 and 0.
    if scaledHi < 0:
        scaledHi = 0
    elif scaledHi > highmark - lowmark:
        scaledHi = 1
    else:
        scaledHi = scaledHi/(highmark-lowmark)
        
    #Let's create the scaled high bar; orange if above threshold, white if below.
    if scaledHi >= 0.5:
        pygame.draw.rect(DISPLAYSURF, ORANGE,((WINDOWWIDTH-325,400),(150,-300*scaledHi)) )
    else:
        pygame.draw.rect(DISPLAYSURF, WHITE,((WINDOWWIDTH-325,400),(150,-300*scaledHi)) )
    
    #This draws the "container" for the bar (in white), and the midmark (in orange). 
    pygame.draw.line(DISPLAYSURF, ORANGE, ((WINDOWWIDTH-325), 250),((WINDOWWIDTH-175), 250), (LINETHICKNESS/5))    
    pygame.draw.rect(DISPLAYSURF, WHITE, ((WINDOWWIDTH-325,100),(150,300)), int(LINETHICKNESS*.5))

    
#Draws the bar for low frequency noise
def drawLoFreq():

    #We create a scale where the ceiling is +2 stdev, and the floor is -2 stdev
    highmark = LoOutput + LoDev*2
    lowmark = LoOutput - LoDev*2
    
    #We scale the current frame's Low Freq noise value by subtracting the lowmark as a baseline
    scaledLo = LoNoise - lowmark
    
    #We must not exceed the ceiling or the floor; and if we don't, we scale the value between 1 and 0.
    if scaledLo < 0:
        scaledLo = 0
    elif scaledLo > highmark - lowmark:
        scaledLo = 1
    else:
        scaledLo = scaledLo/(highmark-lowmark)
        
    #Let's create the scaled high bar; red if above threshold, white if below.
    if scaledLo >= 0.5:
        pygame.draw.rect(DISPLAYSURF, RED,((WINDOWWIDTH-325,800),(150,-300*scaledLo)) )
    else:
        pygame.draw.rect(DISPLAYSURF, WHITE,((WINDOWWIDTH-325,800),(150,-300*scaledLo)) )
    
    #This draws the "container" for the bar (in white), and the midmark (in red). 
    pygame.draw.line(DISPLAYSURF, RED, ((WINDOWWIDTH-325), 650),((WINDOWWIDTH-175), 650), (LINETHICKNESS/5))    
    pygame.draw.rect(DISPLAYSURF, WHITE, ((WINDOWWIDTH-325,500),(150,300)), int(LINETHICKNESS*.5))
 
 
 # this sets up the starting point for the stars
def init_stars(DISPLAYSURF):
  """ Create the starfield """
  global stars
  stars = []
  for i in range(MAX_STARS):
    # A star is represented as a list with this format: [X,Y]
    star = [randrange(0,WINDOWWIDTH-500),
            randrange(0,WINDOWHEIGHT - 1)]
    stars.append(star)

    
#This moves the stars incrementally in each game frame;
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


#Draws the arena the game will be played in. 
def drawArena():
    DISPLAYSURF.fill((0,0,0))
    #Draw outline of arena
    pygame.draw.rect(DISPLAYSURF, WHITE, ((0,0),(WINDOWWIDTH,WINDOWHEIGHT)), LINETHICKNESS*2)
    pygame.draw.line(DISPLAYSURF, WHITE, ((WINDOWWIDTH-500),0),((WINDOWWIDTH-500),WINDOWHEIGHT), (LINETHICKNESS*2))

    



#This is code for the circle paradigm's threshold marker; not being used at present.
def drawcircle(): #this is the outline of the threshold.
    pygame.draw.circle(DISPLAYSURF, YELLOW, [WINDOWWIDTH/2-200, WINDOWHEIGHT/2], WINDOWHEIGHT/8, 5)


#This code makes the circle which reflects actual EEG power
def drawpowercircle(): #this reflects actual NFT correlates; The fourth index in circle is the radius.  
    multiplier = (SPTruVal-Threshold)/stdev         #This means, look at the current number of standard deviations from baseline
    if multiplier > 2:  #no more than 2 standard deviations allowed.
        multiplier = 2
    if multiplier < -2:
        multiplier = -2
    multiplier = (2.5+multiplier)/2.5
    
    circlerad = int(round((WINDOWHEIGHT/8)*multiplier))
    pygame.draw.circle(DISPLAYSURF, WHITE, [WINDOWWIDTH/2-200, WINDOWHEIGHT/2], circlerad)


#draws a sprite
def drawSprite(b):  
    #Stops it from going too low
    if b.rect.bottom > WINDOWHEIGHT - LINETHICKNESS - 150:
        b.rect.bottom = WINDOWHEIGHT - LINETHICKNESS -150
    #Stops paddle moving too high 
    elif b.rect.top < LINETHICKNESS + 150:
        b.rect.top = LINETHICKNESS + 150
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
    global stage
    global consolidatedoutput
    global HiOutput
    global LoOutput
    BASICFONTSIZE = 20
    SCOREFONTSIZE = 40 
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    SCOREFONT = pygame.font.Font('freesansbold.ttf', SCOREFONTSIZE)

    
    # Flags for whether to quit or pause; starts paused.
    quittingtime = False 
    pausetime = True

    
    #Initialize the pygame FPS clock
    FPSCLOCK = pygame.time.Clock()
    
    
    #Set the size of the screen and label it
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT)) 
    pygame.display.set_caption('NeuroFeedback')
    
    
    #Start with 0 points
    score = 0
    

    #Creates sprites and stars.
    init_stars(DISPLAYSURF)             # *~STARS~*
    b = pygame.sprite.Sprite()          # define parameters of glider sprite
    b.image = pygame.image.load("Glider.png").convert_alpha() # Load the glider sprite
    b.rect = b.image.get_rect() # use image extent values
    b.rect.topleft = [WINDOWWIDTH/2-300, WINDOWHEIGHT/2] # put the image in the center of the player window
   
   
    # make mouse cursor invisible
    pygame.mouse.set_visible(0) 

    
    #Let the games (loop) begin!
    while True: 
        #Processes game events like quitting or keypresses
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quittingtime = True
                break
                
            #This portion does keypresses
            if event.type == pygame.KEYDOWN:  #press space to terminate pauses between blocs
                if event.key == pygame.K_SPACE:
                    if pausetime == True:
                         pausetime = False
                         countdown = time.time() + 300 #This is the number of seconds in a Glider game block

                         #This is for the baselining stages at the beginning and end
                         if stage == 0 or stage == 5:
                            countdown = time.time() + 1.80 #Number of seconds for Baseline block
                            recordtick = time.time()+.25   #Collecting values at a 250 ms interval; decrease to up sampling rate

                         stage = stage + 1 # time to go to the next stage
        
       
        #needed to exit the program gracefully
        if quittingtime == True:    
                break
                
        
        
        #If the game is at a pausing point, such as the beginning screen
        if pausetime == True:
            Pausepoint(stage, score)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            continue
        
        #If the countdown timer reaches zero
        if time.time() > countdown:  
            if stage == 1 or stage == 6:
                print("The subject's Data Baseline is:")
                output = sum(consolidatedoutput)/len(consolidatedoutput)
                print(output)
                print("With a standard deviation of:")
                deviance = np.std(consolidatedoutput)
                print(deviance)
                
                print("The subject's High Noise Baseline is:")
                HiOutput = sum(consolidatedhi)/len(consolidatedhi)
                print(HiOutput)
                print("With a standard deviation of:")
                HiDev = np.std(consolidatedhi)
                print(HiDev)
                
                print("The subject's Low Noise Baseline is:")
                LoOutput = sum(consolidatedlo)/len(consolidatedlo)
                print(LoOutput)
                print("With a standard deviation of:")
                LoDev = np.std(consolidatedlo)
                print(LoDev)
                
            pausetime = True
            b.rect.y = WINDOWHEIGHT/2
            continue
        
        #baselining at stages 1 and 6
        if stage == 1 or stage == 6:
            fixation(recordtick)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            continue

        #Final exit after last stage  
        if stage == 7:
            pygame.quit()
            print("Game over, man.  Game over.")
            quittingtime = True
            break
            
        #Let's make the stage 
        drawArena()
            
            
        #This moves our glider in accordance with the thresholds 
        if SPTruVal > Threshold:  
                b.rect.y	=  b.rect.y - 1
        elif SPTruVal <= Threshold:
            b.rect.y = b.rect.y + 1
            

        #This draws the bar graphs for high and low band noises
        drawHighFreq()
        drawLoFreq()
        
        
        #This determines whether a point should be awarded
        score = checkPointScored(score)#paddle1, ball, score, ballDirX)
 
        #Prints the score and the current electrode power on-screen
        displayScore(score)
        displaySPTruVal(round(SPTruVal,3))
        
        
        #draws the ~*STARS*~
        move_and_draw_stars(DISPLAYSURF)
        #drawcircle()       #dummied out circle code
        #drawpowercircle()
        
        #Final draws and screen update
        drawSprite(b) #Draws the glider in his new position
        pygame.display.flip() #needed to draw the >|<~STARS~>|<
        pygame.display.update() #Refresh all the details that do not fall under the "flip" method. SP NOTE: I don't understand the difference very well.
        
        FPSCLOCK.tick(FPS) #Tells the game system that it is not untouched by the inexorable march of time

if __name__=='__main__':
    main()
	
