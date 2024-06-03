import pygame
import random
import os
FPS = 60
WIDTH  = 500 
HEIGHT = 600  

WHITE = (255,255,255)
GREEN = (0, 255, 0)
GREY = (190,190,190)
RED = (255,0,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)
#遊戲初始化 創視窗
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("踩踩踩踩跟我踩")
minesweeper_img = pygame.image.load(os.path.join("img", "地雷.jpg")).convert()
pygame.display.set_icon(minesweeper_img)
clock = pygame.time.Clock()

#寫字
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

#韓式烤布蕾
def draw_game_over(surf):#畫布丁輸
    surf.fill(WHITE)
    draw_text(surf, "GAME OVER", 50, WIDTH // 2, HEIGHT // 2 - 50)
    draw_text(surf, "Press R to Restart or Q to Quit", 30, WIDTH // 2, HEIGHT // 2 + 10)
    pygame.display.update()

def draw_victory(surf):#畫烤布蕾贏
    surf.fill(WHITE)
    draw_text(surf, "YOU WIN", 50, WIDTH // 2, HEIGHT // 2 - 50)
    draw_text(surf, "Press R to Restart or Q to Quit", 30, WIDTH // 2, HEIGHT // 2 + 10)
    pygame.display.update()
#重吃一盤烤布蕾
def reset():
    global Bomb,show_Bomb,detect_floor,flags,count,game_over,victory
    Bomb = [[0]*10 for i in range(10)]#地雷本盤
    show_Bomb =[[0]*10 for i in range(10)]#顯示地雷盤
    detect_floor = [[False]*10 for i in range(10)]#偵測盤
    flags = [[False] * 10 for i in range(10)]
    count = 0
    game_over = False
    victory = False
    while(count < num_Bomb):
        x = int (random.randrange(0,10))
        y = int (random.randrange(0,10))
        if Bomb[x][y] == 0:
            Bomb[x][y] = 1
            count += 1

num_Bomb = 10
reset()
def xy_change(x,y):
    x_new = int(x / 50)
    y_new = int((y-100) / 50)
    x_new,y_new = limit(x_new,y_new)
    return x_new,y_new

def limit(x,y):#限制範圍min:0,max:9
    return max(0, min(9, x)), max(0, min(9, y))
#主菜布蕾
def detect_Bomb(x, y):
    global game_over
    stack = [(x, y)]  # 使用堆疊來模擬遞迴
    while stack:
        x, y = stack.pop()
        x, y = limit(x, y)
        if detect_floor[x][y] == False:
            if Bomb[x][y] == 1:
                game_over = True
                return show_Bomb[x][y],detect_floor[x][y]
            count = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (i != 0 or j!= 0) :
                        x1 = x+i
                        y1 = y+j
                        # x1,y1 = limit(x+i,y+j)
                        if 0 <= x1 <= 9 and 0 <= y1 <= 9:
                            if Bomb[x1][y1]:
                                count += 1
            if count >= 1:
                show_Bomb[x][y] = count
            else:
                show_Bomb[x][y] = 0
                for a in range(-1, 2):
                    for b in range(-1, 2):
                        x1,y1 = limit(x+a,y+b)
                        if (x,y) != (x1,y1):
                            stack.append((x1,y1))  # 將相鄰格子添加到堆疊中
            detect_floor[x][y] = True
    check_victory()
    return show_Bomb[x][y], detect_floor[x][y]

#勝利烤布蕾
def check_victory():
    global victory
    for i in range(10):
        for j in range(10):
            if not detect_floor[i][j] and Bomb[i][j] == 0:
                return
    victory = True
#畫烤布蕾的盤子
def draw_Bomb(surf, x, y):
    BAR_LENGTH = 50
    BAR_HEIGHT = 50
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)#定義外框
    pygame.draw.rect(surf, BLACK, outline_rect, 2)#畫外框

#吃烤布蕾
running = True
game_over = False
while running:
    clock.tick(FPS)
    mouse_x,mouse_y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif (game_over or victory) and event.type == pygame.KEYDOWN:
            if game_over or victory:
                if event.key == pygame.K_r:
                    reset()
                elif event.key == pygame.K_q:
                    running = False
        elif not (game_over or victory) and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x_new,y_new = xy_change(mouse_x,mouse_y)
                if detect_floor[x_new][y_new] == 0 and not flags[x_new][y_new]:   
                        detect_Bomb(x_new,y_new)
                        show_Bomb[x_new][y_new],detect_floor[x_new][y_new] = (detect_Bomb(x_new,y_new))
            elif event.button == 3:
                x_new,y_new = xy_change(mouse_x,mouse_y)
                if not detect_floor[x_new][y_new]:
                    flags[x_new][y_new] = not flags[x_new][y_new]
                          
    #畫面顯示
    if not game_over and not victory:
        screen.fill(WHITE)
        for size_x in range(10):
            for  size_y in range(10):
                draw_Bomb(screen,50 * size_x,100 +  50 * size_y)
                if detect_floor[size_x][size_y]:            
                    draw_text(screen,str(show_Bomb[size_x][size_y]),30,50*size_x+25,100+50*size_y+10)
                elif flags[size_x][size_y]:
                    draw_text(screen,"*",30,50*size_x+25,100+50*size_y+10)
        remaining_Bombs = num_Bomb - sum(sum(row) for row in flags)

        draw_text(screen,str(remaining_Bombs),50,50,25)
    pygame.display.update()
    if game_over:
        draw_game_over(screen)
    elif victory:
        draw_victory(screen)

pygame.quit() 
