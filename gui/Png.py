import pygame, sys
from pygame.locals import *
import numpy as np
import time
from random import randrange #for starfield, random number generator



# Number of frames per second
# Change this value to speed up or slow down your game
FPS = 50




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

#Flags for high and low noise; false until noise thresholds are passed.
HighNoiseFlag = False
LowNoiseFlag = False

#Timers and flags for continual success scoring
FirstSuccessTimer = time.time()
FirstSuccessFlag = False
ContinualSuccessFlag = False
ContinualSuccessTimer = time.time()

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

    #Black out everything on the screen
    DISPLAYSURF.fill(BLACK)
    
    
    if stage == 0:
        if time.time() < initialization: #if I don't make a 5 scond delay, things go funny
            resultSurf = SCOREFONT.render('PLEASE WAIT WHILE INITIALIZING', True, WHITE)
        else:
            resultSurf = SCOREFONT.render('PRESS SPACE TO BEGIN BASELINE', True, WHITE)
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
    

    
        
    # I kind of did a hack job here, but basically this sets up the screen display for each stage.
    
    if stage != 0:
        #Draw the grid 
        pygame.draw.rect(DISPLAYSURF, WHITE, ((WINDOWWIDTH-635,WINDOWHEIGHT-300),(-600,-400)), LINETHICKNESS)
        
        
        
        #latitude lines
        latitudes = 8 #This is the number of times to split latitudinally
        for i in range(0, latitudes):
            pygame.draw.line(DISPLAYSURF, WHITE, ((WINDOWWIDTH-635),WINDOWHEIGHT-300-int(i*400/latitudes)),((WINDOWWIDTH-1235),WINDOWHEIGHT-300-int(i*400/latitudes)), int(LINETHICKNESS*.2))
            
            increment = 5
            resultSurf = BASICFONT.render(str(i*increment), True, WHITE)
            resultRect = resultSurf.get_rect()
            resultRect.center = (WINDOWWIDTH-1265, (WINDOWHEIGHT-298-int(i*400/latitudes)))
            DISPLAYSURF.blit(resultSurf, resultRect)
        
        #Display the longitude lines and labels
        #This was done in a stupid way, but it works.  Should have used a loop.
        resultSurf = BASICFONT.render("Trial 1", True, WHITE)
        resultRect = resultSurf.get_rect()
        resultRect.center = (WINDOWWIDTH-1155, WINDOWHEIGHT-250)
        DISPLAYSURF.blit(resultSurf, resultRect)
        pygame.draw.line(DISPLAYSURF, WHITE, ((WINDOWWIDTH-1085),WINDOWHEIGHT-300),((WINDOWWIDTH-1085),WINDOWHEIGHT-700), int(LINETHICKNESS*.2))

        resultSurf = BASICFONT.render("Trial 2", True, WHITE)
        resultRect = resultSurf.get_rect()
        resultRect.center = (WINDOWWIDTH-1005, WINDOWHEIGHT-250)
        DISPLAYSURF.blit(resultSurf, resultRect)
        pygame.draw.line(DISPLAYSURF, WHITE, ((WINDOWWIDTH-935 ),WINDOWHEIGHT-300),((WINDOWWIDTH-935 ),WINDOWHEIGHT-700), int(LINETHICKNESS*.2))

        resultSurf = BASICFONT.render("Trial 3", True, WHITE)
        resultRect = resultSurf.get_rect()
        resultRect.center = (WINDOWWIDTH-855, WINDOWHEIGHT-250)
        DISPLAYSURF.blit(resultSurf, resultRect)
        pygame.draw.line(DISPLAYSURF, WHITE, ((WINDOWWIDTH-785 ),WINDOWHEIGHT-300),((WINDOWWIDTH-785 ),WINDOWHEIGHT-700), int(LINETHICKNESS*.2))

        resultSurf = BASICFONT.render("Trial 4", True, WHITE)
        resultRect = resultSurf.get_rect()
        resultRect.center = (WINDOWWIDTH-705, WINDOWHEIGHT-250)
        DISPLAYSURF.blit(resultSurf, resultRect)
        
      
        
        if stage >= 2:
            pygame.draw.circle(DISPLAYSURF, RED, [WINDOWWIDTH - 1160, WINDOWHEIGHT-300-50/increment*score1], 8) #tie Windowheight to score
            
            resultSurf = BASICFONT.render('%s Points' %(score1), True, YELLOW)
            resultRect = resultSurf.get_rect()
            resultRect.center = (WINDOWWIDTH-1155, WINDOWHEIGHT-225)
            DISPLAYSURF.blit(resultSurf, resultRect)
        if stage >= 3:
            pygame.draw.circle(DISPLAYSURF, RED, [WINDOWWIDTH - 1010, WINDOWHEIGHT-300-50/increment*score2], 8)
            pygame.draw.line(DISPLAYSURF, RED, ((WINDOWWIDTH-1160),WINDOWHEIGHT-300-50/increment*score1),((WINDOWWIDTH-1010),WINDOWHEIGHT-300-50/increment*score2), int(LINETHICKNESS*.4)) #ie line height to previous circle
            
            resultSurf = BASICFONT.render('%s Points' %(score2), True, YELLOW)
            resultRect = resultSurf.get_rect()
            resultRect.center = (WINDOWWIDTH-1005, WINDOWHEIGHT-225)
            DISPLAYSURF.blit(resultSurf, resultRect)

            
        if stage >= 4:
            pygame.draw.circle(DISPLAYSURF, RED, [WINDOWWIDTH - 860, WINDOWHEIGHT-300-50/increment*score3], 8)
            pygame.draw.line(DISPLAYSURF, RED, ((WINDOWWIDTH-1010),WINDOWHEIGHT-300-50/increment*score2),((WINDOWWIDTH-860),WINDOWHEIGHT-300-50/increment*score3), int(LINETHICKNESS*.4))

            resultSurf = BASICFONT.render('%s Points' %(score3), True, YELLOW)
            resultRect = resultSurf.get_rect()
            resultRect.center = (WINDOWWIDTH-855, WINDOWHEIGHT-225)
            DISPLAYSURF.blit(resultSurf, resultRect)

        if stage >= 5:
            pygame.draw.line(DISPLAYSURF, RED, ((WINDOWWIDTH-860),WINDOWHEIGHT-300-50/increment*score3),((WINDOWWIDTH-710),WINDOWHEIGHT-300-50/increment*score4), int(LINETHICKNESS*.4))
            pygame.draw.circle(DISPLAYSURF, RED, [WINDOWWIDTH - 710, WINDOWHEIGHT-300-50/increment*score4], 8)
            
            resultSurf = BASICFONT.render('%s Points' %(score4), True, YELLOW)
            resultRect = resultSurf.get_rect()
            resultRect.center = (WINDOWWIDTH-705, WINDOWHEIGHT-225)
            DISPLAYSURF.blit(resultSurf, resultRect)
        
        if stage == 2 or stage == 3 or stage == 4:
            displayedlevel = Level
            if successflag == True:
                ontime = ontime + time.time() - successjar
                successflag = False
            if ontime/300 > .6:
                displayedlevel = displayedlevel + 1

                resultSurf = SCOREFONT.render('LEVEL UP', True,  TURQUOISE)
                resultRect = resultSurf.get_rect()
                resultRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2-250)
                DISPLAYSURF.blit(resultSurf, resultRect)
            elif ontime/300 < .2:
                displayedlevel = displayedlevel - 1
                resultSurf = SCOREFONT.render('LEVEL DOWN', True, ORANGE)
                resultRect = resultSurf.get_rect()
                resultRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2-250)
                DISPLAYSURF.blit(resultSurf, resultRect)
                #This announces difficulty
    return score

    
#BASELINE MODULE
def fixation(recordtick):


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
    global HighNoiseFlag
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
        HighNoiseFlag = True
    else:
        pygame.draw.rect(DISPLAYSURF, WHITE,((WINDOWWIDTH-325,400),(150,-300*scaledHi)) )
        HighNoiseFlag = False
    
    #This draws the "container" for the bar (in white), and the midmark (in orange). 
    pygame.draw.line(DISPLAYSURF, ORANGE, ((WINDOWWIDTH-325), 250),((WINDOWWIDTH-175), 250), (LINETHICKNESS/5))    
    pygame.draw.rect(DISPLAYSURF, WHITE, ((WINDOWWIDTH-325,100),(150,300)), int(LINETHICKNESS*.5))

    
#Draws the bar for low frequency noise
def drawLoFreq():
    global LowNoiseFlag
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
        LowNoiseFlag = True
        pygame.draw.rect(DISPLAYSURF, RED,((WINDOWWIDTH-325,800),(150,-300*scaledLo)) )
    else:
        pygame.draw.rect(DISPLAYSURF, WHITE,((WINDOWWIDTH-325,800),(150,-300*scaledLo)) )
        LowNoiseFlag = False
    
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
    DISPLAYSURF.set_at(star,(255,255,255)) #Turns on the next star position


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


#Checks to see if a point has been scored; returns new score
def checkPointScored(score): # paddle1, ball, score, ballDirX):
    global FirstSuccessTimer
    global FirstSuccessFlag 
    global ContinualSuccessFlag 
    global ContinualSuccessTimer 

    #Start by checking for success state

    if SPTruVal > Threshold and HighNoiseFlag == False and HighNoiseFlag == False:
        if FirstSuccessFlag == False:       #Sees if the first round has begun;this just sets the first timer, really.
            if time.time() > ContinualSuccessTimer: #Make sure previous successes do not allow rapid-fire point generation
                FirstSuccessFlag = True
                FirstSuccessTimer = time.time() +.25
                
        elif FirstSuccessFlag == True:       
            if ContinualSuccessFlag == False:           #If the first point hasn't been made
                if time.time() > FirstSuccessTimer:      #Have .25 seconds passed?
                    score = score + 1
                    coin.play()                         #Award a point and give a coin!
                    ContinualSuccessTimer = time.time() + 3 #Make the timer 3 seconds forward
                    ContinualSuccessFlag = True            
            else:                                       #read: If at least one point has been scored    
                if time.time() > ContinualSuccessTimer:  #read: if 3 seconds have passed since the first point
                    score = score + 1
                    coin.play()                         #Award a point and give a coin!
                    ContinualSuccessTimer = time.time() + 3 #Make the timer 3 seconds forward
                    ContinualSuccessFlag = True   
    else:
        FirstSuccessFlag = False
        ContinualSuccessFlag = False
       
    return score


#Displays the current score on the screen 
def displayScore(score):
    resultSurf = SCOREFONT.render('Score = %s' %(score), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (650, 40)
    DISPLAYSURF.blit(resultSurf, resultRect)

	
#Displays debugging stuff; the calling of SPTruVal here is kind of an artifact, ignore it I think
def displaySPTruVal(SPTruVal):
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
        resultSurf = BASICFONT.render('hinoi', True, WHITE)
        resultRect = resultSurf.get_rect()
        resultRect.topleft = (WINDOWWIDTH - 300, 70)
        DISPLAYSURF.blit(resultSurf, resultRect)
    if LowNoiseFlag == True:
        resultSurf = BASICFONT.render('lonoi', True, WHITE)
        resultRect = resultSurf.get_rect()
        resultRect.topleft = (WINDOWWIDTH - 375, 70)
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
    global stage
    global consolidatedoutput
    global HiOutput
    global LoOutput
    global initialization
    global Level
    global ontime
    global successflag
    global successtimer
    global successjar
    global Threshold
    global f
    
    
    #This is the period of time the threshold is surpassed, starting at zero:
    ontime = 0
    
    #This opens the file to be written to:
    f = open('NFT_Output.csv', 'w') #This should have the custom name plugged in later;
    
    initialization = time.time() + 5 #5 seconds are needed for the data stream to connect properly.
    BASICFONTSIZE = 20
    SCOREFONTSIZE = 40 
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    SCOREFONT = pygame.font.Font('freesansbold.ttf', SCOREFONTSIZE)
    Level = 0 #this is the starting point of threshold challenge.

    
    # Flags for whether to quit or pause; starts paused.
    quittingtime = False 
    pausetime = True
    
    #This is used in counting success time; the success time counter goes forward only if this is true
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
    b.rect.topleft = [WINDOWWIDTH/2-300, WINDOWHEIGHT/2] # put the image in the center of the player window
   
   
    # make mouse cursor invisible
    pygame.mouse.set_visible(0) 

    
    #Let the games (loop) begin!
    while True: 
        #Processes game events like quitting or keypresses
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                f.close()
                quittingtime = True
                break
                
            #This portion does keypresses
            if event.type == pygame.KEYDOWN:  #press space to terminate pauses between blocs
                if event.key == pygame.K_SPACE:
                    if pausetime == True:
                         pausetime = False
                         ontime = 0             #This sets the beginning period of time to zero
                         countdown = time.time() + 300 #This is the number of seconds in a Glider game block; set to 300 when done debugging
                         FirstSuccessTimer = time.time()
                         score = 0

                         #This is for the baselining stages at the beginning and end
                         if stage == 0 or stage == 5:
                            countdown = time.time() + 180 #Number of seconds for Baseline block
                            recordtick = time.time()+.25   #Collecting values at a 250 ms interval; decrease to up sampling rate
                            
                         #This increases or decreases the threshold of the ratio, based on performance in the previous blocks
                         
                         if stage == 2 or stage == 3 or stage == 4:
                            if ontime/300 > .6:
                                Threshold = Threshold + stdev/2
                                Level = Level + 1
                            elif ontime/300 < .2:
                                Threshold = Threshold - stdev/2
                                Level = Level - 1
                                
                                

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
                f.write(str(output) + ',')
                Threshold = output
                print("With a standard deviation of:")
                deviance = np.std(consolidatedoutput)
                print(deviance)
                f.write(str(deviance) + ',')
                print("The subject's High Noise Baseline is:")
                HiOutput = sum(consolidatedhi)/len(consolidatedhi)
                print(HiOutput)
                f.write(str(HiOutput) + ',')
                print("With a standard deviation of:")
                HiDev = np.std(consolidatedhi)
                print(HiDev)
                f.write(str(HiDev) + ',')
                print("The subject's Low Noise Baseline is:")
                LoOutput = sum(consolidatedlo)/len(consolidatedlo)
                print(LoOutput)
                f.write(str(LoOutput) + ',')
                print("With a standard deviation of:")
                LoDev = np.std(consolidatedlo)
                print(LoDev)
                f.write(str(LoDev) + ',\n')
                
            pausetime = True
            if stage == 2 or stage == 3 or stage == 4 or stage == 5:
                f.write(str(score) + ',' + str(Threshold) + ',' + str(Level) + ',' + str(ontime + time.time() - successjar) + ',\n')
            successjar = 0
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
            
        #This moves our glider in accordance with the thresholds and colors him if wrong; 
        #LIKELY INEFFICIENT METHOD OF IMAGE LOADING, perhaps revisit later.
        if SPTruVal > Threshold and HighNoiseFlag == False and HighNoiseFlag == False:  
            b.rect.y	=  b.rect.y - 1 #It is counterintuitive, but lower numbers means higher on the screen.
            b.image = pygame.image.load("GliderGood.png").convert_alpha()
            successflag = True 
        elif HighNoiseFlag == True and LowNoiseFlag == True:
            b.image = pygame.image.load("GliderRedOrange.png").convert_alpha()
            b.rect.y	=  b.rect.y + 1
            successflag = False 
        elif LowNoiseFlag == True:
            b.image = pygame.image.load("GliderRed.png").convert_alpha()
            b.rect.y	=  b.rect.y + 1
            successflag = False
        elif HighNoiseFlag == True:
            b.image = pygame.image.load("GliderOrange.png").convert_alpha()
            b.rect.y	=  b.rect.y + 1
            successflag = False
        elif SPTruVal <= Threshold:
            b.image = pygame.image.load("Glider.png").convert_alpha()
            b.rect.y = b.rect.y + 1
            successflag = False
        
        #This determines whether a point should be awarded
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
        displaySPTruVal(round(SPTruVal,3))
        
        
        #draws the ~*STARS*~
        move_and_draw_stars(DISPLAYSURF)

        #dummied out circle display code
        #drawcircle()       
        #drawpowercircle()
        
        #Final draws and screen update
        drawSprite(b) #Draws the glider in his new position
        pygame.display.flip() #needed to draw the >|<~STARS~>|<
        pygame.display.update() #Refresh all the details that do not fall under the "flip" method. SP NOTE: I don't understand the difference very well.
        
        FPSCLOCK.tick(FPS) #Tells the game system that it is not untouched by the inexorable march of time

if __name__=='__main__':
    main()
	
