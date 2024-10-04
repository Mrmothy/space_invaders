import pygame, random
from os.path import join


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

    def __init__(self, bullet_group):
        """Initialize the player"""
        super().__init__()
        #Set the player image
        self.image = pygame.image.load(join("Assets","player_ship.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH / 2
        self.rect.bottom = WINDWO_HEIGHT

        #Set Player Values
        self.lives = 5
        self.velocity = 8

        self.bullet_group = bullet_group

        #Set Shoot Sound
        self.shoot_sound = pygame.mixer.Sound(join("Assets", "player_fire.wav"))
        self.shoot_sound.set_volume(.25)

    def update(self):
        """Update the player"""
        keys = pygame.key.get_pressed()

        #Move the player within the bounds of the screen
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.velocity
        

    def fire(self):
        """Fire a bullet"""
        #Restrict the number of bullets at a time. 

        if len(self.bullet_group) < 3:
            self.shoot_sound.play()            
            PlayerBullet(self.rect.centerx, self.rect.top, self.bullet_group)


    def reset(self):
        """Reset the players position"""
        self.rect.centerx = WINDOW_WIDTH / 2

class Alien(pygame.sprite.Sprite):
    """A class to model an enemy Alien"""

    def __init__(self, x, y, velocity, bullet_group):
        """Initialize the alien"""
        super().__init__()
        #Load image
        self.image = pygame.image.load(join("Assets", "alien.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        #Starting positions
        self.starting_x = x
        self.starting_y = y

        self.direction = 1
        self.velocity = velocity

        self.bullet_group = bullet_group

        self.shoot_sound = pygame.mixer.Sound(join("Assets", 'alien_fire.wav'))
        self.shoot_sound.set_volume(.25)
        
    def update(self):
        """Update the alien"""
        self.rect.x += self.direction * self.velocity

        #Randomly fire a bullet
        if random.randint(0, 1000) > 999 and len(self.bullet_group) < 3:
            self.shoot_sound.play()
            self.fire()


    def fire(self):
        """Fire a bullet"""
        pass

    def reset(self):
        """Reset the aliens position"""
        self.rect.topleft = (self.starting_x, self.starting_y)
        self.direction = 1

class PlayerBullet(pygame.sprite.Sprite):
    """A class to model a bullet fired by the player"""

    def __init__(self, x, y, bullet_group):
        """Initialize the bullet"""
        super().__init__()

        self.image = pygame.image.load(join("Assets", 'green_laser.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.velocity = 10
        bullet_group.add(self)

    def update(self):
        """Update the bullet"""
        self.rect.y -= self.velocity
        
        #If the bullet is off screen kill it
        if self.rect.bottom < 0:
            self.kill()

class AlienBullet(pygame.sprite.Sprite):
    """A class to model a bullet fired by the alien"""

    def __init__(self):
        """Initialize the bullet"""
        pass

    def update(self):
        """Update the bullet"""
        pass

#Creates Bullet groups
my_player_bullet_group = pygame.sprite.Group()
my_alien_bullet_group = pygame.sprite.Group()

#Create a player group
my_player_group = pygame.sprite.Group()
my_player = Player(my_player_bullet_group)
my_player_group.add(my_player)

#Create an Alien Group. Will add alien object via the game's start new round method
my_alien_group = pygame.sprite.Group()

#Create a Game object
my_game = Game()



#Main game loop
running = True
while running:
    #Check to see if player exits game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #The player wants to fire
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.fire()

    #Fill Display
    display_surface.fill((0, 0, 0))

    #Update and display all sprite groups
    my_player_group.update()
    my_player_group.draw(display_surface)

    my_alien_group.update()
    my_alien_group.draw(display_surface)

    my_player_bullet_group.update()
    my_player_bullet_group.draw(display_surface)

    my_alien_bullet_group.update()
    my_alien_bullet_group.draw(display_surface)

    #Update and draw game object
    my_game.update()
    my_game.draw()

    #Update display and tick clock
    pygame.display.update()
    clock.tick(FPS)


#End game loop
pygame.quit()