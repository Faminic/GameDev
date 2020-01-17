#will contain settings variables for game in general

#general game settings
title = "Have fun!"
width = 900
height = 750
fps = 60
font_name = "arial"


#savefile settings
hsFile = "highscore.txt"


#spritesheet settings
player_spritesheet = "player_spritesheet.png"
platform_spritesheet = "platform_spritesheet.png"
enemy1_spritesheet = "enemies_spritesheet.png"
hud_spritesheet = "hud_spritesheet.png"



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
platform_list = [(0,height-60, 13, 0),
                (width/2 - 150,height*3/4 - 50, 4, 1),
                (width*3/4-100,height*0.5,3,2),
                (30,height-425,3,3),
                (475,150,4,4),
                (175,100,3,0)]


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
barnacle_spawn = 20 #40/100 chance to spawn
spider_spawn = 5
mouse_spawn = 10


#layer settings -> order in which things appear on screen
player_layer = 3
mob_layer = 2
platform_layer = 1
background_layer = 0