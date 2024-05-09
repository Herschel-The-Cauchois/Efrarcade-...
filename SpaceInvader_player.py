from pygame import *


class Player(sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = image.load("./assets/shipofficiel.png")  # Loads the ship's image.
        self.image = transform.rotate(self.image, -90)  # Rotates it to respect the gameplay.
        self.image = transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()  # Defines a collision box for the player and its coordinates set.
        self.rect = Rect.inflate(self.rect, -30, -30)
        self.hp = 100
        self.rect.x = 0
        self.rect.y = (500 - 100)//2
        self.damage = 1
        self.velocity = 1                                                   # Default player speed.

    def move(self):
        """When summoned, and if a corresponding key pressing event happens, executes the corresponding movement to the
        player."""
        l = 1000 - 100
        h = 500 - 100                                                       # Defines dimensional constant to limit the player's ability to move.
        keys = key.get_pressed()                                            # Retrieves all keys pressed.

        if self.hp < 1:                                                     # Forbids the player from moving if it isn't alive.
            self.kill()
            return

        if (keys[K_RIGHT] or keys[K_d]) and self.rect.x < l:                # Move the player's ship if the right key is pressed and the ship is within the defined zone.
            self.rect.x += 5*self.velocity                                  # Velocity is factored it for potential speed malus or bonuses.

        if (keys[K_LEFT] or keys[K_q]) and self.rect.x > 0:
            self.rect.x -= 5*self.velocity

        if (keys[K_UP] or keys[K_z]) and self.rect.y > 0:
            self.rect.y -= 5*self.velocity

        if (keys[K_DOWN] or keys[K_s]) and self.rect.y < h:
            self.rect.y += 5*self.velocity

    def is_touching_enemy(self, enemies):
        """Check if the player is touching an enemy."""
        for i in enemies:
            if self.rect.colliderect(i.rect):                               # Verification if one enemy hitbox hits the player's.
                return True


class Projectile(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image.load("./assets/white_placeholder.svg")
        self.image = transform.scale(self.image, (10, 5))                   # Resizes image sprite to correct size
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.damage = 1
        self.velocity = 1

    def displacement(self):
        if self.rect.x > 1000:
            self.kill()
        else:
            self.rect.x += 5 * self.velocity                                # Speed of projectile

    def has_touched_enemies(self, enemies):
        for i in enemies:
            if self.rect.colliderect(i.rect):                               # Check if enemy has been hit by a projectile.
                i.hp -= self.damage                                         # If so, removes hp to the enemy and kills the projectile.
                print(i.hp)
                self.kill()
                return True
        return False
    
    def has_touched_bullet(self, bullets):
        for i in bullets:
            if self.rect.colliderect(i.rect) and i.rect != self.rect:       # Checks if a different bullet hit the projectile
                self.kill()                                                 # Kills both bullets.
                i.kill()
                return True                                                 # Returns a True boolean to confirm concerned bullet has been killed.
        return False                                                        # If no collision, returns False.
