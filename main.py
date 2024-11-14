# this file was created by Riley Hay
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

'''
Sources 
Chat gpt "How do I add a menu screen to the game"
Chat gpt "How do I add a image for the background"
Chat gpt "The image is not displaying"
Chat gpt "What is the rgb code for a dark green color"
Chat gpt "How do I make gaps in the pipe"
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
        self.showing_menu = True
        self.background = pg.image.load(path.join(r'C:\Users\Riley.Hay26\OneDrive - Bellarmine College Preparatory\_Junior Year\Comp si', 'wp6956942.webp'))
        self.background = pg.transform.scale(self.background, (WIDTH, HEIGHT))  # Scale to fit screen
        #self.menu_background = pg.image.load(path.join(r'C:\Users\Riley.Hay26\OneDrive - Bellarmine College Preparatory\_Junior Year\Comp si', 'menubackground.jpg'))
        #self.menu_background = pg.transform.scale(self.menu_background, (WIDTH, HEIGHT))  # Scale to fit screen

    # Load external resources or data, like map files
    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.map = Map(path.join(self.game_folder, 'level1.txt'))

    # Reset game state, initialize sprites, and groups
    def reset(self):
        self.game_over = False
        self.new()  # Reset the game by calling new

    # Set up the game state, initialize sprites, and groups
    def new(self):
        self.load_data()
        print(self.map.data)
        # Create all sprites and groups
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.pipes = pg.sprite.Group()
        # Instantiate bird object
        self.bird = Bird(100, HEIGHT // 2)
        self.all_sprites.add(self.bird)

    # Show a menu screen before the game starts
    def show_menu(self):
        # Display a menu with "Start" and "Quit" options
        self.screen.fill(BLACK)
        self.draw_text(self.screen, "Flapping Fowl", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text(self.screen, "Press ENTER to start", 24, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text(self.screen, "Press Q to quit", 24, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()

        # Wait for user input
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    waiting = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:  # Enter key to start the game
                        self.showing_menu = False
                        waiting = False
                    if event.key == pg.K_q:  # Q key to quit the game
                        self.running = False
                        waiting = False

    # Function to spawn pipes with a random gap height
    # def spawn_pipes(self):
    #     gap_height = random.randint(100, HEIGHT - 200)
    #     pipe = Pipe(WIDTH, gap_height)
    #     self.all_sprites.add(pipe)
    #     self.pipes.add(pipe)
    def spawn_pipes(self):
        gap_y = random.randint(100, HEIGHT - 200)  # Random gap position within a range

         # Create upper and lower pipes with the gap in between
        upper_pipe = Pipe(WIDTH, gap_y, 'upper')
        lower_pipe = Pipe(WIDTH, gap_y, 'lower')
  
        # Add pipes to sprite groups
        self.all_sprites.add(upper_pipe, lower_pipe)
        self.pipes.add(upper_pipe, lower_pipe)

    # Main game loop to manage events, updates, and drawing
    def run(self):
        last_pipe_spawn = pg.time.get_ticks()
        pipe_spawn_interval = 2000
        # Main game loop
        while self.running:
            if self.showing_menu:
                self.show_menu()
                self.reset()  # Reset game state each time the menu is shown

            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

            # Spawn pipes at set intervals
            if pg.time.get_ticks() - last_pipe_spawn > pipe_spawn_interval:
                self.spawn_pipes()
                last_pipe_spawn = pg.time.get_ticks()

            # If game over, show the menu
            if self.game_over:
                self.showing_menu = True

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
            self.game_over = True  # Trigger game over if bird falls below screen
        pipe_collisions = pg.sprite.spritecollide(self.bird, self.pipes, False, pg.sprite.collide_mask)
        if pipe_collisions or self.bird.rect.bottom > HEIGHT or self.bird.rect.top < 0:  # Add top screen collision
            self.game_over = True
            self.showing_menu = True  # Return to the menu

    # Draw text on the screen
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('impact')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

    # Render game visuals, including sprites, background, and text
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        #self.screen.blit(self.menu_background, (0, 0))
        #self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.dt * 1000), 24, WHITE, WIDTH / 30, HEIGHT / 30)
        self.draw_text(self.screen, "DONT HIT THE FLOOR", 24, BLACK, WIDTH / 2, HEIGHT / 24)
        self.draw_text(self.screen, "BUT DONT FLY TOO HIGH", 24, BLACK, WIDTH / 2, HEIGHT / 1.1)
        pg.display.flip()

if __name__ == "__main__":
    g = Game()
    g.new()
    g.run()
    pg.quit()
