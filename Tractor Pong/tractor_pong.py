"""
Filename: tractor_pong.py
Author: Lee Dillard
Created: 04/26/2024
Purpose: Finishing up
"""

# pip install pygame-ce
# Import pygame library
import pygame
import pygame_menu as pm
from random import randint
# Import exit for clean program shutdown
from sys import exit
import config

class TractorPong:
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

        # Create the game surface (window)
        self.surface = pygame.display.set_mode(
            (config.WIDTH, config.HEIGHT)
        )

        # Set window caption
        pygame.display.set_caption("Tractor Pong")

        # Set up computer control clock object to control the speed of the game
        self.clock = pygame.time.Clock()

        self.load_assets()

#------------------------------LOAD ASSETS-------------------------------#
    def load_assets(self):
        # Load png impge, use as program icon
        self.ball_ico = pygame.image.load("./assets/soccer_ball.png").convert_alpha()
        pygame.display.set_icon(self.ball_ico)

        # Load the images from the file system into a variable
        self.ball = pygame.image.load(
            "assets/soccer_ball.png").convert_alpha()
        self.tractor = pygame.image.load(
            "assets/green_tractor.png").convert_alpha()
        
        # Create a rectangle the same size as the image
        # rect is used to set the location of the image
        self.ball_rect = self.ball.get_rect()
        self.tractor_rect = self.tractor.get_rect()

        # Speed in pixels for the tractor
        self.tractor_speed = 4

        # Initial position of the ball rectangle x random, y/top = 10
        self.set_ball_location()
        self.ball_rect.y = 10

        # Ball speed in pixels for x, y
        self.set_ball_direction()
        self.speed_y = 3

        # Initial location of the tractor
        self.tractor_rect.left = config.WIDTH // 2
        self.tractor_rect.top = config.HEIGHT - 90

        # Keep track of score
        self.score = 0

        self.ball_hit = pygame.mixer.Sound("./assets/ball.mp3")
        self.game_over_snd = pygame.mixer.Sound("./assets/tractor_driving_game_over.wav")

        # Set volume for sound effect in range 0.0 to 1.0
        pygame.mixer.Sound.set_volume(self.game_over_snd, .5)

        # Load and play back background music
        pygame.mixer.music.load("./assets/tractor_driving.wav")

        # Set volume to 30%, range from 0.0 (mute) to 1.0 (full volume)
        pygame.mixer.music.set_volume(0.3)

        # Stop any other music from playing
        pygame.mixer.stop()

        # Play background game music in continuous loop from the beginning
        pygame.mixer.music.play(-1)

        # Create font for scoring
        self.font_score = pygame.font.SysFont("Veranda", 20)

        # Only allow these events to be captured
        # This helps optimize the game for slower computers
        pygame.event.set_allowed(
            [
                pygame.QUIT,
                pygame.KEYDOWN,
                pygame.KEYUP,
            ]
        )


#--------------------------------GAME LOOP---------------------------#
    def game_loop(self):
        """Infinite game loop"""
        while True:
            self.check_events()
            self.update_tractor()
            self.update_ball()
            self.check_collision()
            self.draw()

            # Cap game speed to 60 fps
            self.clock.tick(60)

#-------------------------------SET BALL LOCATION--------------------#
    def set_ball_location(self):
        """Set random initial ball direction along the x axis"""
        # Randomly determine the initial x coordinate of the ball
        # along the x-axis (left or right)
        self.ball_rect.x = randint(20, config.WIDTH - 20)

#-------------------------SET BALL DIRECTION---------------------------#
    def set_ball_direction(self):
        """Set random initial ball direction along the x axis"""
        # Randomly determine the initial direction of the ball
        # along the x-axis (left or right)
        ball_direction_x = randint(0, 1)

        # If the randomly chosen direction is 0 (left),
        # set the horizontal speed of the ball to move to the right
        if ball_direction_x == 0:
            self.speed_x = 3

        # If the randomly chosen direction is 1 (right),
        # set the horizontal speed of the ball to move to the left
        else:
            self.speed_x = -3

#--------------------------CHECK EVENTS-----------------------------#
    def check_events(self):
        """Listen for and handle all program events"""
        for event in pygame.event.get():

            # Closing the game causes the QUIT event to be fired
            if event.type == pygame.QUIT:
                # Quit pygame
                pygame.quit()
                # Exit Python
                exit()

#---------------------------------DISPLAY GAME OVER----------------------------------#
    def game_over(self):
        """Display game over on top of the stopped game"""
        # Stop background sound
        pygame.mixer.music.stop()

        # Play game_over music until user clicks a button
        pygame.mixer.Sound.play(self.game_over_snd, loops=-1)

        # Define a meny object for the game over screen
        game_over = pm.Menu(
            title="Game Over",          # Set title menu to "Game Over"
            width=config.WIDTH,         # Set to width of game surface
            height=config.HEIGHT,       # Set to height game surface
            # Set the theme of the menu to an orange color scheme
            theme=pm.themes.THEME_ORANGE
        )

        # Display final score
        game_over.add.label(f"Score: {self.score}")

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

#---------------------CHECK COLLISION-------------------#
    def check_collision(self):
        """Check for collision between to rects"""
        # The ball has to be above the tractor to collide
        # Does the ball collide with the tractor?
        # If so, reverse the ball y direction [1]
        if self.tractor_rect.colliderect(
            self.ball_rect
        ) and self.ball_rect.bottom < self.tractor_rect.top + 4:
            
            # Reverse y direction
            self.speed_y = self.speed_y * -1

            # Randomly change x direction
            direction = randint(0, 1)
            if direction == 0:
                self.speed_x = self.speed_x * -1

            # Increase speed by 10% each time the ball is hit
            self.speed_x = self.speed_x * 1.05
            self.speed_y = self.speed_y * 1.05

            # Increase score by 1
            self.score = self.score + 1
            pygame.mixer.Sound(self.ball_hit)

#---------------------UPDATE TRACTOR-------------------#
    def update_tractor(self):
        # Capture key pressed events into a list
        keys = pygame.key.get_pressed()

        # Check if the left arrow key is pressed
        if keys[pygame.K_LEFT]:
            # Is the tractor to the right of the window
            if self.tractor_rect.left > 0:
                # Move tractor rectangle to the left by subtraction it's speed
                self.tractor_rect.left -= self.tractor_speed

        # Check if the right arrow key is pressed
        if keys[pygame.K_RIGHT]:
            # Is the tractor to the left of the window
            if self.tractor_rect.right < config.WIDTH:
                # Move tractor rectangle to the right by adding it's speed
                self.tractor_rect.right += self.tractor_speed

        # The ESC key will quit the game
        if keys[pygame.K_ESCAPE]:
            # Quit Pygame
            pygame.quit()
            # Exit Python
            exit()

#------------------------UPDATE BALL-----------------------------#
    def update_ball(self):
        # Check for collision with left or right wall
        if self.ball_rect.left <= 0 or self.ball_rect.right >= config.WIDTH:
            # Reverse x direction multiply by -1
            self.speed_x = self.speed_x * -1

        # Check for collision with top or bottom wall
        if self.ball_rect.top <= 0:
            # Reverse y direction multiply by -1
            self.speed_y = self.speed_y * -1

        # Move ball position every frame
        self.ball_rect.x = self.ball_rect.x + self.speed_x
        self.ball_rect.y = self.ball_rect.y + self.speed_y

        # Ball hits bottom, player loses
        if self.ball_rect.bottom > config.HEIGHT:
            self.game_over()

#------------------------------DRAW--------------------------------#
    def draw(self):
        """Draw everything onto the backbuffer"""
        # Fill the display surface to clear the previous screen
        # Comment out this line to see why it is necessary
        self.surface.fill(config.COUGAR_GOLD)

        # Draw the ball on the surface
        self.surface.blit(
            self.ball,             # Image to draw
            self.ball_rect         # Location to draw the image
        )
        
        # Draw the tractor on the backbuffer
        self.surface.blit(
            self.tractor,           # Image to draw
            self.tractor_rect       # Locaton to draw the image
        )

        # Render score before drawing it on the surface
        score_display = self.font_score.render(
            f"{self.score}",        # Score
            True,                   # Antialiasing true
            "black"                 # Font color
        )

        # Draw score on the surface
        self.surface.blit(score_display, (10, 10))

        #-----------COPY BACKBUFFER INTO VIDEO MEMORY--------------#
        # Copy the backbuffer into video memory
        pygame.display.update()

def main():
    # Initialize program object and start game
    tractor_pong = TractorPong()
    tractor_pong.game_loop()

main()



# or self.ball_rect.bottom >= config.HEIGHT