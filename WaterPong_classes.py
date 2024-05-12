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
        topright_rectangle = self.rect.topright[0], self.rect.topright[1]+20
        bottom_rectangle_tuple = self.rect.bottomleft[0], self.rect.bottomleft[1]-10
        self.loss_rects = [Rect(self.rect.topleft, (10, 100)), Rect(topright_rectangle, (10, 100)), Rect(bottom_rectangle_tuple, (100, 10))]


class GoalGlass(sprite.Sprite):
    def __init__(self, x, y):
        """Initializes the goal glasses' sprite."""
        super().__init__()
        self.image = image.load("./assets/cup_red.png")
        self.image = transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.filled = 0  # Boolean that states whether the ball has already filled this cup.
        self.rect.x = x  # Sets up the glass' coordinates as passed in the function parameters.
        self.rect.y = y
        self.win_rect = Rect(self.rect.topleft, (80, 20))  # This is the only spot where the player can land the ball
        # To win.
        self.loss_rects = [Rect(self.rect.topleft, (10, 100)), Rect((self.rect.topright[0]-20, self.rect.topright[1]), (10, 100))]
        # Defines the hitboxes where if touched, the game will consider it a loss.


class Ball(sprite.Sprite):
    def __init__(self, player_glass_coord: tuple):
        """Initializes the Ball's sprite."""
        super().__init__()
        self.image = image.load("./assets/The BallTM.png")
        self.image = transform.scale(self.image, (25, 25))  # Rescales the sprite.
        self.rect = self.image.get_rect()  # Creates hit box
        self.rect.center = player_glass_coord  # Centers it around the top of the player's glass.
        self.trajectory = []

    def trajectory_calculation(self, angle: int, acceleration: int):
        """Precalculates a list of points in the canvas that will correspond to the skeleton of the trajectory
        the ball will physically follow. Takes into account the angle of launch in degrees related to the ground
        and its acceleration."""
        trajectory_list = []  # Creates an empty list to hold all the mathematical points of the trajectory.
        temp = [self.rect.center[0], self.rect.center[1]]  # This list will hold the successive values of the
        # ball's coordinates after each update following the trajectorial equation.
        t = 0.1
        while 0 < temp[0] < 690 and 0 < temp[1] < 500:  # Until one of the points is out of the game's bounds:
            temp[0] += acceleration*cos(radians(angle))*t  # Adds horizontal displacement to x coordinate.
            temp[1] -= acceleration*sin(radians(angle))*t-0.5*9.81*t**2  # Adds the vertical one for y.
            temp[0], temp[1] = int(temp[0]), int(temp[1])  # Turns the values into integers to be comprehensible by
            # pygame.
            trajectory_list.append([temp[0], temp[1]])  # Appends the newly generated point to the trajectory list.
            t += 0.1
        self.trajectory = trajectory_list  # Places the generated trajectory inside the ball's attribute.
        parabola_momentum = trajectory_list[0]
        for i in range(0, len(self.trajectory)):
            # Looks for the extreme of the parabola by looking for the point with the minimal height. This is because
            # Pygame's y-axis is reversed !
            if self.trajectory[i][1] < parabola_momentum[1]:
                parabola_momentum = self.trajectory[i]
        self.trajectory = bezier_curve_calc([self.trajectory[0], parabola_momentum, self.trajectory[len(self.trajectory)-1]], 1000)  # Extrapolates from the math curve to
        # get a smooth curve movement to display.

    def launch(self):
        """Manages to update point by point the placement of the ball throughout its trajectory in the launch phase. It
        places the ball coordinate pair by coordinate pair following the list of lists in the self.Trajectory attribute,
        deleting the couple of coordinates already went through from the trajectory list after."""
        if self.trajectory:
            self.rect.x = self.trajectory[0][0]  # Sets the coordinates of the ball as those of the point we want
            self.rect.y = self.trajectory[0][1]  # To displace it to.
            self.trajectory.pop(0)  # Removes the point from the lists of points to go through.
            return True
        if not self.trajectory:
            return False  # If the list is empty, return False


class Vector(sprite.Sprite):
    def __init__(self, ball_topright: tuple):
        """Initializes the vector's sprite and its default values."""
        super().__init__()
        self.image = image.load("./assets/vecteur test.png")
        self.orig_image = self.image  # Keeps a copy of the original image to avoid loading it at each transformation.
        self.image = transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect(center=ball_topright)  # Puts the trajectory arrow near and above the ball
        # to visualise.
        self.pos = Vector2(ball_topright)  # Data for rotation management.
        self.offset = Vector2(10, -10)
        self.angle = 0  # Holds the essential data that will be used for the trajectory calculation.
        self.acceleration = 1
        self.length = 1

    def graphical_rotation(self, angle: int, acceleration: int, ball):
        """When called, realizes the scaling and rotation of the arrow vector sprite following an angle and acceleration
         given by user manipulation."""
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
        """Initializes the game globally, the objects and sprites inside it for better global management."""
        self.score = 0
        self.multiply = 1
        self.game_sprites = sprite.Group()
        self.player_glass = PlayerGlass()  # Instantiates the glass that will represent the player's.
        self.glass_goal1 = GoalGlass(500, 400)  # Instantiates the glass surrounded by a few rects
        self.glass_goal2 = GoalGlass(300, 400)
        self.glass_goal3 = GoalGlass(200, 400)
        self.ball = Ball(self.player_glass.rect.midtop)  # Instantiates the ball object
        self.vector = Vector(self.ball.rect.topright)  # Instantiates the vector arrow to visualise the player inputs
        self.game_sprites.add(self.player_glass)  # Adds successfully each sprite to the sprite group for display.
        self.game_sprites.add(self.glass_goal1)
        self.game_sprites.add(self.glass_goal2)
        self.game_sprites.add(self.glass_goal3)
        self.game_sprites.add(self.ball)
        self.game_sprites.add(self.vector)
        self.launch = 0  # Sets the launch state by default to 0.
        self.attempts = 10  # Sets the number of attempts by default to 10.
        # Then creates the list of collision rectangles that will cause a failure.
        self.forbidden_rects = self.glass_goal1.loss_rects + self.glass_goal2.loss_rects + self.glass_goal3.loss_rects + self.player_glass.loss_rects
