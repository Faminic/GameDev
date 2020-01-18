#will contain settings variables for game in general

#general game settings
title = "Have fun!"
width = 900
height = 750
fps = 60
font_name = "arial"
silver_coin_min = 50 #number of points needed to get silver coin
gold_coin_min = 100 #number of points needed to get gold coin
invincible_item_duration = 8000


#savefile settings
hsFile = "highscore.txt"


#spritesheet settings
player_spritesheet = "player_spritesheet.png"
platform_spritesheet = "platform_spritesheet.png"
enemy1_spritesheet = "enemies_spritesheet.png"
hud_spritesheet = "hud_spritesheet.png"
items_spritesheet = "items_spritesheet.png"



#colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
lightblue = (0,155,155)
bgcolor = lightblue


#player properties
player_acc = 0.5
player_friction = -0.12
player_gravity = 0.5
player_jump = 15 #jump height
player_invincible = 2500


#starting platforms -> all platforms that appear at the start of a level
#arguments are x,y,width,terrain
platform_list = [(0,height-60, 13),
                (width/2 - 150,height*3/4 - 50, 4),
                (width*3/4-100,height*0.5,3),
                (30,height-425,3),
                (475,150,4),
                (175,100,3)]


#platform spawn properties -> properties used when spawning new platforms
plat_width_min = 3
plat_width_max = 5


#platform terrain types
#order will be grass, sand, stone, snow, castle -> so if terrain = 0, then terrain is grass

#main menu text
main_menu_title = "Game Name - TBD"
main_menu_text1 = "Use left and right arrows to move"
main_menu_text2 = "Use space to jump"
main_menu_text3 = "Press any key to play"


#game over text
go_title = "Game Over"
go_text1 = "Final Score: "
go_text2 = "Highscore: "
go_text3 = "Press space to play again"
go_text4 = "Press any other key to return to the main menu"
go_hs_text = "NEW HIGH SCORE!!!"


#sound settings
jumpSound = "jump.wav"
mob_hit_sound = "hit.wav"
falling_sound = "fall.wav"
main_menu_bgmusic = "allthat.ogg"
go_bgmusic = "november.ogg"
stage_1_bgmusic = "jazzyfrenchy.ogg"


#mob spawn settings
bee_spawn = 6000 #every 6 seconds
bat_spawn = 8000 
barnacle_spawn = 40 #40/100 chance to spawn
spider_spawn = 5
mouse_spawn = 10


#layer settings -> order in which things appear on screen
player_layer = 4
item_layer = 3
mob_layer = 2
platform_layer = 1
background_layer = 0


#stage-specific settings

#stage 1 -> Palace Green
bee_spawn_1 = 5000 
bat_spawn_1 = 0 #in the code, you just pass
barnacle_spawn_1 = 20 
spider_spawn_1 = 0
mouse_spawn_1 = 0

heart_spawn_1 = 5
bomb_spawn_1 = 0
star_spawn_1 = 0

#stage 2 -> Snowy Durham
bee_spawn_2 = 5000 
bat_spawn_2 = 0 
barnacle_spawn_2 = 30 
spider_spawn_2 = 0
mouse_spawn_2 = 10

heart_spawn_2 = 5
bomb_spawn_2 = 5
star_spawn_2 = 5

#stage 3 -> Kingsgate Bridge
bee_spawn_3 = 8000 
bat_spawn_3 = 10000 
barnacle_spawn_3 = 20 
spider_spawn_3 = 0
mouse_spawn_3 = 15

heart_spawn_3 = 5
bomb_spawn_3 = 10
star_spawn_3 = 10

#stage 4 -> Cathedral
bee_spawn_4 = 10000 
bat_spawn_4 = 8000 
barnacle_spawn_4 = 10
spider_spawn_4 = 5
mouse_spawn_4 = 15

heart_spawn_4 = 10
bomb_spawn_4 = 15
star_spawn_4 = 10

#stage 5 -> Bill Bryson
bee_spawn_5 = 12000
bat_spawn_5 = 10000 
barnacle_spawn_5 = 10
spider_spawn_5 = 15
mouse_spawn_5 = 10

heart_spawn_5 = 15
bomb_spawn_5 = 20
star_spawn_5 = 10


#Level Selection Text
ls_instructions_title = "Advanced Instructions"
ls_instructions_text1 = "Aim is to collect two treasures hidden in each level while avoiding all enemies"
ls_instructions_text2 = "Treasure 1: A silver coin that appears after you reach a score of 50"
ls_instructions_text3 = "Treasure 2: A gold coin that appears after you reach a score of 100"

ls_instructions_text4 = "The following items may spawn: Extra Heart, Bomb to kill all"
ls_instructions_text5 = "enemies on screen and Star to be immune to enemies for 8 seconds"
ls_instructions_text6 = "You can exit the screen on the left and appear on the right and vice versa"
ls_instructions_text7 = "Higher levels are harder, so you are adivsed to complete them in order"
ls_instructions_text8 = "Once the gold coin is collected, the level is completed and you return to the main menu"
ls_instructions_text9 = "Collect 5 silver coins and 5 gold coins to find all 10 hidden treasures"

ls_title = "Level Selection"

ls1_title = "Level 1: Palace Green"
ls1_text = "Press 1 to start this level" 

ls2_title = "Level 2: Snowy Durham"
ls2_text = "Press 2 to start this level" 

ls3_title = "Level 3: Kingsgate Bridge"
ls3_text = "Press 3 to start this level" 

ls4_title = "Level 4: Durham Cathedral"
ls4_text = "Press 4 to start this level" 

ls5_title = "Level 5: Bill Bryson Library"
ls5_text = "Press 5 to start this level" 