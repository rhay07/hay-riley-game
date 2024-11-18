# this fine was created by riley hay

import pygame as pg
from pygame.sprite import Sprite
from settings import *
import random


# class Bird(pg.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__()  
#         self.image = pg.Surface((30, 30))
#         self.image.fill((ORANGE)) 
#         self.rect = self.image.get_rect()
#         self.rect.center = (x, y)
#         self.y_velocity = 0

#     def update(self):
#         self.y_velocity += 1  # Gravity effect
#         self.rect.y += self.y_velocity

#     def flap(self):
#         self.y_velocity = -14  # Flap up by reducing y_velocity
class Bird(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Load the two frames
        self.frames = [
            pg.image.load("fowl-1.png").convert_alpha(),
            pg.image.load("fowl-2.png").convert_alpha()
        ]
        
        # Scale the frames if necessary
        self.frames = [pg.transform.scale(frame, (100, 100)) for frame in self.frames]
        
        # Set the initial frame
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Animation timer
        self.last_update = pg.time.get_ticks()  # Track time since the last frame change
        self.frame_rate = 200  # Milliseconds per frame

        # Movement variables
        self.velocity = 0

    def flap(self):
        self.velocity = -10  # Set the velocity for flapping
    
    def animate(self):
        # Update frame if enough time has passed
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            # Toggle between frames 0 and 1
            self.current_frame = (self.current_frame + 1) % 2
            self.image = self.frames[self.current_frame]

    def update(self):
        # Call animate function to update frames
        self.animate()

        # Apply gravity and update position
        self.velocity += 0.5  # Simulate gravity
        self.rect.y += int(self.velocity)

        # Check boundaries (e.g., game over if out of bounds)
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0  # Stop the bird at the bottom



class Pipe(pg.sprite.Sprite):
    def __init__(self, x, gap_y, position):
        super().__init__()

        # Load the pipe image
        self.pipe_image = pg.image.load('greenvine6.png').convert_alpha()

        # Get the dimensions of the pipe image
        pipe_width, pipe_height = self.pipe_image.get_size()

        # Create a surface for the pipe
        pipe_surface_height = HEIGHT  # Pipe will stretch to screen height
        self.image = pg.Surface((pipe_width, pipe_surface_height), pg.SRCALPHA)  # Transparent background

        # Tile the pipe image to fill the surface
        for y in range(0, pipe_surface_height, pipe_height):
            self.image.blit(self.pipe_image, (0, y))

        # Flip the image for 'upper' pipes
        if position == 'upper':
            self.image = pg.transform.flip(self.image, False, True)

        # Set the rectangle for positioning
        self.rect = self.image.get_rect()
        if position == 'upper':
            self.rect.bottom = gap_y  # Align bottom of top pipe to the gap
        elif position == 'lower':
            self.rect.top = gap_y + PIPEGAP  # Align top of bottom pipe to the gap

        self.rect.x = x

    def update(self):
        # Move the pipes to the left
        self.rect.x -= 6

        # Remove pipes that are off-screen
        if self.rect.right < 0:
            self.kill()
