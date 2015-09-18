import pygame
from random import randrange
 
MAX_STARS  = 250
STAR_SPEED = 1


 
def init_stars(screen):
  """ Create the starfield """
  global stars
  stars = []
  for i in range(MAX_STARS):
    # A star is represented as a list with this format: [X,Y]
    star = [randrange(0,300 - 1),
            randrange(0,300 - 1)]
    stars.append(star)
 
def move_and_draw_stars(screen):
  """ Move and draw the stars in the given screen """
  global stars
  for star in stars:
    star[0] -= STAR_SPEED
    # If the star hit the bottom border then we reposition
    # it in the top of the screen with a random X coordinate.
    if star[0] <= 1:
      star[0] = 300
      star[1] = randrange(0,299)
 
    screen.set_at(star,(255,255,255))
 
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