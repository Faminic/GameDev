# Will contain all sprite classes for my game
import pygame as pg
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self,game):
        pg.sprite.Sprite.__init__(self)
        self.game = game #is a reference to the current game
        self.image = self.game.spritesheet.get_image(67,190,66,92,1.5)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2)
        self.pos = vec(width/2, height/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    
    def jump(self):
        # jump only if standing on a platform -> do that by checking if there is a collision 1 pixel below
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms,False)
        self.rect.y += -1
        if hits:
            self.vel.y = -player_jump

    def update(self):
        self.acc = vec(0,player_gravity) #gravity basically pulls you down
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -player_acc
        if keys[pg.K_RIGHT]:
            self.acc.x = player_acc
        
        #apply friction
        self.acc.x += self.vel.x * player_friction
        #actual motion equation
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        #make player wrap around the sides of the screen
        if self.pos.x > width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = width

        self.rect.midbottom = self.pos


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#class for loading and dealing with spritesheets
class Spritesheet:
    def __init__(self,filename):
        self.spritesheet = pg.image.load(filename).convert()
    
    #have multiple images in spritesheet, so this function helps get a specific image out
    def get_image(self,x,y,width,height,scaleBy):
        image = pg.Surface((width,height))
        image.blit(self.spritesheet,(0,0),(x,y,width,height))
        #scale it appropriately
        image = pg.transform.scale(image, (round(width/scaleBy),round(height/scaleBy)))
        return image

