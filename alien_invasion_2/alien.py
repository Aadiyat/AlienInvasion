import pygame
from pygame.sprite import Sprite
import pygame.mixer

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""
    
    # Position of the aliens will be set in relation to the rect attributes of
    # the screen.
    def __init__(self, ai_settings, screen):
        """Initialise the alien and set its starting position."""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        # Load the images and set its rect attribute.
        self.image = pygame.image.load('images\\alien.bmp')
        self.rect = self.image.get_rect()
        
        # Start each nw alien near the top left of the screen.
        # The x coordinate is set be equal to the width of the alien so there
        # is a gap between the top of the screen and the alien equal to the 
        # alien's width. Same for height
        self.rect.x = self.rect.width 
        self.rect.y = self.rect.height
        
        # Store the alien's exact positon by creating a variable that can hold
        # decimal values.
        self.x = float(self.rect.x)
        
        # Set bullet-alien collision sound.
        self.alien_explosion = pygame.mixer.Sound('sounds\\alien_explode.wav')
        self.alien_explosion.set_volume(0.07)
    
    # Checks if alien has hit edge of screen. If it has it will move down
    def check_edges(self):
        """Return True if alien is at the edge of screen."""
        screen_rect = self.screen.get_rect()
        
        if self.rect.right >= screen_rect.right:
            return True
        
        elif self.rect.left <= 0:
            return True
    
    # method to move the aliens across and down the screen.
    def update(self):
        """Move the alien right  or left."""
        
        # Update alien's x position from speed and direction
        self.x += (self.ai_settings.alien_speed_factor *
            self.ai_settings.fleet_direction)
        # update value of self.rect.x with new value of rect.x
        self.rect.x = self.x        
    
    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)

