import pygame
import sys

pygame.init()


WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
gravityConstant = .15
failSound = pygame.mixer.Sound('lossSound.mp3')
timeKeyPressed_W = 0
timeKeyPressed_UP = 0



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
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height) # hitbox
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
               
class Platform:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
  
#Obstacles      
Obstacles = [Obstacle(WIDTH-100,HEIGHT-120,20,20, (0,0,0)), Obstacle(WIDTH-200,HEIGHT-220,20,20, (0,0,0)), Obstacle(WIDTH-300,HEIGHT-230,20,20, (0,0,0)), Obstacle(WIDTH-250,HEIGHT-465,20,20, (0,0,0)), Obstacle(WIDTH-350,HEIGHT-652,20,20, (0,0,0)), Obstacle(WIDTH-522,HEIGHT-231,20,20, (0,0,0)), Obstacle(WIDTH-444,HEIGHT-200,20,20, (0,0,0))]
#Charaters    
Characters = [Character(100, 300, 20, 20, (255, 0, 0), .30), Character(200, 250, 20, 20 , (255, 0, 0), .30)]
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
    if keys[pygame.K_w] and character.y > 0:
        timeKeyPressed_W += 1
        print(timeKeyPressed_W)
         # funkar inte men 

        if timeKeyPressed_W < 500:
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
    if keys[pygame.K_UP] and character.y > 0:
        timeKeyPressed_UP += 1
        print(timeKeyPressed_UP)
         # funkar inte men 

        if timeKeyPressed_UP < 500:
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
        
#Functions that handles gravity move0ment
def gravity(character):
    if character.y < HEIGHT - character.height:
        character.y += gravityConstant
        character.rect.y = character.y  
    else: 
        if character == Characters[0]:
            reset0(True)
        if character == Characters[1]:
            reset1(True)
        
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
    
    

pygame.quit()
sys.exit()
