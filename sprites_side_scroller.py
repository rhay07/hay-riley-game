# this fine was created by riley hay

import pygame as pg
from pygame.sprite import Sprite
from settings import *
import random
vec = pg.math.Vector2

class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups, game.all_walls)
        self.game = game
        self.image = pg.Surface((32, 32))
        self.rect = self.image.get_rect()
        self.image.fill(RED)
        #self.rect.x = x
        #self.rect.y = y
        # self.x = x * TILESIZE
        # self.y = y * TILESIZE
        self.pos = vec(x*TILESIZE, y*TILESIZE)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.speed = 5
        self.jumping = False
        self.jump_power = 25
        # self.vx, self.vy = 0, 0
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
    def get_keys(self):
        keys = pg.key.get_pressed()
        # if keys[pg.K_s]:
        #     self.vy -= self.speed
        if keys[pg.K_d]:
            self.vx -= self.speed
        #if keys[pg.K_w]:
        #    self.vy += self.speed
        if keys[pg.K_a]:
            self.vx += self.speed
        if keys[pg.K_SPACE]:
            self.jump()

    def jump(self):
        print("im trying to jump")
        print(self.vel.y)
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -self.jump_power
    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "powerup":
                print("i just hit a powerup...")
    def update(self):
        self.acc = vec(0, Gravity)
        self.get_keys()
        self.acc.x += self.vel.x * Friction
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # self.x += self.vx * self.game.dt
        # self.y += self.vy * self.game.dt
        self.collide_with_stuff(self.game.all_powerups, True)
        self.collide_with_walls('x')
        self.rect.x = self.pos.x
        self.collide_with_walls('y')
        self.rect.y = self.pos.y
        # self.rect.x += 1


class Mob(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((32, 32))
        self.rect = self.image.get_rect()
        self.image.fill(GREEN)
        self.rect.x = 300
        self.rect.y = 200
        self.speed = 10
        self.category = random.choice([0,1])
    def update(self):
     
        # moving towards the side of the screen
        self.rect.x += self.speed
        # when it hits the side of the screen, it will move down
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.speed *= -1
            self.rect.y += 32
        #elif self.rect.colliderect(self.game.player):
        #    self.speed *= -1
        #elif self.rect.colliderect(self):
        #    self.speed *= -1

class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        self.game = game
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(WHITE)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self):
        pass

class Powerup(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_powerups
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(PINK)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE