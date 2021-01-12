from time import sleep
import numpy as np
import random
import copy
import os


def formatmap(num):
    global x, y
    x = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    y = [9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
    map1[num][y[num]][x[num]] = 2
    for i in range(10):
        if i % 2 == 0:
            for j in range(7):
                map1[num][i][j] = 1
                map1[num][i][j] = 1
            map1[num][i][random.randrange(1, 6)] = 0
    for i in range(10):
        map1[num][i][0] = 1
        map1[num][i][6] = 1


def findhole(num):
    hole = 0
    count = 0
    for i in range(7):
        if map1[num][y[num] - 1][i] == 0:
            hole = i
            count += 1
    if count > 1:
        return 99
    return hole


def runchromo(num, i):
    global chromo
    if chromo[num][i] == 0:
        return 0
    elif chromo[num][i] == 1:
        return 1
    elif chromo[num][i] == 2:
        return 2


def showmap():
    global gene, chromo, select
    os.system("cls")
    print(f"GEN : {gene}")
    print(chromo)
    print(select)
    for i in range(10):
        for h in range(10):
            for j in range(7):
                if map1[h][i][j] == 1:
                    print("■", end=" ")
                elif map1[h][i][j] == 2:
                    print("★", end=" ")
                else:
                    print("□", end=" ")
            print(" ", end=" ")
        print("\n")


def left(num):
    global x, y
    try:
        if map1[num][y[num]][x[num] - 1] == 0:
            map1[num][y[num]][x[num]] = 0
            x[num] -= 1
            map1[num][y[num]][x[num]] = 2
    except IndexError:
        pass


def right(num):
    global x, y
    try:
        if map1[num][y[num]][x[num] + 1] == 0:
            map1[num][y[num]][x[num]] = 0
            x[num] += 1
            map1[num][y[num]][x[num]] = 2
    except IndexError:
        pass


def up(num):
    global x, y
    try:
        if map1[num][y[num] - 1][x[num]] == 0:
            map1[num][y[num]][x[num]] = 0
            y[num] -= 1
            map1[num][y[num]][x[num]] = 2
    except IndexError:
        pass


def down(num):
    global x, y
    try:
        if map1[num][y[num] + 1][x[num]] == 0:
            map1[num][y[num]][x[num]] = 0
            y[num] += 1
            map1[num][y[num]][x[num]] = 2
    except IndexError:
        pass


chromo = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
          [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]  # 0 = up, 1 = left, 2= right
new_chromo = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
              [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]  # 마지막은 y의 좌표
for i in range(10):
    for j in range(3):
        chromo[i][j] = random.randint(0, 2)
count = 0
num = 0
hole = 0
mutation = 0.1  # 돌연변이가 나타날 확률
select = [0, 0]  # 선택된 우성 염색체
gene = 0  # 세대
rank = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
x = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
y = [9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
x_1 = x
y_1 = y
map1 = np.zeros([10, 10, 7])  # 3차원 배열 설정

while True:
    map1 = np.zeros([10, 10, 7])
    for i in range(10):
        formatmap(i)  # 맵들 전체 설정
    showmap()
    for start in range(27):
        for num in range(10):
            hole = findhole(num)
            if y[num] == 0:
                continue
            elif x[num] == hole:
                if runchromo(num, 0) == 0:
                    up(num)
                elif runchromo(num, 0) == 1:
                    left(num)
                elif runchromo(num, 0) == 2:
                    right(num)
            elif hole == 99:
                if runchromo(num, 0) == 0:
                    up(num)
                elif runchromo(num, 0) == 1:
                    left(num)
                elif runchromo(num, 0) == 2:
                    right(num)
            elif x[num] > hole:
                if runchromo(num, 1) == 0:
                    up(num)
                elif runchromo(num, 1) == 1:
                    left(num)
                elif runchromo(num, 1) == 2:
                    right(num)
            elif x[num] < hole:
                if runchromo(num, 2) == 0:
                    up(num)
                elif runchromo(num, 2) == 1:
                    left(num)
                elif runchromo(num, 2) == 2:
                    right(num)
            chromo[num][3] = y[num]
            rank[num] = chromo[num][3]
        showmap()
        sleep(0.25)
        if x[:] == x_1[:] and y[:] == y_1[:]:
            break
        x_1[:] = x[:]
        y_1[:] = y[:]

    if rank == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
        showmap()
        print("끝")
        break
    for i in range(2):
        select[i] = np.argsort(rank)[i]  # 우수 유전자 추출
    for i in range(10):
        for j in range(3):
            if random.random() < mutation:  # 돌연변이 발생
                new_chromo[i][j] = random.randint(0, 2)
            else:
                new_chromo[i][j] = chromo[select[random.randint(0, 1)]][j]
    chromo = copy.deepcopy(new_chromo)
    gene += 1
    if gene > 100:
        break
showmap()
print("끝")
