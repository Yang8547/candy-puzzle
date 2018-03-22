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



################################
# Delivery 2
################################

# node class
class Node:
    def __init__(self, value, parent, move):
        self.value = value
        self.parent = parent
        self.move = move
        self.H = 0
        self.G = 0
        self.F = 0


# function for find all children of the current accessed node
# search all possible move which is around ' ' in current node config
# find the correspond char in play board and the new config after choose the move action
# and then create new node for children node
def children(node):
    children = []
    currentIndex = np.where(node.value == ' ')
    currentPlayBoardChar = ''.join(playBoard[currentIndex])
    currentPlayBoardPos = ord(currentPlayBoardChar)

    # create new node for each possible movement add into a list
    for pm in potentialMove:
        childNode = None
        config = np.copy(node.value)
        move = chr(currentPlayBoardPos + pm)
        if (set([move,currentPlayBoardChar]) == set(['E','F'])):
            continue
        if (set([move, currentPlayBoardChar]) == set(['J', 'K'])):
            continue
        if np.any(playBoard == move):
            moveToIndex = np.where(playBoard == move)
            config[moveToIndex], config[currentIndex] = config[currentIndex], config[moveToIndex]
            childNode = Node(config, node, move)
            childNode.H = heuristic(config)
            childNode.G = node.G + 1
            childNode.F = childNode.H + childNode.G
            children.append(childNode)

    return children

# function to calculate the heuristic value of the config
# need to be improved in the next delivery
def heuristic(nodeValue):
    # the heuristic value is the number of different char in row 1 and row 3
    h = 0
    for i in range(5):
        if nodeValue[0, i] != nodeValue[2, i]:
            h += 1
    return h

# function to perform automatic mode
# we use Algorithm A* for search that will give us the shortest solution path to the goal
def autoMode():
    gameStep = 0

    for i in range(len(allIniConfig)):
        solutionPath = []  # list for record sequence of valid moves
        start = time.time()  # start timing

        openList = set()
        closeList = set()

        # load and display the initial play board for user
        print("candyBox:")
        iniConfig = allIniConfig.popleft()
        candyBox = loadInitialConfiguration(iniConfig)
        printCandyBox(candyBox)

        # the search root will be the node initial configuration
        searchRoot = Node(np.copy(candyBox), None, '')
        searchRoot.G = 0
        searchRoot.H = heuristic(searchRoot.value)
        searchRoot.F = searchRoot.H + searchRoot.G
        openList.add(searchRoot)

        # search loop
        while openList:
            current = min(openList, key=lambda x: x.F)
            candyBox = np.copy(current.value)

            # check if the current node is the goal state, if yes, find the solution path
            if checkWon(candyBox):
                end = time.time()
                timeElapsed = end - start

                # construct the solution path
                while current.parent != None:
                    solutionPath.insert(0, current)
                    current = current.parent
                solutionPath.insert(0, current)

                gameStep += len(solutionPath) - 1
                f = open('solutionPath.txt', 'a', newline='')
                print('length of close list: ', len(closeList))

                # in console print the configs and write the moves into the file
                for node in solutionPath:
                    printCandyBox(node.value)
                    f.write(node.move)
                f.write("\r\n" + format(timeElapsed * 1000) + "ms\r\n")
                f.close()
                print("Congratulations! You solved this puzzle!")
                break

            # remove the current node from open list and add it into close list
            openList.remove(current)
            closeList.add(current)

            # for the each child of current access node, check whether the config(state) is in the close list(ignore it) or in the open list
            # if it is in the open list, check the G value (is it the shortest path from start to n) if current g smaller than node.g in open list
            # update the g value and parent of the node in open list
            for node in children(current):
                inClose = False
                inOpen = False
                for closeNode in closeList:
                    if np.array_equal(closeNode.value, node.value):
                        inClose = True
                        break
                if inClose:
                    continue
                for openNode in openList:
                    if np.array_equal(openNode.value, node.value):
                        current_g = current.G + 1
                        if openNode.G > current_g:
                            openNode.G = current_g
                            openNode.F = openNode.G + openNode.H
                            openNode.move = node.move
                            openNode.parent = current
                        inOpen = True
                        break
                if inOpen == False:
                    openList.add(node)

    # record the total step fro solving all puzzles
    f = open('solutionPath.txt', 'a')
    f.write(format(gameStep))
    f.close()




# main game
# read all configuration from file
allIniConfig = readInput("inputs.txt")
mode = input("Please Manual Mode(M) OR Automatic Mode(A) M/A:")
mode = mode.upper()

if mode == 'M':
    manualMode()
else:
    autoMode()








