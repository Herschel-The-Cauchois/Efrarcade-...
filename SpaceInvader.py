from SpaceInvader_enemies import *
from SpaceInvader_player import *
import random

"""
SPACE INVADER
"""


# Class containing different elements of the game
class Game:
    def __init__(self):
        self.enemies = sprite.Group()  # Sprite group that will manage enemies
        self.bullets = sprite.Group()  # Sprite group that will manage bullets
        self.projectiles = []  # Regroups projectiles objects for interactions with enemies
        self.bullet_velocity = 5  # Attribute that will contain the general speed of bullets during the game
        self.player = Player()  # Initializes the player class
        self.level = 1
        self.enemy_count = 0
        self.score = 0
        self.activate = 0
        """self.spawn(811, 11, 4, "EnemyShip")  # Makes an enemy spawn upon initialisation
        self.spawn(500, 0, 3, "Sinusoid")  # Makes another enemy spawn
        self.spawn(550, 250, 6, "EnemyBullets")  # Spawns a random bullet
        self.spawn(30, 0, 5, "Randominator")  # Spawns a Randominator
        self.spawn(450, 250, 0, "EnemyShip", 0, 15)  # Immobile enemy spawning for bullet position tests
        self.spawn(575, 250, 0, "Sinusoid")
        self.spawn(100, 150, 0, "Randominator", 0, 15, 5, 3)"""
        print(self.enemies.sprites())  # Prints lists of sprite present in the sprite groups
        print(self.bullets.sprites())

    def spawn(self, x: int, y: int, velocity: int, type: str, transformation: int = 0, hp: int = -1, damage: int = -1, cadence: int = -1):
        """Method that will spawn enemies and bullets, by instantiating their respective class following the type
        parameter, give the instance a position from the x and y parameter, a velocity, other enemy related properties
        and for enemy bullets a rotation angle."""
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
            a.damage = damage
            self.bullets.add(a)  # Adds it to the bullet group for specific management
            return
        elif type == "PlayerProjectile":
            projectile = Projectile()  # Create a projectile
            projectile.rect.x = x
            projectile.rect.y = y  # Inserts the coordinates to center the bullet spawn point
            # At the tip of the player's ship
            game.bullets.add(projectile)  # Adds it to the bullet sprite group for management
            self.projectiles.append(projectile.rect)  # References its hitbox in the player projectile list
            return
        elif type == "Randominator":
            a = Randominator()
        else:
            # In case of a wrong type of entity entered, returns an input.
            print("Incorrect type input for spawn method : "+type)
            return
        # By default, assume it is an enemy that is spawned and will proceed to add it to the enemy group.
        a.rect.x = x  # Instead of the default position in (0,0), puts the sprite in coordinates passed in parameters
        a.rect.y = y
        a.velocity = velocity
        if hp != -1:  # Optional hp, damage and cadence modifiers relative to default values set up in their class.
            a.hp = hp
        if damage != -1:
            a.damage = damage
        if cadence != -1:
            a.cadence = cadence
        self.enemies.add(a)  # Displays one enemy by adding it to the enemies group sprite.

    def update(self):
        # This method, used down below will trigger the displacement method of each enemy sprite, hence making them move
        # while making sure each sprite move independently following the established rule relative to the enemy type.
        bullet_spawn = []
        for i in range(0, len(self.enemies)):
            if i < len(self.enemies):  # Due to the sprite killing method integrated in the enemy class, this condition
                # is needed because it provoked out of range related problems
                self.enemies.sprites()[i].displacement()  # Activates the displacement method of each enemy
                bullet_spawn.append(self.enemies.sprites()[i].detection(self.player))  # Puts in a list the tuple
                # yielded from each enemy's player detection method
                if self.enemies.sprites()[i].hp < 1:
                    self.score += self.enemies.sprites()[i].score  # When an enemy is killed, increments the score according to the points it is supposed to give.
                    print("Score : {}".format(self.score))
                    self.enemies.sprites()[i].kill()  # Kill the sprites of dead enemies.
                    mixer.Sound("assets/enemy_boom.mp3").play()  # Plays a sound when an enemy is killed.
                    self.enemy_count += 1  # Adds one to the enemy killed in the wave
                    self.activate = 0  # If one enemy is killed, reports to the game that the next wave can be activated
                    # if enough enemies are killed
        for elem in bullet_spawn:
            if elem[0] != -1:
                # If there is any tuple that contains a valid x coordinate, proceeds to make a bullet spawn from the
                # enemy's position using elements from the bullet spawn tuple.
                self.spawn(elem[0], elem[1], self.bullet_velocity, "EnemyBullets", elem[2], -1, elem[3])
        for i in range(0, len(self.bullets)):
            if i < len(self.bullets):  # This is a solution to the same out of range problem as for enemies.
                if self.bullets.sprites()[i].rect in self.projectiles:  # Checks if bullet belongs to player's.
                    if not self.bullets.sprites()[i].has_touched_bullet(self.bullets):
                        # Checks if bullet hasn't been killed by hitting an enemy bullet. If not, displaces it.
                        if not self.bullets.sprites()[i].has_touched_enemies(self.enemies):
                            # Checks if the bullet hasn't touched an enemy and if it was killed by such actions.
                            self.bullets.sprites()[i].displacement()  # If bullet successfully countered, +1 point
                    else:
                        self.score += 1
                else:
                    if i < len(self.bullets):
                        self.bullets.sprites()[i].displacement()  # Triggers the bullet's displacement.

    def levels(self):
        """Method that following specific triggers will make waves of enemy spawn one after another, following
        enemies killed count for intra-level waves and marking the succession to another level."""
        if self.level == 1:
            if self.enemy_count == 0 and self.activate == 0:
                self.spawn(850, 15, 2, "EnemyShip", 0, 5, 1, 3)
                self.activate = 1  # Marks the wave as activated to prevent repetitively spawning it.
            if self.enemy_count == 1 and self.activate == 0:
                # Follows the count of enemy dead in the wave to trigger the next
                self.spawn(700, 15, 2, "EnemyShip", 0, 7, 1, 3)
                self.spawn(750, 15, 1, "Sinusoid", 0, 10, 1, 3)
                self.activate = 1
            if self.enemy_count == 3 and self.activate == 0:
                self.spawn(100, 255, 2, "Randominator", 0, 5, 2, 3)
                self.activate = 1
            if self.enemy_count == 4:
                # When all the enemies of the level are killed, resets enemy count and goes to next level.
                self.level = 2
                self.enemy_count = 0
        if self.level == 2:
            if self.enemy_count == 0 and self.activate == 0:
                mixer.Sound("assets/level_up.mp3").play()
                self.score += self.player.hp  # Plays a reward sound and player gets a remaining hp score bonus !
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
            if self.enemy_count == 6 and self.activate == 0:
                self.level = 5
                self.enemy_count = 0
        if self.level == 5:
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
            if self.enemy_count == 6 and self.activate == 0:
                self.level = 6
                self.enemy_count = 0
        if self.level == 6:
            if self.enemy_count == 0 and self.activate == 0:
                mixer.Sound("assets/level_up.mp3").play()
                self.score += self.player.hp
                self.activate = 1


init()  # Initializes pygame
font.init()  # Initializes font module

# Creates a window with the name of the game, and sets the future background image
screen_width = 1000
screen_height = 500  # Dimensions of the game window
ratio = screen_width / screen_height
game = Game()  # Initializes the game class
display.set_caption("Efrarcade")  # Titles the pygame window to Efrarcade
scene = display.set_mode((screen_width, screen_height), RESIZABLE)
background = Surface(scene.get_size())  # Creates a surface for the background of the game
clock = time.Clock()
star_positions = []  # Lists that holds the position of each respective star.
game_over_font = font.SysFont("Comic Sans MS", 30)
game_over_text = game_over_font.render("Game Over :(", False, (255, 255, 255))


def generate_stars():
    """Generates stars that will move from the right to the left. There is a 10% probability of star generation
    introduced, preventing overabundance of stars. Once created, puts it in a tracking list, then moving it leftwards
    until it is removed from the screen. It disposes of three properties : x position, y position and speed.
    """
    if random.randint(0, 100) < 10:
        star_positions.append([screen_width, random.randint(0, screen_height), random.randint(1, 3)])
    for star in star_positions:  # Loop that generalizes the behavior to all stars.
        star[0] -= star[2]  # Subtracts x position by the speed.
        if star[0] < 0:  # Detects if it is off the screen.
            star_positions.remove(star)


def paint_stars(s):
    """Draw each star on the scene."""
    for star in star_positions:
        draw.circle(s, (255, 255, 255), (star[0], star[1]), 1)  # Represents them as a circle.


def game_loop():
    is_active = True  # Elementary boolean that stays True until QUIT event is triggered.
    while is_active:
        scene.blit(background, (0, 0))  # Draws background.
        draw.rect(scene, (0, 0, 0), (0, 0, 1000, 100))  # Trying to draw a slot for the game stats...
        if game.player.hp > 0:
            game_over = 0
            scene.blit(game.player.image, (game.player.rect.x, game.player.rect.y))  # Draws player if alive.

        game.enemies.draw(scene)
        game.bullets.draw(scene)
        game.update()  # Draw each bullet and enemy before launching the update method for all of them.
        game.levels()

        # Draw each star on the background scene
        generate_stars()
        paint_stars(scene)
        game.player.move()
        if game.player.is_touching_enemy(game.enemies.sprites()):  # Detects if the player touches any enemy.
            print("Player touched enemy, x: {0}, y: {1},  {2}, HP : {3}".format(game.player.rect.x, game.player.rect.y, game.bullets, game.player.hp))
            game.player.hp -= 1
        display.update()  # Updates the display
        clock.tick(60)
        display.flip()  # Sets the background and refreshes the window

        if sprite.spritecollideany(game.player, game.bullets):  # Detects is there is collision with smth
            bullets = [elem for elem in game.bullets]  # References all bullets in a list
            bullets_hitting = game.player.rect.collidelistall([elem.rect for elem in bullets])  # List all
            # indexes of bullets which rectangle hitbox touches the player's ship
            for bullet in bullets_hitting:  # For each of the concerned bullets, does following action :
                if bullets[bullet] not in game.projectiles:  # If the concerned bullet isn't a player projectile
                    game.player.hp -= bullets[bullet].damage  # Removes hp from the player and kills the bullet
                    print(game.player.hp)
                    bullets[bullet].kill()  # Deletes bullets, since it has hit its target.

        if game.player.hp < 1:  # If the player dies...
            scene.blit(game_over_text, (500, 250))
            for enemy in game.enemies.sprites():
                enemy.kill()  # Kills all enemies.
            for bullet in game.bullets.sprites():
                bullet.kill()  # Kills all bullets.
            game.player.kill()  # Kills the player.
            if not game_over:
                mixer.Sound("assets/game_over.mp3").play()
                game_over = 1

        for thing in event.get():
            if thing.type == QUIT:
                # If quitting event detected, closes the windows
                is_active = False
                quit()
            if thing.type == KEYDOWN and thing.key == K_SPACE and game.player.hp > 0:
                # If the space key is pressed and the player is alive, spawns projectile
                game.spawn(game.player.rect.x + 60, game.player.rect.y + 36, 1, "PlayerProjectile")
            if thing.type == VIDEORESIZE:  # WIP
                new_width = thing.w
                new_height = int(new_width / ratio)
                screen = display.set_mode((new_width, new_height), RESIZABLE)


game_loop()
