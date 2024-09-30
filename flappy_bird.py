import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 30  # Reduced FPS to slow down the game a bit
GRAVITY = 0.3  # Lower gravity to make the bird fall slower

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Load bird and background images
bird_img = pygame.image.load('bird.png')
bird_img = pygame.transform.scale(bird_img, (50, 40))  # Resize bird to 40x30 pixels
background_img = pygame.image.load('background.png')

# Resize background to fit the screen
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flying Eram')

# Set clock for controlling frame rate
clock = pygame.time.Clock()

# Font for displaying the score and button text
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)  # Large font for final score

# Bird class
class Bird:
    def __init__(self):
        self.bird_rect = bird_img.get_rect(center=(50, SCREEN_HEIGHT // 2))
        self.velocity = 0

    def move(self):
        self.velocity += GRAVITY
        self.bird_rect.y += int(self.velocity)

    def jump(self):
        self.velocity = -7  # Reduced jump strength to match slower gravity

    def draw(self):
        screen.blit(bird_img, self.bird_rect)  # Draw bird image

# Pipe class
class Pipe:
    def __init__(self):
        self.width = 60
        self.height = random.randint(150, 400)
        self.gap = 150
        self.x = SCREEN_WIDTH
        self.pipe_rect_top = pygame.Rect(self.x, 0, self.width, self.height)
        self.pipe_rect_bottom = pygame.Rect(self.x, self.height + self.gap, self.width, SCREEN_HEIGHT - self.height - self.gap)
        self.scored = False

    def move(self):
        self.x -= 3  # Slowed down pipe speed
        self.pipe_rect_top.x = self.x
        self.pipe_rect_bottom.x = self.x

    def draw(self):
        pygame.draw.rect(screen, (0, 255, 0), self.pipe_rect_top)  # Green pipe
        pygame.draw.rect(screen, (0, 255, 0), self.pipe_rect_bottom)

    def off_screen(self):
        return self.x < -self.width

# Check for collision with tolerance
def check_collision_with_tolerance():
    tolerance = 5  # Pixels for forgiving collision tolerance
    bird_rect = bird.bird_rect

    for pipe in pipes:
        # Inflate the pipe's rect by the tolerance
        pipe_rect_top = pipe.pipe_rect_top.inflate(tolerance, tolerance)
        pipe_rect_bottom = pipe.pipe_rect_bottom.inflate(tolerance, tolerance)

        # Check for collisions with the inflated pipe rects
        if bird_rect.colliderect(pipe_rect_top) or bird_rect.colliderect(pipe_rect_bottom):
            return True

    # Check if the bird hits the top or bottom of the screen
    if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT:
        return True

    return False

# Update score
def update_score():
    global score
    for pipe in pipes:
        if pipe.x + pipe.width < bird.bird_rect.x and not pipe.scored:
            score += 1
            pipe.scored = True

# Display the score
def display_score():
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (10, 10))

# Display the final score at the end of the game
def display_final_score():
    text = large_font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100))

# Function to display the "Start Game" button
def display_start_button():
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 - 25, 150, 50)
    pygame.draw.rect(screen, BLUE, button_rect)
    text = font.render("Start Game", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - 65, SCREEN_HEIGHT // 2 - 15))
    return button_rect

# Function to display the "Play Again" button after losing
def display_play_again_button():
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 50, 150, 50)
    pygame.draw.rect(screen, BLUE, button_rect)
    text = font.render("Play Again", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - 65, SCREEN_HEIGHT // 2 + 60))
    return button_rect

# Function to wait for the user to click the "Start Game" button
def wait_for_start():
    waiting = True
    while waiting:
        screen.blit(background_img, (0, 0))  # Draw the background image
        button_rect = display_start_button()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False

# Function to wait for the user to click the "Play Again" button after losing
def wait_for_play_again():
    waiting = True
    while waiting:
        screen.blit(background_img, (0, 0))  # Draw the background image
        display_final_score()  # Display final score
        button_rect = display_play_again_button()  # Display "Play Again" button
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False

# Initialize the bird, pipes, and score
bird = Bird()
pipes = []
score = 0

# Main game loop
def game_loop():
    global pipes, score
    running = True

    # Display start button and wait for the user to click
    wait_for_start()

    # Reset the game state
    bird.__init__()
    pipes = [Pipe()]
    score = 0

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        # Move the bird and pipes
        bird.move()

        if check_collision_with_tolerance():
            running = False  # End game on collision

        update_score()

        for pipe in pipes:
            pipe.move()

        # Add new pipes
        if pipes[-1].x < SCREEN_WIDTH - 200:
            pipes.append(Pipe())

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if not pipe.off_screen()]

        # Draw the game
        screen.blit(background_img, (0, 0))  # Draw the background image
        bird.draw()

        for pipe in pipes:
            pipe.draw()

        display_score()

        # Update the display and control the frame rate
        pygame.display.flip()
        clock.tick(FPS)

    # Display final score and "Play Again" button
    wait_for_play_again()

    # Restart the game
    game_loop()

# Run the game loop
game_loop()