"""
This is the main game interface.
It initialises the game objects and contains the main loop.
For game logic see game_functions.py
"""

import pygame
from pygame.sprite import Group
from time import sleep

from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    pygame.init()
    ai_settings = Settings()
    
    screen = pygame.display.set_mode((ai_settings.screen_width,
        ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    # Make game button.
    play_button = Button(ai_settings, screen, "Play")
    # Create an instance to store game statistics.
    stats = GameStats(ai_settings) 
        
    # Make a ship.
    ship = Ship(ai_settings, screen)
    # Make a group to store bullets in.
    bullets = Group() 
    # Make groups to store missiles and explosions in.
    missiles = Group()
    explosions = Group()
    
    # Make a group to store aliens in 
    aliens = Group()
    # Create fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)
    
    # Create an instance of the scorboard
    sb = Scoreboard(ai_settings, screen, stats, ship)
    
    # Create a clock to regulate fps
    clock = pygame.time.Clock()
    
    # Check for stored high score.
    gf.get_high_score(stats, sb)
    
    # Main game loop.    
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button,ship,
            bullets, missiles, aliens)        
    
    # Update position of aliens, bullets, missiles and ship only if the game is
    # still active.        
        if stats.game_active:
            ship.update_position()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, bullets,
                aliens) #2
            gf.update_missiles(ai_settings, screen, stats, sb, missiles,
                explosions, aliens)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, bullets,
                aliens)
        
        # Update screen regardless of whether game is active.    
        gf.update_screen(ai_settings, screen, stats, sb, ship, bullets, 
            missiles, aliens, explosions, play_button)
        
        clock.tick(240)
        
run_game()
