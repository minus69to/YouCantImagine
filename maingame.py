import math
import snaker
import random
import sys
import dxball
import menu
from subprocess import call
import pygame

screenwidth = 800
screenheight = 600

points = 0
gamespeed = 15
font = pygame.font.Font('freesansbold.ttf', 20)

lifes = 3
def score():
    global points, gamespeed
    points+=1
    if points % 100 == 0:
        gamespeed+=2
    text = font.render("Points: "+str(points), True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.topleft = (10,10)
    text2 = font.render("Lives: "+str(lifes),True, (0,0,0))
    text2Rect = text2.get_rect()
    text2Rect.topleft = (700,10)
    screen.blit(text,textRect)
    screen.blit(text2, text2Rect)
    print()
clock = pygame.time.Clock()
j = 0

pygame.init()


class backgroundpoint:
    x = 0
    y = 0


class runningPlayer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.playerImg = [pygame.image.load("runnig1-removebg-preview.png").convert_alpha(),
                          pygame.image.load("runnig2-removebg-preview.png").convert_alpha(),pygame.image.load("runnig3-removebg-preview.png").convert_alpha(),pygame.image.load("runnig4-removebg-preview.png").convert_alpha(),pygame.image.load("runnig5-removebg-preview.png").convert_alpha()]
        self.index = 0
        for i in self.playerImg:
            i = pygame.transform.scale(i,(85,158))
        self.image = self.playerImg[self.index]
        self.image.set_colorkey((0,0,0,0))
        self.image = pygame.transform.scale(self.image, (85, 158))

        self.rect = self.image.get_rect()
        self.playerx = 250
        self.playery = 400
        self.rect.topleft = [self.playerx, self.playery]
        #print(self.image.get_colorkey())
        self.jumping = False
        self.down = False
        self.ygrav = 2
        self.jheight = 30
        self.yval = self.jheight

    def update(self, x, y):
        if (x):
            self.jumping = x
        elif (y):
            self.down = y
        if self.jumping:
            self.playery -= self.yval
            self.yval -= self.ygrav
            if self.yval < - self.jheight:
                self.jumping = False
                self.yval = self.jheight
            self.image = pygame.image.load("runnig4-removebg-preview.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (85,158))
            self.image.set_colorkey((0, 0, 0, 0))
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.playerx, self.playery]
            self.index = 0
        else:
            self.index += 1
            if self.index == 5:
                self.index = 0
            self.image = self.playerImg[self.index].convert_alpha()
            self.image = pygame.transform.scale(self.image , (85,158))
            self.image.set_colorkey((0, 0, 0, 0))

    def inPress(self):
        if (self.jumping):
            return self.playery >= 250
    def destroy(self):
        self.kill()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.playerImg = [pygame.image.load("snake1.jpg").convert_alpha(),
                          pygame.image.load("snake2.jpg").convert_alpha(),
                          pygame.image.load("snakes3.jpg").convert_alpha()]
        self.index = 0
        for i in self.playerImg:
            i.set_colorkey((255, 255, 255, 0))
        self.image = self.playerImg[self.index]
        # self.image = pygame.transform.scale(self.image,(50,20))
        self.rect = self.image.get_rect()
        self.rect.x = screenwidth
        self.rect.y = 700

    def update(self):
        self.rect.x -= 5
        self.index += 1
        if (self.index > 2):
            self.index = 0
        if self.rect.x < -self.rect.width:
            self.kill()


snakes = []
balls = []
coins = []
walls = []
class SnakeO:
    def __init__(self):
        self.playerImg = [pygame.image.load("snake1.jpg").convert_alpha(),
                          pygame.image.load("snake2.jpg").convert_alpha(),
                          pygame.image.load("snake3.jpg").convert_alpha(),
                          pygame.image.load("snake4.jpg").convert_alpha(),
                         ]
        self.index = 0
        #for i in self.playerImg:
        #    i.set_colorkey((0, 0, 0, 0))
        self.image = self.playerImg[self.index]
        self.image = pygame.transform.scale(self.image, (200, 50))
        self.rect = self.image.get_rect()
        self.rect.x = screenwidth
        self.rect.y = 510
        self.sound = pygame.mixer.Sound('snake_hiss.mp3')

    def update(self):
        self.sound.play()
        # clock.tick(15)
        self.rect.x -= gamespeed
        #print(self.index)
        self.index += 1
        if (self.index >= 4):
            self.index = 0
        self.image = self.playerImg[self.index]
        self.image = pygame.transform.scale(self.image, (4 * 50, 2 * 20 + 10))
        #self.image.set_colorkey((0, 0, 0, 0))
        if (self.rect.x < -self.rect.width):
            snakes.pop()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Ball:
    def __init__(self):
        self.image = pygame.image.load('bomb1.jpg')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.image.set_colorkey((255,255,255,0))
        self.rect.x=screenwidth
        self.rect.y= random.randint(0,4)*50
        self.yval = 2*math.ceil(gamespeed/10)
        self.ygrav = 1*math.ceil(gamespeed/10)
        self.jumping = True
        self.stay = False
    def update(self):
        self.rect.x-=gamespeed
        if self.stay:
            if(self.rect.x<10):
                balls.pop()
        elif self.jumping:
            self.rect.y-=self.yval
            self.yval-=self.ygrav
            if(self.rect.y<=300):
                self.jumping = False
        else:
            self.rect.y += self.yval
            self.yval += self.ygrav
            if(self.rect.y>=450):
                x, y = self.rect.x,self.rect.y
                self.jumping = False
                self.stay = True
                self.image = pygame.image.load('blast.jpg')
                self.image = pygame.transform.scale(self.image, (100, 100))
                self.rect = self.image.get_rect()
                y+=10
                self.rect.x,self.rect.y=x,y
                self.image.set_colorkey((255, 255, 255, 0))
                self.draw(screen)
                #balls.pop()
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Coin:
    def __init__(self):
        self.image = pygame.image.load('coin.png')
        self.image = pygame.transform.scale(self.image,(50,50))
        self.rect = self.image.get_rect()

        self.rect.x = screenwidth
        self.rect.y = 500
    def update(self):
        self.rect.x -= gamespeed
        if(self.rect.x<0):
            coins.pop()
    def draw(self, screen):
        screen.blit(self.image,self.rect)
screen = pygame.display.set_mode((screenwidth, screenheight))
runningplayer_group = pygame.sprite.Group()
runningplayer = runningPlayer()
runningplayer_group.add(runningplayer)
running = False

bg = pygame.image.load('lastbag.jpg').convert()
bg = pygame.transform.scale(bg, (screenwidth, screenheight))
bg_width = bg.get_width()

xpos = 0
ypos = 0

class Walls():
    def __init__(self):
        self.image = pygame.image.load('wall.jpg')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()

        self.rect.x = screenwidth
        self.rect.y = 500

    def update(self):
        self.rect.x -= gamespeed
        if (self.rect.x < 0):
            walls.pop()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

def background():
    global xpos, ypos
    img_width = bg.get_width()
    screen.blit(bg, (xpos, ypos))
    screen.blit(bg, (xpos + img_width, ypos))
    if xpos <= -img_width:
        screen.blit(bg, (xpos + img_width, ypos))
        xpos = 0
    xpos -= gamespeed
pos = 0
indx = 0
# while True:
#     background()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#             sys.exit()
#     pygame.display.update()
#     clock.tick(30)
#
#
def main():
    global running, runningplayer, runningplayer_group, lifes
    if not running:
        runningplayer_group = pygame.sprite.Group()
        runningplayer = runningPlayer()
        runningplayer_group.add(runningplayer)
        running = True
    clock.tick(30)
    global pos, snakes, balls, coins, points, walls
    jumper = False
    down = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if (pygame.key.get_pressed()[pygame.K_SPACE]):
        jumper = True
        down = False
    elif (pygame.key.get_pressed()[pygame.K_DOWN]):
        jumper = False
        down = True
    elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
        running = False
        runningplayer.destroy()
        pos=0
        snakes =[]
        coins = []
        balls = []
        points = 0
    else:
        jumper = False
        down = False
    background()
    # pygame.display.update()
    runningplayer_group.draw(screen)
    runningplayer_group.update(jumper, down)
    if len(snakes) == 0 and len(balls) == 0 and len(coins) == 0:
        x = random.randint(0,2)
        if x == 0 :
            snakes.append(SnakeO())
        elif x == 1 :
            coins.append(Coin())
        else:
            balls.append(Ball())


    for snake in snakes:
        snake.draw(screen)
        snake.update()
        x, y =runningplayer.rect.topleft
        if runningplayer.rect.colliderect(snake.rect):
        # if runningplayer.rect.x>=snake.rect.x and runningplayer.rect.x<=snake.rect.x+snake.rect.width:
        #     if runningplayer.rect.y>snake.rect.y-snake.rect.width:
             pos = 3
             lifes-= 1
             break
             #sys.exit()
    for snake in balls:
        snake.draw(screen)
        snake.update()
        if runningplayer.rect.colliderect(snake.rect):
            pos = 2
            break
    for coin in coins:
        coin.draw(screen)
        coin.update()
        if runningplayer.rect.colliderect(coin.rect):
            points+=1000
            coins.remove(coin)
            #sys.exit()

    for coin in walls:
        coin.draw(screen)
        coin.update()
        if runningplayer.rect.colliderect(coin.rect):
            points-=1000
            walls.remove(coin)

    if pos == 2 or pos == 3:
        balls = []
        snakes = []
        coins = []
    score()
    pygame.display.update()
    pygame.display.flip()

    clock.tick(30)
dx = dxball.DxBall()
sk = snaker.Snake()
mm = menu.Menu()
inds = 0
indm = 0
def dxball1():
    global indx, pos, dx
    if(dx.endgame()):
        pos = 1
        indx = 0
    if indx==0:

        dx = dxball.DxBall()
        indx = 1
    dx.run()
def snakers():
    global inds, pos, sk

    if inds == 0:
        sk = snaker.Snake()
        inds = 1

    if(sk.gameend()):
        pos = 1
        #print("HAla")
        inds = 0

    sk.run()
def mainMenu():
    global  indm, pos, mm
    global running, runningplayer, runningplayer_group, lifes
    if indm == 0:
        mm = menu.Menu()
        indm = 1
    if(mm.getMenu()):
        pos = 1
        indm = 0
    mm.run()


while True:
    if lifes == 0:
        sys.exit()
        running = False
        runningplayer.destroy()
        pos = 0
        snakes = []
        coins = []
        balls = []
        points = 0
    if pos == 0:
        mainMenu()
    elif pos == 1:
        main()
    elif pos == 2:
        dxball1()
    elif pos == 3:
        snakers()


