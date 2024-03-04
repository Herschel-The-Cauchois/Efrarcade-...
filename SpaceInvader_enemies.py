from pygame import *


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
