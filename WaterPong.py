import time
import pygame
import csv

from WaterPong_classes import *  # Imports all the classes designed in the Waterpong files.


def import_score():                                                                                     # Function that imports the score from the csv file 
    score = []
    final = []

    with open('score_wp.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            if row and int(row[1])>10:
                score.append(row)
    counter = 1
    while score:
        max_score = 0
        max_index = 0

        for i in range(len(score)):
            if score[i]:
                if int(score[i][1]) > max_score:
                    max_score = int(score[i][1])
                    max_index = i

        final.append(f"{counter}. {score[max_index][0]} : {score[max_index][1]}")
        score.pop(max_index)
        counter += 1
    return final


def info_bar(game):
    info_font = pygame.font.Font("./assets/pixel_font.ttf", 20)
    htp_font = pygame.font.Font("./assets/pixel_font.ttf", 15)
    info_surface = Surface((200, 500))
    info_surface.fill((0, 0, 0))
    essays_txt = info_font.render(f"{game.attempts} tries left", False, (255, 255, 255))
    if game.multiply != 1:
        score_txt = info_font.render(f"Score multiply by {game.multiply}", False, (255, 0, 0))
        info_surface.blit(score_txt, (20, 90))
    info_surface.blit(essays_txt, (20, 10))
    score_txt = info_font.render(f"Score: {game.score}", False, (255, 255, 255))
    info_surface.blit(score_txt, (20, 30))
    acceleration_txt = info_font.render(f"Acceleration: {game.vector.acceleration}", False, (255, 255, 255))
    angle_txt = info_font.render(f"Angle: {game.vector.angle}", False, (255, 255, 255))
    info_surface.blit(acceleration_txt, (20, 50))
    info_surface.blit(angle_txt, (20, 70))
    htp_txt = htp_font.render("Arrows : precise input", False, (255, 255, 255))
    htp_txt2 = htp_font.render("zqsd : faster input", False, (255, 255, 255))
    htp_txt3 = htp_font.render("Space : launch the ball", False, (255, 255, 255))
    info_surface.blit(htp_txt, (15, 110))
    info_surface.blit(htp_txt2, (15, 130))
    info_surface.blit(htp_txt3, (15, 150))
    draw.line(info_surface, (255, 255, 255), (0, 0), (0, 500), 2)
    draw.line(info_surface, (255, 255, 255), (0, 0), (200, 0), 2)
    draw.line(info_surface, (255, 255, 255), (0, 500/2-70), (200, 500/2-70), 2)

    minus = 0
    scores = import_score()

    for i in range(len(scores)):                                                                                #so that we can later just show top 10, for now there is not enought data
        score_text = info_font.render(scores[i], False, (255, 255, 255))
        info_surface.blit(score_text, (10, 500/2-50+minus))
        minus += 30
    return info_surface


def game_over_screen(username, scene, event, score):
    game_over_font = pygame.font.Font("./assets/pixel_font.ttf", 30)
    game_over_text = game_over_font.render("Game Over :( Press Enter to restart", True, (255, 255, 255))
    active = True

    while active:
        for events in event.get():
            if events.type == QUIT:
                active = False
                with open('score_wp.csv', 'a') as file:
                    writer = csv.writer(file)
                    writer.writerow([username, score])

            if events.type == KEYDOWN:
                if events.key == K_RETURN:
                    with open('score_wp.csv', 'a') as file:
                        writer = csv.writer(file)
                        writer.writerow([username, score])
                    bp_game_loop(username)
                    active = False

        scene.blit(game_over_text, (800/2 - game_over_text.get_width()/2, 250))
        display.flip()


def victory_screen(username, scene, event, cup_num, score):
    victory_font = pygame.font.Font("./assets/pixel_font.ttf", 20)
    if cup_num < 4:
        victory_text = victory_font.render(f"Congratulation ! There is still {3-cup_num} cups to get", True, (255, 255, 255))
        victory_text2 = victory_font.render(f"Double ? Press Space to continue or Enter to quit and register score", True, (255, 255, 255))
        scene.blit(victory_text, (800/2 - victory_text.get_width()/2, 250))
        scene.blit(victory_text2, (800/2 - victory_text2.get_width()/2, 300))
    else:
        victory_text = victory_font.render(f"Congratulation ! You won the game !", True, (255, 255, 255))
        scene.blit(victory_text, (800/2 - victory_text.get_width()/2, 250))
    active = True

    while active:
        for events in event.get():
            if events.type == QUIT:
                active = False
                with open('score_wp.csv', 'a') as file:
                    writer = csv.writer(file)
                    writer.writerow([username, score])
                quit()

            if events.type == KEYDOWN:
                if events.key == K_RETURN:
                    with open('score_wp.csv', 'a') as file:
                        writer = csv.writer(file)
                        writer.writerow([username, score])
                    bp_game_loop(username)
                if events.key == K_SPACE and cup_num < 4:
                    active = False


        display.flip()
    print("quit active")


def bp_game_loop(username: str):
    """The function that contains the main program of the game, that will run continuously until ordered to do
        otherwise by user action."""
    pygame.font.init()  # Initializes the parts of pygame that manages the sound and the fonts.
    mixer.init()
    game_over = 0
    display.set_caption("Efrarcade - Water Pong")
    scene = display.set_mode((800, 500), RESIZABLE)
    background = image.load("./assets/Bar background.jpg")  # Creates a surface for the background of the game
    background = transform.scale(background, (800, 500))
    is_active = True  # Elementary boolean that stays True until QUIT event is triggered.
    clock = time.Clock()  # In game clock for screen refreshing rate to smooth animations.
    game = Game()
    game.vector.graphical_rotation(0, 1, game.ball)  # Does the initial rotation of the arrow-vector representing
    # the trajectory's input.
    while is_active:
        clock.tick(10000)
        scene.blit(background, (0, 0))  # Draws background.
        game.game_sprites.update()
        game.game_sprites.draw(scene)
        draw.rect(scene, (0, 255, 0), game.glass_goal1.win_rect)  # For testing, draws collision rectangles
        draw.rect(scene, (0, 255, 0), game.glass_goal2.win_rect)
        draw.rect(scene, (0, 255, 0), game.glass_goal3.win_rect)
        for rectangle in game.forbidden_rects:
            draw.rect(scene, (255, 0, 0), rectangle)
        scene.blit(info_bar(game), (600, 0))
        display.flip()  # Draws every graphical element of the game.
        if game.attempts < 1:
            # If the player has exhausted its attempts, freezes the game and shows the game over screen.
            mixer.Sound("assets/water pong game over.mp3").play()
            game_over_screen(username, scene, event, game.score)
            is_active = False
        if game.launch == 1:
            # This condition verifies that the game is in the ball launching state.
            if game.ball.rect.collidelistall(game.forbidden_rects):
                # Detects if there is any collision with the border of a glass.
                mixer.Sound("assets/ball fell.mp3").play()
                game.attempts -= 1
                print(game.attempts)
                game.launch = 0
            elif game.ball.rect.colliderect(game.glass_goal1.win_rect) or game.ball.rect.colliderect(game.glass_goal2.win_rect) or game.ball.rect.colliderect(game.glass_goal3.win_rect):
                # If the player makes the ball successfully land in the glass
                game.multiply += 1
                game.score += game.attempts * game.multiply
                if game.ball.rect.colliderect(game.glass_goal1.win_rect):
                    game.game_sprites.remove(game.glass_goal1)
                if game.ball.rect.colliderect(game.glass_goal2.win_rect):
                    game.game_sprites.remove(game.glass_goal2)
                if game.ball.rect.colliderect(game.glass_goal3.win_rect):
                    game.game_sprites.remove(game.glass_goal3)
                mixer.Sound("assets/ball placed.mp3").play()
                if game.glass_goal1 not in game.game_sprites and game.glass_goal2 not in game.game_sprites and game.glass_goal3 not in game.game_sprites:
                    # If all the cups have a ball in it, plays the victory sound.
                    mixer.Sound("assets/water pong won.mp3").play()
                victory_screen(username, scene, event, game.multiply, game.score)
                print("Left victory screen")
                game.launch = 0
                game.attempts = 10
                game.ball.rect.center = game.player_glass.rect.midtop
                game_over = 2
            elif not game.ball.launch():
                # If in launch, triggers the launch method of the ball until it reaches its end point or collides with
                # Specific rectangles. If no contact with the winning collision rectangles, notes this as a loss.
                mixer.Sound("assets/ball fell.mp3").play()
                game.attempts -= 1
                print(game.attempts)
                game.launch = 0
        else:
            # If the launch mode is off, automatically puts back the ball to the top of the glass.
            game.ball.rect.center = game.player_glass.rect.midtop

        keys_held = key.get_pressed()
        # Detects if the keys A, E, Z or S are held to increase or decrease faster the angle and acceleration.
        if keys_held[K_q] and not game.launch:
            game.vector.graphical_rotation(game.vector.angle + 1, game.vector.acceleration, game.ball)
        if keys_held[K_d] and not game.launch:
            game.vector.graphical_rotation(game.vector.angle - 1, game.vector.acceleration,
                                           game.ball)
        if keys_held[K_z] and not game.launch:
            game.vector.graphical_rotation(game.vector.angle, game.vector.acceleration + 1,
                                           game.ball)
        if keys_held[K_s] and not game.launch:
            game.vector.graphical_rotation(game.vector.angle, game.vector.acceleration - 1,
                                           game.ball)
        for thing in event.get():
            if thing.type == QUIT:
                # If quitting event detected, closes the windows
                is_active = False
            if thing.type == KEYDOWN:
                # Before the launch of the ball, lets the player adjust precisely the acceleration that the ball will
                # have as well as its angle to maximise the accuracy of the trajectory.
                if thing.key == K_LEFT and not game.launch:
                    game.vector.graphical_rotation(game.vector.angle + 1, game.vector.acceleration, game.ball)
                if thing.key == K_RIGHT and not game.launch:
                    game.vector.graphical_rotation(game.vector.angle - 1, game.vector.acceleration,
                                                   game.ball)
                if thing.key == K_UP and not game.launch:
                    game.vector.graphical_rotation(game.vector.angle, game.vector.acceleration + 1,
                                                   game.ball)
                if thing.key == K_DOWN and not game.launch:
                    game.vector.graphical_rotation(game.vector.angle, game.vector.acceleration - 1,
                                                   game.ball)
                if thing.key == K_SPACE and not game.launch:
                    # If the game hasn't launched the ball and space is pressed, launches the ball.
                    game.ball.trajectory_calculation(game.vector.angle, game.vector.acceleration)
                    # Interesting tuple of values to get in goal glass (72, 17), (67,16), (75,18)
                    game.launch = 1
    quit()

bp_game_loop("Test")
