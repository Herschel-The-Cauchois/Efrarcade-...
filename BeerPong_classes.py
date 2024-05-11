from pygame import *
from math import *
from SpaceInvader_enemies import bezier_curve_calc  # For displaying curve trajectory purposes
clock = time.Clock()


class PlayerGlass(sprite.Sprite):
    def __init__(self):
        """Initializes the glass as a simple graphic sprite."""
        super().__init__()
        self.image = image.load("./assets/Water glass.png")
        self.image = transform.scale(self.image, (100, 100))  # Rescales glass image after loading it
        self.rect = self.image.get_rect()  # Creates general hitbox
        self.rect.x = 0
        self.rect.y = 400


class GoalGlass(sprite.Sprite):
    def __init__(self):
        """Initializes the goal glasses' sprite."""
        super().__init__()
        self.image = image.load("./assets/Water glass.png")
        self.image = transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = 600
        self.rect.y = 400


class Ball(sprite.Sprite):
    def __init__(self, player_glass_coord: tuple):
        """Initializes the Ball's sprite."""
        super().__init__()
        self.image = image.load("./assets/The BallTM.png")
        self.image = transform.scale(self.image, (25, 25))  # Rescales the sprite.
        self.rect = self.image.get_rect()  # Creates hit box
        # self.rect = Rect.inflate(self.rect, -15, -15) To see if we need rect redimensioning
        self.rect.center = player_glass_coord  # Centers it around the top of the player's glass.
        self.trajectory = []

    def trajectory_calculation(self, angle: int, acceleration: int):
        """Precalculates a list of points in the canvas that will correspond to the skeleton of the trajectory
        the ball will physically follow. Takes into account the angle of launch in degrees related to the ground
        and its acceleration."""
        print((angle, acceleration))
        trajectory_list = []  # Creates an empty list to hold all the mathematical points of the trajectory.
        temp = [self.rect.center[0], self.rect.center[1]]  # This list will hold the successive values of the
        # ball's coordinates after each update following the trajectorial equation.
        t = 0.1
        while 0 < temp[0] < 690 and 0 < temp[1] < 500:  # Until one of the points is out of bounds:
            temp[0] += acceleration*cos(radians(angle))*t  # Adds horizontal displacement to x coordinate.
            temp[1] -= acceleration*sin(radians(angle))*t-0.5*9.81*t**2  # Adds the vertical one for y.
            temp[0], temp[1] = int(temp[0]), int(temp[1])  # Turns the values into integers to be comprehensible by
            # pygame.
            trajectory_list.append([temp[0], temp[1]])  # Appends the newly generated point to the trajectory list.
            t += 0.1
        self.trajectory = trajectory_list  # Places the generated trajectory inside the ball's attribute.
        parabola_momentum = trajectory_list[0]
        for i in range(0, len(self.trajectory)):
            # Looks for the extremum of the parabola by looking for the point with the minimal height. This is because
            # Pygame's y-axis is reversed !
            if self.trajectory[i][1] < parabola_momentum[1]:
                parabola_momentum = self.trajectory[i]
        self.trajectory = bezier_curve_calc([self.trajectory[0], parabola_momentum, self.trajectory[len(self.trajectory)-1]], 1000)  # Extrapolates from the math curve to
        # get a smooth curve movement to display.

    def launch(self):
        if self.trajectory:
            self.rect.x = self.trajectory[0][0]
            self.rect.y = self.trajectory[0][1]
            self.trajectory.pop(0)
            return True
        if not self.trajectory:
            return False


class Vector(sprite.Sprite):
    def __init__(self, ball_topright: tuple):
        super().__init__()
        self.image = image.load("./assets/vecteur test.png")
        self.orig_image = self.image  # Keeps a copy of the original image to avoid loading it at each transformation.
        self.image = transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect(center=ball_topright)  # Puts the trajectory arrow near and above the ball for schematisation.
        self.pos = Vector2(ball_topright)  # Data for rotation management.
        self.offset = Vector2(10, -10)
        self.angle = 0  # Holds the essential data that will be used for the trajectory calculation.
        self.acceleration = 1
        self.length = 1

    def graphical_rotation(self, angle: int, acceleration: int, ball):
        if 0 <= angle < 91 and 1 <= acceleration <= 30:
            self.angle = angle
            self.length = int(acceleration/3)
            self.acceleration = acceleration  # Modifies the input data with the player's modifications.
            # Applies length and angle transformation to the arrow. To preserve its position, the offset vectors once
            # Rotated allows a recalibration of the position due to the rect modifications induced by image rotation.
            self.image = transform.rotozoom(self.orig_image, self.angle, 1)
            self.image = transform.scale(self.image, (20 + self.length * 5, 20 + self.length * 5))
            offset_rotation = self.offset.rotate(angle)
            self.rect = self.image.get_rect(center=self.pos+offset_rotation)  # Places the arrow at the desired
            # Corrected position.
            return True
        else:
            # If the player's modification induces entering wrong values, doesn't do anything.
            return False


class Game:
    def __init__(self):
        self.score = 0
        self.game_sprites = sprite.Group()
        self.player_glass = PlayerGlass()  # Instantiates the glass that will represent the player's.
        self.glass_goal = GoalGlass()  # Instantiates the glass surrounded by a few rects
        self.ball = Ball(self.player_glass.rect.midtop)
        self.vector = Vector(self.ball.rect.topright)
        self.game_sprites.add(self.player_glass)  # Adds successfully each sprite to the sprite group for display.
        self.game_sprites.add(self.glass_goal)
        self.game_sprites.add(self.ball)
        self.game_sprites.add(self.vector)
        self.launch = 0
        self.forbidden_rects = []
        print(self.game_sprites.sprites())
