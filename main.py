import pygame
import sys
import math

pygame.init()


WIDTH, HEIGHT = 600, 600 # Width and Height of the window
WHITE = (255, 255, 255) # The color white
JUMPDURATION = 150 # Jump duration in game ticks
SPEED = 1 # Character speed in pixels per game tick
STARTPOSX = 0 # Start position on the x axis
STARTPOSY = 500 # Start position on the y axis
gravityConstant = .5 # Gravity constant in pixels per game tick
failSound = pygame.mixer.Sound('lossSound.mp3') # Sound for the fail sound
winSound = pygame.mixer.Sound('winSound.mp3') # Sound for the win sound
timeKeyPressed_W = 0 # Counter for jumpduration in game ticks for key_w
timeKeyPressed_UP = 0 # Counter for jumpduration in game ticks for key_UP
jumpAllowed_W = False # Flag for if jumping is allowed for W
jumpAllowed_UP = False # Flag for if jumping is allowed for UP
key_wUP = False # Flag for if key_w is realsed
key_upUP = False # Flag for if key_UP is realsed
file_path = 'levels.txt' # File path for textfile with all the levels
clock = pygame.time.Clock() # Used to control the speed of the game
FPS = 240 # Frames per second (game ticks per second)


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

levels = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.0, 0, 0, 2.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 2.75, 0, 0, 0, 1.0, 1.0, 0, 0, 1.0, 2.75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 2.0, 0, 2.0, 2.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.75, 0, 0, 0, 0, 0, 0, 0, 0, 
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.0, 0, 0, 0, 0, 0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 
1.0, 1.0, 0, 0, 0, 2.0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], [0, 0, 0, 2.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 2.75, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 2.75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 2.75, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 2.75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.5, 2.5, 2.5, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 0, 0, 0, 2.0, 2.0, 2.0, 2.0, 2.0, 0, 0, 0, 0, 0, 0, 2.0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.25, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.0, 2.0, 2.0, 2.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0
]]
#########################################################################


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
                print("hello")
                if level[cnt]%1 == 0:
                    print("hello1")
                    triangle_points = [(y*30, x*30+30), (y*30 +15, x*30+15), (y*30+30, x*30+30)]
                    xS = triangle_points[0][0] + (30 - spikeWidth)/2
                    yS = triangle_points[0][1] - spikeHeight
                    obstacle = Obstacle(xS, yS, spikeWidth, spikeHeight, (128,128,128), triangle_points)
                    Obstacles.append(obstacle)
                elif level[cnt]%1 == 0.25: 
                    print("hello2")
                    triangle_points = [(y*30+30, x*30), (y*30 +15, x*30+15), (y*30+30, x*30+30)]
                    xS = triangle_points[0][0] - (spikeHeight)
                    yS = triangle_points[0][1] + (30-spikeWidth)/2
                    obstacle = Obstacle(xS, yS, spikeHeight, spikeWidth, (128,128,128), triangle_points)
                    Obstacles.append(obstacle)
                elif level[cnt]%1 == 0.5:
                    print("hello3")
                    triangle_points = [(y*30, x*30), (y*30 +15, x*30+15), (y*30+30, x*30)]
                    xS = triangle_points[0][0] + (30 - spikeWidth)/2
                    yS = triangle_points[0][1]
                    obstacle = Obstacle(xS, yS, spikeWidth, spikeHeight, (128,128,128), triangle_points)
                    Obstacles.append(obstacle)
                elif level[cnt]%1 == 0.75:
                    print("hello4")
                    triangle_points = [(y*30, x*30), (y*30 +15, x*30+15), (y*30, x*30+30)]
                    xS = triangle_points[0][0]
                    yS = triangle_points[0][1] + spikeHeight
                    obstacle = Obstacle(xS, yS, spikeHeight, spikeWidth, (128,128,128), triangle_points)
                    Obstacles.append(obstacle)
                print()
            elif math.floor(level[cnt]) == 3:
                area = winArea(y*30, x*30,width,height, (255, 0, 0))    ###This should be the finish not a platform... its now a win area :)
                winAreas.append(area) 
            cnt += 1

def win(): # When you complete a map
    global Obstacles
    global Platforms
    global winAreas
    levelNr = 0
    winSound.play()
    pygame.time.delay(int(winSound.get_length()*1000))
    print(f"You completed area {levelNr+1}!")
    levelNr += 1
    for i in range(len(Characters)):
        Characters[i].x = STARTPOSX
        Characters[i].y = STARTPOSY
    
    Obstacles = []
    Platforms = []
    winAreas = []    
    makeLevel(levels[levelNr])
    
    
    

#########################################################################

      
Obstacles = [] # A list of all the obstacles

    
Characters = [Character(STARTPOSX, STARTPOSY, 20, 20, (255, 100, 100), SPEED), Character(STARTPOSX, STARTPOSY, 20, 20 , (255, 0, 0), SPEED)] # A list of all the characters


Platforms = [] # A list of all the platforms


winAreas = [] # A list of all the win areas :)

#########################################################################


def checkKeyUp(): # Function that checks if a key is realesed and if so block if from being pressed (mitigated by gravity and platformCollision to allow jumping if on ground or platform collision)
    keys = pygame.key.get_pressed()
    global key_wUP
    global key_upUP
    if not keys[pygame.K_w]:
        key_wUP = True
    if not keys[pygame.K_UP]:
        key_upUP = True


#########################################################################


def winCollision(character, platform): # Function that checks if you colide with the block that makes you win
    if character.rect.bottom == platform.rect.top and platform.rect.left < character.rect.x+character.width and platform.rect.right > character.rect.x:
       win() 
        
            
    if character.rect.top == platform.rect.bottom and platform.rect.left < character.rect.x+character.width and platform.rect.right > character.rect.x:
        win()
        
    if character.rect.left == platform.rect.right: 
        if character.rect.y+character.height > platform.rect.top and character.rect.y < platform.rect.bottom:            
            win()
            
    if character.rect.right == platform.rect.left: 
        if character.rect.y+character.height > platform.rect.top and character.rect.y < platform.rect.bottom:            
           win()

        
def platformCollision(character, platform): # Function that handles collision detection between platforms and characters
    if character.rect.bottom == platform.rect.top and platform.rect.left < character.rect.x+character.width and platform.rect.right > character.rect.x:
        #print("yes")
        character.y -= gravityConstant
        character.rect.y = character.y
        if character == Characters[0]:
            reset0(True)
        if character == Characters[1]:
            reset1(True)
        if character == Characters[0]:
            canJump0(True)
        if character == Characters[1]:
            canJump1(True)
        
        
            
    if character.rect.top == platform.rect.bottom and platform.rect.left < character.rect.x+character.width and platform.rect.right > character.rect.x:
        character.y += character.speed
        character.rect.y = character.y
    
    if character.rect.left == platform.rect.right: 
        if character.rect.y+character.height > platform.rect.top and character.rect.y < platform.rect.bottom:            
            character.x += character.speed
            character.rect.x = character.x
            
    if character.rect.right == platform.rect.left: 
        if character.rect.y+character.height > platform.rect.top and character.rect.y < platform.rect.bottom:            
            character.x -= character.speed
            character.rect.x = character.x



def gravity(character): # Functions that handles gravity move0ment
    if character.y < HEIGHT - character.height:
        character.y += gravityConstant
        character.rect.y = character.y
        if character == Characters[0]:
            canJump0(False)
        if character == Characters[1]:
            canJump1(False)  
    else: 
        if character == Characters[0]:
            reset0(True)
        if character == Characters[1]:
            reset1(True)
        if character == Characters[0]:
            canJump0(True)
        if character == Characters[1]:
            canJump1(True)


#########################################################################



def collision(character, obj): # Function for testing collision and plays a sound if you collided and then exits the game
    if character.rect.colliderect(obj.rect):
        failSound.play()
        pygame.time.delay(int(failSound.get_length()*1000))
        global running 
        running = False


#########################################################################


 
def move0(character): # Handle character move0ment WASD   
    keys = pygame.key.get_pressed()
    global timeKeyPressed_W
    
    if keys[pygame.K_d] and character.x < WIDTH-character.width:
        character.x += character.speed
        character.rect.x = character.x
    if keys[pygame.K_a] and character.x > 0:
        character.x -= character.speed
        character.rect.x = character.x
    if keys[pygame.K_w] and character.y > 0 and jumpAllowed_W == True and key_wUP == False:
        timeKeyPressed_W += 1
        #print(timeKeyPressed_W) 

        if timeKeyPressed_W < JUMPDURATION:
            character.y -= character.speed+.15
            character.rect.y = character.y   



def move01(character): # Handle charater movment arrow keys
    keys = pygame.key.get_pressed()
    global timeKeyPressed_UP
    if keys[pygame.K_RIGHT] and character.x < WIDTH-character.width:
        character.x += character.speed
        character.rect.x = character.x
    if keys[pygame.K_LEFT] and character.x > 0:
        character.x -= character.speed
        character.rect.x = character.x
    if keys[pygame.K_UP] and character.y > 0 and jumpAllowed_UP == True and key_upUP == False:
        timeKeyPressed_UP += 1
        #print(timeKeyPressed_UP)


        if timeKeyPressed_UP < JUMPDURATION:
            character.y -= character.speed+.15
            character.rect.y = character.y


def reset0(reset): # resets the counter for jumping for the character with WASD controlls
    if reset == True:
        global timeKeyPressed_W
        timeKeyPressed_W = 0


def reset1(reset): # resets the counter for jumping for the character with arrow keys controlls
    if reset == True:
        global timeKeyPressed_UP
        global key_upUP
        timeKeyPressed_UP = 0
        key_upUP = False


def canJump0(canJump): # Checks if the character can jump WASD controlls
    global jumpAllowed_W
    global key_wUP
    if canJump == False and timeKeyPressed_W == 0:
        jumpAllowed_W = False
        key_wUP = False
    else:
        jumpAllowed_W = True
        
        
def canJump1(canJump): # Checks if the character can jump arrow keys controlls
    global jumpAllowed_UP
    if canJump == False and timeKeyPressed_UP == 0:
        jumpAllowed_UP = False
    else:
        jumpAllowed_UP = True


#########################################################################        


#levels = read_lists_from_file(file_path)
makeLevel(levels[0]) # Loads the level
# print(imported_lists) Test to see that the levels load correctly


running = True
while running: # Main loop
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


#########################################################################


    #Calls function that handles movment events
    move0(Characters[0])
    move01(Characters[1])
    checkKeyUp()


#########################################################################   


    #Calls function that handles collision
    for o in range(len(Characters)):
        for i in range(len(Obstacles)):
            collision(Characters[o], Obstacles[i])


#########################################################################


    #Calls function that handles gravity
    for i in range(len(Characters)):
        gravity(Characters[i])


    #Calls function that handles Platform collision
    for o in range(len(Characters)):
        for i in range(len(Platforms)):
            platformCollision(Characters[o], Platforms[i])

    #Calls function that checks if you won
    for o in range(len(Characters)):
        for i in range(len(winAreas)):
            winCollision(Characters[o], winAreas[i])



#########################################################################  
 
  
    # Clear the screen
    screen.fill(WHITE)


#########################################################################


    # Draw the character & obstacles & platforms
    for i in range(len(Characters)):
        Characters[i].draw()
    
    for i in range(len(Obstacles)):
        Obstacles[i].draw()
        Obstacles[i].drawHitbox()
    
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
