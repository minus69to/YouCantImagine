import pygame
import sys
import random

score = 0
count = 0
class Crosshair(pygame.sprite.Sprite):

    def __init__(self, posX, posY,pic1):
        super().__init__()
        self.small_image = pygame.image.load(pic1)
        self.image = pygame.transform.scale(self.small_image, (50, 50))
        self.image.set_alpha(255)
        self.rect = self.image.get_rect(center=(posX, posY))
        self.sound = pygame.mixer.Sound("sound.mp3")

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

    def shoot(self):
        global score
        global count
        self.sound.play()
        pygame.sprite.spritecollide(crosshair,target_group,True)
        score += 1
        if count > 0:
            count -= 1
        print(score)

class Target(pygame.sprite.Sprite):
    def __init__(self, posX, posY, pic1):
        super().__init__()
        self.small_image = pygame.image.load(pic1)
        self.image = pygame.transform.scale(self.small_image, (75, 75))
        self.image.set_alpha(255)
        self.rect = self.image.get_rect(center=(posX, posY))
        self.move = random.randint(0,1)
        self.speed = random.randint(2,3)

    def update(self):
        if self.move == 0:
            global count
            self.rect.centerx += self.speed
            if self.rect.centerx > 750 :
                count -= 1
                self.kill()
        elif self.move == 1:
            self.rect.centerx -= self.speed
            if self.rect.centerx < 25:
                count -= 1
                self.kill()

pygame.init()

clock = pygame.time.Clock()

screenWidth = 800
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))

crosshair = Crosshair( 100, 100, "ch.png")

crosshair_group = pygame.sprite.Group()
crosshair_group.add(crosshair)

target_group = pygame.sprite.Group()
for i in range(20):
    target_group.add(Target(random.randint(0, screenWidth), random.randint(0, screenHeight), "tg.png"))
    count += 1

back = pygame.image.load('background4.png')

while True:
    pygame.mouse.set_visible(False)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            crosshair.shoot()
    pygame.display.flip()
    if count > 0:
        screen.blit(back, (0, 0))
    target_group.draw(screen)
    crosshair_group.draw(screen)
    target_group.update()
    crosshair_group.update()
    clock.tick(60)