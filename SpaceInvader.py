from pygame import *

"""
SPACE INVADER
"""

init()  # Initializes pygame

# Creates a window with the name of the game, and sets the future background image
display.set_caption("Efrarcade")
scene = display.set_mode((1000, 500))
background = image.load("./assets/test.png")

is_active = True

# Main loop that will reproduce a series of checks while the window is deemed active
while is_active:
    scene.blit(background, (0, 0))
    display.flip()  # Sets the background and refreshes the window
    for thing in event.get():
        if thing.type == QUIT:
            # If quitting event detected, closes the windows
            is_active = False
            quit()
