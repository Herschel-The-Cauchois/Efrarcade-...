import pygame
import sys
scene=pygame.display.set_mode((1000, 1000))
def level_bar(player_level, player_xp):
    """Creates a rectangle that will show in a % the player's level progression."""
    
    pygame.draw.rect(scene, (0, 255, 0), (0, 0, (player_xp/100)*100, 25))                           # Fill the rectangle with the player's level progression
    pygame.draw.rect(scene, (255, 255, 255), (0, 0, 100, 25), 2)                                    # Draw the border rectangle


def game_loop():
    """Main game loop."""
    while True:
        level_bar(1, 50)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

game_loop()