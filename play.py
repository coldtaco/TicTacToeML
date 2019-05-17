import numpy as np
from keras.models import Sequential, load_model
def checkWin(board):
    winList=["012","345","678","036","147","258","048","246"]
    for x in winList:
        if ((board[int(x[0])] == board[int(x[1])] and board[int(x[1])] == board[int(x[2])]) and board[int(x[0])]!=0):
            return board[int(x[0])]
    if 0 not in board :
        return 2
    return 0
model = load_model('Win.h5')
def nextMove(board):
    predict = model.predict(np.array([board]))
    nextMove = np.argmax(predict)
    while board[nextMove] != 0:
        predict[0][nextMove]-=1
        nextMove=np.argmax(predict)
    nextPlayer = 0
    nextBoard = list(board)
    for x in board:
        nextPlayer+=int(x)
    nextBoard[nextMove] = 1 if nextPlayer == 0 else -1
    return nextBoard
def print_board(board):
    symbols = ['O',' ','X']
    board_plus1 = [int(x) + 1 for x in board]
    print(' ' + symbols[board_plus1[0]] + ' | ' + symbols[board_plus1[1]] + ' | ' + symbols[board_plus1[2]])
    print('___________')
    print(' ' + symbols[board_plus1[3]] + ' | ' + symbols[board_plus1[4]] + ' | ' + symbols[board_plus1[5]])
    print('___________')
    print(' ' + symbols[board_plus1[6]] + ' | ' + symbols[board_plus1[7]] + ' | ' + symbols[board_plus1[8]])
    print()
def statusCheck(s):
    if s == 1:
        print("You win!")
    elif s==-1:
        print("You lose!")
    elif s==2:
        print("Tie!")
while True:
    ended = False
    status = 0
    board = [0,0,0,0,0,0,0,0,0]
    while not ended:
        taken = int(input("Next move? (1-9)"))-1
        board[taken]=1
        print_board(board)
        status=checkWin(board)
        if status != 0:
            statusCheck(status)
            break
        print("The computer goes:")
        board = nextMove(board)
        print_board(board)
        status=checkWin(board)
        if status != 0:
            statusCheck(status)
            break