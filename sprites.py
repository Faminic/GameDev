# Will contain all sprite classes for my game
import pygame as pg
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30,40))
        self.image.fill(yellow)
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2)
        self.pos = vec(width/2, height/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    
    def update(self):
        self.acc = vec(0,0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -player_acc
        if keys[pg.K_RIGHT]:
            self.acc.x = player_acc
        
        #apply friction
        self.acc += self.vel * player_friction
        #actual motion equation
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        #make player wrap around the sides of the screen
        if self.pos.x > width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = width

        self.rect.center = self.pos