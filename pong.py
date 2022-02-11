from cgitb import text
from re import S
import pygame
import sys
import random
import time

mode = ''
score_left = 0
score_right = 0
diff = 0
rate = 75
rally = 0
hit = 'l'
endless = False

#images
ps = pygame.image.load('Personal/PongWithController/ps4icons/ps.png')
ps_scale = pygame.transform.scale(ps,(32,32))
o = pygame.image.load('Personal/PongWithController/ps4icons/o.png')
o_scale = pygame.transform.scale(o,(32,32))
x = pygame.image.load('Personal/PongWithController/ps4icons/x.png')
x_scale = pygame.transform.scale(x,(32,32))
options = pygame.image.load('Personal/PongWithController/ps4icons/options.png')
options_scale = pygame.transform.scale(options,(47,57))

pygame.init()
clock = pygame.time.Clock()

screen_width = 1920
screen_height = 1080
# screen = pygame.display.set_mode((screen_width,screen_height))
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN,32)
pygame.display.set_caption('Controller Pong')

ball = pygame.Rect(screen_width/2 - 16,screen_height/2 - 16,32,32)
player1 = pygame.Rect(screen_width - 20,screen_height/2 - 70,10,140)
player2 = pygame.Rect(10,screen_height/2 - 70,10,140)

bg_color = (28, 108, 100)
light_grey = (200,200,200)

ballX = random.randint(5,8)
ballY = random.randint(-8,8)
oppY = 7

multiplier = 1.1

high = 0

def ballsy():
    global ballX, ballY, diff, score_left, score_right, rally, hit, oppY, multiplier, high
    ball.x += ballX
    ball.y += ballY

    if ball.top <= 0 or ball.bottom >= screen_height:
        ballY *= -1
    elif ball.left <= 0 and hit == 'r' and not endless:
        score_right +=1
        ball.center = (screen_width/2,screen_height/2)
        time.sleep(1)
        ballX = random.randint(5,8)
        ballY = random.randint(-8,8)
        time.sleep(1)
        diff = random.randint(-4,4)
        if rally > high:high = rally
        rally = 0
        hit = 'l'
        oppY += 2
    elif ball.left <= 0 and hit == 'r' and endless:
        ballX *= -1
    elif ball.right >= screen_width and hit == 'l':
        score_left +=1
        ball.center = (screen_width/2,screen_height/2)
        time.sleep(1)
        ballX = random.randint(-8,-5)
        ballY = random.randint(-8,8)
        time.sleep(1)
        if rally > high:high = rally
        rally = 0
        hit = 'r'
    
    elif ball.right >= screen_width and hit == 'r':
        ballX *= -1
    elif ball.left <= 0 and hit == 'l':
        ballX *= -1
    
    elif ball.colliderect(player1) and hit == 'l':
        ballX *= -1
        ballX = ballX*multiplier
        ballY = ballY*multiplier
        rally+=1
        hit = 'r'
        oppY += 1
    elif ball.colliderect(player2) and hit == 'r':
        ballX *= -1
        ballX = ballX*multiplier
        ballY = ballY*multiplier
        diff = random.randint(-4,4)
        rally+=1
        hit = 'l'

def pause():
    global mode, endless, multiplier
    paused = True
    fg = (145, 146, 230)
    bg = (8, 88, 80)
    font = pygame.font.Font('freesansbold.ttf', 32)

    pause_text = font.render('Paused',True,fg,bg)
    textRect = pause_text.get_rect()

    line1 = font.render(" Press M to change to mouse input ",True,fg,bg)
    textRect2 = line1.get_rect()
    textRect2.bottom += 300

    line2 = font.render(" Press C to change to controller input ",True,fg,bg)
    textRect3 = line2.get_rect()
    textRect3.bottom += 400

    line3 = font.render(" Press Q to quit ",True,fg,bg)
    textRect4 = line3.get_rect()
    textRect4.bottom += 200
    
    line4 = font.render(" Press P to resume ",True,fg,bg)
    textRect5 = line4.get_rect()
    textRect5.bottom += 100

    current_mode = ' Current Mode : ' + str(mode)
    line5 = font.render(current_mode,True,fg,bg)
    textRect6 = line5.get_rect()
    textRect6.bottom += 500

    endlessm = font.render(" Toggle Endless Mode? E ",True,fg,bg)
    endlessRect = endlessm.get_rect()
    endlessRect.bottom += 600
    
    while paused:
        clock.tick(0)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    mode = 'controller'
                    clock.tick(rate)
                    paused = False
                elif event.key == pygame.K_m:
                    mode = 'mouse'
                    clock.tick(rate)
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.QUIT
                    sys.exit()
                elif event.key == pygame.K_p:
                    clock.tick(rate)
                    paused = False
                elif event.key == pygame.K_e and endless == False:
                    endless = True
                    paused = False
                    multiplier = 1.03
                    game_reset()
                elif event.key == pygame.K_e and endless == True:
                    endless = False
                    paused = False
                    multiplier = 1.1
                    game_reset()
            elif event.type == pygame.JOYBUTTONDOWN:
                if pygame.joystick.Joystick(0).get_button(6):
                    paused = False
                elif pygame.joystick.Joystick(0).get_button(5):
                    pygame.QUIT
                    sys.exit()
                elif pygame.joystick.Joystick(0).get_button(0):
                    mode = 'mouse'
                    clock.tick(rate)
                    paused = False
                elif pygame.joystick.Joystick(0).get_button(1):
                    mode = 'controller'
                    clock.tick(rate)
                    paused = False
                 
        screen.blit(pause_text,textRect)
        screen.blit(line3,textRect4)
        screen.blit(line4,textRect5)
        screen.blit(endlessm,endlessRect)
        if pygame.joystick.get_count():
            screen.blit(line1,textRect2)
            screen.blit(line2,textRect3)
            screen.blit(line5,textRect6)
            screen.blit(ps_scale,(100,200))
            screen.blit(o_scale,(100,400))
            screen.blit(x_scale,(100,300))
            screen.blit(options_scale,(90,80))
        pygame.display.update()

def inputs():
    global mode
    joystick_count = pygame.joystick.get_count()
    if joystick_count != 0 and mode == '':
        multi_input = True
        # choice = input("Controller mode or Mouse mode? (c/m) ")
        # if choice.lower() == 'c':
        #     mode = 'controller'
        # elif choice.lower() == 'm':
        #     mode = 'mouse'
        # print("Press 'P' to start playing")
        fg = (145, 146, 230)
        font = pygame.font.Font('freesansbold.ttf', 32)

        multi_text = font.render('Press P to pause the game anytime and change controls / quit',True,fg,'grey12')
        multiRect = multi_text.get_rect()
        multiRect.center = (screen_width/2, screen_height/2 - 200)

        joystick_text = font.render('Press C to use joystick',True,fg,'grey12')
        joystickRect = joystick_text.get_rect()
        joystickRect.center = (screen_width/2, screen_height/2 - 300)

        mouse_text = font.render('Press M to use mouse',True,fg,'grey12')
        mouseRect = mouse_text.get_rect()
        mouseRect.center = (screen_width/2, screen_height/2 - 400)

        select_text = font.render('You have 2 inputs (Controller / Mouse)',True,fg,'grey12')
        selectRect = select_text.get_rect()
        selectRect.center = (screen_width/2, screen_height/2 - 500)

        while multi_input:
            clock.tick(0)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        mode = 'controller'
                        clock.tick(rate)
                        multi_input = False
                    elif event.key == pygame.K_m:
                        mode = 'mouse'
                        clock.tick(rate)
                        multi_input = False
            screen.blit(multi_text,multiRect)
            screen.blit(joystick_text,joystickRect)
            screen.blit(mouse_text,mouseRect)
            screen.blit(select_text ,selectRect)
            pygame.display.update()
    else:
        multi_input = False

def end_screen():
    global my_joystick, rally, high
    exit_text = gamefont.render("Q or PS to exit, Space or x to retry",False,white,bg_color)
    exit_rect = exit_text.get_rect()
    exit_rect.center = (screen_width/2,screen_height/2 + 78)
    
    if not endless:
        if score_left >= 10:
            clock.tick(0)
            lose_text = endfont.render("You Lose!",False,red,bg_color)
            lose_rect = lose_text.get_rect()
            lose_rect.center = (screen_width/2,screen_height/2)
            screen.blit(lose_text,lose_rect)
            screen.blit(exit_text,exit_rect)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    pygame.QUIT
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    game_reset()
                if event.type == pygame.JOYBUTTONDOWN:
                    if my_joystick.get_button(0):
                        game_reset()
                    elif my_joystick.get_button(5):
                        pygame.QUIT
                        sys.exit()

        if score_right >= 10:
            clock.tick(0)
            win_text = endfont.render("You Win!",False,green,bg_color)
            win_rect = win_text.get_rect()
            win_rect.center = (screen_width/2,screen_height/2)
            screen.blit(win_text,win_rect)
            screen.blit(exit_text,exit_rect)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.QUIT
                        sys.exit()
                    elif event.key == pygame.K_SPACE:
                        game_reset()
                if event.type == pygame.JOYBUTTONDOWN:
                    if my_joystick.get_button(5):
                        pygame.QUIT
                        sys.exit()
                    elif my_joystick.get_button(0):
                        game_reset()
    if endless:
        if ball.right >= screen_width and hit == 'l':
            ball.center = (screen_width/2,screen_height/2)
            time.sleep(2)
            rally = 0
        if rally > high:high = rally
        highscore = gamefont.render("Highscore : " +f"{high}",False,white,bg_color)
        screen.blit(highscore,(screen_width/2 + 30,10))
    pygame.display.update()

                
def game_reset():
    clock.tick(rate)
    global score_left,score_right,rally,hit,ballY,ballX,oppY,ball,player1,player2
    score_right = 0
    score_left = 0
    
    rally = 0
    hit = 'l'
    
    ballX = random.randint(5,8)
    ballY = random.randint(-8,8)
    oppY = 7
    
    ball = pygame.Rect(screen_width/2 - 16,screen_height/2 - 16,32,32)
    player1 = pygame.Rect(screen_width - 20,screen_height/2 - 70,10,140)
    player2 = pygame.Rect(10,screen_height/2 - 70,10,140)
    
    screen.fill(bg_color)
    pygame.draw.rect(screen,light_grey,player1)
    pygame.draw.rect(screen,light_grey,player2)
    pygame.draw.ellipse(screen,light_grey,ball)
    pygame.draw.aaline(screen,light_grey,(screen_width/2,0),(screen_width/2,screen_height))
    
    player_text = gamefont.render(f"{score_right}",False,white)
    screen.blit(player_text,(screen_width/2 + 16,screen_height/2 - 24))

    opponent_text = gamefont.render(f"{score_left}",False,white)
    screen.blit(opponent_text,(screen_width/2 - 40,screen_height/2 - 24))

    rally_text = gamefont.render(f"{rally}",False,white)
    screen.blit(rally_text,(30,10))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause()
        
        global my_joystick
        if event.type == pygame.JOYBUTTONDOWN:
            if my_joystick.get_button(6):
                pause()
    inputs()
    ballsy()

    joystick_count = pygame.joystick.get_count()
    if joystick_count == 0 or mode == 'mouse':
        mouseX, mouseY = pygame.mouse.get_pos()
        player1.y = mouseY - 70
    else:
        # Use joystick #0 and initialize it
        my_joystick = pygame.joystick.Joystick(0)
        my_joystick.init()
        horiz_axis_pos = my_joystick.get_axis(0)
        vert_axis_pos = my_joystick.get_axis(1)
        if player1.y >= 0 or player1.y <= screen_height:
            player1.y += int(vert_axis_pos * 10)
        if player1.y <= 0:
            player1.y = 1
        if player1.y >= screen_height-140:
            player1.y = screen_height-140

    if endless:
        player2.y = ball.y - 70
    if not endless:
        if ball.x <= screen_width*0.75:
            if player2.top < ball.y:
                player2.top += oppY
            if player2.bottom > ball.y:
                player2.bottom -= oppY


    mauve = (145, 146, 230)

    gamefont = pygame.font.Font("freesansbold.ttf",48)
    white = (255,255,255)
    endfont = pygame.font.Font("freesansbold.ttf",108)
    red = (255,0,0)
    green = (0,255,0)

    screen.fill(bg_color)
    pygame.draw.rect(screen,light_grey,player1)
    pygame.draw.rect(screen,light_grey,player2)
    pygame.draw.ellipse(screen,light_grey,ball)
    pygame.draw.aaline(screen,light_grey,(screen_width/2,0),(screen_width/2,screen_height))

    if not endless:
        player_text = gamefont.render(f"{score_right}",False,white)
        screen.blit(player_text,(screen_width/2 + 16,screen_height/2 - 24))

        opponent_text = gamefont.render(f"{score_left}",False,white)
        screen.blit(opponent_text,(screen_width/2 - 40,screen_height/2 - 24))

    rally_text = gamefont.render("Rally : "+f"{rally}",False,white)
    screen.blit(rally_text,(30,10))

    end_screen()

    pygame.display.flip()
    clock.tick(rate)

#Change enemy randint from every tick to every collision with player2 (enemy). DONE
#Also add difficulty and scoring system + menu where bg is a diff color, tick = 0 and options can be selected
#As difficulty goes higher, decrease randint boundaries and increase enemy speed / ball speed
#Make unbeatable mode where enemy always hits ball and count collisions to track highscore?

#ps4 controls based on my testing :
# button 5 = PS button
# 6 = options
# 7 = L3
# 9 = left bumper
# 10 = right bumper
