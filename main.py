import pygame
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

BG = pygame.transform.scale(pygame.image.load('bg.jpeg'), (WIDTH,HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5

BOLT_WIDTH = 10
BOLT_HEIGHT = 20
BOLT_VEL = 5

FONT = pygame.font.SysFont("comicsans", 30)

def draw(player, elapsed_time, bolts):
    WIN.blit(BG,(0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))
    
    pygame.draw.rect(WIN, "red", player)

    for bolt in bolts:
        pygame.draw.rect(WIN, "white", bolt)

    pygame.display.update()


def main():
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, 
                         PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    bolt_add_increment = 2000
    bolt_count = 0

    bolts = []
    hit = False

    while run:
        bolt_count += clock.tick(144)

        elapsed_time = time.time() - start_time

        if bolt_count > bolt_add_increment:
            for _ in range(3):
                bolt_x = random.randint(0, WIDTH - BOLT_WIDTH)
                bolt = pygame.Rect(bolt_x, -BOLT_HEIGHT, BOLT_WIDTH, BOLT_HEIGHT)
                bolts.append(bolt)

            bolt_add_increment = max(200, bolt_add_increment - 50)
            bolt_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break


        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        elif keys[pygame.K_d] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL
            
        for bolt in bolts[:]:
            bolt.y += BOLT_VEL
            if bolt.y > HEIGHT:
                bolts.remove(bolt)
            elif bolt.y + bolt.height >= player.y and bolt.colliderect(player):
                bolts.remove(bolt)
                hit = True
                break


        if hit:
            lost_text = FONT.render("You Lost!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break
        
        draw(player, elapsed_time, bolts)


    pygame.quit()

if __name__ == "__main__":
    main()