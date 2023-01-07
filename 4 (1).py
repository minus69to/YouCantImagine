import pygame
import random
import os


hFlag = 0
vFlag = 0
pygame.mixer.init()

pygame.init()



# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

# Creating window
screen_width = 800
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

#Background Image
bgimg = pygame.image.load("bgimg2SMT.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()


# Game Title
pygame.display.set_caption("Welcome to new adventure !")
pygame.display.update()
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 55)
font1 = pygame.font.Font('1f.ttf', 40)
font3 = pygame.font.Font('3f.ttf', 30)
font4 = pygame.font.Font('4f.ttf', 50)
font5 = pygame.font.Font('4f.ttf', 30)


def text_screen(text, color, x, y, num):
    if num == 1:
        # screen_text = font4.render(text, True, color)
        screen_text = font1.render(text, True, color)
    elif num == 2:
        screen_text = font1.render(text, True, color)
    elif num == 3:
        screen_text = font3.render(text, True, color)
    elif num == 4:
        screen_text = font4.render(text, True, color)
    elif num == 5:
        screen_text = font5.render(text, True, color)

    gameWindow.blit(screen_text, [x,y])


def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        # gameWindow.fill((233,210,229))
        # gameWindow.fill(bgimg)

        welcomeimg = pygame.image.load("welcomeSMT.jpg")
        welcomeimg = pygame.transform.scale(welcomeimg, (screen_width, screen_height)).convert_alpha()
        gameWindow.blit(welcomeimg, (0, 0))

        text_screen("It was not supposed to be :)", (0,0,255), 120, 250,1)
        text_screen("Press __SPACE__ Bar To Play", (0,0,255), 130, 320,1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('background2SMT.mp3')
                    pygame.mixer.music.play()
                    gameloop()

        pygame.display.update()
        clock.tick(60)


# Game Loop
def gameloop():
    # Game specific variables
    hFlag = 0
    vFlag =0
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_listBonus = []
    snk_length = 1


    # Check if hiscore file exists
    if(not os.path.exists("hiscore.txt")):
        with open("hiscore.txt", "w") as f:
            f.write("0")

    with open("hiscore.txt", "r") as f:
        hiscore = f.read()

    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)
    score = 0
    init_velocity = 5
    snake_size = 30
    fps = 60
    bonus = (int((random.randint(40, 70) / 10)) * 10)
    bouns_x = random.randint(50, screen_width - 50)
    bouns_y = random.randint(50, screen_height - 50)
    while not exit_game:
        if game_over:
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))
            gameWindow.fill(white)

            ##############################################
            gmoverimg = pygame.image.load("gameoverimg.jpg")
            gmoverimg = pygame.transform.scale(gmoverimg, (screen_width, screen_height)).convert_alpha()
            gameWindow.blit(gmoverimg, (0, 0))

            # text_screen("Game Over !", red, 110, 180,4)
            text_screen("Press Enter To Continue", black, 5, 280,5)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                       if hFlag==0:
                           hFlag =1
                       if  hFlag==1 :
                           velocity_x = init_velocity
                           velocity_y = 0
                           vFlag=0
                       else:
                           pass

                    if event.key == pygame.K_LEFT:
                        if hFlag == 0:
                            hFlag = -1
                        if hFlag == -1:
                            velocity_x = -init_velocity
                            velocity_y = 0
                            vFlag=0
                        else:
                            pass

                    if event.key == pygame.K_UP:
                        if vFlag==0:
                            vFlag=1
                        if vFlag==1:
                            velocity_y = - init_velocity
                            velocity_x = 0
                            hFlag=0

                    if event.key == pygame.K_DOWN:
                        if vFlag == 0:
                            vFlag = -1
                        if vFlag == -1:
                            velocity_y =  init_velocity
                            velocity_x = 0
                            hFlag = 0

                    if event.key == pygame.K_q:
                        score +=10

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) < 26 and abs(snake_y - food_y) < 26:
                pygame.mixer.music.load('mix2SMT.mp3')
                pygame.mixer.music.play()

                init_velocity = init_velocity + 1

                score +=10
                food_x = random.randint(20, screen_width // 1.2)
                food_y = random.randint(20, screen_height // 1.2)
                snk_length +=5

                if score>int(hiscore):
                    hiscore = score

            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))
            text_screen("Score : " + str(score) + "                                              Hiscore: "+str(hiscore), black, 5, 5,3)
            # pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            pygame.draw.circle (gameWindow, red, [food_x, food_y],snake_size/2.5)


            head = []
            head.append(snake_x)
            head.append(snake_y)

            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load('gameover2SMT.mp3')
                pygame.mixer.music.play()

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                pygame.mixer.music.load('gameover2SMT.mp3')
                pygame.mixer.music.play()
            plot_snake(gameWindow, (0,0,255), snk_list, snake_size)

            ##############################
            if score <= bonus <= score+20 :

                pygame.draw.rect(gameWindow, (69,69,69), [bouns_x, bouns_y,snake_size*1.5,snake_size*1.5])
                #print(bonus)

            ##############################
            if abs(snake_x - bouns_x) < 26 and abs(snake_y - bouns_y) < 26 and score <= bonus <= score+20 :
                pygame.mixer.music.load('hahaSMT.mp3')
                pygame.mixer.music.play()

                # init_velocity = 5

                sc_check = random.randint(1,3)
                if sc_check == 1:
                    score = score + 10
                    init_velocity = 5
                    print(score)
                else:
                    score += 20
                    init_velocity = init_velocity + 5
                    print(score)
                # snk_length = 1


        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
welcome()
