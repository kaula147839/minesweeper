import pygame
import random

FPS = 60
WIDTH = 500
HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)


def draw_game_over(surf):
    surf.fill(WHITE)
    draw_text(surf, "GAME OVER", 50, WIDTH // 2, HEIGHT // 2 - 50)
    draw_text(surf, "Press R to Restart or Q to Quit", 30, WIDTH // 2, HEIGHT // 2 + 10)
    pygame.display.update()


def reset():
    global Bomb, show_Bomb, detect_floor, flags, count, game_over
    Bomb = [[0] * 10 for _ in range(10)]
    show_Bomb = [[0] * 10 for _ in range(10)]
    detect_floor = [[False] * 10 for _ in range(10)]
    flags = [[False] * 10 for _ in range(10)]
    count = 0
    game_over = False
    while count < num_Bomb:
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        if Bomb[x][y] == 0:
            Bomb[x][y] = 1
            count += 1


num_Bomb = 10
reset()


def xy_change(x, y):
    x_new = int(x / 50)
    y_new = int((y - 100) / 50)
    x_new, y_new = limit(x_new, y_new)
    return x_new, y_new


def limit(x, y):
    return max(0, min(9, x)), max(0, min(9, y))


def detect_Bomb(x, y):
    global count, game_over
    count = 0
    stack = [(x, y)]
    while stack:
        x, y = stack.pop()
        x, y = limit(x, y)
        if not detect_floor[x][y]:
            if Bomb[x][y] == 1:
                game_over = True
                return show_Bomb[x][y], detect_floor[x][y]
            for i in range(-1, 2):
                for j in range(-1, 2):
                    x1, y1 = limit(x + i, y + j)
                    if Bomb[x1][y1]:
                        count += 1
            if count >= 1:
                show_Bomb[x][y] = count
            else:
                show_Bomb[x][y] = 0
                for a in range(-1, 2):
                    for b in range(-1, 2):
                        x1, y1 = limit(x + a, y + b)
                        if (x, y) != (x1, y1) and not detect_floor[x1][y1] and show_Bomb[x1][y1] == 0:
                            stack.append((x1, y1))
            detect_floor[x][y] = True
    return show_Bomb[x][y], detect_floor[x][y]


def draw_Bomb(surf, x, y):
    BAR_LENGTH = 50
    BAR_HEIGHT = 50
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    pygame.draw.rect(surf, BLACK, outline_rect, 2)


running = True
game_over = False
while running:
    clock.tick(FPS)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset()
            elif event.key == pygame.K_q:
                running = False
        elif not game_over and pygame.mouse.get_pressed(num_buttons=3)[0]:
            x_new, y_new = xy_change(mouse_x, mouse_y)
            if detect_floor[x_new][y_new] == 0 and not flags[x_new][y_new]:
                detect_Bomb(x_new, y_new)
                show_Bomb[x_new][y_new], detect_floor[x_new][y_new] = detect_Bomb(x_new, y_new)
        elif not game_over and pygame.mouse.get_pressed(num_buttons=3)[2]:
            x_new, y_new = xy_change(mouse_x, mouse_y)
            if not detect_floor[x_new][y_new]:
                flags[x_new][y_new] = not flags[x_new][y_new]

    if not game_over:
        screen.fill(WHITE)
        for size_x in range(10):
            for size_y in range(10):
                draw_Bomb(screen, 50 * size_x, 100 + 50 * size_y)
                if detect_floor[size_x][size_y]:
                    draw_text(screen, str(show_Bomb[size_x][size_y]), 30, 50 * size_x + 10, 100 + 50 * size_y + 10)
                elif flags[size_x][size_y]:
                    draw_text(screen, "*", 30, 50 * size_x + 10, 100 + 50 * size_y + 10)
        remaining_Bombs = num_Bomb - sum(sum(row) for row in flags)
        draw_text(screen, str(remaining_Bombs), 50, 50, 25)
    pygame.display.update()
    if game_over:
        draw_game_over(screen)
pygame.quit()
