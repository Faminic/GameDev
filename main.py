import pygame as pg
import random
from settings import *
from sprites import *
from os import path

#The following resources were used when creating this game
#Sprite sheets from https://opengameart.org/content/platformer-art-complete-pack-often-updated
#YouTube Tutorial by https://www.youtube.com/watch?v=uWvb3QzA48c&list=PLsk-HSGFjnaG-BwZkuAOcVwWldfCLu1pq&index=1 to learn pygame fundamentals
#Jump Noise came from https://freesound.org/people/cabled_mess/sounds/350906/
#Fall Noise came from https://freesound.org/people/cabled_mess/sounds/371451/
#Hit Noise came from https://freesound.org/people/cabled_mess/sounds/350984/
#grass stage background music: https://www.bensound.com/royalty-free-music/track/jazzy-frenchy
#main menu background music: https://www.bensound.com/royalty-free-music/track/november
#game over background music: https://www.bensound.com/royalty-free-music/track/all-that-chill-hop

'''
To do after tutorial
- Add hearts
- Have warning for when bee/bat spawns
- Incorporate Levels
- Implement a reset all values function for level specific components
- Adjust how data is saved and read
- Reset all saved data before submission (or create a function that does it)
- Give the game a name and add it to the main/starting screen
- Change variable names and structure
- Test the game on the uni system
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
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group() #store all platforms here so we can do collisions easily
        self.mobs = pg.sprite.Group() #store all the mobs
        self.plat_spawn_counter = 0 #used to determine where platforms spawn
        self.mid_plat_height = 0
        self.left_plat_height = 0
        self.right_plat_height = 0
        self.bee_timer = 0
        self.bat_timer = 0
        self.player = Player(self)
        #adding all starting platforms
        for plat in platform_list:
            Platform(self,*plat)
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
        #load enemy spritesheet
        self.enemy_spritesheet = Spritesheet(path.join(img_dir,enemy1_spritesheet))
        #load sounds
        self.sound_dir = path.join(self.dir, "sounds")
        self.jump_sound = pg.mixer.Sound(path.join(self.sound_dir,jumpSound))
        self.hit_sound = pg.mixer.Sound(path.join(self.sound_dir,mob_hit_sound))
        self.fall_sound = pg.mixer.Sound(path.join(self.sound_dir,falling_sound))

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
                #need to first find lowest platform they collided with, since hits does not have it ordered
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                #make player fall off edge of platform
                if self.player.pos.x < lowest.rect.right +9 and self.player.pos.x > lowest.rect.left - 9:
                    #make player stand on platform
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top
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
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y),2)
                #now need to kill items that are pushed down
                if mob.rect.top >= height:
                    mob.kill()
        
        #spawn new platforms to replace lost ones
        widthCutoff = width/3
        while len(self.platforms) < 7:
            platWidth = random.randrange(plat_width_min,plat_width_max)
            if self.plat_spawn_counter == 0:
                self.left_plat_height = random.randrange(-55,-30)
                Platform(self,random.randrange(self.plat_spawn_counter*widthCutoff,(self.plat_spawn_counter+1)*widthCutoff-(platWidth*70)),
                         self.left_plat_height,
                         platWidth,0)
                self.plat_spawn_counter += 1
            elif self.plat_spawn_counter == 1:
                self.mid_plat_height = random.randrange(-55,-30)
                Platform(self,random.randrange(self.plat_spawn_counter*widthCutoff,(self.plat_spawn_counter+1)*widthCutoff-(platWidth*70)),
                         self.mid_plat_height,
                         platWidth,0)
                self.plat_spawn_counter += 1
            elif self.plat_spawn_counter == 2:
                self.right_plat_height = random.randrange(-55,-30)
                Platform(self,random.randrange(self.plat_spawn_counter*widthCutoff,(self.plat_spawn_counter+1)*widthCutoff-(platWidth*70)),
                         self.right_plat_height,
                         platWidth,0)
                self.plat_spawn_counter += 1
            else:

                Platform(self,random.randrange(widthCutoff,2*widthCutoff),
                         min(self.left_plat_height,self.mid_plat_height,self.right_plat_height) -30,
                         platWidth,0)
                self.plat_spawn_counter = 0
        
        #game over
        if self.player.rect.bottom > height:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.fall_sound.play()
            self.playing = False
        
        #spawn bees
        bee_now = pg.time.get_ticks()
        if bee_now - self.bee_timer > bee_spawn + random.choice([-1000,-500,0,500,1000]):
            self.bee_timer = bee_now
            Bee(self)
        #spawn bats
        bat_now = pg.time.get_ticks()
        if bat_now - self.bat_timer > bat_spawn + random.choice([-1000,-500,0,500,1000]):
            self.bat_timer = bat_now
            Bat(self)
        
        #mob collision
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False)
        if mob_hits:
            #now do a mask collision to check if an actual collision occurred or if rectangles just overlapped
            mob_hits2 = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask)
            if mob_hits2:
                self.hit_sound.play()
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
        self.draw_text(str(self.score),30,white,width/2,15)
        #after drawing everything, flip the display
        pg.display.flip()

    #Show the start screen or main menu for game
    def show_start_screen(self):
        pg.mixer.music.load(path.join(self.sound_dir,main_menu_bgmusic))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(bgcolor)
        self.draw_text(main_menu_title, 48, white,width/2, height/4)
        self.draw_text(main_menu_text1, 22, white,width/2, height/2)
        self.draw_text(main_menu_text2, 22, white,width/2, height/2 + 50)
        self.draw_text(main_menu_text3, 22, white,width/2, height/2 + 100)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    #Show game over screen
    def show_go_screen(self):
        #if player has quit during a level, then game over screen not needed
        if not self.running:
            return
        pg.mixer.music.load(path.join(self.sound_dir,go_bgmusic))
        pg.mixer.music.play(loops=-1)
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
        pg.mixer.music.fadeout(500)
        
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