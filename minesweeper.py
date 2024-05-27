import pygame
import random
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
show_Bomb =[[0]*10 for i in range(10)]#顯示地雷盤
detect_floor = [[0]*10 for i in range(10)]#偵測盤
count = 0
#烤布雷
def limit(x,y):#限制範圍min:0,max:9
    if x < 0:
        x = 0
    if x > 9:
        x = 9
    if y < 0:
        y = 0
    if y > 9:
        y = 9
    return x,y
while(count <= 10):
    x = int (random.randrange(0,10))
    y = int (random.randrange(0,10))
    if Bomb[x][y] == 0:
        Bomb[x][y] = 1
        count += 1
for i in range(10):
    for j in range(10):
        show_Bomb[i][j] = 0
count = 0
def detect_Bomb(x,y):#創韓式烤布雷
    x,y = limit(x,y)
    if Bomb[x][y] == 1:
        running = False
        #return running
    elif show_Bomb[x][y] == -1:
        for i in range(-1,2):
            for j in range(-1,2):
                x1 = x+i
                y1 = y+j
                if x1 >= 0 and x1 <= 9 and y1 >= 0 and y1 <= 9:
                    if Bomb[x1][y1] == 1:
                        count += 1
        if count >= 1:
            show_Bomb[x][y] = count  #顯示地雷數
            return show_Bomb[x][y]
        else:
            show_Bomb[x][y] = 0
            for a in range(-1,2):
                for b in range(-1,2):
                    detect_Bomb(x+a,y+b)
        detect_floor[x][y] = True
        return detect_floor[x][y]

def draw_Bomb(surf, x, y):#畫烤布雷的底盤
    BAR_LENGTH = 50
    BAR_HEIGHT = 50
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)#定義外框
    pygame.draw.rect(surf, BLACK, outline_rect, 2)#畫外框



#迴圈
running = True

while running:
    clock.tick(FPS)
    mouse_x,mouse_y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif pygame.mouse.get_pressed(num_buttons=3)[0] == True:
            if mouse_y > 100:
                x_new = int(mouse_x / 50)
                y_new = int((mouse_y-100) / 50)
                x_new,y_new = limit(x_new,y_new)
                if detect_floor[x_new][y_new] == 0:   
                    detect_Bomb(x_new,y_new)
                    show_Bomb[:][:],detect_floor[:][:] = (detect_Bomb(x_new,y_new))
                          
    #畫面顯示
    screen.fill(WHITE)
    for size_x in range(10):
        for  size_y in range(10):
            draw_Bomb(screen,50 * size_x,100 +  50 * size_y)
    x_new = int(mouse_x / 50)
    y_new = int((mouse_y-100) / 50)
    x_new,y_new = limit(x_new,y_new)
    if  detect_floor[x_new][y_new] == True:
        for i in range(10):
            for  j in range(10):
                draw_text(screen,str(show_Bomb[i][j]),30,50*i+10,100+50*j+10)
    draw_text(screen, str(mouse_x),18,WIDTH/2,10)
    draw_text(screen, str(mouse_y),18,WIDTH/2+25,10)
    draw_text(screen, str(pygame.mouse.get_pressed(num_buttons=3)[0]),18,WIDTH/2,28)

    pygame.display.update()
while running == 0:
    draw_text(screen,str("GAME OVER"),40,WIDTH/2,HEIGHT/2) 
pygame.quit() 
