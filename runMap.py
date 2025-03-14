import pygame
from randomMap import randomMapGame

#init
pygame.init()
clock = pygame.time.Clock()

map = randomMapGame()

isGameRunning = True
while isGameRunning:
    map.run()

    pygame.display.flip()
    clock.tick(60)

# Close pygame
pygame.quit()
