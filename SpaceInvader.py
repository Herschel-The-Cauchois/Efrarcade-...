from pygame import *
import pygame
from pygame.locals import *

"""
SPACE INVADER
"""

#INFOS
"""
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



#PLAYER MOVEMENT

class Player:

    def __init__(self, x, y, ship):
        self.x = x                              # x and y are the coordinates of the player's ship
        self.y = y                     
        self.ship = ship                        # The ship is the image of the player's spaceship
        

    def move(self):

        l = L - 150                            # The player's ship can't go beyond the window
        h = H - 100
        

        
        for event in pygame.event.get():          

            if event.type == pygame.KEYDOWN:       # If a key is pressed, the player's ship moves
                

                if event.key == K_RIGHT:           #Right arrow key
                    if persoRect.x < l:
                        persoRect.x += 10
                    

                if event.key == K_LEFT:            #Left arrow key
                    if persoRect.x > 0:
                        persoRect.x -= 10


                if event.key == K_UP:              #Up arrow key
                    if persoRect.y > 0:
                        persoRect.y -= 20


                if event.key == K_DOWN:            #Down arrow key
                    if persoRect.y < h:
                        persoRect.y += 20

                






#GAME LOOP

while is_active:
    scene.blit(background, (0, 0))
    scene.blit(perso,(persoRect.x, persoRect.y))
    display.flip()                                  # Sets the background and refreshes the window
    clock.tick(30)


    Player.move(perso)

    for thing in event.get():
        if thing.type == QUIT:                      # If the window is closed, the game stops
            is_active = False
            quit()


