import tensorflow as tf
import matplotlib.pyplot as plt
import csv
import random
import numpy as np
import random
import keras
import ast
from keras.models import Sequential, load_model
from keras.layers import Activation, Dense
from keras import losses
from keras.utils import plot_model
modelWin = Sequential()
modelWin.add(Dense(81, activation='relu', input_dim=9))
modelWin.add(Dense(9, activation='softmax'))
modelWin.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

def checkWin(board):
    winList=["012","345","678","036","147","258","048","246"]
    for x in winList:
        if ((board[int(x[0])] == board[int(x[1])] and board[int(x[1])] == board[int(x[2])]) and board[int(x[0])]!=0):
            return 1
    if 0 not in board :
        return 2
    return 0

def nextMoveTie(boards):
    board = boards[-1]
    predict = modelWin.predict(np.array([board]))
    nextMove = np.argmax(predict)
    if random.choice(range(5)) == 0:
        nextMove = randMove(board)
    while board[nextMove] != 0:
        predict[0][nextMove]-=1
        nextMove=np.argmax(predict)
    nextPlayer = 0
    nextBoard = list(board)
    for x in board:
        nextPlayer+=int(x)
    nextBoard[nextMove] = 1 if nextPlayer == 0 else -1
    boards.append(nextBoard)
    ended = checkWin(nextBoard)
    if ended == 2 or ended == 1:
        return (boards,calRewardsWL(boards),calRewardsTie(boards))
    return nextMoveWL(boards)

def nextMoveWL(boards):
    board = boards[-1]
    predict = modelWin.predict(np.array([board]))
    nextMove = np.argmax(predict)
    '''if random.choice(range(20)) == 0:
        nextMove = randMove(board)
    if random.choice(range(75)) == 0:
        print_board(board)
        nextMove = int(input('Enter number: '))-1'''
    while board[nextMove] != 0:
        predict[0][nextMove]-=1
        nextMove=np.argmax(predict)
    nextPlayer = 0
    nextBoard = list(board)
    for x in board:
        nextPlayer+=int(x)
    nextBoard[nextMove] = 1 if nextPlayer == 0 else -1
    boards.append(nextBoard)
    ended = checkWin(nextBoard)
    if ended == 2 or ended == 1:
        return  (boards,calRewardsWL(boards),calRewardsTie(boards))
    return nextMoveTie(boards)

def randMove(x):
    taken = []
    for i,j in enumerate(x):
        if j !=0:
            taken.append(i)
    untaken = list()
    for x in range(9):
        if x not in taken:
            untaken.append(x)
    Selection = random.choice(untaken)
    return int(Selection)

def print_board(board):
    symbols = ['O',' ','X']
    board_plus1 = [int(x) + 1 for x in board]
    print(' ' + symbols[board_plus1[0]] + ' | ' + symbols[board_plus1[1]] + ' | ' + symbols[board_plus1[2]])
    print('___________')
    print(' ' + symbols[board_plus1[3]] + ' | ' + symbols[board_plus1[4]] + ' | ' + symbols[board_plus1[5]])
    print('___________')
    print(' ' + symbols[board_plus1[6]] + ' | ' + symbols[board_plus1[7]] + ' | ' + symbols[board_plus1[8]])
    print()

def moveOrd(boards):
    moves=[]
    for x in range(len(boards)-1):
        diff=np.subtract(boards[x+1],boards[x])
        for i,x in enumerate(diff):
            if x != 0:
                moves.append(i)
    return moves

def calRewardsWL(boards):
    boards = list(boards)
    moves = len(boards)-1
    movesOrd = moveOrd(boards)
    rDecay = 0.7
    winTie = checkWin(boards[-1])
    winner = sum(boards[-1])
    print(winner)
    rList = []
    if winTie == 1:
        reward = 5
    elif winTie == 2:
        reward = 0
    boards.pop()
    for i,j in enumerate(boards):
        currPlayer = sum(j)
        rMatrix = [0,0,0,0,0,0,0,0,0]
        if reward == 5:
            if currPlayer==winner:
                rMatrix[movesOrd[i]] = -1*reward*rDecay**(moves-i-1)
            else:
                rMatrix[movesOrd[i]] = reward*rDecay**(moves-i-1)
        else:
            rMatrix[movesOrd[i]] = reward*rDecay**(moves-i-1)
        rList.append(rMatrix)
    return rList

def calRewardsTie(boards):
    pass

for x in range(25000):
    board = [[0,0,0,0,0,0,0,0,0]]
    if x%2==1:
        boards,WL,tie = nextMoveTie(board)
    else:
        boards,WL, tie = nextMoveWL(board)
    if x%20==0:
        for y in boards:
            if y == boards[0]:
                continue
            print_board(y)
    _=boards.pop()
    boards,WL = np.array(boards),np.array(WL)
    modelWin.fit(boards,WL,validation_split=0.25, epochs=10, batch_size=16, verbose=0)
modelWin.save('Win.h5')