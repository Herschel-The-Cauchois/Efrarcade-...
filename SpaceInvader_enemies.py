from math import sqrt
from random import *
from SpaceInvader_player import *


def bezier_curve_calc(controls: list, details: int):
    """
    This very important function use the mathematical work of 
    Bézier to generate a curve on a computer with the help of 
    a list of control points to create an exhaustive enough list 
    of the curve's point to be visually credible. See material 
    used for the script copied/inspired for the implementation.
    Controls parameter must be a list of 2 element tuples (x,y), 
    details a power of 10.
    """
    t = 0                                                                               # This variable increases for each point generation as it allows the calculation of the "proportion" of one
                                                                                        # control point's coordinates and its neighbor to pinpoint at one point of the segment between them.
    curve = []                                                                          # This list will hold all the points of the future curve.
    while t <= 1:                                                                       # Because t is used to get a proportion, it can't be > 1.
        working_list = controls[:]                                                      # To prevent altering original control points list, makes a copy.
        while len(working_list) != 1:
            for pos, coord in enumerate(working_list):                                  # Enumerate allows us to retrieve easily element + index couple
                """
                Will pass each control points through the Bezier 
                function and make the last one pop until there is
                Only one remaining : a point belonging to the curve.
                """
                if coord != working_list[-1]:                           # Last control point is excluded of course because there is no element after.
                    working_list[pos] = int((1-t)*coord[0]+t*working_list[pos+1][0]), int((1-t)*coord[1]+t*working_list[pos+1][1])
            working_list.pop()
        curve.append(working_list[0])                                                   # Appends found point to the curve list.
        t += 1/details                                                                  # Increments t by 1/details, the more the incrementation is small -> more points -> more seamless curve.
    return curve


class Enemies(sprite.Sprite):
    def __init__(self):
        super().__init__()                                                              # Initializes super class that encapsulate all enemies
        self.hp = 0
        self.damage = 0
        self.time = 0


class EnemyShip(Enemies):                                                               # Class for the basic enemy ship
    def __init__(self):
        super().__init__()                                                              # Initializes sprite class
        """
        Classical sprite initialisation : load image, initialize rectangle, positions...
        """
        self.image = image.load("./assets/EnemyShip.png")
        self.image = transform.scale(self.image, (50, 50))                              # Resizes image sprite to correct size
        self.image = transform.rotate(self.image, -90)                                  # Rotates the enemy to face the left side of the screen
        self.hp = 50                                                                    # + sets new common properties for enemies of that type such as constant hp stat
        self.type = "EnemyShip"                                                         # Declares type of enemy for it to be identifiable to the game
        self.damage = 1                                                                 # Damage inflicted by the enemy
        self.rect = self.image.get_rect()                                               # Creates hit box
        self.rect = Rect.inflate(self.rect, -15, -15)
        self.rect.x = 0
        self.rect.y = 0                                                                 # Sets up starting position of the ship by setting up the enemy's coordinate
        self.reached_border = 0
        self.velocity = 2
        self.cadence = 3
        self.score = 25                                                                 # For each enemy, the number of points given when they are killed

    def displacement(self):
        """
        Method that moves the ship across the screen. 
        This enemy will move in straight lines until it 
        reaches a certain level to leave space for the 
        player to move.
        """
        if self.rect.y >= 450 or self.rect.y <= 10:                                     # If the ship is too high or too low, it will move it to the left before reversing the displacement behavior.
            
            if self.rect.x > 100:
                """
                This condition verifies if the ship isn't too 
                much to the left. If its x coordinate is too low,
                it will move it leftward anymore, or move it 
                to the strict minimum x coordinate. This is to 
                let a space for the player to move.
                """
                if self.rect.x - 8 * (int(sqrt(self.velocity))) < 100:
                    self.rect.x = 100
                else:
                    for i in range(0, 8):
                        self.rect.x -= 1 * (int(sqrt(self.velocity)))                   # The sqrt factor makes the left translation
                                                                                        # movement dependent on velocity but helps attenuate the effect when the velocity is high.
            if self.rect.y >= 450:
                self.reached_border = 1
            else:
                self.reached_border = 0
        if self.reached_border == 0:
            self.rect.y += 1 * self.velocity
        elif self.reached_border == 1:
            self.rect.y -= 1 * self.velocity

    def detection(self, player):
        """
        Detects the position of the player relative to the ship and returns a 
        tuple containing the expected position of the bullet that will be spawned, 
        the bullet's damage and its rotation angle to aim at the player's ship. 
        The cadence attribute allows to personalize the frequency of bullet spawning 
        in a certain amount of time.
        """
        if player.rect.x < self.rect.x - 35:                                            # Detects the position of the player relative to the ship's position.
            flag = 0

        elif player.rect.x < self.rect.x + 35 and player.rect.y < self.rect.y:
            flag = 1

        elif player.rect.x < self.rect.x + 35 and player.rect.y > self.rect.y:
            flag = 3

        else:
            flag = 2

        if self.time >= 100/self.cadence:
            self.time = 0
            if flag == 0:                                                               # Makes the bullet spawn to the left of the enemy.
                return self.rect.x-20, self.rect.y+20, -90, self.damage
            
            if flag == 1:                                                               # Bis repetita for different positions, here above the enemy.
                return self.rect.x+20, self.rect.y-20, 180, self.damage
            
            if flag == 2:                                                               # Right of the enemy.
                return self.rect.x+50, self.rect.y+20, 90, self.damage
            
            if flag == 3:                                                               # Under the enemy.
                return self.rect.x+20, self.rect.y+50, 0, self.damage
        
        else:                                                                           # If the timer isn't at the right value, increments it and returns a tuple of incorrect values.
            self.time += 1
            return -1, -1, 0, 0


class Sinusoid(Enemies):                                                            # New enemy, sinusoid, which will follow a sinusoidal trajectory
    def __init__(self):
        super().__init__()                                                          # Initializes sprite class
       
        # Classical sprite initialisation : load image, initialize rectangle, positions...
        self.image = image.load("./assets/Sinusoid.png")
        self.image = transform.scale(self.image, (30, 50))                          # Resizes image sprite to correct size
        self.image = transform.rotate(self.image, -90)                              # Rotates the enemy to face the left side of the screen
        self.hp = 50                                                                # + sets new common properties for enemies of that type such as constant hp stat
        self.type = "Sinusoid"                                                      # Declares type of enemy for it to be identifiable to the game
        self.damage = 5                                                             # Damage inflicted by the enemy
        self.rect = self.image.get_rect()                                           # Creates hit box
        self.rect = Rect.inflate(self.rect, -5, -5)
        self.rect.x = 0
        self.rect.y = 0                                                             # Sets up starting position of the ship by setting up the enemy's coordinate
        self.reached_border = 0                                                     # Determines if the ship has reached one of the borders.
        self.trajectory = []                                                        # This attribute host the list of points the enemy will have to go through.
        self.velocity = 10
        self.cadence = 3
        self.score = 35

    def displacement(self):
        """
        This method moves the ship across the screen. This enemy will 
        move in sinusoidal-simile curves until a certain level until 
        it reaches a certain border.
        """
        if not self.trajectory:                                                     # This boolean expression was proposed by the IDE to detect when this list is empty.
                                                                                    # if said list is empty, it means it completed a calculated trajectory.
                                                                                    # It will perform anyway a similar behavior reversal pattern as for the simple EnemyShip
            if self.rect.x > 100:                                                   # This condition verifies if the ship isn't on the left. If its x coordinate is below designated level,
                                                                                    # it will not lower again its altitude, or place it at the minimal x level.
                if self.rect.x - 8 * self.velocity < 100:
                    self.rect.x = 100
                
                else:
                    self.rect.x -= 8 * self.velocity                                # Sqrt attenuation isn't used here due to the general low velocity of the sinusoid
            
            if (self.rect.y - 450) > -400:                                          # Since the trigger for knowing when a Sinusoid has reached the game's border is different, this
                                                                                    # condition tests differently due to the unpredictability of the Bézier curve points if it has hit a border.
                self.reached_border = 1
            
            else:
                self.reached_border = 0
            
            if self.reached_border:                                                 # The iterations down there allows the easy recreation of the periodic pattern of the sine wave.
                for i in range(0, 10):
                                                                                    # A sine wave can be resumed in 4 points : start, location of maximum, location of minimum,
                                                                                    # end point. For the control points to emulate better a sine wave pattern, each control points
                                                                                    # are located relative to 50 pixel periods from the lower border (500 px for y).
                    self.trajectory += bezier_curve_calc(
                        [(self.rect.x, 500 - 50 * i), (self.rect.x + 75, 500 - 50 * i - 13),
                         (self.rect.x - 75, 500 - 50 * i - 38,), (self.rect.x, 500 - 50 * (i + 1))], 100)
            
            elif not self.reached_border:                                           # Same as above, except control points are located relative to the upper border (y = 0).
                for i in range(0, 10):
                    self.trajectory += bezier_curve_calc(
                        [(self.rect.x, 0 + 50 * i), (self.rect.x + 75, 0 + 50 * i + 13),
                         (self.rect.x - 75, 0 + 50 * i + 38,), (self.rect.x, 0 + 50 * (i + 1))], 100)
        
        else:                                                                       # Case where the trajectory defined in the curve list is not done. It will go through in one update to velocity times 1 point.
            for i in range(0, self.velocity):
                if self.trajectory:                                                 # conditions checks if during the execution of the loop, there is still elements in the curve list to prevent out of range related errors.
                    self.rect.x = self.trajectory[0][0]
                    self.rect.y = self.trajectory[0][1]
                    self.trajectory.pop(0)                                          # After going to a point, the sprite doesn't need to go through it again.
                                                                                    # Hence, it is deleted. In the order of the indexes.

    def detection(self, player):
        """
        Detects the position of the player relative to the ship and returns 
        a tuple containing the expected position of the bullet that will be 
        spawned, the bullet's damage and its rotation angle to aim at the
        player's ship. The cadence attribute allows to personalize the frequency 
        of bullet spawning in a certain amount of time.
        """
        if player.rect.x < self.rect.x - 35:                                        # Detects the position of the player relative to the ship's position.
            flag = 0

        elif player.rect.x < self.rect.x + 35 and player.rect.y < self.rect.y:
            flag = 1

        elif player.rect.x < self.rect.x + 35 and player.rect.y > self.rect.y:
            flag = 3

        else:
            flag = 2

        if self.time >= 100 / self.cadence:
            self.time = 0
            if flag == 0:                                                           # Makes the bullet spawn to the left of the enemy.
                return self.rect.x - 20, self.rect.y + 9, -90, self.damage
            
            if flag == 1:                                                           # Bis repetita for different positions, here above the enemy.
                return self.rect.x + 20, self.rect.y - 20, 180, self.damage
            
            if flag == 2:                                                           # Right of the enemy.
                return self.rect.x + 50, self.rect.y + 9, 90, self.damage
            
            if flag == 3:                                                           # Under the enemy.
                return self.rect.x + 20, self.rect.y + 30, 0, self.damage
        
        else:                                                                       # If the timer isn't at the right value, increments it and returns a tuple of incorrect values.
            self.time += 1
            return -1, -1, 0, 0


class Randominator(Enemies):                                                        #Pretty much identical
    def __init__(self):
        super().__init__()  

        self.image = image.load("./assets/Randominator.png")
        self.image = transform.scale(self.image, (40, 35))                          # Resizes image sprite to correct size
        self.image = transform.rotate(self.image, -90)                              # Rotates the enemy to face the left side of the screen
        self.hp = 100                                                               # + sets new common properties for enemies of that type such as constant hp stat
        self.type = "Randominator"                                                  # Declares type of enemy for it to be identifiable to the game
        self.damage = 10                                                            # Damage inflicted by the enemy
        self.rect = self.image.get_rect()                                           # Creates hit box
        self.rect = Rect.inflate(self.rect, -15, -15)
        self.rect.x = 0
        self.rect.y = 0 
        self.reached_border = 0  
        self.trajectory = []  
        self.velocity = 10
        self.cadence = 3
        self.score = 100

    def displacement(self):
        """
        This method makes the enemy move following a random calculated trajectory 
        by the Bézier curve function methodology. It hence generates a certain number 
        of random control points that will generate a random trajectory if the self-
        trajectory attribute list is empty, or else make the enemy go through as many 
        points of the trajectory as there is units in the velocity attribute.
        """
        
        if not self.trajectory:
            control_points = [(randint(100, 950), randint(10, 475)) for k in range(0, randint(3, 16))]  # Self generate a certain number of control points to be able to randomly generate a trajectory.
            for i in range(0, len(control_points)):                                                     # To be able to have a somewhat coherent trajectory, the control points are selection sorted by distance from the initial position of the ship.
                maxdis = 0                                                                              # variable that store the maximum distance to reduce calculations during the sort.
                maxind = 0                                                                              # index of the set of coordinates with maximum distance variable.
                maxpos = (self.rect.x, self.rect.y)                                                     # where the tuple with maximum distance will be temporarily stored for the swap down below.
                for j in range(0, len(control_points)-i):
                    if sqrt(((control_points[j][0]-self.rect.x)**2)+((control_points[j][1]-self.rect.y)**2)) > maxdis:
                        """
                        If 2D vectorial distance calculation of one of the control points is superior to the
                        previous maximum distance, takes its information in the specified variables for it to become
                        the set of coordinates with maximum distance from the starting point.
                        """
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
                if self.trajectory:                                                                     # conditions checks if during the execution of the loop, there is stil elements in the curve list to prevent out of range related errors.
                    self.rect.x = self.trajectory[0][0]
                    self.rect.y = self.trajectory[0][1]
                    self.trajectory.pop(0)                                                              # After going to a point, the sprite doesn't need to go through it again.
                   

    def detection(self, player):
        """
        Detects the position of the player relative to the ship and returns a 
        tuple containing the expected position of the bullet that will be spawned, 
        the bullet's damage and its rotation angle to aim at the player's ship. 
        The cadence attribute allows to personalize the frequency of bullet spawning 
        in a certain amount of time.
        """
        if player.rect.x < self.rect.x - 35:
            flag = 0

        elif player.rect.x < self.rect.x + 15 and player.rect.y < self.rect.y:
            flag = 1

        elif player.rect.x < self.rect.x + 15 and player.rect.y > self.rect.y:
            flag = 3

        else:
            flag = 2
        
        if self.time >= 100 / self.cadence:
            self.time = 0
            if flag == 0:                                                           # Makes the bullet spawn to the left of the enemy.
                return self.rect.x - 20, self.rect.y + 15, -90, self.damage
            
            if flag == 1:                                                           # Bis repetita for different positions, here above the enemy.
                return self.rect.x + 13, self.rect.y - 20, 180, self.damage
            
            if flag == 2:                                                           # Right of the enemy.
                return self.rect.x + 35, self.rect.y + 15, 90, self.damage
            
            if flag == 3:                                                           # Under the enemy.
                return self.rect.x + 13, self.rect.y + 40, 0, self.damage
        
        else:
            self.time += 1
            return -1, -1, 0, 0


class EnemyBullets(Enemies):                                                        # Same here                      
    def __init__(self):
        super().__init__() 
        self.image = image.load("./assets/white_placeholder.svg")
        self.image = transform.scale(self.image, (7, 15))  
        self.transformation = 0.
        self.hp = 1
        self.type = "EnemyBullet"
        self.damage = 1
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.reached_border = 0 
        self.velocity = 10

    def displacement(self):
        """
        Method that will make the enemy bullet move through the screen in 
        a linear trajectory, deduced from the transformation impulsed by the 
        game's spawn method to the EnemyBullet instance.
        """
        if 10 < self.rect.x < 990 and 10 < self.rect.y < 490:
            if self.transformation == -90:
                self.rect.x -= self.velocity                                        # Displaces the bullet of a number of pixel equal to the velocity.
            elif self.transformation == 0:
                self.rect.y += self.velocity
            elif self.transformation == 90:
                self.rect.x += self.velocity
            elif self.transformation == 180:
                self.rect.y -= self.velocity
        else:
            self.kill()                                                             # Once it has reached the border, will automatically disappear.

    def rotate(self):
        """
        Method that applies a rotation transformation following the rotation 
        angle given by the transformation attribute.
        """
        self.image = transform.rotate(self.image, self.transformation)


class Boss(Enemies):                                                            # Class for game's boss
    def __init__(self):
        super().__init__()                                                      # Initializes sprite class
        
        # Classical sprite initialisation : load image, initialize rectangle, positions...
        self.image = image.load("./assets/Boss.png")
        self.image = transform.scale(self.image, (500, 500))                    # Resizes image sprite to correct size
        self.image = transform.rotate(self.image, -90)                          # Rotates the enemy to face the left side of the screen
        self.hp = 100                                                           # + sets new common properties for enemies of that type such as constant hp stat
        self.type = "Boss"                                                      # Declares type of enemy for it to be identifiable to the game
        self.damage = 5                                                         # Damage inflicted by the enemy
        self.rect = self.image.get_rect()                                       # Creates hit box
        self.rect = Rect.inflate(self.rect, -15, -15)                           # Tries to redimensionate the hitbox.
        self.rect.x = 0
        self.rect.y = 0                                                         # Sets up starting position of the ship by setting up the enemy's coordinate
        self.reached_border = 0
        self.velocity = 2
        self.cadence = 8
        self.score = 1000                                                       # For each enemy, the number of points given when they are killed

    def displacement(self):
        self.rect.x += self.velocity

    def detection(self, player):
        if self.time >= 100 / self.cadence:
            self.time = 0
            return self.rect.x, randint(30, 450), -90, self.damage              # Will make spawn a bullet at a random height.
        
        else:                                                                   # If the timer isn't at the right value, increments it and returns a tuple of incorrect values.
            self.time += 1
            return -1, -1, 0, 0
