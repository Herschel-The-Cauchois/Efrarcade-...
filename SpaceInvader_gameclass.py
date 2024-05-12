from SpaceInvader_enemies import *


# Class containing different elements of the game
class Game:
    def __init__(self):
        self.enemies = sprite.Group()                                               # Sprite group that will manage enemies
        self.bullets = sprite.Group()                                               # Sprite group that will manage bullets
        self.projectiles = []                                                       # Regroups projectiles objects for interactions with enemies
        self.bullet_velocity = 5                                                    # Attribute that will contain the general speed of bullets during the game
        self.player = Player()                                                      # Initializes the player class
        self.level = 1
        self.enemy_count = 0
        self.score = 0
        self.activate = 0
        self.boss = sprite.Group()


    def spawn(self, x: int, y: int, velocity: int, type: str, transformation: int = 0, hp: int = -1, damage: int = -1, cadence: int = -1):
        """
        Method that will spawn enemies and bullets, by instantiating their respective class following the type
        parameter, give the instance a position from the x and y parameter, a velocity, other enemy related properties
        and for enemy bullets a rotation angle.
        """
        if type == "EnemyShip":                                                     # Assigns to variable "a" the correct type of enemy that will be added to the game
            a = EnemyShip()

        elif type == "Sinusoid":
            a = Sinusoid()

        elif type == "EnemyBullets":
            a = EnemyBullets()

            a.rect.x = x                                                            # Special case for enemy bullets, since they're in a specific group
            a.rect.y = y
            a.transformation = transformation                                       # Passes as an attribute for the bullet the rotation necessary it will have to go through before spawning
            a.rotate()
            a.velocity = velocity
            a.damage = damage
            self.bullets.add(a)                                                     # Adds it to the bullet group for specific management
            return

        elif type == "PlayerProjectile":
            projectile = Projectile()                                               # Create a projectile
            projectile.rect.x = x
            projectile.rect.y = y                                                   # Inserts the coordinates to center the bullet spawn point
            # At the tip of the player's ship
            self.bullets.add(projectile)                                            # Adds it to the bullet sprite group for management
            self.projectiles.append(projectile.rect)                                # References its hitbox in the player projectile list
            return
            
        elif type == "Randominator":
            a = Randominator()

        elif type == "Boss":
            a = Boss()
            self.boss.add(a)

        else:                                                                       # In case of a wrong type of entity entered, returns an input.
            print("Incorrect type input for spawn method : "+type)
            return

        # By default, assume it is an enemy that is spawned and will proceed to add it to the enemy group.
        a.rect.x = x                                                                # Instead of the default position in (0,0), puts the sprite in coordinates passed in parameters
        a.rect.y = y
        a.velocity = velocity
        if hp != -1:                                                                # Optional hp, damage and cadence modifiers relative to default values set up in their class.
            a.hp = hp
        if damage != -1:
            a.damage = damage
        if cadence != -1:
            a.cadence = cadence
        self.enemies.add(a)                                                         # Displays one enemy by adding it to the enemies group sprite.

    def update(self):
        """
        This method, used down below will trigger the displacement method of each enemy sprite, 
        hence making them move while making sure each sprite move independently following the 
        established rule relative to the enemy type.
        """
        bullet_spawn = []
        for i in range(0, len(self.enemies)):
            if i < len(self.enemies):                                                           # Due to the sprite killing method integrated in the enemy class, this condition is needed because it provoked out of range related problems
                self.enemies.sprites()[i].displacement()                                        # Activates the displacement method of each enemy
                bullet_spawn.append(self.enemies.sprites()[i].detection(self.player))           # Puts in a list the tuple yielded from each enemy's player detection method
                if self.enemies.sprites()[i].hp < 1:
                    self.score += self.enemies.sprites()[i].score                               # When an enemy is killed, increments the score according to the points it is supposed to give.
                    self.enemies.sprites()[i].kill()                                            # Kill the sprites of dead enemies.
                    mixer.Sound("assets/enemy_boom.mp3").play()                                 # Plays a sound when an enemy is killed.
                    self.enemy_count += 1                                                       # Adds one to the enemy killed in the wave
                    self.activate = 0                                                           # If one enemy is killed, reports to the game that the next wave can be activated
                                                                                                # if enough enemies are killed
        for elem in bullet_spawn:
            if elem[0] != -1:                                                                   # If there is any tuple that contains a valid x coordinate, proceeds to make a bullet spawn from the enemy's position using elements from the bullet spawn tuple.
                self.spawn(elem[0], elem[1], self.bullet_velocity, "EnemyBullets", elem[2], -1, elem[3])
        
        for i in range(0, len(self.bullets)):
            if i < len(self.bullets):                                                           # This is a solution to the same out of range problem as for enemies.
                if self.bullets.sprites()[i].rect in self.projectiles:                          # Checks if bullet belongs to player's.
                    if not self.bullets.sprites()[i].has_touched_bullet(self.bullets):          # Checks if bullet hasn't been killed by hitting an enemy bullet. If not, displaces it.
                        if not self.bullets.sprites()[i].has_touched_enemies(self.enemies):     # Checks if the bullet hasn't touched an enemy and if it was killed by such actions.
                            self.bullets.sprites()[i].displacement()                            # If bullet successfully countered, +1 point
                    
                    else:
                        self.score += 1
                
                else:
                    if i < len(self.bullets):
                        self.bullets.sprites()[i].displacement()                                # Triggers the bullet's displacement.

    def levels(self):
        """
        Method that following specific triggers will make waves of enemy spawn one after another, following
        enemies killed count for intra-level waves and marking the succession to another level.
        """
        if self.level == 1:
            if self.enemy_count == 0 and self.activate == 0:
                self.spawn(850, 15, 2, "EnemyShip", 0, 5, 1, 3)
                self.activate = 1                                                               # Marks the wave as activated to prevent repetitively spawning it.
            
            if self.enemy_count == 1 and self.activate == 0:                                    # Follows the count of enemy dead in the wave to trigger the next
                self.spawn(700, 15, 2, "EnemyShip", 0, 7, 1, 3)
                self.spawn(750, 15, 1, "Sinusoid", 0, 10, 1, 3)
                self.activate = 1

            if self.enemy_count == 3 and self.activate == 0:
                self.spawn(100, 255, 2, "Randominator", 0, 5, 2, 3)
                self.activate = 1

            if self.enemy_count == 4:                                                           # When all the enemies of the level are killed, resets enemy count and goes to next level.
                self.level = 2
                self.enemy_count = 0

        if self.level == 2:
            if self.enemy_count == 0 and self.activate == 0:
                mixer.Sound("assets/level_up.mp3").play()
                self.score += self.player.hp                                                    # Plays a reward sound and player gets a remaining hp score bonus !
                self.spawn(800, 30, 2, "EnemyShip", 0, 15, 2, 3)
                self.spawn(750, 50, 2, "Sinusoid", 0, 7, 2, 3)
                self.spawn(750, 100, 2, "Sinusoid", 0, 7, 2, 3)
                self.activate = 1

            if self.enemy_count == 3 and self.activate == 0:
                self.spawn(350, 250, 3, "EnemyShip", 0, 5, 3, 3)
                self.spawn(700, 250, 3, "EnemyShip", 0, 5, 3, 3)
                self.activate = 1

            if self.enemy_count == 5:
                self.level = 3
                self.enemy_count = 0

        if self.level == 3:
            if self.enemy_count == 0 and self.activate == 0:
                mixer.Sound("assets/level_up.mp3").play()
                self.score += self.player.hp
                self.spawn(500, 140, 3, "Randominator", 0, 15, 3, 4)
                self.spawn(800, 20, 2, "EnemyShip", 0, 7, 1, 3)
                self.activate = 1

            if self.enemy_count == 2 and self.activate == 0:
                self.level = 4
                self.enemy_count = 0

        if self.level == 4:
            if self.enemy_count == 0 and self.activate == 0:
                mixer.Sound("assets/level_up.mp3").play()
                self.score += self.player.hp
                self.spawn(230, 900, 3, "Sinusoid", 0, 15, 3, 2)
                self.spawn(900, 150, 3, "Sinusoid", 0, 15, 3, 2)
                self.activate = 1

            if self.enemy_count == 2 and self.activate == 0:
                self.spawn(230, 900, 3, "Sinusoid", 0, 15, 3, 2)
                self.spawn(900, 150, 3, "Sinusoid", 0, 15, 3, 2)
                self.spawn(350, 100, 4, "Randominator", 0, 3, 2, 3)
                self.spawn(650, 100, 4, "Randominator", 0, 3, 2, 3)
                self.activate = 1

            if self.enemy_count == 6 and self.activate == 0:                                    # When all the enemies of the level are killed, resets enemy count and goes to next level.
                self.level = 5
                self.enemy_count = 0

        if self.level == 5:                                                                     # Level 5 is a boss level
            if self.enemy_count == 0 and self.activate == 0:
                mixer.Sound("assets/level_up.mp3").play()
                self.score += self.player.hp
                self.spawn(700, 50, 5, "Sinusoid", 0, 7, 3, 3)
                self.spawn(650, 400, 5, "Sinusoid", 0, 12, 3, 3)
                self.spawn(680, 200, 3, "EnemyShip", 0, 5, 5, 3)
                self.spawn(670, 300, 4, "EnemyShip", 0, 7, 3, 3)
                self.spawn(710, 100, 3, "Sinusoid", 0, 9, 3, 4)
                self.spawn(660, 175, 3, "Sinusoid", 0, 10, 4, 3)
                self.activate = 1

            if self.enemy_count == 6 and self.activate == 0:                                    # When all the enemies of the level are killed, resets enemy count and goes to next level.
                self.level = 6
                self.enemy_count = 0

        if self.level == 6:
            if self.enemy_count == 0 and self.activate == 0:
                mixer.Sound("assets/level_up.mp3").play()
                self.score += self.player.hp
                self.spawn(900, 900, 4, "Sinusoid", 0, 15, 4, 2)
                self.spawn(900, 150, 4, "Sinusoid", 0, 15, 4, 2)
                self.spawn(800, 250, 4, "Sinusoid", 0, 15, 4, 2)
                self.spawn(350, 100, 4, "Randominator", 0, 7, 2, 3)
                self.spawn(650, 100, 4, "Randominator", 0, 7, 2, 3)
                self.activate = 1

            if self.enemy_count == 5 and self.activate == 0:
                self.spawn(600, 200, 2, "EnemyShip", 0, 15, 4, 3)
                self.spawn(900, 150, 4, "Randominator", 0, 7, 2, 2)
                self.spawn(350, 250, 4, "Randominator", 0, 5, 2, 2)
                self.spawn(200, 360, 4, "Randominator", 0, 6, 2, 2)
                self.activate = 1

            if self.enemy_count == 9:
                self.level = 7
                self.enemy_count = 0

        if self.level == 7:
            if self.enemy_count == 0 and self.activate == 0:
                mixer.Sound("assets/level_up.mp3").play()
                self.score += self.player.hp
                self.spawn(350, 250, 4, "Randominator", 0, 3, 1, 2)
                self.spawn(200, 360, 1, "Randominator", 0, 7, 2, 3)
                self.spawn(350, 250, 2, "Randominator", 0, 10, 5, 2)
                self.spawn(500, 360, 4, "Randominator", 0, 8, 2, 1)
                self.spawn(190, 250, 3, "Randominator", 0, 5, 3, 2)
                self.spawn(650, 360, 4, "Randominator", 0, 7, 4, 3)
                self.activate = 1

            if self.enemy_count == 6:
                self.level = 8
                self.enemy_count = 0
                
        if self.level == 8:
            if self.enemy_count == 0 and self.activate == 0:
                mixer.Sound("assets/level_up.mp3").play()
                self.score += self.player.hp
                self.spawn(565, 10, 0, "Boss", 0, -1, -1, -1)
                self.activate = 1
            if self.enemy_count == 1:
                self.level = 9
