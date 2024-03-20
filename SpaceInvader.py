from SpaceInvader_enemies import *

"""
SPACE INVADER
"""


# Class containing different elements of the game
class Game:
    def __init__(self):
        self.enemies = sprite.Group()  # Sprite group that will manage enemies
        self.bullets = sprite.Group()  # Sprite group that will manage enemy bullets (temporarily in enemy group)
        self.spawn(11, 0, 20, "EnemyShip")  # Makes an enemy spawn upon initialisation
        self.spawn(50, 150, 3, "Sinusoid")  # Makes another enemy spawn
        self.spawn(250, 0, 6, "EnemyBullets")  # Spawns a random bullet
        self.spawn(30, 0, 5, "Randominator")  # Spawns a Randominator
        print(self.enemies.sprites())  # Prints lists of sprite present in the enemy group

    def spawn(self, x: int, y: int, velocity: int, type: str):
        if type == "EnemyShip":  # Assigns to variable "a" the correct type of enemy that will be added to the game
            a = EnemyShip()
        elif type == "Sinusoid":
            a = Sinusoid()
        elif type == "EnemyBullets":
            a = EnemyBullets()
        elif type == "Randominator":
            a = Randominator()
        a.rect.x = x  # Instead of the default position in (0,0), puts the sprite in coordinates passed in parameters
        a.rect.y = y
        a.velocity = velocity
        self.enemies.add(a)  # Displays one enemy by adding it to the enemies group sprite.

    def update(self):
        # This method, used down below will trigger the displacement method of each enemy sprite, hence making them move
        # while making sure each sprite move independently following the established rule relative to the enemy type.
        for i in range(0, len(self.enemies)):
            if i < len(self.enemies):  # Due to the sprite killing method integrated in the enemy class, this condition
                # is needed because it provoked out of range related problems
                self.enemies.sprites()[i].displacement()


init()  # Initializes pygame

# Creates a window with the name of the game, and sets the future background image
display.set_caption("Efrarcade")
scene = display.set_mode((1000, 500))
background = image.load("./assets/test.png")

is_active = True
game = Game()  # Initializes the game class

# Main loop that will reproduce a series of checks while the window is deemed active
while is_active:
    scene.blit(background, (0, 0))

    # Draws enemy group of sprites.
    game.enemies.draw(scene)
    game.update()

    display.flip()  # Sets the background and refreshes the window

    for thing in event.get():
        if thing.type == QUIT:
            # If quitting event detected, closes the windows
            is_active = False
            quit()
