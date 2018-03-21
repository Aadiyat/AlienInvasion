"""
This module stores and updates the game stats, such as high score
"""
class GameStats():
    """Tracks statistics for alien invasion."""
    
    def __init__(self, ai_settings):
        """Initialise statistics."""
        self.ai_settings = ai_settings
        self.reset_stats()
        # Start game in inactive state.
        self.game_active = False
      
        
        self.high_score = 0
    
    def reset_stats(self):
        """Initialise statistics that can change during the game."""
        self.ships_left = self.ai_settings.ship_limit
        # Reset score every time the game restarts.
        self.score = 0
        self.level = 1
        self.missiles_left = self.ai_settings.missiles_allowed

