# this file was created by riley hay
# import needed modules and libraries
#Used Ai for debugging and help learning what code does.
import pygame as pg
from settings import *
from sprites_side_scroller import *
from tilemap import *
from os import path
import sys
import random
'''
Goals: Make the game challenging but fun.
Rules: Gravity and death
Feedback: Jumping when space bar
Freedom: You get to choose how your charecter moves.

Alpha goal: make gravity to make the flappy bird.

Beta goal: make pipes work and kill the bird

final: debug the final game for release
'''

class Game:
    # Initializes all game properties like display, audio, time, etc.
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Riley's Game")
        self.clock = pg.time.Clock()
        self.running = True
        self.game_over = False

    # Load external resources or data, like map files
    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.map = Map(path.join(self.game_folder, 'level1.txt'))

    # Set up the game state, initialize sprites, and groups
    def new(self):
        self.load_data()
        print(self.map.data)
        # Create all sprites and groups
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.pipes = pg.sprite.Group()

        # Instantiate bird object and add to all_sprites
        self.bird = Bird(100, HEIGHT // 2)
        self.all_sprites.add(self.bird)

    # Method to spawn pipes at intervals
    def spawn_pipes(self):
        gap_height = random.randint(100, HEIGHT - 200)  # Random gap height between pipes
        pipe = Pipe(WIDTH, gap_height)
        self.all_sprites.add(pipe)  
        self.pipes.add(pipe)

    # Main game loop to manage events, updates, and drawing
    def run(self):
        last_pipe_spawn = pg.time.get_ticks()
        pipe_spawn_interval = 1500  # Spawn pipes every 1.5 seconds

        # Main game loop
        while self.running and not self.game_over:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

            # Spawn pipes at set intervals
            if pg.time.get_ticks() - last_pipe_spawn > pipe_spawn_interval:
                self.spawn_pipes()
                last_pipe_spawn = pg.time.get_ticks()

    # Handle user input and other events
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN and not self.game_over:
                if event.key == pg.K_SPACE:
                    self.bird.flap()

    # Update game elements and check for conditions like game over
    def update(self):
        # Update sprites and check for game over
        self.all_sprites.update()    
        if self.bird.rect.y > HEIGHT:
            self.game_over = True


    # Draw text on the screen
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial') 
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

    # Render game visuals, including sprites, background, and text
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.dt * 1000), 24, WHITE, WIDTH / 30, HEIGHT / 30)
        self.draw_text(self.screen, "FLAPPY BIRD!!!!", 24, WHITE, WIDTH / 2, HEIGHT / 24)
        pg.display.flip()

if __name__ == "__main__":
    g = Game()
    g.new()
    g.run()
    pg.quit()
