from SpaceInvader_gameclass import *
import random

"""
SPACE INVADER
"""

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
secret_code = [K_UP, K_UP, K_DOWN, K_DOWN, K_LEFT, K_RIGHT, K_LEFT, K_RIGHT, K_b, K_a]
code_enter = []
code_index = 0
activated = 0


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
    global code_index
    global code_enter
    global secret_code
    global activated
    game_over = 0
    is_active = True  # Elementary boolean that stays True until QUIT event is triggered.
    while is_active:
        scene.blit(background, (0, 0))  # Draws background.
        draw.rect(scene, (0, 0, 0), (0, 0, 1000, 100))  # Trying to draw a slot for the game stats...
        if game.player.hp > 0:
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
                game.score += game.level*10  # Level Completion bonus at game over.
                game_over = 1

        if game.level == 9 and game_over != 2:  # If the player has completed all the levels...
            print("A.")
            for enemy in game.enemies.sprites():
                enemy.kill()  # Kills all enemies.
            for bullet in game.bullets.sprites():
                bullet.kill()  # Kills all bullets.
            game.player.kill()  # Kills the player.
            mixer.Sound("assets/level_up.mp3").play()
            game_over = 2

        for thing in event.get():
            if thing.type == QUIT:
                # If quitting event detected, closes the windows
                is_active = False
                quit()
            if thing.type == KEYDOWN and thing.key == K_SPACE and game.player.hp > 0:
                # If the space key is pressed and the player is alive, spawns projectile
                game.spawn(game.player.rect.x + 60, game.player.rect.y + 36, 1, "PlayerProjectile")
            if thing.type == KEYDOWN:
                if thing.key == secret_code[code_index]:
                    code_enter.append(thing.key)
                    code_index += 1
                    if code_enter == secret_code:
                        # We removed the index reset to prevent the player from accessing the boss twice.
                        code_index = 0
                        if not activated:
                            for enemy in game.enemies.sprites():
                                enemy.kill()  # Kills all enemies.
                            for bullet in game.bullets.sprites():
                                bullet.kill()  # Kills all bullets.
                            game.activate = 0
                            game.level = 8
                            game.score = 0
                            print("Boss cheatcode activated !")
                            mixer.Sound("./assets/konami vine boom.mp3").play()
                            activated = 1
                else:
                    code_enter = []
                    code_index = 0
            if thing.type == VIDEORESIZE:  # WIP
                new_width = thing.w
                new_height = int(new_width / ratio)
                screen = display.set_mode((new_width, new_height), RESIZABLE)


game_loop()
