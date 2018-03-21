import sys
import pygame

from bullet import Bullet
from super_bullet import Missile
from super_bullet import Explosion
from alien import Alien
from time import sleep 
from threading import Timer 
import json

def check_events(ai_settings, screen, stats, sb, play_button, ship, bullets,
        missiles, aliens):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # Detect left mouse button clicks.
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get coordinates of click. Activate game if player clicks on the
            # Play button.
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                bullets, aliens, mouse_x, mouse_y)
        # Detect keypresses and releases.
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, sb, ship,
                bullets, missiles, aliens)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def check_keydown_events(event, ai_settings, screen, stats, sb, ship, bullets,
        missiles, aliens):
    """Respond to keypresses."""
    # Control ship movement with right and left arrow keys.
    if event.key == pygame.K_RIGHT: 
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True    
        # Fire bullet only if game is active.
    if event.key == pygame.K_SPACE and stats.game_active:
        # Create a new bullet and add it to the bullets group.
        fire_bullet(ai_settings, screen, ship, bullets)
        # Fire missiles, again only if game is active.
    if event.key == pygame.K_z and stats.game_active:
        fire_missile(ai_settings, screen, stats, sb, ship, missiles)
        # Start the game with the return key.
    if event.key == pygame.K_RETURN:
        check_return_key(ai_settings, screen, stats, sb, ship, bullets,
            missiles, aliens)
    if event.key == pygame.K_ESCAPE:
        sys.exit()

def check_keyup_events(event, ship):        
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False

def fire_missile(ai_settings, screen, stats, sb, ship, missiles):
    """Fire a missile."""
    if stats.missiles_left > 0:
        new_missile = Missile(ai_settings, screen, ship)
        missiles.add(new_missile)
        # Substract from missiles left
        stats.missiles_left -= 1
        # Prep scoreboard to show number of missiles left
        sb.prep_missiles()
        
def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit is not reached."""
    #Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        # A new bullet will be created only if there are fewer bullets on the
        # screen than is allowed.  
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        # Play bullet sound effect when a new bullet is fired.
        new_bullet.bullet_firing.play(loops = 0, maxtime = 1000, fade_ms = 0)

# Starting and restarting game.
def check_return_key(ai_settings, screen, stats, sb, ship, bullets, missiles,
    aliens):
    """Starts the game when player presses Return."""
    if not stats.game_active:
        # Reset alien speed, bullet speed, ship speed
        ai_settings.initialise_dynamic_settings()
        stats.reset_stats()
        # Set game to active
        stats.game_active = True
        
        # Empty any aliens, missiles and bullets from previous game
        aliens.empty()
        bullets.empty()
        missiles.empty()
        
        # Reset scoreboards and level display
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        sb.prep_missiles()
        
        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, bullets,
        aliens, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    # Use collidepoint to check if the mouse click overlaps the regions defined
    # by the play button.
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    # Start game only if the game is inactive. Obviously.
    if button_clicked and not stats.game_active:
        # Reset dynamic game settings, game stats and activate game.
        ai_settings.initialise_dynamic_settings()
        # Hide mouse button once the game begins.
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        
        # Reset scoreboards
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        sb.prep_missiles()
        # Also, empty the list of aliens and bullets, to allow restarting.
        aliens.empty()
        bullets.empty()
        
        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

# Missile functions
def update_missiles(ai_settings, screen, stats, sb, missiles, explosions,
    aliens):
    """
    Update position of missiles, get rid of missiles that have left the 
    screen.
    """
    # Update missile position
    missiles.update()
    # Delete missiles that are no longer in the screen.
    for missile in missiles.copy():
        if missile.rect.bottom <= 0:
            missiles.remove(missile)
    
    check_missile_alien_collisions(ai_settings, screen, missiles, explosions,
        aliens)
    
    if explosions:
        check_explosion_alien_collisions(ai_settings, stats, sb, explosions,
            aliens)
            
def check_missile_alien_collisions(ai_settings, screen, missiles, explosions,
    aliens):
    """
    Check for collisions between missiles and aliens and create an explosion
    centered at the collision.
    """
    # Detect collisions.
    collisions = pygame.sprite.groupcollide(missiles, aliens, True, False)
    if collisions:
        for missile in collisions.keys():
            # Get explosion coordinates.
            explosion_centerx = missile.rect.centerx
            explosion_centery = missile.rect.top
            # Create explosion
            explosion = Explosion(ai_settings, screen, explosion_centerx,
                explosion_centery)
            explosions.add(explosion)
            
            # Set a timer to remove the explosion right after it's made.
            t = Timer(0.5, delete_explosions, args =[explosions, explosion])
            t.start() 
            
def delete_explosions(explosions, explosion):
    """Remove explosion after some time has passed."""
    explosions.remove(explosion)
        
def check_explosion_alien_collisions(ai_settings, stats, sb, explosions,
    aliens):
    """Detect collision between explosions and aliens."""
    collisions = pygame.sprite.groupcollide(explosions, aliens, False, True)
    # Pass collisions dictionary to update_current_score.
    update_current_score(collisions, ai_settings, stats, sb) 

# Bullet functions                
def update_bullets(ai_settings, screen, stats, sb, ship, bullets, aliens):
    """Update position of bullets and get rid of old bullets."""
    
    #Update bullet position.
    bullets.update()
    
    #Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        # make a copy of bullets group
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    # Check if any bullets have hit aliens as soon as possible so check 
    # immediately after updating bullets. 
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
        bullets, aliens)
    
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
        bullets, aliens):
    """Respond to bullet-alien collisions."""
    # Detect collisions
    # Delete any aliens hit.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    # Update score and play explosion sound for aliens hit.
    if collisions:
        update_current_score(collisions, ai_settings, stats, sb)
        play_alien_explosion(collisions)
    
    # Progress to next level when all aliens are destroyed.
    if len(aliens) == 0:
        start_new_level(ai_settings, screen, stats, sb, ship, bullets, aliens)

def start_new_level(ai_settings, screen, stats, sb, ship, bullets, aliens):
    """Start a new level once all aliens are destroyed."""    
    # Destroy all bullets and create a new fleet.
    bullets.empty()
    # Once all aliens are destroyed, chnage level and increase the speed of
    # the game.
    ai_settings.increase_speed()
    stats.level += 1
    sb.prep_level()
    # Then create a new fleet with aliens that move faster.
    create_fleet(ai_settings, screen, ship, aliens)

def update_current_score(collisions, ai_settings, stats, sb):
    """Update current game score whenever an alien is hit."""
    # Loop through all aliens that were hit. Award points for each alien.
    for aliens in collisions.values():
        stats.score += ai_settings.alien_points * len(aliens)
        sb.prep_score()
    # Check high score each time an alien is hit.
    check_high_score(stats, sb)

def play_alien_explosion(collisions):
    """Plays alien explosion sound track"""
    for aliens in collisions.values():
        for alien in aliens:
            alien.alien_explosion.play(loops = 0, maxtime = 1000, fade_ms = 0)

# Aliean functions.
def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height - 
                            (3 * alien_height) - ship_height)
    number_rows = int(available_space_y/(2*alien_height))
    return number_rows

def get_number_aliens_x(ai_settings, alien_width):
    """Returns a value for the number of aliens that will fit in a row."""
    available_space_x = ai_settings.screen_width - 2* alien_width
    # Get integer value of number of aliens since we don't want partial aliens
    number_alien_x = int(available_space_x/(2*alien_width))
    
    return number_alien_x
    
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it."""
    # Create an instance of Alien
    alien = Alien(ai_settings, screen)
    # Get width of alien from rect attributes.
    alien_width = alien.rect.width
    # Maintain a gap equal to the width of one alien between aliens.
    alien.x = alien_width + (2 * alien_width * alien_number)
    alien.rect.x = alien.x
    
    # The y_coordinate of the alien will depend on which row it's in
    # Similar calculation as for alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height  * row_number
    
    # Add alien to aliens group
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):    
    
    # Create an instance of alien to get alien.rect.width
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    # Call functions to get number of aliens in a row and number of rows.
    number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
        alien.rect.height)
    # Range counts from 0 to number_aliens_x and creates an alien for each 
    # number in the range. Each row is repeated for number of rows.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)
        
def check_fleet_edge(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    # Check if alien is at an edge for every alien in the fleet.
    # If it is change the direction for the whole fleet.
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    # Drop the whole fleet by dropping each alien in the fleet.
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    # Change direction of the fleet.
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, stats, screen, sb, ship, bullets, aliens):
    """
    Check if the fleet is at an edge, 
    and then update the position of all aliens in the fleet.
    """
    
    check_fleet_edge(ai_settings, aliens)
    aliens.update()
    
    # Check if any aliens hit the bottom of the screen.
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, bullets, aliens)
    
    # Check for collisions between alien and ship. 
    # Check for alien ship collisions immediately after updating aliens
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, bullets, aliens)
    
def ship_hit(ai_settings, stats, screen, sb, ship, bullets, aliens):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
    # Reduces number of ships left by one.
        stats.ships_left -= 1
        # Update scoreboard.
        sb.prep_ships()
    
    # Empty the list of bullets and aliens.
        aliens.empty()
        bullets.empty()
    
    # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
    # Don't create a new ship, simply center the one that's already on screen
    
    # Pause.
        sleep(1)
    
    # If no more ships are left end the game.
    else:
        stats.game_active = False
        # Write new high score once game ends.
        store_high_score(stats)
        # Set the mouse to be visible once the game ends.
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, sb, ship, bullets, aliens):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            # If one alien hits the bottom it doesn't matter if any else do, so
            # break the loop once one alien hits.
            ship_hit(ai_settings, stats, screen, sb, ship, bullets, aliens)
            break

# Score functions.
def check_high_score(stats, sb):
    """Check if there's a new high score."""
    if stats.score > stats.high_score:
        # If the current score is greater than the stored high score, the 
        # high score is set to the current score.
        stats.high_score = stats.score
        sb.prep_high_score()        

def store_high_score(stats):
    """Writes the high score to json file."""
    file_path = 'high_score.json'
    high_score = stats.high_score
    with open(file_path, 'w') as f_obj:
        json.dump(high_score, f_obj)

def read_high_score():
    """Reads high score from file."""
    file_path = 'high_score.json'
    try:
        with open(file_path, 'r') as f_obj:
            high_score = json.load(f_obj)
    except FileNotFoundError:
        return None
    else:
        return high_score
        
def get_high_score(stats, sb):
    """Sets high score in game stats to the value stored."""
    high_score = read_high_score()
    
    if high_score:
        # If there is an existing all time high score stored
        # Set the high score to the value stored
        stats.high_score = high_score
        # Prep the scoreboard to display stored high score.
        sb.prep_high_score()
        
# Screen function.
def update_screen(ai_settings, screen, stats, sb, ship, bullets, missiles,
    aliens, explosions, play_button):
    """Update images on the screen and flip to the new screen."""
    
    #Redraw the screen during each pass through the loop."""
    screen.fill(ai_settings.bg_colour)
    
    #Redraw all the bullets behind the ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    
    for missile in missiles.sprites():
        missile.draw_missile()
    
    for explosion in explosions.sprites():
        explosion.draw_explosion()
    #Draw the ship
    ship.blitme()
    
    # Draw the aliens 
    aliens.draw(screen)
    
    # Draw the scoreboard
    sb.show_score()
    
    # Draw play button on top of everything and only if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()
    
    #Make the most recently drawn screen visible
    pygame.display.flip()
