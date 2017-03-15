# coding: utf-8

import curses
from random import randint

#map and score
HEIGHT=10
WIDTH =30
score=0
pointsum = HEIGHT*WIDTH
board=[0]*pointsum
BLANKMARK= HEIGHT*WIDTH+5

#foodinf
FOODMARK=0
foodindex=5*WIDTH+5

#snakeinf
HEAD=0
size=1
SNAKEMARK=pointsum*2 +1 
snake = [0] * (pointsum +1)
snake[HEAD] = 1*WIDTH+1

#direction
LEFT=-1
RIGHT=1
UP=-WIDTH
DOWN=WIDTH
direction = [LEFT,RIGHT,UP,DOWN]
key = 0
nextstep=LEFT
ERROR=-5

def board_reset(snake,foodindex,board):
    global size,pointsum
    for i in xrange(pointsum):
        if i in snake[:size]:
            board[i] = SNAKEMARK
        elif i==foodindex:
            board[i] = FOODMARK
        else:
            board[i] = BLANKMARK

def canmove(initidx,dir):
    flag=False
    if dir==LEFT:
        flag = True if initidx%WIDTH >1 else False
    elif dir==RIGHT:
        flag = True if initidx%WIDTH <WIDTH - 2 else False
    elif dir==UP:
        flag = True if initidx/WIDTH >1 else False
    elif dir==DOWN:
        flag = True if initidx/WIDTH <HEIGHT - 2 else False
    return flag

def Breadth_First_Search(snake,foodindex,board):
    global direction,pointsum
    fakeboard = [0] *pointsum
    searchpoion=[]
    searchpoion.append(foodindex)
    flag = False
    while len(searchpoion) != 0:
        idx = searchpoion.pop()
        fakeboard[idx] = 1
        for i in xrange(4):
            if canmove(idx,direction[i]):
                if idx + direction[i] == snake[HEAD]:
                    flag = True
                if board[idx+direction[i]] != SNAKEMARK:
                    if board[idx+direction[i]]>board[idx]+1:
                        board[idx+direction[i]] = board[idx]+1
                    if fakeboard[idx+direction[i]] == 0:
                        searchpoion.append(idx+direction[i])
    return flag

def find_short_way(snake,board):
    global direction
    short = SNAKEMARK
    finaldirection = ERROR
    for i in xrange(4):
        if canmove(snake[HEAD],direction[i]) and board[snake[HEAD]+direction[i]]<short:
            short = board[snake[HEAD]+direction[i]]
            finaldirection = direction[i]
    return finaldirection

def  new_food():
    global WIDTH,HEIGHT,foodindex,snake,board
    flag = True
    while flag:
        w = randint(1, WIDTH-2)
        h = randint(1, HEIGHT-2)
        foodindex = h * WIDTH + w
        if not (foodindex in snake[:size]):
            flag = False
    win.addch(foodindex/WIDTH, foodindex%WIDTH, '.')

def moveto_nextstep(nextstep):
    global snake,board,size,pointsum,score
    for i in xrange(pointsum,0,-1):
        snake[i] = snake[i-1]
    snake[HEAD] += nextstep
    win.addch(snake[HEAD]/WIDTH, snake[HEAD]%WIDTH, '0')
    if board[snake[HEAD+1]+nextstep] == FOODMARK:
        board[foodindex] = SNAKEMARK
        size += 1
        score +=1
        if size < pointsum :
            new_food()
    else:
        board[snake[HEAD]] = SNAKEMARK
        board[snake[size]] = BLANKMARK
        win.addch(snake[size]/WIDTH, snake[size]%WIDTH, ' ')
        snake[size] = 0

curses.initscr()
win = curses.newwin(HEIGHT, WIDTH, 0, 0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)
win.addch(foodindex/WIDTH, foodindex%WIDTH, '.')

while key != 27:
    win.border(0)
    win.addstr(0, 2, 'S:' + str(score) + ' ')
    win.timeout(10)
    win.getch()

    board_reset(snake,foodindex,board)
    
    if Breadth_First_Search(snake,foodindex,board):
        nextstep=find_short_way(snake,board)
    else:
        print ERROR
    moveto_nextstep(nextstep)

curses.endwin()
