import random
import math
from copy import copy, deepcopy
import sys
import time
import curses


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        return "("+str(self.x)+","+str(self.y)+")"

def printBoard(board, startPos = Pos(0,0)):
    for i in range(17):
        scr.addstr(startPos.y + i, startPos.x + 10, "|")
        scr.addstr(startPos.y + i, startPos.x + 22, "|")
    scr.addstr(startPos.y + 5, startPos.x,  "----------+-----------+----------")
    scr.addstr(startPos.y + 11, startPos.x, "----------+-----------+----------")

    for i in range(9):
        for j in range(9):
            scr.addstr(startPos.y + i * 2, startPos.x + j * 4, str(board[i][j]))

    scr.refresh()

def printProgressBar(prog, max, startPos = Pos(0,0), title=""):
    if max == 0: return
    barWidth = 33
    numBlocks = math.floor(barWidth * prog/max)
    bar = ""
    for i in range(numBlocks):
        bar += chr(9608)
    for i in range(barWidth-numBlocks):
        bar += '-'
    scr.addstr(startPos.y+1, startPos.x, bar)
    bar = title
    for i in range(33 - len(title)):
        bar += " "
    scr.addstr(startPos.y, startPos.x, bar)
    

tried = 0
total = 0
def findAnySolution(board, depth=1):
    global total
    global tried
    
    for i in range(9):
        for j in range(9):
            if board[i][j] == " ":
                options = validOptions(board, i, j)

                for choice in options:
                    newBoard = deepcopy(board)
                    newBoard[i][j] = choice

                    printBoard(newBoard, Pos(44,0))
                    tried += total/math.pow(9, depth)
                    printProgressBar(tried, total, Pos(44, 18), "Testing solvability...")

                    result = findAnySolution(newBoard, depth+1)
                    if result:
                        return True

                return False # Program reaches here if it finds a spot with no possibilities (unsolvable boardstate)
        
    return True # Program reaches here if the board is full.

seenBoardStates = []
def isNotUnique(board, depth=1):
    global solution
    global seenBoardStates
    global tried
    global total

    for i in range(9):
        for j in range(9):
            if board[i][j] == " ":

                options = validOptions(board, i, j)

                for choice in options:
                    
                    newBoard = deepcopy(board)
                    newBoard[i][j] = choice

                    if newBoard in seenBoardStates:
                        continue
                    seenBoardStates.append(newBoard)

                    printBoard(newBoard, Pos(44,0))
                    tried += total/math.pow(9, depth)
                    printProgressBar(tried, total, Pos(44, 18), "Testing for unique solution...")

                    result = isNotUnique(newBoard, depth+1)
                    if result:
                        return result
                
                return
    
    # Reaches here if board is full
    if board != solution: # If this solution is different to the first solution
        return board       # This board is not unique.

def numPossibilities(board):
    result = 1
    for i in range(9):
        for j in range(9):
            if board[i][j] == " ":
                result *= len(validOptions(board, i, j))
    return result

def validOptions(board, i, j):
    options = [1,2,3,4,5,6,7,8,9]
    # Row and Col
    for n in range(9):
        num = board[i][n]
        if num in options:
            options.remove(num)
        num = board[n][j]
        if num in options:
            options.remove(num)
    # Box
    boxX = math.floor(i/3)
    boxY = math.floor(j/3)
    for x in range(3*boxX, 3*(boxX+1)):
        for y in range(3*boxY, 3*(boxY+1)):
            num = board[x][y]
            if num in options:
                options.remove(num)
    
    return options
            
def isValid(board):
    for i in range(9):
        for j in range(9):
            num = board[i][j]
            if num == " ":
                continue
            
            # Row and Col
            for n in range(9):
                if board[i][n] == num and n != j:
                    # print("invalid", num, "in row", i, "col", n)
                    return False
                if board[n][j] == num and n != i:
                    # print("invalid", num, "on row", n, "col", j)
                    return False
             
            # Box
            boxX = math.floor(i/3)
            boxY = math.floor(j/3)
            for x in range(3*boxX, 3*boxX + 3):
                for y in range(3*boxY, 3*boxY + 3):
                    if board[x][y] == num and not (x == i and y == j):
                        # print("invalid", num, "in box", boxX, boxY)
                        return False
    # print("valid board!")
    return True

def isFull(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == " ":
                return False
    return True        

def generate():
    grid = []
    allPositions = []
    for i in range(9):
        grid.append([])
        for j in range(9):
            grid[i].append(" ")
            allPositions.append(Pos(i, j))
    random.shuffle(allPositions)

    global total
    global tried
    i = 0
    while len(allPositions) > 0:
        pos = random.choice(allPositions)
        options = validOptions(grid, pos.x, pos.y)
        grid[pos.x][pos.y] = random.choice(options)
        printBoard(grid)
        printProgressBar(i, 81, Pos(0, 18), "Generating. Filled: " + str(i) + "/81")

        total = numPossibilities(grid)
        tried = 0
        if findAnySolution(grid):
            allPositions.remove(pos)
            i += 1
        else:
            grid[pos.x][pos.y] = " "
    
    return grid

def reduce(board):
    allPositions = []
    for i in range(9):
        for j in range(9):
            allPositions.append(Pos(i, j))
    random.shuffle(allPositions)

    global solution
    global seenBoardStates
    global tried
    global total
    i = 0
    for pos in allPositions:
        numRemoved = board[pos.x][pos.y]
        board[pos.x][pos.y] = " "
        # logs.write("Removing " + str(numRemoved) + " from position " + str(pos))
        printBoard(board)
        printProgressBar(i, 81, Pos(0, 18), "Reducing. Checked: " + str(i) + "/81")
        i += 1

        tried = 0
        total = numPossibilities(board)
        seenBoardStates = []
        newSolution = isNotUnique(board)
        if newSolution:
            # logs.write('Invalid board. Putting back.\n')
            board[pos.x][pos.y] = numRemoved
        # else:
        #     logs.write('Board still valid.\n')

    printProgressBar(81, 81, Pos(0,18), "Reducing. Done!")

    
    return board
    
def boardToString(board):
    result = ""
    for i in range(9):
        for j in range(9):
            result += str(board[i][j])
            if j == 2 or j == 5:
                result += " | "
            else:
                result += "   "
        result += "\n"
        if i == 2 or i == 5:
            result += "----------+-----------+----------"
        elif i != 8:
            result += "          |           |          "
        result += '\n'
    return result


scr = curses.initscr()
scr.clear()
logs = open('./logs.txt', 'w')

fullValidBoard = generate()
solution = deepcopy(fullValidBoard)

reducedBoard = reduce(fullValidBoard)

printBoard(reducedBoard, Pos(88, 0))
logs.write("\n\nReduced Board:\n")
logs.write(boardToString(reducedBoard))

# newSolution = isNotUnique(reducedBoard)
# if newSolution:
#     logs.write("Not Unique!\n")
#     logs.write(boardToString(solution))
#     logs.write(boardToString(newSolution))
# else:

logs.write("Unique Solution:\n")
logs.write(boardToString(solution))
logs.close()