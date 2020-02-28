import copy
import sys
from random import randint

def find_zero(state):
    for y in range(0, len(state)):
        for x in range(0, len(state[y])):
            if state[y][x] == 0:
                return x, y
    return None

def move(direction, state):
    newstate = copy.deepcopy(state)
    pos = find_zero(newstate)
    posx = pos[0]
    posy = pos[1]
    if direction == "DOWN" and posy > 0:
        temp = newstate[posy - 1][posx]
        newstate[posy - 1][posx] = 0
        newstate[posy][posx] = temp
        return newstate
    elif direction == "UP" and posy < len(newstate) - 1:
        temp = newstate[posy + 1][posx]
        newstate[posy + 1][posx] = 0
        newstate[posy][posx] = temp
        return newstate
    elif direction == "RIGHT" and posx > 0:
        temp = newstate[posy][posx - 1]
        newstate[posy][posx - 1] = 0
        newstate[posy][posx] = temp
        return newstate
    elif direction == "LEFT" and posx < len(newstate[0]) - 1:
        temp = newstate[posy][posx + 1]
        newstate[posy][posx + 1] = 0
        newstate[posy][posx] = temp
        return newstate
    else:
        # Illegal move
        return None

def printstate(state):
    if state == None:
        print("Empty")
    else:
        for row in range(0, len(state)):
            s = ""
            for col in state[row]:
                s += str(col) + " "
            print(s.strip())

def testPls(n, input, solution):
    try:
        f = open(input, 'r')
    except IOError:
        raise IOError("Input file not found!")

    lines = f.readlines()

    # max_num = n to the power of 2 - 1
    max_num = n ** 2 - 1

    init_state = [[0 for i in range(n)] for j in range(n)]
    goal_state = [[0 for i in range(n)] for j in range(n)]

    i, j = 0, 0
    for line in lines:
        for number in line.split(" "):
            if number == '':
                continue
            value = int(number, base=10)
            if 0 <= value <= max_num:
                init_state[i][j] = value
                j += 1
                if j == n:
                    i += 1
                    j = 0

    if solution == ["UNSOLVABLE"]:
        return True

    # Instantiate a 2D list of size n x n
    goal_state = [[0 for i in range(n)] for j in range(n)]


    directions = ["RIGHT", "LEFT", "UP", "DOWN"]

    for i in range(1, max_num + 1):
        goal_state[(i - 1) // n][(i - 1) % n] = i
    goal_state[n - 1][n - 1] = 0

    new_state = init_state
    no_of_moves = 0
    for x in range(0, len(solution)):
        temp_state = move(solution[x], new_state)
        if temp_state is not None:
            no_of_moves = no_of_moves + 1
            new_state = temp_state

    return (new_state == goal_state)