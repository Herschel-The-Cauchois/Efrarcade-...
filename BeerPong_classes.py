from pygame import *
from math import *
from SpaceInvader_enemies import bezier_curve_calc  # For displaying curve trajectory purposes


class PlayerGlass(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image.load("./assets/Water glass.png")
        self.image = transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()  # Creates hit box
        # self.rect = Rect.inflate(self.rect, -15, -15) To see if we need rect redimensioning
        self.rect.x = 0
        self.rect.y = 400


class GoalGlass(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image.load("./assets/Water glass.png")
        self.image = transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()  # Creates hit box
        # self.rect = Rect.inflate(self.rect, -15, -15) To see if we need rect redimensioning
        self.rect.x = 600
        self.rect.y = 400


class Ball(sprite.Sprite):
    def __init__(self, player_glass_coord: tuple):
        super().__init__()
        self.image = image.load("./assets/The BallTM.png")
        self.image = transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()  # Creates hit box
        # self.rect = Rect.inflate(self.rect, -15, -15) To see if we need rect redimensioning
        self.rect.center = player_glass_coord


class Vector(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image.load("./assets/vecteur test.png")
        self.image = transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()  # Creates hit box
        # self.rect = Rect.inflate(self.rect, -15, -15) To see if we need rect redimensioning
        self.rect.x = 50  # Puts the vector at a default place
        self.rect.y = 390
        self.angle = 90
        self.acceleration = 1

    def graphical_rotation(self, angle: int, length: int, center: tuple):
        if 0 <= angle < 91 and 1 <= length <= 10:
            self.image = image.load("./assets/vecteur test.png")
            self.angle = angle
            self.acceleration = length
            self.image = transform.rotate(self.image, angle)
            self.image = transform.scale(self.image, (25+length*5, 25+length*5))
            self.rect = self.image.get_rect()
            if 0 <= angle <= 4:
                self.rect.midleft = center
            elif 4 < angle <= 65:
                print(int(sin(radians(angle))*75))
                self.rect.bottomleft = (center[0], center[1]+20)
            elif 75 <= angle <= 90:
                self.rect.midbottom = center
            return True
        else:
            return False


class Game:
    def __init__(self):
        self.score = 0
        self.game_sprites = sprite.Group()
        self.player_glass = PlayerGlass()  # Instantiates the glass that will represent the player's.
        self.glass_goal = GoalGlass()  # Instantiates the glass surrounded by a few rects
        self.ball = Ball(self.player_glass.rect.midtop)
        self.vector = Vector()
        self.game_sprites.add(self.player_glass)  # Adds successfully each sprite to the sprite group for display.
        self.game_sprites.add(self.glass_goal)
        self.game_sprites.add(self.ball)
        self.game_sprites.add(self.vector)
        self.launch = 0
        print(self.game_sprites.sprites())
