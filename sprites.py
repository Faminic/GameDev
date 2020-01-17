# Will contain all sprite classes for my game
import pygame as pg
from settings import *
import random
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self,game):
        self.groups = game.all_sprites
        self._layer = player_layer
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game #is a reference to the current game
        #variables for animations
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        #loading all sprite animation images
        self.load_images()
        self.looking_right = True #player is initially looking right
        self.image = self.standing_frame_r
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height-50)
        self.pos = vec(width/2, height-50)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    
    #load animations
    def load_images(self):
        scaleBy = 1.5
        self.standing_frame_r = self.game.spritesheet.get_image(67,190,66,92,scaleBy)
        self.standing_frame_l = pg.transform.flip(self.standing_frame_r,True,False)
        self.standing_frame_r.set_colorkey(black)
        self.standing_frame_l.set_colorkey(black)
        self.walk_frames_r = [self.game.spritesheet.get_image(0,0,72,97,scaleBy),
                              self.game.spritesheet.get_image(73,0,72,97,scaleBy),
                              self.game.spritesheet.get_image(146,0,72,97,scaleBy),
                              self.game.spritesheet.get_image(0,98,72,97,scaleBy),
                              self.game.spritesheet.get_image(73,98,72,97,scaleBy),
                              self.game.spritesheet.get_image(146,98,72,97,scaleBy),
                              self.game.spritesheet.get_image(219,0,72,97,scaleBy),
                              self.game.spritesheet.get_image(292,0,72,97,scaleBy),
                              self.game.spritesheet.get_image(219,98,72,97,scaleBy),
                              self.game.spritesheet.get_image(365,0,72,97,scaleBy),
                              self.game.spritesheet.get_image(292,98,72,97,scaleBy)]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(black)
            self.walk_frames_l.append(pg.transform.flip(frame,True,False))
        self.jump_frame_r = self.game.spritesheet.get_image(438,93,67,94,scaleBy)
        self.jump_frame_l = pg.transform.flip(self.jump_frame_r,True,False)
        self.jump_frame_r.set_colorkey(black)
        self.jump_frame_l.set_colorkey(black)
        
    
    def jump(self):
        # jump only if standing on a platform -> do that by checking if there is a collision 1 pixel below
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms,False)
        self.rect.y += -2
        if hits:
            self.game.jump_sound.play()
            self.vel.y = -player_jump

    def update(self):
        #do animations
        self.animate()
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
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        if abs(self.vel.y) < 0.1:
            self.vel.y = 0
        self.pos += self.vel + 0.5 * self.acc
        #make player wrap around the sides of the screen
        if self.pos.x > width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = width

        self.rect.midbottom = self.pos
    
    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
            if self.vel.x > 0:
                self.looking_right = True
            else:
                self.looking_right = False
        else:
            self.walking = False
        
        if self.vel.y < 0:
            self.jumping = True
        else:
            self.jumping = False
        
        #show walking animation
        if self.walking:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.looking_right:
                    self.image = self.walk_frames_r[self.current_frame]
                    self.looking_right = True
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                    self.looking_right = False
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        #show jumping animation
        if self.jumping:
            bottom = self.rect.bottom
            if self.looking_right:
                self.image = self.jump_frame_r
                self.looking_right = True
            else:
                self.image = self.jump_frame_l
                self.looking_right = False
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

        #show standing still animation
        if not self.jumping and not self.walking:
            bottom = self.rect.bottom
            if self.looking_right:
                self.image = self.standing_frame_r
            else:
                self.image = self.standing_frame_l
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
        
        #use masks for better collision detection with mobs
        self.mask = pg.mask.from_surface(self.image)
        

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, terrain):
        self.groups = game.all_sprites, game.platforms
        self._layer = platform_layer
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #all sprites for platforms
        #order will be grass, sand, stone, snow, castle
        images = [self.game.plat_spritesheet.get_image(648,0,70,70,1),
                  self.game.plat_spritesheet.get_image(360,792,70,70,1),
                  self.game.plat_spritesheet.get_image(144,648,70,70,1),
                  self.game.plat_spritesheet.get_image(288,144,70,70,1),
                  self.game.plat_spritesheet.get_image(288,792,70,70,1)]
        self.image = pg.Surface((w*70,70))
        for i in range(0,w):
            self.image.blit(images[terrain],(i*70,0))
        self.image.set_colorkey(black)
        #self.image.fill(green)
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

#mob coming from the side of the screen
class Bee(pg.sprite.Sprite):
    def __init__(self,game):
        self._layer = mob_layer
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image_up_r = self.game.enemy_spritesheet.get_image(315,353,56,48,1)
        self.image_down_r = self.game.enemy_spritesheet.get_image(140,23,61,42,1)
        self.image_up_l = pg.transform.flip(self.image_up_r,True,False)
        self.image_down_l = pg.transform.flip(self.image_down_r,True,False)
        self.image_up_r.set_colorkey(black)
        self.image_down_r.set_colorkey(black)
        self.image_up_l.set_colorkey(black)
        self.image_down_l.set_colorkey(black)
        self.spawn_location = random.choice([-80,width+80])
        if self.spawn_location > 0:
            self.image = self.image_up_r
            self.rect = self.image.get_rect()
            self.rect.centerx = self.spawn_location
        else:
            self.image = self.image_up_l
            self.rect = self.image.get_rect()
            self.rect.centerx = self.spawn_location           
        #will have different speeds
        self.velx = random.randrange(1,4)
        self.vely = 0
        if self.rect.centerx > width:
            self.velx *= -1
        #bee spawns somewhere under half screen
        self.rect.y = random.randrange(height/2)
        self.yacc = 0.5
    
    def update(self):
        self.rect.x += self.velx
        self.vely += self.yacc
        #so it bobs up and down
        if self.vely > 3 or self.vely < -3:
            self.yacc *= -1
        tempCenter = self.rect.center
        if self.yacc < 0:
            if self.spawn_location > 0:
                self.image = self.image_up_r
            else:
                self.image = self.image_up_l
        else:
            if self.spawn_location > 0:
                self.image = self.image_down_r
            else:
                self.image = self.image_down_l
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.center = tempCenter
        self.rect.y += self.vely


#mob coming from the bottom of the screen
class Bat(pg.sprite.Sprite):
    def __init__(self,game):
        self._layer = mob_layer
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image_up_r = self.game.enemy_spritesheet.get_image(71,235,70,47,1)
        self.image_down_r = self.game.enemy_spritesheet.get_image(0,0,88,37,1)
        self.image_up_l = pg.transform.flip(self.image_up_r,True,False)
        self.image_down_l = pg.transform.flip(self.image_down_r,True,False)
        self.image_up_r.set_colorkey(black)
        self.image_down_r.set_colorkey(black)
        self.image_up_l.set_colorkey(black)
        self.image_down_l.set_colorkey(black)
        self.spawn_location = random.choice([-60,width+60])
        if self.spawn_location > 0:
            self.image = self.image_up_r
            self.rect = self.image.get_rect()
            self.rect.centerx = self.spawn_location
        else:
            self.image = self.image_up_l
            self.rect = self.image.get_rect()
            self.rect.centerx = self.spawn_location 
        #will have different speeds
        self.velx = random.randrange(3,6)
        self.vely = 0
        if self.rect.centerx > width:
            self.velx *= -1
        #bee spawns somewhere under half screen
        self.rect.y = random.randrange(height/2)
        self.yacc = 0.5

    def update(self):
        self.rect.x += self.velx
        self.vely += self.yacc
        #so it bobs up and down
        if self.vely > 3 or self.vely < -3:
            self.yacc *= -1
        tempCenter = self.rect.center
        if self.yacc < 0:
            if self.spawn_location > 0:
                self.image = self.image_up_r
            else:
                self.image = self.image_up_l
        else:
            if self.spawn_location > 0:
                self.image = self.image_down_r
            else:
                self.image = self.image_down_l
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.center = tempCenter
        self.rect.y += self.vely
    

#Lives remaining
class Heart(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self._layer = player_layer
        self.groups = game.all_sprites, game.hearts
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = self.game.heart_spritesheet.get_image(0,94,53,45,1)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y