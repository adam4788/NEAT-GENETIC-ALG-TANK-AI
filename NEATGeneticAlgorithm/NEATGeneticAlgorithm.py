
import pygame, math
from random import randrange
pygame.init()

winWidth=1300
winHeight=710

win = pygame.display.set_mode((winWidth,winHeight))
pygame.display.set_caption("NEAT Genetic Algorithm Demo")
blueT= pygame.image.load('blueT.png')

class Player(object):
    def __init__(self, x, y, width, height, angle):
        self.x = x
        self.y = y
        self.width =width
        self.height=height
        self.angle=angle
        self.vel=7

        self.bullets= []
        
        self.display=1
        self.originalImage=blueT
        self.image= self.originalImage
        self.rect = self.image.get_rect()

    def shoot(self):
        if len(self.bullets) < 5:  # This will make sure we cannot exceed 5 bullets on the screen at once
            xorigin=int(self.centerX + math.cos(math.radians(p1.angle)*(self.width + 300 )))
            yorigin=int(self.centerY + math.sin(math.radians(p1.angle)*(self.height + 300 )))
            self.bullets.append(projectile(xorigin, yorigin, 6, (255,255,255), self.angle)) 

    def move(self):
        if self.x+5 > self.velX and self.x < winWidth-self.width-self.velX:
            self.x += self.velX
        else:
            if self.x > winWidth-self.width-self.velX:
                self.x += -10
            else:
                self.x += 10
        if self.y+5 > self.velY and self.y < winHeight-self.height-self.velY:
            self.y += self.velY 
        else:
            if self.y > winHeight-self.height-self.velY:
                self.y += -10
            else:
                self.y += 10
       
    def right(self):
        self.angle =(self.angle - 5) % 360
        self.updateImg()
        self.move()

    def left(self):
        self.angle =(self.angle + 5) % 360
        self.updateImg()
        self.move()


    def draw(self, win):
        self.centerX=self.x+self.width/2
        self.centerY=self.y+self.height/2
        self.velX=int(self.vel * math.cos(math.radians(self.angle)))
        self.velY=-int(self.vel * math.sin(math.radians(self.angle)))
        win.blit(self.image, (self.x, self.y))
        for bullet in self.bullets:
            if bullet.x < winWidth and bullet.x > 0 and bullet.y < winHeight and bullet.y >0:
                bullet.x += bullet.velX  # Moves the bullet by its vel
                bullet.y += bullet.velY
            else:
                self.bullets.pop(self.bullets.index(bullet))  # This will remove the bullet if it is off the screen
        for bullet in self.bullets:
            bullet.draw(win)

    def updateImg(self):
        self.image = rotCenter(self.originalImage,self.angle)
        

class projectile(object):
    def __init__(self,x,y,radius,color,angle):
        self.x = int(x)
        self.y = int(y)
        self.radius = radius
        self.color = color
        self.angle = angle
        self.velX = int(15 * math.cos(math.radians(angle)))
        self.velY = -int(15 * math.sin(math.radians(angle)))


    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x, self.y), int(self.radius), int(5))

def rotCenter(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
    
def redrawGameWindow():
    win.fill((0,0,0))
    for bullet in bullets:
        bullet.draw(win)
    p1.draw(win)
    for player in players:
        player.draw(win)
    
    pygame.display.update()


p1 =Player(winWidth/2,winHeight/2,50,50,0)
players= []
for x in range(12):
    players.append(Player((winWidth/4)*(x%4)+75,(winHeight/3)*(x%3)+50,50,50,0))
    print(players[x].y)
run = True
bullets= []
while run:
    pygame.time.delay(50)
    redrawGameWindow()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] :
        p1.left()

    if keys[pygame.K_RIGHT] :
        p1.right()

    if keys[pygame.K_UP] : #up and down is for player only
        if p1.x > p1.velX and p1.x < winWidth-p1.width-p1.velX:
            p1.x += p1.velX
        if p1.y > p1.velY and p1.y < winHeight-p1.height-p1.velY:
            p1.y += p1.velY 
    if keys[pygame.K_DOWN] :
       if p1.x > p1.velX and p1.x < winWidth-p1.width-p1.velX:
            p1.x -= p1.velX
       if p1.y > p1.velY and p1.y < winHeight-p1.height-p1.velY:
            p1.y -= p1.velY

    if keys[pygame.K_SPACE]:
            p1.shoot()
    
    for player in players:
        randomMove=randrange(3)
        if randomMove==0:
            player.shoot()
        if randomMove==1:
            player.left()
        if randomMove==2:
            player.right()
    

    

pygame.quit()