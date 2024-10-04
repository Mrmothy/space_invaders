import pygame, random
from os.path import join


#Initialize pygame
pygame.init()

#Set display surface
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space invaders")

#Set FPS and clock
FPS = 60
clock =  pygame.time.Clock()

#TODO Classes
#*Define classes
class Game:
    """A class to help control and update game play"""
    
    def __init__(self, player, alien_group, player_bullet_group, alien_bullet_group):
        """Initialze the game"""
        #Set game values
        self.round_number = 1
        self.score = 0 

        self.player = player
        self.alien_group = alien_group
        self. player_bullet_group = player_bullet_group
        self.alien_bullet_group = alien_bullet_group

        #Set sounds and music
        self.new_round_sound = pygame.mixer.Sound(join("Assets", "new_round.wav"))
        self.new_round_sound.set_volume(.35)
        self.breach_sound = pygame.mixer.Sound(join("Assets", "breach.wav"))
        self.breach_sound.set_volume(.25)
        self.alien_hit_sound = pygame.mixer.Sound(join("Assets", "player_hit.wav"))
        self.alien_hit_sound.set_volume(.25)

        #Set font
        self.font = pygame.font.Font(join("Assets", "Facon.ttf"), 32)
        

    def update(self):
        """Update the game"""
        self.shift_aliens()
        self.check_collision()
        self.check_round_competition()

    def draw(self):
        """Draw the HUD and other information to display"""
        #Set Colors
        WHITE = (255, 255, 255)

        #Set Test
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.centerx = WINDOW_WIDTH / 2 
        score_rect.top = 10

        round_text = self.font.render(f"Round: {self.round_number}", True, WHITE)
        round_rect = round_text.get_rect()
        round_rect.topleft = (20, 10)

        lives_text = self.font.render(f"Lives: {self.player.lives}", True, WHITE)
        lives_rect = lives_text.get_rect()
        lives_rect.topright = (WINDOW_WIDTH - 20, 10) 

        #Blit HUD to Screen
        display_surface.blit(score_text, score_rect)
        display_surface.blit(round_text, round_rect)
        display_surface.blit(lives_text, lives_rect)
        pygame.draw.line(display_surface, WHITE, (0, 50), (WINDOW_WIDTH, 50), 4)
        pygame.draw.line(display_surface, WHITE, (0, WINDOW_HEIGHT - 100), (WINDOW_WIDTH, WINDOW_HEIGHT - 100), 4)

    def shift_aliens(self):
        """Shift a wave of aliens down the screen and reverse the direction"""
        #Determin if alien group has hit edge
        shift = False
        for alien in (self.alien_group.sprites()):
            if alien.rect.left < 0 or alien.rect.right > WINDOW_WIDTH:
                shift = True
        
        #Shift every alien down, change direction, and check for a breach
        if shift:
            breach = False
            for alien in (self.alien_group.sprites()):
                #Shift down
                alien.rect.y += 10 * self.round_number
                
                #Reverse the direction and move alien off edge so shift does't trigger
                alien.direction = -1 * alien.direction
                alien.rect.x += alien.direction * alien.velocity


                #Check if an alien reached the ship
                if alien.rect.bottom >= WINDOW_HEIGHT - 100:
                    breach = True
            
            #Aliens reached the line
            if breach:
                self.breach_sound.play()
                self.player.lives -= 1
                self.check_game_status()



    def check_collision(self):
        """Check for collisions"""
        pass
    
    def check_round_competition(self):
        """Check to see if a player has completed a single round"""
        pass

    def start_new_round(self):
        """Start a new round"""
        #Create a grid of aliens 11 columns and 5 rows
        for i in range(11):
            for j in range(5):
                alien = Alien(64 + i*64, 64 + j*64, self.round_number, self.alien_bullet_group) 
                self.alien_group.add(alien)
        
        #Pause the game and prompt user to start
        self.new_round_sound.play()
        self.pause_game()

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
        self.rect.bottom = WINDOW_HEIGHT

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
        AlienBullet(self.rect.centerx, self.rect.bottom, self.bullet_group)

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

    def __init__(self, x, y, bullet_group):
        """Initialize the bullet"""
        super().__init__()

        self.image = pygame.image.load(join("Assets", "red_laser.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.velocity = 10

        self.bullet_group = bullet_group
        bullet_group.add(self)


    def update(self):
        """Update the bullet"""
        self.rect.y += self.velocity

        #If the bullet is off screen kill it
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()

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
my_game = Game(my_player, my_alien_group, my_player_bullet_group, my_alien_bullet_group)
my_game.start_new_round()


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