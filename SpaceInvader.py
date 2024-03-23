from SpaceInvader_enemies import *

"""
SPACE INVADER
"""


# Class containing different elements of the game
class Game:
    def __init__(self):
        self.enemies = sprite.Group()  # Sprite group that will manage enemies
        self.bullets = sprite.Group()  # Sprite group that will manage enemy bullets
        self.bullet_velocity = 5  # Attribute that will contain the general speed of bullets during the game
        self.spawn(811, 11, 4, "EnemyShip")  # Makes an enemy spawn upon initialisation
        self.spawn(500, 0, 3, "Sinusoid")  # Makes another enemy spawn
        self.spawn(550, 250, 6, "EnemyBullets")  # Spawns a random bullet
        self.spawn(30, 0, 5, "Randominator")  # Spawns a Randominator
        print(self.enemies.sprites())  # Prints lists of sprite present in the sprite groups
        print(self.bullets.sprites())

    def spawn(self, x: int, y: int, velocity: int, type: str, transformation: int = 0):
        if type == "EnemyShip":  # Assigns to variable "a" the correct type of enemy that will be added to the game
            a = EnemyShip()
        elif type == "Sinusoid":
            a = Sinusoid()
        elif type == "EnemyBullets":
            a = EnemyBullets()
            a.rect.x = x  # Special case for enemy bullets, since they're in a specific group
            a.rect.y = y
            a.transformation = transformation  # Passes as an attribute for the bullet the rotation necessary it
            # will have to go through before spawning
            a.rotate()
            a.velocity = velocity
            self.bullets.add(a)
            return
        elif type == "Randominator":
            a = Randominator()
        a.rect.x = x  # Instead of the default position in (0,0), puts the sprite in coordinates passed in parameters
        a.rect.y = y
        a.velocity = velocity
        self.enemies.add(a)  # Displays one enemy by adding it to the enemies group sprite.

    def update(self):
        # This method, used down below will trigger the displacement method of each enemy sprite, hence making them move
        # while making sure each sprite move independently following the established rule relative to the enemy type.
        bullet_spawn = []
        for i in range(0, len(self.enemies)):
            if i < len(self.enemies):  # Due to the sprite killing method integrated in the enemy class, this condition
                # is needed because it provoked out of range related problems
                self.enemies.sprites()[i].displacement()  # Activates the displacement method of each enemy
                bullet_spawn.append(self.enemies.sprites()[i].detection())  # Puts in a list the tuple yielded from
                # each enemy's player detection method
        for elem in bullet_spawn:
            if elem[0] != -1:
                # If there is any tuple that contains a valid x coordinate, proceeds to make a bullet spawn from the
                # enemy's position using elements from the bullet spawn tuple.
                self.spawn(elem[0], elem[1], self.bullet_velocity, "EnemyBullets", elem[2])
        for i in range(0, len(self.bullets)):
            if i < len(self.bullets):
                self.bullets.sprites()[i].displacement()  # Triggers the bullet's displacement.


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
    game.bullets.draw(scene)
    game.update()

    display.flip()  # Sets the background and refreshes the window

    for thing in event.get():
        if thing.type == QUIT:
            # If quitting event detected, closes the windows
            is_active = False
            quit()
