import pygame
import random
import os  # os是一個方便管理資料的套件
WIDTH  = 500 
HEIGHT = 600  
# 定義長寬
WHITE = (255,255,255)
GREEN = (0, 255, 0)
GREY = (190,190,190)
RED = (255,0,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)
# 定義顏色
# 遊戲初始化 創視窗
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("踩踩踩踩跟我踩")  # 設定名字
minesweeper_img = pygame.image.load(os.path.join("img", "地雷.jpg")).convert()  # 引入照片(os.path是這個檔案(踩地雷)所在位置)
pygame.display.set_icon(minesweeper_img)  # 把左上的小圖標改成上面引入的照片

# 寫字
font_name = pygame.font.match_font('arial')  # 選字體(arial大部分電腦都有)
def draw_text(surf, text, size, x, y):  # surf是要顯示在哪裡,text是要顯示甚麼,size是字大小,xy是顯示的位置
    font = pygame.font.Font(font_name, size)  # 創文字物件
    text_surface = font.render(text, True, BLACK)  # 把文字渲染出來(True的地方是讓字體看起來比較滑順)
    text_rect = text_surface.get_rect()  # 文字定位
    text_rect.centerx = x
    text_rect.top = y  # 定位到輸進來的xy
    surf.blit(text_surface, text_rect)  # 把文字畫出來

# 函式
def draw_game_over(surf):  # 輸了要顯示的東西
    surf.fill(WHITE)
    draw_text(surf, "GAME OVER", 50, WIDTH // 2, HEIGHT // 2 - 50)
    draw_text(surf, "Press R to Restart or Q to Quit", 30, WIDTH // 2, HEIGHT // 2 + 10)
    pygame.display.update()  # 遊戲更新

def draw_victory(surf):  # 贏了要顯示的東西
    surf.fill(WHITE)
    draw_text(surf, "YOU WIN", 50, WIDTH // 2, HEIGHT // 2 - 50)
    draw_text(surf, "Press R to Restart or Q to Quit", 30, WIDTH // 2, HEIGHT // 2 + 10)
    pygame.display.update()  # 遊戲更新

def reset():  # 重新一局
    global Bomb,show_Bomb,detect_floor,flags,count,game_over,victory  # 把這些變數變成全域變數
    # [[0]*10 for i in range(10)]是一個二維陣列,[0]*10 for i in range(10)這個的意思是把每一格都變成0
    Bomb = [[0]*10 for i in range(10)]  # 地雷盤
    show_Bomb =[[0]*10 for i in range(10)]  # 顯示數字的盤
    detect_floor = [[False]*10 for i in range(10)]  # 判斷有沒有被點過的盤
    flags = [[False] * 10 for i in range(10)]  # 旗子(右鍵)的盤
    count = 0  # 已放置的地雷數
    game_over = False
    victory = False
    while(count < num_Bomb):  # 開始佈雷的迴圈
        x = int (random.randrange(0,10))
        y = int (random.randrange(0,10))  # 隨機佈
        if Bomb[x][y] == 0:
            Bomb[x][y] = 1
            count += 1  # 這個是避免重複佈

num_Bomb = 10  # 想玩的總地雷數
reset()

def xy_change(x,y):  # 這個是方便把滑鼠的位置變成格子的xy
    x_new = int(x / 50)
    y_new = int((y-100) / 50)
    x_new,y_new = limit(x_new,y_new)
    return x_new,y_new

def limit(x,y):  # 限制範圍min:0,max:9
    return max(0, min(9, x)), max(0, min(9, y))

def detect_Bomb(x, y):  # 偵測的函式
    global game_over  # 把這變成全域變數
    stack = [(x, y)]  # 使用堆疊來模擬遞迴
    while stack:
        x, y = stack.pop()  # 把xy從堆疊的最上面拿出來
        x, y = limit(x, y)
        if detect_floor[x][y] == False:  # 如果還沒有被偵測過進判斷
            if Bomb[x][y] == 1:  # 如果是地雷
                game_over = True
            count = 0  # 這裡的count是表示點了之後要顯示數字的格子裡的數字
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (i != 0 or j!= 0) :
                        x1 = x+i
                        y1 = y+j
                        if 0 <= x1 <= 9 and 0 <= y1 <= 9:
                            if Bomb[x1][y1]:
                                count += 1  # 這裡是讓他從左上開始偵測有沒有地雷
            if count >= 1:
                show_Bomb[x][y] = count  # 紀錄附近地雷數
            else:
                show_Bomb[x][y] = 0
                for a in range(-1, 2):
                    for b in range(-1, 2):
                        x1,y1 = limit(x+a,y+b)
                        if (x,y) != (x1,y1):  # 避免重複算
                            stack.append((x1,y1))  # 將相鄰格子添加到堆疊中
            detect_floor[x][y] = True
    check_victory()
    return show_Bomb[x][y], detect_floor[x][y]

def check_victory():  # 偵測是不是勝利
    global victory
    for i in range(10):
        for j in range(10):
            if not detect_floor[i][j] and Bomb[i][j] == 0:
                return
    victory = True

def draw_Bomb(surf, x, y):  # 畫方格(擺地雷的位置)
    BAR_LENGTH = 50
    BAR_HEIGHT = 50
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)  # 定義外框
    pygame.draw.rect(surf, BLACK, outline_rect, 2)  # 畫外框

# 主程式
running = True
game_over = False
while running:
    mouse_x,mouse_y = pygame.mouse.get_pos()  # 獲取滑鼠位置
    for event in pygame.event.get():  # 獲取發生的事件
        if event.type == pygame.QUIT:  # 如果按關閉視窗
            running = False
        elif (game_over or victory) and event.type == pygame.KEYDOWN:  # 如果遊戲結束了發生的事件
            if game_over or victory:
                if event.key == pygame.K_r:
                    reset()
                elif event.key == pygame.K_q:
                    running = False
        elif not (game_over or victory) and event.type == pygame.MOUSEBUTTONDOWN:  # 如果遊戲中發生的事件
            if event.button == 1:  # 左鍵按下
                x_new,y_new = xy_change(mouse_x,mouse_y)  # 把滑鼠的xy換成盤子的xy
                if detect_floor[x_new][y_new] == 0 and not flags[x_new][y_new]:  # 如果沒有被觸發跟沒有旗子的話
                        detect_Bomb(x_new,y_new)
                        show_Bomb[x_new][y_new],detect_floor[x_new][y_new] = (detect_Bomb(x_new,y_new))
            elif event.button == 3:  # 右鍵按下
                x_new,y_new = xy_change(mouse_x,mouse_y)
                if not detect_floor[x_new][y_new]:
                    flags[x_new][y_new] = not flags[x_new][y_new]
                          
    # 畫面顯示
    if not game_over and not victory:
        screen.fill(WHITE)
        for size_x in range(10):
            for  size_y in range(10):
                draw_Bomb(screen,50 * size_x,100 +  50 * size_y)
                if detect_floor[size_x][size_y]:  # 判斷detect_floor[size_x][size_y]這格是不是True
                    draw_text(screen,str(show_Bomb[size_x][size_y]),30,50*size_x+25,100+50*size_y+10)
                elif flags[size_x][size_y]:  # 判斷flags[size_x][size_y]這格是不是True
                    draw_text(screen,"*",30,50*size_x+25,100+50*size_y+10)
        remaining_Bombs = num_Bomb - sum(sum(row) for row in flags)  # 計算剩餘地雷數

        draw_text(screen,str(remaining_Bombs),50,50,25)
    pygame.display.update()  # 遊戲更新
    if game_over:
        draw_game_over(screen)
    elif victory:
        draw_victory(screen)

pygame.quit()  # 結束遊戲
