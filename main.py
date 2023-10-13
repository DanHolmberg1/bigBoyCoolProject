import pygame
import sys

pygame.init()


WIDTH, HEIGHT = 600, 600
WHITE = (255, 255, 255)
JUMPDURATION = 200
SPEED = 1
gravityConstant = .5
failSound = pygame.mixer.Sound('lossSound.mp3')
timeKeyPressed_W = 0
timeKeyPressed_UP = 0
jumpAllowed_W = False
jumpAllowed_UP = False
clock = pygame.time.Clock()
FPS = 240


#Imports Maps
def read_lists_from_file(filename):
    with open(filename, 'r') as file:
        lists = []
        for line in file:
            elements = line.strip().split(', ')  # Assuming elements are separated by a comma and a space
            list_data = [element.strip() for element in elements]
            lists.append(list_data)
    return lists
file_path = 'levels.txt'
imported_lists = read_lists_from_file(file_path)
print(imported_lists)





# Create the game window
    
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BIGBOYCOOLPROJECT :)")



class Character:
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
       
class Obstacle: 
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
               
class Platform:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

level_1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.75, 2.5, 2.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.75, 2.0, 2.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.25, 1.25, 
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.0, 2.0, 2.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 2.75, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.75, 0, 0, 0, 0, 0, 0, 0, 1.0, 2.75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
0, 0, 0, 0, 0, 1.0, 2.75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 2.75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.25, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.25, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.0, 2.0, 2.0, 2.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.0, 2.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
0, 0, 0, 0, 0, 0, 2.0, 0, 0, 0, 0, 0, 1.0, 1.0, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]


def makeLevel(level):
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
                    obstacle = Obstacle(xS, yS, spikeWidth,spikeHeight, (128,128,128), triangle_points)
                    Obstacles.append(obstacle)
                elif level[cnt]%1 == 0.25: 
                    print("hello2")
                    triangle_points = [(y*30+30, x*30), (y*30 +15, x*30+15), (y*30+30, x*30+30)]
                    xS = triangle_points[0][0] + (30 - spikeWidth)/2
                    yS = triangle_points[0][1] - spikeHeight
                    obstacle = Obstacle(xS, yS, spikeWidth,spikeHeight, (128,128,128), triangle_points)
                    Obstacles.append(obstacle)
                elif level[cnt]%1 == 0.5:
                    print("hello3")
                    triangle_points = [(y*30, x*30), (y*30 +15, x*30+15), (y*30+30, x*30)]
                    xS = triangle_points[0][0] + (30 - spikeWidth)/2
                    yS = triangle_points[0][1] - spikeHeight
                    obstacle = Obstacle(xS, yS, spikeWidth,spikeHeight, (128,128,128), triangle_points)
                    Obstacles.append(obstacle)
                elif level[cnt]%1 == 0.75:
                    print("hello4")
                    triangle_points = [(y*30, x*30), (y*30 +15, x*30+15), (y*30, x*30+30)]
                    xS = triangle_points[0][0] + (30 - spikeWidth)/2
                    yS = triangle_points[0][1] - spikeHeight
                    obstacle = Obstacle(xS, yS, spikeWidth,spikeHeight, (128,128,128), triangle_points)
                    Obstacles.append(obstacle)
                print()
            cnt += 1


#Obstacles      
Obstacles = [Obstacle(WIDTH-100,HEIGHT-120,20,20, (0,0,0)), Obstacle(WIDTH-200,HEIGHT-220,20,20, (0,0,0)), Obstacle(WIDTH-300,HEIGHT-230,20,20, (0,0,0)), Obstacle(WIDTH-250,HEIGHT-465,20,20, (0,0,0)), Obstacle(WIDTH-350,HEIGHT-652,20,20, (0,0,0)), Obstacle(WIDTH-522,HEIGHT-231,20,20, (0,0,0)), Obstacle(WIDTH-444,HEIGHT-200,20,20, (0,0,0))]
#Charaters    
Characters = [Character(100, 300, 20, 20, (255, 0, 0), SPEED), Character(200, 250, 20, 20 , (255, 0, 0), SPEED)]
#Platforms
Platforms = [Platform(200, 200, 400, 20, (255, 255, 0)), Platform(300, 300, 200, 20, (25, 255, 0)), Platform(200, HEIGHT-150, 200, 20, (0,0,0)), Platform(100, HEIGHT-50, 200, 20, (0,0,0))]
       
#Function that handles collision detection between platforms and characters        
def platformCollision(character, platform):
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
               
#Function for testing collision and plays a sound if you collided and then exits the game
def collision(character, obj):
    if character.rect.colliderect(obj.rect):
        failSound.play()
        pygame.time.delay(int(failSound.get_length()*1000))
        global running 
        running = False
        
#Handle character move0ment WASD    
def move0(character):
    keys = pygame.key.get_pressed()
    global timeKeyPressed_W
    
    if keys[pygame.K_d] and character.x < WIDTH-character.width:
        character.x += character.speed
        character.rect.x = character.x
    if keys[pygame.K_a] and character.x > 0:
        character.x -= character.speed
        character.rect.x = character.x
    if keys[pygame.K_w] and character.y > 0 and jumpAllowed_W == True:
        timeKeyPressed_W += 1
        print(timeKeyPressed_W)
         # funkar inte men 

        if timeKeyPressed_W < JUMPDURATION:
            character.y -= character.speed+.15
            character.rect.y = character.y   
   # if keys[pygame.K_s] and character.y < HEIGHT - character.height: Downward movment if you want to be able to move0 through a platform and speed down.
   #     character.y += character.speed
   #     character.rect.y = character.y
   
#Handle charater movment arrow keys
def move01(character):
    keys = pygame.key.get_pressed()
    global timeKeyPressed_UP
    if keys[pygame.K_RIGHT] and character.x < WIDTH-character.width:
        character.x += character.speed
        character.rect.x = character.x
    if keys[pygame.K_LEFT] and character.x > 0:
        character.x -= character.speed
        character.rect.x = character.x
    if keys[pygame.K_UP] and character.y > 0 and jumpAllowed_UP == True:
        timeKeyPressed_UP += 1
        print(timeKeyPressed_UP)
         # funkar inte men 

        if timeKeyPressed_UP < JUMPDURATION:
            character.y -= character.speed+.15
            character.rect.y = character.y
    #if keys[pygame.K_DOWN] and character.y < HEIGHT - character.height:
     #       character.y += character.speed
      #      character.rect.y = character.y
def reset0(reset):
    if reset == True:
        global timeKeyPressed_W
        timeKeyPressed_W = 0
def reset1(reset):
    if reset == True:
        global timeKeyPressed_UP
        timeKeyPressed_UP = 0

def canJump0(canJump):
    global jumpAllowed_W
    if canJump == False and timeKeyPressed_W == 0:
        jumpAllowed_W = False
    else:
        jumpAllowed_W = True
def canJump1(canJump):
    global jumpAllowed_UP
    if canJump == False and timeKeyPressed_UP == 0:
        jumpAllowed_UP = False
    else:
        jumpAllowed_UP = True

        
#Functions that handles gravity move0ment
def gravity(character):
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

makeLevel(level_1)

running = True
while running: # Main loop
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Calls function that handles movment events
    move0(Characters[0])
    move01(Characters[1])
    
    #Calls function that handles gravity
    for i in range(len(Characters)):
        gravity(Characters[i])
        
    
    #Calls function that handles collision
    for o in range(len(Characters)):
        for i in range(len(Obstacles)):
            collision(Characters[o], Obstacles[i])
            
    #Calls function that handles Platform collision
    for o in range(len(Characters)):
        for i in range(len(Platforms)):
            platformCollision(Characters[o], Platforms[i])
    
    # Clear the screen
    screen.fill(WHITE)

    # Draw the character & obstacles & platforms
    for i in range(len(Characters)):
        Characters[i].draw()
    
    for i in range(len(Obstacles)):
        Obstacles[i].draw()
    
    for i in range(len(Platforms)):
        Platforms[i].draw()
    
    # Update the display
    pygame.display.update()

    clock.tick(FPS)
    
    

pygame.quit()
sys.exit()
