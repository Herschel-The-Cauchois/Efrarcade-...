from BeerPong_classes import *
from pygame.font import *
from pygame import *
import pygame

game_width = 1200
game_height = 500

game_width = 1000
ratio = game_width / game_height

pygame.init()
def info_bar(scene, player1_score, player2_score, try1_left):
    font = pygame.font.Font(None, 30)
    player1 = font.render(f"Player 1 - Score: {player1_score}", True, (255, 255, 255))
    player2 = font.render(f"Player 2 - Score: {player2_score}", True, (255, 255, 255))
    try1 = font.render(f"{try1_left} try left", True, (255, 255, 255))
    player1_rect = player1.get_rect()
    player2_rect = player2.get_rect()
    try1_rect = try1.get_rect()
    player1_rect.left = 10
    player2_rect.right = scene.get_width() - 10
    try1_rect.left = 10
    player1_rect.top = 10
    player2_rect.top = 10
    try1_rect.top = 30
    scene.blit(player1, player1_rect)
    scene.blit(player2, player2_rect)
    scene.blit(try1, try1_rect)

def bp_game_loop(username: str):
    display.set_caption("Efrarcade - Water Pong")
    scene = display.set_mode((700, 500), RESIZABLE)
    background = image.load("./assets/Bar background.jpg")  # Creates a surface for the background of the game
    background = transform.scale(background, (700, 500))
    is_active = True  # Elementary boolean that stays True until QUIT event is triggered.
    game = Game()
    player1_score = 0
    player2_score = 0
    try1_left = 3

    game.vector.graphical_rotation(0, 1, game.ball.rect.center)
    while is_active:
        scene.blit(background, (0, 0))  # Draws background.
        game.game_sprites.update()
        game.game_sprites.draw(scene)
        info_bar(scene, player1_score, player2_score, try1_left)  # Call the info_bar function to display scores
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
                if thing.key == K_SPACE:
                    pass

bp_game_loop("Test")
