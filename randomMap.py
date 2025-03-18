import pygame
from GenerateNoise import Noise
from PIL import Image, ImageEnhance
import math
import random
from spriteSheet import SpriteSheet

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
PLAYER_SPEED = 0.15

mapList = [
    (0,0,       500,500),
    (500,0,     500,500),
    (1000,0,    500,500),
    (0,500,     500,500),
    (500,500,   500,500),
    (1000,500,  500,500),
    (0,1000,    500,500),
    (500,1000,  500,500),
    (1000,1000, 500,500)
]

runSprites = [
    (24,16,40,52),
    (104,16,40,52),
    (184,16,40,52),
    (264,16,40,52),
    (344,16,40,52),
    (424,16,40,52),
    (504,16,40,52),
    (584,16,40,52)
]

idleSprites = [
    (12,12,44,52),
    (76,12,44,52),
    (140,12,44,52),
    (204,12,44,52)
]

class randomMapGame():
    def __init__(self):

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.myFont = pygame.font.SysFont("Times New Roman", 18)
        # self.player = pygame.Rect(250,250,30,30)
        Noise.makeImage(SCREEN_HEIGHT,SCREEN_WIDTH,"bw",50)

        boatDamaged = pygame.image.load('boat2.png').convert_alpha()
        boatRepaired = pygame.image.load('boat3.png').convert_alpha()
        boatGold = pygame.image.load('boat4.png').convert_alpha()
        self.boatDamaged = pygame.transform.scale(boatDamaged, (400,200))
        self.boatRepaired = pygame.transform.scale(boatRepaired, (400,200))
        self.boatGold = pygame.transform.scale(boatGold, (400,200))

        self.treasure = pygame.image.load('treasure2.png').convert_alpha()
        self.emptyTreasure = pygame.image.load('emptyTreasure.png').convert_alpha()
        self.board = pygame.image.load('board1.png').convert_alpha()
        self.rain1 = pygame.image.load('rain1.png').convert_alpha()
        self.rain2 = pygame.image.load('rain2.png').convert_alpha()
        self.rain3 = pygame.image.load('rain3.png').convert_alpha()
        self.rainList = [self.rain1,self.rain2,self.rain3,self.rain1,self.rain2,self.rain3,self.rain1,self.rain2,self.rain3,self.rain1,self.rain2,self.rain3]

        self.pauseScreen = pygame.image.load('pauseScreen.png')

        self.sail1 = pygame.image.load('sail1.png')
        self.sail2 = pygame.image.load('sail2.png')
        self.sail3 = pygame.image.load('sail3.png')
        self.sailList = [self.sail1,self.sail2,self.sail3,self.sail1,self.sail2,self.sail3,self.sail1,self.sail2,self.sail3,self.sail1,self.sail2,self.sail3]

        self.startText = self.myFont.render("Press SPACE to start", 1, "white")

        # for finding pixel color at postion
        self.map_image = pygame.image.load('mapbw.png').convert()
        # background pages
        self.cSquare = pygame.image.load('mapColor.png').convert()
        self.cSprites = SpriteSheet('mapColor.png', mapList)
        self.bSprites = SpriteSheet('mapbw.png', mapList)
        idleSpriteSheet = SpriteSheet('Ghost.png', idleSprites)
        runSpriteSheet = SpriteSheet('Run-Sheet.png', runSprites)

        self.facingRight = False
        self.animIndex = 0

        self.spriteSheets = {
            'IDLE' : idleSpriteSheet,
            'RUN' : runSpriteSheet
        }

        self.anim = 'IDLE'
        self.animSpeed = 0.005
        self.animInc = 0

        self.square = 4
        self.sq = self.cSprites.getSprites(False)[self.square]
        self.bg = self.bSprites.getSprites(False)[self.square]
        

        self.xPos = 80
        self.yPos = 100
        self.speed = PLAYER_SPEED
        # random square for treasure
        tLoc = [0,1,2,3,5,6,7,8]
        self.treasureLocation   = [random.choice(tLoc),(random.randint(100,350),random.randint(100,350)),False]
        # random positions for boards
        bLoc1 = [0,1]
        bLoc2 = [2,3]
        bLoc3 = [5,6]
        bLoc4 = [7,8]
        self.boardLocations = []
        self.boardLocations.append((random.choice(bLoc1),(random.randint(100,350),random.randint(100,350)),False))
        self.boardLocations.append((random.choice(bLoc2),(random.randint(100,350),random.randint(100,350)),False))
        self.boardLocations.append((random.choice(bLoc3),(random.randint(100,350),random.randint(100,350)),False))
        self.boardLocations.append((random.choice(bLoc4),(random.randint(100,350),random.randint(100,350)),False))
        # boat location
        self.boatLocation = [4,(80,100),0]

        self.image = self.spriteSheets[self.anim].getSprites(flipped = not self.facingRight)[0]
        self.rect = self.image.get_rect(center=(self.xPos, self.yPos))

        self.boardsCollected = 0
        self.goldCollected = 0
        self.pause = True
        self.canSail = False
        self.showSailScreen = False

    def walkable(self):
        x = (int(self.xPos + 22))
        y = (int(self.yPos + 52))
        try:
            pixel = self.bg.get_at((x,y))
            if (pixel[:3] != (0,0,0)): #black
                self.speed = PLAYER_SPEED / 4
            else:
                self.speed = PLAYER_SPEED
        except:
            self.speed = PLAYER_SPEED


    def run(self):
        run = True
        while run:
            key = pygame.key.get_pressed()
            # Event handling for quitting the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif key[pygame.K_ESCAPE]:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.pause = not self.pause

            self.selectSquare(self.xPos, self.yPos)
            self.walkable()

            self.anim = 'IDLE'

            
            if key[pygame.K_w]:
                self.yPos -= self.speed
                self.anim = 'RUN'
            if key[pygame.K_s]:
                self.yPos += self.speed
                self.anim = 'RUN'
            if key[pygame.K_a]:
                self.xPos -= self.speed
                self.facingRight = False
                self.anim = 'RUN'
            if key[pygame.K_d]:
                self.xPos += self.speed
                self.facingRight = True
                self.anim = 'RUN'
            if key[pygame.K_RETURN] and self.canSail:
                self.showSailScreen = True
            
            self.move()

            self.animInc += self.animSpeed
            if self.animInc >= 1:
                self.animIndex += int(self.animInc)
                self.animInc = 0  # Reset after applying frame change

            if (self.animIndex >= len(self.spriteSheets[self.anim].getSprites(False))):
                self.animIndex = 0
            self.image = self.spriteSheets[self.anim].getSprites(flipped = not self.facingRight)[self.animIndex]

            self.collisions()
            
            # blit position for boards
            for tup in self.boardLocations:
                if (self.square == tup[0]):
                    coord = tup[1]
                    collected = tup[2]

            # displays for wood and gold
            if self.goldCollected >= 1000:
                self.goldCollected = 1000
            boardsCollectedDisplay = self.myFont.render("Wood: " + str(self.boardsCollected), 1, "white")
            goldCollectedDisplay = self.myFont.render("Gold: " + str(self.goldCollected), 1, "yellow")
            sailDisplay = self.myFont.render("Press enter to sail",1,"white")

            # clear background
            self.screen.fill((0,0,0))
            # self.screen.blit(self.bg,(0,0))
            self.screen.blit(self.sq,(0,0))
            #treasure
            if (self.square == self.treasureLocation[0]):
                if (not self.treasureLocation[2]):
                    self.screen.blit(self.treasure,self.treasureLocation[1])
                else:
                    self.screen.blit(self.emptyTreasure,self.treasureLocation[1])
            # boards
            if (any(self.square == tuple[0] for tuple in self.boardLocations)):
                if (not collected):
                    self.screen.blit(self.board,(coord))
            # boats
            if (self.square == 4):
                if self.boatLocation[2] == 1:
                    self.screen.blit(self.boatRepaired,self.boatLocation[1])
                elif self.boatLocation[2] == 2:
                    self.screen.blit(self.boatGold,self.boatLocation[1])
                    self.screen.blit(sailDisplay,(175,300))
                    self.canSail = True
                else:
                    self.screen.blit(self.boatDamaged,self.boatLocation[1])
            # character
            self.screen.blit(self.image,(self.rect.centerx,self.rect.centery))
            # boards collected and gold
            self.screen.blit(boardsCollectedDisplay,(40,40))
            self.screen.blit(goldCollectedDisplay,(400,40))
            # pause/start screen
            if (self.pause):
                self.screen.blit(self.pauseScreen,(0,0))
                self.screen.blit(self.startText,(175,300))
            # sail screen
            if self.showSailScreen:
                self.screen.blit(self.sailList[self.animIndex],(0,0))
            # rain
            self.screen.blit(self.rainList[self.animIndex],(0,0))
            

            
                

            pygame.display.flip()
    
    def move(self):
        self.rect.centerx = round(self.xPos)
        self.rect.centery = round(self.yPos)
        
    def selectSquare(self, x, y):
        temp = self.square
        if (x <= 0):
            if (self.square == 0 or self.square == 3 or self.square == 6):
                self.xPos = 1
                return
            else:
                self.square -= 1
                self.xPos = SCREEN_WIDTH - 21
        elif (x >= SCREEN_WIDTH - 21):
            if (self.square == 2 or self.square == 5 or self.square == 8):
                self.xPos = SCREEN_WIDTH - 21
                return
            else:
                self.square += 1
                self.xPos = 1
        elif (y <= 0):
            if (self.square == 0 or self.square == 1 or self.square == 2):
                self.yPos = 1
                return
            else:
                self.square -= 3
                self.yPos = SCREEN_HEIGHT - 52 # 52 is player height
        elif (y >= SCREEN_HEIGHT - 52):
            if (self.square == 6 or self.square == 7 or self.square == 8):
                self.yPos = SCREEN_HEIGHT - 52
                return
            else:
                self.square += 3
                self.yPos = 1
        if (0 <= self.square <= 8):
            self.sq = self.cSprites.getSprites(False)[self.square]
            self.bg = self.bSprites.getSprites(False)[self.square]
        else: 
            self.square = temp
            self.sq = self.cSprites.getSprites(False)[self.square]
            self.bg = self.bSprites.getSprites(False)[self.square]

    def collisions(self):
        x = int(self.xPos)
        y = int(self.yPos)
        for tup in self.boardLocations:
            loc = tup[1]

            if (self.square == tup[0] and (x-50) <= loc[0]+70 <= (x+50) and (y-50) <= loc[1]+20 <= (y+50)):
                i = self.boardLocations.index(tup) # returns index of square's location in the list
                a = tup[0]
                b = tup[1]
                c = tup[2]
                if(not c):
                    self.boardLocations[i] = (a,b,True)
                    self.boardsCollected += 1
        tLoc = self.treasureLocation[1]
        if ((self.square == self.treasureLocation[0]) and (x-50 <= tLoc[0]+100 <= x+50) and (y-50 <= tLoc[1]+20 <= y+50)):
            self.goldCollected += 1
            self.treasureLocation[2] = True
            
        bLoc = self.boatLocation[1]
        if (self.square == self.boatLocation[0] and (x-50 <= bLoc[0]+190 <= x+50) and (y-50 <= bLoc[1]+160 <= y+50)):
            if self.boardsCollected == 4:
                self.boatLocation[2] = 1
            if self.treasureLocation[2]:
                self.boatLocation[2] = 2
