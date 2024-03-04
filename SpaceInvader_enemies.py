from pygame import *
from math import sqrt, sin


class Enemies(sprite.Sprite):
    def __init__(self):
        super().__init__()  # Initializes super class that encapsulate all enemies
        self.hp = 0
        self.damage = 0


class EnemyShip(Enemies):
    # Class for the basic enemy ship
    def __init__(self):
        super().__init__()  # Initializes sprite class
        # Classical sprite initialisation : load image, initialize rectangle, positions...
        self.image = image.load("./assets/black_placeholder.svg")
        self.image = transform.scale(self.image, (50, 50))  # Resizes image sprite to correct size
        self.hp = 50  # + sets new common properties for enemies of that type such as constant hp stat
        self.type = "EnemyShip"  # Declares type of enemy for it to be identifiable to the game
        self.damage = 1  # Damage inflicted by the enemy
        self.rect = self.image.get_rect()  # Creates hitbox
        self.rect.x = 0
        self.rect.y = 0  # Sets up starting position of the ship by setting up the enemy's coordinate
        self.reached_border = 0
        self.velocity = 2

    def displacement(self):
        # Will move the ship across the screen. This enemy will move in straight lines until it reaches a certain level.
        if self.rect.x >= 950:
            # If the ship is too much to the right, it will lower its altitude before reversing the displacement
            # behavior.
            if self.rect.y < 400:
                # This condition verifies if the ship isn't too low. If its y coordinate is above designated level,
                # it will not lower again its altitude, and in the case of the lowering process making it go
                # Too much below, it will directly lower it to the minimum altitude.
                if self.rect.y + 8 * (int(sqrt(self.velocity))) > 400:
                    self.rect.y = 400
                else:
                    self.rect.y += 8 * (int(sqrt(self.velocity)))  # The sqrt factor makes the altitude loss dependent
                    # on velocity but helps attenuate the effect instead of using a constant when the velocity is high.
            self.reached_border = 1
        if self.rect.x <= 10:
            # If the ship is too much to the left, it will lower its altitude before reversing the displacement
            # behavior.
            if self.rect.y < 400:
                if self.rect.y + 8 * (int(sqrt(self.velocity))) > 400:
                    self.rect.y = 400
                else:
                    self.rect.y += 8 * (int(sqrt(self.velocity)))
            self.reached_border = 0
        if self.reached_border == 0:
            self.rect.x += 1 * self.velocity
        elif self.reached_border == 1:
            self.rect.x -= 1 * self.velocity


class Sinusoid(Enemies):
    # New enemy, sinusoid, which will follow a sinusoidal trajectory
    def __init__(self):
        super().__init__()  # Initializes sprite class
        # Classical sprite initialisation : load image, initialize rectangle, positions...
        self.image = image.load("./assets/white_placeholder.svg")
        self.image = transform.scale(self.image, (30, 50))  # Resizes image sprite to correct size
        self.hp = 50  # + sets new common properties for enemies of that type such as constant hp stat
        self.type = "Sinusoid"  # Declares type of enemy for it to be identifiable to the game
        self.damage = 5  # Damage inflicted by the enemy
        self.rect = self.image.get_rect()  # Creates hitbox
        self.rect.x = 0
        self.rect.y = 0  # Sets up starting position of the ship by setting up the enemy's coordinate
        self.reached_border = 0
        self.velocity = 10

    def displacement(self):
        # Will move the ship across the screen. This enemy will move in straight lines until it reaches a certain level.
        if self.rect.x >= 990:
            self.reached_border = 1
        if self.rect.x <= 10:
            self.reached_border = 0
        if self.reached_border == 0:
            self.rect.x += 1 * self.velocity
        elif self.reached_border == 1:
            self.rect.x -= 1 * self.velocity
