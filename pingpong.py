import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong Pro - Naomi Celeres")

clock = pygame.time.Clock()

# COLORS
PINK = (255, 182, 193)
BLACK = (0, 0, 0)
GRAY = (80, 80, 80)

# FONT
font = pygame.font.SysFont(None, 55)
small = pygame.font.SysFont(None, 28)

# STATES
menu = True
playing = False
win_screen = False

mode = None
difficulty = "MEDIUM"

WIN_SCORE = 3
player_score = 0
opponent_score = 0
winner_text = ""

# PADDLES
p_w, p_h = 14, 90
player = pygame.Rect(30, HEIGHT//2, p_w, p_h)
opponent = pygame.Rect(WIDTH-44, HEIGHT//2, p_w, p_h)

# BALL
ball = pygame.Rect(WIDTH//2, HEIGHT//2, 14, 14)
ball_speed_x = 6
ball_speed_y = 4


def reset_ball(direction=None):
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH//2, HEIGHT//2)
    direction = direction or random.choice((1, -1))
    ball_speed_x = 6 * direction
    ball_speed_y = 4 * random.choice((-1, 1))


def ai_move():
    speed = {"EASY": 3, "MEDIUM": 5, "HARD": 8}[difficulty]

    if opponent.centery < ball.centery:
        opponent.y += speed
    elif opponent.centery > ball.centery:
        opponent.y -= speed


reset_ball()


while True:
    screen.fill(PINK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            # MENU INPUT
            if menu:
                if event.key == pygame.K_1:
                    mode = "AI"
                if event.key == pygame.K_2:
                    mode = "PVP"
                if event.key == pygame.K_e:
                    difficulty = "EASY"
                if event.key == pygame.K_m:
                    difficulty = "MEDIUM"
                if event.key == pygame.K_h:
                    difficulty = "HARD"

                if event.key == pygame.K_RETURN and mode:
                    menu = False
                    playing = True
                    player_score = 0
                    opponent_score = 0
                    reset_ball()

            # WIN SCREEN RESET
            if win_screen and event.key == pygame.K_RETURN:
                win_screen = False
                menu = True

    keys = pygame.key.get_pressed()

    # ================= MENU =================
    if menu:
        screen.blit(font.render("PING PONG PRO", True, BLACK), (220, 70))
        screen.blit(small.render("NAOMI CELERES EDITION", True, BLACK), (250, 140))

        screen.blit(small.render("PRESS 1 - AI MODE", True, BLACK), (300, 200))
        screen.blit(small.render("PRESS 2 - 2 PLAYER MODE", True, BLACK), (270, 230))

        screen.blit(small.render("E / M / H = EASY / MEDIUM / HARD", True, BLACK), (190, 280))
        screen.blit(small.render("PRESS ENTER TO START", True, BLACK), (280, 330))

        screen.blit(small.render(f"SELECTED: {mode} | {difficulty}", True, BLACK), (250, 380))

    # ================= WIN SCREEN =================
    elif win_screen:
        screen.blit(font.render(winner_text, True, BLACK),
                    (WIDTH//2 - 200, HEIGHT//2 - 50))

        screen.blit(small.render("PRESS ENTER TO PLAY AGAIN", True, BLACK),
                    (WIDTH//2 - 170, HEIGHT//2 + 20))

    # ================= GAME =================
    else:

        # PLAYER 1
        if keys[pygame.K_UP]:
            player.y -= 7
        if keys[pygame.K_DOWN]:
            player.y += 7

        # PLAYER 2 OR AI
        if mode == "PVP":
            if keys[pygame.K_w]:
                opponent.y -= 7
            if keys[pygame.K_s]:
                opponent.y += 7
        else:
            ai_move()

        # LIMIT PADDLES
        player.y = max(0, min(HEIGHT - player.height, player.y))
        opponent.y = max(0, min(HEIGHT - opponent.height, opponent.y))

        # BALL MOVE
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # WALL
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1

        # COLLISION
        if ball.colliderect(player):
            ball_speed_x = abs(ball_speed_x)

        if ball.colliderect(opponent):
            ball_speed_x = -abs(ball_speed_x)

        # SCORE
        if ball.left <= 0:
            opponent_score += 1
            reset_ball(direction=1)

        if ball.right >= WIDTH:
            player_score += 1
            reset_ball(direction=-1)

        # WIN CONDITION
        if player_score == WIN_SCORE:
            win_screen = True
            playing = False
            winner_text = "YOU WIN - NAOMI CELERES"

        if opponent_score == WIN_SCORE:
            win_screen = True
            playing = False
            if mode == "PVP":
                winner_text = "PLAYER 2 WINS"
            else:
                winner_text = "AI WINS"

        # CENTER LINE
        for y in range(0, HEIGHT, 20):
            pygame.draw.rect(screen, GRAY, (WIDTH//2, y, 3, 10))

        # DRAW
        pygame.draw.rect(screen, BLACK, player)
        pygame.draw.rect(screen, BLACK, opponent)
        pygame.draw.circle(screen, BLACK, ball.center, 8)

        # SCORE
        screen.blit(font.render(str(player_score), True, BLACK), (80, 20))
        screen.blit(font.render(str(opponent_score), True, BLACK), (WIDTH-100, 20))

        screen.blit(small.render("NAOMI CELERES", True, BLACK), (10, HEIGHT-30))

    pygame.display.update()
    clock.tick(60)