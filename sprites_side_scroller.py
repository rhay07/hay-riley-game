# this fine was created by riley hay

import pygame as pg
from pygame.sprite import Sprite
from settings import *
import random


class Bird(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()  
        self.image = pg.Surface((30, 30))
        self.image.fill((ORANGE)) 
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.y_velocity = 0

    def update(self):
        self.y_velocity += 1  # Gravity effect
        self.rect.y += self.y_velocity

    def flap(self):
        self.y_velocity = -14  # Flap up by reducing y_velocity


class Pipe(pg.sprite.Sprite):
    def __init__(self, x, gap_height):
        super().__init__()  # Initialize the Sprite superclass
        self.image = pg.Surface((50, HEIGHT))  # Width of the pipe and screen height
        self.image.fill((0, 255, 0)) 

        # Create the gap by cutting the pipe's image
        self.image = pg.Surface((50, HEIGHT))  # Width of the pipe and screen height
        self.image.fill(DARKGREEN)  # Green color for the pipe
        self.rect = self.image.get_rect()
        self.rect.x = x


    def update(self):
        # Move the pipes left to simulate scrolling
        self.rect.x -= 5
    

        # Check if pipes have moved off screen to delete
        if self.rect.right < 0:
            self.kill()
