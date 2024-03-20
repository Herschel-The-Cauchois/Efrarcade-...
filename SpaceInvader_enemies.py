from pygame import *
from math import sqrt
from random import randint


def bezier_curve_calc(controls: list, details: int):
    """This very important function use the mathematical work of Bézier to generate a curve on a computer with the
    help of a list of control points to create an exhaustive enough list of the curve's point to be visually
    credible. See material used for the script copied/inspired for the implementation.
    Controls parameter must be a list of 2 element tuples (x,y), details a power of 10."""
    t = 0  # This variable increases for each point generation as it allows the calculation of the "proportion" of one
    # control point's coordinates and its neighbor to pinpoint at one point of the segment between them.
    curve = []  # This list will hold all the points of the future curve.
    while t <= 1:  # Because t is used to get a proportion, it can't be > 1.
        working_list = controls[:]  # To prevent altering original control points list, makes a copy.
        while len(working_list) != 1:
            for pos, coord in enumerate(working_list):  # Enumerate allows us to retrieve easily element + index couple
                # Will pass each control points through the Bezier function and make the last one pop until there is
                # Only one remaining : a point belonging to the curve.
                if coord != working_list[-1]:
                    # Last control point is excluded of course because there is no element after.
                    working_list[pos] = (1-t)*coord[0]+t*working_list[pos+1][0], (1-t)*coord[1]+t*working_list[pos+1][1]
            working_list.pop()
        curve.append(working_list[0])  # Appends found point to the curve list.
        t += 1/details  # Increments t by 1/details, the more the incrementation is small -> more points -> more
        # seamless curve.
    return curve


class Enemies(sprite.Sprite):
    def __init__(self):
        super().__init__()  # Initializes super class that encapsulate all enemies
        self.hp = 0
        self.damage = 0


class EnemyShip(Enemies):
    # Class for the basic enemy ship
    def __init__(self):
        super().__init__()  # Initializes sprite class
        # Classical sprite initialisation : load image, initialize rectangle, positions...
        self.image = image.load("./assets/black_placeholder.svg")
        self.image = transform.scale(self.image, (50, 50))  # Resizes image sprite to correct size
        self.hp = 50  # + sets new common properties for enemies of that type such as constant hp stat
        self.type = "EnemyShip"  # Declares type of enemy for it to be identifiable to the game
        self.damage = 1  # Damage inflicted by the enemy
        self.rect = self.image.get_rect()  # Creates hit box
        self.rect.x = 0
        self.rect.y = 0  # Sets up starting position of the ship by setting up the enemy's coordinate
        self.reached_border = 0
        self.velocity = 2

    def displacement(self):
        # Will move the ship across the screen. This enemy will move in straight lines until it reaches a certain level.
        if self.rect.x >= 950 or self.rect.x <= 10:
            # If the ship is too much to the right, it will lower its altitude before reversing the displacement
            # behavior.
            # If the ship is too much to the left, it will lower its altitude before reversing the displacement
            # behavior.
            if self.rect.y < 400:
                # This condition verifies if the ship isn't too low. If its y coordinate is above designated level,
                # it will not lower again its altitude, and in the case of the lowering process making it go
                # Too much below, it will directly lower it to the minimum altitude.
                if self.rect.y + 8 * (int(sqrt(self.velocity))) > 400:
                    self.rect.y = 400
                else:
                    self.rect.y += 8 * (int(sqrt(self.velocity)))  # The sqrt factor makes the altitude loss dependent
                    # on velocity but helps attenuate the effect instead of using a constant when the velocity is high.
            if self.rect.x >= 950:
                self.reached_border = 1
            else:
                self.reached_border = 0
        if self.reached_border == 0:
            self.rect.x += 1 * self.velocity
        elif self.reached_border == 1:
            self.rect.x -= 1 * self.velocity


class Sinusoid(Enemies):
    # New enemy, sinusoid, which will follow a sinusoidal trajectory
    def __init__(self):
        super().__init__()  # Initializes sprite class
        # Classical sprite initialisation : load image, initialize rectangle, positions...
        self.image = image.load("./assets/white_placeholder.svg")
        self.image = transform.scale(self.image, (30, 50))  # Resizes image sprite to correct size
        self.hp = 50  # + sets new common properties for enemies of that type such as constant hp stat
        self.type = "Sinusoid"  # Declares type of enemy for it to be identifiable to the game
        self.damage = 5  # Damage inflicted by the enemy
        self.rect = self.image.get_rect()  # Creates hit box
        self.rect.x = 0
        self.rect.y = 0  # Sets up starting position of the ship by setting up the enemy's coordinate
        self.reached_border = 0  # Determines if the ship has reached one of the borders.
        self.trajectory = []  # This attribute host the list of points the enemy will have to go through.
        self.velocity = 10

    def displacement(self):
        # Will move the ship across the screen. This enemy will move in sinusoidal-simile curves
        # until it reaches a certain border.
        if not self.trajectory:  # This boolean expression was proposed by the IDE to detect when this list is empty.
            # if said list is empty, it means it completed a calculated trajectory.
            # If the ship is too much to the right, it will lower its altitude before reversing the displacement
            # behavior.
            # If the ship is too much to the left, it will lower its altitude before reversing the displacement
            # behavior.
            if self.rect.y < 400:
                # This condition verifies if the ship isn't too low. If its y coordinate is above designated level,
                # it will not lower again its altitude, and in the case of the lowering process making it go
                # Too much below, it will directly lower it to the minimum altitude.
                if self.rect.y + 8 * (int(sqrt(self.velocity))) > 400:
                    self.rect.y = 400
                else:
                    self.rect.y += 8 * (int(sqrt(self.velocity)))  # The sqrt factor makes the altitude loss dependent
                    # on velocity but helps attenuate the effect instead of using a constant when high velocity.
            if (self.rect.x - 950) > -900:
                # Since the trigger for knowing when a Sinusoid has reached the game's border is different, this
                # condition tests differently due to the unpredictability of the Bézier curve points if it has
                # hit a border.
                self.reached_border = 1
            else:
                self.reached_border = 0
            if self.reached_border:
                # The iterations down there allows the easy recreation of the periodic pattern of the sine wave.
                for i in range(0, 19):
                    # A sine wave can be resumed in 4 points : start, location of maximum, location of minimum,
                    # end point. For the control points to emulate better a sine wave pattern, each control points
                    # are located relative to 50 pixel periods from the right border (950 px for x).
                    self.trajectory += bezier_curve_calc(
                        [(950 - 50 * i, self.rect.y), (950 - 50 * i - 13, self.rect.y + 75),
                         (950 - 50 * i - 38, self.rect.y - 75), (950 - 50 * (i + 1), self.rect.y)], 100)
            elif not self.reached_border:
                # Same as above, except control points are located relative to the left border (x = 0).
                for i in range(0, 19):
                    self.trajectory += bezier_curve_calc(
                        [(0 + 50 * i, self.rect.y), (0 + 50 * i + 13, self.rect.y + 75),
                         (0 + 50 * i + 38, self.rect.y - 75), (0 + 50 * (i + 1), self.rect.y)], 100)
        else:
            # Case where the trajectory defined in the curve list is not done. It will go through in one update to
            # velocity times 1 point.
            for i in range(0, self.velocity):
                if self.trajectory:  # conditions checks if during the execution of the loop, there is still
                    # elements in the curve list to prevent out of range related errors.
                    self.rect.x = self.trajectory[0][0]
                    self.rect.y = self.trajectory[0][1]
                    self.trajectory.pop(0)  # After going to a point, the sprite doesn't need to go through it again.
                    # Hence, it is deleted. In the order of the indexes.


class Randominator(Enemies):
    def __init__(self):
        super().__init__()  # Initializes sprite class
        # Classical sprite initialisation : load image, initialize rectangle, positions...
        self.image = image.load("./assets/red_placeholder.svg")
        self.image = transform.scale(self.image, (40, 35))  # Resizes image sprite to correct size
        self.hp = 100  # + sets new common properties for enemies of that type such as constant hp stat
        self.type = "Randominator"  # Declares type of enemy for it to be identifiable to the game
        self.damage = 10  # Damage inflicted by the enemy
        self.rect = self.image.get_rect()  # Creates hit box
        self.rect.x = 0
        self.rect.y = 0  # Sets up starting position of the ship by setting up the enemy's coordinate
        self.reached_border = 0  # Determines if the ship has reached one of the borders.
        self.trajectory = []  # This attribute host the list of points the enemy will have to go through.
        self.velocity = 10

    def displacement(self):
        if not self.trajectory:
            control_points = [(randint(0, 950), randint(10, 390)) for k in range(0, randint(3, 13))]
            # Self generate a certain number of control points to be able to randomly generate a trajectory.
            for i in range(0, len(control_points)):
                # To be able to have a somewhat coherent trajectory, the control points are selection sorted by distance
                # from the initial position of the ship.
                maxdis = 0  # variable that store the maximum distance to reduce calculations during the sort.
                maxind = 0  # index of the set of coordinates with maximum distance variable.
                maxpos = (self.rect.x, self.rect.y)  # where the tuple with maximum distance will be temporarily stored
                # for the swap down below.
                for j in range(0, len(control_points)-i):
                    if sqrt(((control_points[j][0]-self.rect.x)**2)+((control_points[j][1]-self.rect.y)**2)) > maxdis:
                        # If 2D vectorial distance calculation of one of the control points is superior to the
                        # previous maximum distance, takes its information in the specified variables for it to become
                        # the set of coordinates with maximum distance from the starting point.
                        maxdis = sqrt(((control_points[j][0]-self.rect.x)**2)+((control_points[j][1]-self.rect.y)**2))
                        maxpos = control_points[j]
                        maxind = j
                # Swaps the positions of the tuple containing the coordinates with maximum distance in the control
                # point list with the tuple at the last position of the considered control point list.
                temp = control_points[len(control_points)-1-i]
                control_points[len(control_points)-1-i] = maxpos
                control_points[maxind] = temp
            control_points = [(self.rect.x, self.rect.y)] + control_points
            self.trajectory = bezier_curve_calc(control_points, 1000)
        else:
            # Case where the trajectory defined in the curve list is not done. It will go through in one update to
            # velocity times 1 point.
            for i in range(0, self.velocity):
                if self.trajectory:  # conditions checks if during the execution of the loop, there is still
                    # elements in the curve list to prevent out of range related errors.
                    self.rect.x = self.trajectory[0][0]
                    self.rect.y = self.trajectory[0][1]
                    self.trajectory.pop(0)  # After going to a point, the sprite doesn't need to go through it again.
                    # Hence, it is deleted. In the order of the indexes.


class EnemyBullets(Enemies):
    def __init__(self):
        super().__init__()  # Initializes sprite class
        # Classical sprite initialisation : load image, initialize rectangle, positions...
        self.image = image.load("./assets/white_placeholder.svg")
        self.image = transform.scale(self.image, (10, 20))  # Resizes image sprite to correct size
        self.hp = 1  # + sets new common properties for enemies of that type such as constant hp stat
        self.type = "EnemyBullet"  # Declares type of enemy for it to be identifiable to the game
        self.damage = 1  # Damage inflicted by the enemy
        self.rect = self.image.get_rect()  # Creates hit box
        self.rect.x = 0
        self.rect.y = 0  # Sets up starting position of the ship by setting up the enemy's coordinate
        self.reached_border = 0  # Determines if the ship has reached one of the borders.
        self.velocity = 10

    def displacement(self):  # Displacement function
        if self.rect.y < 400:
            self.rect.y += self.velocity  # Displaces the bullet of a number of pixel equal to the velocity.
        else:
            self.kill()  # Once it has reached the border, will automatically disappear.
