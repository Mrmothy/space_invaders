import pygame, random


#Initialize pygame
pygame.init()

#Set display surface
WINDOW_WIDTH = 1200
WINDWO_HEIGHT = 700
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDWO_HEIGHT))
pygame.display.set_caption("Space invaders")

#Set FPS and clock
FPS = 60
clock =  pygame.time.Clock()

#TODO Classes
#*Define classes
class Game:
    """A class to help control and update game play"""
    
    def __init__(self):
        """Initialze the game"""
        pass

    def update(self):
        """Update the game"""
        pass

    def draw(self):
        """Draw the HUD and other information to display"""
        pass

    def shift_aliens(self):
        """Shift a wave of aliens down the screen and reverse the direction"""
        pass

    def check_collision(self):
        """Check for collisions"""
        pass
    
    def check_round_competition(self):
        """Check to see if a player has completed a single round"""
        pass

    def start_new_round(self):
        """Start a new round"""
        pass

    def check_game_status(self):
        """Check to see the status of the game and how the player died"""
        pass

    def pause_game(self):
        """Pause the game"""
        pass

    def reset_game(self):
        """Rest the game"""
        pass

class Player(pygame.sprite.Sprite):
    """A class to model a space ship the user can control"""

    def __init__(self):
        """Initialize the player"""
        pass

    def update(self):
        """Update the player"""
        pass

    def fire(self):
        """Fire a bullet"""
        pass

    def reset(self):
        """Reset the players position"""
        pass

class Alien(pygame.sprite.Sprite):
    """A class to model an enemy Alien"""

    def __init__(self):
        """Initialize the alien"""
        pass

    def update(self):
        """Update the alien"""
        pass

    def fire(self):
        """Fire a bullet"""
        pass

    def reset(self):
        """Reset the aliens position"""
        pass

class PlayerBullet(pygame.sprite.Sprite):
    """A class to model a bullet fired by the player"""

    def __init__(self):
        """Initialize the bullet"""
        pass

    def update(self):
        """Update the bullet"""
        pass

class AlienBullet(pygame.sprite.Sprite):
    """A class to model a bullet fired by the alien"""

    def __init__(self):
        """Initialize the bullet"""
        pass

    def update(self):
        """Update the bullet"""
        pass


#Main game loop
running = True
while running:
    #Check to see if player exits game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Update display and tick clock
    pygame.display.update()
    clock.tick(FPS)


#End game loop
pygame.quit()