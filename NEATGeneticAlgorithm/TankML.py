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
        self.x2 = self.centerX + int(math.cos(ang - 0.1) * 400)
        self.y2 = self.centerY + int(-math.sin(ang - 0.1) * 400)
        self.point_list.append((self.x2, self.y2))
        self.x3 = self.centerX + int(math.cos(ang + 0.1) * 400)
        self.y3 = self.centerY + int(-math.sin(ang + 0.1) * 400)
        self.point_list.append((self.x3, self.y3))
        self.poly = Polygon([(self.x1, self.y1), (self.x2, self.y2), (self.x3, self.y3)])
        pygame.draw.polygon(win, self.color, self.point_list, 1)

    def shoot(self):
        if len(self.bullets) < 1:  # This will make sure we cannot exceed 5 bullets on the screen at once
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
        self.rectpoly = Polygon(
            [(self.x, self.y), (self.x + self.width, self.y), (self.x + self.width, self.y + self.height),
             (self.x, self.y + self.height)])
        self.centerX = int(self.x + self.width / 2)
        self.centerY = int(self.y + self.height / 2)
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

    def aim(self):
        self.aiming = 1

    def noaim(self):
        self.aiming = 0

    def danger(self):
        self.indanger = 1

    def notdanger(self):
        self.indanger = 0

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
    framerate = 30
    gen += 1
    i = 0
    max_time_per_gen = 300
    activation_turn = 0.7  # threshold to activate output
    nets = []
    players = []
    ge = []
    xi = 0
    for genome_id, genome in genomes:
        random_angle = randrange(360)
        random_pos = randrange(200)
        genome.fitness = 0  # start with fitness level of 0
        # net = neat.nn.FeedForwardNetwork.create(genome, config)
        net = neat.nn.recurrent.RecurrentNetwork.create(genome, config)
        nets.append(net)
        players.append(Player((winWidth / 4) * (xi % 4) + 75 + random_pos, (winHeight / 3) * (xi % 3) + 50 + random_pos,
                              random_angle))
        xi += 1
        ge.append(genome)

    clock = pygame.time.Clock()
    run = True
    while run and len(players) > 0:
        i = 1 + i
        redrawGameWindow(win, players, gen)
        clock.tick(framerate)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]: # change framerate
            if framerate == 30:
                framerate = 60
            else:
                framerate = 30
            pygame.time.delay(200)
        if keys[pygame.K_TAB] or i % max_time_per_gen == 0:  # or clock.get_ticks()>13000:
            print(len(players))
            # maybe
            nets.clear()
            ge.clear()
            players.clear()
            run = False
            pygame.time.delay(200)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        for x, player in enumerate(players):  # give each player a fitness of 0.1 for each frame it stays alive

            output = nets[players.index(player)].activate(
                (player.indanger, player.aiming, player.angle))  # inputs
            # print(output)
            if output[0] < activation_turn and output[1] < activation_turn and output[2] < activation_turn:  # if not moving fitness is reduced
                ge[x].fitness -= 0.00001
            if output[0] > activation_turn:
                player.right()
                ge[x].fitness += 0.00
            if output[1] > activation_turn:
                player.left()
                ge[x].fitness += 0.00
            if output[2] > 0.5:
                player.shoot()
                if player.aiming == 1:
                    ge[x].fitness += 0.00001
                else:
                    ge[x].fitness -= 0.0
            if player.x + 5 > player.velX and player.x < winWidth - player.width - player.velX:
                ge[players.index(player)].fitness += 0.0
            else:
                if player.x > winWidth - player.width - player.velX:
                    player.x += -25
                else:
                    player.x += 25
            if player.y + 5 > player.velY and player.y < winHeight - player.height - player.velY:
                ge[players.index(player)].fitness += 0.0
            else:
                if player.y > winHeight - player.height - player.velY:
                    player.y += -25
                else:
                    player.y += 25
            for playerT in players:
                if player.poly.intersects(playerT.rectpoly):
                    playerT.danger()
                    player.aim()
                    ge[players.index(player)].fitness += 0.0
                    ge[players.index(playerT)].fitness -= 0.0
                else:
                    playerT.notdanger()
                    player.noaim()
                for bullet in player.bullets:
                    if bullet.y - bullet.radius < playerT.hitbox[1] + playerT.hitbox[
                        3] and bullet.y + bullet.radius > \
                            playerT.hitbox[1]:  # Checks x coords
                        if bullet.x + bullet.radius > playerT.hitbox[0] and bullet.x - bullet.radius < \
                                playerT.hitbox[
                                    0] + \
                                playerT.hitbox[2]:  # Checks y coords
                            playerT.hit()
                            ge[players.index(player)].fitness += 1
                            ge[players.index(playerT)].fitness -= 1
                            nets.pop(players.index(playerT))
                            ge.pop(players.index(playerT))
                            players.pop(players.index(playerT))

        redrawGameWindow(win, players, gen)

def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 5000)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)

