import pygame
import random

# 定義顏色
WHITE = (255, 255, 255)
GREY = (192, 192, 192)
DARK_GREY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 初始化遊戲
pygame.init()

# 設置遊戲畫布的大小
WIDTH, HEIGHT = 600, 600  # 調整視窗大小
CELL_SIZE = 40
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE

# 創建遊戲畫布
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("踩地雷")

# 生成地雷的位置
mines = []
for _ in range(30):  # 30個地雷
    mines.append((random.randint(0, ROWS - 1), random.randint(0, COLS - 1)))

# 計算鄰近地雷數
def count_adjacent_mines(row, col):
    count = 0
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            r = row + dr
            c = col + dc
            if (0 <= r < ROWS and 0 <= c < COLS and (r, c) in mines):
                count += 1
    return count

# 獲取空白區域
def get_blank_area(row, col):
    blank_area = set()
    stack = [(row, col)]
    while stack:
        r, c = stack.pop()
        if (r, c) not in blank_area and 0 <= r < ROWS and 0 <= c < COLS:
            blank_area.add((r, c))
            if count_adjacent_mines(r, c) == 0:
                for dr in range(-1, 2):
                    for dc in range(-1, 2):
                        stack.append((r + dr, c + dc))
    return blank_area


# 繪製地雷板
def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            color = GREY
            if (row, col) in revealed:
                color = BLACK
                if (row, col) in mines:
                    pygame.draw.rect(screen, (255, 0, 0), (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                else:
                    count = count_adjacent_mines(row, col)
                    if count > 0:
                        font = pygame.font.Font(None, 30)  # 改變字體大小
                        text = font.render(str(count), True, BLACK)
                        text_rect = text.get_rect(center=(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2))  # 設置文字位置
                        screen.blit(text, text_rect)
                    else:
                        pygame.draw.rect(screen, WHITE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif (row, col) in flags:
                pygame.draw.rect(screen, RED, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)


# 繪製重新開始按鈕
def draw_restart_button():
    pygame.draw.rect(screen, GREY, (200, 200, 200, 100))
    font = pygame.font.Font(None, 40)
    text = font.render("Restart", True, BLACK)
    text_rect = text.get_rect(center=(300, 250))
    screen.blit(text, text_rect)

# 主遊戲循環
revealed = set()
flags = set()
game_over = False
game_over_time = None
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            row = pos[1] // CELL_SIZE
            col = pos[0] // CELL_SIZE
            if not game_over:
                if event.button == 1:  # 左鍵點擊
                    if (row, col) not in revealed and (row, col) not in flags:
                        if (row, col) in mines:
                            game_over = True
                            game_over_time = pygame.time.get_ticks()
                        else:
                            blank_area = get_blank_area(row, col)
                            revealed |= blank_area
                elif event.button == 3:  # 右鍵點擊
                    if (row, col) not in revealed:
                        if (row, col) in flags:
                            flags.remove((row, col))  # 移除旗子
                        else:
                            flags.add((row, col))  # 放置旗子
            else:
                if game_over_time is not None and pygame.time.get_ticks() - game_over_time >= 2000:
                    # 顯示重新開始按鈕
                    if 200 <= pos[0] <= 400 and 200 <= pos[1] <= 300:
                        # 檢查重新開始按鈕是否被點擊
                        mines = []
                        for _ in range(30):
                            mines.append((random.randint(0, ROWS - 1), random.randint(0, COLS - 1)))
                        revealed = set()
                        flags = set()
                        game_over = False

    screen.fill(WHITE)  # 填充背景色

    # 滑鼠滑道的區域變成深色
    pos = pygame.mouse.get_pos()
    row = pos[1] // CELL_SIZE
    col = pos[0] // CELL_SIZE
    if 0 <= row < ROWS and 0 <= col < COLS:
        pygame.draw.rect(screen, DARK_GREY, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # 繪製地雷板
    draw_board()

    if game_over:
        # 繪製 "Game Over" 文字
        font = pygame.font.Font(None, 60)
        text = font.render("Game Over", True, RED)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(text, text_rect)
        # 繪製重新開始按鈕
        if game_over_time is not None and pygame.time.get_ticks() - game_over_time >= 2000:
            draw_restart_button()

    pygame.display.flip()

pygame.quit()