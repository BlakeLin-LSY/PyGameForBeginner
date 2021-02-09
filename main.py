import os
import pygame

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First GAME!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
PAUSE_FONT = pygame.font.SysFont('comicsans', 100)
TIME_FONT = pygame.font.SysFont('comicsans',40)

# pygame.mixer.Sound()
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun_Silencer.mp3'))

BOARDER_WIDTH = 10
BOARDER_X = WIDTH // 2
BOARDER = pygame.Rect(BOARDER_X - BOARDER_WIDTH // 2, 0, BOARDER_WIDTH, HEIGHT)
FPS = 60
VEL = 5  # Velocity of the movement
BULLET_VEL = 7  # Velocity of bullets
BULLET_SIZE = (10, 5)
MAX_BULLET_NUMBER = 7
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 30

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
YELLOW_SPACESHIP = pygame.transform.rotate(YELLOW_SPACESHIP, 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
RED_SPACESHIP = pygame.transform.rotate(RED_SPACESHIP, 270)

SPACE = pygame.image.load(os.path.join('Assets', 'space.png'))
SPACE = pygame.transform.scale(SPACE, (WIDTH, HEIGHT))


def yellow_handle_movement(key_pressed, yellow):
    if key_pressed[pygame.K_a] and yellow.x - VEL > 5:  # left
        yellow.x -= VEL
    if key_pressed[pygame.K_d] and yellow.x + VEL < BOARDER_X - 15 - SPACESHIP_WIDTH // 2:  # right
        yellow.x += VEL
    if key_pressed[pygame.K_w] and yellow.y - VEL > 5:  # up
        yellow.y -= VEL
    if key_pressed[pygame.K_s] and yellow.y + VEL < HEIGHT - 20 - SPACESHIP_HEIGHT:  # down
        yellow.y += VEL


def red_handle_movement(key_pressed, red):
    if key_pressed[pygame.K_LEFT] and red.x - VEL > BOARDER_X + 5:  # left
        red.x -= VEL
    if key_pressed[pygame.K_RIGHT] and red.x + VEL < WIDTH - 15 - SPACESHIP_WIDTH // 2:  # right
        red.x += VEL
    if key_pressed[pygame.K_UP] and red.y - VEL > 5:  # up
        red.y -= VEL
    if key_pressed[pygame.K_DOWN] and red.y + VEL < HEIGHT - 20 - SPACESHIP_HEIGHT:  # down
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL  # Right to left
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health, time, BOOL_PAUSE = False):
    # WIN.fill(WHITE)
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BOARDER)
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    red_health_text = HEALTH_FONT.render("HEALTH: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("HEALTH: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    time_text = TIME_FONT.render("Time: " + str(time).zfill(3) + " s", 1, RED)
    WIN.blit(time_text, (WIDTH//2 - time_text.get_width()//2 - 10, 10))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    if BOOL_PAUSE:
        draw_text = PAUSE_FONT.render("PAUSE!", 1, WHITE)
        WIN.blit(draw_text,(WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))

    pygame.display.update()


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)

def key_handler(key_pressed):

    if key_pressed[pygame.K_ESCAPE]:
        pygame.event.post(pygame.QUIT)



def main():
    red = pygame.Rect(WIDTH - 100, HEIGHT // 2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(0 + 100, HEIGHT // 2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    yellow_bullets = []
    red_bullets = []

    yellow_health = 10
    red_health = 10

    clock = pygame.time.Clock()
    pause = False
    game_time = 0
    second = round(game_time)

    run = True
    while run:
        clock.tick(FPS)
        # print(clock.get_time())

        # if game_time % 5 == 0:
        #     print(game_time)
        print(game_time)
        if pause:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pause = False
                    else:
                        pass
        else:
            game_time += (clock.get_time() * 0.001)
            if round(game_time) > second:
                second = round(game_time)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLET_NUMBER:
                        bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, BULLET_SIZE[0],
                                             BULLET_SIZE[1])
                        yellow_bullets.append(bullet)
                        BULLET_FIRE_SOUND.play()

                    if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLET_NUMBER:
                        bullet = pygame.Rect(red.x + red.width, red.y + red.height // 2 - 2, BULLET_SIZE[0], BULLET_SIZE[1])
                        red_bullets.append(bullet)
                        BULLET_FIRE_SOUND.play()

                    if event.key == pygame.K_ESCAPE: # Reset the game
                        run = False

                    if event.key == pygame.K_SPACE:
                        if not pause:
                            pause = True
                        else:
                            pause = False

                if event.type == YELLOW_HIT:
                    yellow_health -= 1
                    BULLET_HIT_SOUND.play()

                if event.type == RED_HIT:
                    red_health -= 1
                    BULLET_HIT_SOUND.play()

            key_pressed = pygame.key.get_pressed()

            yellow_handle_movement(key_pressed, yellow)
            red_handle_movement(key_pressed, red)

            handle_bullets(yellow_bullets, red_bullets, yellow, red)

            draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health, second, pause)
            winner_text = ""
            if yellow_health == 0:
                winner_text = "Red Wins!!"

            if red_health == 0:
                winner_text = "Yellow Wins!!"

            if winner_text != "":
                draw_winner(winner_text)
                break
    main()

if __name__ == '__main__':
    print('Game Start!')
    main()
