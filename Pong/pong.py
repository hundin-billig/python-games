"""
Filename: pong.py
Author: Lee Dillard
Created: 04/26/2024
Purpose: Add sound and game over
"""

# pip install pygame-ce

# Import pygame library
import pygame
#pip install pygame-ce
import pygame_menu as pm
# Import exit for clean program shutdown
from sys import exit
from random import randint
random.seed()
from time import sleep
import config
from paddle import Paddle

class Pong:

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

        # Set screen width and height as a tuple
        self.surface = pygame.display.set_mode(
            (config.WIDTH, config.HEIGHT)
        )

        # Set window caption
        pygame.display.set_caption("Pong")

        # Define the clock to keep the game running at a set speed
        self.clock = pygame.time.Clock()

        # Create the ball rectangle object
        self.ball = pygame.Rect(
            config.WIDTH // 2 - config.BALL_RADIUS,             # Set x- coordinate
            config.HEIGHT // 2 - config.BALL_RADIUS,            # Set y- coordinate
            config.BALL_RADIUS,                                 # Set width of ball
            config.BALL_RADIUS                                  # Set height of ball
        )

        self.set_ball_direction()

        # Set up player paddles
        self.player = Paddle(
            5,                              # x coordinate
            (config.HEIGHT - 100) // 2      # y coordinate
        )

        self.computer = Paddle(
            config.WIDTH - 15,              # x coordinate
            (config.HEIGHT - 100) // 2      # y coordinate
        )

        self.computer_speed = 3

        # Load background music file into memory
        pygame.mixer.music.load('./assets/inspiring-and-uplifting-indie-rock.mp3')

        # Set volume to 30%, range from 0.0 (mute) to 1.0 (full volume)
        pygame.mixer.music.set_volume(0.3)

        # Play in a loop until stopped
        pygame.mixer.music.play(-1)

        self.score_font = pygame.font.SysFont("freesansbold", 18)
        self.player_score = 0
        self.computer_score = 0

        # Movement of ping pong ball in pixels
        self.ball_speed_x = 3
        self.ball_speed_y = 3

#---------------------------DISPLAY GAME OVER--------------------------#
    def game_over(self):
        """Display game over menu using the Pygame Menu library"""
        # Stop background sound
        pygame.mixer.music.stop()

        # Play crash sound
        crash = pygame.mixer.Sound('./assets/game_over.wav')
        crash.play()
        #crash.set_volume(0.3)

        # Wait 2 seconds while crash plays
        sleep(2)

        # Define a menu object for the game over screen
        game_over = pm.Menu(
            title="Game over",                  # Set the title menu to "Game Over"
            width=config.WIDTH,                 # Set to width of game surface
            height=config.HEIGHT,               # Set to height of game surface
            # Set the theme of the menu to an blue color scheme
            theme=pm.themes.THEME_SOLARIZED
        )

        # Display final score
        game_over.add.label(f"Player Score: {self.player_score}")
        game_over.add.label(f"Computer Score: {self.computer_score}")

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

#------------------------------SET BALL DIRECTION----------------------#
    def set_ball_direction(self):
        """Set initial ball direction along the x and y axis"""
        # Randomly determine the initial direction of the ball
        # along the x-axis (left or right)
        ball_direction_x = random.randint(0, 1)

        # If the randomly chosen direction is 0 (left),
        # set the horizontal speed of the ball to move to the right
        if ball_direction_x == 0:
            self.ball_speed_x = 3

        # If the randomly chosen direction is 1 (right),
        # set the horizontal speed of the ball to move to the left
        else:
            self.ball_speed_x = -3

        # Randomly determine the initial direction of the ball
        # along the y-axis (up or down)
        ball_direction_y = randint(0, 1)

        # If the randomly chosen direction is 0 (up),
        # set the vertical speed of the ball to move downwards
        if ball_direction_y == 0:
            self.ball_speed_y = 3

        # If the randomly chosen direction is 1 (down),
        # set the vertical speed of the ball to move upwards
        else:
            self.ball_speed_y = -3

#------------------------------CHECK COLLISION----------------------------#
    def check_collision(self):
        """Check for all collisions"""
        # Check for collision with left or right wall
        # Subtract ball radius to bounce off the edge of the ball
        if self.ball.left < 0 or self.ball.right >= config.WIDTH:

            # Ball goes off the table
            self.game_over()

            # Reverse y direction multiply by -1
            self.ball_speed_x = self.ball_speed_x * -1

        # Check for collision with top or bottom wall
        if self.ball.top < 0 or self.ball.bottom >= config.HEIGHT:

            # Reverse y direction multiply by -1
            self.ball_speed_y = self.ball_speed_y * -1

        # Ball collisions with paddles
        if self.ball.colliderect(self.player):
            # Reverse ball direction
            self.ball_speed_x *= -1
            self.player_score += 1

            # Play ball bounce sound
            crash = pygame.mixer.Sound('./assests/hit.wav')
            crash.play()
            crash.set_volume(0.3)

        elif self.ball.colliderect(self.computer):
            # Reverse ball direction
            self.ball_speed_x *= -1
            self.computer_score += 1

            # Play ball bounce sound
            crash = pygame.mixer.Sound('./assests/hit.wav')
            crash.play()
            crash.set_volume(0.3)        

#------------------------------CHECK EVENTS----------------------------#
    def check_events(self):
        """"Listen for and handle all program events"""
        # Iterate (loop) through all captured events
        for event in pygame.event.get():

            # Closing the game causes the QUIT event to be fired
            if event.type == pygame.QUIT:
                # Quit pygame
                pygame.quit()
                # Exit Python
                exit()

#--------------------GET KEYS------------------#
    def get_keys(self):
        # Update player paddle position
        # Get the state of all keyboard keys pressed at the moment
        keys = pygame.key.get_pressed()

        # Check if the UP arrow key is pressed
        if keys[pygame.K_UP]:
            # If the UP arrow key is pressed, move the player up
            self.player.move_up()

        # Check if the DOWN arrow key is pressed
        if keys[pygame.K_DOWN]:
            # If the DOWN arrow key is pressed, move the player down
            self.player.move_down()

        # The ESC key will quit the game
        if keys[pygame.K_ESCAPE]:
            # Quit Pygame
            pygame.quit()
            # Exit Python
            exit()

#------------------------------------GAME LOOP----------------------------#
    def game_loop(self):
        """Infinite game loop"""
        while True:
            self.check_events()

            self.computer.move_computer_paddle()
            self.get_keys()

            self.check_collision()

            #----------------------------DRAW ON BACKBUFFER-----------------------#
            # Draw everything in the backbuffer first
            # Fill the display surface with black
            self.surface.fill(config.BLACK)

            self.draw_net()

            # Draw a rectangle for the player's paddle
            # on the screen using Pygame's draw function
            pygame.draw.rect(
                self.surface,           # Surface to draw on
                config.WHITE,           # Color to draw with
                self.player             # rect image object to draw
            )

            # Draw a rectangle for the computer's paddle
            # on the screen using Pygame's draw function
            pygame.draw.rect(
                self.surface,           # Surface to draw on
                config.WHITE,           # Color to draw with
                self.computer           # rect image object to draw
            )

            # Move the ball position every frame
            self.ball.x += self.ball_speed_x
            self.ball.y += self.ball_speed_y

            # Draw ball to the backbuffer
            pygame.draw.ellipse(
                self.surface,           # Surface to draw on
                config.WHITE,           # Color to draw with
                self.ball               # Rect image object to draw
            )

            # Render the player's score text using specified font,
            # color, and score value
            player_score = self.score_font.render(
                "Player:" + str(self.player_score), True, config.WHITE)
            
            # Render the computer's score text using specified font,
            # color, and score value
            computer_score = self.score_font.render(
                "Computer:" + str(self.computer_score), True, config.WHITE)

            # Display the player's score text on the game surface
            # at the specified position
            self.surface.blit(player_score, (30, 5))
            # Display the computer's score text on the game surface
            # at the specified position
            self.surface.blit(computer_score, (config.WIDTH - 150, 5)) 

            #----------------------UPDATE SURFACE---------------------------#
            # From back buffer, update pygame display to reflect any changes
            pygame.display.update()

            # Cap game speed to 60 fps
            self.clock.tick(60)

#----------------------------------DRAW NET----------------------------------#
    def draw_net(self):
        # Define the width of the net lines
        net_width = 2

        #Loop through the height of the game screen
        # with the step of 2 pixels
        for i in range(0, config.HEIGHT, 20):

            # Draw a rectangle representing a part of the net
            pygame.draw.rect(
                self.surface,               # Surface to draw on
                config.WHITE,               # Color of the rectangle (white)
                (                           # Rectangle coordinates and size
                    # x-coordinate of the left corner of the rectangle
                    config.WIDTH // 2- net_width // 2,
                    i,   # Y-coordinate of top corner of rectangle
                    net_width,              # Width of the rectangle
                    10                      # Height of the rectangle
                )
            )

#----------------------------------MAIN PROGRAM----------------------------------#
def main():
    # Create pong program object
    pong = Pong()
    # Start infinite game loop
    pong.game_loop()

main()