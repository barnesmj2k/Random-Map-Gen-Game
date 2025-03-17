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
music = mixer.Sound("AquaticColorsAlexMoiseev.wav") 
mixer.music.load("Storm.mp3") 
# Setting the volume  
# Start playing the song 
mixer.Sound.play(music)
mixer.music.play(3,8) 

isGameRunning = True
while isGameRunning:
    map.run()

    pygame.display.flip()
    clock.tick(60)

# Close pygame
pygame.quit()
