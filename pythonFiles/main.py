import pygame, sys, math
from button import Button


pygame.init()


WIDTH, HEIGHT = 600, 600 # Width and Height of the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255) # The color white
JUMPDURATION = 100 # Jump duration in game ticks
SPEED = 0.7 # Character speed in pixels per game tick
STARTPOSX = 5 # Start position on the x axis
STARTPOSY = HEIGHT - 50 # Start position on the y axis
gravityConstant = .028 # Gravity constant in pixels per game tick
file_path = 'levels.txt' # File path for textfile with all the levels
levelNr = 0
nrOfDeaths = 0
clock = pygame.time.Clock() # Used to control the speed of the game
FPS = 240 # Frames per second (game ticks per second)
characterOnPlatformList = []
characterOnPlatform = False
timeKeyPressed_W = 0
timeKeyPressed_Up = 0
keyPressDownCntCharacter1 = 0
keyPressUppCntCharacter1 = 0
keyPressDownCntCharacter2 = 0
keyPressUppCntCharacter2 = 0
w, h = 100, 200
keyPress = {"w": False, "a": False, "s": False, "d": False, "up": False, "left": False, "right": False, "down": False}
running = False
collisionOn = True

p1Image = pygame.image.load('images\p1.png')
p2Image = pygame.image.load('images\p2.png')
grassImage = pygame.image.load('images\Grass.png')
dirtImage = pygame.image.load('images\Dirt.png')
goalImage = pygame.image.load('images\Goal.png')
metalImage = pygame.image.load('images\metal.png')
#########################################################################


# Create the game window  
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BIGBOYCOOLPROJECT :)")


#########################################################################


class Character: # A class for the creation of a characters
    def __init__(self, x, y, width, height, image, speed):
        self.rect = pygame.Rect(x, y, width, height) #hitbox
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.speed = speed
        self.vY = 0 
        self.vX = 0 
        self.spikeCollision = {"right": False, "left": False, "upp": False, "down": False}
        
    def draw(self):
        screen.blit(self.image, (self.x,self.y))
        #pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
       
class Obstacle: # A class for the creation of a obstacles
    def __init__(self, x, y, width, height, color,trianglePoints):
        self.rect = pygame.Rect(x, y, width, height) # hitbox
        self.trianglePoints = trianglePoints
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.outlineColor = (80,80,80)

    def draw(self):
        pygame.draw.polygon(screen, self.color, self.trianglePoints)
        pygame.draw.polygon(screen, self.outlineColor, self.trianglePoints, 2)
    
    def drawHitbox(self):
        pygame.draw.rect(screen, (255,0,0), (self.x, self.y, self.width, self.height))
               
class Platform: # A class for the creation of a platforms
    def __init__(self, x, y, width, height, image):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image
    def draw(self):
        #pygame.draw.rect(screen, self.color, self.rect)
        if self.image == grassImage:
            screen.blit(self.image, (self.rect.x, self.rect.y-2))
        elif self.image == dirtImage:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        elif self.image == metalImage:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        
class winArea: # A class for the creation of a Win Area
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
    def draw(self):
        screen.blit(goalImage, (self.rect.x, self.rect.y))



#########################################################################

levels = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 
0, 0, 0, 0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.25, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.0, 2.0, 2.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
0, 1.0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.0, 2.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.5, 2.5, 2.5, 2.5, 2.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.0, 2.0, 2.0, 2.0, 2.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5.0, 0, 5.0, 5.0, 5.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5.0, 0, 5.0, 0, 0, 2.25, 2.75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5.0, 0, 5.0, 0, 0, 0, 0, 0, 2.25, 2.75, 2.25, 2.75, 0, 5.0, 5.0, 5.0, 0, 0, 0, 0, 5.0, 5.0, 5.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5.0, 0, 5.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5.0, 0, 5.0, 0, 2.25, 2.75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5.0, 0, 0, 5.0, 5.0, 5.0, 0, 0, 0, 0, 2.25, 2.75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5.0, 0, 5.0, 2.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5.0, 0, 5.0, 2.5, 0, 0, 0, 0, 0, 0, 0, 0, 5.0, 5.0, 5.0, 0, 0, 0, 0, 0, 5.0, 5.0, 5.0, 0, 0, 2.25, 2.75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5.0, 0, 5.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5.0, 0, 5.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5.0, 5.0, 5.0, 0, 5.0, 5.0, 5.0, 0, 0, 0, 0, 0, 0, 2.25, 2.75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5.0, 0, 5.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5.0, 0, 5.0, 0, 0, 0, 0, 0, 0, 0, 3.0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 4.0, 1.0, 4.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3.0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 2.0, 0, 0, 0, 0, 0, 0, 0, 2.0, 2.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 0, 0, 0, 0, 0, 0, 2.0, 2.5, 0, 0, 0, 0, 0,  
0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 2.75, 0, 0, 0, 2.5, 0, 0, 0, 0, 0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 2.0, 2.0, 2.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 0, 0, 0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 0, 0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 0, 0, 0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0],[0, 0, 0, 0, 0, 0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 2.75, 0, 0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 2.5, 4.0, 4.0, 4.0, 4.0, 2.5, 2.5, 2.5, 2.5, 2.5, 0, 0, 3.0, 4.0, 2.75, 2.5, 4.0, 4.0, 4.0, 2.5, 0, 2.5, 2.5, 2.5, 2.5, 0, 0, 0, 0, 0, 0, 0, 0, 4.0, 2.75, 0, 2.5, 2.5, 2.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.25, 1.0, 2.75, 0, 0, 4.0, 2.75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.5, 0, 0, 0, 4.0, 2.75, 0, 0, 0, 0, 0, 2.0, 2.0, 2.0, 0, 2.0, 2.0, 2.0, 0, 2.0, 2.0, 2.0, 0, 0, 4.0, 2.75, 0, 0, 0, 0, 1.0, 
1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0, 0, 4.0, 2.75, 0, 0, 0, 0, 0, 0, 0, 0, 4.0, 4.0, 2.5, 2.5, 2.5, 2.5, 2.5, 4.0, 2.0, 2.0, 4.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4.0, 2.75, 0, 0, 0, 2.25, 4.0, 1.0, 1.0, 4.0, 0, 2.0, 0, 2.0, 2.0, 0, 0, 0, 0, 0, 2.5, 0, 0, 0, 0, 2.25, 4.0, 4.0, 4.0, 4.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 2.0, 0, 0, 0, 0, 2.25, 4.0, 4.0, 4.0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 2.25, 4.0, 4.0, 4.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4.0, 0, 0, 0, 0, 0, 4.0, 4.0, 4.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4.0, 0, 0, 0, 0, 0, 2.5, 4.0, 4.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4.0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 2.5, 0, 0, 0, 0, 0, 2.25, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4.0, 4.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4.0, 4.0, 0, 0, 0, 1.0, 0, 0, 1.0, 0, 0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 4.0, 4.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 4.0, 4.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],[4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 0, 0, 0, 0, 0, 0, 0, 4.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4.0, 4.0, 0, 0, 0, 0, 0, 0, 0, 4.0, 0, 0, 0, 0, 2.0, 2.0, 0, 0, 0, 0, 4.0, 4.0, 0, 3.0, 0, 0, 0, 0, 0, 2.0, 0, 0, 2.25, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 0, 4.0, 4.0, 0, 0, 2.0, 2.0, 0, 0, 0, 1.5, 0, 0, 1.5, 4.0, 2.5, 2.5, 2.5, 4.0, 2.75, 0, 4.0, 4.0, 1.5, 1.5, 1.5, 1.5, 2.75, 0, 0, 0, 0, 0, 0, 4.0, 2.75, 0, 2.25, 4.0, 1.5, 0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 2.75, 0, 0, 0, 0, 0, 2.25, 4.0, 2.75, 0, 2.25, 4.0, 2.75, 0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 2.75, 0, 0, 0, 0, 0, 1.5, 4.0, 2.75, 0, 2.25, 4.0, 1.0, 0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 2.75, 0, 1.5, 0, 0, 0, 2.25, 4.0, 2.75, 0, 2.25, 4.0, 0, 2.25, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 2.75, 0, 2.25, 1.0, 2.75, 0, 0, 2.5, 0, 0, 2.25, 4.0, 2.75, 0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 2.75, 0, 2.25, 4.0, 2.75, 0, 2.0, 0, 0, 0, 2.25, 4.0, 0, 0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 2.75, 0, 2.25, 4.0, 1.0, 1.0, 1.0, 0, 2.0, 0, 2.0, 4.0, 0, 2.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 1.5, 0, 2.25, 4.0, 4.0, 4.0, 4.0, 1.0, 1.0, 0, 1.0, 4.0, 0, 1.5, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 2.75, 0, 2.25, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 0, 4.0, 2.75, 0, 2.25, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 2.75, 0, 2.25, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 0, 4.0, 2.75, 0, 2.25, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 2.75, 0, 2.25, 4.0, 4.0, 4.0, 0, 2.5, 0, 0, 4.0, 2.75, 0, 2.25, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 2.75, 0, 1.5, 0, 0, 0, 0, 0, 1.0, 1.0, 4.0, 2.75, 0, 0, 2.25, 4.0, 4.0, 4.0, 4.0, 4.0, 2.75, 0, 0, 0, 0, 0, 0, 0, 0, 4.0, 0, 0, 0, 0, 0, 2.5, 2.5, 4.0, 4.0, 4.0, 2.75, 0, 0, 0, 0, 0, 0, 0, 0, 4.0, 2.0, 2.0, 2.0, 2.0, 0, 2.0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 4.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],[0, 0, 0, 0, 0, 0, 2.25, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 2.5, 2.5, 2.5, 5.0, 2.0, 0, 5.0, 2.75, 0, 0, 2.25, 5.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.0, 0, 5.0, 2.5, 0, 5.0, 2.75, 0, 0, 2.25, 5.0, 0, 0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 0, 5.0, 0, 0, 5.0, 2.75, 0, 0, 2.0, 5.0, 0, 2.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 0, 5.0, 0, 2.0, 5.0, 2.75, 0, 0, 5.0, 5.0, 0, 2.5, 5.0, 5.0, 
5.0, 5.0, 5.0, 5.0, 5.0, 2.0, 0, 5.0, 0, 2.5, 5.0, 2.75, 0, 0, 0, 5.0, 0, 0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 0, 5.0, 2.0, 0, 5.0, 2.75, 0, 0, 5.0, 5.0, 2.0, 0, 5.0, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 0, 0, 5.0, 2.5, 0, 5.0, 2.75, 0, 0, 0, 5.0, 2.5, 0, 5.0, 2.25, 2.75, 0, 2.0, 2.25, 2.75, 0, 0, 5.0, 0, 2.0, 5.0, 0, 0, 0, 0, 5.0, 0, 0, 5.0, 0, 2.0, 0, 2.5, 0, 0, 0, 0, 5.0, 0, 2.5, 5.0, 5.0, 0, 
0, 0, 5.0, 0, 0, 5.0, 0, 2.5, 0, 0, 5.0, 5.0, 5.0, 5.0, 5.0, 2.0, 0, 5.0, 0, 0, 2.0, 0, 5.0, 0, 2.0, 5.0, 0, 2.0, 0, 2.25, 2.75, 0, 0, 0, 5.0, 2.5, 0, 5.0, 0, 2.25, 5.0, 0, 0, 0, 2.5, 5.0, 0, 2.5, 0, 0, 0, 0, 2.0, 0, 5.0, 0, 3.0, 5.0, 2.0, 2.0, 5.0, 0, 0, 0, 2.25, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 2.0, 2.0, 2.0, 2.0, 5.0, 0, 0, 0, 0, 0, 0, 0, 0, 5.0, 2.75, 2.25, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 0, 5.0, 5.0, 5.0, 5.0, 5.0, 2.0, 2.0, 5.0, 5.0, 5.0, 5.0, 2.5, 5.0, 0, 2.25, 5.0, 5.0, 5.0, 5.0, 0, 5.0, 0, 0, 0, 5.0, 5.0, 5.0, 5.0, 2.75, 2.25, 5.0, 2.0, 5.0, 0, 2.25, 0, 0, 2.25, 5.0, 0, 0, 0, 2.0, 2.0, 0, 0, 0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 0, 2.25, 2.25, 2.5, 2.25, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 0, 5.0, 0, 0, 0, 0, 0, 0, 0, 0, 2.75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0]]


#def read_lists_from_file(filename): # Reads levels.txt to load maps
#    with open(filename, 'r') as file:
#        lists = []
#        for line in file:
#            elements = line.strip().split(', ')  # Assuming elements are separated by a comma and a space
#            list_data = [element.strip() for element in elements]
#            lists.append(list_data)
#    return lists 

def makeLevel(level): # Ask David
    cnt = 0
    width = 30
    height = 30
    spikeWidth = 20
    spikeHeight = 7
    
    for x in range(20):
        for y in range(20):
            if math.floor(level[cnt]) == 1:
                platform = Platform(y*30, x*30,width,height, grassImage)
                Platforms.append(platform) 
                
            elif math.floor(level[cnt]) == 2:
                if level[cnt]%1 == 0:
                    triangle_points = [(y*30, x*30+30), (y*30 +15, x*30+15), (y*30+30, x*30+30)]
                    xS = triangle_points[0][0] + (30 - spikeWidth)/2
                    yS = triangle_points[0][1] - spikeHeight
                    obstacle = Obstacle(xS, yS, spikeWidth, spikeHeight, (128,128,128), triangle_points)
                    Obstacles.append(obstacle)
                    
                elif level[cnt]%1 == 0.25:
                    triangle_points = [(y*30+30, x*30), (y*30 +15, x*30+15), (y*30+30, x*30+30)]
                    xS = triangle_points[0][0] - (spikeHeight)
                    yS = triangle_points[0][1] + (30-spikeWidth)/2
                    obstacle = Obstacle(xS, yS, spikeHeight, spikeWidth, (128,128,128), triangle_points)
                    Obstacles.append(obstacle)
                    
                elif level[cnt]%1 == 0.5:
                    triangle_points = [(y*30, x*30), (y*30 +15, x*30+15), (y*30+30, x*30)]
                    xS = triangle_points[0][0] + (30 - spikeWidth)/2
                    yS = triangle_points[0][1]
                    obstacle = Obstacle(xS, yS, spikeWidth, spikeHeight, (128,128,128), triangle_points)
                    Obstacles.append(obstacle)
                    
                elif level[cnt]%1 == 0.75:
                    triangle_points = [(y*30, x*30), (y*30 +15, x*30+15), (y*30, x*30+30)]
                    xS = triangle_points[0][0]
                    yS = triangle_points[0][1] + spikeHeight
                    obstacle = Obstacle(xS, yS, spikeHeight, spikeWidth, (128,128,128), triangle_points)
                    Obstacles.append(obstacle)

            elif math.floor(level[cnt]) == 3:
                area = winArea(y*30, x*30,width,height, (255, 0, 0))    ###This should be the finish not a platform... its now a win area :)
                winAreas.append(area) 
            elif math.floor(level[cnt]) == 4: 
                platform = Platform(y*30, x*30,width,height, dirtImage)
                Platforms.append(platform) 
            elif math.floor(level[cnt]) == 5: 
                platform = Platform(y*30, x*30,width,height, metalImage)
                Platforms.append(platform) 
            cnt += 1

def win(): # When you complete a map
    global Obstacles
    global Platforms
    global winAreas
    global levelNr
    
    print(f"You completed area {levelNr+1}!")
    levelNr += 1
    print(levelNr)
    for character in Characters:
        character.x = STARTPOSX
        character.y = STARTPOSY
        
    Obstacles = []
    Platforms = []
    winAreas = [] 
    if levelNr < len(levels):
        makeLevel(levels[levelNr])
    else:
        mainMenu()
        levelNr = 0
    
    

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("images/font.ttf", size)

#########################################################################

      
Obstacles = [] # A list of all the obstacles

    
Characters = [Character(STARTPOSX, STARTPOSY, 20, 20, p1Image, SPEED), Character(STARTPOSX, STARTPOSY, 20, 20, p2Image, SPEED)] # A list of all the characters


Platforms = [] # A list of all the platforms


winAreas = [] # A list of all the win areas :)


#########################################################################


def winCollision(character, platform): # Function that checks if you colide with the block that makes you win
    try: 
       character.rect.colliderect(platform.rect)
    except:
        screen.fill("white")
    else: 
        if character.rect.colliderect(platform.rect):
            win()

characterOnPlatform = True 


#########################################################################


def spikeCollision(character, obj): # Function for testing spikeCollision and plays a sound if you collided and then exits the game
    global nrOfDeaths
    global running
    if character.rect.colliderect(obj.rect) and collisionOn:
        character.x = STARTPOSX
        character.y = STARTPOSY
        character.rect.x = STARTPOSX
        character.rect.y = STARTPOSY
          


#########################################################################




def gravity(character): # Functions that handles gravity move0ment
    if character.y < HEIGHT - character.height:
        if character.vY < 2 and not character.spikeCollision["down"]:
            character.vY += gravityConstant


def boarder(character):
    if character.x < 0:
        character.x = 0
    if character.x + character.width > WIDTH:
        character.x = WIDTH - character.width
    if character.y < 0:
        character.y = 0
    if character.y + character.height > HEIGHT:
        character.y = HEIGHT - character.height


def jumpCounter():
    global keyPressDownCntCharacter1
    global keyPressUppCntCharacter1
    global keyPressDownCntCharacter2
    global keyPressUppCntCharacter2
    global timeKeyPressed_W
    global timeKeyPressed_Up
    if keyPress["w"]:
        keyPressDownCntCharacter1 = 1
    if not keyPress["w"] and keyPressDownCntCharacter1 == 1: 
        keyPressUppCntCharacter1 += 1
        keyPressDownCntCharacter1 = 0
        timeKeyPressed_W = 0
    if keyPress["up"]:
        keyPressDownCntCharacter2 = 1
    if not keyPress["up"] and keyPressDownCntCharacter2 == 1: 
        keyPressUppCntCharacter2 += 1
        keyPressDownCntCharacter2 = 0
        timeKeyPressed_Up = 0
        
maxJumps = 2


def characterVelocity(character): # Handle character move0ment WASD   
    global timeKeyPressed_W
    global timeKeyPressed_Up
    
    if character == Characters[0] and keyPress["a"] and not keyPress["d"]:
        character.vX = -SPEED
    elif character == Characters[0] and keyPress["d"] and not keyPress["a"]:
        character.vX = SPEED
    elif  character == Characters[1] and keyPress["left"] and not keyPress["right"]:
        character.vX = -SPEED
    elif  character == Characters[1] and keyPress["right"] and not keyPress["left"]:
        character.vX = SPEED
    else:
        character.vX = 0
        
        
    if character == Characters[0] and keyPress["w"] and timeKeyPressed_W < 40 and keyPressUppCntCharacter1 < maxJumps:
        timeKeyPressed_W += 1
        character.vY = -1.1        
        
    if character == Characters[1] and keyPress["up"] and timeKeyPressed_Up < 40 and keyPressUppCntCharacter2 < maxJumps:
        timeKeyPressed_Up += 1
        character.vY = -1.1


def collision(character): # Function that handles spikeCollision detection between platforms and characters
    global timeKeyPressed_W
    global timeKeyPressed_Up
    global jumpReset
    global jump
    global keyPressUppCntCharacter1
    global keyPressUppCntCharacter2
    
    character.spikeCollision = {"right": False, "left": False, "upp": False, "down": False}
    character.x += character.vX
    character.rect.x = character.x
    
    for platformNr in Platforms:
        platform = platformNr

        if character.rect.colliderect(platform.rect):
            if character.vX > 0:
                character.x = platform.rect.left - character.width
                character.spikeCollision["right"]  = True 
            if character.vX < 0:
                character.x = platform.rect.right
                character.spikeCollision["left"]  = True

    character.rect.x = character.x

    character.y += character.vY
    character.rect.y = character.y

    for platformNr in Platforms:
        platform = platformNr
        
        if character.rect.colliderect(platform.rect):
            if character == Characters[0] and character.vY > 0:
                character.y = platform.rect.top - character.height
                character.spikeCollision["down"] = True
                character.vY = 0
                timeKeyPressed_W = 0
                keyPressUppCntCharacter1 = 0

            if character == Characters[0] and character.vY < 0:
               character.y = platform.rect.bottom
               character.spikeCollision["upp"] = True 
               character.vY = 0

            if character == Characters[1] and character.vY > 0:
                character.y = platform.rect.top - character.height
                character.spikeCollision["down"] = True
                character.vY = 0
                timeKeyPressed_Up = 0
                keyPressUppCntCharacter2 = 0

            if character == Characters[1] and character.vY < 0:
               character.y = platform.rect.bottom
               character.spikeCollision["upp"] = True 
               character.vY = 0
               
               
    character.rect.y = character.y

   
#########################################################################        
def toggleFullscreen():
    global screen
    if not screen.get_flags() & pygame.FULLSCREEN:
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))

makeLevel(levels[0]) # Loads the level

def toggleCollision():
    global collisionOn
    if not collisionOn:
        collisionOn = True
    else:
        collisionOn = False




#########################################################################
def mainLoop():
    global STARTPOSX
    global STARTPOSY
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                keyPress["a"] = True
            if event.key == pygame.K_d:
                keyPress["d"] = True
            if event.key == pygame.K_w or event.key == pygame.K_KP0:
                keyPress["w"] = True
            if event.key == pygame.K_s:
                keyPress["s"] = True
            if event.key == pygame.K_LEFT:
                keyPress["left"] = True
            if event.key == pygame.K_RIGHT:
                keyPress["right"] = True
            if event.key == pygame.K_UP:
                keyPress["up"] = True
            if event.key == pygame.K_DOWN:
                keyPress["down"] = True                
            if event.key == pygame.K_F11:
                toggleFullscreen()
            if event.key == pygame.K_F5:
                toggleCollision()
            if event.key == pygame.K_F4:
                STARTPOSX = Characters[0].x
                STARTPOSY = Characters[0].y
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                keyPress["a"] = False
            if event.key == pygame.K_d:
                keyPress["d"] = False
            if event.key == pygame.K_w or event.key == pygame.K_KP0:
                keyPress["w"] = False
            if event.key == pygame.K_s:
                keyPress["s"] = False
            if event.key == pygame.K_LEFT:
                keyPress["left"] = False
            if event.key == pygame.K_RIGHT:
                keyPress["right"] = False
            if event.key == pygame.K_UP:
                keyPress["up"] = False
            if event.key == pygame.K_DOWN:
                keyPress["down"] = False
#########################################################################   


   #Calls function that handles spikeCollision
    for character in Characters:
        for obstacle in Obstacles:
            spikeCollision(character, obstacle)


########################################################################


    #Calls function that handles Platform spikeCollision

    #collision(Characters[0])
    #collision(Characters[1])
    
    for character in Characters:
        collision(character)
        characterVelocity(character)
        gravity(character)
        boarder(character)


    jumpCounter()
    
    #Calls function that checks if you won
    for winArea in winAreas:
        for character in Characters:
            winCollision(character, winArea)
        #winCollision(Characters[1], winAreas[i])

   

#########################################################################  
  
  
  
  
    # Clear the screen
    screen.fill((46, 203, 255))


#########################################################################


    # Draw the character & obstacles & platforms
    for charater in Characters:
        charater.draw()
    
    for obstacle in Obstacles:
        obstacle.draw()
    
    for platform in Platforms:
        platform.draw()
    
    for winArea in winAreas:
        winArea.draw()
    
    

#########################################################################

    # Update the display
    pygame.display.update()

    clock.tick(FPS)
    
#########################################################################
def play():
    while True:
       mainLoop()
    
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("white")
        
        OPTIONS_TEXT0 = get_font(10).render("This is the controlls screen.", True, "Black")
        OPTIONS_RECT0 = OPTIONS_TEXT0.get_rect(center=(WIDTH/2, 100))
        
        OPTIONS_TEXT1 = get_font(9).render("Player ONE uses WASD to controll the it's character", True, "Black")
        OPTIONS_RECT1 = OPTIONS_TEXT1.get_rect(center=(WIDTH/2, 150))
        
        OPTIONS_TEXT2 = get_font(9).render("Player TWO uses the arrow keys to controll the it's character", True, "Black")
        OPTIONS_RECT2 = OPTIONS_TEXT2.get_rect(center=(WIDTH/2, 200))
        
        screen.blit(OPTIONS_TEXT0, OPTIONS_RECT0)
        screen.blit(OPTIONS_TEXT1, OPTIONS_RECT1)
        screen.blit(OPTIONS_TEXT2, OPTIONS_RECT2)


        OPTIONS_BACK = Button(image=None, pos=(WIDTH/2, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    mainMenu()

        pygame.display.update()



def mainMenu():
    while True:
        screen.fill("black")

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(30).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH/2, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("images/Play Rect.png"), pos=(WIDTH/2, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("images/Options Rect.png"), pos=(WIDTH/2, 375), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("images/Quit Rect.png"), pos=(WIDTH/2, 500), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

mainMenu()
    
