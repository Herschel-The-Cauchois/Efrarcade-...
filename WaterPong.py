import time
import pygame

from WaterPong_classes import *  # Imports all the classes designed in the Waterpong files.

def info_bar(game):
    info_font = pygame.font.Font("./assets/pixel_font.ttf", 20)
    info_surface = Surface((200, 500))
    info_surface.fill((0, 0, 0))
    essays_txt = info_font.render(f"Encore {game.attempts} essais", False, (255, 255, 255))
    info_surface.blit(essays_txt, (20, 10))
    return info_surface

def game_over_screen(username, scene, event):
    game_over_font = pygame.font.Font("./assets/pixel_font.ttf", 30)
    game_over_text = game_over_font.render("Game Over :( Press Enter to restart", True, (255, 255, 255))
    active = True

    while active:
        for events in event.get():
            if events.type == QUIT:
                active = False

            if events.type == KEYDOWN:
                if events.key == K_RETURN:
                    bp_game_loop(username)

        scene.blit(game_over_text, (800/2 - game_over_text.get_width()/2, 250))
        display.flip()


def bp_game_loop(username: str):
    pygame.font.init()
    """The function that contains the main program of the game, that will run continuously until ordered to do
    otherwise by user action."""
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
        clock.tick(1000)
        scene.blit(background, (0, 0))  # Draws background.
        game.game_sprites.update()
        game.game_sprites.draw(scene)
        """draw.rect(scene, (0, 255, 0), game.glass_goal.win_rect)  # For testing, draws collision rectangles
        for rectangle in game.forbidden_rects:
            draw.rect(scene, (255, 0, 0), rectangle)"""
        scene.blit(info_bar(game), (600, 0))
        display.flip()  # Draws every graphical element of the game.
        if game.attempts < 1:
            # If the player has exhausted its attempts, freezes the game and shows the game over screen.
            game_over_screen(username, scene, event)
            is_active = False
        if game.launch == 1:
            # This condition verifies that the game is in the ball launching state.
            if game.ball.rect.collidelistall(game.forbidden_rects):
                # Detects if there is any collision with the border of a glass.
                game.attempts -= 1
                print(game.attempts)
                game.launch = 0
            elif game.ball.rect.colliderect(game.glass_goal1.win_rect) or game.ball.rect.colliderect(game.glass_goal2.win_rect) or game.ball.rect.colliderect(game.glass_goal3.win_rect):
                # If the player makes the ball successfully land in the glass
                print("Congrats !")
                game_over = 2
            elif not game.ball.launch():
                # If in launch, triggers the launch method of the ball until it reaches its end point or collides with
                # Specific rectangles. If no contact with the winning collision rectangles, notes this as a loss.
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
