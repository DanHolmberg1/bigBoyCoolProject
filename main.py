import pygame
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
gravity = .15

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BIGBOYCOOLPROJECT :)")

class Character:
    def __init__(self, x, y, width, height, color, speed):
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
        pygame.quit()
        sys.exit()

       
    
# Obstacles
Obstacle1 = Obstacle(WIDTH-100,HEIGHT-20,20,20, (0,0,0))
#Charaters    
character1 = Character(100, 300, 50, 50, (255, 0, 0), .4)

running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle character movement
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_d] and character1.x < WIDTH-character1.width:
        character1.x += character1.speed
        character1.rect.x = character1.x
        print(character1.rect.x, "", character1.rect.y)
    if keys[pygame.K_a] and character1.x > 0:
        character1.x -= character1.speed
        character1.rect.x = character1.x
    if keys[pygame.K_w]:
        character1.y -= character1.speed
        character1.rect.y = character1.y
    if keys[pygame.K_s] and character1.y < HEIGHT - character1.height:
        character1.y += character1.speed
        character1.rect.y = character1.y

    # Gravity
    if character1.y < HEIGHT - character1.height:
        character1.y += gravity
        character1.rect.y = character1.y

    #Check for collisions
    collision(character1, Obstacle1)

    # Clear the screen
    screen.fill(WHITE)

    # Draw the character
    character1.draw()
    Obstacle1.draw()


    # Update the display
    pygame.display.update()

pygame.quit()
sys.exit()
