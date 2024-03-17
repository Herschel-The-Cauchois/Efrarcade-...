from pygame import *
from math import sqrt, sin


def bezier_curve_calc(weights: list, details: int):
    t = 0
    curve = []
    while t <= 1:
        working_list = weights[:]
        while len(working_list) != 1:
            for pos, coord in enumerate(working_list):
                if coord != working_list[-1]:
                    working_list[pos] = (1-t)*coord[0]+t*working_list[pos+1][0], (1-t)*coord[1]+t*working_list[pos+1][1]
            working_list.pop()
        curve.append(working_list[0])
        t += 1/details
    return curve


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
        if self.rect.x >= 950 or self.rect.x <= 10:
            # If the ship is too much to the right, it will lower its altitude before reversing the displacement
            # behavior.
            # If the ship is too much to the left, it will lower its altitude before reversing the displacement
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
            if self.rect.x >= 950:
                self.reached_border = 1
            else:
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
        self.trajectory = []
        self.velocity = 10

    def displacement(self):
        # Will move the ship across the screen. This enemy will move in sinusoidal-simile curves
        # until it reaches a certain level.
        if not self.trajectory:  # This boolean expression was proposed by the IDE to detect when this list is empty.
            # if said list is empty, it means it completed a calculated trajectory.
            # If the ship is too much to the right, it will lower its altitude before reversing the displacement
            # behavior.
            # If the ship is too much to the left, it will lower its altitude before reversing the displacement
            # behavior.
            if self.rect.y < 400:
                # This condition verifies if the ship isn't too low. If its y coordinate is above designated level,
                # it will not lower again its altitude, and in the case of the lowering process making it go
                # Too much below, it will directly lower it to the minimum altitude.
                if self.rect.y + 8 * (int(sqrt(self.velocity))) > 400:
                    self.rect.y = 400
                else:
                    self.rect.y += 8 * (int(sqrt(self.velocity)))  # The sqrt factor makes the altitude loss dependent
                    # on velocity but helps attenuate the effect instead of using a constant when high velocity.
            if self.rect.x >= 950:
                self.reached_border = 1
            else:
                self.reached_border = 0

            self.trajectory = bezier_curve_calc()
        """if self.rect.x >= 950:
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
            self.rect.y += 100 * sin(self.velocity/1000)
        elif self.reached_border == 1:
            self.rect.x -= 1 * self.velocity
            self.rect.y += 100 * sin(self.velocity/1000)"""
