from pygame import *


class Player(sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = image.load("./assets/ship.png")  # Loads the ship's image.
        self.image = transform.rotate(self.image, -90)  # Rotates it to respect the gameplay.
        self.rect = self.image.get_rect()  # Defines a collision box for the player and its coordinates set.
        self.hp = 100
        self.rect.x = 0
        self.rect.y = (500 - 100)/2
        self.velocity = 1  # Default player speed.

    def move(self):
        """When summoned, and if a corresponding key pressing event happens, executes the corresponding movement to the
        player."""
        l = 1000 - 100
        h = 500 - 100  # Defines dimensional constant to limit the player's ability to move.
        keys = key.get_pressed()  # Retrieves all keys pressed.

        if (keys[K_RIGHT] or keys[K_d]) and self.rect.x < l:
            # Move the player's ship if the right key is pressed and the ship is within the defined zone.
            self.rect.x += 5*self.velocity  # Velocity is factored it for potential speed malus or bonuses.

        if (keys[K_LEFT] or keys[K_q]) and self.rect.x > 0:
            self.rect.x -= 5*self.velocity

        if (keys[K_UP] or keys[K_z]) and self.rect.y > 0:
            self.rect.y -= 5*self.velocity

        if (keys[K_DOWN] or keys[K_s]) and self.rect.y < h:
            self.rect.y += 5*self.velocity

    def touchEnemy(self, ennemies):
        "Check if the player is touching an ennemy."
        for i in ennemies:
            if self.rect.colliderect(i.rect):
                return True


class Projectile(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image.load("./assets/white_placeholder.svg")
        self.image = transform.scale(self.image, (10, 5))  # Resizes image sprite to correct size
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.velocity = 1

    def displacement(self):
        self.rect.x += 5 * self.velocity  # Speed of projectile

    def touchedEnemy(self, enemies):
        for i in enemies:
            if self.rect.colliderect(i.rect):
                return True