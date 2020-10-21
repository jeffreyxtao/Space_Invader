# set up pygame and random
import pygame
import random
import math
from pygame import mixer


pygame.init()

# create game screen
screen = pygame.display.set_mode((800, 600))

# set title and icon and background music
pygame.display.set_caption("Space Shooter")
icon = pygame.image.load("space shooter icon.png")
pygame.display.set_icon(icon)
mixer.music.load("background.wav")
mixer.music.play(-1)

# set up player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0


def player():
    screen.blit(playerImg, (round(playerX), round(playerY)))


# set up enemy
num_of_enemies = 5
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.2)
    enemyY_change.append(40)


def enemy(x, y, i):
    screen.blit(enemyImg[i], (round(x), round(y)))


# set up bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = random.randint(0, 736)
bulletY = 480
bulletY_change = 0.4
bullet_state = "ready"


def bullet(x, y):
    global bullet_state
    bullet_state = "firing"
    screen.blit(bulletImg, (round(x + 16), round(y + 10)))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


score = 0
font = pygame.font.Font('freesansbold.ttf', 32)


def show_score():
    x = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(x, (10, 10))


over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    x = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(x, (200, 250))

running = True
while running:

    # set background
    screen.fill((0, 8, 15))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            # bullet movement
            if bullet_state == "ready":
                if event.key == pygame.K_SPACE:
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX = playerX + playerX_change

    # adding player boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # moving bullet
    if bullet_state == "firing":
        bullet(bulletX, bulletY)
        bulletY = bulletY - bulletY_change
        if bulletY <= 0:
            bullet_state = "ready"
            bulletY = 480

    # moving enemies
    for i in range(num_of_enemies):

        # Game Over

        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 1000
            game_over_text()
            break

        enemyX[i] = enemyX[i] + enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.2
            enemyY[i] = enemyY[i] + enemyY_change[i]
        if enemyX[i] >= 736:
            enemyX_change[i] = -0.2
            enemyY[i] = enemyY[i] + enemyY_change[i]

        # collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score = score + 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    show_score()
    player()
    pygame.display.update()
