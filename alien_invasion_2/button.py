"""
Module for the play button
"""

import pygame.font
# we'll make a rect and then add a label to it.
class Button():
    
    #msg will contain any text given an instance of Button
    def __init__(self, ai_settings, screen, msg):
        """Initialise button attributes."""
        self.screen =  screen
        self.screen_rect = screen.get_rect()
        
        # Set the dimensions an properties of the button.
        self.width, self.height = 200, 50
        self.button_colour = (230, 0, 30)
        self.text_colour = (255, 255, 255)
        # Prepare text for the button. Use default font, 48 font size
        self.font = pygame.font.SysFont(None, 48)
        
        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        
        # prep_msg renders the message as an iamge
        self.prep_msg(msg)
    
    def prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        # turn the text stored in msg into an image.
        # Turn anti-aliasing on,
        self.msg_image = self.font.render(msg, True, self.text_colour,
            self.button_colour)
        # Create a rect of the image and center the image at the button    
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw_button(self):
        # Draw the button and then draw message on top
        self.screen.fill(self.button_colour, self.rect)
        # Draw the message on top by specifying image and rect.
        self.screen.blit(self.msg_image, self.msg_image_rect)
        
