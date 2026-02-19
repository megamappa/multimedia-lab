import pygame
import random
import sys
import os

# INIT
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge - Advanced")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 26)
big_font = pygame.font.SysFont("Arial", 60)

WHITE = (255,255,255)
RED = (220,50,50)
BLACK = (15,15,15)
CYAN = (0,255,255)

# # LOAD ASSET
rocket_img = pygame.transform.scale(
    pygame.image.load("roket.png").convert_alpha(), (70, 80))

meteor_img = pygame.transform.scale(
    pygame.image.load("meteor.png").convert_alpha(), (50, 50))

explosion_img = pygame.transform.scale(
    pygame.image.load("explosion.png").convert_alpha(), (60, 60))

laser_sound = pygame.mixer.Sound("laser.wav")
explosion_sound = pygame.mixer.Sound("explosion.wav")


# HIGH SCORE
if not os.path.exists("highscore.txt"):
    with open("highscore.txt", "w") as f:
        f.write("0")

with open("highscore.txt", "r") as f:
    high_score = int(f.read())

# PLAYER
player_rect = rocket_img.get_rect(center=(WIDTH//2, HEIGHT-100))
player_speed = 7

# LASER
lasers = []
laser_speed = 10

# METEOR & EXPLOSION
meteors = []
explosions = []
meteor_speed = 3

def spawn_meteor():
    x = random.randint(0, WIDTH-50)
    y = random.randint(-150, -50)
    meteors.append(pygame.Rect(x, y, 50, 50))

# RESET GAME
def reset_game():
    global meteors, lasers, explosions, game_over
    global start_time, kill_score, meteor_speed
    meteors.clear()
    lasers.clear()
    explosions.clear()
    kill_score = 0
    start_time = pygame.time.get_ticks()
    meteor_speed = 5
    game_over = False
    player_rect.centerx = WIDTH // 2

# SCORE
start_time = pygame.time.get_ticks()
kill_score = 0
game_over = False
running = True

# GAME LOOP
while running:
    clock.tick(60)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_SPACE:
                laser = pygame.Rect(
                    player_rect.centerx - 3,
                    player_rect.top,
                    6, 20)
                lasers.append(laser)
                laser_sound.play()

    keys = pygame.key.get_pressed()

    # GAME OVER
    if game_over:
        if score > high_score:
            high_score = score
            with open("highscore.txt","w") as f:
                f.write(str(high_score))

        go = big_font.render("GAME OVER", True, RED)
        sc = font.render(f"Skor: {score}", True, WHITE)
        hs = font.render(f"High Score: {high_score}", True, WHITE)
        r = font.render("Tekan R untuk Restart", True, WHITE)
        e = font.render("ESC untuk Keluar", True, WHITE)

        screen.blit(go,(WIDTH//2-go.get_width()//2,200))
        screen.blit(sc,(WIDTH//2-sc.get_width()//2,270))
        screen.blit(hs,(WIDTH//2-hs.get_width()//2,310))
        screen.blit(r,(WIDTH//2-r.get_width()//2,350))
        screen.blit(e,(WIDTH//2-e.get_width()//2,390))

        if keys[pygame.K_r]:
            reset_game()
        if keys[pygame.K_ESCAPE]:
            running = False

        pygame.display.flip()
        continue

    # PLAYER MOVE
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
        player_rect.x += player_speed

    # SPAWN METEOR
    if random.randint(1, 30) == 1:
        spawn_meteor()

    # METEOR MOVE
    for meteor in meteors[:]:
        meteor.y += meteor_speed

        if meteor.top > HEIGHT:
            meteors.remove(meteor)

        if meteor.colliderect(player_rect):
            explosion_sound.play()
            game_over = True

    # LASER MOVE & HIT
    for laser in lasers[:]:
        laser.y -= laser_speed

        if laser.bottom < 0:
            lasers.remove(laser)

        for meteor in meteors[:]:
            if laser.colliderect(meteor):
                explosion_sound.play()
                meteors.remove(meteor)
                lasers.remove(laser)
                explosions.append(meteor.copy())
                kill_score += 5
                break

    # EXPLOSION DRAW
    for exp in explosions[:]:
        screen.blit(explosion_img, exp)
        explosions.remove(exp)

    # SCORE SYSTEM
    time_score = (pygame.time.get_ticks() - start_time) // 1000
    score = time_score + kill_score
    meteor_speed = 5 + score // 20

    # DRAW
    screen.blit(rocket_img, player_rect)

    for meteor in meteors:
        screen.blit(meteor_img, meteor)

    for laser in lasers:
        pygame.draw.rect(screen, CYAN, laser)

    screen.blit(font.render(f"Skor: {score}", True, WHITE), (10,10))
    screen.blit(font.render(f"High: {high_score}", True, WHITE), (10,40))

    pygame.display.flip()

pygame.quit()
sys.exit()
