# this file was created by riley hay
#import needed moduals and librarys

import pygame as pg

from settings import *
from sprites import *

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
    def new(self):
        #allowing new things to be made in the game, and CREATES ALL SPRITES GROUP!!!! so we can update and render
        self.all_sprites = pg.sprite.Group()
        self.player = Player(self, 1, 1)
        # instantiated a mob
        self.mob = Mob(self, 100,100)
        #
        for i in range(60):
            Mob(self, (0, 200), (0, 200))
        for i in range(6):
            print(i*TILESIZE)
            Wall(self, i*TILESIZE, i*TILESIZE)

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
        print(self.player.rect.colliderect(self.mob))
        pass
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pg.display.flip()


if __name__ == "__main__":
    g = Game()
    g.new()
    g.run()

        
        