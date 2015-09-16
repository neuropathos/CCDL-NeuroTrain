import pygame, sys
from pygame.locals import *
import time
import numpy as np
# Number of frames per second
# Change this value to speed up or slow down your game
FPS = 100
val = 0
output = 0
consolidatedoutput = []
ticks = 0
#Global Variables to be used through our program
pygame.display.init()
disp = pygame.display.Info()
WINDOWWIDTH = disp.current_w
WINDOWHEIGHT = disp.current_h
LINETHICKNESS = 10

Baseline = False #this goes back to the visualizer in a frankly slightly arcade way



# Set up the colours
BLACK     = (0  ,0  ,0  )
WHITE     = (255,255,255)

#Draws the arena the game will be played in. 
def drawArena():
    DISPLAYSURF.fill((0,0,0))

    #Draw centre line
    pygame.draw.line(DISPLAYSURF, WHITE, ((WINDOWWIDTH/2), 10+WINDOWHEIGHT/2),((WINDOWWIDTH/2),WINDOWHEIGHT/2-10), (LINETHICKNESS/2))
    pygame.draw.line(DISPLAYSURF, WHITE, ((10+WINDOWWIDTH/2),WINDOWHEIGHT/2),((WINDOWWIDTH/2 - 10),WINDOWHEIGHT/2), (LINETHICKNESS/2))



def displaySPTruVal(val):
    resultSurf = BASICFONT.render('SPVal = %s' %(val), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 300, 25)
    DISPLAYSURF.blit(resultSurf, resultRect)

#Displays the current score on the screen 
def displayScore(output):
    resultSurf = BASICFONT.render('Score = %s' %(output), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 150, 25)
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
    pygame.display.set_caption('Fixation Cross')


  
    #Draws the starting position of the Arena
    drawArena()
    displaySPTruVal(round(val,3))
    
    #Displays the Electrode Value on the screen  for debugging
    
    pygame.mouse.set_visible(0) # make cursor invisible
	
    #preamble()#enable press key to start
    quittingtime = False
    Baseline = True 
    output = 0
    ticks = 0
    recordtick = time.time()+5
    while True: #main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                print("The subject's Baseline is:")
                output = sum(consolidatedoutput)/len(consolidatedoutput)
                print(output)
                print("With a standard deviation of:")
                deviance = np.std(consolidatedoutput)
                print(deviance)

                
                quittingtime = True
                Baseline = False
                # print(sum(consolidatedoutput)/ticks)
                # print(sum(consolidatedoutput)/ticks)
                # print(ticks)
                # print(len(consolidatedoutput))
                # print(consolidatedoutput)
                pygame.quit()
                break
             # mouse movement commands
            #elif event.type == MOUSEMOTION:
            #    mousex, mousey = event.pos
            #    paddle1.y = mousey
        if quittingtime == True:
            break
        if time.time() >= recordtick:
            recordtick = time.time()+.25
            ticks = ticks+1
            consolidatedoutput.append(val)
            output = sum(consolidatedoutput)/len(consolidatedoutput)
            deviance = np.std(consolidatedoutput)
            #output = #(output + val)/ticks #val is defined in visualizer
        drawArena()
        displaySPTruVal(round(val,3))
        displayScore(round(output,3))
        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__=='__main__':
    main()
	
