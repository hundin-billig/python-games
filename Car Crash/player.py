"""
Filename: player.py
Author: Lee Dillard
Created: 04/13/2024
Purpose: All logic for the player's car is in this class
"""

 # Import pygame library
import pygame
import config

class Player(pygame.sprite.Sprite):
    """Define the player class and methods"""

#---------------------------------------INITIALIZE PLAYER OBJECT---------------------------------#
    def __init__(self):
        """Construct a player object from Sprite class"""

        # Call the constuctor of the superclass (pygame.sprite.Sprite)
        super().__init__()

        # Load player car image from file into a variable
        self.image = pygame.image.load(
            "./assets/player.png"
        ).convert_alpha()

        # Get the rectangle area of the player car surface
        self.rect = self.image.get_rect()

        # Player initial position
        # Place car in the center of the x axis
        # Divide the width of the screen by 2,
        # Subtract half the width of the car rect to center car
        x = config.WIDTH // 2 - self.rect.width // 2

        # Subtract 120 from screen height to move car up
        # almost off the screen
        y = config.HEIGHT - 120

        # Move player to initial position
        self.rect.move_ip((x, y))

    #--------------------UPDATE-----------------#
    def update(self):
        """Update the car's position"""
        # Called each time through the game loop
        # Read the keyboard to see if any keys pressed
        pressedKeys = pygame.key.get_pressed()

        # Keep the player on the screen
        # The sprite can't move past the left edge of the surface
        if self.rect.left > 0:

            # Left arrow key pressed, move left 5 pixels at a time
            if pressedKeys[pygame.K_LEFT]:
                self.rect.move_ip(-5, 0)

        # The sprite can't move past the right edge of the surface
        if self.rect.right < config.WIDTH:

            # Right arrow key pressed, move right 5 pixels at a time
            if pressedKeys[pygame.K_RIGHT]:
                self.rect.move_ip(5, 0)
