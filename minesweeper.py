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
pygame.display.set_caption("minesweeper")
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

#烤布雷

Bomb = [[0]*10 for i in range(10)]#地雷本盤
show_Bomb = [[0]*10 for i in range(10)]#顯示地雷盤
count = 0
while(count <= 15):
    x = random.randrange(0,10)
    y = random.randrange(0,10)
    if Bomb[x][y] == 0:
        Bomb[x][y] = 1
        count += 1
count = 0
def detect_Bomb(x,y):#創韓式烤布雷
    if Bomb[x][y] == 1:
        running = False
    else:
        for i in range(-1,2):
            for j in range(-1,2):
                if Bomb[x+i][y+j] == 1:
                    count += 1
        if count >= 1:
            show_Bomb[x][y] = count#顯示是否有地雷
        else:
            for a in range(-1,2):
                for b in range(-1,2):
                    detect_Bomb(x+a,y+b)


        


#迴圈
running = True

while running:
    clock.tick(FPS)
    mouse_x,mouse_y= pygame.mouse.get_pos()
    mouse_press = pygame.mouse.get_pressed()

    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    #更新遊戲
    #畫面顯示
    screen.fill(WHITE)
    draw_text(screen, str(mouse_x),18,WIDTH/2,10)
    draw_text(screen, str(mouse_y),18,WIDTH/2-10,10)
    draw_text(screen, str(mouse_press),18,WIDTH/2,28)

    pygame.display.update()
pygame.quit() 