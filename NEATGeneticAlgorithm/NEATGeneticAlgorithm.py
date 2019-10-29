
import pygame, math
from random import randrange
pygame.init()

winWidth=1300
winHeight=710

win = pygame.display.set_mode((winWidth,winHeight))
pygame.display.set_caption("NEAT Genetic Algorithm Demo")
blueT= pygame.image.load('blueT.png')

class Player(object):
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.width =50
        self.height=50
        self.angle=angle
        self.vel=7

        self.bullets= []
        self.pointX=self.x
        self.pointY=self.y
        self.pointOrigin=self.x
        self.redRGB=randrange(255)
        self.greenRGB=randrange(255)
        self.blueRGB=randrange(255)
        self.color = (self.redRGB, self.greenRGB, self.blueRGB) 
        
        self.display=1
        self.originalImage=blueT
        self.image= self.originalImage
        self.rect = self.image.get_rect()
        self.hitbox = (self.x , self.y , self.width+2, self.height+2) # NEW

    def polygon(self, win):#its lines now
        point_list = []
        ang = math.radians(self.angle) #i * 3.14159 / num_points + counter * 3.14159 / 60
        x = self.centerX + int(math.cos(ang) )
        y = self.centerY + int(-math.sin(ang) )
        point_list.append((x, y))
        x = self.centerX + int(math.cos(ang-0.1)*500 )
        y = self.centerY + int(-math.sin(ang-0.1)*500 )
        point_list.append((x, y))
        x = self.centerX + int(math.cos(ang+0.1)*500 )
        y = self.centerY + int(-math.sin(ang+0.1)*500 )
        point_list.append((x, y))
        pygame.draw.lines(win, self.color, True, point_list)

    def shoot(self):
        if len(self.bullets) < 5:  # This will make sure we cannot exceed 5 bullets on the screen at once
            xorigin=int(self.centerX + self.velX*10)
            yorigin=int(self.centerY + self.velY*10)
            self.bullets.append(Projectile(xorigin, yorigin, 6, (self.color), self.angle)) 

    def move(self):
        if self.x+5 > self.velX and self.x < winWidth-self.width-self.velX:
            self.x += self.velX
        else:
            if self.x > winWidth-self.width-self.velX:
                self.x += -25
            else:
                self.x += 25
        if self.y+5 > self.velY and self.y < winHeight-self.height-self.velY:
            self.y += self.velY 
        else:
            if self.y > winHeight-self.height-self.velY:
                self.y += -25
            else:
                self.y += 25
       
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
        self.polygon(win)
        self.hitbox = (self.x , self.y , self.width+2, self.height+2)
        pygame.draw.rect(win, (255,0,0), self.hitbox,2) # To draw the hit box around the tanks
        for bullet in self.bullets:
            bullet.draw(win)
        for bullet in self.bullets:
            if bullet.x >= winWidth or bullet.x < 0 or bullet.y > winHeight or bullet.y <0:
                self.bullets.pop(self.bullets.index(bullet))  # This will remove the bullet if it is off the screen

    def updateImg(self):
        self.image = rotCenter(self.originalImage,self.angle)

    def hit(self):  # This will display when the enemy is hit
        self.bullets.clear()
        print('hit')

class Projectile(object):
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
        self.hitbox = (self.x-self.radius , self.y-self.radius , self.radius*2, self.radius*2) # NEW
        pygame.draw.rect(win, (255,0,0), self.hitbox,2) # To draw the hit box around the tanks
        self.x += self.velX  # Moves the bullet by its vel
        self.y += self.velY

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
    p1.draw(win)
    for player in players:
        player.draw(win)
    
    pygame.display.update()


p1 =Player(winWidth/2,winHeight/2,0)
players= []
for x in range(12):
    players.append(Player((winWidth/4)*(x%4)+75,(winHeight/3)*(x%3)+50,0))

run = True
while run:
    pygame.time.delay(40)
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
            print(len(players))
    
    for player in players:#random move generator
        randomMove=randrange(3)
        if randomMove==0:
            player.shoot()
        if randomMove==1:
            player.left()
        if randomMove==2:
            player.right()

        for bullet in p1.bullets:
            if bullet.y - bullet.radius < player.hitbox[1] + player.hitbox[3] and bullet.y + bullet.radius > player.hitbox[1]: # Checks x coords
                    if bullet.x + bullet.radius > player.hitbox[0] and bullet.x - bullet.radius < player.hitbox[0] + player.hitbox[2]: # Checks y coords
                        p1.bullets.pop(p1.bullets.index(bullet)) # removes bullet from p1 bullet list
                        print(str(p1.color))
                        player.hit() 
                        print(str(player.color))
                        players.pop(players.index(player))

        for bullet in player.bullets:
            for playerT in players:
                if bullet.y - bullet.radius < playerT.hitbox[1] + playerT.hitbox[3] and bullet.y + bullet.radius > playerT.hitbox[1]: # Checks x coords
                        if bullet.x + bullet.radius > playerT.hitbox[0] and bullet.x - bullet.radius < playerT.hitbox[0] + playerT.hitbox[2]: # Checks y coords
                            player.bullets.remove(bullet) # removes bullet from players[0] bullet list
                            print(str(player.color))
                            playerT.hit() 
                            print(str(playerT.color))
                            players.pop(players.index(playerT))

pygame.quit()