import pygame, sys


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.posx = 400
        self.posy = 500
        self.image= pygame.Surface((500,50))
        self.image.fill((255,255,255))
        self.rect= self.image.get_rect(center=(self.posx,self.posy))


    def update(self):
        x, y=pygame.mouse.get_pos()
        self.rect.center = (x,700-200)
    def create_bullet(self):
        return Bullet(pygame.mouse.get_pos()[0],500)
class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        super().__init__()
        self.image= pygame.Surface((50,10))
        self.image.fill((255,0,0))
        self.rect= self.image.get_rect(center=(pos_x,pos_y))
    def update(self):
        self.rect.y-=15
        if self.rect.y <= 20:
            self.kill()
class Ball(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image=pygame.Surface((100,100))
        self.image.fill((255,255,0))
        self.rect= self.image.get_rect(center=(100,100))
        self.side = 1
    def update(self) :
        if(self.rect.centerx<=0):
            self.side=1
        elif(self.rect.centerx>=700):
            self.side=0
        if(self.side==0):
            self.rect.centerx-=15
        elif(self.side==1):
            self.rect.centerx+=15

pygame.init()

Clock = pygame.time.Clock()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Snake")
running = True

pygame.mouse.set_visible(False)
player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)
bullet_group= pygame.sprite.Group()
back=pygame.image.load('background4.png')

ballGroup=pygame.sprite.Group()
ball=Ball()
ballGroup.add(ball)

dog = pygame.image.load('dogecoin.jpg')
x = 0
y = 0
side = 1
up = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            bullet_group.add(player.create_bullet())
        pressed=pygame.key.get_pressed()
        if pressed[pygame.K_DOWN]:
            y += 2
            pygame.display.update()
        elif pressed[pygame.K_UP]:
            y -= 2
            pygame.display.update()
        elif pressed[pygame.K_LEFT]:
            x -= 2
            pygame.display.update()
        elif pressed[pygame.K_RIGHT]:
            x += 2
            pygame.display.update()
    screen.blit(back , (0 , 0))
    #screen.blit(dog , (x , y))
    bullet_group.draw(screen)
    player_group.draw(screen)
    player_group.update()
    pygame.display.update()
    bullet_group.update()
    ballGroup.draw(screen)
    ballGroup.update()
    pygame.display.update()

    Clock.tick(120)

pygame.quit()
sys.exit()
