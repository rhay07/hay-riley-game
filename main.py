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
Chat gpt "How do I add an animated sprite"
Chat gpt "How do I make the sprite half way off screen"
Chat gpt "How do I make a score board"
'''

class Game:
    # Initializes all game properties like display, audio, time, etc. 
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Riley's Game")
        self.clock = pg.time.Clock()
        self.score = 0
        self.highscore = 0
        self.running = True
        self.game_over = False
        self.showing_menu = True
        self.selected_skin = "Default"
        self.background = pg.image.load(path.join(r'C:\Users\Riley.Hay26\OneDrive - Bellarmine College Preparatory\_Junior Year\Comp si', 'vgt0szh38rx11.webp'))
        self.background = pg.transform.scale(self.background, (WIDTH, HEIGHT))  # Scale to fit screen
        self.menu_background = pg.image.load(path.join(r'C:\Users\Riley.Hay26\OneDrive - Bellarmine College Preparatory\_Junior Year\Comp si', 'menubackground.png'))
        self.menu_background = pg.transform.scale(self.menu_background, (WIDTH, HEIGHT))  # Scale to fit screen
        #self.logo1 = pg.image.load("fowl-1.png")  # Load the small image
        #self.logo2 = pg.image.load("fowl-2.png")
        #self.logo1 = pg.transform.scale(self.logo1, (250, 250))  # Scale the logo if needed
        #self.logo2 = pg.transform.scale(self.logo2, (250, 250))
        #self.current_logo = self.logo1  # Start with logo1
        #self.last_update = pg.time.get_ticks()  # Get the time at the start
        #self.switch_time = 500 


    # Load external resources or data, like map files
    def load_data(self):
        self.game_folder = path.dirname(__file__)
        #with open(path.join(self.game_folder, HS_FILE), "w") as f:
        #    f.write(str(self.highscore))
        with open(path.join(self.game_folder, HS_FILE), 'r') as f:
                try:
                    self.highscore = int(f.read())
                except:
                    self.highscore=0
        self.map = Map(path.join(self.game_folder, 'level1.txt'))

    # Reset game state, initialize sprites, and groups
    def reset(self):
        self.game_over = False
        self.score = 0
        self.new()  # Reset the game by calling new

    # Set up the game state, initialize sprites, and groups
    def new(self):
        self.load_data()
        print(self.map.data)
        # Create all sprites and groups
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.pipes = pg.sprite.Group()
        self.vulture = pg.sprite.Group()
        # Instantiate bird object
        #self.bird = Bird(300, HEIGHT // 2)
        self.bird = Bird(300, HEIGHT // 2, skin=self.selected_skin)
        self.vulture = Vulture(-150, HEIGHT // 2.9)
        self.all_sprites.add(self.bird, self.vulture)

    def show_menu(self):
    # Define skin options and initialize the current index
        skin_options = ["Default", "Red", "Quetzal", "Kiwi"]
        current_skin_index = 0

        waiting = True
        while waiting:
        # Draw the menu background
            self.screen.blit(self.menu_background, (0, 0))

        # Display the menu title
            self.draw_text(self.screen, "Flapping Fowl", 48, WHITE, WIDTH / 2, HEIGHT / 4)

        # Show the currently selected skin
            self.draw_text(self.screen, f"Selected Skin: {skin_options[current_skin_index]}", 24, WHITE, WIDTH / 2, HEIGHT / 2)

        # Show instructions for changing skins and starting the game
            self.draw_text(self.screen, "Press LEFT/RIGHT to change skin", 24, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
            self.draw_text(self.screen, "Press ENTER to start", 24, WHITE, WIDTH / 2, HEIGHT * 7 / 8)

        # Refresh the display
            pg.display.flip()

        # Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    waiting = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:  # Start the game
                        self.selected_skin = skin_options[current_skin_index]
                        self.showing_menu = False
                        waiting = False
                    elif event.key == pg.K_RIGHT:  # Switch to the next skin
                        current_skin_index = (current_skin_index + 1) % len(skin_options)
                    elif event.key == pg.K_LEFT:  # Switch to the previous skin
                        current_skin_index = (current_skin_index - 1) % len(skin_options)


    def switch_logo(self):
        # Switch the logo based on time
        now = pg.time.get_ticks()  # Get the current time in milliseconds
        if now - self.last_update > self.switch_time:  # If enough time has passed
            # Toggle between the two logos
            self.current_logo = self.logo2 if self.current_logo == self.logo1 else self.logo1
            self.last_update = now  # Reset the timer

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
                # if self.score > self.highscore:
                #     self.highscore = self.score
                #     with open(path.join(self.game_folder, HS_FILE), "w") as f:
                #         f.write(str(self.highscore))

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
            # if self.score > self.highscore:
            #     self.highscore = self.score
            # with open(path.join(self.game_folder, HS_FILE), "w") as f:
            #     f.write(str(self.highscore))
        for pipe in self.pipes:
            if pipe.rect.x < self.bird.rect.x and not pipe.passed:
                pipe.passed = True
                self.score += 0.5  # Increase score
                #self.highscore += 0.5  # Increase score

    # Draw text on the screen
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('impact ')
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
#        self.draw_text(self.screen, str(self.dt * 1000), 24, WHITE, WIDTH / 30, HEIGHT / 30)
#        self.draw_text(self.screen, "DONT HIT THE FLOOR", 24, BLACK, WIDTH / 2, HEIGHT / 24)
        self.draw_text(self.screen, "BUT DONT FLY TOO HIGH", 24, WHITE, WIDTH / 2, HEIGHT / 1.1)
        self.draw_text(self.screen, f"Score: {self.score}", 24, WHITE, WIDTH / 2, 20)
        # self.draw_text(self.screen, f"High Score: {self.highscore}", 24, WHITE, WIDTH / 2, 45)
        pg.display.flip()

if __name__ == "__main__":
    g = Game()
    g.new()
    g.run()
    pg.quit()
