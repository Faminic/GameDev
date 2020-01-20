import pygame
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
#Item/Treasure Pickup Noise came from https://freesound.org/people/cabled_mess/sounds/350876/
#level 1 background music: https://www.bensound.com/royalty-free-music/track/jazzy-frenchy
#level 2 background music: https://www.bensound.com/royalty-free-music/track/a-new-beginning
#level 3 background music: https://www.bensound.com/royalty-free-music/track/going-higher
#level 4 background music: https://www.bensound.com/royalty-free-music/track/slow-motion
#level 5 background music: https://www.bensound.com/royalty-free-music/track/extreme-action
#main menu background music: https://www.bensound.com/royalty-free-music/track/november
#game over menu background music: https://www.bensound.com/royalty-free-music/track/all-that-chill-hop
#level cleared menu background music: https://www.bensound.com/royalty-free-music/track/funny-song

class Game:
    #initializing the game window and so on
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((width,height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True
        self.restart = False #will be true if player wants to return to main menu
        self.cleared = False #will be true if player has cleared a level
        #all level variables
        self.level1 = False
        self.level2 = False
        self.level3 = False
        self.level4 = False
        self.level5 = False
        #saved progress of treasures -> store these in a save file
        with open("treasures_cleared.txt") as f:
            treasures_cleared = [int(i) for i in f]
        if treasures_cleared[0] == 1:
            self.level1_silver = True
        else:
            self.level1_silver = False
        if treasures_cleared[1] == 1:
            self.level1_gold = True
        else:
            self.level1_gold = False
        if treasures_cleared[2] == 1:
            self.level2_silver = True
        else:
            self.level2_silver = False
        if treasures_cleared[3] == 1:
            self.level2_gold = True
        else:
            self.level2_gold = False
        if treasures_cleared[4] == 1:
            self.level3_silver = True
        else:
            self.level3_silver = False
        if treasures_cleared[5] == 1:
            self.level3_gold = True
        else:
            self.level3_gold = False
        if treasures_cleared[6] == 1:
            self.level4_silver = True
        else:
            self.level4_silver = False
        if treasures_cleared[7] == 1:
            self.level4_gold = True
        else:
            self.level4_gold = False
        if treasures_cleared[8] == 1:
            self.level5_silver = True
        else:
            self.level5_silver = False
        if treasures_cleared[9] == 1:
            self.level5_gold = True
        else:
            self.level5_gold = False
        #saved progress of highscores -> store these in a save file
        with open("highscore.txt") as f:
            highscores = [int(i) for i in f]
        self.highscore1 = highscores[0]
        self.highscore2 = highscores[1]
        self.highscore3 = highscores[2]
        self.highscore4 = highscores[3]
        self.highscore5 = highscores[4]
        self.platform_terrain = 0
        self.font_name = pygame.font.match_font(font_name)
        self.load_data()

    #Start a new game
    def new(self):
        self.score = 0
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.platforms = pygame.sprite.Group() #store all platforms here so we can do collisions easily
        self.mobs = pygame.sprite.Group() #store all the mobs
        self.hearts = pygame.sprite.Group() #stores all the hearts
        self.items = pygame.sprite.Group() #stores all the items
        self.treasure = pygame.sprite.Group() #stores all the treasure
        self.plat_spawn_counter = 0 #used to determine where platforms spawn
        self.mid_plat_height = 0
        self.left_plat_height = 0
        self.right_plat_height = 0
        self.bee_timer = 0
        self.bat_timer = 0
        self.invincible_timer = 0
        self.invincible = False
        self.invincible_timer_item = 0
        self.invincible_item = False
        self.numberOfHearts = 3
        self.player = Player(self)
        #adding all starting platforms
        for plat in platform_list:
            Platform(self,*plat,self.platform_terrain)
        for heart in range(self.numberOfHearts):
            Heart(self,53*(heart)+10,10)
        #choose correct highscore
        if self.level1:
            self.highscore = self.highscore1
            self.silver_acquired = self.level1_silver
            self.gold_acquired = self.level1_gold
            self.background = Background(self,"images/palace_green.jpg")
        elif self.level2:
            self.highscore = self.highscore2
            self.silver_acquired = self.level2_silver
            self.gold_acquired = self.level2_gold
            self.background = Background(self,"images/snowy_durham.jpg")
        elif self.level3:
            self.highscore = self.highscore3
            self.silver_acquired = self.level3_silver
            self.gold_acquired = self.level3_gold
            self.background = Background(self,"images/kingsgate_bridge.jpg")
        elif self.level4:
            self.highscore = self.highscore4
            self.silver_acquired = self.level4_silver
            self.gold_acquired = self.level4_gold
            self.background = Background(self,"images/durham_cathedral.jpg")
        elif self.level5:
            self.highscore = self.highscore5
            self.silver_acquired = self.level5_silver
            self.gold_acquired = self.level5_gold
            self.background = Background(self,"images/bill_bryson.jpg")
        self.run()

    #used to load all necessary data
    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, "images")
        #load player spritesheet
        self.spritesheet = Spritesheet(path.join(img_dir,player_spritesheet))
        #load platform spritesheet
        self.plat_spritesheet = Spritesheet(path.join(img_dir,platform_spritesheet))
        #load enemy spritesheet
        self.enemy_spritesheet = Spritesheet(path.join(img_dir,enemy1_spritesheet))
        #load heart spritesheet
        self.heart_spritesheet = Spritesheet(path.join(img_dir,hud_spritesheet))
        #load items spritesheet
        self.item_spritesheet = Spritesheet(path.join(img_dir,items_spritesheet))
        #load sounds
        self.sound_dir = path.join(self.dir, "sounds")
        self.jump_sound = pygame.mixer.Sound(path.join(self.sound_dir,jumpSound))
        self.hit_sound = pygame.mixer.Sound(path.join(self.sound_dir,mob_hit_sound))
        self.fall_sound = pygame.mixer.Sound(path.join(self.sound_dir,falling_sound))
        self.item_sound = pygame.mixer.Sound(path.join(self.sound_dir,item_sound))

    #Game Loop
    def run(self):
        self.playing = True
        volume_level = 0.3
        self.screen.fill(bgcolor)
        self.screen.blit(self.background.image,self.background.rect)
        if self.level1:
            pygame.mixer.music.load(path.join(self.sound_dir,stage_1_bgmusic))
            pygame.mixer.music.set_volume(volume_level)
            pygame.mixer.music.play(loops=-1)
        elif self.level2:
            pygame.mixer.music.load(path.join(self.sound_dir,stage_2_bgmusic))
            pygame.mixer.music.set_volume(volume_level)
            pygame.mixer.music.play(loops=-1)
        elif self.level3:
            pygame.mixer.music.load(path.join(self.sound_dir,stage_3_bgmusic))
            pygame.mixer.music.set_volume(volume_level)
            pygame.mixer.music.play(loops=-1)
        elif self.level4:
            pygame.mixer.music.load(path.join(self.sound_dir,stage_4_bgmusic))
            pygame.mixer.music.set_volume(volume_level)
            pygame.mixer.music.play(loops=-1)
        elif self.level5:
            pygame.mixer.music.load(path.join(self.sound_dir,stage_5_bgmusic))
            pygame.mixer.music.set_volume(volume_level)
            pygame.mixer.music.play(loops=-1)
        while self.playing:
            self.clock.tick(fps)
            self.events()
            self.update()
            self.draw()
        pygame.mixer.music.fadeout(500)
        
    def update_highscore_savefile(self):
        self.highscores=[self.highscore1,self.highscore2,self.highscore3,self.highscore4,self.highscore5]
        with open(path.join(self.dir, "highscore.txt"),'w') as f:
            for score in self.highscores:
                f.write(str(score)+"\n")

    def update_level_cleared_savefile(self):
        self.treasures_cleared=[int(self.level1_silver),int(self.level1_gold),int(self.level2_silver),int(self.level2_gold),int(self.level3_silver),int(self.level3_gold),int(self.level4_silver),int(self.level4_gold),int(self.level5_silver),int(self.level5_gold)]
        with open(path.join(self.dir, "treasures_cleared.txt"),'w') as f:
            for level in self.treasures_cleared:
                f.write(str(level)+"\n")

    #Update the game
    def update(self):
        self.all_sprites.update()
        #have player stand firmly on top of platform in case of collision (but only when player lands from top)
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
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
            for coin in self.treasure:
                coin.rect.y += max(abs(self.player.vel.y),2)
                if coin.rect.top >= height:
                    coin.kill()
            for item in self.items:
                item.rect.y += max(abs(self.player.vel.y),2)
                if item.rect.top >= height:
                    item.kill()

        #spawn new platforms to replace lost ones
        widthCutoff = width/3
        while len(self.platforms) < 7:
            platWidth = random.randrange(plat_width_min,plat_width_max)
            if self.plat_spawn_counter == 0:
                self.left_plat_height = random.randrange(-45,-30)
                Platform(self,random.randrange(self.plat_spawn_counter*widthCutoff,(self.plat_spawn_counter+1)*widthCutoff-(platWidth*70)),
                         self.left_plat_height,
                         platWidth,self.platform_terrain)
                self.plat_spawn_counter += 1
            elif self.plat_spawn_counter == 1:
                self.mid_plat_height = random.randrange(-45,-30)
                Platform(self,random.randrange(self.plat_spawn_counter*widthCutoff,(self.plat_spawn_counter+1)*widthCutoff-(platWidth*70)),
                         self.mid_plat_height,
                         platWidth,self.platform_terrain)
                self.plat_spawn_counter += 1
            elif self.plat_spawn_counter == 2:
                self.right_plat_height = random.randrange(-45,-30)
                Platform(self,random.randrange(self.plat_spawn_counter*widthCutoff,(self.plat_spawn_counter+1)*widthCutoff-(platWidth*70)),
                         self.right_plat_height,
                         platWidth,self.platform_terrain)
                self.plat_spawn_counter += 1
            else:
                Platform(self,random.randrange(widthCutoff,2*widthCutoff),
                         min(self.left_plat_height,self.mid_plat_height,self.right_plat_height) -30,
                         platWidth,self.platform_terrain)
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
        self.spawn_bees()

        #spawn bats
        self.spawn_bats()

        #break_invicibility
        invincible_now = pygame.time.get_ticks()
        if invincible_now - self.invincible_timer > player_invincible:
            self.invincible_timer = invincible_now
            self.invincible = False

        #break_invicibility from item
        invincible_now_item = pygame.time.get_ticks()
        if invincible_now_item - self.invincible_timer_item > invincible_item_duration:
            self.invincible_timer_item = invincible_now_item
            self.invincible_item = False
        
        #mob collision
        mob_hits = pygame.sprite.spritecollide(self.player, self.mobs, False)
        if mob_hits and not self.invincible and not self.invincible_item:
            #now do a mask collision to check if an actual collision occurred or if rectangles just overlapped
            mob_hits2 = pygame.sprite.spritecollide(self.player, self.mobs, False, pygame.sprite.collide_mask)
            if mob_hits2 and not self.invincible and not self.invincible_item:
                self.hit_sound.play()
                self.numberOfHearts -= 1
                for heart in self.hearts:
                    heart.kill()
                for heart in range(self.numberOfHearts):
                    Heart(self,53*(heart)+10,10)
                if self.numberOfHearts == 0:
                    self.playing = False
                self.invincible = True
        
        #item collision
        item_hits = pygame.sprite.spritecollide(self.player, self.items, False)
        if item_hits:
            self.item_sound.play()
            for item in item_hits:
                if item.rect.width == 70: #so it is a bomb
                    for mob in self.mobs:
                        mob.kill()
                if item.rect.width == 71: #so it is a star
                    self.invincible_item = True
                if item.rect.width == 53: #so it is a heart
                    self.numberOfHearts += 1
                    for heart in self.hearts:
                        heart.kill()
                    for heart in range(self.numberOfHearts):
                        Heart(self,53*(heart)+10,10)
                item.kill()
        
        #treasure collision
        treasure_hits = pygame.sprite.spritecollide(self.player, self.treasure, False)
        if treasure_hits:
            self.item_sound.play()
            if self.score < gold_coin_min:
                self.silver_acquired = True
            else:
                self.gold_acquired = True
            for coin in self.treasure:
                coin.kill()
        #if both treasures are secured, then level is cleared
        if self.level1:
            if self.silver_acquired and self.gold_acquired and not self.level1_silver and not self.level1_gold:
                self.cleared = True
                self.playing = False
        if self.level2:
            if self.silver_acquired and self.gold_acquired and not self.level2_silver and not self.level2_gold:
                self.cleared = True
                self.playing = False
        if self.level3:
            if self.silver_acquired and self.gold_acquired and not self.level3_silver and not self.level3_gold:
                self.cleared = True
                self.playing = False
        if self.level4:
            if self.silver_acquired and self.gold_acquired and not self.level4_silver and not self.level4_gold:
                self.cleared = True
                self.playing = False
        if self.level5:
            if self.silver_acquired and self.gold_acquired and not self.level5_silver and not self.level5_gold:
                self.cleared = True
                self.playing = False



    #Deal with events for game
    def events(self):
        for event in pygame.event.get():
            #check if window is closed
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                    
    
    #Draw the game
    def draw(self):
        self.screen.fill(bgcolor)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score),50,durham_color,width/2,15)
        #after drawing everything, flip the display
        pygame.display.flip()

    #Show the start screen or main menu for game
    def show_start_screen(self):
        pygame.mixer.music.load(path.join(self.sound_dir,main_menu_bgmusic))
        pygame.mixer.music.play(loops=-1)
        self.screen.fill(bgcolor)
        self.draw_text(main_menu_title, 48, white,width/2, height/4)
        self.draw_text(main_menu_text1, 22, white,width/2, height/2)
        self.draw_text(main_menu_text2, 22, white,width/2, height/2 + 50)
        self.draw_text(main_menu_text3, 22, white,width/2, height/2 + 100)
        pygame.display.flip()
        self.wait_for_key()

        if self.running: 
            self.screen.fill(bgcolor)
            self.draw_text(ls_title, 40, white,width/2, 20)
            self.draw_text(ls1_title, 20, white,width/4, 70)
            self.draw_text(ls1_text, 20, white,width/4, 100)
            if self.level1_silver and self.level1_gold:
                self.draw_text("(Level Cleared)", 20, white,width/4, 130)
            self.draw_text(ls2_title, 20, white,width*3/4, 70)
            self.draw_text(ls2_text, 20, white,width*3/4, 100)
            if self.level2_silver and self.level2_gold:
                self.draw_text("(Level Cleared)", 20, white,width*3/4, 130)
            self.draw_text(ls3_title, 20, white,width/4, 180)
            self.draw_text(ls3_text, 20, white,width/4, 210)
            if self.level3_silver and self.level3_gold:
                self.draw_text("(Level Cleared)", 20, white,width/4, 240)
            self.draw_text(ls4_title, 20, white,width*3/4, 180)
            self.draw_text(ls4_text, 20, white,width*3/4, 210)
            if self.level4_silver and self.level4_gold:
                self.draw_text("(Level Cleared)", 20, white,width*3/4, 240)
            self.draw_text(ls5_title, 20, white,width/2,290)
            self.draw_text(ls5_text, 20, white,width/2, 320)
            if self.level5_silver and self.level5_gold:
                self.draw_text("(Level Cleared)", 20, white,width/2, 350)

            self.draw_text(ls_instructions_title, 40, white,width/2, 400)
            self.draw_text(ls_instructions_text6, 20, white,width/2, 450)
            self.draw_text(ls_instructions_text1, 20, white,width/2, 480)
            self.draw_text(ls_instructions_text8, 20, white,width/2, 510)
            self.draw_text(ls_instructions_text2, 20, white,width/2, 540)
            self.draw_text(ls_instructions_text3, 20, white,width/2, 570)
            
            pygame.display.flip()
            self.ls_wait_for_key()

        pygame.mixer.music.fadeout(500)

        

    #Show game over screen
    def show_go_screen(self):
        #if player has quit during a level, then game over screen not needed
        if not self.running:
            return
        pygame.mixer.music.load(path.join(self.sound_dir,go_bgmusic))
        pygame.mixer.music.play(loops=-1)
        self.screen.fill(bgcolor)
        self.draw_text(go_title, 48, white,width/2, height/4)
        self.draw_text(str(go_text1) + str(self.score), 22, white,width/2, height/2)
        #update highscore if necessary
        if self.score > self.highscore:
            self.highscore = self.score
            if(self.level1):
                self.highscore1 = self.highscore
            elif(self.level2):
                self.highscore2 = self.highscore
            elif(self.level3):
                self.highscore3 = self.highscore
            elif(self.level4):
                self.highscore4 = self.highscore
            elif(self.level5):
                self.highscore5 = self.highscore
            self.update_highscore_savefile()
            self.draw_text(go_hs_text, 22, white,width/2, height/2 + 50)
        else:
            self.draw_text(str(go_text2) + str(self.highscore), 22, white,width/2, height/2 + 50)
        self.draw_text(go_text3, 22, white,width/2, height/2 + 100)
        self.draw_text(go_text4, 22, white,width/2, height/2 + 150)
        pygame.display.flip()
        self.wait_for_key()
        self.go_wait_for_key()
        pygame.mixer.music.fadeout(500)
    
    #Show level cleared screen
    def show_cleared_screen(self):
        pygame.mixer.music.load(path.join(self.sound_dir,lc_bgmusic))
        pygame.mixer.music.play(loops=-1)
        #need to update savefiles
        if self.level1:
            self.level1_silver = True
            self.level1_gold = True
        elif self.level2:
            self.level2_silver = True
            self.level2_gold = True
        elif self.level3:
            self.level3_silver = True
            self.level3_gold = True
        elif self.level4:
            self.level4_silver = True
            self.level4_gold = True
        elif self.level5:
            self.level5_silver = True
            self.level5_gold = True
        self.update_level_cleared_savefile()
        #update highscore if necessary
        if self.score > self.highscore:
            self.highscore = self.score
            if(self.level1):
                self.highscore1 = self.highscore
            elif(self.level2):
                self.highscore2 = self.highscore
            elif(self.level3):
                self.highscore3 = self.highscore
            elif(self.level4):
                self.highscore4 = self.highscore
            elif(self.level5):
                self.highscore5 = self.highscore
            self.update_highscore_savefile()
        self.screen.fill(bgcolor)
        self.draw_text(lc_title, 48, white,width/2, height/4)
        self.draw_text(lc_text1, 22, white,width/2, height/2)        
        self.draw_text(lc_text2, 22, white,width/2, height/2 + 100)
        pygame.display.flip()
        self.wait_for_key()
        self.wait_for_key()
        pygame.mixer.music.fadeout(500)
        self.show_start_screen()

    #generic function requiring player to press any key
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                if event.type == pygame.KEYUP:
                    waiting = False
    
    #"wait_for_key" method adapted for game over screen
    def go_wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.restart_levels()
                    self.running = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                    else:
                        self.restart = True
                        self.restart_levels()
                        self.playing = False
                        waiting = False    

    #level selection adapted wait for key
    def ls_wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_1:
                        self.restart_levels()
                        self.level1 = True
                        self.platform_terrain = 0
                        waiting = False
                    if event.key == pygame.K_2:
                        self.restart_levels()
                        self.level2 = True
                        self.platform_terrain = 1
                        waiting = False
                    if event.key == pygame.K_3:
                        self.restart_levels()
                        self.level3 = True
                        self.platform_terrain = 2
                        waiting = False
                    if event.key == pygame.K_4:
                        self.restart_levels()
                        self.level4 = True
                        self.platform_terrain = 3
                        waiting = False
                    if event.key == pygame.K_5:
                        self.restart_levels()
                        self.level5 = True
                        self.platform_terrain = 4
                        waiting = False
    
    def spawn_bees(self):
        if self.level1:
            bee_now = pygame.time.get_ticks()
            if bee_now - self.bee_timer > bee_spawn_1 + random.choice([-1000,-500,0,500,1000]):
                self.bee_timer = bee_now
                Bee(self)
        elif self.level2:
            bee_now = pygame.time.get_ticks()
            if bee_now - self.bee_timer > bee_spawn_2 + random.choice([-1000,-500,0,500,1000]):
                self.bee_timer = bee_now
                Bee(self)
        elif self.level3:
            bee_now = pygame.time.get_ticks()
            if bee_now - self.bee_timer > bee_spawn_3 + random.choice([-1000,-500,0,500,1000]):
                self.bee_timer = bee_now
                Bee(self)
        elif self.level4:
            bee_now = pygame.time.get_ticks()
            if bee_now - self.bee_timer > bee_spawn_4 + random.choice([-1000,-500,0,500,1000]):
                self.bee_timer = bee_now
                Bee(self)
        elif self.level5:
            bee_now = pygame.time.get_ticks()
            if bee_now - self.bee_timer > bee_spawn_5 + random.choice([-1000,-500,0,500,1000]):
                self.bee_timer = bee_now
                Bee(self)

    def spawn_bats(self):
        if self.level1:
            '''
            bat_now = pygame.time.get_ticks()
            if bat_now - self.bat_timer > bat_spawn_1 + random.choice([-1000,-500,0,500,1000]):
                self.bat_timer = bat_now
                Bat(self)
            '''
            pass
        if self.level2:
            '''
            bat_now = pygame.time.get_ticks()
            if bat_now - self.bat_timer > bat_spawn_2 + random.choice([-1000,-500,0,500,1000]):
                self.bat_timer = bat_now
                Bat(self)
            '''
            pass
        if self.level3:
            bat_now = pygame.time.get_ticks()
            if bat_now - self.bat_timer > bat_spawn_3 + random.choice([-1000,-500,0,500,1000]):
                self.bat_timer = bat_now
                Bat(self)
        if self.level4:
            bat_now = pygame.time.get_ticks()
            if bat_now - self.bat_timer > bat_spawn_4 + random.choice([-1000,-500,0,500,1000]):
                self.bat_timer = bat_now
                Bat(self)
        if self.level5:
            bat_now = pygame.time.get_ticks()
            if bat_now - self.bat_timer > bat_spawn_5 + random.choice([-1000,-500,0,500,1000]):
                self.bat_timer = bat_now
                Bat(self)
    
    #resetting all level variables
    def restart_levels(self):
        self.level1 = False
        self.level2 = False
        self.level3 = False
        self.level4 = False
        self.level5 = False
        self.platform_terrain = 0

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

newGame = Game()
newGame.show_start_screen()
while newGame.running:
    newGame.new()
    if newGame.cleared:
        newGame.cleared = False
        newGame.show_cleared_screen()
    else:
        newGame.show_go_screen()
    #so goes back to main screen if any key except space pressed in game over screen
    if newGame.restart:
        newGame.show_start_screen()
        newGame.restart = False

pygame.quit()