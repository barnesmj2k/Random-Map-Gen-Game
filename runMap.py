import pygame
from randomMap import randomMapGame
from pygame import mixer

#init
pygame.init()
clock = pygame.time.Clock()

map = randomMapGame()

# Starting the mixer 
mixer.init() 
# Loading the song 
mixer.music.load("AquaticColorsAlexMoiseev.wav") 
# Setting the volume 
mixer.music.set_volume(0.7) 
# Start playing the song 
mixer.music.play() 

isGameRunning = True
while isGameRunning:
    map.run()

    pygame.display.flip()
    clock.tick(60)

# Close pygame
pygame.quit()
