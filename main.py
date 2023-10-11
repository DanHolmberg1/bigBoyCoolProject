import pygame
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
gravityConstant = .15

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
        
#Function for testing collision
def collision(character, obj):
    if character.rect.colliderect(obj.rect):
        print("Collision")
      
#Handle character movement    
def move(character):
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_d] and character.x < WIDTH-character.width:
        character.x += character.speed
        character.rect.x = character.x
    if keys[pygame.K_a] and character.x > 0:
        character.x -= character.speed
        character.rect.x = character.x
    if keys[pygame.K_w]:
        character.y -= character.speed
        character.rect.y = character.y
    if keys[pygame.K_s] and character.y < HEIGHT - character.height:
        character.y += character.speed
        character.rect.y = character.y
        
def move2(character):
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_RIGHT] and character.x < WIDTH-character.width:
        character.x += character.speed
        character.rect.x = character.x
    if keys[pygame.K_LEFT] and character.x > 0:
        character.x -= character.speed
        character.rect.x = character.x
    if keys[pygame.K_UP]:
        character.y -= character.speed
        character.rect.y = character.y
    if keys[pygame.K_DOWN] and character.y < HEIGHT - character.height:
        character.y += character.speed
        character.rect.y = character.y
 
#Functions that handles gravity movement
def gravity(character):
    if character.y < HEIGHT - character.height:
        character.y += gravityConstant
        character.rect.y = character.y
      


#Obstacles      
Obstacles = [Obstacle(WIDTH-100,HEIGHT-120,20,20, (0,0,0)), Obstacle(WIDTH-200,HEIGHT-220,20,20, (0,0,0)), Obstacle(WIDTH-300,HEIGHT-230,20,20, (0,0,0)), Obstacle(WIDTH-250,HEIGHT-465,20,20, (0,0,0)), Obstacle(WIDTH-350,HEIGHT-652,20,20, (0,0,0)), Obstacle(WIDTH-522,HEIGHT-231,20,20, (0,0,0)), Obstacle(WIDTH-444,HEIGHT-200,20,20, (0,0,0))]
#Charaters    
Characters = [Character(100, 300, 50, 50, (255, 0, 0), .4), Character(200, 250, 50, 50 , (255, 0, 0), .4)]



running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Class the functions that handle movment for the character
    
    move(Characters[0])
    move2(Characters[1])
    
    #Calls function that handles gravity
    for i in range(len(Characters)):
        gravity(Characters[i])
    
    #Calls function that handles collision
    for o in range(len(Characters)):
        for i in range(len(Obstacles)):
            collision(Characters[o], Obstacles[i])

    # Clear the screen
    screen.fill(WHITE)

    # Draw the character & obstacles
    for i in range(len(Characters)):
        Characters[i].draw()
    
    for i in range(len(Obstacles)):
        Obstacles[i].draw()
    
    # Update the display
    pygame.display.update()

pygame.quit()
sys.exit()
