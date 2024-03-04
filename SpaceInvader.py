from SpaceInvader_enemies import *

"""
SPACE INVADER
"""


# Class containing different elements of the game
class Game:
    def __init__(self):
        self.enemies = sprite.Group()
        self.spawn(0, 0, "EnemyShip")  # Makes an enemy spawn upon initialisation
        self.spawn(250, 0, "Sinusoid")  # Makes another enemy spawn
        print(self.enemies.sprites())  # Prints lists of sprite present in the enemy group

    def spawn(self, x: int, y: int, type: str):
        if type == "EnemyShip":  # Assigns to variable "a" the correct type of enemy that will be added to the game
            a = EnemyShip()
        elif type == "Sinusoid":
            a = Sinusoid()
        a.x = x  # Instead of the default position in (0,0), puts the sprite in coordinates passed in parameters
        a.y = y
        self.enemies.add(a)  # Displays one enemy by adding it to the enemies group sprite.


init()  # Initializes pygame

# Creates a window with the name of the game, and sets the future background image
display.set_caption("Efrarcade")
scene = display.set_mode((1000, 500))
background = image.load("./assets/test.png")

is_active = True

# Main loop that will reproduce a series of checks while the window is deemed active
while is_active:
    scene.blit(background, (0, 0))

    # Draws enemy group of sprites.
    game = Game()
    game.enemies.draw(scene)

    display.flip()  # Sets the background and refreshes the window

    for thing in event.get():
        if thing.type == QUIT:
            # If quitting event detected, closes the windows
            is_active = False
            quit()
