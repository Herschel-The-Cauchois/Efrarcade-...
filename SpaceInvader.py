from pygame import *
import pygame
from pygame.locals import *

"""
SPACE INVADER
"""

#INFOS
"""
Axis

  0-|------------ (x)
    |
    |
    |
   (y)
"""

#GLOBAL VARIABLES
global L, H, is_active
global scene, background, perso, persoRect

clock = pygame.time.Clock()
L = 1000
H = 500
is_active = True

#INITIALISATION

init()  

#WINDOW
display.set_caption("Efrarcade")
scene = display.set_mode((L, H))
background = image.load("./assets/test.png")

#PLAYER
perso = image.load("./assets/perso.png").convert()
persoRect = perso.get_rect()
persoRect.x = (L - 150)/2
persoRect.y = H - 100


class Player :

    def __init__(self, perso):
        self.perso = perso


#PLAYER MOVEMENT

class Move:

    def __init__(self, x, y, is_active):
        self.x = x                                      # x and y are the coordinates of the player's ship
        self.y = y                     
        self.is_active = is_active                      # The ship is the image of the player's spaceship
        self.move_right = False
        self.move_left = False
        self.move_up = False
        self.move_down = False

    def move(self):

        l = L - 100                                     # Size ofthe temporary perso 100x100
        h = H - 100                                     # The player's ship can't go beyond the window

        keys = pygame.key.get_pressed()                 # Get the state of all keyboard keys

        if keys[pygame.K_RIGHT] and persoRect.x < l:    # Move the perso if the right key is pressed and the ship is within the window boundaries
            persoRect.x += 10

        if keys[pygame.K_LEFT] and persoRect.x > 0:
            persoRect.x -= 10

        if keys[pygame.K_UP] and persoRect.y > 0:
            persoRect.y -= 20

        if keys[pygame.K_DOWN] and persoRect.y < h:
            persoRect.y += 20


#GAME LOOP

while is_active:
    scene.blit(background, (0, 0))
    scene.blit(perso,(persoRect.x, persoRect.y))
    display.flip()                                      # Sets the background and refreshes the window
    clock.tick(60)


    Move.move(perso)
    pygame.display.update()

    for event in pygame.event.get(): 

        if event.type == QUIT:
            is_active = False                           # Set is_active to False when the window is closed
            quit()         

    if not is_active:                                   # Exit the game loop if is_active is False
        break
