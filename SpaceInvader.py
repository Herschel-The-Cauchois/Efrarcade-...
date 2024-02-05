from pygame import *
from pygame.locals import *

"""
SPACE INVADER
"""

#INFOS
"""
  0-|------------ (x)
    |
    |
    |
   (y)
"""

#CONSTANTES
L = 1000
H = 500
is_active = True

#INITIALISATION

init()  

#WINDOW
display.set_caption("Efrarcade")
scene = display.set_mode((L, H))
background = image.load("./assets/test.png")

#PLAYER
perso = image.load("./assets/perso.png").convert()
persoRect = perso.get_rect()
persoRect.x = (L - 150)/2
persoRect.y = H - 100



#PLAYER MOVEMENT

class Player:

    def __innit__(self, x, y, ship):
        self.x = x                              # x and y are the coordinates of the player's ship
        self.y = y                     
        self.ship = ship                        # The ship is the image of the player's spaceship
        

    def move(self):

        l = L - 150
        h = H - 100
        #event = [K_RIGHT, K_LEFT, K_UP, K_DOWN]

        
        for event in event.get():          


            if event.type == KEYDOWN:       # If a key is pressed, the player's ship moves

                if event.key == K_RIGHT:    #Right arrow key
                    if persoRect.x < l:
                        persoRect.x += 1
                    

                if event.key == K_LEFT:     #Left arrow key
                    if persoRect.x > 0:
                        persoRect.x -= 1


                if event.key == K_UP:       #Up arrow key
                    if persoRect.y > 0:
                        persoRect.y -= 1


                if event.key == K_DOWN:     #Down arrow key
                    if persoRect.y < h:
                        persoRect.y += 1

                






#GAME LOOP

while is_active:
    scene.blit(background, (0, 0))
    scene.blit(perso,(persoRect.x, persoRect.y))
    display.flip()                                  # Sets the background and refreshes the window
    
    Player.move(perso)

    for thing in event.get():
        if thing.type == QUIT:                      # If the window is closed, the game stops
            is_active = False
            quit()


