'''
COMP 472 Project Deliverable 1 Manual Mode
Author: Bochuan An 27878745  Yang An 27878699
'''
import numpy as np
import time
from collections import deque


playBoard = np.array([['A','B','C','D','E'],['F','G','H','I','J'],['K','L','M','N','O']])
# the potential move for each tile -1: move left. +1: move right. -5: move up. +5: move down
potentialMove = [-1, +1, -5, +5]


'''
read the configurations from file. Each configuration is an array and put these arrays in a queue
:param: file: the file name
'''
def readInput(file):
    series = deque()
    with open(file,'r') as f:
        for line in f:
           candy = line.split()
           series.append(candy)
    return series

'''
load one configuration and turn it into an 3*5 2d array
'''
def loadInitialConfiguration(configuration):
    configuration = [s.replace('e', ' ') for s in configuration]
    return np.array(configuration).reshape((3,5))

'''
print candy box 
'''
def printCandyBox(candyBox):
    for line in candyBox:
        print(line)
    print('===================')

'''
print play board
'''
def printPlayBoard():
    for line in playBoard:
        print(line)

'''
check goal state which is the top row is identical to the bottom
'''
def checkWon(candyBox):
    won = (candyBox[2] == candyBox[0]).all()
    return won

'''
check valid move and make movement
:param: move: a char ('A'-'O')
'''
def nextMove(move, candyBox, solutionPath):
    canMove = False # boolean represent whether it is a valid move
    currentPos = ord(move) # integer representing the char

    # if the move char is in the range of play board, get the index of the char in the playboard and check the element of candybox
    # which has the same index to see which move can that tile move
    if np.any(playBoard == move):
        currentIndex = np.where(playBoard == move)
        if candyBox[currentIndex] == ' ':
            print("Invalid move, please try again:")
        else:
            for pm in potentialMove:
                moveTo = chr(currentPos + pm)
                if np.any(playBoard == moveTo):
                    moveToIndex = np.where(playBoard == moveTo)
                    # if the moveTo tile is empty(valid move), swap the two tile and record the movement that user make
                    # print(candyBox[moveToIndex])
                    if candyBox[moveToIndex] == ' ':
                        candyBox[moveToIndex], candyBox[currentIndex] = candyBox[currentIndex], candyBox[moveToIndex]
                        solutionPath.append(move)
                        canMove = True
            if canMove == False:
                print("Invalid move, please try again:")
    else:
        print("Do not have this letter on the playBoard, please try again:")
    return canMove


def manualMode():
    gameStep = 1
    input("Please Press Any Key To Start The Game:")
    print("You will solve ", len(allIniConfig), "puzzles! Let's go! ")
    # main game loop until all configurations are completed
    for i in range(len(allIniConfig)):
        # list for record sequence of valid moves
        solutionPath = []
        # start timing
        start = time.time()
        # load and display the initial play board for user
        print("candyBox:")
        iniConfig = allIniConfig.popleft()
        candyBox = loadInitialConfiguration(iniConfig)
        printCandyBox(candyBox)
        print("====================")
        print("playBoard:")
        printPlayBoard()

        # game loop for each move
        while True:
            move = input("Please choose one letter from 'A' to 'O' to move: ")
            move = move.upper()
            canMove = nextMove(move, candyBox, solutionPath)
            # if make valid move print updated candy box and increment total number of moves
            if canMove == True:
                print("Game Steps:" + format(gameStep))
                print("candyBox:")
                printCandyBox(candyBox)

                print("====================")
                print("playBoard:")
                printPlayBoard()
                gameStep += 1
            # check goal state. If reach the goal state, stop the timer and write the sequence of moves to the output file
            if (checkWon(candyBox)):
                end = time.time()
                timeElapsed = end - start
                f = open('solutionPath.txt', 'a', newline='')
                print('solution path', solutionPath)
                for move in solutionPath:
                    f.write(move)
                f.write("\r\n" + format(timeElapsed * 1000) + "ms\r\n")
                f.close()
                print("Congratulations! You solved this puzzle!")
                break
    f = open('solutionPath.txt', 'a')
    f.write(format(gameStep - 1))
    f.close()


'''
Delivery 2
'''

def autoMode():
	# will be done in delivery 2
    return 0




# main game
# read all configuration from file
allIniConfig = readInput("inputs.txt")
mode = input("Please Manual Mode(M) OR Automatic Mode(A) M/A:")
mode = mode.upper()

if mode == 'M':
    manualMode()
else:
    autoMode()








