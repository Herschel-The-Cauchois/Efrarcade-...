from BeerPong_classes import *


def bp_game_loop(username : str):
    display.set_caption("Efrarcade - Beer Pong")
    scene = display.set_mode((700, 500), RESIZABLE)
    background = image.load("./assets/Bar background.jpg")  # Creates a surface for the background of the game
    background = transform.scale(background, (700, 500))
    is_active = True  # Elementary boolean that stays True until QUIT event is triggered.
    game = Game()
    while is_active:
        scene.blit(background, (0, 0))  # Draws background.
        game.game_sprites.update()
        game.game_sprites.draw(scene)
        display.flip()

        for thing in event.get():
            if thing.type == QUIT:
                # If quitting event detected, closes the windows
                is_active = False
                quit()

bp_game_loop("Test")
