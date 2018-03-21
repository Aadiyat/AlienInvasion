"""
Module for the scoreboard
"""

import pygame.font
from pygame.sprite import Group
from ship import Ship
from super_bullet import Missile

class Scoreboard():
    """A class to report scoring information."""
    
    def __init__(self, ai_settings, screen, stats, ship):
        """Initialise scorekeeping attributes."""
        # Get screen rect attributes
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        
        self.ai_settings = ai_settings
        self.stats = stats
        self.ship = ship
        # Font settings for scoring information
        self.text_colour = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        
        # Prepare the initial score image.
        self.prep_score()
        # Prepare high score image
        self.prep_high_score()
        # Prepare game level image
        self.prep_level()
        # Prepare ships left image
        self.prep_ships()
        # Prepare missiles left image
        self.prep_missiles()
        
    def prep_score(self):
        """Turn the score into a rendered image."""
       
        rounded_score = int(round(self.stats.score, -1))
        # Format score when converting int to string.
        score_str = "{:,}".format(rounded_score)
        # Set background colour of image the same as the background colour of 
        # screen.
        self.score_image = self.font.render(score_str, True, self.text_colour,
            self.ai_settings.bg_colour)
        
        # Display score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        # Right side of the score is used for the alignment
        # Scoreboard will grow to the left 
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
    
    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        # Round high score to nearest 10
        high_score = int(round(self.stats.high_score, -1))
        # Format with commas.
        high_score_str = "{:,}".format(high_score)
        # Render image from text.
        self.high_score_image = self.font.render(high_score_str, True, 
            self.text_colour, self.ai_settings.bg_colour)
        
        # Center the high score on the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top
    
    def prep_level(self):
        """Render the level as an image."""
        self.level_image = self.font.render(str(self.stats.level), True, 
            self.text_colour, self.ai_settings.bg_colour)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        # Display the level 10 pixels under the current score.
        self.level_rect.top = self.score_rect.bottom + 10
    
    def prep_ships(self):
        """Show how many ships are left."""
        # Create a group to store ship sprites in.
        self.ships = Group()
        # Run the loop for every ship the player has left.
        for ship_number in range(self.stats.ships_left):
            # Inside the loop create ship and set the ship's x-coordinate so 
            # that ships appear next to each other and there's a 10 pixel margin
            # between the ships and the left hand corner of the screen.
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
            
    def prep_missiles(self):
        """Draw how many missiles are left."""
        self.sb_missiles = Group()
        for missile_number in range(self.stats.missiles_left):
            # Create a missile for each missile left
            missile = Missile(self.ai_settings, self.screen, self.ship)
            # Change coordinates of missiles
            missile.rect.x = 200 + missile_number * (missile.rect.width + 10)
            missile.rect.y = 10
            self.sb_missiles.add(missile)
    
    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        # Draw ships to screen
        self.ships.draw(self.screen)
        # Draw missiles to screen
        for missile in self.sb_missiles.sprites():
            missile.draw_missile()
            
            
            
        
