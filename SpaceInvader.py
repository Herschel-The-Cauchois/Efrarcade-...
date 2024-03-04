import random
from pygame import *
import pygame
from pygame.locals import *

"""
SPACE INVADER
"""

pygame.init()  # Initializes pygamegame

# Creates a window with the name of the game, and sets the future background image
screen_width = 1000
screen_height = 500
is_active = True
pygame.display.set_caption("Efrarcade")
scene = pygame.display.set_mode((screen_width, screen_height))
background = pygame.Surface(scene.get_size())
clock = pygame.time.Clock()
star_positions = []
def genererateStars():
    """ generate some stars that will move from the right to the left.
    It creates a new star with a 10% chance, to avoid having too many stars. Once its creating it by putting it in a list (to keep track of it), it will move it to the left and remove it from the list if it goes out of the screen.
    An star is a list with 3 elements: x position, y position and speed.
    """
    if random.randint(0, 100) < 10:
        star_positions.append([screen_width, random.randint(0, screen_height), random.randint(1, 3)])
    for star in star_positions:
        star[0] -= star[2]
        if star[0] < 0:
            star_positions.remove(star)
def paintStars(scene):
    """ paint the stars on the scene """
    for star in star_positions:
        pygame.draw.circle(scene, (255, 255, 255), (star[0], star[1]), 1)
    

#PLAYER
perso = image.load("./assets/Perso.png").convert()
persoRect = perso.get_rect()
persoRect.x = (screen_width - 150)/2
persoRect.y = screen_height - 100


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

        l = screen_width - 100                                     # Size ofthe temporary perso 100x100
        h = screen_height - 100                                     # The player's ship can't go beyond the window

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

    # Draw each star onto the scene
    genererateStars()
    paintStars(scene)
    Move.move(perso)
    pygame.display.update()
    clock.tick(60)
    pygame.display.flip()  # Sets the background and refreshes the window

    for thing in pygame.event.get():
        if thing.type == pygame.QUIT:
            # If quitting event detected, closes the windows
            is_active = False
            quit()