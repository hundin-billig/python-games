"""
Filename: paddle.py
Author: Lee Dillard
Created: 04/13/2024
Purpose: Define a paddle's methods and attributes
"""

import config
import pygame

class Paddle:
    # constructor method to initialize the paddle's attributes
    def __init__(self, x, y):
        # Initialize the x-coordinate of the paddle
        self.x = x
        # Initialize the y-coordinate of the paddle
        self.y = y
        # Set the width of the paddle
        self.width = 10
        # Set the height of the paddle
        self.height = 100

        # Create a rectangle object for paddles
        self.rect = pygame.Rect(
            self.x,         # x-coordinate of the top-left corner of the rectangle
            self.y,         # y-coordinate of the top-left corner of the rectangle
            self.width,      # Width of the rectangle
            self.height     # Height of the rectangle
        )

        # Set the speed at which the paddle move
        self.speed = 5

#--------------------MOVE PADDLE UP----------------#
    def move_up(self):
        """Move the paddle up"""
        # Check if the y-coordinate of the paddle is greater than 0
        if self.rect.y > 0:
            # Describe the y-coordinate of the paddle by the speed value
            # which moves the paddle upwards
            self.rect.y = self.rect.y - self.speed

#----------------------MOVE PADDLE UP---------------#
    def move_down(self):
        """Move the paddle down"""
        # Check if the y-coordinate of the paddle is less than
        # the screen height minus the paddle's height
        if self.rect.y < config.HEIGHT - self.height:
            # Increase the y-coordinate of the paddle by the speed value
            # which moves the paddle downwards
            self.rect.y = self.rect.y + self.speed

#-----------------MOVE COMPUTER PADDLE----------------#
    def move_computer_paddle(self):
        """Move computer paddle up and down"""
        # If the computer paddle is inside the top and bottom border
        # keep moving in the same direction
        if self.rect.top + self.speed > 20 and \
                self.rect.bottom + self.speed < config.HEIGHT - 20:
            
            # Move computer paddle in the current direction
            self.rect.y += self.speed

        else:
            # Reverse paddle direction multiply by -1
            self.speed = self.speed * -1