import pygame
pygame.init()

winWidth = 500
winHeight = 500

win = pygame.display.set_mode((winWidth,winHeight))
pygame.display.set_caption("Have fun")

x = 50
y = 5
width = 50
height = 60
vel = 3

#jump variables
jumpHeight = 10
jumpHeightCopy = jumpHeight
isJump = False
startHeight = 0 #height from which you started jumping
jumpVel = 5 #jumping velocity

def redrawGameWindow():


run = True
while run:
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x > vel:
        x -= vel
    if keys[pygame.K_RIGHT] and x < winWidth - width - vel:
        x += vel
    
    if(not isJump):
        if keys[pygame.K_SPACE]:
            isJump = True
            startHeight = y
    else:

        # if keys[pygame.K_SPACE]:
        #     jumpHeight = jumpHeightCopy
                    
        if jumpHeight >= -jumpHeightCopy:
            neg = 1
            if jumpHeight < 0:
                neg = -1
            y -= (jumpVel**2)*0.5*neg
            jumpHeight -= 1
        elif(not y==startHeight):
            y -= (jumpVel**2)*0.5*neg
        else:
            isJump = False
            jumpHeight = 10
    
    win.fill((0,0,0))
    pygame.draw.rect(win, (255,0,0), (x,y,width,height))
    pygame.display.update()

pygame.quit()
