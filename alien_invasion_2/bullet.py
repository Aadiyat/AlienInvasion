"""
This module has the code for the bullets that the ship can fire.
The ship class inherits from sprite so tha all the bullets can be handled
together.
The class has methods to draw the bullets on the screen and update their 
positions.
"""

import pygame
from pygame.sprite import Sprite
import pygame.mixer

class Bullet(Sprite):
    """A class to maange bullets fired from the ship."""
    
    def __init__(self, ai_settings, screen, ship):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = screen
        
        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
            ai_settings.bullet_height) 
        # Place the center of the bullet at the center of the ship.    
        self.rect.centerx = ship.rect.centerx 
        # Place the bullet at the ship's top.
        self.rect.top = ship.rect.top 
        
        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)
        
        self.colour = ai_settings.bullet_colour
        self.speed_factor = ai_settings.bullet_speed_factor
        
        # Set bullet firing sound
        # Load sound track
        self.bullet_firing = pygame.mixer.Sound('sounds\\bullet_firing.wav')
        # Set volume
        self.bullet_firing.set_volume(0.15)

    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.y -= self.speed_factor 
        # Update the rect position
        self.rect.y = self.y 
    
    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.colour, self.rect) #3
