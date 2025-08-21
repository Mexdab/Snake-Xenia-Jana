import pygame, random
from pygame.locals import *

pygame.init()

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CELL_SIZE = 20  # size of each snake block
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load("final.png")  # game icon
pygame.display.set_icon(icon)
pygame.display.set_caption("Snake Xenia")

# Background image
bg = pygame.image.load("mback.png")  # background
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Food image (rat)
food_img = pygame.image.load("rat.png")  # rat image
FOOD_SIZE = 30  # bigger rat size
food_img = pygame.transform.scale(food_img, (FOOD_SIZE, FOOD_SIZE))

# Snake image
snake_img = pygame.image.load("snake_icon.jpg").convert_alpha()  # snake body
snake_img = pygame.transform.scale(snake_img, (CELL_SIZE, CELL_SIZE))

# Sound effect when rat eaten
eat_sound = pygame.mixer.Sound("audio.mp3")  # squeak sound

# Colors
WHITE = (255, 255, 255)

# Font
font = pygame.font.SysFont("Arial", 36)

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Snake and food setup
snake = [(100, 100), (80, 100), (60, 100)]  # initial 3 segments
direction = "RIGHT"
food = (random.randrange(0, SCREEN_WIDTH // CELL_SIZE) * CELL_SIZE,
        random.randrange(0, SCREEN_HEIGHT // CELL_SIZE) * CELL_SIZE)

clock = pygame.time.Clock()
run = True
game_over = False

score = 0
speed = 10

while run:
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == KEYDOWN:
            if event.key == K_UP and direction != "DOWN":
                direction = "UP"
            if event.key == K_DOWN and direction != "UP":
                direction = "DOWN"
            if event.key == K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            if event.key == K_RIGHT and direction != "LEFT":
                direction = "RIGHT"

    if not game_over:
        # Move snake head
        x, y = snake[0]
        if direction == "UP":
            y -= CELL_SIZE
        if direction == "DOWN":
            y += CELL_SIZE
        if direction == "LEFT":
            x -= CELL_SIZE
        if direction == "RIGHT":
            x += CELL_SIZE
        new_head = (x, y)

        # Check collisions
        if (x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT or new_head in snake):
            game_over = True
        else:
            snake.insert(0, new_head)
            # Check if food eaten
            if new_head == food:
                score += 1
                if score % 5 == 0:  # increase speed every 5 rats
                    speed += 1
                eat_sound.play()  # play squeak sound
                food = (random.randrange(0, SCREEN_WIDTH // CELL_SIZE) * CELL_SIZE,
                        random.randrange(0, SCREEN_HEIGHT // CELL_SIZE) * CELL_SIZE)
            else:
                snake.pop()  # remove tail if no food eaten

        # Draw food (rat, centered in grid cell)
        screen.blit(food_img, (food[0] - (FOOD_SIZE - CELL_SIZE)//2,
                               food[1] - (FOOD_SIZE - CELL_SIZE)//2))

        # Draw snake (with image)
        for segment in snake:
            screen.blit(snake_img, (segment[0], segment[1]))

        # Draw score
        draw_text(f"Score: {score}", font, WHITE, SCREEN_WIDTH - 150, 20)

    else:
        draw_text("GAME OVER!", font, WHITE, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20)
        draw_text("Click Anywhere Or Press SPACE To Restart", font, WHITE, SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 2 + 20)

        restart = pygame.mouse.get_pressed()[0]
        keys = pygame.key.get_pressed()
        if restart or keys[K_SPACE]:  # restart with mouse click or SPACE key
            snake = [(100, 100), (80, 100), (60, 100)]
            direction = "RIGHT"
            food = (random.randrange(0, SCREEN_WIDTH // CELL_SIZE) * CELL_SIZE,
                    random.randrange(0, SCREEN_HEIGHT // CELL_SIZE) * CELL_SIZE)
            score = 0
            speed = 10
            game_over = False

    pygame.display.update()
    clock.tick(speed)  # controls snake speed

pygame.quit()



