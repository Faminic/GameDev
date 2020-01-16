import pygame as pg
import random
from settings import *
from sprites import *
from os import path

'''
To do after tutorial
- Make game wider
- Incorporate Levels
- Adjust how data is saved and read
- Reset all saved data before submission (or create a function that does it)
- Give the game a name and add it to the main/starting screen
'''

class Game:
    #initializing the game window and so on
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((width,height))
        pg.display.set_caption(title)
        self.clock = pg.time.Clock()
        self.running = True
        self.restart = False #will be true if player wants to return to main menu
        self.font_name = pg.font.match_font(font_name)
        self.load_data()

    #Start a new game
    def new(self):
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group() #store all platforms here so we can do collisions easily
        self.player = Player(self)
        self.all_sprites.add(self.player)
        #adding all starting platforms
        for plat in platform_list:
            p = Platform(self,*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    #used to load all necessary data
    def load_data(self):
        #load high score
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, "images")
        with open(path.join(self.dir,hsFile), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        #load player spritesheet
        self.spritesheet = Spritesheet(path.join(img_dir,player_spritesheet))
        #load platform spritesheet
        self.plat_spritesheet = Spritesheet(path.join(img_dir,platform_spritesheet))

    #Game Loop
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(fps)
            self.events()
            self.update()
            self.draw()

    #Update the game
    def update(self):
        self.all_sprites.update()
        #have player stand firmly on top of platform in case of collision (but only when player lands from top)
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.rect.midbottom = self.player.pos
                self.player.vel.y = 0 #if not 0, player would slowly fall through the platform
    
        #want to adjust camera when player reaches top
        if self.player.rect.top <= round(height /4):
            #pushing the player and items on screen down == moving the camera upwards
            self.player.pos.y += max(abs(self.player.vel.y),2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y),2)
                #now need to kill items that are pushed down
                if plat.rect.top >= height:
                    plat.kill()
                    self.score += 1
        
        #spawn new items to replace lost ones
        while len(self.platforms) < 10:
            platWidth = random.randrange(plat_width_min,plat_width_max)
            p = Platform(self,random.randrange(0,width-(platWidth*70)),
                         random.randrange(-75,-30),
                         platWidth,0)
            self.platforms.add(p)
            self.all_sprites.add(p)
        
        #game over
        if self.player.rect.bottom > height:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

    #Deal with events for game
    def events(self):
        for event in pg.event.get():
            #check if window is closed
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
    
    #Draw the game
    def draw(self):
        self.screen.fill(bgcolor)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.draw_text(str(self.score),30,white,width/2,15)

        #after drawing everything, flip the display
        pg.display.flip()

    #Show the start screen or main menu for game
    def show_start_screen(self):
        self.screen.fill(bgcolor)
        self.draw_text(main_menu_title, 48, white,width/2, height/4)
        self.draw_text(main_menu_text1, 22, white,width/2, height/2)
        self.draw_text(main_menu_text2, 22, white,width/2, height/2 + 50)
        self.draw_text(main_menu_text3, 22, white,width/2, height/2 + 100)
        pg.display.flip()
        self.wait_for_key()

    #Show game over screen
    def show_go_screen(self):
        #if player has quit during a level, then game over screen not needed
        if not self.running:
            return
        self.screen.fill(bgcolor)
        self.draw_text(go_title, 48, white,width/2, height/4)
        self.draw_text(str(go_text1) + str(self.score), 22, white,width/2, height/2)
        #update highscore if necessary
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text(go_hs_text, 22, white,width/2, height/2 + 50)
            #update file
            with open(path.join(self.dir, hsFile),'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text(str(go_text2) + str(self.highscore), 22, white,width/2, height/2 + 50)
        self.draw_text(go_text3, 22, white,width/2, height/2 + 100)
        self.draw_text(go_text4, 22, white,width/2, height/2 + 150)
        pg.display.flip()
        self.go_wait_for_key()
        
    #generic function requiring player to press any key
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    waiting = False
                if event.type == pg.KEYUP:
                    waiting = False
    
    #"wait_for_key" method adapted for game over screen
    def go_wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    if event.key == pg.K_SPACE:
                        waiting = False
                    else:
                        self.restart = True
                        self.playing = False
                        waiting = False       

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()
    #so goes back to main screen if any key except space pressed in game over screen
    if g.restart:
        g.show_start_screen()
        g.restart = False

pg.quit()