import pygame
from random import randrange



 

 
def main():
  # Pygame stuff
  pygame.init()
  screen = pygame.display.set_mode((640,480))
  pygame.display.set_caption("Starfield Simulation")
  clock = pygame.time.Clock()
 
  init_stars(screen)
 
  while True:
    # Lock the framerate at 50 FPS
    clock.tick(50)
 
    # Handle events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            print("Space Adventure!")
 
    screen.fill((0,0,0))
    move_and_draw_stars(screen)
    pygame.display.flip()
 
if __name__ == "__main__":
  main()