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
        super().__init__()  # Initialize the Sprite superclass
        #self.image = pg.image.load('stone.png')
        self.image = pg.Surface((50, HEIGHT))  # Width of the pipe and screen height
        # Create the gap by cutting the pipe's image
        self.image = pg.Surface((50, HEIGHT))  # Width of the pipe and screen height
        self.image.fill(DARKGREEN)  # Green color for the pipe
        self.rect = self.image.get_rect()

        if position == 'upper':
            # Place the top pipe at the specified gap_y position
            self.rect.bottom = gap_y  # Align bottom of top pipe to the top of the gap
        elif position == 'lower':
            # Place the bottom pipe just below the gap
            self.rect.top = gap_y + PIPEGAP  # Align top of bottom pipe to the bottom of the gap

        self.rect.x = x


    def update(self):
        # Move the pipes left to simulate scrolling
        self.rect.x -= 5


        # Check if pipes have moved off screen to delete
        if self.rect.right < 0:
            self.kill()
