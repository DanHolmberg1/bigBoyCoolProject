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
    if keys[pygame.K_a] and character1.x > 0:
        character1.x -= character1.speed
    if keys[pygame.K_w]:
        character1.y -= character1.speed
    if keys[pygame.K_s] and character1.y < HEIGHT - character1.height:
        character1.y += character1.speed

    # Gravity
    if character1.y < HEIGHT - character1.height:
        character1.y += gravity

    # Clear the screen
    screen.fill(WHITE)

    # Draw the character
    character1.draw()

    # Update the display
    pygame.display.update()

pygame.quit()
sys.exit()
