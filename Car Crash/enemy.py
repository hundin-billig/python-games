"""
Filename: enemy.py
Author: Lee Dillard
Created: 04/26/2024
Purpose: All logic for the enemy's car is in this class
"""

 # Import pygame library
import pygame
from random import randint
import config

class Enemy(pygame.sprite.Sprite):
    """Define the enemy class and methods"""

#---------------------------------------INITIALIZE ENEMY SPRITE---------------------------------#
    def __init__(self):
        """Construct a enemy object from Sprite class"""

        # Call the constuctor of the superclass (pygame.sprite.Sprite)
        super().__init__()

        self.score = 0

        # Set the initial speed of enemy car
        self.speed = config.SPEED

        # Load enemy car image from file into a variable
        self.image = pygame.image.load(
            "./assets/enemy.png").convert_alpha()

        # Get the rectangle area of the enemy car surface
        self.rect = self.image.get_rect()

        # Get a random location 40 pixels away from the left and right.
        x = randint(40, config.WIDTH - 40)

        # y is -120, the car starts above the program window
        y = -120

        # Move enemy to initial position
        self.rect.move_ip((x, y))

    #--------------------UPDATE-----------------#
    def update(self):
        """Update the car's position"""
        # Move the sprite down SPEED pixels at a time
        self.rect.move_ip(0, self.speed)

        # When the top of the sprite reaches the bottom of the surface
        if (self.rect.top > config.HEIGHT):

            # Get a random location 40 pixels away from the left and right
            x = randint(40, config.WIDTH -40)

            # Move car above program window
            y = -120

            # Move car to beginning position
            self.rect.center = (x, y)

            # Increase speed each time the enemy car starts at the top
            self.speed += config.SPEED_INCREASE

            # Increment score every tiime the player dodges an oncoming car
            self.score += 1