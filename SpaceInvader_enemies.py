from pygame import *


class Enemies(sprite.Sprite):
    def __init__(self):
        super().__init__()  # Initializes super class that encapsulate all enemies
        self.hp = 0
        self.damage = 0


class EnemyShip(Enemies):
    def __init__(self):
        super().__init__()  # Initializes sprite class
        # Classical sprite initialisation : load image, initialize rectangle, positions...
        self.image = image.load("./assets/vaisseau_test2.png")
        self.hp = 50  # + sets new common properties for enemies of that type such as constant hp stat
        self.type = "EnemyShip"
        self.damage = 1
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
