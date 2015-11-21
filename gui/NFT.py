import pygame, sys
from pygame.locals import *
import numpy as np
import time
from random import randrange #for starfield, random number generator
print("Initializing the Neurofeedback Paradigm...")

#For debugging NFT; is updated live by visualizer.py.
DISCONNECT = False
LastDISCONNECT = False  #so current and previous states can be compared


# Number of frames per second
# Change this value to speed up or slow down your game
FPS = 50



#Funny variable
CustomName = False

#The default filename for the NFT paradigm:
OutputFilename = 'NFT_MetaData.csv'
ExperimentOutputName = 'NFT_ContRec.csv'

#This is for whether a file is being used for the subject's condition.
ControlRecording = False

pygame.display.init()      
disp = pygame.display.Info()
WINDOWWIDTH = disp.current_w    #I like the screen slightly smaller than window size for ease of portability
WINDOWHEIGHT = disp.current_h
size = [WINDOWWIDTH,WINDOWHEIGHT]

#DEBUG Defaults  (These generally are fed to Png.py from NeuroTrainer.py; if you run Png.py alone, these values are used.

deviance = 0.5         #DEBUG default for stdev of target Hz baseline data
HiDev = 0.5         #DEBUG default for stdev of Hi noise freq baseline data
LoDev = 0.5         #DEBUG default for stdev of Lo noise freq baseline data
Threshold = 1.0     #EEG threshold for changing NFT parameter
HiNoise = 1.0       #High amplitude noise amplitude; Dummy value for the electrode
LoNoise = 1.0       #Low amplitude noise; Dummy value for the electrode
TargetVal = 0        #Signal amplitude; Dummy value for the electrode
SPTruVal = 0        #Value that gets exported from the visualizer
successjar = 0
CONTROL = False     #This decides whether this running of the experiment is real or not.

#These are the time intervals for the training in seconds.
BlocInterval = 300    #300
FixationInterval = 189 #180 #This is extended by 8 seconds as a bandaid solution to the fact that 

#Flags for high and low noise; false until noise thresholds are passed.
HighNoiseFlag = False
LowNoiseFlag = False


resultsarray = []
NEXT = False

#Timers and flags for continual success scoring
FirstSuccessTimer = time.time()
FirstSuccessFlag = False
ContinualSuccessFlag = False
ContinualSuccessTimer = time.time()

#The number of pixels in pygame line functions, by default
LINETHICKNESS = 10  

#Initialize the sound engine then load a sound
pygame.mixer.init()
coin = pygame.mixer.Sound('mariocoin.wav')

#Stars Parameters
MAX_STARS  = 200
STAR_SPEED = 1
stage = 0;

# Set up the colours (RGB values)
BLACK     = (0  ,0  ,0  )
GREY      = (120  ,120  ,120  )
WHITE     = (255,255,255)
YELLOW    = (255,255,0)
ORANGE    = (255,165,0)
RED       = (255,0,0)
TURQUOISE = ( 52, 221, 221)
#Baselining variable declarations; dummy values
output = 0
HiOutput = 0
LoOutput = 0
consolidatedoutput = []
consolidatedhi = []
consolidatedlo = []


#This is both the initial prompt and the breaks between blocks 
def Pausepoint(stage, score):

    #These are scores we want to keep

    global score1
    global score2
    global score3
    global score4
    global ontimer
    global ontime
    global successflag
    global successjar
    global Level
    global remainder
    global ControlRecording
    
    
    #Black out everything on the screen
    DISPLAYSURF.fill(BLACK)
    
    
    if stage == 0:
        if time.time() < initialization: #if I don't make a 5 scond delay, things go funny
            resultSurf = SCOREFONT.render('PLEASE WAIT WHILE INITIALIZING', True, ORANGE)
        else:
            if CONTROL == True or ControlRecording == True: resultSurf = SCOREFONT.render('START RECORDING TO BEGIN BASELINE', True, RED)
            else: resultSurf = SCOREFONT.render('START RECORDING TO BEGIN BASELINE', True, TURQUOISE)
    if stage == 1:
        resultSurf = SCOREFONT.render('PRESS SPACE TO BEGIN STAGE 1', True, WHITE)
    if stage == 2:
        score1 = score
        resultSurf = SCOREFONT.render('PRESS SPACE TO BEGIN STAGE 2', True, WHITE)
    if stage == 3:
        score2 = score
        resultSurf = SCOREFONT.render('PRESS SPACE TO BEGIN STAGE 3', True, WHITE)
    if stage == 4:
        score3 = score
        resultSurf = SCOREFONT.render('PRESS SPACE TO BEGIN STAGE 4', True, WHITE)
    if stage == 5:
        score4 = score
        resultSurf = SCOREFONT.render('Five stages have been completed. FINAL BASELINE!', True, WHITE)
    if stage == 6:
        resultSurf = SCOREFONT.render('All Done!', True, WHITE)

        
    resultRect = resultSurf.get_rect()
    resultRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2-300)
    DISPLAYSURF.blit(resultSurf, resultRect)
    

    
        
    # this sets up the screen display for each stage. (could probably be tidied up better)
    
    if stage != 0:
        #Draw the grid 
        pygame.draw.rect(DISPLAYSURF, WHITE, ((WINDOWWIDTH/2+300,WINDOWHEIGHT/2+200),(-600,-400)), LINETHICKNESS)
        #screen width interval is 100; 
        
        #latitude lines
        latitudes = 8 #This is the number of times to split latitudinally
        for i in range(0, latitudes):
            pygame.draw.line(DISPLAYSURF, WHITE, ((WINDOWWIDTH/2+300),WINDOWHEIGHT/2+200-int(i*400/latitudes)),((WINDOWWIDTH/2-300),WINDOWHEIGHT/2+200-int(i*400/latitudes)), int(LINETHICKNESS*.2))
            
            increment = 20
            resultSurf = BASICFONT.render(str(i*increment), True, WHITE)
            resultRect = resultSurf.get_rect()
            resultRect.center = (WINDOWWIDTH/2-330, (WINDOWHEIGHT/2+202-int(i*400/latitudes)))
            DISPLAYSURF.blit(resultSurf, resultRect)
        
        #Display the longitude lines and labels
        for i in range(0, 4):        
            resultSurf = BASICFONT.render("Trial " + str(i+1), True, WHITE)
            resultRect = resultSurf.get_rect()
            resultRect.center = (WINDOWWIDTH/2-220+(i*150), WINDOWHEIGHT/2+250)
            DISPLAYSURF.blit(resultSurf, resultRect)
            if i == 3: continue #We only need 3 lines
            pygame.draw.line(DISPLAYSURF, WHITE, ((WINDOWWIDTH/2-150+i*150),WINDOWHEIGHT/2+200),((WINDOWWIDTH/2-150+i*150),WINDOWHEIGHT/2-200), int(LINETHICKNESS*.2))        

      
        
        if stage >= 2:
            pygame.draw.circle(DISPLAYSURF, RED, [WINDOWWIDTH/2 - 225, WINDOWHEIGHT/2+200-int(float(score1)/float(increment)*50)], 8) #tie Windowheight to score

            
            resultSurf = BASICFONT.render('%s Points' %(score1), True, YELLOW)
            resultRect = resultSurf.get_rect()
            resultRect.center = (WINDOWWIDTH/2-220, WINDOWHEIGHT/2+275)
            DISPLAYSURF.blit(resultSurf, resultRect)
        if stage >= 3:
            pygame.draw.circle(DISPLAYSURF, RED, [WINDOWWIDTH/2 - 75, WINDOWHEIGHT/2+200-int(float(score2)/float(increment)*50)], 8)
            pygame.draw.line(DISPLAYSURF, RED, ((WINDOWWIDTH/2-225),WINDOWHEIGHT/2+200-int(float(score1)/float(increment)*50)),((WINDOWWIDTH/2-75),WINDOWHEIGHT/2+200-int(float(score2)/float(increment)*50)), int(LINETHICKNESS*0.3)) #ie line height to previous circle
            
            resultSurf = BASICFONT.render('%s Points' %(score2), True, YELLOW)
            resultRect = resultSurf.get_rect()
            resultRect.center = (WINDOWWIDTH/2-70, WINDOWHEIGHT/2+275)
            DISPLAYSURF.blit(resultSurf, resultRect)

            
        if stage >= 4:
            pygame.draw.circle(DISPLAYSURF, RED, [WINDOWWIDTH/2 + 75, WINDOWHEIGHT/2+200-int(float(score3)/float(increment)*50)], 8)
            pygame.draw.line(DISPLAYSURF, RED, ((WINDOWWIDTH/2-75),WINDOWHEIGHT/2+200-int(float(score2)/float(increment)*50)),((WINDOWWIDTH/2 + 75),WINDOWHEIGHT/2+200-int(float(score3)/float(increment)*50)), int(LINETHICKNESS*0.3))

            resultSurf = BASICFONT.render('%s Points' %(score3), True, YELLOW)
            resultRect = resultSurf.get_rect()
            resultRect.center = (WINDOWWIDTH/2 + 80, WINDOWHEIGHT/2+275)
            DISPLAYSURF.blit(resultSurf, resultRect)

        if stage >= 5:
            pygame.draw.line(DISPLAYSURF, RED, ((WINDOWWIDTH/2 + 75),WINDOWHEIGHT/2+200-int(float(score3)/float(increment)*50)),((WINDOWWIDTH/2 + 225),WINDOWHEIGHT/2+200-int(float(score4)/float(increment)*50)), int(LINETHICKNESS*0.3))
            pygame.draw.circle(DISPLAYSURF, RED, [WINDOWWIDTH/2 + 225, WINDOWHEIGHT/2+200-int(float(score4)/float(increment)*50)], 8)
            
            resultSurf = BASICFONT.render('%s Points' %(score4), True, YELLOW)
            resultRect = resultSurf.get_rect()
            resultRect.center = (WINDOWWIDTH/2 + 220, WINDOWHEIGHT/2+275)
            DISPLAYSURF.blit(resultSurf, resultRect)
        
        if stage == 2 or stage == 3 or stage == 4 or stage == 5:
            displayedlevel = Level
			
            # if ontime/BlocInterval > .6:
                # displayedlevel = displayedlevel + 1

                # resultSurf = SCOREFONT.render('LEVEL UP', True,  TURQUOISE)
                # resultRect = resultSurf.get_rect()
                # resultRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2-250)
                # DISPLAYSURF.blit(resultSurf, resultRect)
            # elif ontime/BlocInterval < .2:
                # displayedlevel = displayedlevel - 1
                # resultSurf = SCOREFONT.render('LEVEL DOWN', True, ORANGE)
                # resultRect = resultSurf.get_rect()
                # resultRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2-250)
                # DISPLAYSURF.blit(resultSurf, resultRect)
                #This announces difficulty
    return score

    
#BASELINE MODULE
def fixation(recordtick):
    global consolidatedoutput
    global consolidatedhi
    global consolidatedlo

    #Clear the screen
    DISPLAYSURF.fill(BLACK)
    
    #Draw the reticle
    pygame.draw.line(DISPLAYSURF, GREY, ((WINDOWWIDTH/2), 10+WINDOWHEIGHT/2),((WINDOWWIDTH/2),WINDOWHEIGHT/2-10), (LINETHICKNESS/2))
    pygame.draw.line(DISPLAYSURF, GREY, ((10+WINDOWWIDTH/2),WINDOWHEIGHT/2),((WINDOWWIDTH/2 - 10),WINDOWHEIGHT/2), (LINETHICKNESS/2))
    
    #Fill up the baselining array until time runs out
    if time.time() >= recordtick: 
        recordtick = time.time()+.25  #This collects data every 250 ms.  Lower this number for higher resolution
        consolidatedoutput.append(TargetVal)
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
    global HighNoiseFlag
    #We create a scale where the ceiling is +2 stdev, and the floor is -2 stdev; MODIFIED TO BE EASIER
    highmark = HiOutput + HiDev*8
    lowmark = HiOutput - HiDev*1
    
    #We scale the current frame's Hi Freq noise value by subtracting the lowmark baseline
    scaledHi = HiNoise - lowmark
    
    #We must not exceed the ceiling or the floor; and if we don't, we scale the value as a value between 1 and 0.
    if scaledHi < .1:
        scaledHi = .1
    elif scaledHi > highmark - lowmark:
        scaledHi = 1
    else:
        scaledHi = scaledHi/(highmark-lowmark)
        
    #Let's create the scaled high bar; orange if above threshold, white if below.
    if scaledHi >= 0.5:
        pygame.draw.rect(DISPLAYSURF, ORANGE,((WINDOWWIDTH-324,WINDOWHEIGHT/2-50),(150,-300*scaledHi)) )
        HighNoiseFlag = True
    else:
        pygame.draw.rect(DISPLAYSURF, WHITE,((WINDOWWIDTH-324,WINDOWHEIGHT/2-50),(150,-300*scaledHi)) )
        HighNoiseFlag = False
    
    #This draws the "container" for the bar (in white), and the midmark (in orange). 
    pygame.draw.line(DISPLAYSURF, ORANGE, ((WINDOWWIDTH-324), WINDOWHEIGHT/2-200),((WINDOWWIDTH-175), WINDOWHEIGHT/2-200), (LINETHICKNESS/5))    
    pygame.draw.rect(DISPLAYSURF, WHITE, ((WINDOWWIDTH-324,WINDOWHEIGHT/2-350),(150,300)), int(LINETHICKNESS*.5))


#Draws the bar for low frequency noise
def drawLoFreq():
    global LowNoiseFlag
    #We create a scale where the ceiling is +2 stdev, and the floor is -2 stdev
    highmark = LoOutput + LoDev*8
    lowmark = LoOutput - LoDev*1
    
    #We scale the current frame's Low Freq noise value by subtracting the lowmark as a baseline
    scaledLo = LoNoise - lowmark
    
    #We must not exceed the ceiling or the floor; and if we don't, we scale the value between 1 and 0.
    if scaledLo < .1:
        scaledLo = .1
    elif scaledLo > highmark - lowmark:
        scaledLo = 1
    else:
        scaledLo = scaledLo/(highmark-lowmark)
        
    #Let's create the scaled high bar; red if above threshold, white if below.
    if scaledLo >= 0.5:
        LowNoiseFlag = True
        pygame.draw.rect(DISPLAYSURF, RED,((WINDOWWIDTH-324,WINDOWHEIGHT/2 + 350),(150,-300*scaledLo)) )
    else:
        pygame.draw.rect(DISPLAYSURF, WHITE,((WINDOWWIDTH-324,WINDOWHEIGHT/2 + 350),(150,-300*scaledLo)) )
        LowNoiseFlag = False
    
    #This draws the "container" for the bar (in white), and the midmark (in red). 
    pygame.draw.line(DISPLAYSURF, RED, ((WINDOWWIDTH-324), WINDOWHEIGHT/2+200),((WINDOWWIDTH-175), WINDOWHEIGHT/2+200), (LINETHICKNESS/5))    
    pygame.draw.rect(DISPLAYSURF, WHITE, ((WINDOWWIDTH-324,WINDOWHEIGHT/2 + 50),(150,300)), int(LINETHICKNESS*.5))
 
 
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
def move_and_draw_stars(DISPLAYSURF, b):
  """ Move and draw the stars in the given screen """
  global stars
  for star in stars:
    star[0] -= STAR_SPEED
    if b.rect.bottom > WINDOWHEIGHT - LINETHICKNESS - 150:
        star[1] -= STAR_SPEED
    if b.rect.top < LINETHICKNESS + 150:
        star[1] += STAR_SPEED
    DISPLAYSURF.set_at(star,(255,255,255)) #Turns on the next star position
    # If the star hit the border then we reposition
    # it in the right side of the screen with a random Y coordinate.
    if star[0] <= 1:
      star[0] = WINDOWWIDTH-500
      star[1] = randrange(0,WINDOWHEIGHT)
      
    #In the case of descent  
    if star[1] <= 1:
      star[1] = WINDOWHEIGHT
      star[0] = randrange(1,WINDOWWIDTH-500)
    #In the case of ascent
    elif star[1] >= WINDOWHEIGHT:
      star[1] = 1
      star[0] = randrange(1,WINDOWWIDTH-500)
    
    #Vertical shift for ascent/descent
     #Descent



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
    multiplier = (TargetVal-Threshold)/deviation         #This means, look at the current number of standard deviations from baseline
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
    #Stops sprite moving too high 
    elif b.rect.top < LINETHICKNESS + 150:
        b.rect.top = LINETHICKNESS + 150
    DISPLAYSURF.blit(b.image, b.rect)

    
    

#Checks to see if a point has been scored; returns new score
def checkPointScored(score): # paddle1, ball, score, ballDirX):
    global FirstSuccessTimer
    global FirstSuccessFlag 
    global ContinualSuccessFlag 
    global ContinualSuccessTimer 
    

    #Start by checking for success state

    if TargetVal < Threshold and HighNoiseFlag == False and LowNoiseFlag == False and VoltBaseline < VoltMin + 100 and VoltBaseline > VoltMax - 100:
        if FirstSuccessFlag == False:       #Sees if the first round has begun;this just sets the first timer, really.
            if time.time() > ContinualSuccessTimer: #Make sure previous successes do not allow rapid-fire point generation
                FirstSuccessFlag = True 
                FirstSuccessTimer = time.time() +.25
                
        elif FirstSuccessFlag == True:       
            if ContinualSuccessFlag == False:           #If the first point hasn't been made
                if time.time() > FirstSuccessTimer:      #Have .25 seconds passed?
                    score = score + 1
                    coin.play()                         #Award a point and give a coin!
                    ContinualSuccessTimer = time.time() + 2 #Make the timer 3 seconds forward
                    ContinualSuccessFlag = True            
            else:                                       #read: If at least one point has been scored    
                if time.time() > ContinualSuccessTimer:  #read: if 3 seconds have passed since the first point
                    score = score + 1
                    coin.play()                         #Award a point and give a coin!
                    ContinualSuccessTimer = time.time() + 2 #Make the timer 3 seconds forward
                    ContinualSuccessFlag = True   
    else:
        FirstSuccessFlag = False
        ContinualSuccessFlag = False
       
    return score


#Displays the current score on the screen 
def displayScore(score):
    resultSurf = SCOREFONT.render('Score = %s' %(score), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.center = (WINDOWWIDTH/2-243, 40)
    DISPLAYSURF.blit(resultSurf, resultRect)

	
#Displays debugging stuff; the calling of TargetVal here is kind of an artifact, ignore it I think
def displayDEBUG(TargetVal):
    global VoltMax
    global VoltMin
    global VoltBaseline
    resultSurf = BASICFONT.render('FirstTimer = %s' %(round(FirstSuccessTimer-time.time(),3)), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 300, 25)
    DISPLAYSURF.blit(resultSurf, resultRect)
    resultSurf = BASICFONT.render('ContinuedTimer = %s' %(round(ContinualSuccessTimer-time.time(),3)), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 300, 40)
    DISPLAYSURF.blit(resultSurf, resultRect)
    if FirstSuccessFlag == True:
        resultSurf = BASICFONT.render('Fst+', True, WHITE)
        resultRect = resultSurf.get_rect()
        resultRect.topleft = (WINDOWWIDTH - 300, 55)
        DISPLAYSURF.blit(resultSurf, resultRect)
    if ContinualSuccessFlag == True:
        resultSurf = BASICFONT.render('Cnt+', True, WHITE)
        resultRect = resultSurf.get_rect()
        resultRect.topleft = (WINDOWWIDTH - 375, 55)
        DISPLAYSURF.blit(resultSurf, resultRect)
    if HighNoiseFlag == True:
        resultSurf = BASICFONT.render('hinoi', True, ORANGE)
        resultRect = resultSurf.get_rect()
        resultRect.topleft = (WINDOWWIDTH - 300, 70)
        DISPLAYSURF.blit(resultSurf, resultRect)
    if LowNoiseFlag == True:
        resultSurf = BASICFONT.render('lonoi', True, RED)
        resultRect = resultSurf.get_rect()
        resultRect.topleft = (WINDOWWIDTH - 375, 70)
        DISPLAYSURF.blit(resultSurf, resultRect)  
    resultSurf = BASICFONT.render('LNoi = %s' %(round(LoNoise,1)), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 165, 85)
    DISPLAYSURF.blit(resultSurf, resultRect)
    resultSurf = BASICFONT.render('LNoTh = %s' %(round(LoOutput,1)), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 165, 100)
    DISPLAYSURF.blit(resultSurf, resultRect)
    resultSurf = BASICFONT.render('Lnxt = %s' %(len(consolidatedloNext)), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 165, 115)
    DISPLAYSURF.blit(resultSurf, resultRect)
    
    resultSurf = BASICFONT.render('HNoi = %s' %(round(HiNoise,1)), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 165, 145)
    DISPLAYSURF.blit(resultSurf, resultRect)
    resultSurf = BASICFONT.render('HNoTh = %s' %(round(HiOutput,1)), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 165, 160)
    DISPLAYSURF.blit(resultSurf, resultRect)
    resultSurf = BASICFONT.render('Hnxt = %s' %(len(consolidatedhiNext)), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 165, 175)
    DISPLAYSURF.blit(resultSurf, resultRect)
    
    resultSurf = BASICFONT.render('stage = %s' %(stage), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 165, 190)
    DISPLAYSURF.blit(resultSurf, resultRect)
    
    
    resultSurf = BASICFONT.render('Sign = %s' %(round(TargetVal,3)), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 165, 220)
    DISPLAYSURF.blit(resultSurf, resultRect)
    resultSurf = BASICFONT.render('Thr = %s' %(round(Threshold,1)), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 165, 235)
    DISPLAYSURF.blit(resultSurf, resultRect)
    resultSurf = BASICFONT.render('Snxt = %s' %(len(consolidatedoutputNext)), True, WHITE)
    resultRect = resultSurf.get_rect() 
    resultRect.topleft = (WINDOWWIDTH - 165, 250)
    DISPLAYSURF.blit(resultSurf, resultRect)
    
    resultSurf = BASICFONT.render('oTim = %s' %(round(ontime, 1)), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 165, 280)
    DISPLAYSURF.blit(resultSurf, resultRect)
    
    resultSurf = BASICFONT.render('sJar = %s' %(round(time.time() - successjar, 1)), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 165, 295)
    DISPLAYSURF.blit(resultSurf, resultRect)
    
    resultSurf = BASICFONT.render('Time = %s' %(round(time.time() - countdown, 1)), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 165, 310)
    DISPLAYSURF.blit(resultSurf, resultRect)
    
    resultSurf = BASICFONT.render('VMin = %s' %(round(VoltMin, 1)), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 165, 340)
    DISPLAYSURF.blit(resultSurf, resultRect)
    
    resultSurf = BASICFONT.render('Vmax = %s' %(round(VoltMax, 1)), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 165, 360)
    DISPLAYSURF.blit(resultSurf, resultRect)

    resultSurf = BASICFONT.render('VBas = %s' %(round(VoltBaseline, 1)), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 165, 380)
    DISPLAYSURF.blit(resultSurf, resultRect)

    

    # global  
    # global ContinualSuccessFlag 

#Main function
def main():
    pygame.init()
    
    global DISPLAYSURF
    
    ##Font information
    global BASICFONT, BASICFONTSIZE
    global SCOREFONTSIZE, SCOREFONT
    
    global RecordBypass
    global stage
    global consolidatedoutput 
    global consolidatedhi 
    global consolidatedlo 
    global HiOutput
    global LoOutput
    global initialization
    global Level
    global ontime
    global successflag
    global successtimer
    global successjar
    global Threshold
    global ContinualSuccessTimer
    global FirstSuccessTimer
    global CONTROL
    global TargetVal
    global remainder
    global countdown
    global OutputFilename
    global BlocInterval
    global FixationInterval
    global NEXT
    global ControlRecording
    global CB1
    global C1 
    global CB2
    global C2 
    global CB3
    global C3 
    global CB4
    global C4 
    global VoltMedian
    global VoltMax
    global VoltMin
    global VoltBaseline
    global consolidatedloNext
    global consolidatedhiNext
    global consolidatedoutputNext
    
    #Hopefully this will be read from the recording function at the baseline stages.
    RecordBypass = False

    #This is the period of time the threshold is surpassed, starting at zero:
    ontime = 0
    
    recordtick = 0
    countdown = 0
    
    #For the control period
    ControlIndex = 0
    
    #This opens the files to be written to or read from (in the case of control):
    print('outputfilename is ' + OutputFilename)
    f = open(OutputFilename, 'w') #This should have the custom name plugged in later;
    if ControlRecording == False: ses = open(ExperimentOutputName, 'w' )
    else: 
        #These are the values that will be used for the imitated NFT
        con = open(ControlFile)
        if ControlRecording == True:
        

            CB1 = float((con.readline()[:-1].split(','))[0])
            C1  = (con.readline()[:-1].split(','))
            C1 = [float(i) for i in C1]
            CB2 = float((con.readline()[:-1].split(','))[0])
            C2  = (con.readline()[:-1].split(','))
            C2 = [float(i) for i in C2]
            CB3 = float((con.readline()[:-1].split(','))[0])
            C3  = (con.readline()[:-1].split(','))
            C3 = [float(i) for i in C3]
            CB4 = float((con.readline()[:-1].split(','))[0])
            C4  = (con.readline()[:-1].split(','))
            C4 = [float(i) for i in C4]
            print(CB1)
            print(CB2)
            print(CB3)
            print(CB4)
        
    #5 seconds are needed for the data stream to connect properly.
    initialization = time.time() + 5 
    
    #Initializing the font values
    BASICFONTSIZE = 20
    SCOREFONTSIZE = 40 
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    SCOREFONT = pygame.font.Font('freesansbold.ttf', SCOREFONTSIZE)
    Level = 0 #this is the starting point of threshold challenge.
    
    #These are dummy values for voltage based thresholds.
    VoltMax = 1001
    VoltMedian = 1000
    VoltMin = 999
    VoltBaseline = 1000
    VoltMedianArrayNext = []
    
    #When reading from the control, this time mark will be used for a timing function:
    ControlTimer = time.time() +.25    
    

    
    # Flags for whether to quit or pause; starts paused.
    quittingtime = False 
    pausetime = True
    Disconnect = False
    LastDISCONNECT = False
    
    #This is used in counting success time; the "success time" counter goes forward only if this is true
    successflag = False
    
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
    b.rect.center = [WINDOWWIDTH/2-243, WINDOWHEIGHT/2] # put the image in the center of the player window
   
   
    # make mouse cursor invisible
    pygame.mouse.set_visible(0) 

    
    #Let the games (loop) begin!
    while True:
        #Checks if the headset is connected
        #When disconnect first happens:



        #Processes game events like quitting or keypresses
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                f.close()
                if ControlRecording == False: ses.close()
                else: con.close()
                quittingtime = True
                break
                
            #This portion does keypresses
            if event.type == pygame.KEYDOWN:  #press space to terminate pauses between blocs
                if event.key == pygame.K_SPACE:
                    if pausetime == True and stage != 5:
                        pausetime = False
                        NEXT == False
                        RecordBypass = False #Likely unnecessary, but I'm playing it safe for now.
                        
                        ontime = 0             #This sets the beginning period of time to zero
                        countdown = time.time() + BlocInterval #This is the number of seconds in a Glider game block; set to 300 when done debugging
                        FirstSuccessTimer = time.time()
                        score = 0
                        successjar = 0
                        remainder = 0
                        recordtick = time.time()+.25   #Collecting values at a 250 ms interval; decrease to up sampling rate
                        consolidatedoutput = []
                        consolidatedhi = []
                        consolidatedlo = []
                        consolidatedoutputNext = []
                        consolidatedhiNext = []
                        consolidatedloNext = []
                        ControlCountdown = time.time()
                        ControlTimer = time.time() 
                        VoltMedianArrayNext = []
                        #This is for the baselining stages at the beginning and end
                        if stage == 0 or stage == 5:
                            countdown = time.time() + FixationInterval #Number of seconds for Baseline block
                           
                        # #This increases or decreases the threshold of the ratio, based on performance in the previous blocks
                        #These are blocked out for now, as the thresholds should shift in other ways.
                        # if stage == 2 or stage == 3 or stage == 4:
                           # if ontime/BlocInterval > .6:
                               # Threshold = Threshold + deviance/2
                               # Level = Level + 1
                           # elif ontime/BlocInterval < .2:
                               # Threshold = Threshold - deviance/2
                               # Level = Level - 1
                        stage = stage + 1 # time to go to the next stage
                        
                    #If the control key is pressed
                if event.key == pygame.K_q:  
                    if stage == 0:
                        if pausetime == True:

                            print("CONTROL mode initiated.")
                            CONTROL = True
                if event.key == pygame.K_p:  
                    if stage == 0:                           
                        BlocInterval = 5    #300
                        FixationInterval = 1 #180
                        print('Debug values enabled')

                        
        #This checks SPTruVal, which it should be receiving from the Visualizer script.
        TargetVal = SPTruVal
        #The following is for when the stage is triggered by using the Visualizer interface.
        if NEXT == True and stage != 5 and stage != 0:  
                    if pausetime == True:
                        pausetime = False
                        NEXT = False
                        RecordBypass = False #Likely unnecessary, but I'm playing it safe for now.
                        
                        ontime = 0             #This sets the beginning period of time to zero
                        countdown = time.time() + BlocInterval #This is the number of seconds in a Glider game block; set to 300 when done debugging
                        FirstSuccessTimer = time.time()
                        score = 0
                        successjar = 0
                        remainder = 0
                        recordtick = time.time()+.25   #Collecting values at a 250 ms interval; decrease to up sampling rate
                        consolidatedoutput = []
                        consolidatedhi = []
                        consolidatedlo = []
                        consolidatedoutputNext = []
                        consolidatedhiNext = []
                        consolidatedloNext = []
                        ControlCountdown = time.time()   
                        ControlTimer = time.time()
                        VoltMedianArrayNext = []
                        #This is for the baselining stages at the beginning and end
                        if stage == 0 or stage == 5:
                            countdown = time.time() + FixationInterval #Number of seconds for Baseline block
                           
                        # #This increases or decreases the threshold of the ratio, based on performance in the previous blocks
                        #These are blocked out for now, as the thresholds should shift in other ways.
                        # if stage == 2 or stage == 3 or stage == 4:
                           # if ontime/BlocInterval > .6:
                               # Threshold = Threshold + deviance/2
                               # Level = Level + 1
                           # elif ontime/BlocInterval < .2:
                               # Threshold = Threshold - deviance/2
                               # Level = Level - 1
                        stage = stage + 1 # time to go to the next stage
                        
        if DISCONNECT == True:
            print('DISCONNECT'+ str(round(time.time(),1)))
            if LastDISCONNECT == False:
                PauseStart = time.time()
                time.sleep(.1)
                LastDISCONNECT = True
                pygame.display.flip() #needed to draw the >|<~STARS~>|<
                pygame.display.update() #Refresh all the details that do not fall under the "flip" method. SP NOTE: I don't understand the difference very well.
                
                FPSCLOCK.tick(FPS)                
                continue
            else:  #If disconnection remains, just skip everything
                time.sleep(.250)
                pygame.display.flip() #needed to draw the >|<~STARS~>|<
                pygame.display.update() #Refresh all the details that do not fall under the "flip" method. SP NOTE: I don't understand the difference very well.
                
                FPSCLOCK.tick(FPS)                
                continue
        if DISCONNECT == False:
            if LastDISCONNECT == True:
                PauseTotal = time.time() - PauseStart
                recordtick = recordtick + PauseTotal
                countdown = countdown + PauseTotal
                initialization = initialization + PauseTotal
                ContinualSuccessTimer = ContinualSuccessTimer + PauseTotal
                FirstSuccessTimer= FirstSuccessTimer + PauseTotal
                ontime = ontime + PauseTotal
                successjar = successjar + PauseTotal
        LastDISCONNECT = DISCONNECT  
        #This portion accounts for the possibility of recording bypass.
        if (stage == 0 or stage == 5) and RecordBypass == True:
            if pausetime == True: #Inelegant; make a module for this later so as to encompass keypresses
                pausetime = False
                RecordBypass = False # Can't have the recordbypass triggering prematurely for the second recording.
                if stage == 1 or stage == 2 or stage == 3 or stage == 4: #This is for if there is no stored time to add in the success time jar.

                    if successflag == False:
                        print(str(ontime)+' seconds is supposed ontime. (falseflag)')
                
                ontime = 0             #This sets the beginning period of time to zero
                countdown = time.time() + BlocInterval #This is the number of seconds in a Glider game block; set to 300 when done debugging
                FirstSuccessTimer = time.time()
                score = 0
                recordtick = time.time()+.25   #Collecting values at a 250 ms interval; decrease to up sampling rate
                consolidatedoutput = []
                consolidatedhi = []
                consolidatedlo = []
                consolidatedoutputNext = []
                consolidatedhiNext = []
                consolidatedloNext = []
                VoltMedianArray = []
                ControlCountdown = time.time()
                ControlTimer = time.time() 
                
                                #This is for the baselining stages at the beginning and end
                if stage == 0 or stage == 5:
                    countdown = time.time() + FixationInterval #Number of seconds for Baseline block

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
        
        
        
        
        #Hardcoded to 300 for now, but it used to be 30 seconds.  Baseline determination.
        if time.time()+300 > countdown:
            #if stage == 2 or stage == 3 or stage == 4 or stage == 5: 
                if time.time() >= recordtick: 
                    recordtick = time.time()+.25  #This collects data every 250 ms.  Lower this number for higher resolution
                    if stage == 1 or stage == 6 or (VoltBaseline < VoltMin + 100 and VoltBaseline > VoltMax - 100 and HighNoiseFlag == False and LowNoiseFlag == False):
                        #print('Voltmin', VoltMin, 'Voltmax', VoltMax, 'VoltBaseline', VoltBaseline)
                        consolidatedoutputNext.append(TargetVal)
                    consolidatedhiNext.append(HiNoise)
                    consolidatedloNext.append(LoNoise)
                    VoltMedianArrayNext.append(VoltMedian)

        
        #If the countdown timer reaches zero
        if time.time() > countdown:  
        
            #if stage == 2 or stage == 3 or stage == 4 or stage == 5:
            
            ControlIndex = 0
            
            consolidatedoutput = consolidatedoutputNext
            consolidatedhi = consolidatedhiNext
            consolidatedlo = consolidatedloNext
            VoltMedianArray = VoltMedianArrayNext
					
            #What follows is a series of print statements that tell the administrator about previous sessions.
			#These values are also written to a text file for future examination.
            print("STAGE " + str(stage)) #Just printing the stage
            
            output = sum(consolidatedoutput)/len(consolidatedoutput)
            f.write(str(output) + ',')
            if ControlRecording == False: ses.write(str(output) + "\n")
            print('A return character has been entered.')
            Threshold = output
            print("Data Baseline is: " + str(output))
            
            if ControlRecording == True:
                if stage == 1: Threshold = CB1
                if stage == 2: Threshold = CB2
                if stage == 3: Threshold = CB3
                if stage == 4: Threshold = CB4
            
            deviance = np.std(consolidatedoutput)
            f.write(str(deviance) + ',')
            print("Data baseline STDEV:" + str(deviance))

            HiOutput = sum(consolidatedhi)/len(consolidatedhi)
            f.write(str(HiOutput) + ',')
            print("High Freq. Noise Baseline: " + str(HiOutput))

            
            HiDev = np.std(consolidatedhi)
            f.write(str(HiDev) + ',')
            print("High Freq. Noise STDEV: " + str(HiDev))
 
            LoOutput = sum(consolidatedlo)/len(consolidatedlo)
            f.write(str(LoOutput) + ',')
            print("Low Freq. Noise Baseline is: " + str(LoOutput))

            LoDev = np.std(consolidatedlo)
            f.write(str(LoDev) + ',\n')
            print("Low Freq. Noise STDev is: " + str(LoDev))
            pausetime = True
            if stage == 2 or stage == 3 or stage == 4 or stage == 5:
                if ControlRecording == False: ses.write(str(Threshold) + '\n') #newline for recording
                if successflag == True:
                    remainder = time.time() - successjar
                    # print(ontime)
                    # print(successjar)
                    # print(str(ontime+time.time()-successjar)+' seconds supposed Ontime(endtru).') #ISSUE: probably need to make ontime internally consistent
                    successflag = False
                if successflag == False:
                    print(str(round(ontime+remainder, 2))+' seconds is supposed ontime.') #falseflag  
                f.write(str(score) + ',' + str(Threshold) + ',' + str(Level) + ',' + str(round(ontime+remainder, 2)) + ',\n')
                
            f.write('\n') #New line
            b.rect.y = WINDOWHEIGHT/2
            
            

            
            #This is for the voltage values
            VoltBaseline = np.mean(VoltMedianArray)
            print(str(round(np.mean(VoltMedianArray), 2))+' v is the average of the Median Voltages.') #falseflag         

            continue
        
        #baselining at stages 1 and 6
        if stage == 1 or stage == 6:
            fixation(recordtick)
            #displayDEBUG(round(TargetVal,3))
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            continue

        #Final exit after last stage  
        if stage == 7:
            pygame.quit()
            f.close()
            print("Game over, man.  Game over.")
            quittingtime = True
            break
            
        #Let's make the stage 
        drawArena()


        
        #This draws the bar graphs for high and low band noises
        drawHighFreq()
        drawLoFreq()
        lastflag = successflag   #this is so we can compare the current success state with the previous
        
        #This is all for the control subject case. 
        if ControlRecording == False: ses.write(str(TargetVal)+',')
        else:
            if stage == 2:
                if (len(C1) - 1) < ControlIndex:
                    TargetVal = C1[len(C1) - 1]
                else:
                    TargetVal = C1[ControlIndex-1]
            if stage == 3:
                if (len(C2) - 1) < ControlIndex:
                    TargetVal = C2[len(C2) - 1]
                else:
                    TargetVal = C2[ControlIndex-1]
            if stage == 4:
                if (len(C3) - 1) < ControlIndex:
                    TargetVal = C3[len(C3) - 1]
                else:
                    TargetVal = C3[ControlIndex-1]                    
            if stage == 5:
                if (len(C4) - 1) < ControlIndex:
                    TargetVal = C4[len(C4) - 1]
                else:
                    TargetVal = C4[ControlIndex-1]                    
                    
                    
            if ControlTimer < time.time():
                ControlTimer = ControlTimer + .25
                ControlIndex = ControlIndex + 1
                print(ControlIndex)
                
                
        #This is for the randomized CONTROL condition:
        if CONTROL == True:
            if ControlCountdown <= time.time():
                a = randrange(1,100)
                a = a - stage*5
                if a < 30: ControlVal = Threshold - 1
                else: ControlVal = Threshold + 1
                ControlCountdown = time.time() + (randrange(4, 20)*0.1)
        else: ControlVal = TargetVal
        
        #This moves our glider in accordance with the thresholds and colors him if wrong; 
        #LIKELY INEFFICIENT METHOD OF IMAGE LOADING, perhaps revisit later.
        if LowNoiseFlag == True or HighNoiseFlag == True or VoltBaseline > VoltMin + 100 or VoltBaseline < VoltMax - 100:
            b.image = pygame.image.load("GliderRed.png").convert_alpha()
            b.rect.y	=  b.rect.y + 1
            successflag = False        
        elif (TargetVal < Threshold or ControlVal < Threshold) and HighNoiseFlag == False and LowNoiseFlag == False:  
            b.rect.y	=  b.rect.y - 1 #It is counterintuitive, but lower numbers means higher on the screen.
            b.image = pygame.image.load("GliderGood.png").convert_alpha()
            successflag = True 
        elif TargetVal >= Threshold or ControlVal >= Threshold:
            b.image = pygame.image.load("Glider.png").convert_alpha()
            b.rect.y = b.rect.y + 1
            successflag = False
        #This determines whether a point should be awarded
        TargetVal = ControlVal #This only does anything in CONTROL mode
        score = checkPointScored(score)#paddle1, ball, score, ballDirX)    

        
        
        #COUNTING TIME ABOVE THRESHOLD
        if lastflag == False:       #if the previous time point was not above threshold and noiseless
            if successflag == True: #and the current time point is above threshold and noiseless
                successjar = time.time()    #Begin collecting time in the successjar
        if lastflag == True:        #If the last time point is good
            if successflag == False:#But the current one is bad 
                ontime = ontime + time.time() - successjar  #then dump the success jar

        #Displays the score 
        displayScore(score)
        
        #Displays debug information
        displayDEBUG(round(TargetVal,3))
        
        
        #draws the ~*STARS*~
        move_and_draw_stars(DISPLAYSURF, b)

        #dummied out circle display code
        #drawcircle()       
        #drawpowercircle()
        
        #Final draws and screen update
        drawSprite(b) #Draws the glider in his new position
        pygame.display.flip() #needed to draw the >< ~STARS~ ><
        pygame.display.update() #Refresh all the details that do not fall under the "flip" method. SP NOTE: I don't understand the difference very well.
        
        FPSCLOCK.tick(FPS) #Tells the game system that it is not untouched by the inexorable march of time

if __name__=='__main__':
    main()
	
