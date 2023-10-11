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
        self.rect = pygame.Rect(x, y, width, height)
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
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
class ObstacleTriangle:
    def __init__(self, x1, y1, x2, y2, x3, y3, color):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        self.color = color

    def draw(self):
        pygame.draw.polygon(screen, self.color, [(self.x1, self.y1), (self.x2, self.y2), (self.x3, self.y3)])
    
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
 
#Functions that handles gravity movement
def gravity(character):
    if character.y < HEIGHT - character.height:
        character.y += gravityConstant
        character.rect.y = character.y
      
      
        

# Obstacles
Obstacle1 = Obstacle(WIDTH-100,HEIGHT-120,20,20, (0,0,0))
Obstacle2 = Obstacle(WIDTH-200,HEIGHT-220,20,20, (0,0,0))
Obstacle3 = Obstacle(WIDTH-300,HEIGHT-230,20,20, (0,0,0))
Obstacle4 = Obstacle(WIDTH-250,HEIGHT-465,20,20, (0,0,0))
Obstacle5 = Obstacle(WIDTH-350,HEIGHT-652,20,20, (0,0,0))
Obstacle6 = Obstacle(WIDTH-522,HEIGHT-231,20,20, (0,0,0))
Obstacle7 = Obstacle(WIDTH-444,HEIGHT-200,20,20, (0,0,0))

#Charaters    
character1 = Character(100, 300, 50, 50, (255, 0, 0), .4)

running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Class the functions that handle movment for the character
    move(character1)
    
    
    #Calls function that handles gravity
    gravity(character1)
    
    #Check for collisions
    collision(character1, Obstacle1)
    collision(character1, Obstacle2)
    collision(character1, Obstacle3)
    collision(character1, Obstacle4)
    collision(character1, Obstacle5)
    collision(character1, Obstacle6)
    collision(character1, Obstacle7)
    
    

    # Clear the screen
    screen.fill(WHITE)

    # Draw the character
    character1.draw()
    Obstacle1.draw()
    Obstacle2.draw()
    Obstacle3.draw()
    Obstacle4.draw()
    Obstacle5.draw()
    Obstacle6.draw()
    Obstacle7.draw()
    
    # Update the display
    pygame.display.update()

pygame.quit()
sys.exit()
