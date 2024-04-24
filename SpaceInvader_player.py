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

perso = image.load("./assets/Perso.png").convert()
persoRect = perso.get_rect()
persoRect.x = 0
persoRect.y = int((H - 100)/2)


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
        l = L - 700                                                             # Size of the temporary perso 100x100
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
        self.x += 45
                                                                        # Speed of projectile
    def draw(self):
        pygame.draw.rect(scene, (255, 255, 255), (self.x, self.y, 10, 5))           # Draw the projectile 10x5 pixels (white)


#Life

class Life:

    def __init__(self, life):
        self.life = life

    def draw(self):
        alive_heart_image = image.load("./assets/alive_heart_image.jpeg")
        alive_heart_image = transform.scale(alive_heart_image, (32, 32))
        heart_width = alive_heart_image.get_width()
        heart_height = alive_heart_image.get_height()
        heart_spacing = 5

        for i in range(3):
            heart_x = L - (heart_width + heart_spacing) * (i + 1)
            heart_y = H - heart_height - heart_spacing
            scene.blit(alive_heart_image, (heart_x, heart_y))


    def check_game_over(self):
        dead_heart_image = image.load("./assets/dead_heart_image.jpg")
        dead_heart_image = transform.scale(dead_heart_image, (32, 32))
        heart_width = dead_heart_image.get_width()
        heart_height = dead_heart_image.get_height()
        heart_spacing = 5

        for i in range(3):
            heart_x = L - (heart_width + heart_spacing) * (i + 1)
            heart_y = H - heart_height - heart_spacing
            scene.blit(dead_heart_image, (heart_x, heart_y))







#GAME LOOP
        
projectiles = []
while is_active:                                                                    # Main loop
    scene.blit(background, (0, 0))                                                  # Background
    scene.blit(perso, (persoRect.x, persoRect.y))                                   # Player's ship

    life = Life(3)
    life.draw()

    for projectile in projectiles:                              
        projectile.move()                                       
        projectile.draw()
        if L < projectile.x :                                                       # Remove the projectile if it goes off the screen
            projectiles.remove(projectile)
    display.flip()                                                                  # Update the display
    clock.tick(60)                                              

    Move.move(perso)                                                                # class Move 
    pygame.display.update()      

    if life == 0:
        is_active = False                               


    for event in pygame.event.get():                                                # Event loop
        if event.type == QUIT:
            is_active = False
            quit()
      
        if event.type == KEYDOWN and event.key == pygame.K_SPACE:                   # If the space key is pressed
            projectile = Projectile(persoRect.x + 75, persoRect.y + 50)             # Create a projectile
            projectiles.append(projectile)
            
    if not is_active:                                                               # Exit the game
        break
        