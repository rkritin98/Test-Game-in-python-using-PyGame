import pygame
from pygame.locals import *
pygame.init()
#initiate pygame

win= pygame.display.set_mode((500,480)) #height and width

pygame.display.set_caption("First Game")

#loading images of the playable character
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

#changing fps
clock = pygame.time.Clock()

#initiate size of the character, position and velocity of movement

x=50
y=420
width = 64
height = 64
vel = 5

#Jump is pretty complicated but it uses quadratic equations concepts
isJump = False
jumpCount = 10

#as we input a character we need to know how much they have moved left or right to determine what frame we are showing
left = False
right = False
walkCount= 0

def redrawGameWindow():
    global walkCount

    #win.fill((0,0,0))#if this statement is not present then you'll be drawing a red figure instead of moving it as a block,i.e you wouldnt be drawing over the old rectangle
    #background placement
    win.blit(bg, (0,0))

    #creating and placing our character
    #pygame.draw.rect(win, (255,0,0),(x,y,width,height)) #rect(surface, color, rect)
    #Insering playable human-like character
    if walkCount + 1 >= 27:
        walkCount=0
    
    if left:
        win.blit(walkLeft[walkCount//3], (x,y))
        walkCount +=1
    elif right:
        win.blit(walkRight[walkCount//3],(x,y))
        walkCount +=1
    else:
        win.blit(char,(x,y))

    pygame.display.update()



#main loop
run = True
while run:
    clock.tick(27) #checks for condition in milli seconds 

    #events are the movements like keyboard and mouse we do in a game
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #standard
            run = False

    keys = pygame.key.get_pressed()
    """
    top left coordiantes = (0,0)
    top right coordinated = (500,0)
    bottom left coordinates=(0,500)
    bottom right coordinates=(500,500)
    the character's coordinate is situated at the top left.
    """
    if keys[pygame.K_LEFT] and x > vel:
        x -=vel
        left= True
        right=False
    elif keys[pygame.K_RIGHT] and x < 500 - width - vel:
        x+=vel
        left= False
        right= True
    else:
        right=False
        left=False
        walkCount=0

    if not(isJump):
        """
        if keys[pygame.K_UP] and y > vel :
            y-=vel

        if keys[pygame.K_DOWN] and y < 500 - height - vel:
            y+=vel
        """
        if keys[pygame.K_SPACE]:
            #parabolic movement. Using a Quadratic equation.
            isJump = True
            right=False
            left=False
            walkCount=0

    else:
        if jumpCount >= -10:
            neg=1
            if jumpCount < 0:
                neg = -1
            y -= (jumpCount**2) * 0.5 * neg
            jumpCount-=1
        else:
            isJump=False
            jumpCount=10
     

    #DONT DRAW OBJECTS IN MAIN FUNCTION
    redrawGameWindow()
pygame.quit()
