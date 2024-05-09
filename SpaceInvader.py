from SpaceInvader_gameclass import *
import random
#csv file
import csv

# score importation from the csv
def import_score():
    score=[]
    final=[]
    with open('score.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            score.append(row)
    counter = 1
    while score:
        max_score = 0
        max_index = 0
        for i in range(len(score)):
            if int(score[i][1]) > max_score:
                max_score = int(score[i][1])
                max_index = i
        final.append(f"{counter}. {score[max_index][0]} : {score[max_index][1]}")
        score.pop(max_index)
        counter += 1
    return final

"""
SPACE INVADER
"""

init()  # Initializes pygame
font.init()  # Initializes font module

# Creates a window with the name of the game, and sets the future background image

screen_width = 1200
screen_height = 500

game_width = 1000
game_height = 500  # Dimensions of the game window
ratio = game_width / game_height
game = Game()  # Initializes the game class
display.set_caption("Efrarcade - Space Invader")  # Titles the pygame window to Efrarcade

clock = time.Clock()
star_positions = []  # Lists that holds the position of each respective star.




def level_bar(player_xp):
    """Creates a rectangle that will show in a % the player's level progression."""
    # Create a surface for the level bar
    level_surface = Surface((100, 25))
    # Fill the rectangle with the player's level progression
    if player_xp < 50 and player_xp > 10:
        draw.rect(level_surface, (255, 255, 0), (0, 0, (player_xp/100)*100, 25))
    elif player_xp < 10:
        draw.rect(level_surface, (255, 0, 0), (0, 0, (player_xp/100)*100, 25))
    else:
        draw.rect(level_surface, (0, 255, 0), (0, 0, (player_xp/100)*100, 25))
    # Draw the border rectangle
    draw.rect(level_surface, (255, 255, 255), (0, 0, 100, 25), 2)
    # Return the level bar surface
    return level_surface

def info_bar():
    info_font = font.SysFont("Comic Sans MS", 30)
    """Right display to show the player's stats."""
    #INIT OF THE INFO BAR
    info_surface = Surface((200, game_height))  # Create a surface for the info bar
    info_surface.fill((0, 0, 0))  # Fill the surface with black color
    # Draw a white line to separate the game and the info bar    
    # DISPLAYS
    hp_text = info_font.render("HP:", False, (255, 255, 255))
    #score_text = game_over_font.render("Score: {}".format(game.player.score), False, (255, 255, 255))
    info_surface.blit(hp_text, (75, 10))
    #level_surface = level_bar(game.player.level, game.player.xp)
    level_surface = level_bar(game.player.hp)
    info_surface.blit(level_surface, (50, 35))  # Adjust the position as needed
    info_surface.blit(info_font.render(f"Level: {game.level}/8", False, (255, 255, 255)), (50, 80))
    info_surface.blit(info_font.render(f"Score: {game.score}", False, (255, 255, 255)), (50, 120))
    draw.line(info_surface, (255, 255, 255), (0, 0), (0, game_height), 2)
    draw.line(info_surface, (255, 255, 255), (0, 0), (200, 0), 2)
    draw.line(info_surface, (255, 255, 255), (0, game_height/2-70), (200, game_height/2-70), 2)

    #SCORES
    minus=0
    scores=import_score()
    for i in scores: #so that we can later just show top 10, for now there is not enought data
        score_text = info_font.render(i, False, (255, 255, 255))
        info_surface.blit(score_text, (10, game_height/2-50+minus))
        minus+=30

    # Blit the info bar onto the scene
    return info_surface


def generate_stars():
    """Generates stars that will move from the right to the left. There is a 10% probability of star generation
    introduced, preventing overabundance of stars. Once created, puts it in a tracking list, then moving it leftwards
    until it is removed from the screen. It disposes of three properties : x position, y position and speed.
    """
    if random.randint(0, 100) < 10:
        star_positions.append([game_width, random.randint(0, game_height), random.randint(1, 3)])
    for star in star_positions:  # Loop that generalizes the behavior to all stars.
        star[0] -= star[2]  # Subtracts x position by the speed.
        if star[0] < 0:  # Detects if it is off the screen.
            star_positions.remove(star)


def paint_stars(s):
    """Draw each star on the scene."""
    for star in star_positions:
        draw.circle(s, (255, 255, 255), (star[0], star[1]), 1)  # Represents them as a circle.


def game_loop(username):
    display.set_caption("Efrarcade - Space Invader")
    scene = display.set_mode((screen_width, screen_height), RESIZABLE)
    background = Surface(scene.get_size())  # Creates a surface for the background of the game
    secret_code = [K_UP, K_UP, K_DOWN, K_DOWN, K_LEFT, K_RIGHT, K_LEFT, K_RIGHT, K_b, K_a]
    code_enter = []
    code_index = 0
    activated = 0
    game_over = 0
    is_active = True  # Elementary boolean that stays True until QUIT event is triggered.
    info_font = font.SysFont("Comic Sans MS", 30)
    game_over_text = info_font.render("Game Over :(", False, (255, 255, 255))
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
        clock.tick(60)
        scene.blit(info_bar(), (game_width, 0))
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
                # show a game over screen
                with open('score.csv', 'a') as file:
                    writer = csv.writer(file)
                    writer.writerow([username, game.score])

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

if __name__ == "__main__":
    game_loop("player")