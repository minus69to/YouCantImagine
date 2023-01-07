import pygame
import random
import sys
#import maingame
pygame.init()

screen_size = 800, 600
bgx = pygame.image.load("bg.png")
bgx = pygame.transform.scale(bgx, (screen_size[0], screen_size[1]))

bg1 = pygame.image.load("bg1.jpg")
bg1 = pygame.transform.scale(bg1, (screen_size[0], screen_size[1]))

bg2 = pygame.image.load("bg11.jpg")
bg2 = pygame.transform.scale(bg2, (screen_size[0], screen_size[1]))

paddle = pygame.image.load("box.png")
paddle = pygame.transform.scale(paddle, (screen_size[0] / 10.67, screen_size[1] / 40))
paddle_width = paddle.get_width()
paddle_hight = paddle.get_height()

ball = pygame.image.load("soccer-ball.png")
ball = pygame.transform.scale(ball, (screen_size[0] / 25, screen_size[0] / 25))
ball_dia = ball.get_width()
ball_rad = ball_dia / 2

brick_width = screen_size[0] / 13.33

live = pygame.image.load("live.png")
live = pygame.transform.scale(live, (screen_size[0] / 25, screen_size[0] / 25))

paddle_center_max_xpos = screen_size[0] - paddle_width / 2
ball_max_xpos = screen_size[0] - ball_rad / 1.4
ball_max_ypos = screen_size[1] - ball_rad / 1.4

ball_in_paddle = 0
plying = 1
won = 2
game_over = 3


class Brick():
    def __init__(self, brick_start_x, brick_start_y):
        self.xpos = brick_start_x
        self.ypos = brick_start_y
        self.birck_width = screen_size[0] / 13.33
        self.birck_hight = screen_size[1] / 30
        self.color = None
        self.rect = pygame.Rect(brick_start_x, brick_start_y, self.birck_width, self.birck_hight)


class DxBall():
    def __init__(self):
        self.screen = pygame.display.set_mode((screen_size[0], screen_size[1]))
        self.bg_sound = pygame.mixer.Sound("music1.wav")
        self.bricks = []

        self.clock = pygame.time.Clock()
        self.end_game = False
        if pygame.font:
            self.font = pygame.font.Font(None, 30)

        else:
            self.font = None

        self.start()

    def start(self):
        self.lives = 3
        self.score = 0
        self.state = ball_in_paddle

        self.paddle = paddle
        self.paddle_rect = self.paddle.get_rect()
        self.paddle_rect.center = screen_size[0] / 2, screen_size[1] - screen_size[1] / 4
        self.ball = ball
        self.ball_rect = self.ball.get_rect()
        self.ball_rect.center = screen_size[0] / 2, self.paddle_rect.top - ball_rad / 1.4

        self.game_form = random.randint(1, 3)

        if self.game_form == 1:
            self.brickform1()
        elif self.game_form == 2:
            self.brickform2()
        elif self.game_form == 3:
            self.brickform3()

    def brickform1(self):
        self.target = random.randint(10, 20)
        global new_brick
        brick_start_y = screen_size[1] / 20
        for i in range(8):
            brick_start_x = screen_size[0] / 2 - screen_size[0] / 2.76
            for j in range(9):
                new_brick = Brick(brick_start_x, brick_start_y)
                self.bricks.append(new_brick)
                if (i == 1 or (3 <= i <= 4) or i == 6) and (j == 1 or (3 <= j <= 5) or j == 7):
                    pass
                else:
                    new_brick.color = (255, 0, 255)
                brick_start_x += new_brick.birck_width + screen_size[0] / 160
            brick_start_y += new_brick.birck_hight + screen_size[0] / 160

    def brickform2(self):
        self.target = random.randint(10, 20)
        global new_brick
        brick_start_y = screen_size[1] / 17.14

        for i in range(8):

            if i % 2 == 0:
                brick_start_x = screen_size[0] / 2 - screen_size[0] / 2.76
                for j in range(5):
                    new_brick = Brick(brick_start_x, brick_start_y)
                    self.bricks.append(new_brick)
                    if j % 2 == 0:
                        pass
                    else:
                        new_brick.color = (0, 0, 255)
                    brick_start_x += new_brick.birck_width + screen_size[0] / 160 + new_brick.birck_width
                brick_start_y += new_brick.birck_hight + screen_size[0] / 160
            else:
                brick_start_x = screen_size[0] / 2 - screen_size[0] / 2.76 + brick_width
                for j in range(4):
                    new_brick = Brick(brick_start_x, brick_start_y)
                    self.bricks.append(new_brick)
                    new_brick.color = (0, 0, 255)
                    brick_start_x += new_brick.birck_width + screen_size[0] / 160 + new_brick.birck_width
                brick_start_y += new_brick.birck_hight + screen_size[0] / 160

    def brickform3(self):
        self.target = random.randint(10, 20)
        global new_brick
        brick_start_y = screen_size[1] / 20
        for i in range(9):
            brick_start_x = screen_size[0] / 2 - screen_size[0] / 2.76
            for j in range(9):
                new_brick = Brick(brick_start_x, brick_start_y)
                self.bricks.append(new_brick)
                if i == 1 or i == 7:
                    if 0 < j < 8:
                        self.bricks.remove(new_brick)
                if i == 3 or i == 5:
                    if j == 1 or j == 7 or 2 < j < 6:
                        self.bricks.remove(new_brick)

                new_brick.color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))

                brick_start_x += new_brick.birck_width + screen_size[0] / 160
            brick_start_y += new_brick.birck_hight + screen_size[0] / 160

    def draw_bricks(self):

        for brick in self.bricks:
            pygame.draw.rect(self.screen, brick.color, brick.rect)

    def control(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LEFT]:
            self.paddle_rect.center = self.paddle_rect.center[0] - screen_size[0] / 80, self.paddle_rect.center[1]
            if self.paddle_rect.center[0] < self.paddle.get_width() / 2:
                self.paddle_rect.center = self.paddle.get_width() / 2, screen_size[1] - screen_size[1] / 4

        if pressed[pygame.K_RIGHT]:
            self.paddle_rect.center = self.paddle_rect.center[0] + screen_size[0] / 80, self.paddle_rect.center[1]
            if self.paddle_rect.center[0] > paddle_center_max_xpos:
                self.paddle_rect.center = screen_size[0] - self.paddle.get_width() / 2, screen_size[1] - screen_size[
                    1] / 4

        if pressed[pygame.K_SPACE] and self.state == ball_in_paddle:
            if self.game_form == 1:
                self.velocity = [screen_size[0] / 136, -screen_size[0] / 136]
            elif self.game_form == 2:
                self.velocity = [screen_size[0] / 110, -screen_size[0] / 110]
            else:
                self.velocity = [screen_size[0] / 120, -screen_size[0] / 120]
            self.state = plying
        elif pressed[pygame.K_RETURN] and (self.state == game_over or self.state == won):
            if self.state == game_over:
                self.start()

    def ballmovement(self):

        self.ball_rect.center = self.ball_rect.center[0] + self.velocity[0], self.ball_rect.center[1] + self.velocity[1]

        if self.ball_rect.center[0] <= ball_rad / 1.4:
            self.ball_rect.center = ball_rad / 1.4, self.ball_rect.center[1]
            self.velocity[0] = -self.velocity[0]
        elif self.ball_rect.center[0] >= ball_max_xpos:
            self.ball_rect.center = ball_max_xpos, self.ball_rect.center[1]
            self.velocity[0] = -self.velocity[0]

        if self.ball_rect.center[1] < ball_rad / 1.4:
            self.ball_rect.center = self.ball_rect.center[0], ball_rad / 1.4
            self.velocity[1] = -self.velocity[1]

    def collision(self):
        for brick in self.bricks:
            if self.ball_rect.colliderect(brick):
                self.score += 1
                self.velocity[1] = -self.velocity[1]
                self.bricks.remove(brick)
                break
        if self.score == self.target:
            self.state = won

        if self.ball_rect.colliderect(self.paddle_rect):
            self.ball_rect.center = self.ball_rect.center[0], self.paddle_rect.center[
                                                                  1] - paddle_hight / 2 - ball_rad / 1.4
            self.velocity[1] = -self.velocity[1]
        elif self.ball_rect.center[1] > self.paddle_rect.center[1]:
            self.lives -= 1
            self.paddle_rect.center = screen_size[0] / 2, screen_size[1] - screen_size[1] / 4
            self.ball_rect.center = screen_size[0] / 2, self.paddle_rect.top - ball_rad / 1.4
            if self.lives > 0:
                self.state = ball_in_paddle
            else:
                self.state = game_over

    def scoreshow(self):
        if self.font:
            font_surfce = self.font.render("SCORE : " + str(self.score), False, (255, 255, 255))
            target = self.font.render("TARGET : " + str(self.target), False, (255, 255, 255))
            self.screen.blit(font_surfce,
                             (screen_size[0] - screen_size[0] / 5.33, screen_size[1] - screen_size[0] / 16))
            self.screen.blit(target, (screen_size[0] - screen_size[0] / 5.33, screen_size[1] - screen_size[0] / 28))

    def show_message(self, message):
        if self.font:
            size = self.font.size(message)
            font_surface = self.font.render(message, False, (255, 255, 0))
            x = (screen_size[0] - size[0]) / 2
            y = (screen_size[1] - size[1]) / 2 + screen_size[0] / 16
            self.screen.blit(font_surface, (x, y))

    def endgame(self):
        return self.end_game

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        self.clock.tick(40)

        for brick in self.bricks:
            if self.game_form == 1:
                if brick.color == (255, 0, 255):
                    pass
                else:
                    brick.color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
            if self.game_form == 2:
                if brick.color == (0, 0, 255):
                    pass
                else:
                    brick.color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))

        if self.game_form == 1:
            self.screen.blit(bgx, (0, 0))
        elif self.game_form == 2:
            self.screen.blit(bg1, (0, 0))
        else:
            self.screen.blit(bg2, (0, 0))

        if self.state == plying:
            self.bg_sound.play()
            self.ballmovement()
            self.collision()
        elif self.state == ball_in_paddle:
            self.ball_rect.center = self.paddle_rect.center[0], self.ball_rect.center[1]
            if self.lives == 3:
                self.show_message("Press 'space' key to start.")
        elif self.state == game_over:
            for brick in self.bricks:
                self.bricks.remove(brick)
            self.show_message("Game over.")
        elif self.state == won:
            self.show_message("Gongrats!You have completed the target.")
            self.end_game = True

        self.draw_bricks()
        live_rect = live.get_rect()
        live_rect.center = (
            screen_size[0] - live.get_width() * 3 + live.get_width() / 2 - 15, 2 + live.get_height() / 2)
        for i in range(self.lives):
            self.screen.blit(live, live_rect)
            live_rect.center = live_rect.center[0] + live.get_width() + 5, live_rect.center[1]
        self.control()
        self.screen.blit(self.paddle, self.paddle_rect)
        self.screen.blit(self.ball, self.ball_rect)
        self.scoreshow()
        pygame.display.flip()


if __name__ == "__main__":
    DxBall().run()
