# this file was created by riley hay
#import needed moduals and librarys

import pygame as pg

from settings import *
from sprites import *
from tilemap import *
from os import path
from random import randint
'''
Goals
Rules
Feedback
Freedom
'''

# created a game class to instantiate later
# it will have all the necessary parts to run the game



# created a game class to instantiate later
# it will have all the necessary parts to run the game
class Game:
    # makes the game initlize all properteys of game like display, audio, time, and ect.
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Riley's Game")
        self.clock = pg.time.Clock()
        self.running = True
    def load_data(self):
        self.game_folder = path.dirname (__file__)
        self.map = Map(path.join(self.game_folder, 'level1.txt'))
    def new(self):
        self.load_data()
        print(self.map.data)
        #allowing new things to be made in the game, and CREATES ALL SPRITES GROUP!!!! so we can update and render
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_powerups = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'M':
                    mob = Mob(self, col, row)
                if tile == 'U':
                    Powerup(self, col, row)

    def run(self):
        #making game run
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
        # input
    def events(self):
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
#updating to see if still coliding or not
    def update(self):
        self.all_sprites.update()
        #print(self.player.rect.colliderect(self.mob))
        pass
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surface.blit(text_surface, text_rect)
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.dt*1000), 24, WHITE, WIDTH/30, HEIGHT/30)
        self.draw_text(self.screen, "This game is awesome...", 24, WHITE, WIDTH/2, HEIGHT/24)
        pg.display.flip()


if __name__ == "__main__":
    g = Game()
    g.new()
    g.run()

        
        