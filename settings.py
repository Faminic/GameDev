#will contain settings variables for game in general

#general game settings
title = "Have fun!"
width = 540
height = 760
fps = 60
font_name = "arial"


#savefile settings
hsFile = "highscore.txt"


#spritesheet settings
player_spritesheet = "player_spritesheet.png"
platform_spritesheet = "platform_spritesheet.png"
enemy1_spritesheet = "enemies_spritesheet.png"



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


#starting platforms -> all platforms that appear at the start of a level
#arguments are x,y,width,terrain
platform_list = [(0,height-60, 8, 0),
                (width/2 - 100,height*3/4 - 50, 3, 1),
                (width*3/4,height*0.5,2,2),
                (30,height-475,2,3),
                (350,200,1,4),
                (175,100,1,0)]


#platform spawn properties -> properties used when spawning new platforms
plat_width_min = 1
plat_width_max = 3


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
bee_spawn = 5000 #every 5 seconds


#layer settings -> order in which things appear on screen
player_layer = 3
mob_layer = 2
platform_layer = 1