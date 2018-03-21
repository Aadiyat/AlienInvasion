import pygame
from pygame.sprite import Sprite

class Missile(Sprite):
    """Represent the missile"""
    def __init__(self,  ai_settings, screen, ship):
        """Initialise the missile's attributes."""
        super().__init__()
        # Create a rect for the missile
        self.screen = screen
        self.rect = pygame.Rect(0,0, ai_settings.missile_width, 
            ai_settings.missile_height)
        # Place the missile so that it appears out of centre and top of the 
        # ship
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        
        # Create a variable that can hold decimal value for y positon
        self.y = float(self.rect.y)
        
        self.colour = ai_settings.missile_colour
        # The missile should be slower that bullets to compensate for the 
        # greater destructive power.
        
        self.missile_speed = ai_settings.missile_speed_factor
        
    def update(self):
        """Update the position of the missile."""
        self.y -= self.missile_speed
        self.rect.y = self.y
    
    def draw_missile(self):
        """Draw the missile on the screen."""
        pygame.draw.rect(self.screen, self.colour, self.rect)

class Explosion(Sprite):
    """Represent the explosion from a super bullet."""
    def __init__(self, ai_settings, screen, explosion_centerx, explosion_centery):
        """Initialise explosion attributes."""
        super().__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, ai_settings.explosion_width,
            ai_settings.explosion_height)
        self.rect.centerx = explosion_centerx
        self.rect.centery = explosion_centery
        
        self.colour = ai_settings.explosion_colour
    
    def draw_explosion(self):
        """Draw explosion onto screen."""
        pygame.draw.rect(self.screen, self.colour, self.rect)
        
