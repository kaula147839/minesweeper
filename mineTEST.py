import random
import numpy as np
running = True
Bomb = [[0]*10 for i in range(10)]#地雷本盤
show_Bomb = [[0]*10 for i in range(10)]#顯示地雷盤
count = 0
while(count <= 10):
    x = int (random.randrange(0,10))
    y = int (random.randrange(0,10))
    if Bomb[x][y] == 0:
        Bomb[x][y] = 1
        count += 1

def detect_Bomb(x,y,check):#創韓式烤布雷
    count = 0
    if Bomb[x][y] == 1:
        print("GG")
        return False
    else:
        for i in range(-1,2):
            for j in range(-1,2):
                x1 = x+i
                y1 = y+j
                if x1 >= 0 and x1 <= 9 and y1 >= 0 and y1 <= 9:
                    if Bomb[x1][y1] == 1:
                        count += 1
        check = bool(1)
        if count >= 1:
            show_Bomb[x][y] = count  #顯示地雷數
        else:
            for a in range(-1,2):
                for b in range(-1,2):
                    x_new = x + a
                    y_new = y + b 
                    if x_new > 9 :
                        x_new = 9 
                    if x_new < 0 :
                        x_new = 0 
                    if y_new > 9 :
                        y_new = 9 
                    if y_new < 0 :
                        y_new = 0 
                    detect_Bomb(x_new,y_new,0)
        return True
while(running == True):
    print(np.array(Bomb),"\n")
    print(np.array(show_Bomb))
    x = int (input())
    y = int (input())
    running = detect_Bomb(x,y,0)

