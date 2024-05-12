from BeerPong_classes import *
from pygame.font import *
from pygame import *
import pygame

game_width = 1200
game_height = 500

game_width = 1000
ratio = game_width / game_height

pygame.init()
def info_bar(scene, player1_score, player2_score):
    font = pygame.font.Font(None, 30)
    text1 = font.render(f"Player 1 - Score: {player1_score}", True, (255, 255, 255))
    text2 = font.render(f"Player 2 - Score: {player2_score}", True, (255, 255, 255))
    text1_rect = text1.get_rect()
    text2_rect = text2.get_rect()
    text1_rect.left = 10
    text2_rect.right = scene.get_width() - 10
    text1_rect.top = 10
    text2_rect.top = 10
    scene.blit(text1, text1_rect)
    scene.blit(text2, text2_rect)

def bp_game_loop(username: str):
    display.set_caption("Efrarcade - Water Pong")
    scene = display.set_mode((700, 500), RESIZABLE)
    background = image.load("./assets/Bar background.jpg")  # Creates a surface for the background of the game
    background = transform.scale(background, (700, 500))
    is_active = True  # Elementary boolean that stays True until QUIT event is triggered.
    game = Game()
    player1_score = 0
    player2_score = 0

    game.vector.graphical_rotation(0, 1, game.ball.rect.center)
    while is_active:
        scene.blit(background, (0, 0))  # Draws background.
        game.game_sprites.update()
        game.game_sprites.draw(scene)
        info_bar(scene, player1_score, player2_score)  # Call the info_bar function to display scores
        display.flip()

        for thing in event.get():
            if thing.type == QUIT:
                # If quitting event detected, closes the windows
                is_active = False
                quit()
            if thing.type == KEYDOWN:
                if thing.key == K_LEFT:
                    game.vector.graphical_rotation(game.vector.angle + 1, game.vector.acceleration, game.ball.rect.center)
                if thing.key == K_RIGHT:
                    game.vector.graphical_rotation(game.vector.angle - 1, game.vector.acceleration,
                                                   game.ball.rect.center)
                if thing.key == K_UP:
                    game.vector.graphical_rotation(game.vector.angle, game.vector.acceleration + 1,
                                                   game.ball.rect.center)
                if thing.key == K_DOWN:
                    game.vector.graphical_rotation(game.vector.angle, game.vector.acceleration - 1,
                                                   game.ball.rect.center)

bp_game_loop("Test")
