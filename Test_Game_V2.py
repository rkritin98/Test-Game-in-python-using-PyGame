import pygame
from pygame.locals import *
pygame.init()
#initiate pygame

win= pygame.display.set_mode((500,480)) #height and width

pygame.display.set_caption("Test Game")

#loading images of the playable character
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

#changing fps
clock = pygame.time.Clock()

#health of goblin
score = 0

#Music and sound effects
bulletSound = pygame.mixer.Sound('bullet.wav')
#to play bullet sound effect : bulletSound.play()
hitSound = pygame.mixer.Sound('hit.wav')

music = pygame.mixer.music.load('music.wav')
pygame.mixer.music.play(-1) #-1 means it plays cont even if the sound duration ends


"""       
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
"""

#initiate size of the character, position and velocity of movement
class player(object):
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width= width
        self.height= height
        self.vel = 5
        self.isJump=False
        self.jumpCount=10
        self.left= False
        self.right = False
        self.walkCount = 0
        self.jumpCount=10
        self.standing = True
        self.hitbox = (self.x+17 , self.y+11,29,52) #x,y,width,height
    def draw(self,win):
        #Insering playable human-like character
        if self.walkCount + 1 >= 27:
            self.walkCount=0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
            elif self.right:
                win.blit(walkRight[self.walkCount//3],(self.x,self.y))
                self.walkCount +=1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x,self.y))
            else:
                win.blit(walkLeft[0], (self.x,self.y))
        self.hitbox = (self.x+17 , self.y+11,29,52)
        #pygame.draw.rect(win, (255,0,0), self.hitbox ,2)
    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        #the above above code fixes a bug of respawning below the screen
        self.x = 60
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans',100)
        text = font1.render('-5',1,(255,0,0))
        win.blit(text, (250 - (text.get_width()/2),200))
        pygame.display.update()
        i=0
        while i<300:
            pygame.time.delay(10)
            i+=1
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    i=301
                    pygame.quit()


class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x=x
        self.y=y
        self.radius=radius
        self.color=color
        self.facing=facing
        self.vel= 8*facing
    
    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)


class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
    
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end=end
        self.path = [self.x, self.end]  # This will define where our enemy starts and finishes their path.
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x+17 , self.y+1,31,57)
        self.health =10
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible == True:
            if self.walkCount + 1 >= 33: # Since we have 11 images for each animtion our upper bound is 33. 
                                         # We will show each image for 3 frames. 3 x 11 = 33.
                self.walkCount = 0
                
            if self.vel > 0: # If we are moving to the right we will display our walkRight images
                win.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            else:  # Otherwise we will display the walkLeft images
                win.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0],self.hitbox[1]-20,50,10))
            pygame.draw.rect(win, (0,120,0), (self.hitbox[0],self.hitbox[1]-20,50- (5 * (10 - self.health)),10))
            self.hitbox = (self.x+17 , self.y+1,31,57)
            #pygame.draw.rect(win, (255,0,0), self.hitbox ,2)

    def move(self):
        if self.vel > 0:  # If we are moving right
            if self.x + self.vel< self.path[1]: # If we have not reached the furthest right point on our path.
                self.x += self.vel
            else: # Change direction and move back the other way
                self.vel = self.vel * -1
                self.walkCount = 0
        else: # If we are moving left
            if self.x - self.vel > self.path[0]: # If we have not reached the furthest left point on our path
                self.x += self.vel
            else:  # Change direction
                self.vel = self.vel * -1
                self.walkCount = 0


    def hit(self):
        if self.health >0:
            self.health -=1
        else:
            self.visible=False
        print('hit')
        

def redrawGameWindow():

    #win.fill((0,0,0))#if this statement is not present then you'll be drawing a red figure instead of moving it as a block,i.e you wouldnt be drawing over the old rectangle
    #background placement
    win.blit(bg, (0,0))

    text = font.render("Score: " + str(score),1 , (0,0,0))#text,antialias,color
    win.blit(text, (350,10))

    #creating and placing our character
    #pygame.draw.rect(win, (255,0,0),(x,y,width,height)) #rect(surface, color, rect)
    
    man.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    goblin.draw(win)
    pygame.display.update()



#main loop
font = pygame.font.SysFont('comicsans',30,True,False)#name,size,bold,italic
man = player(50,420,64,64)
bullets=[]
goblin = enemy(100,410,64,64,450)
shootLoop = 0
run = True
while run:
    clock.tick(27) #checks for condition in milli seconds 

    if goblin.visible ==True:
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]: #above the bottom of rect; below the top of rect
                if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0]+ goblin.hitbox[2]: #checks if we are in the right side of the left wall of the rect; checks if we are in the left of the right wall
                    man.hit()
                    score -=5
                    


    if shootLoop>0:
        shootLoop+=1
    if shootLoop>3:
        shootLoop=0


    #events are the movements like keyboard and mouse we do in a game
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #standard
            run = False

    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]: #above the bottom of rect; below the top of rect
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0]+ goblin.hitbox[2]: #checks if we are in the right side of the left wall of the rect; checks if we are in the left of the right wall
                hitSound.play()
                goblin.hit()
                score +=1
                bullets.pop(bullets.index(bullet))


        if bullet.x <500 and bullet.x>0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
    
    
    """
    top left coordiantes = (0,0)
    top right coordinated = (500,0)
    bottom left coordinates=(0,500)
    bottom right coordinates=(500,500)
    the character's coordinate is situated at the top left.
    """
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop==0:
        bulletSound.play()
        if man.left:
            facing=-1
        else:
            facing=1

        if len(bullets)<5:
            bullets.append(projectile(round(man.x + man.width//2),round(man.y+man.height//2),6,(255,0,0),facing))
        
        shootLoop=1

    
    if keys[pygame.K_LEFT] and man.x>man.vel :
        man.x -=man.vel
        man.left= True
        man.right=False
        man.standing= False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x+=man.vel
        man.left= False
        man.right= True
        man.standing= False
    else:
        man.walkCount=0
        man.standing=True

    if not(man.isJump):
        """
        if keys[pygame.K_UP] and y > vel :
            y-=vel

        if keys[pygame.K_DOWN] and y < 500 - height - vel:
            y+=vel
        """
        if keys[pygame.K_UP]:
            #parabolic movement. Using a Quadratic equation.
            man.isJump = True
            man.right=False
            man.left=False
            man.walkCount=0

    else:
        if man.jumpCount >= -10:
            neg=1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount**2) * 0.5 * neg
            man.jumpCount-=1
        else:
            man.isJump=False
            man.jumpCount=10
     

    #DONT DRAW OBJECTS IN MAIN FUNCTION
    redrawGameWindow()
pygame.quit()
