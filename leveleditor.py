# Import and initialize the pygame library
import pygame
import math
import sys

pygame.init()


# Set up the drawing window
screen = pygame.display.set_mode([600, 600])

# Run until the user asks to quit
running = True

block_grid = []

for i in range(400):
     block_grid.append(0)

grid_on = True


def draw_grid():
    if grid_on:
        line_color = (0, 0, 0, 128)  # Color with 50% transparency (alpha value of 128)
        line_surface = pygame.Surface((600, 600), pygame.SRCALPHA)  # Create a transparent surface

        for i in range(20):
            pygame.draw.line(line_surface, line_color, (30*(i+1), 0), (30*(i+1), 600), 1)
            pygame.draw.line(line_surface, line_color, (0, 30*(i+1)), (600, 30*(i+1)), 1)

        screen.blit(line_surface, (0, 0))  # Blit the transparent lines onto the screen


def draw_rect_on_mouse():
     rect_width = 30
     rect_height = 30
     pygame.draw.rect(screen, (150, 75, 0), (x_floor, y_floor, rect_width, rect_height))

def test_button_press():
     if event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 1:  # Left mouse button
               change_block_on_mouse(1)
          elif event.button == 3:  # Right mouse button
               change_block_on_mouse(0)




def change_block_on_mouse(x):
     l = []
     for i in range(20):
          if y_floor == i*30:
               for j in range(20):
                    l.append(j+(i*20))

     for i in range(20):
          if x_floor == i*30:
               block_grid[l[i]] = x

def draw_blocks():
     l = []
     cnt = 0
     rect_width = 30
     rect_height = 30
     for i in range(20):
               for j in range(20):
                    if block_grid[cnt] == 1:
                          pygame.draw.rect(screen, (150, 75, 0), (j*30, i*30, rect_width, rect_height))
                    cnt += 1






draw_blocks()



#Main loop
while running:
     #variables in main loop
     mouse_x, mouse_y = pygame.mouse.get_pos()
     x_floor = mouse_x // 30 * 30   #rounds down to nearest multiple of 30
     y_floor = mouse_y // 30 * 30


     for event in pygame.event.get():
         if event.type == pygame.QUIT:
               running = False


    # Fill the background with white
     screen.fill((255, 255, 255))

     draw_grid()

     draw_rect_on_mouse()

     test_button_press()
     draw_blocks()

     # Flip the display
     pygame.display.flip()

# Time to end the Game
pygame.quit()
sys.exit()