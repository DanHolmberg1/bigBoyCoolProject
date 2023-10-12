# Import and initialize the pygame library
import pygame
import math
import sys

pygame.init()


# Set up the drawing window
screen = pygame.display.set_mode([600, 600])

class Block:
     def __init__(self, type, rotation, color):
          self.type = type
          self.rotation = rotation
          self.color = color

blocks = [Block("dirt",0,(150, 75, 0)),Block("spike",0,(128,128,128))]



block = blocks[0]
block_number = 0 




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
     pygame.draw.rect(screen, block.color, (x_floor, y_floor, rect_width, rect_height))

s_key_pressed = False


def test_button_press():
     global s_key_pressed
     keys = pygame.key.get_pressed()
     if keys[pygame.K_s] and not s_key_pressed:
        change_block()
        
        # Set the flag to True to prevent the action from running again
        s_key_pressed = True
     elif not keys[pygame.K_s]:
        # Reset the flag when the 's' key is released
        s_key_pressed = False

     if event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 1:  # Left mouse button
               change_block_on_mouse(block_number+1)
               print(block_grid)
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
     
     triangle_outline_color = (255, 0, 0)  # Red color
     triangle_fill_color = (0, 0, 255)  # Blue color
     

     for x in range(20):
               for y in range(20):
                    if block_grid[cnt] == 1:
                         pygame.draw.rect(screen, (150, 75, 0), (y*30, x*30, rect_width, rect_height))
                    elif block_grid[cnt] == 2:
                         triangle_points = [(y*30, x*30+30), (y*30+15, x*30+15), (y*30+30, x*30+30)]
                         pygame.draw.polygon(screen, triangle_fill_color, triangle_points)
                         pygame.draw.polygon(screen, triangle_outline_color, triangle_points, 2)  # The '2' specifies the outline thickness
                         #pygame.draw.rect(screen, (128,128,128), (y*30, x*30, rect_width, rect_height))
                    cnt += 1

def change_block():
     global block_number
     global block
     if block_number < (len(blocks)-1):
          block_number += 1
     else: 
          block_number = 0
     block = blocks[block_number]
     print(block.color)




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
