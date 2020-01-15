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
        self.player = Player()
        self.all_sprites.add(self.player)
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