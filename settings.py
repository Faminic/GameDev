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
#spritesheet below comes from https://opengameart.org/content/platformer-art-complete-pack-often-updated
player_spritesheet = "player_spritesheet.png"



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
platform_list = [(0,height-60, width, 60),
                (width/2 - 50,height*3/4, 100, 20),
                (width*3/4,height*0.5,70,20),
                (125,height-350,100,20),
                (350,200,100,20),
                (175,100,50,20)]


#platform spawn properties -> properties used when spawning new platforms
plat_width_min = 0.1*width
plat_width_max = 0.2*width


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
