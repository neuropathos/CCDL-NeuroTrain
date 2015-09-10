import pygame, sys
from pygame.locals import *
import time
# Number of frames per second
# Change this value to speed up or slow down your game
FPS = 100

#Global Variables to be used through our program
pygame.display.init()
disp = pygame.display.Info()
WINDOWWIDTH = disp.current_w
WINDOWHEIGHT = disp.current_h
LINETHICKNESS = 10
PADDLESIZE = (WINDOWHEIGHT/2)
PADDLEOFFSET = 20

# Set up the colours
BLACK     = (0  ,0  ,0  )
WHITE     = (255,255,255)

#Draws the arena the game will be played in. 
def drawArena():
    DISPLAYSURF.fill((0,0,0))

    #Draw centre line
    pygame.draw.line(DISPLAYSURF, WHITE, ((WINDOWWIDTH/2), 10+WINDOWHEIGHT/2),((WINDOWWIDTH/2),WINDOWHEIGHT/2-10), (LINETHICKNESS/2))
    pygame.draw.line(DISPLAYSURF, WHITE, ((10+WINDOWWIDTH/2),WINDOWHEIGHT/2),((WINDOWWIDTH/2 - 10),WINDOWHEIGHT/2), (LINETHICKNESS/2))




# def preamble():
    # recordtick = time.time()+10
    # # pygame.event.clear()
    # print(101)
    # # while True:
#        event = pygame.event.wait()
#        if event.type == QUIT:
#            pygame.quit()
#            sys.exit()
#        elif event.type == KEYDOWN:
#            if event.key = K_c:
        # for event in pygame.event.get():
            # print(102)
            # if event.type == QUIT:
                # print(86)
                # exit()
            # if event.type == KEYDOWN:
                # if event.key == K_c:
                    # recordbreak = time.time()+18
                    # print('okay')
                    # print(1)
                    # while time.time() <= recordbreak:
                        # a = 1
        # break


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


    pygame.mouse.set_visible(0) # make cursor invisible
	
    #preamble()#enable press key to start
    recordtick = time.time()+5
    output = 0
    ticks = 0
    while True: #main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                print output
                pygame.quit()
             # mouse movement commands
            #elif event.type == MOUSEMOTION:
            #    mousex, mousey = event.pos
            #    paddle1.y = mousey
        if time.time() >= recordtick:
            recordtick = time.time()+.25
            ticks = ticks+1
            output = output/ticks + val/ticks #val is defined in visualizer
            
        drawArena()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()
	
