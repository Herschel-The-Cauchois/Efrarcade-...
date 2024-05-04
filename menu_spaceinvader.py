import pygame_menu
import pygame
from SpaceInvader import game_loop

pygame.init()                                                                           #Initialize the window
surface = pygame.display.set_mode((1000, 500), pygame.RESIZABLE)
pygame.display.set_caption('ARCADE')
mytheme = pygame_menu.Theme(background_color=(0, 0, 0, 0),                              #Transparent background
                title_background_color=(4, 47, 126),
                title_font_shadow=False,
                widget_padding=0)

menu = pygame_menu.Menu('SPACE INVADER',1000, 500,
                       theme=mytheme,
                       mouse_enabled=False,
                       mouse_motion_selection=False)

background = pygame_menu.BaseImage(image_path="assets/background_space_invader.jpg")

def main_background() -> None:
    """
    Background color/image of the main menu. In this function, the user can plot images, play sounds, etc.
    """
    background.draw(surface)


def check_name(value):
    print('User name:', value)
    return value


about_menu = pygame_menu.Menu('About',1000, 500,
                       theme=mytheme,
                       mouse_enabled=False,
                       mouse_motion_selection=False)
about_menu.add.label('Pygame is a python game development library')
about_menu.add.label('Pygame Menu assists in creating game menus')
about_menu.add.button('Return to main menu', pygame_menu.events.BACK)



menu.add.button('Play', game_loop, font_name = pygame_menu.font.FONT_8BIT, font_size = 30, font_color = (0,0,0), selection_color = (255,255,255))
menu.add.button('About',about_menu, font_name = pygame_menu.font.FONT_8BIT, font_size = 30, font_color = (0,0,0), selection_color = (255,255,255))
menu.add.button('Quit', pygame_menu.events.EXIT, font_name = pygame_menu.font.FONT_8BIT, font_size = 30, font_color = (0,0,0), selection_color = (255,255,255))


def main_invader():
    menu.mainloop(surface, main_background)
