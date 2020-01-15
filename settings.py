#will contain settings variables for game in general

#general game settings
title = "Have fun!"
width = 540
height = 760
fps = 60
font_name = "arial"

#colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)

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

