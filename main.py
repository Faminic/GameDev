import pygame as pg
import random
from settings import *
from sprites import *


class Game:
    #initializing the game window and so on
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((width,height))
        pg.display.set_caption(title)
        self.clock = pg.time.Clock()
        self.running = True

    #Start a new game
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group() #store all platforms here so we can do collisions easily
        self.player = Player()
        self.all_sprites.add(self.player)
        p1 = Platform(0,height-40, width, 40)
        self.all_sprites.add(p1)
        self.platforms.add(p1)
        p2 = Platform(width/2 - 50,height*3/4, 100, 20)
        self.all_sprites.add(p2)
        self.platforms.add(p2)
        self.run()

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
        #have player stand firmly on top of platform in case of collision
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            self.player.pos.y = hits[0].rect.top
            self.player.vel.y = 0 #if not 0, player would slowly fall through the platform

    #Deal with events for game
    def events(self):
        for event in pg.event.get():
            #check if window is closed
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
    
    #Draw the game
    def draw(self):
        self.screen.fill(black)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    #Show the start screen or main menu for game
    def show_start_screen(self):
        pass

    #Show game over screen
    def show_go_screen(self):
        pass


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()