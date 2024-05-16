"""
Filename: car_crash.py
Author: Lee Dillard
Created: 04/26/2024
Purpose: Add collisions
"""

# pip install pygame-ce
# pip install pygame-menu
# Import pygame and sys modules
import pygame
import pygame_menu as pm
from sys import exit
from time import sleep
#import assets
import config
# Import the player class
import player
import enemy
#import os

class CarCrash:
    def __init__(self):

        # Initialize mixer with larger buffer size for better performance
        pygame.mixer.pre_init(
            44100,          # frequency (Hz)
            16,             # bit depth
            2,              # number of channels, 1 mono, 2 stereo
            4096            # buffer size, larger to optimize music playback
        )

        # Initialze the pygame engine
        pygame.init()

        # Create the game surface (window)
        self.surface = pygame.display.set_mode(
            (config.WIDTH, config.HEIGHT)
        )

        # Set window caption
        pygame.display.set_caption("Car Crash")

        # Load background image from file into an image variable
        self.background = pygame.image.load(
            './assets/street.png').convert_alpha()
        
        # Set up computer control clock object to control the speed of the game
        self.clock = pygame.time.Clock()

        # Optimize game by only allowing these events to be captured
        pygame.event.set_allowed(
            [pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP]
        )

        # Set window icon
        window_icon = pygame.image.load("./assets/car.ico").convert_alpha()
        pygame.display.set_icon(window_icon)

        # Create the player and enemy sprites
        self.create_sprites()

        # Create system font object for score
        self.font_small = pygame.font.SysFont("arialblack", 20)

        # Load sound file into memory
        pygame.mixer.music.load('./assets/background_music.wav')

        # Set volume to 30%, range from 0.0 (mute) to 1.0 (full volume)
        pygame.mixer.music.set_volume(0.3)

        # Play in a loop until stopped
        pygame.mixer.music.play(-1)

#------------------------------------CREATE SPRITES--------------------------------------#
    def create_sprites(self):
        # Create a Player sprite
        self.player_sprite = player.Player()
        self.enemy_sprite = enemy.Enemy()

        # Create Sprites Group, add Sprites to Group
        # a separate enemies group is created,
        # to allow for more enemy Sprites later if needed
        self.enemies = pygame.sprite.Group()
        self.enemies.add(self.enemy_sprite)
 
        # This group includes all sprites
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player_sprite)
        self.all_sprites.add(self.enemy_sprite)

        # Even though we only have one player, we have to add it to a group
        # Only a group has a draw and update method
        #self.all_sprites.add(player_sprite)

#-----------------------------------CHECK EVENTS----------------------------------------#
    def check_events(self):
        """Listen for and handle all window events"""
        # Iterate (loop) through all captured events
        for event in pygame.event.get():

            # Closing the game causes the QUIT event to be fired
            if event.type == pygame.QUIT:
                # Quit pygame
                pygame.quit()
                # Exit Python
                exit()

#---------------------------------DISPLAY GAME OVER----------------------------------#
    def display_game_over(self):
        """Display game over on top of the stopped game"""
        # Stop background sound
        pygame.mixer.music.stop()

        # Play crash sound
        crash = pygame.mixer.Sound('./assets/crash.wav')
        crash.play()
        #crash.set_volume(0.5)

        # Wait 3 second
        sleep(3)

        # Define a meny object for the game over screen
        game_over = pm.Menu(
            title="Game Over",          # Set title menu to "Game Over"
            width=config.WIDTH,         # Set to width of game surface
            height=config.HEIGHT,       # Set to height game surface
            # Set the theme of the menu to an orange color scheme
            theme=pm.themes.THEME_ORANGE
        )

        # Display final score
        game_over.add.label(f"Score: {self.enemy_sprite.score}")

        # Add label to provide space between buttons
        game_over.add.label("")

        # Add a button to the game over menu for exiting the game
        game_over.add.button(
            title="Play Again?",            # Button text
            action=main                     # Call main() to start over
        )

        # Add a label to provide space between buttons
        game_over.add.label("")

        # Add a button to the game over menu for exiting the game
        game_over.add.button(
            title="Exit",            # Button text
            action=pm.events.EXIT    # Exit the game when clicked
        )

        # Run the main loop of the game over menu on the specified surface
        game_over.mainloop(self.surface)

#---------------------------------CHECK COLLISIONS----------------------------------#
    def check_collision(self):
        # If a collision occurs bewtween player and enemy
        if pygame.sprite.spritecollideany(
            self.player_sprite,
            self.enemies
        ):
            self.display_game_over()

#---------------------------------RUN GAME-----------------------------------------------#
    def game_loop(self):
        """Infinite Game Loop"""
        while True:
            self.check_events()
            self.check_collision()

            #----------------DRAW ON BACKBUFFER------------------#
            # Fill in the surface with the background image loaded earlier
            self.surface.blit(self.background, (0, 0))

            #-----------------UPDATE AND DRAW SPRITES-----------------#
            # Run the update method on all sprites
            self.all_sprites.update()

            # Draw all sprites on the surface
            self.all_sprites.draw(self.surface)

            # Render score before drawing on the surface
            self.score = self.font_small.render(
                str(self.enemy_sprite.score), True, config.BLACK
            )

            # Draw score on the surface
            self.surface.blit(self.score, (10, 10))

            #----------------UPDATE SURFACE----------------------------#
            # From backbuffer, update Pygame display to reflect changes
            pygame.display.update()

            # Cap game speed at 60 frames per second
            self.clock.tick(60)

def main():
    # Create game instance
    car_crash = CarCrash()
    # Start the game
    car_crash.game_loop()

main()