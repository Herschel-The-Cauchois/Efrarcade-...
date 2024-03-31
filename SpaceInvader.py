from SpaceInvader_enemies import *
import random
from pygame import *
import pygame
from pygame.locals import *

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
        self.spawn(450, 250, 0, "EnemyShip")  # Enemy spawning for bullet position tests
        self.spawn(575, 250, 0, "Sinusoid")
        self.spawn(700, 150, 0, "Randominator")
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
screen_width = 1000
screen_height = 500
ratio = screen_width / screen_height
is_active = True
game = Game()  # Initializes the game class
pygame.display.set_caption("Efrarcade")
scene = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
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
perso = image.load("./assets/ship.png").convert()
perso = pygame.transform.rotate(perso, -90)
persoRect = perso.get_rect()
persoRect.x = 0
persoRect.y = (H - 100)/2


class Player :

    def __init__(self, perso):
        self.perso = perso


#PLAYER MOVEMENT

class Move:

    def __init__(self, x, y, is_active):
        self.x = x                                                              # x and y are the coordinates of the player's ship
        self.y = y                     
        self.is_active = is_active                                              # The ship is the image of the player's spaceship
        self.move_right = False
        self.move_left = False
        self.move_up = False
        self.move_down = False


    def move(self):
        l = L - 700                                                             # Size ofthe temporary perso 100x100
        h = H - 100                                                             # The player's ship can't go beyond the window


        keys = pygame.key.get_pressed()                                         # Get the state of all keyboard keys

        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and persoRect.x < l:      # Move the perso if the right key is pressed and the ship is within the window boundaries
            persoRect.x += 20

        if (keys[pygame.K_LEFT] or keys[pygame.K_q]) and persoRect.x > 0:
            persoRect.x -= 20

        if (keys[pygame.K_UP] or keys[pygame.K_z]) and persoRect.y > 0:
            persoRect.y -= 20

        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and persoRect.y < h:
            persoRect.y += 20

class Projectile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        self.x += 45                                                                # Speed of projectile

    def draw(self):
        pygame.draw.rect(scene, (255, 255, 255), (self.x, self.y, 10, 5))           # Draw the projectile 10x5 pixels (white)


#GAME LOOP
        
projectiles = []

def game_loop():
    is_active=True
    while is_active:
        scene.blit(background, (0, 0))
        scene.blit(perso,(persoRect.x, persoRect.y))
        
        for projectile in projectiles:                              
          projectile.move()                                       
          projectile.draw()

          if L < projectile.x :                                                       # Remove the projectile if it goes off the screen
              projectiles.remove(projectile)

        # Draw each star onto the scene
        genererateStars()
        paintStars(scene)
        Move.move(perso)
        pygame.display.update()
        clock.tick(60)


        game.enemies.draw(scene)
        game.bullets.draw(scene)
        game.update()

        pygame.display.flip()  # Sets the background and refreshes the window

        for thing in pygame.event.get():
            if thing.type == pygame.QUIT:
                # If quitting event detected, closes the windows
                is_active = False
                quit()
            if event.type == KEYDOWN and event.key == pygame.K_SPACE:                   # If the space key is pressed
              projectile = Projectile(persoRect.x + 75, persoRect.y + 50)             # Create a projectile
              projectiles.append(projectile)
            if thing.type == pygame.VIDEORESIZE: #THIS IS NOT WORKING
                new_width = thing.w
                new_height = int(new_width / ratio)
                screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
