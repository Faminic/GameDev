# Will contain all sprite classes for my game
import pygame
from settings import *
import random
vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self,game):
        self.groups = game.all_sprites
        self._layer = player_layer
        pygame.sprite.Sprite.__init__(self,self.groups)
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
        self.rect.center = (50, height-50)
        self.pos = vec(50, height-50)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    
    #load animations
    def load_images(self):
        scaleBy = 1.5
        self.standing_frame_r = self.game.spritesheet.get_image(67,190,66,92,scaleBy)
        self.standing_frame_l = pygame.transform.flip(self.standing_frame_r,True,False)
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
            self.walk_frames_l.append(pygame.transform.flip(frame,True,False))
        self.jump_frame_r = self.game.spritesheet.get_image(438,93,67,94,scaleBy)
        self.jump_frame_l = pygame.transform.flip(self.jump_frame_r,True,False)
        self.jump_frame_r.set_colorkey(black)
        self.jump_frame_l.set_colorkey(black)
        
    
    def jump(self):
        # jump only if standing on a platform -> do that by checking if there is a collision 1 pixel below
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, self.game.platforms,False)
        self.rect.y += -2
        if hits:
            self.game.jump_sound.play()
            self.vel.y = -player_jump

    def update(self):
        #do animations
        self.animate()
        self.acc = vec(0,player_gravity) #gravity basically pulls you down
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -player_acc
        if keys[pygame.K_RIGHT]:
            self.acc.x = player_acc
        
        #apply friction
        #on ice level, player slides more
        if(self.game.level2):
            self.acc.x += self.vel.x * icy_player_friction
        else:
            self.acc.x += self.vel.x * player_friction
        #on kingsgate bridge, player pushed to the left by sidewind
        if(self.game.level3):
            self.pos.x += player_sidewind
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
        now = pygame.time.get_ticks()
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
        self.mask = pygame.mask.from_surface(self.image)
        

class Platform(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, terrain):
        self.groups = game.all_sprites, game.platforms
        self._layer = platform_layer
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #all sprites for platforms
        #order will be grass, sand, stone, snow, castle
        images = [self.game.plat_spritesheet.get_image(648,0,70,70,1),
                  self.game.plat_spritesheet.get_image(288,144,70,70,1),
                  self.game.plat_spritesheet.get_image(288,792,70,70,1),
                  self.game.plat_spritesheet.get_image(360,792,70,70,1),
                  self.game.plat_spritesheet.get_image(144,648,70,70,1)]
        self.image = pygame.Surface((w*70,70))
        for i in range(0,w):
            self.image.blit(images[terrain],(i*70,0))
        self.image.set_colorkey(black)
        #self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        #spawn treasures
        if self.game.score > silver_coin_min and not self.game.silver_acquired:
            Treasure(self.game,self)
        elif self.game.score > gold_coin_min and not self.game.gold_acquired:
            Treasure(self.game,self)

        if self.game.level1:
            if random.randrange(100) < barnacle_spawn_1:
                Barnacle(self.game,self)
            if random.randrange(100) < spider_spawn_1:
                Spider(self.game,self)
            if random.randrange(100) < mouse_spawn_1:
                Mouse(self.game,self)
            if random.randrange(100) < bomb_spawn_1:
                Bomb(self.game,self)
            if random.randrange(100) < heart_spawn_1:
                HeartItem(self.game,self)
            if random.randrange(100) < star_spawn_1:
                Star(self.game,self)

        if self.game.level2:
            if random.randrange(100) < barnacle_spawn_2:
                Barnacle(self.game,self)
            if random.randrange(100) < spider_spawn_2:
                Spider(self.game,self)
            if random.randrange(100) < mouse_spawn_2:
                Mouse(self.game,self)
            if random.randrange(100) < bomb_spawn_2:
                Bomb(self.game,self)
            if random.randrange(100) < heart_spawn_2:
                HeartItem(self.game,self)
            if random.randrange(100) < star_spawn_2:
                Star(self.game,self)

        if self.game.level3:
            if random.randrange(100) < barnacle_spawn_3:
                Barnacle(self.game,self)
            if random.randrange(100) < spider_spawn_3:
                Spider(self.game,self)
            if random.randrange(100) < mouse_spawn_3:
                Mouse(self.game,self)
            if random.randrange(100) < bomb_spawn_3:
                Bomb(self.game,self)
            if random.randrange(100) < heart_spawn_3:
                HeartItem(self.game,self)
            if random.randrange(100) < star_spawn_3:
                Star(self.game,self)

        if self.game.level4:
            if random.randrange(100) < barnacle_spawn_4:
                Barnacle(self.game,self)
            if random.randrange(100) < spider_spawn_4:
                Spider(self.game,self)
            if random.randrange(100) < mouse_spawn_4:
                Mouse(self.game,self)
            if random.randrange(100) < bomb_spawn_4:
                Bomb(self.game,self)
            if random.randrange(100) < heart_spawn_4:
                HeartItem(self.game,self)
            if random.randrange(100) < star_spawn_4:
                Star(self.game,self)

        if self.game.level5:
            if random.randrange(100) < barnacle_spawn_5:
                Barnacle(self.game,self)
            if random.randrange(100) < spider_spawn_5:
                Spider(self.game,self)
            if random.randrange(100) < mouse_spawn_5:
                Mouse(self.game,self)
            if random.randrange(100) < bomb_spawn_5:
                Bomb(self.game,self)
            if random.randrange(100) < heart_spawn_5:
                HeartItem(self.game,self)
            if random.randrange(100) < star_spawn_5:
                Star(self.game,self)
        

#class for loading and dealing with spritesheets
class Spritesheet:
    def __init__(self,filename):
        self.spritesheet = pygame.image.load(filename).convert()
    
    #have multiple images in spritesheet, so this function helps get a specific image out
    def get_image(self,x,y,width,height,scaleBy):
        image = pygame.Surface((width,height))
        image.blit(self.spritesheet,(0,0),(x,y,width,height))
        #scale it appropriately
        image = pygame.transform.scale(image, (round(width/scaleBy),round(height/scaleBy)))
        return image

#mob coming from the side of the screen
class Bee(pygame.sprite.Sprite):
    def __init__(self,game):
        self._layer = mob_layer
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image_up_r = self.game.enemy_spritesheet.get_image(315,353,56,48,1)
        self.image_down_r = self.game.enemy_spritesheet.get_image(140,23,61,42,1)
        self.image_up_l = pygame.transform.flip(self.image_up_r,True,False)
        self.image_down_l = pygame.transform.flip(self.image_down_r,True,False)
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
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = tempCenter
        self.rect.y += self.vely


#mob coming from the bottom of the screen
class Bat(pygame.sprite.Sprite):
    def __init__(self,game):
        self._layer = mob_layer
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image_up_r = self.game.enemy_spritesheet.get_image(71,235,70,47,1)
        self.image_down_r = self.game.enemy_spritesheet.get_image(0,0,88,37,1)
        self.image_up_l = pygame.transform.flip(self.image_up_r,True,False)
        self.image_down_l = pygame.transform.flip(self.image_down_r,True,False)
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
        self.velx = random.randrange(3,5)
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
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = tempCenter
        self.rect.y += self.vely
    

#Lives remaining
class Heart(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self._layer = player_layer
        self.groups = game.all_sprites, game.hearts
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = self.game.heart_spritesheet.get_image(0,94,53,45,1)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Barnacle(pygame.sprite.Sprite):
    def __init__(self,game,plat):
        self._layer = mob_layer
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.plat = plat
        self.image1 = self.game.enemy_spritesheet.get_image(318,239,51,57,1)
        self.image2 = self.game.enemy_spritesheet.get_image(528,220,51,58,1)
        self.image1.set_colorkey(black)
        self.image2.set_colorkey(black)
        self.spawn_location = random.randrange(self.plat.rect.left+50,self.plat.rect.right-50)
        self.image = self.image1
        self.rect = self.image.get_rect()
        self.rect.centerx = self.spawn_location      
        self.vely = 0
        self.rect.bottom = self.plat.rect.top
        self.yacc = 0.5
    
    def update(self):
        self.vely += self.yacc
        #so it bobs up and down
        if self.vely > 3 or self.vely < -3:
            self.yacc *= -1
        tempCenter = self.rect.center
        if self.yacc < 0:
            self.image = self.image2
        else:
            self.image = self.image1
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = tempCenter


class Spider(pygame.sprite.Sprite):
    def __init__(self,game,plat):
        self._layer = mob_layer
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.plat = plat
        self.image_walk_l = self.game.enemy_spritesheet.get_image(0,90,72,51,1)
        self.image_walk_l2 = self.game.enemy_spritesheet.get_image(0,37,77,53,1)
        self.image_walk_r = pygame.transform.flip(self.image_walk_l,True,False)
        self.image_walk_r2 = pygame.transform.flip(self.image_walk_l2,True,False)
        self.image_walk_l.set_colorkey(black)
        self.image_walk_l2.set_colorkey(black)
        self.image_walk_r.set_colorkey(black)
        self.image_walk_r2.set_colorkey(black)
        self.spawn_location = self.plat.rect.centerx
        self.image = self.image_walk_r
        self.rect = self.image.get_rect()
        self.rect.centerx = self.spawn_location   
        self.rect.bottom = self.plat.rect.top   
        #will have different speeds
        self.velx = random.randrange(2,4)
        self.vely = 0
        self.yacc = 0.5
    
    def update(self):
        self.rect.x += self.velx
        self.vely += self.yacc
        #change direction
        if self.rect.centerx > self.plat.rect.right - 50:
            self.velx *= -1
        if self.rect.centerx < self.plat.rect.left + 50:
            self.velx *= -1
        #animations
        if self.vely > 3 or self.vely < -3:
            self.yacc *= -1
        tempCenter = self.rect.center
        if self.yacc < 0:
            if self.velx > 0:
                self.image = self.image_walk_r2
            else:
                self.image = self.image_walk_l2
        else:
            if self.velx > 0:
                self.image = self.image_walk_r
            else:
                self.image = self.image_walk_l
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = tempCenter


class Mouse(pygame.sprite.Sprite):
    def __init__(self,game,plat):
        self._layer = mob_layer
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.plat = plat
        self.image_walk_l = self.game.enemy_spritesheet.get_image(197,475,59,35,1)
        self.image_walk_l2 = self.game.enemy_spritesheet.get_image(256,475,58,35,1)
        self.image_walk_r = pygame.transform.flip(self.image_walk_l,True,False)
        self.image_walk_r2 = pygame.transform.flip(self.image_walk_l2,True,False)
        self.image_walk_l.set_colorkey(black)
        self.image_walk_l2.set_colorkey(black)
        self.image_walk_r.set_colorkey(black)
        self.image_walk_r2.set_colorkey(black)
        self.spawn_location = self.plat.rect.centerx
        self.image = self.image_walk_r
        self.rect = self.image.get_rect()
        self.rect.centerx = self.spawn_location   
        self.rect.bottom = self.plat.rect.top   
        #will have different speeds
        self.velx = random.randrange(1,3)
        self.vely = 0
        self.yacc = 0.5
    
    def update(self):
        self.rect.x += self.velx
        self.vely += self.yacc
        #change direction
        if self.rect.centerx > self.plat.rect.right - 40:
            self.velx *= -1
        if self.rect.centerx < self.plat.rect.left + 40:
            self.velx *= -1
        #animations
        if self.vely > 3 or self.vely < -3:
            self.yacc *= -1
        tempCenter = self.rect.center
        if self.yacc < 0:
            if self.velx > 0:
                self.image = self.image_walk_r2
            else:
                self.image = self.image_walk_l2
        else:
            if self.velx > 0:
                self.image = self.image_walk_r
            else:
                self.image = self.image_walk_l
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = tempCenter

class Treasure(pygame.sprite.Sprite):
    def __init__(self,game,plat):
        self._layer = player_layer
        self.groups = game.all_sprites, game.treasure
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.plat = plat
        self.image_silver = self.game.item_spritesheet.get_image(288,288,70,70,1)
        self.image_gold = self.game.item_spritesheet.get_image(288,360,70,70,1)
        self.image_silver.set_colorkey(black)
        self.image_gold.set_colorkey(black)
        self.spawn_location = self.plat.rect.centerx
        if(self.game.score >= gold_coin_min):
            self.image = self.image_gold
        else:
            self.image = self.image_silver
        self.rect = self.image.get_rect()
        self.rect.centerx = self.spawn_location   
        self.rect.bottom = self.plat.rect.top - 2

class Bomb(pygame.sprite.Sprite):
    def __init__(self,game,plat):
        self._layer = item_layer
        self.groups = game.all_sprites, game.items
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.plat = plat
        self.image = self.game.item_spritesheet.get_image(432,432,70,70,1)
        self.image.set_colorkey(black)
        self.spawn_location = self.plat.rect.centerx
        self.rect = self.image.get_rect()
        self.rect.centerx = self.spawn_location
        self.rect.bottom = self.plat.rect.top - 2

class HeartItem(pygame.sprite.Sprite):
    def __init__(self,game,plat):
        self._layer = item_layer
        self.groups = game.all_sprites, game.items
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.plat = plat
        self.image = self.game.heart_spritesheet.get_image(0,94,53,45,1)
        self.image.set_colorkey(black)
        self.spawn_location = self.plat.rect.centerx
        self.rect = self.image.get_rect()
        self.rect.centerx = self.spawn_location
        self.rect.bottom = self.plat.rect.top - 2

class Star(pygame.sprite.Sprite):
    def __init__(self,game,plat):
        self._layer = item_layer
        self.groups = game.all_sprites, game.items
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.plat = plat
        self.image = self.game.item_spritesheet.get_image(504,288,71,70,1)
        self.image.set_colorkey(black)
        self.spawn_location = self.plat.rect.centerx
        self.rect = self.image.get_rect()
        self.rect.centerx = self.spawn_location
        self.rect.bottom = self.plat.rect.top - 2


class Background(pygame.sprite.Sprite):
    def __init__(self,game,file):
        self._layer = background_layer
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0