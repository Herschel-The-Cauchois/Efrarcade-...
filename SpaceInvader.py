import pygame
import random

"""
SPACE INVADER
"""

pygame.init()  # Initializes pygamegame

# Creates a window with the name of the game, and sets the future background image
screen_width = 1000
screen_height = 500
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
    


is_active = True

# Main loop that will reproduce a series of checks while the window is deemed active
while is_active:
    scene.blit(background, (0, 0))

    # Draw each star onto the scene
    genererateStars()
    paintStars(scene)

    pygame.display.flip()  # Sets the background and refreshes the window

    for thing in pygame.event.get():
        if thing.type == pygame.QUIT:
            # If quitting event detected, closes the windows
            is_active = False
            quit()