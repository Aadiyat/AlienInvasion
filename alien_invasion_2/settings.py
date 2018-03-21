class Settings():
    """A class to store all settings for Alien Invasion."""
    
    def __init__(self):
        """Initialise the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = (230, 230, 230)
        
        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 12
        self.bullet_colour = (60, 60, 60)
        self.bullets_allowed = 3
        # Limit the number of bullets the player can have on the screen at a
        # time to encourage accuracy.
    
    # Alien settings
        self.fleet_drop_speed = 10
    
    # Missile settings.
        self.missile_width = 6
        self.missile_height = 18
        self.missile_colour = (30, 30, 30)
        self.missile_speed_factor = 3.5
        self.missiles_allowed = 3
    
    # Explosion settings.
        self.explosion_width = 200
        self.explosion_height = 200
        self.explosion_colour = (230, 130, 0)
        
    # How quickly the game speeds up.    
        self.speedup_scale = 1.1
    
    # how quickly the points values of aliens increases
        self.score_scale = 1.5
        
        self.initialise_dynamic_settings()
    
    def initialise_dynamic_settings(self):
        """Intialise settings that change thorughout the game."""
        self.ship_speed_factor = 5
        self.bullet_speed_factor = 8
        self.alien_speed_factor = 4        
        
        self.alien_points = 50
        
        # Fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        # aliens always move to the right at the start of a new game.
    
        # Increase the speed of the game by multiplying these settings by the
        # speed up scale.
        
    def increase_speed(self):
        """Increase speed settings and alien points value."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        
        # use int function to increase score by whole points.
        self.alien_points = int(self.alien_points * self.score_scale)
        
        
