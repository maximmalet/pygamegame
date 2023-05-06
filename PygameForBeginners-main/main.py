import pygame
import os
pygame.font.init()
pygame.mixer.init()

#modifiable CONSTANTS

WIDTH, HEIGHT = 500, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hollow Knight Shooter")
#COLORS & FONTS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
#WINDOW Objects


BORDER = pygame.Rect(0, 500, WIDTH, 5)
#SOUNDS
#ADDED AMBIENT TRACK
AMBIENCE = pygame.mixer.Sound(os.path.join('Assets', '09. City of Tears.mp3'))
BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/sword2.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/sword.mp3')
EXPLOSION_SOUND = pygame.mixer.Sound('Assets/explosion.mp3')

HEALTH_FONT = pygame.font.SysFont('montserrat', 40)
WINNER_FONT = pygame.font.SysFont('montserrat', 100)

FPS = 120
VEL = 5
BULLET_VEL = 8
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
#USER EVENTS

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
#loading Images
#transform Images

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

def create_explosion(surface, x, y):
    """Create an explosion effect at the given coordinates."""
    # Load the explosion image (leave it large because that way its funnier)
    explosion_img = pygame.image.load("Assets/explosion.png").convert_alpha()

    # Play the explosion sound
    EXPLOSION_SOUND.play()

    # Draw the explosion images on the surface
    rect = explosion_img.get_rect(center=(x, y))
    surface.blit(explosion_img, rect)
    # Update the display and wait a bit
    pygame.display.update()
    pygame.time.wait(100)

    # Clear the explosion images from the surface
    rect = pygame.Rect(x-100, y-100, 200, 200)
    surface.fill((0, 0, 0), rect)

    # Update the display
    pygame.display.update()

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, GREEN, BORDER)

    red_health_text = HEALTH_FONT.render(
        "VIGOR: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "VIGOR: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_q] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_e] and yellow.x + VEL + SPACESHIP_WIDTH < WIDTH:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_2] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_w] and yellow.y + VEL + BORDER.y < HEIGHT + SPACESHIP_HEIGHT:  # DOWN
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_j] and red.x - VEL - SPACESHIP_WIDTH > BORDER.x:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_l] and red.x + VEL + SPACESHIP_WIDTH < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_i] and red.y - VEL > HEIGHT/2 + SPACESHIP_HEIGHT:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_k] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        #update position
        #target collision
        #Off-Screen despawn

        bullet.y += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
            create_explosion(WIN, bullet.x, bullet.y)
        elif bullet.y > HEIGHT:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.y -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
            create_explosion(WIN, bullet.x, bullet.y)
        elif bullet.y < 0:
            red_bullets.remove(bullet)

#Winner screen
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.fill(GREEN)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)



#main loop
def main():
    
    AMBIENCE.play()
    red = pygame.Rect(100, 600, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 20
    yellow_health = 20

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet1 = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 5, 10)
                    bullet2 = pygame.Rect(
                        yellow.x + 10 + yellow.width, yellow.y + yellow.height//2 - 17, 5, 10)
                    yellow_bullets.append(bullet1)
                    yellow_bullets.append(bullet2)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RALT:
                    bullet1 = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 5, 10)
                    bullet2 = pygame.Rect(
                        red.x + 10, red.y + red.height//2 - 17, 5, 10)
                    red_bullets.append(bullet1)
                    red_bullets.append(bullet2)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health)

    main()


if __name__ == "__main__":
    main()
