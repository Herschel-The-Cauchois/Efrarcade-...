from pygame import *
from SpaceInvader_enemies import bezier_curve_calc  # For displaying curve trajectory purposes


class PlayerGlass(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image.load("./assets/Beer mug.png")
        self.image = transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()  # Creates hit box
        # self.rect = Rect.inflate(self.rect, -15, -15) To see if we need rect redimensioning
        self.rect.x = 0
        self.rect.y = 400


class GoalGlass(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image.load("./assets/Beer mug.png")
        self.image = transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()  # Creates hit box
        # self.rect = Rect.inflate(self.rect, -15, -15) To see if we need rect redimensioning
        self.rect.x = 600
        self.rect.y = 400


class Ball(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image.load("./assets/The BallTM.png")
        self.image = transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()  # Creates hit box
        # self.rect = Rect.inflate(self.rect, -15, -15) To see if we need rect redimensioning
        self.rect.x = 250
        self.rect.y = 200


class Game:
    def __init__(self):
        self.score = 0
        self.game_sprites = sprite.Group()
        self.player_glass = PlayerGlass()  # Instantiates the glass that will represent the player's.
        self.glass_goal = GoalGlass()  # Instantiates the glass surrounded by a few rects
        self.ball = Ball()
        self.game_sprites.add(self.player_glass)  # Adds successfully each sprite to the sprite group for display.
        self.game_sprites.add(self.glass_goal)
        self.game_sprites.add(self.ball)
        print(self.game_sprites.sprites())
