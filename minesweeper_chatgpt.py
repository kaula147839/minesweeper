import pygame
import random

FPS = 60
WIDTH, HEIGHT = 500, 600

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

Bomb = [[0]*10 for _ in range(10)]
show_Bomb = [[0]*10 for _ in range(10)]
detect_floor = [[0]*10 for _ in range(10)]

def limit(x, y):
    return max(0, min(9, x)), max(0, min(9, y))

count = 0
while count < 10:
    x, y = random.randrange(10), random.randrange(10)
    if Bomb[x][y] == 0:
        Bomb[x][y] = 1
        count += 1

for i in range(10):
    for j in range(10):
        show_Bomb[i][j] = 0
        detect_floor[i][j] = False

def detect_Bomb(x, y):
    global count
    stack = [(x, y)]
    while stack:
        x, y = stack.pop()
        x, y = limit(x, y)
        if detect_floor[x][y] == False:
            count = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    x1, y1 = limit(x + i, y + j)
                    if Bomb[x1][y1] == 1:
                        count += 1
            if count > 0:
                show_Bomb[x][y] = count
            else:
                show_Bomb[x][y] = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        x1, y1 = limit(x + i, y + j)
                        if (x1, y1) != (x, y):
                            stack.append((x1, y1))
            detect_floor[x][y] = True
    return show_Bomb[x][y], detect_floor[x][y]

def draw_Bomb(surf, x, y):
    BAR_LENGTH = 50
    BAR_HEIGHT = 50
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    pygame.draw.rect(surf, BLACK, outline_rect, 2)

running = True

while running:
    clock.tick(FPS)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif pygame.mouse.get_pressed(num_buttons=3)[0]:
            x_new = mouse_x // 50
            y_new = (mouse_y - 100) // 50
            x_new, y_new = limit(x_new, y_new)
            if not detect_floor[x_new][y_new]:   
                detect_Bomb(x_new, y_new)
                          
    screen.fill(WHITE)
    for size_x in range(10):
        for size_y in range(10):
            draw_Bomb(screen, 50 * size_x, 100 + 50 * size_y)
    
    for i in range(10):
        for j in range(10):
            if detect_floor[i][j]:
                draw_text(screen, str(show_Bomb[i][j]), 30, 50*i+25, 100+50*j+10)
    
    draw_text(screen, str(mouse_x), 18, WIDTH/2, 10)
    draw_text(screen, str(mouse_y), 18, WIDTH/2+25, 10)
    draw_text(screen, str(pygame.mouse.get_pressed(num_buttons=3)[0]), 18, WIDTH/2, 28)

    pygame.display.update()

pygame.quit()
