"""
Filename: flappy_bird.py
Author: Lee Dillard
Created: 04/26/2024
Purpose: Add collisions and End Game screen
"""

# pip install pygame-ce

# Import pygame library
import pygame
# pip install pygame-menu
import pygame_menu as pm
# Import exit for clean program shutdown
from sys import exit
from random import randint
from time import sleep
import config

class FlappyBird:

    def __init__(self):
        # Initialize mixer with larger buffer size for better performance
        pygame.mixer.pre_init(
            44100,          # frequency (Hz)
            16,             # bit depth
            2,              # number of channels, 1 mono, 2 stereo
            4096            # buffer size, larger to optimize music playback
        )

        # Initialize the Pygame engine
        pygame.init()

        # set screen width and height as a tuple
        self.surface = pygame.display.set_mode(
            (config.WIDTH, config.HEIGHT)
        )

        # Set window caption
        pygame.display.set_caption("Flappy Bird")

        # Define the clock object to keep the game running at a set speed
        self.clock = pygame.time.Clock()
        
        self.init_bird()
        self.init_pipes()

        # Load flappy bird png icon
        self.bird_ico = pygame.image.load("./assets/flappy_bird_ico.png").convert_alpha()

        pygame.display.set_icon(self.bird_ico)

        # Load background music file into memory
        pygame.mixer.music.load('./assets/flying_minimal.mp3')

        # Set volume to 30%, range from 0.0 (mute) to 1.0 (full volume)
        pygame.mixer.music.set_volume(0.3)

        # Play in a loop until stopped
        pygame.mixer.music.play(-1)

        self.score = 0
        self.game_over = False
        self.pass_pipe = False
        self.score_font = pygame.font.SysFont("arialblack", 18)
#---------------------------------INIT PIPES------------------------------------#
    def init_pipes(self):
        """Load pipe images, get rect, set initial positions"""
        # Set the gap between the pipes
        self.pipe_gap_size = self.bird_rect.height * 5

        # How many pixels at a time the pipes move
        self.pipe_move = 4

        # Load pipe images
        self.pipe_lower = pygame.image.load(
            "./assets/pipe.png").convert_alpha()
        
        # Rotate upper pipe 180 degrees 
        self.pipe_upper = pygame.transform.rotate(
            pygame.image.load("./assets/pipe.png").convert_alpha(), 180
        )

        # Get rectangles around images for easier manipulation
        self.pipe_lower_rect = self.pipe_lower.get_rect()
        self.pipe_upper_rect = self.pipe_upper.get_rect()

        # Set initial pipe location off screen to right
        self.pipe_lower_rect.left = config.WIDTH
        self.pipe_upper_rect.left = config.WIDTH

        # Initial placement of pipes vertically
        self.pipe_upper_rect.bottom = randint(
            50,                                 # Stay 50 away from top
            config.HEIGHT // 2                  # Upper range of random numbers
        )

        # Set lower pipe vertical location
        self.pipe_lower_rect.top = self.pipe_upper_rect.bottom + self.pipe_gap_size

        # Set score counted to false
        self.score_counted = False

#----------------------------------INIT FLAPPY BIRD-----------------------------#
    def init_bird(self):
        """Load bird image, get rect, set initial position"""
        # Load the bird image into a variable
        self.bird = pygame.image.load(
            "./assets/flappy_bird.png").convert_alpha()

        # Get rectangle around bird for easier game manipulation
        self.bird_rect = self.bird.get_rect()

        # Set bird to initial position
        self.bird_rect.move_ip(
            150,                    # Horizontal (x) position
            config.HEIGHT // 2      # Vertical (y) position
        )

#-----------------------RESET PIPES-------------------------#
    def reset_pipes(self):
        """Reset pipes every time they leave the screen"""
        # Pick a random height for the bottom of the top pipe
        self.pipe_upper_rect.bottom = randint(
            50,                             # Set the maximum random number to 50
            config.HEIGHT // 2              # Set maximum to half the surface height
        )

        # Set lower pipe top to upper pipe bottom plus pipe gap
        self.pipe_lower_rect.top = self.pipe_upper_rect.bottom \
            + self.pipe_gap_size
    
        # Set initial off screen to right
        self.pipe_upper_rect.left = config.WIDTH
        self.pipe_lower_rect.left = config.WIDTH

        # New set of pipes, reset score counter
        self.score_counted = False

#---------------------------DISPLAY SCORE--------------------------#
    def display_score(self):
        """Display the score on the screen"""
        # Create text image for the score display
        text = self.score_font.render(f"Score: {self.score}", True, "white")
        self.surface.blit(
            text,       # Image to display
            [3, 3]      # x, y to display the image
        )

#---------------------------DISPLAY GAME OVER--------------------------#
    def display_game_over(self):
        """Display game over menu using the Pygame Menu library"""
        # Stop background sound
        pygame.mixer.music.stop()

        # Play crash sound
        crash = pygame.mixer.Sound('./assets/crash_short.wav')
        crash.play()
        #crash.set_volume(0.3)

        # Wait 4 seconds while crash plays
        sleep(3)

        # Define a menu object for the game over screen
        game_over = pm.Menu(
            title="Game over",                  # Set the title menu to "Game Over"
            width=config.WIDTH,                 # Set to width of game surface
            height=config.HEIGHT,               # Set to height of game surface
            # Set the theme of the menu to an blue color scheme
            theme=pm.themes.THEME_BLUE
        )

        # Display final score
        game_over.add.label(f"Score: {self.score}")

        # Add label to provide space between buttons
        game_over.add.label("")

        # Add a button to the game over menu for exiting the game
        game_over.add.button(
            title="Play Again?",                # Button text
            action=main                         # Call main() to start over
        )

        # Add label to provide space between buttons
        game_over.add.label("")

        # Add a button to the game over menu for exiting the game
        game_over.add.button(
            title="Exit",                       # Button text
            action=pm.events.EXIT               # Exit the game when clicked
        )

        # Run the main loop of the game over menu on the specified surface
        game_over.mainloop(self.surface)
    
#---------------------------------DETECT COLLISIONS--------------------------------#
    def detect_collision(self):
        # If the bird hits the top or bottom of screen, game over
        if self.bird_rect.bottom > config.HEIGHT\
                or self.bird_rect.top < 0:
            self.display_game_over()

        # The bird is between the pipes
        if self.bird_rect.right > self.pipe_upper_rect.left \
                and self.bird_rect.right < self.pipe_upper_rect.right:
            
            # If the bird runs into a pipe, game over
            if self.bird_rect.top < self.pipe_upper_rect.bottom \
                    or self.bird_rect.bottom > self.pipe_lower_rect.top:
                self.display_game_over()


#---------------------------------CHECK EVENTS--------------------------------#
    def check_events(self):
        """Listen for and handle all program events"""
        # Iterate (loop) through all captured events
        for event in pygame.event.get():

            # Closing the game causes the QUIT event to be fired
            if event.type == pygame.QUIT:
                # Quit pygame
                pygame.quit()
                # Exit Python
                exit()

#-------------------------------GAME LOOP-------------------------------#
    def game_loop(self):
        """Infinite game loop"""
        while True:
            self.check_events()
            self.detect_collision()
            # Simulate gravity by moving the bird down
            # unless the UP key is pressed
            # Reset gravity to 3 each time through the loop
            gravity = 3

            # Get list of keys being pressed
            key_input = pygame.key.get_pressed()
            
            # If up cursor pressed, move up 5 pixels
            if key_input[pygame.K_UP]:
                gravity -= 5

            #------------------INCREASE DIFFICULTY-------------------#

            # Adding difficulty relative to score
            # Increase the speed and decrease the gap of blocks
            if 5 <= self.score < 10:
                self.pipe_move = 5
                self.pipe_gap_size = self.bird_rect.height * 4

            elif 10 <= self.score < 20:
                self.pipe_move = 7
                self.pipe_gap_size = self.bird_rect.height * 3.5

            #------------------SCORING-------------------#            
            # If the bird makes it past the pipes, increase score
            if self.bird_rect.left > self.pipe_upper_rect.right \
                    and not self.score_counted:
                
                # Increase score
                self.score += 1

                # Track whether the current set of pipes have had a score
                self.score_counted = True


#------------------MOVE SPRITES--------------------#
            # Move the bird by adding gravity value to y location
            self.bird_rect.y = self.bird_rect.y + gravity

            # Move pipe images from right to left
            self.pipe_upper_rect.left = self.pipe_upper_rect.left - self.pipe_move
            self.pipe_lower_rect.left = self.pipe_lower_rect.left - self.pipe_move

            # If the pipes are off the screen, reset them
            if self.pipe_upper_rect.right < 0:
                self.reset_pipes()

            #--------------------DRAW ON BACKBUFFER-----------------------#
            # Draw everything in the backbuffer first
            # Fill the display surface with blue
            self.surface.fill(config.SKY_BLUE)
           
            # Draw bird to the backbuffer
            self.surface.blit(
                self.bird,       # Source image
                self.bird_rect   # Destination location of image
            )

            # Draw pipes to the backbuffer
            self.surface.blit(
                self.pipe_lower,                # Source image
                self.pipe_lower_rect            # Destination location of image
            )
            self.surface.blit(
                self.pipe_upper,                # Source image
                self.pipe_upper_rect            # Destination location of image
            )

            #-------------------------UPDATE SURFACE----------------------#
            # From back buffer, update pygame display to reflect any changes
            pygame.display.update()

            # Cap game speed to 60 fps
            self.clock.tick(60)


def main():
    # Create flappy bird program object
    flappy_bird = FlappyBird()
    # Start infinite game loop
    flappy_bird.game_loop()

# Start the program
main()