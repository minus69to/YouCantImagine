import math
import random
import sys

import pygame


screenwidth = 800
screenheight = 600

clock=pygame.time.Clock()
j = 0
pygame.init()
class backgroundpoint:
    x=0
    y=0

class runningPlayer(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.playerImg = [pygame.image.load("player4.jpg").convert_alpha(), pygame.image.load("player4.jpg").convert_alpha()]
            self.index=0
            self.playerImg[0].set_colorkey((255,0,0,0))
            self.playerImg[1].set_colorkey((255,0,0,0))
            self.image = self.playerImg[self.index]
            self.rect=self.image.get_rect()
            self.playerx = 250
            self.playery = 250
            self.rect.topleft=[self.playerx,self.playery]
            self.jumping = False
            self.down=False
            self.ygrav = 2
            self.jheight = 30
            self.yval = self.jheight

        def update(self, x,y):
            if(x):
                self.jumping = x
                print(x)
            elif (y):
                self.down=y
            if self.jumping:
                print(x, self.playery, self.yval)

                self.playery-=self.yval
                self.yval-=self.ygrav
                if self.yval < - self.jheight:
                    self.jumping = False
                    self.yval = self.jheight
                self.image=pygame.image.load('player1.jpg')
                self.rect = self.image.get_rect()
                self.rect.topleft = [self.playerx, self.playery]
                self.index = 0

            elif self.down:
                self.image = pygame.image.load('player4.jpg')
                self.rect = self.image.get_rect()
                self.rect.topleft = [self.playerx, self.playery]
                self.index = 0
                print("Here")
                self.down = False
            else:
                self.index += 1
                if self.index == 2:
                    self.index = 0
                self.image = self.playerImg[self.index]
        def inPress(self):
            if(self.jumping):
                return self.playery>=250

class backgroundtry(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.backgroundimage=[pygame.image.load("7.jpeg"), pygame.image.load("28.jpeg"), pygame.image.load("3.jpeg"), pygame.image.load(
            "2.jpeg"), pygame.image.load("5.jpeg"), pygame.image.load("6.jpeg"), pygame.image.load(
            "1.jpeg"), pygame.image.load("8.jpeg")]
        self.backindex = 0
        self.m=0
        self.background=[backgroundpoint() for i in range(8)]
        for rbg in self.background:
            rbg.x += self.m
            self.m += 138
        self.backspeed = 15
        for i in range(0,8):
            self.image = self.backgroundimage[i]
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.background[i].x,self.background[i].y]
    def change(self):
            self.backindex+=1
            self.background[self.backindex].x = self.background[self.backindex].x - self.backspeed
            if self.background[self.backindex].x < 0:
                self.background[self.backindex].x=screenwidth
    def change2(self):
            self.change()
            print("yes")
            self.image = self.backgroundimage[self.backindex]
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.background[self.backindex].x, self.background[self.backindex].y]
    def update(self):
        self.backindex += 1
        if self.backindex >= 8:
            self.backindex = 0
        self.background[self.backindex].x = self.background[self.backindex].x - self.backspeed
        if self.background[self.backindex].x < 0:
            self.background[self.backindex].x = screenwidth

        self.image = self.backgroundimage[self.backindex]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.background[self.backindex].x, self.background[self.backindex].y]

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.playerImg = [pygame.image.load("snake1.jpg").convert_alpha(), pygame.image.load("snake2.jpg").convert_alpha(), pygame.image.load("snakes3.jpg").convert_alpha()]
        self.index = 0
        print("sdaf")
        for i in self.playerImg:
            i.set_colorkey((255, 255, 255, 0))
        self.image =self.playerImg[self.index]
        #self.image = pygame.transform.scale(self.image,(50,20))
        self.rect = self.image.get_rect()
        self.rect.x = screenwidth
        self.rect.y = 700
    def update(self):
        self.rect.x -=5
        print("sdada")
        self.index += 1
        if(self.index>2):
            self.index = 0
        if self.rect.x< -self.rect.width:
            self.kill()
        #    obstacles.pop()
            print()
snakes = []
class SnakeO:
    def __init__(self):
        self.playerImg = [pygame.image.load("snake1.jpg").convert_alpha(),
                          pygame.image.load("snake2.jpg").convert_alpha(),
                          pygame.image.load("snakes3.jpg").convert_alpha()]
        self.index = 0
        print("sdaf")
        for i in self.playerImg:
            i.set_colorkey((255, 255, 255, 0))
        self.image = self.playerImg[self.index]
        self.image = pygame.transform.scale(self.image, (200,50))
        self.rect = self.image.get_rect()
        self.rect.x = screenwidth
        self.rect.y = 360
    def update(self):
        self.rect.x -= 15
        print(self.index)
        self.index += 1
        if (self.index > 2):
            self.index = 0
        self.image = self.playerImg[self.index]
        self.image = pygame.transform.scale(self.image, (4  *50,2*20+10        ))

        if(self.rect.x< -self.rect.width):
            snakes.pop()
    def draw(self, screen):
        screen.blit(self.image, self.rect)

screen = pygame.display.set_mode((1000, 440))
runningplayer_group=pygame.sprite.Group()
runningplayer=runningPlayer()
runningplayer_group.add(runningplayer)

obstacle_group = pygame.sprite.Group()
#runningbackground_group=pygame.sprite.Group()
#runningbackground=backgroundtry()
#runningbackground_group.add(runningbackground)
#runningbackground_group.draw(screen)
running = True

bg = pygame.image.load('back.jpg').convert()
bg = pygame.transform.scale(bg,(bg.get_width(),screenheight))
bg_width = bg.get_width()

scroll = 0
tiles = math.ceil(screenwidth/bg_width)+4
jumper=False
down=False
#background =
while running:
    #screen.fill((0, 0, 0))
    if random.randint(0,2) == 0:
        print("Yes")
        obstacle_group.add(Obstacle())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #runningbackground_group.draw(screen)
    #runningbackground_group.update()
    if(pygame.key.get_pressed()[pygame.K_SPACE]):
        jumper=True
        down=False
    elif(pygame.key.get_pressed()[pygame.K_DOWN]):
        jumper=False
        down=True
    else:
        jumper=False
        down=False

    for i in range(0, tiles):
        screen.blit(bg,(i*bg_width+scroll, 0))
    scroll-=15
    if abs(scroll) >= screenwidth+5:
        scroll = 0
    #runningplayer_group.clear(screen,bg)
    obstacle_group.draw(screen)
    obstacle_group.update()
    runningplayer_group.draw(screen)
    runningplayer_group.update(jumper, down)

    if len(snakes) == 0:
        if random.randint(0,2) == 0:
            snakes.append(SnakeO())
    for snake in snakes:
        snake.draw(screen)
        snake.update()
        if runningplayer.rect.colliderect(snake.rect):
            sys.exit()
    #clock.tick(0.0015)
    #pygame.display.update()
    pygame.display.flip()
    clock.tick(20)



