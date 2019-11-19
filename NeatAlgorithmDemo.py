import os

import pygame, math, neat, random
from random import randrange
from shapely.geometry import Polygon

pygame.init()

winWidth = 1300
winHeight = 710
STAT_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 70)
DRAW_LINES = False
WIN = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption("NEAT Algorithm demo")

win = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption("NEAT Genetic Algorithm Demo")
blueT = pygame.image.load('blueT.png')

gen = 0


class Player(object):
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.angle = angle
        self.vel = 7
        self.point = 0

        self.bullets = []
        self.pointX = self.x
        self.pointY = self.y
        self.pointOrigin = self.x
        self.redRGB = randrange(255)
        self.greenRGB = randrange(255)
        self.blueRGB = randrange(255)
        self.color = (self.redRGB, self.greenRGB, self.blueRGB)
        self.indanger = 0
        self.aiming = 0
        self.display = 1
        self.originalImage = blueT
        self.image = self.originalImage
        self.rect = self.image.get_rect()
        self.rectpoly = Polygon(
            [(self.x, self.y), (self.x + self.width, self.y), (self.x + self.width, self.y + self.height),
             (self.x, self.y + self.height)])
        self.hitbox = (self.x, self.y, self.width + 2, self.height + 2)  # NEW

    def polygon(self, win):
        self.point_list = []
        ang = math.radians(self.angle)  # i * 3.14159 / num_points + counter * 3.14159 / 60
        self.x1 = int(self.centerX + self.velX * 10)
        self.y1 = int(self.centerY + self.velY * 10)
        self.point_list.append((self.x1, self.y1))
        self.x2 = self.centerX + int(math.cos(ang - 0.1) * 500)
        self.y2 = self.centerY + int(-math.sin(ang - 0.1) * 500)
        self.point_list.append((self.x2, self.y2))
        self.x3 = self.centerX + int(math.cos(ang + 0.1) * 500)
        self.y3 = self.centerY + int(-math.sin(ang + 0.1) * 500)
        self.point_list.append((self.x3, self.y3))
        self.poly = Polygon([(self.x1, self.y1), (self.x2, self.y2), (self.x3, self.y3)])
        self.rectpoly = self.poly
        pygame.draw.polygon(win, self.color, self.point_list, 1)

    def shoot(self):
        if len(self.bullets) < 2:  # This will make sure we cannot exceed 5 bullets on the screen at once
            xorigin = int(self.centerX + self.velX * 10)
            yorigin = int(self.centerY + self.velY * 10)
            self.bullets.append(Projectile(xorigin, yorigin, 6, (self.color), self.angle))

    def move(self):
        self.x += self.velX
        self.y += self.velY

    def right(self):
        self.angle = (self.angle - 5) % 360
        self.updateImg()
        self.move()

    def left(self):
        self.angle = (self.angle + 5) % 360
        self.updateImg()
        self.move()

    def draw(self, win):
        self.centerX = self.x + self.width / 2
        self.centerY = self.y + self.height / 2
        self.velX = int(self.vel * math.cos(math.radians(self.angle)))
        self.velY = -int(self.vel * math.sin(math.radians(self.angle)))
        self.updateImg()
        win.blit(self.image, (int(self.x), int(self.y)))
        self.polygon(win)
        self.hitbox = (int(self.x), int(self.y), self.width + 2, self.height + 2)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)  # To draw the hit box around the tanks
        for bullet in self.bullets:
            bullet.draw(win)
        for bullet in self.bullets:
            if bullet.x >= winWidth or bullet.x < 0 or bullet.y > winHeight or bullet.y < 0:
                self.bullets.pop(self.bullets.index(bullet))  # This will remove the bullet if it is off the screen

    def updateImg(self):
        self.image = rot_center(self.originalImage, self.angle)

    def hit(self):  # This will display when the enemy is hit
        self.bullets.clear()
        self.point = self.point - 1

    def kills(self):
        self.point = self.point + 5

    def aim(self):
        self.aiming = 1
        self.point = self.point + 1

    def noaim(self):
        self.aiming = 0

    def danger(self):
        self.point = self.point - 1
        self.indanger = 1

    def notdanger(self):
        self.indanger = -1


class Projectile(object):
    def __init__(self, x, y, radius, color, angle):
        self.x = int(x)
        self.y = int(y)
        self.radius = radius
        self.color = color
        self.angle = angle
        self.velX = int(15 * math.cos(math.radians(angle)))
        self.velY = -int(15 * math.sin(math.radians(angle)))

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), int(self.radius), int(5))
        self.hitbox = (self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)  # NEW
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)  # To draw the hit box around the tanks
        self.x += self.velX  # Moves the bullet by its vel
        self.y += self.velY


def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def redrawGameWindow(win, players, gen):
    if gen == 0:
        gen = 1

    win.fill((0, 0, 0))
    for player in players:
        player.draw(win)

    # generations
    score_label = STAT_FONT.render("Gens: " + str(gen - 1), 1, (255, 255, 255))
    win.blit(score_label, (10, 10))

    # alive
    score_label = STAT_FONT.render("Alive: " + str(len(players)), 1, (255, 255, 255))
    win.blit(score_label, (10, 50))

    pygame.display.update()


def eval_genomes(genomes, config):
    global WIN, gen
    win = WIN
    gen += 1
    i = 0

    # p1 = Player(winWidth / 2, winHeight / 2, 0)

    nets = []
    players = []
    ge = []
    xi = 0
    for genome_id, genome in genomes:
        random_angle = randrange(360)
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        players.append(Player((winWidth / 4) * (xi % 4) + 75, (winHeight / 3) * (xi % 3) + 50, random_angle))
        xi = xi + 1
        ge.append(genome)

    clock = pygame.time.Clock()
    run = True
    while run and len(players) > 2:
        i = 1 + i
        redrawGameWindow(win, players, gen)
        clock.tick(30)

        keys = pygame.key.get_pressed()
        # player p1 move set
        '''
        if keys[pygame.K_UP]:  # up and down is for player only
            if p1.x > p1.velX and p1.x < winWidth - p1.width - p1.velX:
                p1.x += p1.velX
            if p1.y > p1.velY and p1.y < winHeight - p1.height - p1.velY:
                p1.y += p1.velY
        if keys[pygame.K_DOWN]:
            if p1.x > p1.velX and p1.x < winWidth - p1.width - p1.velX:
                p1.x -= p1.velX
            if p1.y > p1.velY and p1.y < winHeight - p1.height - p1.velY:
                p1.y -= p1.velY
        if keys[pygame.K_SPACE]:
            p1.shoot()
            print(len(players))'''
        if keys[pygame.K_TAB] or i % 240 == 0:  # or clock.get_ticks()>13000:
            print(len(players))
            run = False
            pygame.time.delay(200)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        for x, player in enumerate(players):  # give each bird a fitness of 0.1 for each frame it stays alive

            if player.x + 5 > player.velX and player.x < winWidth - player.width - player.velX:
                ge[x].fitness += 0.0
            else:
                ge[x].fitness -= 3
                player.left()
                if player.x > winWidth - player.width - player.velX:
                    player.x += -25
                else:
                    player.x += 25
            if player.y + 5 > player.velY and player.y < winHeight - player.height - player.velY:
                ge[x].fitness += 0.0
            else:
                ge[x].fitness -= 3
                player.right()
                if player.y > winHeight - player.height - player.velY:
                    player.y += -25
                else:
                    player.y += 25

            output = nets[players.index(player)].activate(
                (player.x, player.y, player.indanger, player.aiming))
            print(output, i)

            activation_turn = 0.5
            if output[0] < activation_turn and output[1] < activation_turn:
                ge[x].fitness -= 4
            if output[0] > activation_turn:
                player.right()
                ge[x].fitness += 0.05
            if output[1] > activation_turn:
                player.left()
                ge[x].fitness += 0.05
            if output[2] > 0.4:
                player.shoot()
                if player.aiming == 1:
                    ge[x].fitness += 6
                else:
                    ge[x].fitness -= 1

        for player in players:
            '''if p1.poly.intersects(player.rectpoly):
                player.danger()
                ge[players.index(player)].fitness -= .5
            else:
                player.notdanger()'''

            for playerT in players:
                if player.poly.intersects(playerT.rectpoly):
                    playerT.danger()
                    player.aim()
                    ge[players.index(player)].fitness += 4
                    ge[players.index(playerT)].fitness -= 4
                else:
                    playerT.notdanger()
                    player.noaim()

            '''for bullet in p1.bullets:
                if bullet.y - bullet.radius < player.hitbox[1] + player.hitbox[3] and bullet.y + bullet.radius > player.hitbox[1]:  # Checks x coords
                    if bullet.x + bullet.radius > player.hitbox[0] and bullet.x - bullet.radius < player.hitbox[0] + player.hitbox[2]:  # Checks y coords
                        p1.bullets.pop(p1.bullets.index(bullet))  # removes bullet from p1 bullet list
                        print(str(p1.color))
                        player.hit()
                        print(str(player.color))
                        ge[players.index(player)].fitness -= 5
                        nets.pop(players.index(player))
                        ge.pop(players.index(player))
                        players.pop(players.index(player))'''

            for bullet in player.bullets:
                for playerT in players:
                    if bullet.y - bullet.radius < playerT.hitbox[1] + playerT.hitbox[3] and bullet.y + bullet.radius > \
                            playerT.hitbox[1]:  # Checks x coords
                        if bullet.x + bullet.radius > playerT.hitbox[0] and bullet.x - bullet.radius < playerT.hitbox[
                            0] + \
                                playerT.hitbox[2]:  # Checks y coords

                            playerT.hit()
                            player.kills()
                            ge[players.index(player)].fitness += 14
                            ge[players.index(playerT)].fitness -= 4
                            nets.pop(players.index(playerT))
                            ge.pop(players.index(playerT))
                            players.pop(players.index(playerT))

        redrawGameWindow(win, players, gen)


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)
    p = neat.Population(config)

    # add reporter to show progress in terminal
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 1000)  # how many generations

    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "ConfigFile.txt")
    run(config_path)
