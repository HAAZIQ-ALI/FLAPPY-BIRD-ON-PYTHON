import pygame as py
import random
import os
os.chdir("C:/Users/User/Desktop/flappy bird")


# Initialize Pygame
py.init()

# Set up display
screen = py.display.set_mode((288, 512))
py.display.set_caption("FLAPPY BIRD BY HAAZIQ")

# Background image
image_path = "assets\\sprites\\background-day.png"
background = py.image.load(image_path)

# Bird images
bird_upwing = py.image.load("assets\\sprites\\bluebird-upflap.png")
bird_midwing = py.image.load("assets\\sprites\\bluebird-midflap.png")
bird_downwing = py.image.load("assets\\sprites\\bluebird-downflap.png")

bird_rect = bird_upwing.get_rect(center=(50, 250))

# Animation settings
bird_frames = [bird_upwing, bird_midwing, bird_downwing]
current_bird_state = 0
animation_counter = 0

# Gravity and movement settings
bird_velocity = 0
gravity = 0.1
flap_strength = -2.99 

# Pipe settings
pipe_gap = 200     
pipe_velocity = 3
pipe_frequency = 1400
pipe_timer = py.USEREVENT + 1
py.time.set_timer(pipe_timer, pipe_frequency)

# Pipe images
pipe_top_image = py.image.load("assets\\sprites\\pipe-green.png")
pipe_bottom_image = py.image.load("assets\\sprites\\pipe-green.png")

# Score settings
score = 0
score_images = [py.image.load(f"assets\\sprites\\{i}.png") for i in range(10)]

# Background music
music_path = "assets\\simpsonwave 1995 (slowed).mp3"
py.mixer.music.load(music_path)
py.mixer.music.play(-1)

# Define Pipe class
class Pipe:
    def __init__(self, top_rect, bottom_rect):
        self.top_rect = top_rect
        self.bottom_rect = bottom_rect
        self.scored = False

# Function to create pipes
def create_pipe():
    gap_y = random.randint(100, 300)
    top_rect = pipe_top_image.get_rect(midbottom=(288, gap_y - pipe_gap // 2))
    bottom_rect = pipe_bottom_image.get_rect(midtop=(288, gap_y + pipe_gap // 2))
    return Pipe(top_rect, bottom_rect)

# Function to move pipes
def move_pipes(pipes):
    for pipe in pipes:
        pipe.top_rect.centerx -= pipe_velocity
        pipe.bottom_rect.centerx -= pipe_velocity
    return [pipe for pipe in pipes if pipe.top_rect.right > 0]

# Check collisions
def check_collision(bird_rect, pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe.top_rect) or bird_rect.colliderect(pipe.bottom_rect):
            return True
    return bird_rect.top <= 0 or bird_rect.bottom >= 512

# Game loop
running = True
pipes = []
while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        if event.type == pipe_timer:
            pipes.append(create_pipe())

    # Bird flapping
    keys = py.key.get_pressed()
    if keys[py.K_SPACE]:
        bird_velocity = flap_strength

    # Bird movement
    bird_velocity += gravity
    bird_rect.y += bird_velocity

    # Animate bird
    animation_counter += 1
    if animation_counter % 10 == 0:
        current_bird_state = (current_bird_state + 1) % len(bird_frames)

    # Update pipes
    pipes = move_pipes(pipes)

    # Check for collisions
    if check_collision(bird_rect, pipes):
        running = False

    # Update score
    for pipe in pipes:
        if pipe.top_rect.right < bird_rect.left and not pipe.scored:
            score += 1
            pipe.scored = True

    # Draw everything
    screen.blit(background, (0, 0))
    for pipe in pipes:
        screen.blit(pipe_top_image, pipe.top_rect)
        screen.blit(pipe_bottom_image, pipe.bottom_rect)
    screen.blit(bird_frames[current_bird_state], bird_rect)

    # Draw score
    score_text = str(score)
    x_offset = 10
    for digit in score_text:
        screen.blit(score_images[int(digit)], (x_offset, 10))
        x_offset += 20

    py.display.update()

py.quit()
                 