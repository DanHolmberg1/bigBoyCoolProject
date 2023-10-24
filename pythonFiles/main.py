import pygame
import sys
import math

pygame.init()


WIDTH, HEIGHT = 600, 600 # Width and Height of the window
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



#########################################################################


# Create the game window  
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BIGBOYCOOLPROJECT :)")


#########################################################################


class Character: # A class for the creation of a characters
    def __init__(self, x, y, width, height, color, speed):
        self.rect = pygame.Rect(x, y, width, height) #hitbox
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        self.vY = 0 
        self.vX = 0 
        self.spikeCollision = {"right": False, "left": False, "upp": False, "down": False}
        
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
       
class Obstacle: # A class for the creation of a obstacles
    def __init__(self, x, y, width, height, color,trianglePoints):
        self.rect = pygame.Rect(x, y, width, height) # hitbox
        self.trianglePoints = trianglePoints
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        pygame.draw.polygon(screen, self.color, self.trianglePoints)
    
    def drawHitbox(self):
        pygame.draw.rect(screen, (255,0,0), (self.x, self.y, self.width, self.height))
               
class Platform: # A class for the creation of a platforms
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        
class winArea: # A class for the creation of a Win Area
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)



#########################################################################

levels = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 0, 0, 0, 0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.25, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.0, 2.0, 2.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.0, 2.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.5, 2.5, 2.5, 2.5, 2.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 2.0, 2.0, 2.0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3.0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 2.0, 0, 0, 0, 0, 0, 0, 0, 2.0, 2.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 0, 0, 0, 0, 0, 0, 2.0, 2.5, 0, 0, 0, 0, 0, 
0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 2.75, 0, 0, 0, 2.5, 0, 0, 0, 0, 0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 2.0, 2.0, 2.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 0, 0, 0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 0, 0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 0, 0, 0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0],[0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.75, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.5, 1.0, 1.0, 1.0, 1.0, 2.5, 2.5, 2.5, 2.5, 2.5, 0, 0, 3.0, 1.0, 2.75, 2.5, 1.0, 1.0, 1.0, 2.5, 0, 2.5, 2.5, 2.5, 2.5, 0, 0, 0, 0, 0, 0, 0, 0, 1.5, 2.75, 0, 2.5, 2.5, 2.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.25, 1.0, 2.75, 0, 0, 1.0, 2.75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.5, 0, 0, 0, 1.0, 2.75, 0, 0, 0, 0, 0, 2.0, 2.0, 2.0, 0, 2.0, 2.0, 2.0, 0, 2.0, 2.0, 2.0, 0, 0, 1.0, 2.75, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0, 0, 1.0, 2.75, 0, 0, 0, 0, 0, 0, 0, 
0, 1.0, 1.0, 2.5, 2.5, 2.5, 2.5, 2.5, 1.0, 2.0, 2.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 2.75, 0, 0, 0, 2.25, 1.0, 1.0, 1.0, 1.0, 0, 2.0, 0, 2.0, 2.0, 0, 0, 0, 0, 0, 2.5, 0, 0, 0, 0, 2.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 2.0, 0, 0, 0, 0, 2.25, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 2.25, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 
0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 0, 0, 0, 0, 0, 2.5, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 2.5, 0, 0, 0, 0, 0, 2.25, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 0, 0, 0, 1.0, 0, 0, 1.0, 0, 0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]



def read_lists_from_file(filename): # Reads levels.txt to load maps
    with open(filename, 'r') as file:
        lists = []
        for line in file:
            elements = line.strip().split(', ')  # Assuming elements are separated by a comma and a space
            list_data = [element.strip() for element in elements]
            lists.append(list_data)
    return lists 


def makeLevel(level): # Ask David
    cnt = 0
    width = 30
    height = 30
    spikeWidth = 20
    spikeHeight = 7
    for x in range(20):
        for y in range(20):
            if math.floor(level[cnt]) == 1:
                platform = Platform(y*30, x*30,width,height, (150, 75, 0))
                Platforms.append(platform) 
            elif math.floor(level[cnt]) == 2:
                #print("hello")
                if level[cnt]%1 == 0:
                    #print("hello1")
                    triangle_points = [(y*30, x*30+30), (y*30 +15, x*30+15), (y*30+30, x*30+30)]
                    xS = triangle_points[0][0] + (30 - spikeWidth)/2
                    yS = triangle_points[0][1] - spikeHeight
                    obstacle = Obstacle(xS, yS, spikeWidth, spikeHeight, (128,128,128), triangle_points)
                    Obstacles.append(obstacle)
                elif level[cnt]%1 == 0.25: 
                    #print("hello2")
                    triangle_points = [(y*30+30, x*30), (y*30 +15, x*30+15), (y*30+30, x*30+30)]
                    xS = triangle_points[0][0] - (spikeHeight)
                    yS = triangle_points[0][1] + (30-spikeWidth)/2
                    obstacle = Obstacle(xS, yS, spikeHeight, spikeWidth, (128,128,128), triangle_points)
                    Obstacles.append(obstacle)
                elif level[cnt]%1 == 0.5:
                    #print("hello3")
                    triangle_points = [(y*30, x*30), (y*30 +15, x*30+15), (y*30+30, x*30)]
                    xS = triangle_points[0][0] + (30 - spikeWidth)/2
                    yS = triangle_points[0][1]
                    obstacle = Obstacle(xS, yS, spikeWidth, spikeHeight, (128,128,128), triangle_points)
                    Obstacles.append(obstacle)
                elif level[cnt]%1 == 0.75:
                    #print("hello4")
                    triangle_points = [(y*30, x*30), (y*30 +15, x*30+15), (y*30, x*30+30)]
                    xS = triangle_points[0][0]
                    yS = triangle_points[0][1] + spikeHeight
                    obstacle = Obstacle(xS, yS, spikeHeight, spikeWidth, (128,128,128), triangle_points)
                    Obstacles.append(obstacle)
              #  print()
            elif math.floor(level[cnt]) == 3:
                area = winArea(y*30, x*30,width,height, (255, 0, 0))    ###This should be the finish not a platform... its now a win area :)
                winAreas.append(area) 
            cnt += 1

def win(): # When you complete a map
    global Obstacles
    global Platforms
    global winAreas
    global levelNr
    
    #pygame.time.delay(int(winSound.get_length()*1000)) # Detta dödar men vi kan skita i den :)
    print(f"You completed area {levelNr+1}!")
    levelNr += 1
    print(levelNr)
    for i in range(len(Characters)):
        Characters[i].x = STARTPOSX
        Characters[i].y = STARTPOSY
        
    Obstacles = []
    Platforms = []
    winAreas = []    
    makeLevel(levels[levelNr])
    
    
    

#########################################################################

      
Obstacles = [] # A list of all the obstacles

    
Characters = [Character(STARTPOSX, STARTPOSY, 20, 20, (255, 100, 100), SPEED)] # A list of all the characters


Platforms = [] # A list of all the platforms


winAreas = [] # A list of all the win areas :)

#########################################################################



#########################################################################


def winCollision(character, platform): # Function that checks if you colide with the block that makes you win
    if character.rect.colliderect(platform.rect):
        win()

characterOnPlatform = True 











#########################################################################



def spikeCollision(character, obj): # Function for testing spikeCollision and plays a sound if you collided and then exits the game
    global nrOfDeaths
    global running
    if character.rect.colliderect(obj.rect):
        nrOfDeaths += 1
        #print(f"You have {3-nrOfDeaths} lifes left!")
        if nrOfDeaths < 1000:
            for i in range(len(Characters)):
                Characters[i].x = STARTPOSX
                Characters[i].y = STARTPOSY
                Characters[i].rect.x = STARTPOSX
                Characters[i].rect.y = STARTPOSY
        else: 
            makeLevel(levels[0])
            nrOfDeaths = 0        


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

keyPressDownCnt = 0
keyPressUppCnt = 0


def jumpCounter():
    global keyPressDownCnt
    global keyPressUppCnt
    global timeKeyPressed_W
    if keyPress["w"]:
        keyPressDownCnt = 1
    if not keyPress["w"] and keyPressDownCnt == 1: 
        keyPressUppCnt += 1
        keyPressDownCnt = 0
        timeKeyPressed_W = 0

        
maxJumps = 2


    


def characterVelocity(character): # Handle character move0ment WASD   

    global timeKeyPressed_W
    if keyPress["a"] and not keyPress["d"]:
        character.vX = -SPEED
    elif keyPress["d"] and not keyPress["a"]:
        character.vX = SPEED
    else:
        character.vX = 0

    if keyPress["w"] and timeKeyPressed_W < 40 and keyPressUppCnt < maxJumps:
        timeKeyPressed_W += 1

        character.vY = -1.1


def collision(character): # Function that handles spikeCollision detection between platforms and characters
    global timeKeyPressed_W
    global jumpReset
    global jump
    global keyPressUppCnt
    characterVelocity(character)
    gravity(character)
    boarder(character)

    character.spikeCollision = {"right": False, "left": False, "upp": False, "down": False}
    character.x += character.vX
    character.rect.x = character.x
    
    for i in range(len(Platforms)):
        platform = Platforms[i]

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

    for i in range(len(Platforms)):
        platform = Platforms[i]
        
        if character.rect.colliderect(platform.rect):
            if character.vY > 0:
                character.y = platform.rect.top - character.height
                character.spikeCollision["down"] = True
                character.vY = 0
                timeKeyPressed_W = 0
                keyPressUppCnt = 0

            if character.vY < 0:
               character.y = platform.rect.bottom
               character.spikeCollision["upp"] = True 
               character.vY = 0

    character.rect.y = character.y

   
#########################################################################        


#levels = read_lists_from_file(file_path)
makeLevel(levels[0]) # Loads the level
# print(imported_lists) Test to see that the levels load correctly

keyPress = {"w": False, "a": False, "s": False, "d": False}

running = True

while running: # Main loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                keyPress["a"] = True
            if event.key == pygame.K_d:
                keyPress["d"] = True
            if event.key == pygame.K_w:
                keyPress["w"] = True
            if event.key == pygame.K_s:
                keyPress["s"] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                keyPress["a"] = False
            if event.key == pygame.K_d:
                keyPress["d"] = False
            if event.key == pygame.K_w:
                keyPress["w"] = False
            if event.key == pygame.K_s:
                keyPress["s"] = False



#########################################################################


    #Calls function that handles movment events
    #move0(Characters[0])


    #print(Characters[0].vY)

#########################################################################   


   #Calls function that handles spikeCollision
    for o in range(len(Characters)):
        for i in range(len(Obstacles)):
            spikeCollision(Characters[o], Obstacles[i])


########################################################################


    #Calls function that handles Platform spikeCollision

    collision(Characters[0])

    jumpCounter()
    

    


    #Calls function that checks if you won
    for i in range(len(winAreas)):
        print(winAreas[i])
        winCollision(Characters[0], winAreas[i])

   

#########################################################################  
 
  
    # Clear the screen
    screen.fill(WHITE)


#########################################################################


    # Draw the character & obstacles & platforms
    for i in range(len(Characters)):
        Characters[i].draw()
    
    for i in range(len(Obstacles)):
        Obstacles[i].draw()
    
    for i in range(len(Platforms)):
        Platforms[i].draw()
    
    for i in range(len(winAreas)):
        winAreas[i].draw()
    
    

#########################################################################

    # Update the display
    pygame.display.update()

    clock.tick(FPS)
    
    
pygame.quit()
sys.exit()
